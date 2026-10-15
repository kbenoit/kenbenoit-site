#!/usr/bin/env python3
"""Check the search and AI-visibility requirements of docs/build-spec.md section 10.

  python3 _automation/check_ai_visibility.py --dir public
  python3 _automation/check_ai_visibility.py --url https://kenbenoit.net      (also fetches as GPTBot, ClaudeBot, Googlebot)

Checks: robots.txt welcomes crawlers and lists an https sitemap; sitemap.xml is all https and every entry exists;
llms.txt exists with the key URLs; every publication page has Google Scholar citation_* tags and valid
ScholarlyArticle/Book JSON-LD with a plain-text abstract; citation_pdf_url points at an existing /pdfs/ file.
Exit status 1 on any failure.
"""
import argparse, glob, html, json, os, re, sys, urllib.request, urllib.error, urllib.parse

ap = argparse.ArgumentParser()
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--dir"); g.add_argument("--url")
ap.add_argument("--report")
a = ap.parse_args()
fails, notes = [], []


def ok(cond, msg):
    (notes if cond else fails).append(("PASS " if cond else "FAIL ") + msg)


def fetch(path, ua="Mozilla/5.0 (compatible; check_ai_visibility)"):
    if a.dir:
        p = a.dir.rstrip("/") + urllib.parse.unquote(path)
        if p.endswith("/"): p += "index.html"
        return (200, open(p, encoding="utf-8", errors="replace").read()) if os.path.isfile(p) else (404, "")
    req = urllib.request.Request(a.url.rstrip("/") + path, headers={"User-Agent": ua})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


# robots.txt
st, robots = fetch("/robots.txt")
ok(st == 200, "robots.txt exists")
ok(re.search(r"(?im)^user-agent:\s*\*", robots) is not None, "robots.txt has User-agent: *")
ok(not re.search(r"(?im)^user-agent:\s*(gptbot|claudebot|perplexitybot|ccbot|google-extended)", robots), "robots.txt has no blocks aimed at AI crawlers")
ok(re.search(r"(?im)^sitemap:\s*https://", robots) is not None, "robots.txt lists an https Sitemap")
ok("llms.txt" in robots, "robots.txt points to /llms.txt")
disallows = re.findall(r"(?im)^disallow:\s*(\S+)", robots)

# sitemap
st, sm = fetch("/sitemap.xml")
ok(st == 200, "sitemap.xml exists")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
ok(len(locs) > 100, f"sitemap has {len(locs)} URLs")
ok(all(l.startswith("https://") for l in locs), "every sitemap <loc> starts with https://")
ok(not any(urllib.parse.urlparse(l).path.startswith(d) for l in locs for d in disallows), "no sitemap URL is disallowed by robots.txt")
if a.dir:
    missing = [l for l in locs if fetch(urllib.parse.urlparse(l).path)[0] != 200]
    ok(not missing, f"every sitemap URL exists in the build ({len(missing)} missing)" + (": " + ", ".join(missing[:5]) if missing else ""))

# llms.txt
st, llms = fetch("/llms.txt")
ok(st == 200 and llms.startswith("# "), "llms.txt exists with a title")
for key in ("/bio/", "/publication/", "/projects/", "/teaching/", "/pdfs/KenBenoitCV.pdf"):
    ok(key in llms, f"llms.txt links {key}")

# publication pages
if a.dir:
    pages = sorted(glob.glob(a.dir.rstrip("/") + "/publication/*/index.html"))
    pages = [p for p in pages if not p.endswith("/page/index.html")]
else:
    pages = [None]
bad = []
for p in pages:
    path = "/publication/" + os.path.basename(os.path.dirname(p)) + "/" if p else "/publication/benoit-2026-llms-political-texts/"
    st, t = fetch(path)
    errs = []
    if "name=citation_title" not in t and 'name="citation_title"' not in t: errs.append("no citation_title")
    if not re.search(r'name="?citation_author"?', t): errs.append("no citation_author")
    if not re.search(r'name="?citation_publication_date"?', t): errs.append("no citation_publication_date")
    blocks = re.findall(r'<script type="?application/ld\+json"?>(.*?)</script>', t, re.S)
    ld = None
    for b in blocks:
        try:
            d = json.loads(b)
            if isinstance(d, dict) and d.get("@type") in ("ScholarlyArticle", "Book"): ld = d
        except Exception:
            errs.append("invalid JSON-LD")
    if ld is None: errs.append("no ScholarlyArticle/Book JSON-LD")
    elif re.search(r"&(amp|lt|gt|quot|#\d+);|<[a-z]+>", ld.get("abstract", "")): errs.append("abstract has HTML/entities")
    m = re.search(r'name="?citation_pdf_url"? content="?([^">\s]+)', t)
    if m and a.dir:
        pp = urllib.parse.urlparse(m.group(1)).path
        if not os.path.isfile(a.dir.rstrip("/") + urllib.parse.unquote(pp)): errs.append("citation_pdf_url file missing")
    if errs: bad.append((path, errs))
ok(not bad, f"{len(pages)} publication page(s) have valid Scholar tags and JSON-LD" + ("" if not bad else f" ({len(bad)} with problems)"))
for path, errs in bad[:10]: fails.append(f"FAIL   {path}: {', '.join(errs)}")

# fetched as crawlers (live only)
if a.url:
    for ua in ("GPTBot", "ClaudeBot", "PerplexityBot", "Googlebot"):
        sts = [fetch(p, ua)[0] for p in ("/", "/publication/", "/llms.txt")]
        ok(all(s == 200 for s in sts), f"fetchable as {ua}")

out = ["# Search and AI-visibility check", "", f"Target: `{a.dir or a.url}`", ""] + [f"- {l}" for l in notes + fails] + ["", "**FAIL**" if fails else "**PASS**"]
print("\n".join(out))
if a.report: open(a.report, "w", encoding="utf-8").write("\n".join(out) + "\n")
sys.exit(1 if fails else 0)
