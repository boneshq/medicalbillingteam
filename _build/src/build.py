#!/usr/bin/env python3
"""Static build for medicalbillingteam.com -> writes the site to the REPO ROOT (GitHub Pages: main, /).

  python3 _build/src/build.py                  # preview build: links prefixed with /medicalbillingteam (GitHub Pages project URL)
  BASE_PATH= python3 _build/src/build.py       # custom-domain build (after CNAME cutover): root-relative links

Noindex switch: _build/config.json "indexing_enabled". While false, EVERY page ships
<meta name="robots" content="noindex,nofollow">. Flip to true only after Tony's okay."""
import json, os, re, shutil, html, datetime, pathlib, yaml
from pages import PAGES, NAV
from md import convert, front_matter, inline
from icons import ico

B = pathlib.Path(__file__).resolve().parent.parent      # _build/
ROOT = B.parent                                          # repo root = publish dir
CFG = json.loads((B / 'config.json').read_text())
BASE_PATH = os.environ.get('BASE_PATH', CFG['preview_base_path']).rstrip('/')
INDEX = bool(CFG.get('indexing_enabled'))
SITE = CFG['canonical_base'].rstrip('/')
TODAY = datetime.date.today().isoformat()
BYKEY = {p['key']: p for p in PAGES}
E = lambda s: html.escape(str(s or ''), quote=True)
DISC = CFG['disclosure']
AFF = CFG['affiliation']   # final wording: CODE-DESK-V2-SLOTS.md §4 (full / short / referral)
GALLERY = json.loads((B / 'ags-gallery.json').read_text()) if (B / 'ags-gallery.json').exists() else {}
ASSET_V = datetime.datetime.now().strftime('%Y%m%d%H%M')
BAA_Q = 'Does the operator of this site sign a BAA?'  # distinct from the vendor-page FAQ question
BAA_LINE = 'Alliance Global Solutions signs a BAA before any PHI access.'  # approved copy addition (Tony via Alliance Global, 2026-10-18); HIPAA page disclosure only
SPEC_SECTIONS = re.compile(r'^(short form|sticky cta|footer$|form fields|implementation notes|other ways to reach us|get the checklist)', re.I)
FAQ_HEAD = re.compile(r'^(short )?faq$', re.I)
BYLINE_RE = re.compile(r'^\*By the Medical Billing Team editors.*\*\s*$', re.M)
# Build-level copy override (Tony, 2026-10-18 1:31 PM ET): AGS location = "US-based management and admin; staff in the
# Philippines, Colombia and other countries". Applied to content, frontmatter (FAQ/schema), llms.txt and llms-full.txt so a
# content re-sync can't revert it; Alliance Global will fix the source. No office addresses. Build fails if the old wording returns.
COPY_FIXES = [
    ("Its staff are based in the Philippines and Colombia, and", "Its management and admin are US-based, its staff are in the Philippines, Colombia and other countries, and"),
    ("Its staff are based in the Philippines and Colombia.", "Its management and admin are US-based, and its staff are in the Philippines, Colombia and other countries."),
    ("- **Where staff are based:** the Philippines and Colombia", "- **Where staff are based:** US-based management and admin; staff in the Philippines, Colombia and other countries"),
    ("Staff work from the Philippines and Colombia.", "Management and admin are US-based; staff work from the Philippines, Colombia and other countries."),
    ("with dedicated staff in the Philippines and Colombia", "with US-based management and admin and dedicated staff in the Philippines, Colombia and other countries"),
    ("with staff in the Philippines and Colombia", "with US-based management and admin and staff in the Philippines, Colombia and other countries"),
    ("dedicated remote staff, based in the Philippines and Colombia, for roles", "dedicated remote staff, with US-based management and admin and staff in the Philippines, Colombia and other countries, for roles"),
    ("places remote billing and RCM staff from the Philippines.", "places remote billing and RCM staff from the Philippines, Colombia and other countries, with US-based management and admin."),
    ("provides remote staff based in the Philippines.", "provides remote staff based in the Philippines, Colombia and other countries, with US-based management and admin."),
    ("provides remote staff from the Philippines;", "provides remote staff from the Philippines, Colombia and other countries, with US-based management and admin;"),
    ("Alliance Global Solutions staff are based in the Philippines and Colombia;", "Alliance Global Solutions has US-based management and admin and staff in the Philippines, Colombia and other countries;"),
    ("including the Philippines and Colombia", "including the Philippines, Colombia and other countries"),
]
def fix_copy(s):
    for _a, _b in COPY_FIXES: s = s.replace(_a, _b)
    return s
LOC_OLD = re.compile(r'Philippines and Colombia|staff (?:from|based in) the Philippines[.;]')
CLAIM_RE = re.compile(r'\b(25|twenty[- ]five)\s*\+?\s*(-\s*)?(years?|yrs?)\b', re.I)   # no tenure claims anywhere (Tony via AG 2026-10-18)
BANNED = ['subcontractor business associate and signs a BAA with the billing company']  # unconfirmed claim (Tony via CEO 2026-10-18); build fails if it reappears
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
def human(d):
    y, m, dd = str(d).split('-'); return f'{MONTHS[int(m)-1]} {int(dd)}, {y}'

def load(p):
    f = B / 'content' / f"{p['key']}.md"
    p.update(ready=False, body='', sections=[], toc=[], faqs=[], raw='', meta={})
    if not f.exists(): return
    txt = f.read_text()
    for _a, _b in COPY_FIXES: txt = txt.replace(_a, _b)
    for b in BANNED:
        if b in txt: raise SystemExit(f'BLOCKED: unconfirmed claim in {f.name}: {b!r}')
    meta = {}
    if txt.startswith('---\n'):
        end = txt.find('\n---', 4)
        meta = yaml.safe_load(txt[4:end]) or {}
        txt = txt[end + 4:].lstrip('\n')
    p['meta'] = meta
    if str(meta.get('status', '')).lower() == 'stub' or not txt.strip(): return
    p['ready'] = True
    p['draft'] = 'DRAFT' in str(meta.get('status', '')).upper()
    p['slot'] = str(meta.get('copy_status', '')).lower() == 'slot'   # interim copy awaiting the 4 PM drop
    p['vendor'] = meta.get('vendor_slots') or meta.get('vendor') or {}
    p['steps'] = (p['vendor'].get('steps') if p['vendor'] else None) or meta.get('steps') or []
    p['images'] = meta.get('images') or []
    p['tech'] = meta.get('tech_section') or {}
    p['jsonld_extra'] = meta.get('jsonld') or ''
    p['gated'] = bool(meta.get('gated'))
    p['robots_fm'] = str(meta.get('robots') or '')
    p['date_published'] = str(meta.get('date_published') or '')
    p['date_modified'] = str(meta.get('date_modified') or p['date_published'])
    p['author'] = str(meta.get('author') or '')
    p['reviewer'] = str(meta.get('reviewer') or '').strip()
    if meta.get('pillar'):
        pk = [x['key'] for x in PAGES if x['path'] == meta['pillar']]
        if pk and pk[0] != p['key']: p['parent'] = pk[0]
    if meta.get('title'): p['title'] = meta['title']
    if meta.get('meta_description'): p['description'] = meta['meta_description']
    p['faqs'] = [(x['q'], x['a']) for x in (meta.get('faq') or []) if x.get('q') and x.get('a')]
    p['schema_types'] = meta.get('schema_type') or []
    # Approved copy addition (Tony via Alliance Global, 2026-10-18): BAA Q&A, visible + FAQPage JSON-LD, identical wording.
    if p['key'] in ('hipaa-outsourced-medical-billing', 'faq') and not any(q == BAA_Q for q, _ in p['faqs']):
        at = next((i + 1 for i, (q, _) in enumerate(p['faqs']) if 'BAA' in q or 'business associate agreement' in q), len(p['faqs']))
        p['faqs'].insert(at, (BAA_Q, BAA_LINE))
        if p['key'] == 'faq':   # /faq/ renders its body questions; insert the same Q&A after the BAA question
            txt = re.sub(r'(^###\s+Will the staffing provider sign a business associate agreement\?.*?)(?=^###\s)', lambda m: m.group(1) + f'### {BAA_Q}\n\n{BAA_LINE}\n\n', txt, count=1, flags=re.M | re.S)
    txt = re.sub(r'^>\s*\*\*DRAFT FOR LEGAL REVIEW\.\*\*.*$', '', txt, flags=re.M)   # template renders the draft banner
    m = re.search(r'^#\s+(.+)$', txt, re.M)
    if m: p['h1'] = m.group(1).strip(); txt = txt[:m.start()] + txt[m.end():]
    p['has_byline'] = bool(BYLINE_RE.search(txt))
    txt = BYLINE_RE.sub('', txt)                                             # template renders the byline from frontmatter
    txt = re.sub(r'^\*Disclosure:.*\*\s*$', '', txt, flags=re.M)          # footer carries it
    txt = re.sub(r'\n-{3,}\s*\n\*Affiliation disclosure:.*?\*\s*$', '\n', txt, flags=re.S)   # trailing short disclosure: footer carries it (#35)
    txt = re.sub(r'^\*Affiliation disclosure:.*\*\s*$', '', txt, flags=re.M)
    # component markers (survive comment stripping)
    txt = re.sub(r'<!--\s*IMAGE SLOT ([\w-]+).*?-->', r'<!--IMG:\1-->', txt, flags=re.S)
    txt = re.sub(r'<!--\s*VENDOR CARD.*?-->', '<!--VCARD-->', txt, flags=re.S)
    txt = re.sub(r'<!--\s*VENDOR TEASER.*?-->', '<!--VTEASER-->', txt, flags=re.S)
    txt = re.sub(r'<!--\s*LATEST-UPDATES.*?-->', '<!--UPDATES-->', txt, flags=re.S)
    txt = re.sub(r'<!--\s*HOME TEASER.*?-->', '<!--TEASER-->', txt, flags=re.S)
    txt = re.sub(r'<!--(?!(?:IMG:[\w-]+|VCARD|VTEASER|UPDATES|TEASER)-->).*?-->', '', txt, flags=re.S)   # build notes
    if p['tech']:   # #38: Technology section renders from frontmatter; body duplicate replaced by the component marker
        txt, n = re.subn(r'^## Technology\s*\n.*?(?=^## |\Z)', '<!--TECH-->\n\n', txt, count=1, flags=re.M | re.S)
        if not n: txt = re.sub(r'(^## Related guides)', '<!--TECH-->\n\n\\1', txt, count=1, flags=re.M)
    if p['key'] == 'medical-billing-technology':   # #39: latest updates come from _build/data/tech-updates.yml
        txt = re.sub(r'<!--UPDATES-->\s*(?:^- .*\n?)+', '<!--UPDATES-->\n\n', txt, flags=re.M)
    parts = re.split(r'^(?=##\s)', txt, flags=re.M)
    keep = []
    p['faq_head'] = None; p['faq_tail'] = ''
    for part in parts:
        hm = re.match(r'##\s+(.+)', part)
        if hm and (SPEC_SECTIONS.match(hm.group(1).strip()) or hm.group(1).strip() in CFG.get('hold_sections', {})): continue
        if hm and FAQ_HEAD.match(hm.group(1).strip()) and p['faqs'] and p['key'] != 'faq':
            # visible FAQ is rendered from frontmatter (single source); keep any non-Q&A tail lines
            rest = part[hm.end():]
            for q, a in p['faqs']:
                rest = re.sub(r'^###\s+' + re.escape(q) + r'\s*\n+' + re.escape(a) + r'\s*\n?', '', rest, flags=re.M)
            leftover = re.sub(r'^###\s+.*$', '', rest, flags=re.M)
            p['faq_head'] = hm.group(1).strip(); p['faq_tail'] = re.sub(r'\n-{3,}\s*$', '', leftover.strip())
            keep.append('<!--FAQ-->\n')
            continue
        keep.append(part)
    p['intro'] = keep[0] if keep and not keep[0].lstrip().startswith('##') else ''
    p['sections'] = [s for s in keep if s.lstrip().startswith('##') or s.startswith('<!--FAQ-->')]
    clean = '\n'.join(keep).strip()
    clean = re.sub(r'\n-{3,}\s*$', '', clean)
    p['raw'] = clean.replace('<!--FAQ-->', '').strip()
    p['body'], p['toc'] = convert(clean)
    if p['faq_head']:
        p['toc'].append((re.sub(r'[^a-z0-9]+', '-', p['faq_head'].lower()).strip('-'), p['faq_head']))

for p in PAGES:
    load(p)
    if p['kind'] in ('utility',): p['ready'] = True
    if p['key'] in CFG.get('held_pages', []): p['ready'] = False; p['held'] = True   # not published (go-live quality rule)
    if '<!--TECH-->' in p.get('body', ''):
        ids = [i for i, _ in p['toc']]
        at = ids.index('related-guides') if 'related-guides' in ids else len(p['toc'])
        p['toc'].insert(at, ('technology', 'Technology'))
    p['indexable'] = p['ready'] and p['kind'] != 'utility' and not p.get('draft') and not p.get('slot') and 'noindex' not in p.get('robots_fm', '')

# CODE-DESK #39: Technology "Latest updates" feed (append-only data file; only status: approved renders, newest first)
_uf = B / 'data' / 'tech-updates.yml'
UPDATES = sorted([x for x in (yaml.safe_load(_uf.read_text()) if _uf.exists() else []) or [] if str(x.get('status')) == 'approved'],
                 key=lambda x: str(x['date']), reverse=True)
for _x in UPDATES:
    for _k in ('date', 'headline', 'source_name', 'source_url'):
        if not _x.get(_k): raise SystemExit(f'tech-updates.yml: approved item missing {_k}: {_x}')
_hub = BYKEY['medical-billing-technology']
if UPDATES and str(UPDATES[0]['date']) > _hub.get('date_modified', ''): _hub['date_modified'] = str(UPDATES[0]['date'])   # bump on publish

def url(p): return SITE + p['path']

# ---------------- partials ----------------
def ga():
    gid = (CFG.get('ga4_measurement_id') or '').strip()
    if not re.fullmatch(r'G-[A-Z0-9]{4,}', gid) or 'XXXX' in gid: return ''   # renders nothing until Tony's measurement ID is set
    return ('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());'
            f'gtag("config","{gid}");(function(){{var d=0;function l(){{if(d)return;d=1;var s=document.createElement("script");s.async=1;'
            f's.src="https://www.googletagmanager.com/gtag/js?id={gid}";document.head.appendChild(s)}}'
            '["pointerdown","keydown","scroll","touchstart","focusin"].forEach(function(e){addEventListener(e,l,{once:1,passive:1})});'
            'addEventListener("load",function(){(window.requestIdleCallback||setTimeout)(l,{timeout:4000})})})()</script>')

# Home and featured-vendor FAQs must be different (each has its own FAQPage); fail the build on any shared question.
_norm = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
for _v in [x for x in PAGES if x['kind'] == 'vendor']:
    _dup = {_norm(q) for q, _ in BYKEY['index']['faqs']} & {_norm(q) for q, _ in _v['faqs']}
    if _dup: raise SystemExit(f'DUPLICATE FAQ between home and {_v["path"]}: {sorted(_dup)}')

AGS_ID = 'https://www.allianceglobalsolutions.com/#organization'
def jsonld(p):
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": CFG['site_name'], "url": SITE + "/",
           "logo": SITE + "/logo.svg", "description": DISC,
           "parentOrganization": {"@type": "Organization", "@id": AGS_ID, "name": "Alliance Global Solutions", "url": "https://www.allianceglobalsolutions.com/"}}
    site = {"@type": "WebSite", "@id": SITE + "/#website", "name": CFG['site_name'], "url": SITE + "/",
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"}
    g = [org, site]
    if p['key'] != 'index':
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
        if p['parent']:
            crumbs.append({"@type": "ListItem", "position": 2, "name": BYKEY[p['parent']]['label'], "item": url(BYKEY[p['parent']])})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": p['label'], "item": url(p)})
        g.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if p['ready'] and (p['kind'] in ('pillar', 'cluster') or 'Article' in p.get('schema_types', [])):
        g.append({"@type": "Article", "headline": p.get('h1', p['title'])[:110], "description": p['description'],
                  "mainEntityOfPage": url(p), "url": url(p), "inLanguage": "en-US",
                  "datePublished": p.get('date_published') or None, "dateModified": p.get('date_modified') or None,
                  "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}})
    st = [t for t in p.get('schema_types', []) if t in ('AboutPage', 'ContactPage', 'WebPage', 'CollectionPage', 'ProfilePage')]
    if st or p['kind'] in ('page', 'form', 'legal', 'directory', 'vendor'):
        g.append({"@type": st[0] if st else 'WebPage', "name": p['title'], "url": url(p), "description": p['description'],
                  "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}})
    if p['kind'] == 'vendor' and p['vendor']:
        g[-1]["mainEntity"] = {"@id": AGS_ID}
    if p['kind'] == 'directory':
        g[-1]["mainEntity"] = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": v['vendor']['name'], "url": url(v)}
                               for i, v in enumerate(x for x in PAGES if x['kind'] == 'vendor' and x['vendor'])]}
    if 'HowTo' in p.get('schema_types', []):
        steps = [(m.group(1), m.group(2)) for m in re.finditer(r'^##\s+Step\s+(\d+):\s*(.+)$', p['raw'], re.M)]
        if steps:
            g.append({"@type": "HowTo", "name": p.get('h1', p['title']), "step": [{"@type": "HowToStep", "position": int(n), "name": t} for n, t in steps]})
    if p['faqs'] and p['key'] != 'thank-you':   # FAQPage only mirrors the visible FAQ (rendered from the same frontmatter list)
        g.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                  "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faqs']]})
    g = [{k: v for k, v in x.items() if v is not None} for x in g]
    out = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + '</script>'
    for blk in [x for x in str(p.get('jsonld_extra') or '').splitlines() if x.strip()]:   # #36: Organization + Service from frontmatter
        if re.search(r'aggregateRating|"review"', blk): raise SystemExit(f'ratings/reviews not allowed in schema: {p["path"]}')
        out += '<script type="application/ld+json">' + json.dumps(json.loads(blk), ensure_ascii=False) + '</script>'
    return out

def head(p):
    robots = 'index, follow, max-image-preview:large' if (INDEX and p['indexable'] and not p.get('force_noindex')) else 'noindex, nofollow'
    title = p['title']
    og = SITE + '/og-default.jpg'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(p['description'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url(p)}">
<meta property="og:type" content="{'website' if p['key']=='index' else 'article'}">
<meta property="og:site_name" content="{E(CFG['site_name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(p['description'])}">
<meta property="og:url" content="{url(p)}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(p['description'])}">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="{E(CFG['site_name'])}: remote billing and RCM staffing, explained for US practices">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(CFG['site_name'])}: remote billing and RCM staffing, explained for US practices">
<meta name="theme-color" content="#0f2340">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/hankengrotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
{p.get('preload_img', '')}<link rel="stylesheet" href="/styles.css?v={ASSET_V}">
{jsonld(p)}
{ga()}
</head>'''

NAV_LBL = {'what-is-revenue-cycle-management': 'What is RCM', 'revenue-cycle-management-staffing': 'RCM Staffing',
  'credentialing-services': 'Credentialing', 'prior-authorization-specialist': 'Prior Authorization',
  'eligibility-verification-prior-authorization': 'Insurance Verification', 'treatment-center-vob': 'VOB for Treatment Centers',
  'hire-remote-medical-coders': 'Coding', 'ar-specialist': 'A/R', 'virtual-medical-assistant': 'Virtual Assistants',
  'virtual-medical-receptionist': 'Virtual Receptionists', 'denial-management': 'Denial Management',
  **{f'denial-code-co-{n}': f'CO-{n}' for n in (16, 22, 29, 97, 197, 204)}}

def nav(cur):
    def on(k): return cur == k or BYKEY[cur]['parent'] == k
    def a(lbl, k):
        return f'<li><a href="{BYKEY[k]["path"]}"{" aria-current=\"page\"" if on(k) else ""}>{E(lbl)}</a></li>'
    def item(lbl, v):
        if isinstance(v, str): return a(lbl, v) if BYKEY[v]['ready'] else ''
        sub = ''.join(a(NAV_LBL.get(k, BYKEY[k]['label']), k) for k in v if BYKEY[k]['ready'])
        act = ' class="on"' if any(on(k) for k in v) else ''
        return f'<li class="dd"><details><summary{act}>{E(lbl)}{ico("chevron-down", "ic chev")}</summary><ul class="dd-menu">{sub}</ul></details></li>'
    items = ''.join(item(l, v) for l, v in NAV)
    bar = '' if INDEX else '<div class="staging-bar">Preview build: not indexed.</div>'
    return f'''<body class="pg-{cur}">{bar}<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap hdr">
<a class="brand" href="/"><img src="/logo.svg" alt="" width="30" height="30"><span>Medical Billing <b>Team</b></span></a>
<nav class="nav-desk" aria-label="Main"><ul class="nav">{items}</ul></nav>
<a class="btn btn-sm hdr-cta" href="/contact/">Free assessment</a>
<details class="menu"><summary aria-label="Open menu"><span class="burger" aria-hidden="true"></span>Menu</summary><nav aria-label="Mobile"><ul class="nav">{items}<li><a class="m-cta" href="/contact/">Free assessment</a></li></ul></nav></details>
</div></header>'''

F = CFG['form']
def sel(name, label, opts, required=True):
    o = ''.join(f'<option>{E(x)}</option>' for x in opts)
    return f'<label><span>{E(label)}{"" if required else " <i>(optional)</i>"}</span><select name="{name}"{" required" if required else ""}><option value="">Select…</option>{o}</select></label>'
def inp(name, label, typ='text', required=True, ac='', hint='', maxl=150):
    h = f'<small>{E(hint)}</small>' if hint else ''
    return f'<label><span>{E(label)}{"" if required else " <i>(optional)</i>"}</span><input name="{name}" type="{typ}"{" required" if required else ""} maxlength="{maxl}"{f" autocomplete={chr(34)}{ac}{chr(34)}" if ac else ""}>{h}</label>'

def tcpa_links():
    l = [f'<a href="{BYKEY[k]["path"]}">{n}</a>' for k, n in (('privacy', 'Privacy Policy'), ('terms', 'Terms')) if BYKEY[k]['ready']]
    return f' See our {" and ".join(l)}.' if l else ''

FORM_ON = bool(CFG['form_backend'].get('apps_script_url'))   # flips to live automatically once apps_script_url is set

def form(form_id):
    full = form_id == 'full'
    name = inp('name', 'Your name', ac='name', maxl=100)
    practice = inp('practice_name', 'Practice or company name', ac='organization')
    provs = sel('num_providers', 'Number of providers', F['providers'])
    email = inp('work_email', 'Work email', 'email', ac='email', hint='Please use your practice or company email.')
    phone = inp('phone', 'Phone', 'tel', required=False, ac='tel', hint="Only if you'd like a call or text.", maxl=30)
    if full:   # contact.md field order 1-10
        top = [name, sel('role', 'Your role', F['roles']), practice, sel('specialty', 'Specialty', F['specialties']), provs,
               sel('monthly_collections', 'Monthly collections range', F['collections']), sel('billing_setup', 'Current billing setup', F['setups'])]
        boxes = ''.join(f'<label class="chip"><input type="checkbox" name="help_areas" value="{E(x)}"> {E(x)}</label>' for x in F['help_areas'])
        mid = f'<fieldset class="chips"><legend>Where do you need help? <i>(optional)</i></legend>{boxes}</fieldset>'
        bottom = [email, phone]
    else:      # index.md hero order: name, work email, practice, providers, phone
        top = [name, email, practice, provs, phone] if form_id == 'hero' else [name, practice, provs, email, phone]
        mid, bottom = '', []
    tcpa = (f'<label class="check tcpa" hidden><input type="checkbox" name="tcpa_consent" value="yes"> '
            f'<span>{E(CFG["tcpa_text"])}{tcpa_links()}</span></label>')
    grid2 = ' grid-2' if full else ''
    fields = f'<div class="grid{grid2}">{"".join(top)}</div>{mid}' + (f'<div class="grid{grid2}">{"".join(bottom)}</div>' if bottom else '')
    btn = 'Send me the checklist' if form_id == 'checklist' else 'Request my assessment'
    above = f'<p class="phi" role="note"><strong>Do not include any patient information.</strong> {E(CFG["phi_notice"].split(". ",1)[1])}</p>'
    if full: above += f'<p class="fine">{E(CFG["email_notice"])}</p><p class="fine"><strong>Reminder: do not include any patient information.</strong></p>'
    if form_id == 'checklist': above += '<p class="fine">We\'ll email you the checklist and occasional guides about billing staffing. Unsubscribe any time.</p>'
    above += f'<p class="referral" role="note">{ico("handshake")}<span>{E(AFF["referral"])}</span></p>'   # slots §4: directly above submit
    off = '' if FORM_ON else ('<p class="form-off" role="status"><strong>Online requests are temporarily unavailable.</strong> '
                              'Please try again shortly. Nothing you type here is sent or stored.</p>')
    under = ''
    if form_id == 'hero': under = '<p class="fine em-note">We\'ll email you within one business day. You can unsubscribe from our emails at any time.</p>'
    if form_id != 'footer':   # #35: short disclosure under forms (the footer form sits directly above the footer disclosure)
        under += f'<p class="fine affil">{inline(AFF["short"])}</p>'
    return f'''<form class="lead-form lead-{form_id}{'' if FORM_ON else ' is-off'}" id="{'assessment' if form_id=='hero' else 'form-'+form_id}" method="post" action="#" novalidate
 data-tcpa-version="{E(CFG['tcpa_version'])}" data-thanks="{'#unlocked' if form_id == 'checklist' else '/thank-you/'}">
<input type="hidden" name="form_id" value="{form_id}">
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
{fields}{tcpa}
{above}{off}
<button class="btn btn-cta" type="submit"{'' if FORM_ON else ' disabled aria-disabled="true"'}>{btn}{ico('arrow-right')}</button>
<p class="form-msg" role="status" aria-live="polite"></p>
{under}
</form>'''

def ags_block(p):
    links = []
    if not links: return ''
    li = ''.join(f'<li><a href="{E(u)}" rel="noopener">{E(t)}</a></li>' for t, u in links)
    return f'<aside class="related-ext"><h2>About the staffing provider behind this site</h2><p>{E(CFG["ags_intro"])}</p><ul>{li}</ul></aside>'

FOOT = [('Guides', [('what-is-revenue-cycle-management', 'RCM'), ('hipaa-outsourced-medical-billing', 'HIPAA'), ('medical-billing-staffing-cost', 'Costs'),
                     ('medical-billing-technology', 'Technology'), ('denial-management', 'Denial Management')]),
        ('Services', [('credentialing-services', 'Credentialing'), ('prior-authorization-specialist', 'Prior Auth'), ('treatment-center-vob', 'VOB'),
                      ('hire-remote-medical-coders', 'Coding'), ('ar-specialist', 'A/R'), ('virtual-medical-assistant', 'Virtual Assistants')]),
        ('Vendors', [('approved-vendors', 'Approved vendors'), ('how-we-vet-vendors', 'How we vet vendors'),
                     ('featured-vendor-alliance-global-solutions', 'Alliance Global Solutions profile')]),
        ('Site', [('about', 'About & disclosure'), ('how-it-works', 'How it works'), ('faq', 'FAQ'), ('contact', 'Contact'), ('privacy', 'Privacy'), ('terms', 'Terms')])]

def footer(p):
    cols = ''.join(f'<div><h2 class="fh">{E(h)}</h2><ul>' + ''.join(f'<li><a href="{BYKEY[k]["path"]}">{E(l)}</a></li>' for k, l in ks if BYKEY[k]['ready']) + '</ul></div>' for h, ks in FOOT)
    band = '' if p['key'] in ('contact', 'thank-you') else f'''<section class="cta-band" id="footer-cta"><div class="wrap cta-grid">
<div><h2>Short on billing staff?</h2><p>Get a free, no-obligation staffing assessment. No patient info needed.</p></div>
{form("footer")}</div></section>'''
    sticky = '' if p['key'] in ('contact', 'thank-you') else f'''<div class="sticky-cta" hidden><span class="s-m">Free billing staffing assessment</span><span class="s-d">Short on billing staff? Get a free, no-obligation staffing assessment. No patient info needed.</span>
<a class="btn btn-sm" href="{'#assessment' if p['key']=='index' else '/contact/'}">Get my free assessment</a><button class="x" type="button" aria-label="Dismiss">×</button></div>'''
    return f'''{band}
<footer class="site-footer"><div class="wrap">
<div class="fcols">{cols}</div>
<p class="disclosure" id="disclosure"><strong>Affiliation disclosure:</strong> {inline(AFF['short'])}</p>
<p class="fine">Please do not submit patient information through this site. Content is general information, not legal, compliance or financial advice. © {datetime.date.today().year} {E(CFG['site_name'])}</p>
</div></footer>{sticky}
<script>document.addEventListener('click',function(e){{document.querySelectorAll('.nav-desk details[open]').forEach(function(d){{if(!d.contains(e.target))d.removeAttribute('open')}})}})</script>
<script src="/form-config.js" defer></script><script src="/form.js" defer></script></body></html>'''

def stub(p):
    return f"""<div class="placeholder"><p><strong>Copy pending.</strong> This guide is being written. Until it is published, this page is a stub
(noindex, not in the sitemap or llms.txt).</p><p>Topic: {E(p['description'])}</p></div>"""

def crumbs(p):
    parts = ['<a href="/">Home</a>']
    if p['parent']: parts.append(f'<a href="{BYKEY[p["parent"]]["path"]}">{E(BYKEY[p["parent"]]["label"])}</a>')
    parts.append(f'<span aria-current="page">{E(p["label"])}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span class="sep" aria-hidden="true">/</span> '.join(parts) + '</nav>'

PAGE_ICON = {'revenue-cycle-management-staffing': 'network', 'denial-management': 'file-x-2', 'reduce-ar-days': 'hourglass',
  'eligibility-verification-prior-authorization': 'calendar-check', 'hire-remote-medical-coders': 'file-search', 'ar-specialist': 'receipt-text',
  'credentialing-specialist': 'badge-check', 'prior-authorization-specialist': 'clipboard-check', 'hire-remote-medical-billers': 'users-round',
  'medical-billing-outsourcing': 'layers', 'offshore-medical-billers': 'headset', 'virtual-medical-assistant': 'monitor-check',
  'hipaa-outsourced-medical-billing': 'shield-check', 'medical-billing-staffing-cost': 'calculator', 'behavioral-health-billing': 'brain',
  'how-it-works': 'list-checks', 'faq': 'circle-help', 'checklist': 'clipboard-check', 'about': 'book-open-check', 'contact': 'messages-square'}

def children(p):
    kids = [c for c in PAGES if c['parent'] == p['key']]
    if not kids: return ''
    cards = ''.join(f'<a class="tile" href="{c["path"]}"><span class="tile-ic">{ico(PAGE_ICON.get(c["key"], "file-check-2"))}</span><h3>{E(c["label"])}{"" if c["ready"] else " <small>(coming soon)</small>"}</h3><p>{E(c["description"])}</p><span class="tile-go">{ico("arrow-right")}</span></a>' for c in kids)
    return f'<section class="kids"><h2>Guides in this section</h2><div class="tiles">{cards}</div></section>'

def siblings(p):
    if not p['parent'] or re.search(r'^##\s+Related guides', p.get('raw', ''), re.M): return ''   # copy carries its own Related guides block
    par = BYKEY[p['parent']]
    li = ''.join(f'<li><a href="{c["path"]}">{E(c["label"])}</a></li>' for c in PAGES if c['parent'] == p['parent'] and c['key'] != p['key'])
    return f'<aside class="related"><h2>More in <a href="{par["path"]}">{E(par["label"])}</a></h2><ul>{li}</ul></aside>'

def byline(p):
    if not (p.get('has_byline') and p.get('date_published')): return ''
    rv = f' · Reviewed by {E(p["reviewer"])}' if p.get('reviewer') else ''
    return (f'<p class="byline">By the Medical Billing Team editors · Published <time datetime="{p["date_published"]}">{human(p["date_published"])}</time>'
            f' · Updated <time datetime="{p["date_modified"]}">{human(p["date_modified"])}</time>{rv} · <a href="/about/#how-we-write-our-guides">How we research and review</a></p>')

def faq_html(p, head='FAQ'):
    hid = re.sub(r'[^a-z0-9]+', '-', head.lower()).strip('-')
    items = ''.join(f'<details><summary><span>{E(q)}</span>{ico("arrow-right", "ic chev")}</summary><div class="ans"><p>{E(a)}</p></div></details>' for q, a in p['faqs'])
    tail = convert(p.get('faq_tail', ''))[0] if p.get('faq_tail') else ''
    return f'<section class="faq" aria-labelledby="{hid}"><h2 id="{hid}">{E(head)}</h2>{items}{tail}</section>'

def enhance(h):
    """Presentation-only wrappers around the converted copy (no text changes)."""
    h = re.sub(r'<p><strong>Short answer:</strong>(.*?)</p>', r'<div class="short-answer"><p><strong>Short answer:</strong>\1</p></div>', h, count=1, flags=re.S)
    h = re.sub(r'<h2 id="related-guides">Related guides</h2>\s*<ul>(.*?)</ul>', r'<aside class="related-guides"><h2 id="related-guides">Related guides</h2><ul>\1</ul></aside>', h, flags=re.S)
    h = re.sub(r'<p><strong>Practical tip:</strong>(.*?)</p>', r'<p class="tip"><strong>Practical tip:</strong>\1</p>', h, flags=re.S)
    return h

# ---------------- directory + featured vendor (LVNY hub/partner patterns) ----------------
PAGE_ICON.update({'approved-vendors': 'store', 'how-we-vet-vendors': 'user-search', 'alliance-global-solutions': 'building-2'})

def slot_note(p):
    """Preview-only marker on pages whose copy is interim (copy_status: slot)."""
    if not p.get('slot') or INDEX: return ''
    return '<div class="slot-note" role="note"><strong>Copy slot.</strong> Interim wording; final copy arrives with the Alliance Global positioning drop. Not indexed.</div>'

def affil_box(cls='', text=None):
    return f'<div class="affil-box {cls}" id="affiliation" role="note">{ico("handshake")}<p>{inline(text or AFF["full"])}</p></div>'

def vendors():
    return [v for v in PAGES if v['kind'] == 'vendor' and v['vendor']]

LOGO_ICON = '<img class="vc-logo" src="/images/logo-ags-icon.webp" alt="Alliance Global Solutions icon logo with winged letter A" width="56" height="56" loading="lazy" decoding="async">'

def card_wrap(inner, v, cls='vendor-card'):
    """Vendor card component (no stars, ratings, reviews or testimonials): logo + badge + copy + profile CTA."""
    d = v['vendor']
    return (f'<article class="{cls}"><div class="vc-top">{LOGO_ICON}<p class="vc-badge">{ico("handshake")}{E(d.get("affiliation_badge", "Affiliated: operates this site"))}</p></div>'
            f'{inner}<a class="btn btn-sm vc-go" href="{v["path"]}">View vendor profile{ico("arrow-right")}</a></article>')

def vendor_card_html(h, v):
    def rw(m):
        inner = re.sub(r'<p><strong>Affiliation: operates this site\.</strong></p>\s*', '', m.group(1))
        return card_wrap(inner.replace('<ul>', '<ul class="vc-list">', 1), v)
    return re.sub(r'<!--VCARD-->\s*(.*?)(?=<h2|$)', rw, h, count=1, flags=re.S)

def vendor_teaser_html(h, v):
    h = h.replace('<!--VTEASER-->', '')
    return re.sub(r'(<p><strong>Alliance Global Solutions</strong>.*?</p>)', lambda m: card_wrap(m.group(1) +
                  '<p class="vc-links"><a href="/approved-vendors/">All approved vendors</a> · <a href="/how-we-vet-vendors/">How we vet vendors</a></p>', v, 'vendor-card vc-teaser'), h, count=1, flags=re.S)

def gimg(it, sizes, lazy=True):
    ss = ', '.join(f'/img/ags/{it["stem"]}-{w}.webp {w}w' for w, _, _ in it['sizes'])
    w0, h0 = it['sizes'][0][1], it['sizes'][0][2]
    return (f'<img src="/img/ags/{it["stem"]}-{it["sizes"][0][0]}.webp" srcset="{ss}" sizes="{sizes}" alt="{E(it["alt"])}" '
            f'width="{w0}" height="{h0}" {"loading=\"lazy\" " if lazy else ""}decoding="async">')

def image_slot(slot):
    off, team = GALLERY.get('office', []), GALLERY.get('team', [])
    if slot == 'hero' and off:
        it = off[0]
        cap = f'<figcaption>{E(it["caption"])}</figcaption>' if it.get('caption') else ''
        return f'<figure class="vp-hero-img">{gimg(it, "(min-width:1080px) 760px, 100vw")}{cap}</figure>'
    if slot == 'gallery' and (len(off) > 1 or team):
        figs = ''.join(f'<figure>{gimg(it, "(min-width:960px) 250px, 50vw")}</figure>' for it in off[1:])
        tm = ''.join(f'<li>{gimg(it, "(min-width:960px) 120px, 30vw")}</li>' for it in team)
        return ((f'<div class="vp-gallery g-n{len(off) - 1}">{figs}</div>' if figs else '') +
                (f'<ul class="g-team" aria-label="Alliance Global Solutions team members">{tm}</ul>' if tm else '') +
                '<p class="g-note">Photos supplied by Alliance Global Solutions.</p>')
    return ''   # location (BGC skyline): HELD until rights are confirmed

def tech_html(p):
    t = p.get('tech') or {}
    if not t.get('body') or p['key'] in ('contact', 'privacy', 'terms', 'index'): return ''
    link = t.get('link') or '/medical-billing-technology/'
    more = '' if p['path'] == link else f'<p class="tech-more"><a href="{link}">Technology in medical billing: guide and latest updates{ico("arrow-right")}</a></p>'
    return f'<section class="tech-section" aria-labelledby="technology"><h2 id="technology"><span class="ts-ic">{ico("cpu")}</span>Technology</h2><p>{inline(t["body"])}</p>{more}</section>'

def updates_html(items, teaser=False):
    if not items: return ''
    li = ''
    for x in items:
        src = f'<a href="{E(x["source_url"])}" rel="noopener">Source: {E(x["source_name"])}</a>'
        summ = '' if teaser else f' {E(x.get("summary", ""))}'
        li += f'<li><time datetime="{x["date"]}">{human(x["date"])}</time><p><strong>{E(x["headline"])}</strong>{summ} {src}</p></li>'
    tail = ('<p class="tech-more"><a href="/medical-billing-technology/#latest-updates">More technology updates' + ico('arrow-right') + '</a></p>') if teaser else ''
    return f'<ul class="updates{" updates-teaser" if teaser else ""}">{li}</ul>{tail}'

def components(h, p):
    h = h.replace('<!--TECH-->', tech_html(p))
    h = h.replace('<!--UPDATES-->', updates_html(UPDATES))
    h = h.replace('<!--TEASER-->', updates_html(UPDATES[:3], teaser=True))
    vs = vendors()
    if vs:
        if '<!--VCARD-->' in h: h = vendor_card_html(h, vs[0])
        if '<!--VTEASER-->' in h: h = vendor_teaser_html(h, vs[0])
    h = re.sub(r'<!--IMG:([\w-]+)-->', lambda m: image_slot(m.group(1)), h)
    return re.sub(r'<!--(?:VCARD|VTEASER|UPDATES|TEASER|TECH)-->', '', h)

def vendor_main(p):
    d = p['vendor']
    facts = (f'<dl class="vp-facts"><div><dt>{ico("users-round")}Team size range</dt><dd>{E(d.get("team_size_range", ""))}</dd></div>'
             f'<div><dt>{ico("map-pin")}Locations</dt><dd>US-based management and admin; staff in the Philippines, Colombia and other countries</dd></div>'
             f'<div><dt>{ico("file-signature")}HIPAA</dt><dd>Signs a BAA with each client before any PHI access</dd></div>'
             f'<div><dt>{ico("messages-square")}References</dt><dd>{E(d.get("references", ""))}</dd></div>'
             f'<div><dt>{ico("handshake")}Listing</dt><dd>{E(d.get("affiliation_badge", ""))}. <a href="#affiliation">Disclosure</a></dd></div></dl>')
    svc = ''.join(f'<li><a href="{s["url"]}">{E(s["name"])}</a></li>' for s in d.get('services', []))
    h = p['body']
    h = re.sub(r'<p><strong>Affiliation disclosure:</strong>\s*(.*?)</p>', lambda m: f'<div class="affil-box vp-affil" id="affiliation" role="note">{ico("handshake")}<p><strong>Affiliation disclosure:</strong> {m.group(1)}</p></div>', h, count=1, flags=re.S)
    h = re.sub(r'(<h2 id="getting-started-in-3-steps">.*?</h2>\s*)<ol>', r'\1<ol class="steps-list">', h, count=1, flags=re.S)
    h = components(h, p)
    h = h.replace('<!--FAQ-->', faq_html(p, p.get('faq_head') or 'FAQ'))
    h = enhance(h)
    toc = f'<details class="toc" open><summary>{ico("list")}On this page</summary><ol>' + ''.join(f'<li><a href="#{i}">{E(t)}</a></li>' for i, t in p['toc']) + '</ol></details><script>if(innerWidth<1080)document.currentScript.previousElementSibling.removeAttribute("open")</script>'
    return f"""<main id="main" class="vendor-page">
<section class="vp-hero"><div class="wrap">{crumbs(p)}<div class="vp-grid">
<div class="vp-id"><img class="vp-logo" src="/images/logo-ags.webp" alt="Alliance Global Solutions logo" width="103" height="88" decoding="async">
<p class="eyebrow vp-eye">{ico("badge-check")}Featured approved vendor · {E(d.get('affiliation_badge', ''))}</p>
<h1>{E(p.get('h1', d['name']))}</h1><span class="rule ph-rule" aria-hidden="true"><i></i><i></i><i></i></span>
<p class="vp-tag">{E(d.get('tagline', ''))}</p>{byline(p)}
<div class="vp-cta"><a class="btn btn-cta" href="/contact/">Request help{ico("arrow-right")}</a></div></div>
<div class="vp-card">{facts}<h2 class="vp-sv-h">Services</h2><ul class="vp-sv">{svc}</ul></div></div></div></section>
<div class="wrap page-grid has-toc"><aside class="toc-col"><div class="toc-stick">{toc}{aside_cta(p)}</div></aside><article class="prose vp-body">{h}</article></div>
<div class="wrap">{siblings(p)}</div></main>"""

def aside_cta(p):
    # Stitch cost/RCM screens: help card under the TOC (desktop only); reuses the sticky-bar copy, no new claims
    return (f'<div class="aside-cta">{ico("clipboard-check")}<p><strong>Short on billing staff?</strong> Get a free, no-obligation staffing assessment. No patient info needed.</p>'
            f'<a class="btn btn-cta btn-sm" href="/contact/">Get my free assessment</a></div>')

def page_main(p):
    h1 = p.get('h1', p['title'].split(' | ')[0])
    if p['key'] == 'contact':
        intro = convert(p['intro'])[0] if p['ready'] else '<p>Tell us about your practice and a billing staffing specialist will follow up. No patient information.</p>'
        rest = convert('\n'.join(p['sections']))[0] if p['sections'] else ''
        body = intro + '<div class="form-card form-card-full">' + form('full') + '</div>' + rest
    elif p['key'] == 'thank-you':
        body = ('<p>Thank you. We\'ve received your request. Alliance Global Solutions, our affiliated approved vendor, will email you, usually within one business day.</p>'
                '<p>In the meantime: <a href="/checklist/">Medical Billing Health Checklist</a> · <a href="/hipaa-outsourced-medical-billing/">HIPAA guide for outsourced billing staff</a> · <a href="/revenue-cycle-management-staffing/">RCM staffing guide</a></p>')
    elif p.get('gated'):
        body = (convert(p['intro'])[0] + '<div class="gate form-card"><h2>Get the checklist</h2>' + form('checklist') +
                ('' if (FORM_ON or INDEX) else '<p class="fine preview-note">Preview only: the form backend is off, so the gate can\'t unlock. <button type="button" class="linkbtn" data-unlock>Show the gated content</button> (preview reviewers only).</p>') +
                '</div><div class="gated" id="unlocked" hidden>' + convert('\n'.join(p['sections']))[0] + '</div>')
    else:
        body = p['body'] if p['ready'] else stub(p)
    if p.get('draft'):
        body = '<div class="draft-banner"><strong>DRAFT: for legal review.</strong> Not approved for publication. Bracketed items are placeholders.</div>' + body
    toc = ''
    if len(p['toc']) >= 4 and p['kind'] in ('pillar', 'cluster'):
        toc = f'<details class="toc" open><summary>{ico("list")}On this page</summary><ol>' + ''.join(f'<li><a href="#{i}">{E(t)}</a></li>' for i, t in p['toc']) + '</ol></details><script>if(innerWidth<1080)document.currentScript.previousElementSibling.removeAttribute("open")</script>'
    if '<!--FAQ-->' in body:
        body = body.replace('<!--FAQ-->', faq_html(p, p.get('faq_head') or 'FAQ'))
    elif p['faqs'] and p['key'] != 'faq' and not re.search(r'^##\s+.*FAQ', p['raw'], re.M | re.I):
        body += faq_html(p)
    body = enhance(components(body, p))
    if p['key'] == 'about':   # #35: full disclosure component right under the operator-disclosure heading (slots §4 text)
        body = re.sub(r'(<h2 id="disclosure-who-operates-this-site">.*?</h2>)', lambda m: m.group(1) + affil_box(), body, count=1, flags=re.S)
    if p['key'] == 'contact':   # "Who receives your request" callout = contact-area disclosure
        body = re.sub(r'<blockquote>\s*<p><strong>Who receives your request:</strong>', '<blockquote class="affil-box" id="affiliation"><p><strong>Who receives your request:</strong>', body, count=1)
    disc = f'<p class="disclosure-inline">{ico("building-2")}<span>{E(DISC)}{(" " + E(BAA_LINE)) if p["key"] == "hipaa-outsourced-medical-billing" else ""}</span></p>'
    icon = PAGE_ICON.get(p['key'])
    badge = f'<span class="page-ic">{ico(icon)}</span>' if icon else ''
    return f"""<main id="main"><div class="page-hero"><div class="wrap">{crumbs(p)}{slot_note(p)}<div class="ph-row">{badge}<h1>{E(h1)}</h1></div><span class="rule ph-rule" aria-hidden="true"><i></i><i></i><i></i></span>
{byline(p)}{disc}</div></div>
<div class="wrap page-grid{' has-toc' if toc else ''}">{('<aside class="toc-col"><div class="toc-stick">' + toc + aside_cta(p) + '</div></aside>') if toc else ''}<article class="prose">{body}</article></div>
<div class="wrap">{'' if p['kind'] == 'directory' else children(p)}{siblings(p)}</div></main>"""

TOPIC_ICON = {'who-this-site-helps': ['user-round-check', 'stethoscope', 'building-2', 'briefcase-medical', 'layers'],
  'common-billing-problems-we-write-about': ['file-x-2', 'hourglass', 'clock-alert', 'calendar-check', 'users-round'],
  'the-remote-billing-team-model-explained': ['monitor-check', 'list-checks', 'user-round-check', 'key-round'],
  'hipaa-comes-first': ['file-signature', 'key-round', 'lock-keyhole', 'graduation-cap']}

def iconize_list(h, icons):
    i = [0]
    def li(m):
        n = icons[i[0] % len(icons)]; i[0] += 1
        return f'<li><span class="li-ic">{ico(n)}</span><span class="li-t">{m.group(1)}</span></li>'
    return re.sub(r'<li>(.*?)</li>', li, h, flags=re.S)

def home_main(p):
    if p['ready']:
        hero = convert(p['intro'])[0]
        secs = []
        for s in p['sections']:
            if s.startswith('<!--FAQ-->'):
                secs.append(f'<section class="band band-faq" id="short-faq"><div class="wrap narrow">{faq_html(p, p.get("faq_head") or "FAQ")}</div></section>'); continue
            h = re.match(r'##\s+(.+)', s).group(1)
            hid = re.sub(r'[^a-z0-9]+', '-', h.lower()).strip('-')
            inner = components(convert(s)[0], p)
            if hid in TOPIC_ICON:
                first_ul = inner.find('<ul>')
                if first_ul >= 0:
                    end = inner.find('</ul>', first_ul) + 5
                    inner = inner[:first_ul] + '<ul class="feature-list">' + iconize_list(inner[first_ul + 4:end - 5], TOPIC_ICON[hid]) + '</ul>' + inner[end:]
            if 'hipaa' in hid:
                inner = re.sub(r'<p><a href="([^"]+)">(Read the full HIPAA guide[^<]*)</a></p>', r'<p><a class="btn btn-light" href="\1">\2</a></p>', inner)
                secs.append(f'<section class="hipaa-band" id="{hid}"><div class="wrap hipaa-grid"><div class="hipaa-art">{p.get("hipaa_img", "")}<span class="shield">{ico("shield-check", "ic big")}</span></div><div class="prose">{inner}</div></div></section>')
            elif hid.startswith('how-it-works'):
                secs.append(f'<section class="band band-steps" id="{hid}"><div class="wrap narrow prose">{inner}</div></section>')
            elif hid.startswith('free-resource'):
                secs.append(f'<section class="band band-resource" id="{hid}"><div class="wrap"><div class="resource-card"><span class="res-ic">{ico("clipboard-check", "ic big")}</span><div class="prose">{inner}</div></div></div></section>')
            else:
                cls = 'band band-alt' if len(secs) % 2 else 'band'
                width = 'mid' if hid in ('who-this-site-helps', 'common-billing-problems-we-write-about') else 'narrow'
                secs.append(f'<section class="{cls}" id="{hid}"><div class="wrap {width} prose">{inner}</div></section>')
        rest = ''.join(secs)
    else:
        hero = stub(p); rest = ''
    def pill(c): return f'<li><a href="{c["path"]}">{ico(PAGE_ICON.get(c["key"], "file-check-2"))}{E(c["label"])}</a></li>'
    rcm = ''.join(pill(c) for c in PAGES if c['parent'] == 'revenue-cycle-management-staffing')
    mbs = ''.join(pill(c) for c in PAGES if c['parent'] == 'hire-remote-medical-billers')
    mbs_ul = f'<ul class="sublinks">{mbs}</ul>' if mbs else ''
    topics = f"""<section class="band topics" id="explore"><div class="wrap"><h2>Explore by topic</h2><div class="tiles tiles-topics">
<div class="tile tile-wide"><span class="tile-ic">{ico('network')}</span><h3><a href="/revenue-cycle-management-staffing/">RCM staffing</a></h3><ul class="sublinks">{rcm}</ul></div>
<div class="tile"><span class="tile-ic">{ico('users-round')}</span><h3><a href="/hire-remote-medical-billers/">Medical billing staffing</a></h3><p>Remote, offshore and outsourced billers.</p>{mbs_ul}</div>
<div class="tile"><span class="tile-ic">{ico('shield-check')}</span><h3><a href="/hipaa-outsourced-medical-billing/">HIPAA &amp; outsourcing</a></h3><p>BAAs, minimum necessary, access controls and what to ask any agency.</p></div>
<div class="tile"><span class="tile-ic">{ico('calculator')}</span><h3><a href="/medical-billing-staffing-cost/">Cost comparisons</a></h3><p>In-house vs. billing company vs. dedicated remote staff.</p></div>
<div class="tile"><span class="tile-ic">{ico('brain')}</span><h3><a href="/behavioral-health-billing/">Behavioral health billing</a></h3><p>Billing staff for behavioral health practices and treatment centers.</p></div>
</div></div></section>"""
    return f"""<main id="main">
<section class="hero">{p.get('hero_img', '')}<div class="wrap hero-grid">
<div class="hero-h"><p class="eyebrow">For US medical practices &amp; billing companies</p><h1>{E(p.get('h1', p['title']))}</h1><span class="rule" aria-hidden="true"><i></i><i></i><i></i></span></div>
<div class="hero-form form-card"><h2 class="form-title">Get your free staffing assessment</h2>{form("hero")}</div>
<div class="hero-copy prose">{hero}<p class="disclosure-inline">{ico("building-2")}<span>{E(DISC)}</span></p></div>
</div></section>
<section class="trust" aria-label="At a glance"><div class="wrap"><ul class="trust-row">
<li>{ico('file-signature')}<span>Alliance Global Solutions signs a BAA before any PHI access</span></li>
<li>{ico('lock-keyhole')}<span>No patient information needed</span></li>
<li>{ico('monitor-check')}<span>Dedicated staff who work in your systems</span></li>
<li>{ico('circle-check-big')}<span>Free, no-obligation staffing assessment</span></li>
</ul></div></section>
{topics}{rest}
</main>"""

# ---------------- write ----------------
gen_file = B / 'generated.json'
old = json.loads(gen_file.read_text()) if gen_file.exists() else []
for rel in old:
    t = ROOT / rel
    if t.is_dir(): shutil.rmtree(t)
    elif t.exists(): t.unlink()
generated = []
for f in (B / 'static').iterdir():
    if f.is_dir():
        if (ROOT / f.name).exists(): shutil.rmtree(ROOT / f.name)
        shutil.copytree(f, ROOT / f.name)
    else: shutil.copy2(f, ROOT / f.name)
    generated.append(f.name)

_FB = CFG.get('ags_link_fallback') or {}
_VR = CFG.get('vendor_link_rel') or {}
def outbound(h):
    if _FB.get('enabled'): h = h.replace(_FB['from'], _FB['to'])
    if _VR.get('hosts'):
        hp = '|'.join(re.escape(x) for x in _VR['hosts'])
        h = re.sub(r'(<a href="https?://(?:www\.)?(?:' + hp + r')[^"]*")([^>]*)>', lambda m: m.group(1) + re.sub(r'\s*rel="[^"]*"', '', m.group(2)) + f' rel="{_VR.get("rel", "noopener")}">' if 'rel=' in m.group(2) or True else m.group(0), h)
    return h

def prefix(h):
    if not BASE_PATH: return h
    h = re.sub(r'(\b(?:href|src|action|data-thanks)=")/(?!/)', rf'\1{BASE_PATH}/', h)
    return re.sub(r'\bsrcset="([^"]+)"', lambda m: 'srcset="' + re.sub(r'(^|,\s*)/(?!/)', rf'\1{BASE_PATH}/', m.group(1)) + '"', h)

IMG = BYKEY['index']
IMG['hero_img'] = ('<picture class="hero-bg" aria-hidden="true"><source media="(min-width:1300px)" srcset="/img/hero-office-dusk-1920.webp">'
                   '<source media="(min-width:700px)" srcset="/img/hero-office-dusk-1280.webp">'
                   '<img src="/img/hero-office-dusk-768.webp" alt="" width="768" height="429" fetchpriority="high" decoding="async"></picture>')
IMG['hipaa_img'] = ('<img src="/img/hipaa-glass-shield-480.webp" srcset="/img/hipaa-glass-shield-480.webp 480w, /img/hipaa-glass-shield-800.webp 800w" '
                    'sizes="(min-width:960px) 420px, 100vw" alt="" width="480" height="643" loading="lazy" decoding="async">')
for p in PAGES:
    rel = p['path'].strip('/')
    d = ROOT / rel if rel else ROOT
    d.mkdir(parents=True, exist_ok=True)
    if p.get('held'): continue
    main = home_main(p) if p['key'] == 'index' else vendor_main(p) if p['kind'] == 'vendor' else page_main(p)
    html_out = head(p) + nav(p['key']) + main + footer(p)
    for _hp in [x['path'] for x in PAGES if x.get('held')]:   # unlink held (unpublished) pages, keep the words
        html_out = re.sub(r'<a href="' + re.escape(_hp) + r'(?:#[^"]*)?"[^>]*>(.*?)</a>', r'\1', html_out)
    (d / 'index.html').write_text(prefix(outbound(html_out)))
    generated.append(rel.split('/')[0] if rel else 'index.html')

# 404
nf = dict(BYKEY['thank-you'], key='thank-you', title='Page not found', label='Not found', path='/404.html', force_noindex=True)
(ROOT / '404.html').write_text(prefix(head(nf).replace(f'href="{SITE}/404.html"', f'href="{SITE}/"') + nav('thank-you') +
    '<main id="main" class="wrap narrow page-404"><h1>Page not found</h1><p><a href="/">Go to the home page</a> or <a href="/contact/">request a free staffing assessment</a>.</p></main>' + footer(BYKEY['thank-you'])))
generated.append('404.html')

idx = [p for p in PAGES if p['indexable']]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{url(p)}</loc><lastmod>{p.get("date_modified") or TODAY}</lastmod></url>\n' for p in idx) + '</urlset>\n')
# robots.txt: MSD (boneshq/microschool-directory) pattern, adapted
bots = CFG['ai_crawlers']
(ROOT / 'robots.txt').write_text('# medicalbillingteam.com — open to all crawlers and AI assistants\n'
    '# (Preview/staging pages are kept out of indexes with <meta name="robots" content="noindex,nofollow">, not here.)\n'
    '# Crawler access is allowed here on purpose; until cutover every page carries noindex via the indexing_enabled switch.\n'
    'User-agent: *\nAllow: /\nDisallow: /thank-you/\n\n# AI training crawlers explicitly allowed (Tony, 2026-10-18)\n'
    + ''.join(f'User-agent: {b}\nAllow: /\n' for b in CFG['ai_training_crawlers'])
    + '\n# AI search / assistant and search-engine crawlers explicitly allowed\n'
    + ''.join(f'User-agent: {b}\nAllow: /\n' for b in bots) + f'\nSitemap: {SITE}/sitemap.xml\n')

# llms.txt: served verbatim from the copywriter's file (CODE-DESK #7)
(ROOT / 'llms.txt').write_text(outbound(fix_copy((B / 'content' / 'llms.txt').read_text())))   # verbatim + location override
# llms-full.txt: regenerated from published markdown on every build (CODE-DESK #8; logic from medbill/gen/llmsfull.py)
FULL_ORDER = ['index','what-is-revenue-cycle-management','revenue-cycle-management-staffing','hipaa-outsourced-medical-billing','medical-billing-staffing-cost','medical-billing-technology','credentialing-services','credentialing-specialist','prior-authorization-specialist','eligibility-verification-prior-authorization','treatment-center-vob','behavioral-health-billing','ar-specialist','hire-remote-medical-coders','hire-remote-medical-billers','virtual-medical-assistant','virtual-medical-receptionist','medical-billing-outsourcing','offshore-medical-billers','denial-management','denial-code-co-16','denial-code-co-22','denial-code-co-29','denial-code-co-97','denial-code-co-197','denial-code-co-204','reduce-ar-days','approved-vendors','how-we-vet-vendors','featured-vendor-alliance-global-solutions','how-it-works','faq','about']   # = medbill/gen/llmsfull.py order
FT = ["# Medical Billing Team: full text\n\n> Concatenated public guides from medicalbillingteam.com, generated " + TODAY + ". Operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the site's only approved vendor; requests may be referred to it. Excludes forms, legal drafts and gated content.\n"]
for k in FULL_ORDER:
    f = B / 'content' / f'{k}.md'
    if not f.exists() or not BYKEY[k]['ready']: continue
    src = fix_copy(f.read_text()); fm, body = src.split('---', 2)[1], src.split('---', 2)[2]
    slug = re.search(r'^slug:\s*"?([^"\n]+)"?', fm, re.M).group(1)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    if k == 'index':
        body = re.sub(r'## Short form \(hero\).*?(?=## Who this site helps)', '', body, flags=re.S)
        body = re.sub(r'## Sticky CTA bar.*', '', body, flags=re.S)
    body = re.sub(r'\]\(/', '](https://medicalbillingteam.com/', body)
    for _hp in [x['path'] for x in PAGES if x.get('held')]:
        body = re.sub(r'\[([^\]]+)\]\(https://medicalbillingteam\.com' + re.escape(_hp) + r'[^)]*\)', r'\1', body)
    FT.append("\n---\n\nSource: https://medicalbillingteam.com%s\n\n" % slug + body.strip() + "\n")
_lf = B / 'content' / 'llms-full.txt'
if _lf.exists():   # CODE-DESK #52: serve the copywriter's regenerated file; apply location override, held-page unlinks, AGS fallback
    _txt = fix_copy(_lf.read_text())
    for _hp in [x['path'] for x in PAGES if x.get('held')]:
        _txt = re.sub(r'\[([^\]]+)\]\(https://medicalbillingteam\.com' + re.escape(_hp) + r'[^)]*\)', r'\1', _txt)
    (ROOT / 'llms-full.txt').write_text(outbound(_txt))
else: (ROOT / 'llms-full.txt').write_text(outbound(''.join(FT)))
(ROOT / '.nojekyll').write_text('')
(ROOT / 'CNAME').write_text(CFG.get('custom_domain', 'medicalbillingteam.com') + '\n')   # go-live (Tony via CEO 1:22 PM ET); Pages settings/DNS handled elsewhere
generated.append('CNAME')
fb = CFG['form_backend']
fc = {'mode': 'apps_script', 'enabled': bool(fb.get('apps_script_url')), 'endpoint': fb.get('apps_script_url', ''), 'formKey': fb.get('form_key', '')}
lines = ['/* generated by _build/src/build.py from _build/config.json form_backend. Endpoint + formKey are public by design. */', 'window.MBT_FORM = ' + json.dumps(fc) + ';']
(ROOT / 'form-config.js').write_text('\n'.join(lines) + '\n')
generated.append('form-config.js')
generated += ['sitemap.xml', 'robots.txt', 'llms.txt', 'llms-full.txt', '.nojekyll']
gen_file.write_text(json.dumps(sorted(set(generated)), indent=1))
ver = set(CFG.get('ags_verified_200', []))
pending = {}
for p in PAGES:
    for u in set(re.findall(r'https?://(?:www\.)?allianceglobalsolutions\.com[^)\s"]*', p.get('raw', ''))):
        if u.replace('://allianceglobalsolutions', '://www.allianceglobalsolutions') not in ver: pending.setdefault(u, []).append(p['path'])
status = {'ags_links_pending_prod_check': pending, 'built': datetime.datetime.now().isoformat(timespec='seconds'), 'base_path': BASE_PATH, 'indexing_enabled': INDEX,
          'form_backend_enabled': bool(CFG['form_backend'].get('apps_script_url')),
          'live_ready': [p['path'] for p in PAGES if p['ready'] and p['kind'] != 'utility'],
          'stubs': [p['path'] for p in PAGES if not p['ready']]}
(B / 'build-status.json').write_text(json.dumps(status, indent=1))
print(json.dumps(status, indent=1))

# CODE-DESK #14 (internal part): fail the build on any broken same-site link or asset reference.
_broken = []
for _f in ROOT.rglob('*.html'):
    if any(s in _f.parts for s in ('_build', '.git', 'node_modules')): continue
    for _u in re.findall(r'(?:href|src)="(' + re.escape(BASE_PATH) + r'/[^"#?]*)', _f.read_text()):
        _rel = _u[len(BASE_PATH):].lstrip('/')
        _t = ROOT / _rel
        if not (_t.is_file() or (_t / 'index.html').is_file()): _broken.append(f'{_f.relative_to(ROOT)} -> {_u}')
if _broken:
    raise SystemExit('BROKEN INTERNAL LINKS:\n' + '\n'.join(sorted(set(_broken))))
print('internal link check: OK')

# No "25 years" / "25+ years" claim anywhere in published output: copy, alt text, schema, llms files, scripts.
_claims = []
for _f in ROOT.rglob('*'):
    if not _f.is_file() or any(s in _f.parts for s in ('_build', '.git', 'node_modules', 'scripts')): continue
    if _f.suffix.lower() not in ('.html', '.txt', '.xml', '.js', '.json', '.svg', '.css', '.md'): continue
    for _m in CLAIM_RE.finditer(_f.read_text(errors='ignore')): _claims.append(f'{_f.relative_to(ROOT)}: {_m.group(0)!r}')
for _f in ROOT.rglob('*.webp'):   # image names (published) must not carry badge/tenure assets
    if re.search(r'home-pic|years|badge', _f.name, re.I): _claims.append(f'{_f.relative_to(ROOT)}: image name')
if _claims: raise SystemExit('BLOCKED TENURE CLAIM(S):\n' + '\n'.join(_claims))
print('tenure-claim check (25 years / 25+ years): OK')

# Location override guard (Tony 1:31 PM ET): old AGS location wording must not reach published output.
_loc = []
for _f in list(ROOT.rglob('*.html')) + [ROOT / 'llms.txt', ROOT / 'llms-full.txt']:
    if any(s in _f.parts for s in ('_build', '.git', 'node_modules', 'v1')): continue
    for _m in LOC_OLD.finditer(_f.read_text(errors='ignore')): _loc.append(f'{_f.relative_to(ROOT)}: {_m.group(0)!r}')
if _loc: raise SystemExit('OLD AGS LOCATION WORDING:\n' + '\n'.join(_loc))
print('location override check: OK')

# Link graph (CODE-DESK #46): each published page needs 3+ inbound and 3+ outbound contextual internal links (main content only).
_out, _in = {}, {}
_pub = {x['path']: x for x in PAGES if x['ready'] and not x.get('held') and x['kind'] != 'utility'}
for _pth in _pub:
    _h = (ROOT / _pth.strip('/') / 'index.html') if _pth != '/' else ROOT / 'index.html'
    _m = re.search(r'<main id="main".*?</main>', _h.read_text(), re.S)
    _links = {re.sub(r'#.*', '', u) for u in re.findall(r'href="(/[^"]*)"', _m.group(0) if _m else '')} - {_pth}
    _links = {u for u in _links if u in _pub}
    _out[_pth] = _links
    for u in _links: _in.setdefault(u, set()).add(_pth)
_weak = [f'{p_}: out {len(_out[p_])}, in {len(_in.get(p_, ()))}' for p_ in _pub if len(_out[p_]) < 3 or len(_in.get(p_, ())) < 3]
print('link graph: min out', min(len(v) for v in _out.values()), 'min in', min(len(_in.get(k, ())) for k in _pub))
if _weak: raise SystemExit('LINK GRAPH < 3:\n' + '\n'.join(_weak))
