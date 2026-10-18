# medicalbillingteam.com

An unbranded informational resource site for US medical practices on medical billing and RCM staffing. Static HTML on **GitHub Pages** (main, /), the MSD pattern.

- **Preview:** https://boneshq.github.io/medicalbillingteam/ (every page `noindex,nofollow` until Tony okays indexing)
- **Canonical / production:** https://medicalbillingteam.com/ (DNS not cut over yet; see `docs/DNS-GSC-CUTOVER.md`)

## Build
```
_build/sync-content.sh            # pull copy from /workspace/alliance-global/medbill/site-content/
python3 _build/src/build.py       # writes the site to the repo root; prints live-ready vs stub pages
git add -A && git commit -m "..." && git push   # = deploy
```
No dependencies beyond Python 3 + PyYAML. No JS framework; one small `form.js`.

## Switches (`_build/config.json`)
- `indexing_enabled` (false): when false, every page carries `<meta name="robots" content="noindex,nofollow">`.
- `preview_base_path` ("/medicalbillingteam"): set to "" at the custom-domain cutover.
- `ga4_measurement_id`: placeholder until Tony creates the GA4 web stream.
- `form_backend`: `mode` supabase|apps_script, `enabled` (false until a backend exists). See `_build/supabase/medbill_leads.sql` and `_build/apps-script/`.

## Content rules
No fake reviews, testimonials, stats or claims. Every page shows the operator disclosure. Forms are non-PHI only, with a visible no-patient-information notice. Pages without real copy stay stubs.

`secret-scan` workflow + `scripts/sync-lane/secretscan.py` copied from boneshq/msd.
