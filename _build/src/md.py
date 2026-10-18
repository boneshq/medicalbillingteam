"""Tiny Markdown -> HTML converter (no dependencies). Supports headings, paragraphs,
lists, blockquotes, tables, hr, bold/italic/code, links. Raw HTML lines pass through."""
import html, re

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1" loading="lazy">', t)
    def link(m):
        text, url = m.group(1), m.group(2)
        ext = url.startswith('http') and 'medicalbillingteam.com' not in url
        attrs = ' rel="noopener" target="_blank"' if ext else ''
        return f'<a href="{url}"{attrs}>{text}</a>'
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![*\w])\*([^*]+)\*(?!\w)', r'<em>\1</em>', t)
    t = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'<em>\1</em>', t)
    return t

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def convert(src):
    lines = src.replace('\r\n', '\n').split('\n')
    out, i, toc = [], 0, []
    para = []
    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    while i < len(lines):
        ln = lines[i]; s = ln.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith('<') and not s.startswith('<http'):
            flush(); out.append(ln); i += 1; continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            flush(); lvl = len(m.group(1)); txt = m.group(2).strip().rstrip('#').strip()
            lvl = max(lvl, 2)  # page template owns the single H1
            hid = slugify(txt)
            if lvl == 2: toc.append((hid, txt))
            out.append(f'<h{lvl} id="{hid}">{inline(txt)}</h{lvl}>'); i += 1; continue
        if re.match(r'^(-{3,}|\*{3,})$', s):
            flush(); out.append('<hr>'); i += 1; continue
        if s.startswith('>'):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append('<blockquote>' + convert('\n'.join(buf))[0] + '</blockquote>'); continue
        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\|?\s*:?-{2,}', lines[i+1].strip()):
            flush()
            row = lambda r: [c.strip() for c in r.strip().strip('|').split('|')]
            head = row(s); i += 2; body = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                body.append(row(lines[i])); i += 1
            h = ''.join(f'<th>{inline(c)}</th>' for c in head)
            b = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body)
            out.append(f'<div class="table-wrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'); continue
        lm = re.match(r'^([-*+]|\d+[.)])\s+(.*)$', s)
        if lm:
            flush(); ordered = lm.group(1)[0].isdigit(); items = []
            while i < len(lines):
                mm = re.match(r'^\s*([-*+]|\d+[.)])\s+(.*)$', lines[i])
                if mm: items.append(mm.group(2)); i += 1
                elif lines[i].startswith('  ') and lines[i].strip() and items:
                    items[-1] += ' ' + lines[i].strip(); i += 1
                else: break
            tag = 'ol' if ordered else 'ul'
            def item(x):
                x = re.sub(r'^\[( |x)\]\s*', lambda m: '☐ ' if m.group(1) == ' ' else '☑ ', x)
                return f'<li>{inline(x)}</li>'
            out.append(f'<{tag}>' + ''.join(item(x) for x in items) + f'</{tag}>'); continue
        para.append(s); i += 1
    flush()
    return '\n'.join(out), toc

def front_matter(src):
    """Optional YAML-ish front matter between --- lines: key: value pairs."""
    meta = {}
    if src.startswith('---\n'):
        end = src.find('\n---', 4)
        if end != -1:
            for ln in src[4:end].split('\n'):
                if ':' in ln:
                    k, v = ln.split(':', 1); meta[k.strip().lower()] = v.strip().strip('"\'')
            src = src[end+4:].lstrip('\n')
    return meta, src
