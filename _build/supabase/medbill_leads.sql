-- medicalbillingteam.com lead store (MSD pattern: anon may INSERT only; no SELECT/UPDATE/DELETE).
-- NOT APPLIED. Needs Tony's go + an admin path (Supabase SQL editor as project owner, or a sanctioned migration).
-- Target project: the existing MSD project (ref fhbczvfrsgkbpvammxip), or a new FREE-tier project.
-- Non-PHI fields only. No free-text field exists on purpose.

create table if not exists public.medbill_leads (
  id                  uuid primary key default gen_random_uuid(),
  created_at          timestamptz not null default now(),
  site                text not null default 'medicalbillingteam' check (site = 'medicalbillingteam'),
  form_id             text not null check (form_id in ('hero','full','footer','checklist')),
  name                text not null check (char_length(name) between 1 and 100),
  role                text check (role is null or char_length(role) <= 80),
  practice_name       text not null check (char_length(practice_name) between 1 and 150),
  specialty           text check (specialty is null or char_length(specialty) <= 80),
  num_providers       text check (num_providers is null or char_length(num_providers) <= 40),
  monthly_collections text check (monthly_collections is null or char_length(monthly_collections) <= 40),
  billing_setup       text check (billing_setup is null or char_length(billing_setup) <= 80),
  help_areas          text[] not null default '{}' check (cardinality(help_areas) <= 12),
  work_email          text not null check (char_length(work_email) <= 150 and work_email ~* '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$'),
  phone               text check (phone is null or phone ~ '^[0-9()+.\- ]{7,30}$'),
  tcpa_consent        boolean not null default false,
  tcpa_text_version   text check (tcpa_text_version is null or char_length(tcpa_text_version) <= 40),
  source_page         text check (source_page is null or char_length(source_page) <= 500),
  utm                 jsonb not null default '{}'::jsonb check (pg_column_size(utm) < 2000),
  user_agent          text check (user_agent is null or char_length(user_agent) <= 300),
  elapsed_ms          integer check (elapsed_ms is null or elapsed_ms >= 0),
  is_test             boolean not null default false,
  tcpa_consent_at     timestamptz,
  phi_flag            boolean not null default false,
  status              text not null default 'new'
);

alter table public.medbill_leads enable row level security;
alter table public.medbill_leads force row level security;

-- Default deny, then allow exactly one thing: anonymous INSERT of a well-formed row.
revoke all on public.medbill_leads from anon, authenticated;
grant insert (site, form_id, name, role, practice_name, specialty, num_providers, monthly_collections, billing_setup,
              help_areas, work_email, phone, tcpa_consent, tcpa_text_version, source_page, utm, user_agent,
              elapsed_ms, is_test)
  on public.medbill_leads to anon;

drop policy if exists "anon insert medbill leads" on public.medbill_leads;
create policy "anon insert medbill leads" on public.medbill_leads
  for insert to anon
  with check (
    status = 'new'
    and (elapsed_ms is null or elapsed_ms >= 3000)            -- server-side min time-to-submit
    and (tcpa_consent = false or (phone is not null and tcpa_text_version is not null))
  );
-- No SELECT/UPDATE/DELETE policies: anon cannot read or change rows. Reads happen with the
-- service role from a trusted place only (never in the browser, never committed).

create index if not exists medbill_leads_created_at_idx on public.medbill_leads (created_at desc);
create index if not exists medbill_leads_email_idx on public.medbill_leads (work_email, created_at desc);

-- Server-side hygiene (runs as table owner): consent timestamp, PHI-pattern flag, simple per-email rate limit.
create or replace function public.medbill_leads_before_insert() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.created_at := now();
  new.status := 'new';
  new.tcpa_consent_at := case when new.tcpa_consent then now() else null end;
  if coalesce(new.name,'') || ' ' || coalesce(new.practice_name,'') ~ '(\m(0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])[/-](19|20)[0-9]{2}\M)|([0-9]{9,})' then
    new.phi_flag := true;            -- looks like a DOB or member/claim ID: flag for scrub per plan §11
  end if;
  if (select count(*) from public.medbill_leads where work_email = new.work_email and created_at > now() - interval '1 hour') >= 5 then
    raise exception 'rate limited';
  end if;
  return new;
end $$;
drop trigger if exists medbill_leads_bi on public.medbill_leads;
create trigger medbill_leads_bi before insert on public.medbill_leads
  for each row execute function public.medbill_leads_before_insert();

-- Verify after applying (as anon, from the box):
--   curl -s -o /dev/null -w '%{http_code}\n' -X POST "$SUPABASE_URL/rest/v1/medbill_leads" \
--     -H "apikey: $ANON" -H "Authorization: Bearer $ANON" -H 'Content-Type: application/json' -H 'Prefer: return=minimal' \
--     -d '{"form_id":"full","name":"TEST - Code Desk","practice_name":"TEST PRACTICE","work_email":"test@example.com","elapsed_ms":5000,"is_test":true}'
--   -> 201
--   curl -s "$SUPABASE_URL/rest/v1/medbill_leads?select=id" -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
--   -> 401/permission denied (anon cannot read)
-- Lead alert (NOT WIRED; needs Tony's go + a Supabase Database Webhook or Edge Function and a mail-sending secret,
-- none of which exist through a sanctioned, already-configured path on the box):
--   Database Webhook on INSERT into public.medbill_leads -> Edge Function `medbill-lead-alert` that emails ONLY
--   tony@altfunding.com ("New MedicalBillingTeam lead (<form_id>)" + link to the Supabase table view; no lead
--   details in the email body), and skips rows where is_test = true. The secrets it needs (mail API key or SMTP creds)
--   live only in Supabase function secrets, never in this repo. Recipient list is hard-coded to tony@altfunding.com.
-- Revert: drop trigger medbill_leads_bi on public.medbill_leads; drop function public.medbill_leads_before_insert(); drop table public.medbill_leads;
