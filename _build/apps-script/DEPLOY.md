# Deploy the lead backend (Google Apps Script → "MedicalBillingTeam Leads" Sheet)

The form posts to an Apps Script web app that appends one row per lead to the **Leads** tab of
https://docs.google.com/spreadsheets/d/1-6vsIf2-g_eHqXTy3Wb2JEEPIy7mfPEE-EYjTnXXVM4/edit
and emails an alert to **tony@altfunding.com only**. Supabase is not used.

Bots don't sign in to Google as Tony, so the deploy is Tony's one step.

## Tony's one step (about 2 minutes, signed in as tony@altfunding.com)

Open the Sheet, then **Extensions → Apps Script**. Replace everything in `Code.gs` with this repo's
`_build/apps-script/Code.gs` (Code Desk sends it as a paste-ready block), click **Save**, then
**Deploy → New deployment → gear icon → Web app** with:

| Setting | Value |
|---|---|
| Description | `medbill leads v1` |
| Execute as | **Me (tony@altfunding.com)** |
| Who has access | **Anyone** (required so the public form can POST without a Google login; nobody can read the sheet through it) |

Click **Deploy → Authorize access → tony@altfunding.com → Advanced → Go to (unsafe) → Allow**
(scopes: this spreadsheet, send email as you, script cache/lock). Copy the **Web app URL**
(`https://script.google.com/macros/s/…/exec`) and paste it to Code Desk in chat.

## What happens after (Code Desk)

1. Put the URL in `_build/config.json` → `form_backend.apps_script_url`. Nothing else changes.
2. `python3 _build/src/build.py` writes it into `/form-config.js` (`enabled` becomes true automatically). Commit + push.
3. Submit one test lead from the preview with `?mbt_test=1` (name `TEST - Code Desk`). Confirm the row lands with `is_test=true`
   and that **no** alert email is sent for it. Then one non-test row with Tony's okay to confirm the alert arrives, and mark it `status=test`.

**The URL is public by design.** The browser must know where to POST, so once set it is visible in `/form-config.js` on the
public site. It is not a secret. `form_key` (`mbt-public-v1`) is public too: a junk filter, not a credential. Abuse limits live in the
script: honeypot, minimum 3 s time-to-submit, form-key and form-id checks, select values must match the allowed lists, PHI-like text
rejected, 30 submissions per 10 minutes overall, same email at most once per 2 minutes, formula-injection guard.

Until the URL is set the form does not send anything and tells the visitor plainly: "Preview build: the form backend is not connected yet, so nothing was sent."
If the endpoint errors or its response can't be read, the visitor sees "Sorry, something went wrong. Please try again in a minute." The form never shows success unless the script confirms `{"ok":true}`.

## Sheet columns (Leads tab, row 1; already present)
`received_at, form_id, name, role, practice_name, specialty, num_providers, monthly_collections, billing_setup, help_areas, work_email, phone, tcpa_consent, tcpa_text_version, source_page, utm, user_agent, elapsed_ms, is_test, status`

## Test locally
`node _build/apps-script/test_code.js` (runs doPost's core `handle_` against stubbed Sheet/Mail/Cache).

## Revert
Apps Script → Deploy → Manage deployments → Archive. Set `form_backend.apps_script_url` to `""`, rebuild, push.
To stop alerts only: set `ALERT_ENABLED = false` in the script and Deploy → Manage deployments → Edit → New version.
