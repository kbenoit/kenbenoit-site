#!/usr/bin/env python3
"""Refresh the software badges on /projects/.

Reads data/software.json (the package list: edit that to add or remove a package) and writes
  data/package_stats.json   CRAN version, CRAN title and downloads in the last month, or the GitHub description for
                            packages not on CRAN, plus the date fetched
  static/bibtex/<pkg>.bib   a BibTeX entry for each package that has a DOI (CRAN's DOI, or JOSS), fetched from doi.org

Standard library only. Run:  python3 _automation/update_packages.py   then rebuild and commit the changed files.
Uses crandb.r-pkg.org, cranlogs.r-pkg.org, api.github.com and doi.org.
"""
import datetime, json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "kenbenoit-site-update-packages"}


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def get_json(url):
    try:
        return json.loads(fetch(url))
    except Exception as e:
        print("  ! failed:", url, str(e)[:60], file=sys.stderr)
        return None


cfg = json.load(open(os.path.join(ROOT, "data", "software.json"), encoding="utf-8"))
stats, bibs = {}, 0
os.makedirs(os.path.join(ROOT, "static", "bibtex"), exist_ok=True)
for g in cfg["groups"]:
    for p in g["packages"]:
        n = p["name"]
        print(n)
        entry = {}
        if p.get("cran"):
            d = get_json(f"https://crandb.r-pkg.org/{n}")
            dl = get_json(f"https://cranlogs.r-pkg.org/downloads/total/last-month/{n}")
            if d:
                entry["version"] = d.get("Version")
                entry["title"] = re.sub(r"\s+", " ", d.get("Title", "")).strip()
            if isinstance(dl, list) and dl:
                entry["downloads_month"] = dl[0].get("downloads")
        elif p.get("github"):
            d = get_json(f"https://api.github.com/repos/{p['github']}")
            if d and d.get("description"):
                entry["title"] = d["description"].strip()
        if p.get("bibtex_doi"):
            try:
                bib = fetch(f"https://doi.org/{p['bibtex_doi']}", {"Accept": "application/x-bibtex"}).strip()
                bib = re.sub(r"^(@\w+)\{[^,]+,", lambda m: f"{m.group(1)}{{{n},", bib, count=1)   # key = package name
                bib = re.sub(r",\s+(\w+=)", r",\n  \1", bib)                                         # one field per line
                bib = re.sub(r"\s*\}\s*$", "\n}", bib)
                open(os.path.join(ROOT, "static", "bibtex", f"{n}.bib"), "w", encoding="utf-8").write(bib + "\n")
                entry["bibtex"] = True
                bibs += 1
            except Exception as e:
                print("  ! no BibTeX:", str(e)[:60], file=sys.stderr)
        stats[n] = entry
out = {"fetched": datetime.date.today().isoformat(), "packages": stats}
json.dump(out, open(os.path.join(ROOT, "data", "package_stats.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"\nWrote data/package_stats.json ({len(stats)} packages) and {bibs} BibTeX files.")
