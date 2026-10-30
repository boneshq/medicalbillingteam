# medicalbillingteam.com

An unbranded informational resource site for US medical practices on medical billing and RCM staffing. Static HTML on **GitHub Pages** (main, /), the MSD pattern.

**What gets published:** Pages runs Jekyll over the repo root, and `_config.yml` keeps internal files off the live site. `_build/`, `.github/`, `docs/`, `scripts/` and this README are never served. Don't add `.nojekyll`: it makes Pages publish every file in the repo. The `pages-check` workflow builds the site the way Pages does and fails a PR if an internal file would be published or a public file would change.

- **Production:** https://medicalbillingteam.com/ (live and indexable since the 2026-10-18 DNS/GSC cutover; record in `docs/DNS-GSC-CUTOVER.md`). `main` = production: merging deploys.
- **Preview:** none. https://boneshq.github.io/medicalbillingteam/ now 301s to the custom domain. Preview a change locally (`python -m http.server --directory .`) or in a PR (`pages-check` builds it the way Pages does).

## Build
```
_build/sync-content.sh            # pull copy from /workspace/alliance-global/medbill/site-content/
python3 _build/src/build.py       # writes the site to the repo root; prints live-ready vs stub pages
git add -A && git commit -m "..." && git push   # = deploy
```
No dependencies beyond Python 3 + PyYAML. No JS framework; one small `form.js`.

## Switches (`_build/config.json`)
- `indexing_enabled` (true since 2026-10-18): when false, every page carries `<meta name="robots" content="noindex,nofollow">`.
- `preview_base_path` ("" since the cutover): the GitHub Pages project-URL prefix for preview builds.
- `ga4_measurement_id`: G-C7EWRCM4TV (GA4 property 559449061).
- `form_backend`: the lead form posts to the Supabase Edge Function `mbt-lead` (project afg-reddit-geo), which writes the 'MedicalBillingTeam Leads' Sheet and emails tony@. The `mode` value is still `apps_script` for compatibility (same POST contract). The endpoint URL and `form_key` are public by design.
- `phone` (added 2026-10-30): `display` + `e164` render the call CTA (header, mobile menu, sticky bar, footer band, contact card, Organization schema). Both empty = no call CTA. `tel:` clicks fire GA4 `phone_call_click` with `cta_location`.
- `call_tracking.snippet`: CTM tracking/DNI script (account 601667), injected before `</body>` on every page when set.

## Content rules
No fake reviews, testimonials, stats or claims. Every page shows the operator disclosure. Forms are non-PHI only, with a visible no-patient-information notice. Pages without real copy stay stubs.

`secret-scan` workflow + `scripts/sync-lane/secretscan.py` copied from boneshq/msd.

## AI chat assistant (`chat` in `_build/config.json`)
- **Widget:** `_build/chat/chat.src.js` → `/chat.js` (vanilla JS, no dependencies). An inline loader in the footer injects it only after window `load` + `delay_ms` (8 s) + idle, so it doesn't affect first paint. Desktop gets a small teaser card; phones get a one-line pill next to a 48 px bubble (no takeover). Dismissing it sets `localStorage.mbt_chat_dismissed=1`, after which only the bubble shows. It shows the AI disclosure, the affiliation disclosure (`affiliation.short`), the form's `phi_notice`, and a "Schedule a consultation" mini-form (name, email, phone, optional practice, optional TCPA box, honeypot). GA4 `generate_lead` (`form_type: chat`) fires only after the backend confirms the lead, and no visitor text goes to analytics.
- **Flag:** `enabled: false` shows the widget only with `?mbt_chat=1` (it sticks for the tab; `?mbt_chat=0` clears it). `enabled: true` shows it to everyone. Rebuild after changing it.
- **Retrieval index:** `/chat-index.json` is regenerated from `llms-full.txt` on every build (one chunk per H2, link URLs dropped, `$` prices replaced with `[price omitted]`). The backend fetches it from the live site and caches it for 15 min, so content updates flow through without a redeploy.
- **Backend:** Supabase Edge Function `mbt-chat` in afg-reddit-geo (`https://tuolsdkjnzrtqmmzxvoq.supabase.co/functions/v1/mbt-chat`). The source is in the box kit `alliance-global/medbill/form-backend/supabase/functions/mbt-chat/`. Leads go through mbt-lead's core with `form_id=chat` (the same Sheet row shape), and each transcript is emailed to tony@altfunding.com only.
- **Model / provider switch (Supabase secrets only, no code change):** `LLM_BASE_URL` (any OpenAI-compatible `/v1`), `LLM_MODEL` and `LLM_API_KEY`, with an optional `LLM_FALLBACK_BASE_URL` / `LLM_FALLBACK_MODEL` / `LLM_FALLBACK_API_KEY` set. Knobs: `LLM_MAX_TOKENS`, `LLM_TEMPERATURE`, `LLM_TIMEOUT_MS`, `LLM_EXTRA_BODY` (JSON) and `LLM_REQUIRE_FREE` (`1` refuses any model id not ending in `:free`). To move to the Spark Qwen API later, set `LLM_BASE_URL=<spark vLLM>/v1`, `LLM_MODEL=<served qwen id>`, `LLM_API_KEY=<spark key>` and `LLM_REQUIRE_FREE=0`. The function also needs to be able to reach that URL from the internet.
