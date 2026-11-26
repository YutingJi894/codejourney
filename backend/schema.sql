create table if not exists public.progress (
 user_id uuid primary key references auth.users(id) on delete cascade,
 data jsonb not null default '{}'::jsonb
);
alter table public.progress enable row level security;
create policy "Read own progress" on public.progress for select to authenticated using (auth.uid() = user_id);
create policy "Insert own progress" on public.progress for insert to authenticated with check (auth.uid() = user_id);
create policy "Update own progress" on public.progress for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
grant select, insert, update on public.progress to authenticated;
