# Automation

Checks that run on every pull request (`.github/workflows/checks.yml`) and on every Netlify deploy preview
(`netlify.toml`). All are plain Python 3 with no dependencies.

| Script | What it checks |
|---|---|
| `check_legacy_urls.py` | Every page and static file the old kenbenoit.net served returns 200, or a 301 to a page that does. The inventory is `legacy_urls.txt` (568 paths, built from the old site in October 2026). |
| `check_ai_visibility.py` | `robots.txt`, `sitemap.xml` (all https), `llms.txt`, and Google Scholar `citation_*` tags plus ScholarlyArticle JSON-LD on every publication page. |

| `update_packages.py` | Refreshes the software badges on /projects/: CRAN versions and monthly downloads into `data/package_stats.json`, the credited co-authors of each package (shown as "with ..."), and a BibTeX entry per package into `static/bibtex/`. Set `"coauthors": [...]` on a package in `data/software.json` to override the names, or `"coauthors": false` on a group to show none. Not a check; run it by hand (or on a schedule), rebuild, and commit the changed files. |

```bash
hugo --gc --minify && npx pagefind --site public
python3 _automation/check_legacy_urls.py --dir public
python3 _automation/check_ai_visibility.py --dir public
# against a deployed site or deploy preview:
python3 _automation/check_legacy_urls.py --url https://deploy-preview-7--kenbenoit-site.netlify.app
python3 _automation/check_ai_visibility.py --url https://kenbenoit.net
```

## Adding or removing a package

Edit `data/software.json` (name, whether it is on CRAN, GitHub repository, documentation site, DOI), then run `python3 _automation/update_packages.py`.

## Adding a redirect

Add a line to `data/redirects.yaml` (`from`, `to`). The build writes it into `_redirects`. Run the legacy check to confirm.

## Accessibility

Last checked with axe-core (WCAG 2.0/2.1 A and AA plus best practices) on 14 page types at desktop and 375px width:
see `docs/reports/accessibility-check.md`. To repeat, serve `public/`, load `axe.min.js` from the `axe-core` npm package in the browser
and call `axe.run()`.
