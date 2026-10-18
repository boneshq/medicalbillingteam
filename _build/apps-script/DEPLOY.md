# Deploy the Sheet backend (Apps Script). Tony, about 3 minutes, in his own browser as tony@altfunding.com

Bots never sign in to Google in the box browser, so these clicks are Tony's.

1. Open the Sheet: https://docs.google.com/spreadsheets/d/1-6vsIf2-g_eHqXTy3Wb2JEEPIy7mfPEE-EYjTnXXVM4/edit
2. **Extensions → Apps Script.** Delete the stub and paste all of `_build/apps-script/Code.gs`. Save.
3. **Deploy → New deployment →** gear → **Web app**.
   - Description: `medbill leads v1`
   - Execute as: **Me (tony@altfunding.com)**
   - Who has access: **Anyone**. This is required so the public form can POST without a Google login. Nobody can read the sheet through it.
4. Click **Deploy**, then **Authorize access**. Choose tony@altfunding.com, then Advanced → Go to (unsafe) → Allow. That covers Sheets plus, only if the alert is on, send-mail.
5. Copy the **Web app URL** (`https://script.google.com/macros/s/…/exec`) and give it to Code Desk.
6. Code Desk then sets `_build/config.json`: `"form_backend": {"mode": "apps_script", "enabled": true, "apps_script_url": "<URL>"}`, rebuilds, pushes, and sends one TEST submission (`?mbt_test=1`, name "TEST - Code Desk") to confirm the row lands.

Email alert: `ALERT_ENABLED = false` by default. When it's on, it emails tony@altfunding.com only, never for `is_test` rows, and never includes lead details.
Revert: Apps Script → Deploy → Manage deployments → Archive. Set `form_backend.enabled=false` and push.
