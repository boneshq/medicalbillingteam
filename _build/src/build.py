#!/usr/bin/env python3
"""Static build for medicalbillingteam.com -> writes the site to the REPO ROOT (GitHub Pages: main, /).

  python3 _build/src/build.py                  # preview build: links prefixed with /medicalbillingteam (GitHub Pages project URL)
  BASE_PATH= python3 _build/src/build.py       # custom-domain build (after CNAME cutover): root-relative links

Noindex switch: _build/config.json "indexing_enabled". While false, EVERY page ships
<meta name="robots" content="noindex,nofollow">. Flip to true only after Tony's okay."""
import json, os, re, shutil, html, datetime, pathlib, yaml
from pages import PAGES, NAV
from md import convert, front_matter
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
AFF = CFG['affiliation']   # SLOT: final wording ~4 PM ET
GALLERY = json.loads((B / 'ags-gallery.json').read_text()) if (B / 'ags-gallery.json').exists() else {}
ASSET_V = datetime.datetime.now().strftime('%Y%m%d%H%M')
BAA_Q = 'Does Alliance Global Solutions sign a BAA?'
BAA_LINE = 'Alliance Global Solutions signs a BAA before any PHI access.'  # approved copy addition (Tony via Alliance Global, 2026-10-18); HIPAA page disclosure only
SPEC_SECTIONS = re.compile(r'^(short form|sticky cta|footer$|form fields|implementation notes|other ways to reach us|get the checklist)', re.I)
FAQ_HEAD = re.compile(r'^(short )?faq$', re.I)
BYLINE_RE = re.compile(r'^\*By the Medical Billing Team editors.*\*\s*$', re.M)
COPY_FIXES = [  # minimal wording fixes applied on top of AG copy (approved via Alliance Global 2026-10-18 1:03 PM ET)
    ("so if it adds agency staff, the agency becomes a **subcontractor business associate**, and HHS says a business associate must have a BAA with its subcontractor before disclosing PHI to it",
     "so if it brings in staff from an outside agency, that agency generally becomes the billing company's **subcontractor business associate**. As a general rule, HHS says a business associate must have a BAA with its subcontractor before disclosing PHI to it"),
]
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
    p['vendor'] = meta.get('vendor') or {}
    p['steps'] = meta.get('steps') or []
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
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)                        # build notes
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
    p['indexable'] = p['ready'] and p['kind'] != 'utility' and not p.get('draft') and not p.get('slot') and 'noindex' not in p.get('robots_fm', '')

def url(p): return SITE + p['path']

# ---------------- partials ----------------
def ga():
    gid = CFG.get('ga4_measurement_id', '')
    if not gid or 'X' in gid:
        return '<!-- GA4 placeholder: set _build/config.json ga4_measurement_id (G-...) after Tony creates the web stream -->'
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{gid}");</script>')

# Home and featured-vendor FAQs must be different (each has its own FAQPage); fail the build on any shared question.
_norm = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
for _v in [x for x in PAGES if x['kind'] == 'vendor']:
    _dup = {_norm(q) for q, _ in BYKEY['index']['faqs']} & {_norm(q) for q, _ in _v['faqs']}
    if _dup: raise SystemExit(f'DUPLICATE FAQ between home and {_v["path"]}: {sorted(_dup)}')

def jsonld(p):
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": CFG['site_name'], "url": SITE + "/",
           "logo": SITE + "/logo.svg", "description": DISC,
           "sameAs": ["https://www.allianceglobalsolutions.com/"], "parentOrganization": {"@type": "Organization", "name": "Alliance Global Solutions", "url": "https://www.allianceglobalsolutions.com/"}}
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
        g[-1]["mainEntity"] = {"@type": "Organization", "name": p['vendor']['name'], "url": p['vendor'].get('website'),
                               "description": p['vendor'].get('tagline')}
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
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + '</script>'

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

def nav(cur):
    def a(lbl, k):
        on = cur == k or BYKEY[cur]['parent'] == k
        return f'<li><a href="{BYKEY[k]["path"]}"{" aria-current=\"page\"" if on else ""}>{E(lbl)}</a></li>'
    items = ''.join(a(l, k) for l, k in NAV)
    bar = '' if INDEX else '<div class="staging-bar">Preview build: not indexed. Pages marked “copy pending” are stubs.</div>'
    return f'''<body class="pg-{cur}">{bar}<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap hdr">
<a class="brand" href="/"><img src="/logo.svg" alt="" width="30" height="30"><span>Medical Billing <b>Team</b></span></a>
<nav class="nav-desk" aria-label="Main"><ul class="nav">{items}</ul></nav>
<a class="btn btn-sm hdr-cta" href="/contact/">Free assessment</a>
<details class="menu"><summary aria-label="Open menu"><span class="burger" aria-hidden="true"></span>Menu</summary><nav aria-label="Mobile"><ul class="nav">{items}<li><a href="/contact/">Free assessment</a></li></ul></nav></details>
</div></header>'''

F = CFG['form']
def sel(name, label, opts, required=True):
    o = ''.join(f'<option>{E(x)}</option>' for x in opts)
    return f'<label><span>{E(label)}{"" if required else " <i>(optional)</i>"}</span><select name="{name}"{" required" if required else ""}><option value="">Select…</option>{o}</select></label>'
def inp(name, label, typ='text', required=True, ac='', hint='', maxl=150):
    h = f'<small>{E(hint)}</small>' if hint else ''
    return f'<label><span>{E(label)}{"" if required else " <i>(optional)</i>"}</span><input name="{name}" type="{typ}"{" required" if required else ""} maxlength="{maxl}"{f" autocomplete={chr(34)}{ac}{chr(34)}" if ac else ""}>{h}</label>'

def form(form_id):
    fb = CFG['form_backend']
    full = form_id == 'full'
    rows = [inp('name', 'Your name', ac='name', maxl=100)]
    if full: rows.append(sel('role', 'Your role', F['roles']))
    rows += [inp('practice_name', 'Practice or company name', ac='organization')]
    if full: rows.append(sel('specialty', 'Specialty', F['specialties']))
    rows.append(sel('num_providers', 'Number of providers', F['providers']))
    if full:
        rows += [sel('monthly_collections', 'Monthly collections range', F['collections']),
                 sel('billing_setup', 'Current billing setup', F['setups'])]
    rows.append(inp('work_email', 'Work email', 'email', ac='email', hint='Please use your practice or company email.'))
    rows.append(inp('phone', 'Phone', 'tel', required=False, ac='tel', hint="Only if you'd like a call or text.", maxl=30))
    help_html = ''
    if full:
        boxes = ''.join(f'<label class="chip"><input type="checkbox" name="help_areas" value="{E(x)}"> {E(x)}</label>' for x in F['help_areas'])
        help_html = f'<fieldset class="chips"><legend>Where do you need help? <i>(optional)</i></legend>{boxes}</fieldset>'
    tcpa = (f'<label class="check tcpa" hidden><input type="checkbox" name="tcpa_consent" value="yes"> '
            f'<span>{E(CFG["tcpa_text"])} See our <a href="/privacy/">Privacy Policy</a> and <a href="/terms/">Terms</a>.</span></label>')
    btn = 'Send me the checklist' if form_id == 'checklist' else 'Request my assessment'
    return f'''<form class="lead-form lead-{form_id}" id="{'assessment' if form_id=='hero' else 'form-'+form_id}" method="post" novalidate
 data-tcpa-version="{E(CFG['tcpa_version'])}" data-thanks="{'#unlocked' if form_id == 'checklist' else '/thank-you/'}">
<input type="hidden" name="form_id" value="{form_id}">
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<div class="grid{' grid-2' if full else ''}">{''.join(rows)}</div>
{tcpa}{help_html}
<p class="phi" role="note"><strong>Do not include any patient information.</strong> {E(CFG['phi_notice'].split('. ',1)[1])}</p>
{f'<p class="fine">{E(CFG["email_notice"])}</p>' if full else ''}{'<p class="fine">We\'ll email you the checklist and occasional guides about billing staffing. Unsubscribe any time.</p>' if form_id == 'checklist' else ''}
<button class="btn btn-cta" type="submit">{btn}{ico('arrow-right')}</button>
<p class="form-msg" role="status" aria-live="polite"></p>
<p class="fine"><span class="em-note">We'll email you within one business day. No patient information, please. </span><span class="affil">{E(AFF['short'])} <a href="/about/#affiliation">Disclosure</a></span></p>
</form>'''

def ags_block(p):
    links = []
    if not links: return ''
    li = ''.join(f'<li><a href="{E(u)}" rel="noopener">{E(t)}</a></li>' for t, u in links)
    return f'<aside class="related-ext"><h2>About the staffing provider behind this site</h2><p>{E(CFG["ags_intro"])}</p><ul>{li}</ul></aside>'

def footer(p):
    links = ''.join(f'<li><a href="{BYKEY[k]["path"]}">{E(BYKEY[k]["label"])}</a></li>' for k in
        ['about', 'how-it-works', 'hipaa-outsourced-medical-billing', 'medical-billing-staffing-cost', 'behavioral-health-billing', 'faq', 'checklist', 'contact', 'privacy', 'terms'])
    def grp(pk):
        kids = ''.join(f'<li><a href="{c["path"]}">{E(c["label"])}</a></li>' for c in PAGES if c['parent'] == pk)
        return f'<div><h2 class="fh"><a href="{BYKEY[pk]["path"]}">{E(BYKEY[pk]["label"])}</a></h2><ul>{kids}</ul></div>'
    band = '' if p['key'] in ('contact', 'thank-you') else f'''<section class="cta-band" id="footer-cta"><div class="wrap cta-grid">
<div><h2>Short on billing staff?</h2><p>Get a free, no-obligation staffing assessment. No patient info needed.</p></div>
{form("footer")}</div></section>'''
    sticky = '' if p['key'] in ('contact', 'thank-you') else f'''<div class="sticky-cta" hidden><span class="s-m">Free billing staffing assessment</span><span class="s-d">Short on billing staff? Get a free, no-obligation staffing assessment. No patient info needed.</span>
<a class="btn btn-sm" href="{'#assessment' if p['key']=='index' else '/contact/'}">Get my free assessment</a><button class="x" type="button" aria-label="Dismiss">×</button></div>'''
    return f'''{band}
<footer class="site-footer"><div class="wrap">
<div class="fcols"><div><h2 class="fh">Guides</h2><ul>{''.join(f'<li><a href="{BYKEY[k]["path"]}">{E(BYKEY[k]["label"])}</a></li>' for k in ['hire-remote-medical-billers', 'revenue-cycle-management-staffing', 'hipaa-outsourced-medical-billing', 'medical-billing-staffing-cost', 'behavioral-health-billing'])}</ul></div>{grp('revenue-cycle-management-staffing')}<div><h2 class="fh">Site</h2><ul>{links}</ul></div></div>
<p class="disclosure"><strong>Disclosure:</strong> {E(DISC)} {E(AFF['full'])} <a href="/about/#affiliation">About &amp; disclosure</a></p>
<p class="fine">Please do not submit patient information through this site. Content is general information, not legal, compliance or financial advice. © {datetime.date.today().year} {E(CFG['site_name'])}</p>
</div></footer>{sticky}
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

def affil_box(cls=''):
    return f'<div class="affil-box {cls}" id="affiliation" role="note">{ico("handshake")}<p>{E(AFF["full"])}</p></div>'

def vendors():
    return [v for v in PAGES if v['kind'] == 'vendor' and v['vendor']]

def vendor_card(v):
    d = v['vendor']
    sv = ''.join(f'<li>{ico("check")}{E(s)}</li>' for s in d.get('services', [])[:5])
    loc = f'<p class="vc-meta">{ico("map-pin")}Staff location: {E(d["staff_location"])}</p>' if d.get('staff_location') else ''
    return f"""<article class="vendor-card"><p class="vc-tag">{E(d.get('label') or 'Approved vendor')} · Billing &amp; RCM staff</p>
<h3><a href="{v['path']}">{E(d['name'])}</a></h3><p class="vc-line">{E(d.get('tagline', ''))}</p>
<ul class="vc-list">{sv}</ul>{loc}<p class="vc-meta">{ico("file-signature")}{E(d.get('baa', ''))}</p>
<p class="vc-aff">{ico("handshake")}Affiliated: operates this site. <a href="/about/#affiliation">Disclosure</a></p>
<a class="btn btn-sm vc-go" href="{v['path']}">View vendor profile{ico('arrow-right')}</a></article>"""

def empty_slot():
    # Plainly labeled empty state; must never look like a real vendor (Tony via CEO 2026-10-18)
    return """<div class="vendor-empty"><p class="ve-h">More vetted vendors coming</p>
<p>We add a vendor only after it passes <a href="/how-we-vet-vendors/">our vetting checks</a>. No other vendors are listed yet.</p></div>"""

def directory_block(head='Approved vendor directory', lead=True):
    cards = ''.join(vendor_card(v) for v in vendors()) + empty_slot()
    intro = ('<p class="dir-lead">Vendors listed here passed <a href="/how-we-vet-vendors/">our vetting checks</a>. '
             'Alliance Global Solutions, which operates this site, is the only approved vendor today.</p>') if lead else ''
    return f'<section class="directory" id="directory"><h2>{E(head)}</h2>{intro}<div class="vendor-grid">{cards}</div></section>'

def gallery_html():
    off, team = GALLERY.get('office', []), GALLERY.get('team', [])
    if not off and not team:
        return '' if INDEX else '<section class="vp-gallery empty"><p class="slot-note"><strong>Photo slot.</strong> Real Alliance Global Solutions office and team photos will appear here.</p></section>'
    def img(it, sizes, lazy=True):
        ss = ', '.join(f'/img/ags/{it["stem"]}-{w}.webp {w}w' for w, _, _ in it['sizes'])
        w0, h0 = it['sizes'][0][1], it['sizes'][0][2]
        return (f'<img src="/img/ags/{it["stem"]}-{it["sizes"][0][0]}.webp" srcset="{ss}" sizes="{sizes}" alt="{E(it["alt"])}" '
                f'width="{w0}" height="{h0}" {"loading=\"lazy\" " if lazy else ""}decoding="async">')
    o = ''.join(f'<figure class="g-{"lead" if i == 0 else "item"}">{img(it, "(min-width:960px) 560px, 100vw" if i == 0 else "(min-width:960px) 280px, 50vw", lazy=i > 0)}'
                f'{("<figcaption>" + E(it["caption"]) + "</figcaption>") if it.get("caption") else ""}</figure>' for i, it in enumerate(off))
    tm = ''.join(f'<li>{img(it, "(min-width:960px) 160px, 30vw")}</li>' for it in team)
    o_html = f'<div class="g-office g-n{min(len(off), 5)}">{o}</div>' if off else ''
    t_html = f'<h3 class="g-h">The team</h3><ul class="g-team">{tm}</ul>' if team else ''
    return f'<section class="vp-gallery" aria-labelledby="vp-photos"><h2 id="vp-photos">Inside Alliance Global Solutions</h2>{o_html}{t_html}<p class="g-note">Photos supplied by Alliance Global Solutions.</p></section>'

def vendor_main(p):
    d = p['vendor']
    ts = d.get('team_size_range') or ''
    ts_row = (f'<div><dt>{ico("users-round")}Team size range</dt><dd>{E(ts)}</dd></div>' if ts else
              ('' if INDEX else f'<div class="slot"><dt>{ico("users-round")}Team size range</dt><dd><em>Slot: pending confirmation</em></dd></div>'))
    facts = (f'<dl class="vp-facts"><div><dt>{ico("briefcase-medical")}Services</dt><dd>{E(", ".join(d.get("services", [])))}</dd></div>'
             f'<div><dt>{ico("map-pin")}Staff location</dt><dd>{E(d.get("staff_location", ""))}</dd></div>'
             f'<div><dt>{ico("file-signature")}HIPAA</dt><dd>{E(d.get("baa", ""))}</dd></div>{ts_row}'
             f'<div><dt>{ico("handshake")}Listing</dt><dd>Affiliated vendor (operates this site). <a href="#affiliation">Disclosure</a></dd></div></dl>')
    steps = ''.join(f'<li><p class="step-k">Step {i + 1}</p><h3>{E(s["t"])}</h3><p>{E(s.get("d", ""))}</p></li>' for i, s in enumerate(p['steps']))
    body = convert(p['intro'])[0] if p.get('intro') else ''
    if p['sections']: body += convert('\n'.join(x for x in p['sections'] if not x.startswith('<!--FAQ-->')))[0]
    web = f'<a class="btn btn-ghost" href="{E(d["website"])}" rel="noopener" target="_blank">Visit website{ico("external-link")}</a>' if d.get('website') else ''
    return f"""<main id="main" class="vendor-page">
<section class="vp-hero"><div class="wrap">{crumbs(p)}{slot_note(p)}<div class="vp-grid">
<div class="vp-id"><p class="eyebrow vp-eye">{ico("badge-check")}{E(d.get('label') or 'Featured vendor')} · Approved</p>
<h1>{E(d['name'])}</h1><span class="rule ph-rule" aria-hidden="true"><i></i><i></i><i></i></span>
<p class="vp-tag">{E(d.get('tagline', ''))}</p>
<div class="vp-cta"><a class="btn btn-cta" href="/contact/">Request help{ico("arrow-right")}</a>{web}</div></div>
<div class="vp-card">{facts}</div></div></div></section>
<div class="wrap vp-body">{affil_box('vp-affil')}
{gallery_html()}
<section class="vp-about prose">{body}</section>
{f'<section class="vp-steps" aria-labelledby="vp-how"><h2 id="vp-how">How working with {E(d["name"])} works</h2><ol class="steps-list">{steps}</ol></section>' if steps else ''}
<section class="vp-cta-band"><div><h2>Talk to {E(d['name'])}</h2><p>Get a free, no-obligation staffing assessment. No patient information needed.</p></div><a class="btn btn-cta" href="/contact/">Get my free assessment{ico("arrow-right")}</a></section>
{faq_html(p, 'Questions about ' + d['name']) if p['faqs'] else ''}
{siblings(p)}</div></main>"""

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
        body = ('<p>Thank you. We\'ve received your request. A staffing specialist will email you, usually within one business day.</p>'
                '<p>In the meantime: <a href="/checklist/">Medical Billing Health Checklist</a> · <a href="/hipaa-outsourced-medical-billing/">HIPAA guide for outsourced billing staff</a> · <a href="/revenue-cycle-management-staffing/">RCM staffing guide</a></p>')
    elif p.get('gated'):
        body = (convert(p['intro'])[0] + '<div class="gate form-card"><h2>Get the checklist</h2>' + form('checklist') +
                ('' if bool(CFG['form_backend'].get('apps_script_url')) else '<p class="fine preview-note">Preview only: the form backend is off, so the gate can\'t unlock. <button type="button" class="linkbtn" data-unlock>Show the gated content</button> (preview reviewers only).</p>') +
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
    body = enhance(body)
    if p['key'] == 'about':   # affiliation disclosure (positioning change 2026-10-18): right under the operator disclosure heading
        body = re.sub(r'(<h2 id="disclosure-who-operates-this-site">.*?</h2>)', lambda m: m.group(1) + affil_box(), body, count=1, flags=re.S) if 'disclosure-who-operates-this-site' in body else affil_box() + body
    disc = f'<p class="disclosure-inline">{ico("building-2")}<span>{E(DISC)}{(" " + E(BAA_LINE)) if p["key"] == "hipaa-outsourced-medical-billing" else ""}</span></p>'
    icon = PAGE_ICON.get(p['key'])
    badge = f'<span class="page-ic">{ico(icon)}</span>' if icon else ''
    return f"""<main id="main"><div class="page-hero"><div class="wrap">{crumbs(p)}{slot_note(p)}<div class="ph-row">{badge}<h1>{E(h1)}</h1></div><span class="rule ph-rule" aria-hidden="true"><i></i><i></i><i></i></span>
{byline(p)}{disc}</div></div>
<div class="wrap page-grid{' has-toc' if toc else ''}">{('<aside class="toc-col"><div class="toc-stick">' + toc + aside_cta(p) + '</div></aside>') if toc else ''}<article class="prose">{body}</article></div>
<div class="wrap">{directory_block() if p['kind'] == 'directory' else children(p)}{siblings(p)}</div></main>"""

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
            inner = convert(s)[0]
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
{topics}<section class="band band-dir"><div class="wrap">{directory_block()}</div></section>{rest}
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
    main = home_main(p) if p['key'] == 'index' else vendor_main(p) if p['kind'] == 'vendor' else page_main(p)
    (d / 'index.html').write_text(prefix(head(p) + nav(p['key']) + main + footer(p)))
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
shutil.copy2(B / 'content' / 'llms.txt', ROOT / 'llms.txt')
# llms-full.txt: regenerated from published markdown on every build (CODE-DESK #8; logic from medbill/gen/llmsfull.py)
FULL_ORDER = ['index','revenue-cycle-management-staffing','hipaa-outsourced-medical-billing','medical-billing-staffing-cost','hire-remote-medical-billers','denial-management','reduce-ar-days','eligibility-verification-prior-authorization','behavioral-health-billing','ar-specialist','hire-remote-medical-coders','prior-authorization-specialist','credentialing-specialist','virtual-medical-assistant','medical-billing-outsourcing','offshore-medical-billers','how-it-works','faq','about']
FT = ["# Medical Billing Team: full text\n\n> Concatenated public guides from medicalbillingteam.com, generated " + TODAY + ". Operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff. Excludes forms, legal drafts and gated content.\n"]
for k in FULL_ORDER:
    f = B / 'content' / f'{k}.md'
    if not f.exists() or not BYKEY[k]['ready']: continue
    src = f.read_text(); fm, body = src.split('---', 2)[1], src.split('---', 2)[2]
    slug = re.search(r'^slug:\s*"?([^"\n]+)"?', fm, re.M).group(1)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    if k == 'index':
        body = re.sub(r'## Short form \(hero\).*?(?=## Who this site helps)', '', body, flags=re.S)
        body = re.sub(r'## Sticky CTA bar.*', '', body, flags=re.S)
    body = re.sub(r'\]\(/', '](https://medicalbillingteam.com/', body)
    FT.append("\n---\n\nSource: https://medicalbillingteam.com%s\n\n" % slug + body.strip() + "\n")
(ROOT / 'llms-full.txt').write_text(''.join(FT))
(ROOT / '.nojekyll').write_text('')
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
