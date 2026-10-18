#!/usr/bin/env python3
"""Static build for medicalbillingteam.com -> writes the site to the REPO ROOT (GitHub Pages: main, /).

  python3 _build/src/build.py                  # preview build: links prefixed with /medicalbillingteam (GitHub Pages project URL)
  BASE_PATH= python3 _build/src/build.py       # custom-domain build (after CNAME cutover): root-relative links

Noindex switch: _build/config.json "indexing_enabled". While false, EVERY page ships
<meta name="robots" content="noindex,nofollow">. Flip to true only after Tony's okay."""
import json, os, re, shutil, html, datetime, pathlib, yaml
from pages import PAGES, NAV
from md import convert, front_matter

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
SPEC_SECTIONS = re.compile(r'^(short form|sticky cta|footer$|form fields|implementation notes|other ways to reach us)', re.I)

def load(p):
    f = B / 'content' / f"{p['key']}.md"
    p.update(ready=False, body='', sections=[], toc=[], faqs=[], raw='')
    if not f.exists(): return
    txt = f.read_text()
    meta = {}
    if txt.startswith('---\n'):
        end = txt.find('\n---', 4)
        meta = yaml.safe_load(txt[4:end]) or {}
        txt = txt[end + 4:].lstrip('\n')
    if str(meta.get('status', '')).lower() == 'stub' or not txt.strip(): return
    p['ready'] = True
    if meta.get('title'): p['title'] = meta['title']
    if meta.get('meta_description'): p['description'] = meta['meta_description']
    p['faqs'] = [(x['q'], x['a']) for x in (meta.get('faq') or []) if x.get('q') and x.get('a')]
    p['schema_types'] = meta.get('schema_type') or []
    m = re.search(r'^#\s+(.+)$', txt, re.M)
    if m: p['h1'] = m.group(1).strip(); txt = txt[:m.start()] + txt[m.end():]
    txt = re.sub(r'^\*Disclosure:.*\*\s*$', '', txt, flags=re.M)          # footer carries it
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)                        # build notes
    # split into H2 sections; drop build-spec sections
    parts = re.split(r'^(?=##\s)', txt, flags=re.M)
    keep = []
    for part in parts:
        hm = re.match(r'##\s+(.+)', part)
        if hm and (SPEC_SECTIONS.match(hm.group(1).strip()) or hm.group(1).strip() in CFG.get('hold_sections', {})): continue
        keep.append(part)
    p['intro'] = keep[0] if keep and not keep[0].lstrip().startswith('##') else ''
    p['sections'] = [s for s in keep if s.lstrip().startswith('##')]
    clean = '\n'.join(keep).strip()
    clean = re.sub(r'\n-{3,}\s*$', '', clean)
    p['raw'] = clean
    p['body'], p['toc'] = convert(clean)

for p in PAGES:
    load(p)
    if p['kind'] in ('utility',): p['ready'] = True
    p['indexable'] = p['ready'] and p['kind'] != 'utility'

def url(p): return SITE + p['path']

# ---------------- partials ----------------
def ga():
    gid = CFG.get('ga4_measurement_id', '')
    if not gid or 'X' in gid:
        return '<!-- GA4 placeholder: set _build/config.json ga4_measurement_id (G-...) after Tony creates the web stream -->'
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{gid}");</script>')

def jsonld(p):
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": CFG['site_name'], "url": SITE + "/",
           "logo": SITE + "/logo.svg", "description": DISC,
           "parentOrganization": {"@type": "Organization", "name": "Alliance Global Solutions", "url": "https://www.allianceglobalsolutions.com/"}}
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
                  "datePublished": TODAY, "dateModified": TODAY,
                  "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}})
    if p['faqs']:
        g.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                  "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faqs']]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + '</script>'

def head(p):
    robots = 'index, follow, max-image-preview:large' if (INDEX and p['indexable']) else 'noindex, nofollow'
    title = p['title']
    og = SITE + '/og-default.png'
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
<meta name="theme-color" content="#0b4f8a">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
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
<a class="brand" href="/"><img src="/logo.svg" alt="" width="28" height="28"><span>Medical Billing <b>Team</b></span></a>
<nav class="nav-desk" aria-label="Main"><ul class="nav">{items}</ul></nav>
<a class="btn btn-sm hdr-cta" href="/contact/">Free assessment</a>
<details class="menu"><summary aria-label="Open menu">Menu</summary><nav aria-label="Mobile"><ul class="nav">{items}<li><a href="/contact/">Free assessment</a></li></ul></nav></details>
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
    btn = 'Request my free assessment' if full else 'Request my assessment'
    return f'''<form class="lead-form lead-{form_id}" id="{'assessment' if form_id=='hero' else 'form-'+form_id}" method="post" novalidate
 data-tcpa-version="{E(CFG['tcpa_version'])}" data-thanks="/thank-you/">
<input type="hidden" name="form_id" value="{form_id}">
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<div class="grid{' grid-2' if full else ''}">{''.join(rows)}</div>
{tcpa}{help_html}
<p class="phi" role="note"><strong>Do not include any patient information.</strong> {E(CFG['phi_notice'].split('. ',1)[1])}</p>
{f'<p class="fine">{E(CFG["email_notice"])}</p>' if full else ''}
<button class="btn" type="submit">{btn}</button>
<p class="form-msg" role="status" aria-live="polite"></p>
<p class="fine">We'll email you within one business day. No patient information, please.</p>
</form>'''

def ags_block(p):
    links = CFG['ags_links'].get(p['key']) or CFG['ags_links'].get('_default', [])
    if not links: return ''
    li = ''.join(f'<li><a href="{E(u)}" rel="noopener">{E(t)}</a></li>' for t, u in links)
    return f'<aside class="related-ext"><h2>About the staffing provider behind this site</h2><p>{E(CFG["ags_intro"])}</p><ul>{li}</ul></aside>'

def footer(p):
    links = ''.join(f'<li><a href="{BYKEY[k]["path"]}">{E(BYKEY[k]["label"])}</a></li>' for k in
        ['about', 'how-it-works', 'hipaa-outsourced-medical-billing', 'faq', 'checklist', 'contact', 'privacy', 'terms'])
    def grp(pk):
        kids = ''.join(f'<li><a href="{c["path"]}">{E(c["label"])}</a></li>' for c in PAGES if c['parent'] == pk)
        return f'<div><h3><a href="{BYKEY[pk]["path"]}">{E(BYKEY[pk]["label"])}</a></h3><ul>{kids}</ul></div>'
    band = '' if p['key'] in ('contact', 'thank-you') else f'''<section class="cta-band" id="footer-cta"><div class="wrap cta-grid">
<div><h2>Short on billing staff?</h2><p>Get a free, no-obligation staffing assessment. No patient info needed.</p></div>
{form("footer")}</div></section>'''
    sticky = '' if p['key'] in ('contact', 'thank-you') else f'''<div class="sticky-cta" hidden><span class="s-m">Free billing staffing assessment</span><span class="s-d">Short on billing staff? Get a free, no-obligation staffing assessment. No patient info needed.</span>
<a class="btn btn-sm" href="{'#assessment' if p['key']=='index' else '/contact/'}">Get started</a><button class="x" type="button" aria-label="Dismiss">×</button></div>'''
    return f'''{band}
<footer class="site-footer"><div class="wrap">
<div class="fcols">{grp('medical-billing-staffing')}{grp('revenue-cycle-management-staffing')}<div><h3>Site</h3><ul>{links}</ul></div></div>
<p class="disclosure"><strong>Disclosure:</strong> {E(DISC)} <a href="/about/">About &amp; disclosure</a></p>
<p class="fine">Please do not submit patient information through this site. Content is general information, not legal, compliance or financial advice. © {datetime.date.today().year} {E(CFG['site_name'])}</p>
</div></footer>{sticky}
<script src="/form-config.js" defer></script><script src="/form.js" defer></script></body></html>'''

def stub(p):
    return f'''<div class="placeholder"><p><strong>Copy pending.</strong> This guide is being written. Until it is published, this page is a stub
(noindex, not in the sitemap or llms.txt).</p><p>Topic: {E(p['description'])}</p></div>'''

def crumbs(p):
    parts = ['<a href="/">Home</a>']
    if p['parent']: parts.append(f'<a href="{BYKEY[p["parent"]]["path"]}">{E(BYKEY[p["parent"]]["label"])}</a>')
    parts.append(f'<span aria-current="page">{E(p["label"])}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">›</span> '.join(parts) + '</nav>'

def children(p):
    kids = [c for c in PAGES if c['parent'] == p['key']]
    if not kids: return ''
    cards = ''.join(f'<a class="card" href="{c["path"]}"><h3>{E(c["label"])}</h3><p>{E(c["description"])}</p></a>' for c in kids)
    return f'<section class="kids"><h2>Guides in this section</h2><div class="cards">{cards}</div></section>'

def siblings(p):
    if not p['parent']: return ''
    par = BYKEY[p['parent']]
    li = ''.join(f'<li><a href="{c["path"]}">{E(c["label"])}</a></li>' for c in PAGES if c['parent'] == p['parent'] and c['key'] != p['key'])
    return f'<aside class="related"><h2>More in <a href="{par["path"]}">{E(par["label"])}</a></h2><ul>{li}</ul></aside>'

def page_main(p):
    h1 = p.get('h1', p['title'].split(' | ')[0])
    if p['key'] == 'contact':
        intro = convert(p['intro'])[0] if p['ready'] else '<p>Tell us about your practice and a billing staffing specialist will follow up. No patient information.</p>'
        rest = convert('\n'.join(p['sections']))[0] if p['sections'] else ''
        body = intro + form('full') + rest
    elif p['key'] == 'thank-you':
        body = ('<p>Thank you. We\'ve received your request. A staffing specialist will email you, usually within one business day.</p>'
                '<p>In the meantime: <a href="/checklist/">Medical Billing Health Checklist</a> · <a href="/hipaa-outsourced-medical-billing/">HIPAA guide for outsourced billing staff</a> · <a href="/revenue-cycle-management-staffing/">RCM staffing guide</a></p>')
    else:
        body = p['body'] if p['ready'] else stub(p)
    toc = ''
    if len(p['toc']) >= 4 and p['kind'] in ('pillar', 'cluster'):
        toc = '<details class="toc" open><summary>On this page</summary><ul>' + ''.join(f'<li><a href="#{i}">{E(t)}</a></li>' for i, t in p['toc'] if t.lower() != 'faq') + '</ul></details>'
    faq = ''
    if p['faqs'] and not re.search(r'^##\s+FAQ', p['raw'], re.M | re.I):
        faq = '<section class="faq"><h2>FAQ</h2>' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p['faqs']) + '</section>'
    elif p['faqs']:
        faq = '<section class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p['faqs']) + '</section>'
    return f'''<main id="main" class="wrap narrow">{crumbs(p)}<article><h1>{E(h1)}</h1>
<p class="disclosure-inline">{E(DISC)}</p>{toc}
<div class="prose">{body}{faq}</div></article>{children(p)}{siblings(p)}{ags_block(p) if p['kind'] in ('pillar','cluster') or p['key']=='about' else ''}</main>'''

def home_main(p):
    if p['ready']:
        hero = convert(p['intro'])[0]
        secs = []
        for s in p['sections']:
            h = re.match(r'##\s+(.+)', s).group(1)
            inner = convert(s)[0]
            cls = 'hipaa-band' if 'hipaa' in h.lower() else 'band'
            secs.append(f'<section class="{cls}"><div class="wrap narrow prose">{inner}</div></section>')
        rest = ''.join(secs)
    else:
        hero = stub(p); rest = ''
    rcm = ''.join(f'<li><a href="{c["path"]}">{E(c["label"])}</a></li>' for c in PAGES if c['parent'] == 'revenue-cycle-management-staffing')
    mbs = ''.join(f'<li><a href="{c["path"]}">{E(c["label"])}</a></li>' for c in PAGES if c['parent'] == 'medical-billing-staffing')
    topics = f'''<section class="band topics"><div class="wrap"><h2>Explore by topic</h2><div class="cards">
<div class="card"><h3><a href="/medical-billing-staffing/">Medical billing staffing</a></h3><ul class="pills">{mbs}</ul></div>
<div class="card"><h3><a href="/revenue-cycle-management-staffing/">RCM staffing</a></h3><ul class="pills">{rcm}</ul></div>
<div class="card"><h3><a href="/hipaa-outsourced-medical-billing/">HIPAA &amp; outsourcing</a></h3><p>BAAs, minimum necessary, access controls and what to ask any agency.</p></div>
<div class="card"><h3><a href="/medical-billing-staffing-cost/">Cost comparisons</a></h3><p>In-house vs. billing company vs. dedicated remote staff.</p></div>
</div></div></section>'''
    return f'''<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div class="hero-form"><h2 class="form-title">Get your free staffing assessment</h2>{form("hero")}</div>
<div class="hero-h"><p class="eyebrow">For US medical practices &amp; billing companies</p><h1>{E(p.get('h1', p['title']))}</h1></div>
<div class="hero-copy prose">{hero}<p class="disclosure-inline">{E(DISC)}</p></div>
</div></section>
{topics}{rest}
<section class="band"><div class="wrap narrow">{ags_block(p)}</div></section>
</main>'''

# ---------------- write ----------------
gen_file = B / 'generated.json'
old = json.loads(gen_file.read_text()) if gen_file.exists() else []
for rel in old:
    t = ROOT / rel
    if t.is_dir(): shutil.rmtree(t)
    elif t.exists(): t.unlink()
generated = []
for f in (B / 'static').iterdir():
    shutil.copy2(f, ROOT / f.name); generated.append(f.name)

def prefix(h):
    if not BASE_PATH: return h
    return re.sub(r'(\b(?:href|src|action|data-thanks)=")/(?!/)', rf'\1{BASE_PATH}/', h)

for p in PAGES:
    rel = p['path'].strip('/')
    d = ROOT / rel if rel else ROOT
    d.mkdir(parents=True, exist_ok=True)
    main = home_main(p) if p['key'] == 'index' else page_main(p)
    (d / 'index.html').write_text(prefix(head(p) + nav(p['key']) + main + footer(p)))
    generated.append(rel.split('/')[0] if rel else 'index.html')

# 404
nf = dict(BYKEY['thank-you'], key='thank-you', title='Page not found', label='Not found', path='/404.html')
(ROOT / '404.html').write_text(prefix(head(nf).replace(f'href="{SITE}/404.html"', f'href="{SITE}/"') + nav('thank-you') +
    '<main id="main" class="wrap narrow"><h1>Page not found</h1><p><a href="/">Go to the home page</a> or <a href="/contact/">request a free staffing assessment</a>.</p></main>' + footer(BYKEY['thank-you'])))
generated.append('404.html')

idx = [p for p in PAGES if p['indexable']]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in idx) + '</urlset>\n')
# robots.txt: MSD (boneshq/microschool-directory) pattern, adapted
bots = CFG['ai_crawlers']
(ROOT / 'robots.txt').write_text('# medicalbillingteam.com — open to all crawlers and AI assistants\n'
    '# (Preview/staging pages are kept out of indexes with <meta name="robots" content="noindex,nofollow">, not here.)\n'
    'User-agent: *\nAllow: /\nDisallow: /thank-you/\n\n# Major AI / LLM crawlers explicitly welcomed\n'
    + ''.join(f'User-agent: {b}\nAllow: /\n' for b in bots) + f'\nSitemap: {SITE}/sitemap.xml\n')

def line(p): return f'- [{p["title"].split(" | ")[0]}]({url(p)}): {p["description"]}'
L = [f'# {CFG["site_name"]}', '', f'> {CFG["llms_summary"]}', '',
     'medicalbillingteam.com publishes plain-English guides for US medical practices and medical billing companies on staffing billing and revenue cycle work: in-house vs. outsourced vs. dedicated remote or offshore staff, RCM roles and KPIs, HIPAA safeguards for outsourced staff, and costs.', '',
     '## Disclosure', DISC, '',
     '## Key facts', '- Audience: US medical practices, specialty groups, multi-location groups and medical billing companies',
     '- Topics: medical billing staffing, remote/offshore billers, RCM staffing, HIPAA and outsourcing, cost comparisons',
     '- Lead form: practice-level details only; the site never asks for patient information (PHI)',
     '- Operator: Alliance Global Solutions (https://www.allianceglobalsolutions.com/), a provider of remote staff based in the Philippines', '']
groups = [('Medical billing staffing', lambda p: p['key'] == 'medical-billing-staffing' or p['parent'] == 'medical-billing-staffing'),
          ('RCM staffing', lambda p: p['key'] == 'revenue-cycle-management-staffing' or p['parent'] == 'revenue-cycle-management-staffing'),
          ('HIPAA and costs', lambda p: p['key'] in ('hipaa-outsourced-medical-billing', 'medical-billing-staffing-cost')),
          ('About and help', lambda p: p['key'] in ('index', 'how-it-works', 'faq', 'checklist', 'about', 'contact', 'privacy', 'terms'))]
for g, fn in groups:
    rows = [line(p) for p in idx if fn(p)]
    if rows: L += [f'## {g}', ''] + rows + ['']
L += ['Full text of published guides: ' + SITE + '/llms-full.txt', 'Full URL list: ' + SITE + '/sitemap.xml', '',
      'This site welcomes citation by AI assistants and search engines.', '']
(ROOT / 'llms.txt').write_text('\n'.join(L))
FT = [f'# {CFG["site_name"]} — full text of published pages', '', f'> {CFG["llms_summary"]}', '', f'Disclosure: {DISC}', '']
for p in idx:
    if not p['raw']: continue
    FT += ['', '---', '', f'# {p.get("h1", p["title"])}', '', f'URL: {url(p)}', '', p['raw'].strip()]
    if p['faqs']: FT += ['', '## FAQ', ''] + [f'**{q}**\n{a}\n' for q, a in p['faqs']]
(ROOT / 'llms-full.txt').write_text('\n'.join(FT) + '\n')
(ROOT / '.nojekyll').write_text('')
fb = CFG['form_backend']
fc = {'mode': fb['mode'], 'enabled': bool(fb['enabled']), 'supabaseUrl': fb['supabase_url'], 'table': fb['table'], 'appsScriptUrl': fb['apps_script_url']}
lines = ['/* generated by _build/src/build.py from _build/config.json form_backend */', 'window.MBT_FORM = ' + json.dumps(fc) + ';']
if fb.get('supabase_anon_key'):
    lines.append('window.MBT_FORM.anonKey = ' + json.dumps(fb['supabase_anon_key']) + '; // secretscan:allow public Supabase anon key (role=anon, insert-only RLS), same pattern as MSD front end')
(ROOT / 'form-config.js').write_text('\n'.join(lines) + '\n')
generated.append('form-config.js')
generated += ['sitemap.xml', 'robots.txt', 'llms.txt', 'llms-full.txt', '.nojekyll']
gen_file.write_text(json.dumps(sorted(set(generated)), indent=1))
status = {'built': datetime.datetime.now().isoformat(timespec='seconds'), 'base_path': BASE_PATH, 'indexing_enabled': INDEX,
          'form_backend_enabled': CFG['form_backend']['enabled'],
          'live_ready': [p['path'] for p in PAGES if p['ready'] and p['kind'] != 'utility'],
          'stubs': [p['path'] for p in PAGES if not p['ready']]}
(B / 'build-status.json').write_text(json.dumps(status, indent=1))
print(json.dumps(status, indent=1))
