import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
app = FastAPI(title='CodeJourney API')
app.add_middleware(CORSMiddleware, allow_origins=os.getenv('FRONTEND_ORIGINS','http://localhost:5173').split(','), allow_methods=['GET','PUT'], allow_headers=['Authorization','Content-Type'])
class Progress(BaseModel):
    p: dict = Field(default_factory=dict)
    days: dict = Field(default_factory=dict)
    notes: dict = Field(default_factory=dict)
    code: dict = Field(default_factory=dict)
    complexity: dict = Field(default_factory=dict)
async def request(method, token, data=None):
    if not token or not token.startswith('Bearer '): raise HTTPException(401,'Sign in required')
    url=os.environ['SUPABASE_URL'].rstrip('/')
    headers={'apikey':os.environ['SUPABASE_ANON_KEY'],'Authorization':token}
    async with httpx.AsyncClient(timeout=15) as client:
        user=await client.get(url+'/auth/v1/user',headers=headers)
        if user.status_code!=200: raise HTTPException(401,'Invalid session')
        uid=user.json()['id']
        headers['Prefer']='resolution=merge-duplicates,return=representation'
        r=await client.request(method,url+'/rest/v1/progress',headers=headers,params={'user_id':'eq.'+uid} if method=='GET' else {'on_conflict':'user_id'},json={'user_id':uid,'data':data} if data is not None else None)
        if r.status_code>=400: raise HTTPException(502,'Database request failed')
        rows=r.json(); return rows[0]['data'] if rows else Progress().model_dump()
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/progress',response_model=Progress)
async def get_progress(authorization: str=Header(default='')): return await request('GET',authorization)
@app.put('/progress',response_model=Progress)
async def put_progress(progress:Progress,authorization:str=Header(default='')): return await request('POST',authorization,progress.model_dump())
