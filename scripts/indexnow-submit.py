#!/usr/bin/env python3
"""Submit medicalbillingteam.com URLs to IndexNow (Bing, Yandex, Seznam, Naver share submissions).

The key is public by design: build.py serves it at https://<host>/<key>.txt from
_build/config.json `indexnow_key`. No secrets are involved. Standard library only.

Usage:
  python3 scripts/indexnow-submit.py --all                 every URL in the LIVE sitemap
  python3 scripts/indexnow-submit.py --since <git-sha>     pages whose HTML changed since <sha> (default HEAD~1)
  python3 scripts/indexnow-submit.py URL [URL ...]         specific URLs (must be in the live sitemap)
  add --dry-run to print what would be sent without submitting.

Only URLs listed in the live sitemap are ever submitted, so noindex pages (/thank-you/, /404.html)
are excluded automatically. Exit code is non-zero if the key file is not live or IndexNow rejects the batch.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = 'https://api.indexnow.org/indexnow'
UA = 'mbt-indexnow/1.0 (+https://medicalbillingteam.com/)'


def fetch(url, tries=1, wait=20):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            last = (e.code, e.read().decode('utf-8', 'replace'))
        except urllib.error.URLError as e:
            last = (0, str(e.reason))
        if i + 1 < tries: time.sleep(wait)
    return last


def changed_urls(base, since):
    out = subprocess.run(['git', '-C', str(ROOT), 'diff', '--name-only', f'{since}', 'HEAD'],
                         capture_output=True, text=True, check=True).stdout.split()
    urls = []
    for f in out:
        if f == 'index.html': urls.append(base + '/')
        elif f.endswith('/index.html') and not f.startswith(('_', '.', 'docs/', 'scripts/')):
            urls.append(f'{base}/{f[:-len("index.html")]}')
    return urls


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('urls', nargs='*')
    ap.add_argument('--all', action='store_true', help='submit every URL in the live sitemap')
    ap.add_argument('--since', default='HEAD~1', help='git revision to diff against for changed pages (default HEAD~1)')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    cfg = json.loads((ROOT / '_build' / 'config.json').read_text(encoding='utf-8'))
    key = str(cfg.get('indexnow_key') or '').strip()
    if not re.fullmatch(r'[a-f0-9]{32}', key): sys.exit('indexnow_key missing or malformed in _build/config.json')
    host = (ROOT / 'CNAME').read_text(encoding='utf-8').strip()
    base = f'https://{host}'

    st, body = fetch(f'{base}/sitemap.xml', tries=3)
    if st != 200: sys.exit(f'live sitemap not reachable: HTTP {st}')
    in_sitemap = re.findall(r'<loc>([^<]+)</loc>', body)
    allowed = set(in_sitemap)

    if a.all: want = in_sitemap
    elif a.urls: want = a.urls
    else: want = changed_urls(base, a.since)
    urls = list(dict.fromkeys(u for u in want if u in allowed))
    skipped = [u for u in want if u not in allowed]
    if skipped: print(f'skipped (not in live sitemap): {skipped}')
    if not urls:
        print('nothing to submit (no changed public pages)')
        return
    print(f'{len(urls)} URL(s):'); [print('  ' + u) for u in urls]

    key_url = f'{base}/{key}.txt'
    st, body = fetch(key_url, tries=10, wait=30)   # Pages + CDN can lag a deploy by a few minutes
    if st != 200 or body.strip() != key: sys.exit(f'key file not live at {key_url} (HTTP {st}); not submitting')
    print(f'key file live: {key_url}')
    if a.dry_run:
        print('dry run: not submitted'); return

    payload = json.dumps({'host': host, 'key': key, 'keyLocation': key_url, 'urlList': urls[:10000]}).encode()
    req = urllib.request.Request(ENDPOINT, data=payload, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code, text = r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        code, text = e.code, e.read().decode('utf-8', 'replace')
    print(f'IndexNow HTTP {code} {text[:300]}'.rstrip())
    if code not in (200, 202): sys.exit(1)


if __name__ == '__main__':
    main()
