#!/usr/bin/env python3
"""Check that every URL the old kenbenoit.net served still works on the new site.

A legacy path passes if the new site returns 200 for it, or a 301 to a path that returns 200.

  Local build:   python3 _automation/check_legacy_urls.py --dir public
  Live/preview:  python3 _automation/check_legacy_urls.py --url https://deploy-preview-7--kenbenoit-site.netlify.app

The inventory is _automation/legacy_urls.txt (every page and static file of the old site).
With --dir the redirects in <dir>/_redirects are applied the way Netlify applies them.
Exit status is 1 if any path fails, so it can gate a deploy preview. Use --report FILE for a Markdown report.
"""
import argparse, os, re, sys, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))


def load_inventory(path):
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]


def load_redirects(dirpath):
    rules = []
    f = os.path.join(dirpath, "_redirects")
    if not os.path.exists(f):
        return rules
    for line in open(f, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):   # comments only at line start; '#' elsewhere is a URL fragment
            continue
        parts = line.split()
        if len(parts) >= 2:
            status = parts[2].rstrip("!") if len(parts) > 2 else "301"
            rules.append((parts[0], parts[1], status))
    return rules


class Local:
    def __init__(self, d):
        self.d = d.rstrip("/")
        self.rules = load_redirects(d)

    def exists(self, path):
        p = urllib.parse.unquote(path.split("#")[0].split("?")[0])
        full = self.d + p
        if p.endswith("/"):
            return os.path.isfile(full + "index.html")
        return os.path.isfile(full) or os.path.isfile(full + "/index.html") or os.path.isfile(full + ".html")

    @staticmethod
    def _pattern(src):
        """Netlify rule source -> regex. :name matches one path segment; a trailing * matches the rest (:splat)."""
        out = ""
        for tok in re.split(r"(:[A-Za-z_]+|\*)", src):
            if tok == "*":
                out += "(?P<splat>.*)"
            elif tok.startswith(":") and len(tok) > 1:
                out += "(?P<%s>[^/]+)" % tok[1:]
            else:
                out += re.escape(tok)
        return re.compile("^" + out + "$")

    def redirect(self, path):
        for src, dst, status in self.rules:
            for cand in {path, path.rstrip("/"), path.rstrip("/") + "/"}:
                m = self._pattern(src).match(cand)
                if m:
                    out = dst
                    for k, v in m.groupdict().items():
                        out = out.replace(":" + k, v)
                    return out
        return None

    def check(self, path):
        if self.exists(path):
            return "200", None
        dst = self.redirect(path)
        if dst is None:
            return "MISSING", None
        if dst.startswith("http"):
            return "301→external", dst
        return ("301→200", dst) if self.exists(dst) else ("301→MISSING", dst)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


class Remote:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.opener = urllib.request.build_opener(NoRedirect)

    def get(self, path):
        req = urllib.request.Request(self.base + urllib.parse.quote(path, safe="/%:@&=+$,;~*'()?"), method="GET",
                                     headers={"User-Agent": "legacy-url-check"})
        try:
            r = self.opener.open(req, timeout=30)
            return r.status, r.headers.get("Location")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Location")
        except Exception as e:
            return 0, str(e)

    def check(self, path):
        st, loc = self.get(path)
        if st == 200:
            return "200", None
        if st in (301, 302, 307, 308):
            dst = urllib.parse.urlparse(urllib.parse.urljoin(self.base + path, loc)).path
            if loc and loc.startswith("http") and not loc.startswith(self.base):
                return "301→external", loc
            st2, _ = self.get(dst)
            return ("301→200", dst) if st2 == 200 else ("301→MISSING", dst)
        return "MISSING", None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dir", help="built site directory (e.g. public)")
    g.add_argument("--url", help="base URL of a deployed site or deploy preview")
    ap.add_argument("--inventory", default=os.path.join(HERE, "legacy_urls.txt"))
    ap.add_argument("--report", help="write a Markdown report to this file")
    a = ap.parse_args()
    site = Local(a.dir) if a.dir else Remote(a.url)
    paths = load_inventory(a.inventory)
    results = [(p,) + site.check(p) for p in paths]
    counts = {}
    for _, s, _ in results:
        counts[s] = counts.get(s, 0) + 1
    bad = [r for r in results if r[1] in ("MISSING", "301→MISSING")]
    redirected = [r for r in results if r[1].startswith("301")]
    lines = [f"# Legacy URL check", "", f"Target: `{a.dir or a.url}`  ", f"Checked: {len(paths)} paths from the old site.", "",
             "| Result | Count |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in sorted(counts.items())] + [""]
    lines += ["**PASS: every legacy path returns 200 or redirects to a page that does.**" if not bad else f"**FAIL: {len(bad)} paths do not resolve.**", ""]
    if bad:
        lines += ["## Failing paths", "", "| Old path | Result | Redirect target |", "|---|---|---|"] + [f"| `{p}` | {s} | `{d or ''}` |" for p, s, d in bad] + [""]
    if redirected:
        lines += ["## Redirected paths (301)", "", "| Old path | New path |", "|---|---|"] + [f"| `{p}` | `{d}` |" for p, s, d in redirected] + [""]
    out = "\n".join(lines)
    if a.report:
        open(a.report, "w", encoding="utf-8").write(out + "\n")
    print(out if len(bad) < 40 else "\n".join(lines[:12]) + f"\n... {len(bad)} failing; see report")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
