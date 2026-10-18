# medicalbillingteam.com: prepared DNS, GSC and cutover (NOTHING APPLIED)

Prepared 2026-10-18 by Code Desk. Every step below is gated on **Tony's okay via CEO**.
Registrar/DNS: GoDaddy (Tony's account). NS stay `ns19/ns20.domaincontrol.com`. No Cloudflare.

## Current state (read via DNS-over-HTTPS, 2026-10-18 ~12:05 PM ET)
| Name | Type | Value |
|---|---|---|
| medicalbillingteam.com | A | 15.197.148.33, 3.33.130.190 (GoDaddy parking) |
| www.medicalbillingteam.com | CNAME | medicalbillingteam.com |
| medicalbillingteam.com | TXT, MX, AAAA | none |
| medicalbillingadvisor.com | NS / A | ns23/ns24.domaincontrol.com / 13.248.213.45, 76.223.67.189 (GoDaddy parking; still in the auction-transfer queue) |

## 1. Apex + www → GitHub Pages (replace the parking records)
| Host | Type | Value | TTL |
|---|---|---|---|
| @ | A | 185.199.108.153 | 600 |
| @ | A | 185.199.109.153 | 600 |
| @ | A | 185.199.110.153 | 600 |
| @ | A | 185.199.111.153 | 600 |
| @ | AAAA (optional) | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153 | 600 |
| www | CNAME | boneshq.github.io | 3600 |
Delete: `@ A 15.197.148.33`, `@ A 3.33.130.190`, and the `www CNAME medicalbillingteam.com`, which gets replaced.

Optional anti-takeover (recommended): GitHub → boneshq org/user Settings → Pages → Add a verified domain → `medicalbillingteam.com`. GitHub then shows a TXT record:
| _github-pages-challenge-boneshq | TXT | `<value GitHub shows>` |

## 2. GSC domain property (sc-domain:medicalbillingteam.com)
| Host | Type | Value |
|---|---|---|
| @ | TXT | `google-site-verification=<token>` |
The token only exists once someone starts adding the property in GSC (Tony: Search Console → Add property → Domain → medicalbillingteam.com → copy the TXT). Code Desk didn't create the property, per CEO. Alternative after cutover is the MSD pattern: an HTML-file verification at the repo root.
After it's verified, Tony adds `claude-gtm-manager@openclaw-email-486619.iam.gserviceaccount.com` as **Full** (Settings → Users and permissions).

## 3. Cutover runbook (after Tony's okay)
1. Repo: `echo medicalbillingteam.com > CNAME`. In `_build/config.json` set `"preview_base_path": ""`. Set `"indexing_enabled": true` only if Tony also okays indexing. Then `python3 _build/src/build.py && git add -A && git commit -m "cutover" && git push`.
2. `gh api -X PUT repos/boneshq/medicalbillingteam/pages -f cname=medicalbillingteam.com`
3. GoDaddy DNS (box; token loaded from 1Password into the subprocess env only):
   ```
   export GDDY_PAT="$(op item get fvs6b25xlenuz6l6jn3o2yeju4 --vault Avva --fields credential --reveal)"
   curl -s -X PUT "https://api.godaddy.com/v1/domains/medicalbillingteam.com/records/A/@" -H "Authorization: Bearer $GDDY_PAT" -H 'Content-Type: application/json' \
     -d '[{"data":"185.199.108.153","ttl":600},{"data":"185.199.109.153","ttl":600},{"data":"185.199.110.153","ttl":600},{"data":"185.199.111.153","ttl":600}]'
   curl -s -X PUT "https://api.godaddy.com/v1/domains/medicalbillingteam.com/records/CNAME/www" -H "Authorization: Bearer $GDDY_PAT" -H 'Content-Type: application/json' \
     -d '[{"data":"boneshq.github.io","ttl":3600}]'
   ```
   (Bearer PAT, same as the GoDaddy Domain Inventory refresh command; or use `~/.local/bin/gddy`.)
4. Wait for the certificate (minutes to about an hour), then `gh api -X PUT repos/boneshq/medicalbillingteam/pages -F https_enforced=true`.
5. Verify: `curl -sI https://medicalbillingteam.com/` → 200 `server: GitHub.com`; `curl -sI https://www.medicalbillingteam.com/` → 301 to the apex.
6. GSC TXT (section 2), then **sitemap submit via the SA**. That's a gated write, so Tony's go is needed (the skill marks sitemap submits off-limits without it):
   ```
   python3 /workspace/gsc/gsc.py   # gated sitemap submit; see its README: site sc-domain:medicalbillingteam.com, sitemap https://medicalbillingteam.com/sitemap.xml
   lvny-analytics gsc-sitemaps --site sc-domain:medicalbillingteam.com   # read back
   ```
7. GA4: Tony creates a web stream (Alternative Funding GA4 account, like MSD and AltFi) and gives the SA Viewer. Put the `G-…` ID in `_build/config.json` `ga4_measurement_id`, rebuild and push. Mark `generate_lead` as a key event (form.js fires it with `form_id` only, no field values).

**Revert:** restore the A records 15.197.148.33 and 3.33.130.190 and `www CNAME medicalbillingteam.com`; delete CNAME from the repo; `gh api -X DELETE repos/boneshq/medicalbillingteam/pages` if you also want Pages off.

## 4. medicalbillingadvisor.com → 301 (later, after the transfer lands in Tony's account and Tony's okay)
- Preferred (free): GoDaddy **Domain Forwarding**: Forward to `https://medicalbillingteam.com`, **Permanent (301)**, "Forward only" (no masking), and also forward `www`. GoDaddy sets its own forwarding A records.
- Alternative: point it to a tiny second GitHub Pages repo whose 404/index does a meta-refresh. This is weaker than a real 301, so not recommended.
- The About page copy says "medicalbillingadvisor.com redirects to this site". That isn't true yet, so remove the line or keep it only once the forward is live.
