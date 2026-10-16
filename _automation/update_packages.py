#!/usr/bin/env python3
"""Refresh the software badges on /projects/.

Reads data/software.json (the package list: edit that to add or remove a package) and writes
  data/package_stats.json   CRAN version, CRAN title and total downloads since 2012, or the GitHub description for
                            packages not on CRAN, the credited co-authors, plus the date fetched
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


def clean_title(t):
    """CRAN puts single quotes around package and software names in titles; drop them for display."""
    t = re.sub(r"[‘'’]([^‘'’]+)[‘'’]", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def authors_from_cran(author_field):
    """Name [roles] pairs from a CRAN `Author` field."""
    return [(m.group(1).strip(), [r.strip() for r in m.group(2).split(",")])
            for m in re.finditer(r"([A-ZÀ-Ý][^\[\],()]*?)\s*\[([^\]]+)\]", author_field)]


def authors_from_description(text):
    """Name, roles pairs from the Authors@R field of a DESCRIPTION file (packages not on CRAN)."""
    m = re.search(r"Authors@R:\s*(.*?)(?=\n[A-Za-z][A-Za-z/@-]*:)", text, re.S)
    out = []
    for pm in re.finditer(r"person\((.*?)\)\s*(?:,|\)|$)", m.group(1) if m else "", re.S):
        s = pm.group(1)
        g = re.search(r'(?:given\s*=\s*)?"([^"]+)"', s)
        f = re.search(r'family\s*=\s*"([^"]+)"', s) or re.search(r'"[^"]+"\s*,\s*"([^"]+)"', s)
        r = re.search(r'role\s*=\s*(c\([^)]*\)|"[^"]*")', s)
        if g and f:
            out.append((f"{g.group(1)} {f.group(1)}", re.findall(r'"([a-z]+)"', r.group(1)) if r else []))
    return out


def coauthors(pkg, group, cran_data):
    """People credited as authors (or maintainer) of the package, other than the site owner. A group can opt out."""
    if group.get("coauthors") is False:
        return None
    if pkg.get("coauthors"):
        return pkg["coauthors"]
    auth = []
    if cran_data:
        auth = authors_from_cran(cran_data.get("Author", ""))
    elif pkg.get("github"):
        for branch in ("master", "main"):
            try:
                auth = authors_from_description(fetch(f"https://raw.githubusercontent.com/{pkg['github']}/{branch}/DESCRIPTION"))
                break
            except Exception:
                continue
    return [n for n, roles in auth if ("aut" in roles or "cre" in roles) and "Benoit" not in n]


cfg = json.load(open(os.path.join(ROOT, "data", "software.json"), encoding="utf-8"))
stats, bibs = {}, 0
os.makedirs(os.path.join(ROOT, "static", "bibtex"), exist_ok=True)
for g in cfg["groups"]:
    for p in g["packages"]:
        n = p["name"]
        print(n)
        entry = {}
        d = None
        if p.get("cran"):
            d = get_json(f"https://crandb.r-pkg.org/{n}")
            dl = get_json(f"https://cranlogs.r-pkg.org/downloads/total/2012-10-01:{datetime.date.today().isoformat()}/{n}")   # all time (the logs begin in October 2012)
            if d:
                entry["version"] = d.get("Version")
                entry["title"] = clean_title(d.get("Title", ""))
            if isinstance(dl, list) and dl:
                entry["downloads_total"] = dl[0].get("downloads")
        elif p.get("github"):
            d = get_json(f"https://api.github.com/repos/{p['github']}")
            if d and d.get("description"):
                entry["title"] = clean_title(d["description"])
        co = coauthors(p, g, d if p.get("cran") else None)
        if co:
            entry["coauthors"] = co
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
