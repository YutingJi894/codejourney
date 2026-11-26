# CodeJourney 2.0
A full-stack LeetCode learning tracker: React, TypeScript, FastAPI and Supabase PostgreSQL. User-scoped progress is stored as JSONB with row-level security. Python solutions are stored as text, not executed.

## Setup
1. Create a Supabase project. Run `backend/schema.sql` once in SQL Editor. Enable email authentication. Copy project URL and public anon key (never the service role key).
2. Backend: `cd backend; python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt`. Set `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `FRONTEND_ORIGINS=http://localhost:5173` in your shell using export. Run `uvicorn main:app --reload`. API docs: http://localhost:8000/docs.
3. Frontend: `cd frontend; cp .env.example .env.local`. Fill the public Supabase values and API URL. Run `npm install` then `npm run dev`. Open http://localhost:5173.

## Deploy
- Export your old site's backup before replacing it. Copy this project's files into your existing repository root; remove the old root index.html after backup. Commit and push.
- Render: create a Python Web Service from the repository. Root directory `backend`, build `pip install -r requirements.txt`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Set SUPABASE_URL, SUPABASE_ANON_KEY, FRONTEND_ORIGINS (your exact Vercel production origin, no trailing slash). Copy the HTTPS service URL.
- Vercel: existing project Settings, root directory `frontend`, framework Vite, build `npm run build`, output `dist`. Set VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY, VITE_API_URL (Render URL, no trailing slash). Redeploy. In Supabase Auth URL configuration set Site URL to your production Vercel URL and add localhost for development if needed.
- Sign up, confirm email, sign in, import old backup from Backup page. Check that saved records persist after refresh and on another browser.

## Limitations
Whole-document saves use last-write-wins; avoid editing simultaneously on multiple devices. No Python execution, AI tutor, or syntax highlighting. No production deployment or end-to-end test has been performed. Hosting plan limits and availability may vary.
