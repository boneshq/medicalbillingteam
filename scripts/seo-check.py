#!/usr/bin/env python3
"""Validate the generated public site's search and AI discovery surfaces.

Run after `_build/src/build.py`: python scripts/seo-check.py [site-root]
Read-only, standard library only. This does not claim a page is indexed or ranked.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import datetime
import json
import re
import runpy
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.h1_count = 0
        self.canonicals = []
        self.robots = []
        self.ids = []
        self.links = []
        self.schemas = []
        self._schema = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonicals.append(a.get("href", ""))
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content", ""))
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "script" and a.get("type") == "application/ld+json":
            self._schema = []

    def handle_data(self, data):
        if self._schema is not None:
            self._schema.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._schema is not None:
            self.schemas.append("".join(self._schema))
            self._schema = None


def frontmatter_value(source, key):
    """Read only simple scalar fields; no YAML evaluation or build import."""
    match = re.match(r"\A---\r?\n(.*?)\r?\n---", source, re.S)
    if not match:
        return ""
    value = re.search(r"^" + re.escape(key) + r":\s*(.*?)\s*$", match[1], re.M)
    if not value:
        return ""
    return value[1].split(" #", 1)[0].strip().strip("\"'")


def main(root):
    errors, warnings = [], []
    config = json.loads((root / "_build/config.json").read_text(encoding="utf-8"))
    base = config["canonical_base"].rstrip("/")
    pages = {}
    for path in root.rglob("*.html"):
        relative = path.relative_to(root)
        if any(part.startswith((".", "_")) for part in relative.parts):
            continue
        route = "/" + relative.as_posix()
        if route.endswith("index.html"):
            route = route[:-len("index.html")]
        page = pages[route] = Page(path)
        if page.h1_count != 1:
            errors.append(f"{route}: expected one H1, found {page.h1_count}")
        if len(page.canonicals) != 1:
            errors.append(f"{route}: expected one canonical, found {len(page.canonicals)}")
        elif route != "/404.html" and page.canonicals[0] != base + route:
            errors.append(f"{route}: canonical is not the absolute self URL")
        if not page.robots:
            errors.append(f"{route}: missing robots metadata")
        if not page.schemas:
            errors.append(f"{route}: missing structured data")
        for schema in page.schemas:
            try:
                json.loads(schema)
            except json.JSONDecodeError as exc:
                errors.append(f"{route}: invalid JSON-LD: {exc.msg}")
        repeated = [key for key, count in Counter(page.ids).items() if count > 1]
        if repeated:
            warnings.append(f"{route}: duplicate element IDs: {', '.join(repeated)}")

    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    sitemap_urls = [entry.findtext("s:loc", namespaces=namespace) for entry in sitemap]
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append("sitemap.xml: duplicate URLs")
    if not sitemap_urls:
        errors.append("sitemap.xml: empty sitemap")
    for entry in sitemap:
        url = entry.findtext("s:loc", namespaces=namespace) or ""
        path = urlsplit(url).path
        page = pages.get(path)
        if not url.startswith(base + "/") or url != base + path:
            errors.append(f"sitemap.xml: URL is not a canonical site URL: {url}")
        if not page:
            errors.append(f"sitemap.xml: no generated page for {url}")
            continue
        if page.canonicals != [url]:
            errors.append(f"sitemap.xml: canonical mismatch for {url}")
        if any("noindex" in value.lower() for value in page.robots):
            errors.append(f"sitemap.xml: noindex page included: {url}")
        lastmod = entry.findtext("s:lastmod", namespaces=namespace)
        try:
            if datetime.date.fromisoformat(lastmod or "") > datetime.date.today():
                errors.append(f"sitemap.xml: future lastmod for {url}")
        except ValueError:
            errors.append(f"sitemap.xml: invalid lastmod for {url}")

    for route, page in pages.items():
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme not in ("", "http", "https"):
                continue
            if parts.netloc and parts.netloc != urlsplit(base).netloc:
                continue
            if parts.path and not parts.path.startswith("/"):
                continue
            target = parts.path or route
            if parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f"{route}: broken internal fragment {link}")

    full = (root / "llms-full.txt").read_text(encoding="utf-8")
    source_parts = re.split(r"^Source: (https?://\S+)\s*$", full, flags=re.M)
    exported = {source_parts[i]: source_parts[i + 1] for i in range(1, len(source_parts), 2)}
    if len(exported) != (len(source_parts) - 1) // 2:
        errors.append("llms-full.txt: duplicate page sections")
    chat = json.loads((root / "chat-index.json").read_text(encoding="utf-8"))
    chat_urls = {chunk.get("u") for chunk in chat.get("chunks", [])}
    registry = runpy.run_path(str(root / "_build/src/pages.py"))["PAGES"]
    eligible_urls = set()
    for spec in registry:
        url = base + spec["path"]
        source_path = root / "_build/content" / (spec["key"] + ".md")
        if url not in sitemap_urls or not source_path.exists():
            continue
        source = source_path.read_text(encoding="utf-8")
        if spec["kind"] in ("form", "legal", "utility") or frontmatter_value(source, "gated").lower() == "true":
            continue
        eligible_urls.add(url)
        if url not in exported:
            errors.append(f"llms-full.txt: published guide omitted: {url}")
            continue
        if url not in chat_urls:
            errors.append(f"chat-index.json: published guide omitted: {url}")
        heading = re.search(r"^# (.+)$", source, re.M)
        if heading and heading[1] not in exported[url]:
            errors.append(f"llms-full.txt: current H1 missing for {url}")
        modified = frontmatter_value(source, "date_modified")
        if modified:
            date = datetime.date.fromisoformat(modified)
            human = f"{date.strftime('%B')} {date.day}, {date.year}"
            if modified not in exported[url] and human not in exported[url]:
                errors.append(f"llms-full.txt: current modification date missing for {url}")
    for url in sorted(set(exported) - eligible_urls):
        errors.append(f"llms-full.txt: non-public or excluded page exported: {url}")
    for url in sorted(chat_urls - set(exported)):
        errors.append(f"chat-index.json: source URL absent from llms-full.txt: {url}")

    robots = (root / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {base}/sitemap.xml" not in robots:
        errors.append("robots.txt: missing canonical sitemap reference")
    for warning in warnings:
        print("seo-check: WARNING:", warning)
    for error in errors:
        print("seo-check: ERROR:", error)
    if errors:
        print(f"seo-check: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    print(f"seo-check: PASS ({len(pages)} HTML pages, {len(sitemap_urls)} sitemap URLs, {len(eligible_urls)} AI guide sections; {len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    site_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    sys.exit(main(site_root))
