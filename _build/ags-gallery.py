#!/usr/bin/env python3
"""Real AGS office/team photos -> responsive WebP for the Featured Vendor gallery.

  python3 _build/ags-gallery.py [SRC]      (default SRC: /workspace/alliance-global/medbill/ags-images)

Only files listed in _build/ags-gallery-select.json are used (curated: REAL AGS photos only; never AI images of
people as staff, never stock, never logos). Missing files are skipped, so the gallery handles 0..N images.
Writes _build/static/img/ags/*.webp and _build/ags-gallery.json ({"office": [...], "team": [...]})."""
import json, re, sys, pathlib, warnings
from PIL import Image, ImageOps
warnings.filterwarnings('ignore')
B = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/workspace/alliance-global/medbill/ags-images')
SEL = json.loads((B / 'ags-gallery-select.json').read_text()) if (B / 'ags-gallery-select.json').exists() else {}
OUT = B / 'static' / 'img' / 'ags'
OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob('*.webp'): old.unlink()
WIDTHS = {'office': (640, 1000), 'team': (320, 480)}
res = {}
for group in ('office', 'team'):
    res[group] = []
    for i, it in enumerate(SEL.get(group, [])):
        f = SRC / it['file']
        if not f.exists(): continue
        try: im = ImageOps.exif_transpose(Image.open(f))
        except Exception as e: print('skip', f.name, e); continue
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (247, 245, 240)); bg.paste(im, mask=im.split()[-1]); im = bg
        else: im = im.convert('RGB')
        if group == 'team':   # uniform 4:5 portrait crop, top-weighted
            im = ImageOps.fit(im, (min(im.width, 800), round(min(im.width, 800) * 1.25)), Image.LANCZOS, centering=(0.5, 0.2))
        stem = f'{group}-{i + 1:02d}'
        sizes = []
        for w in WIDTHS[group]:
            if im.width < w and sizes: continue
            r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            r.save(OUT / f'{stem}-{w}.webp', 'WEBP', quality=78, method=6); sizes.append([w, r.width, r.height])
        res[group].append({'stem': stem, 'sizes': sizes, 'alt': it['alt'], 'caption': it.get('caption', '')})
(B / 'ags-gallery.json').write_text(json.dumps(res, indent=1))
print({k: len(v) for k, v in res.items()}, 'gallery images; total KB', sum(p.stat().st_size for p in OUT.glob('*.webp')) // 1024)
