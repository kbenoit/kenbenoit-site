# kenbenoit.net Rebuild: Build Specification

**Status:** Draft v0.1, 15 October 2026. For review by Kenneth Benoit before any build work starts.
**Owner:** Kenneth Benoit
**Build agent:** Claude Code (or another coding agent), working in a new repository

---

## 0. How to use this document

This specification sits on top of Gary King's mysite build prompt:
<https://gking.harvard.edu/mysite/files/ACADEMIC_SITE_PROMPT.md>

The agent must read that prompt in full and follow it, **except where this document overrides it**. Where the two conflict, this document wins. All overrides are collected in §12.

The live site at `kenbenoit.net` (repo `kbenoit/kbenoit-hugo-site`, Hugo 0.110 + Academic 4.8, hosted on Netlify) stays untouched and live throughout the build. It is the source of all content.

---

## 1. Goals

1. **Structure like <https://brandonstewart.org>:** a name-first hero, a featured spotlight, featured publications, a dense filterable publications page with one page per item, and Bio / Teaching / Software / People pages.
2. **Look like <https://muellerstefan.net>:** crisp system typography, near-black text on white, light grey panels, and one deep-blue accent (exact values in §5).
3. **Keep multiple pages.** Do not adopt Stefan's single-page layout.
4. **Preserve every existing URL** (§9). Nothing that is cited, bookmarked or indexed today may return 404.
5. **Low maintenance.** The owner edits Markdown, or asks an agent; there is no theme-upgrade treadmill.

**Non-goals:** a new visual identity drawn at random (skip the mysite design quest, §12), comments, analytics, or a newsletter.

---

## 2. Repository, platform and hosting

| Item | Decision |
|---|---|
| Repository | **New** repo, suggested name `kbenoit/kenbenoit-site`. The old repo becomes an archive after cut-over. |
| Generator | Hugo **extended**, pinned to an exact version (use the version mysite currently specifies; King's site runs 0.160.1). Pin it in `netlify.toml` and in a `.hugo-version` note. |
| Theme | Hugo Blox `blox-tailwind` v0.10.0 via Go module, **vendored** in `_vendor/` (as mysite requires) |
| Search | Pagefind, with its index built at deploy time |
| Hosting | **Netlify** (override of mysite's GitHub Pages). The build command runs Hugo, then Pagefind. |
| Domain | `https://kenbenoit.net/`, with `baseURL` hard-coded (never derived from a CI variable) |
| Branch previews | Netlify deploy previews on pull requests |
| Security headers | Carry over the `[[headers]] for = "/*"` block from the old `netlify.toml`: `X-Content-Type-Options`, `X-Frame-Options = SAMEORIGIN`, `Referrer-Policy`, `Strict-Transport-Security`, `Permissions-Policy` |
| Redirects | Netlify `_redirects` file generated from `data/redirects.yaml` (§9) |

### 2.1 Git workflow (overrides mysite's "commit and push to main")

- **Never commit or push directly to `main`.** `main` changes only by merging a pull request that the owner has approved.
- **One branch per phase** (§13), named `phase-1-design`, `phase-2-publications` and so on. Small fixes within a phase go on that phase's branch.
- **Open a pull request at the end of each phase.** Its description gives:
  - what changed
  - the Netlify deploy-preview link
  - desktop and 375px mobile screenshots
  - anything flagged for the owner's decision
- **The owner merges, not the agent.** The agent may push to its own phase branches without asking.
- **Netlify setup:** builds `main` for production and builds deploy previews for pull requests. Until the cut-over (Phase 5), the Netlify site uses its `*.netlify.app` address only. **Do not attach kenbenoit.net** without the owner's explicit go-ahead.
- **Never** force-push, rewrite history on `main`, or delete branches the owner hasn't merged.
- **Keep this specification in the repo** as `docs/build-spec.md`. If a decision changes, update the spec in the same pull request.

---

## 3. Owner facts (source of truth: `Kenneth_Benoit_CV.docx`)

- **Name:** Kenneth Benoit (navbar brand: `KENNETH BENOIT`)
- **Title:** Dean, School of Social Sciences, and Lee Kong Chian Professor of Computational Social Science
  - The Lee Kong Chian title runs 2026–2027 only (its endowment expires July 2027). Put it in **one** front-matter field (`params.owner.title`) so it can be changed back in one edit.
- **Institution:** Singapore Management University, linked to <https://socsc.smu.edu.sg>
- **Address:** School of Social Sciences, 10 Canning Rise, Singapore Management University, Singapore 179873
- **Email:** kbenoit@smu.edu.sg
- **Profiles:**
  - Google Scholar `hp1p9TEAAAAJ`
  - GitHub `kbenoit`
  - X/Bluesky `@kenbenoit`
  - Stack Overflow (user 4158274)
- **Photo:** `content/authors/admin/avatar.jpg` from the old repo (2048×2048)
- **Favicon:** `assets/images/icon.png` from the old repo (already a crop of the new photo)
- **CV PDF:** `/pdfs/KenBenoitCV.pdf`, exported from the Word CV. Keep this exact path.
- **Bio text:** reuse `content/authors/admin/_index.md` from the old repo, keeping the owner's wording (mysite §14.7, "preserve the owner's voice").

---

## 4. Information architecture

### 4.1 Navbar

Brand on the left, links on the right, search icon (mysite navbar rules apply):

`KENNETH BENOIT` · Bio · Publications · Software · Teaching · People · Blog · CV · 🔍

- **CV** links straight to `/pdfs/KenBenoitCV.pdf`, as on Stefan's site.
- **Research Areas** isn't a separate page; it is a section of the home page, linked as `/#research-areas` from the hero.

### 4.2 Pages

| Page | URL | Content |
|---|---|---|
| Home | `/` | Hero (§6.1), project spotlight (§6.2), research areas (§6.3), featured publications (§6.4) |
| Bio | `/bio/` | Full bio, academic positions, education, service, grants and awards (merging the old `/cv/` sub-pages) |
| Publications | `/publication/` | Filterable list (§7), plus `/publication/<slug>/` for each item |
| Software | `/software/` | One card per package (§8.2) |
| Teaching | `/teaching/` | From the CV teaching section, plus links to course pages in the blog archive |
| People | `/people/` | Current post-doc, PhD alumni, post-doc alumni, then co-authors (§8.3) |
| Blog | `/posts/` (keep the existing path) | 58 posts with their original URLs (§8.4) |

---

## 5. Visual design: Stefan Müller's tokens

**Skip the mysite design quest.** The owner has supplied reference sites, and the prompt itself says to skip the quest in that case. Implement these tokens in `assets/css/custom.css`:

```css
:root {
  --color-bg: #ffffff;
  --color-surface: #f5f5f5;      /* panels, sidebar, spotlight band */
  --color-text: #121212;
  --color-text-muted: #6d665f;
  --color-border: #e5e5e5;
  --color-accent: #23559f;       /* deep blue: buttons, active tab, rules */
  --color-link: #23559f;
  --color-link-hover: #43961c;   /* green hover, as on Stefan's site */
  --color-accent-2: #516c5b;
  --color-accent-bright: #3b86c8;
  --color-institution: TBD;      /* SMU brand colour; look up the official value. Use sparingly or omit (decision 5, §14). */
  --shadow-soft: 0 16px 40px rgba(45, 41, 38, 0.08);
  --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-hyperlegible: "Atkinson Hyperlegible", var(--font-sans);
}
```

- **Body text:** `--font-sans` (the system font stack). It is crisp because it uses each platform's own font.
- **Headings and the brand:** `--font-hyperlegible`, self-hosted as `.woff2` files (400, 400 italic, 700 and 700 italic) under `static/fonts/`. The font is under the SIL Open Font License; no Google Fonts call.
- **Font size:** normal (`L` in Blox terms) with generous line height. **No cream or off-white backgrounds**; the page is plain white.
- **Spotlight band:** `--color-surface`.
- **Buttons:** one style, either solid accent or accent outline, used consistently.
- **Light mode only:** force light mode as mysite requires.
- **Accessibility:** all text must meet WCAG AA contrast. Check the muted colour on the surface colour.

---

## 6. Home page (modelled on brandonstewart.org)

### 6.1 Hero

- **Layout:** photo on the left (rounded square or circle, about 200px), with text on the right.
- **Text, in order:**
  1. An eyebrow line with the institution, `SINGAPORE MANAGEMENT UNIVERSITY`
  2. The name, as the `h1`
  3. The title
  4. A 3–4 sentence bio
- **Buttons, all in one style:** Download CV · Email · Google Scholar · GitHub
- **Mobile:** the photo stacks above the text.

### 6.2 Project spotlight (like Brandon's featured book)

- One featured item at a time, set in `data/spotlight.yaml` so it's easy to swap.
- **Default:** the LLM research programme. Lead with the AJPS 2026 paper, "Using Large Language Models to Analyze Political Texts Through Natural Language Understanding", plus West European Politics 2026 and the quallmer package.
- **Alternate:** quanteda, if the owner prefers.

### 6.3 Research areas

These are collapsible accordions, as mysite specifies. Each area shows 3–5 featured items and a "View all →" link to the publications list filtered to that area.

**Proposed areas (owner to confirm or rename):**

1. **Large language models and political text:** AJPS 2026, WEP 2026, quallmer, LSE Public Policy Review 2024, Asian Management Insights 2025
2. **Text as data: measurement and scaling:** Wordscores (APSR 2003), crowd-sourcing (APSR 2016), Treating Words as Data with Error (AJPS 2009), textual complexity (AJPS 2019), Lowe et al. (LSQ 2011), validating latent traits (PA 2013)
3. **Party competition and policy positions:** *Party Policy in Modern Democracies*, expert surveys, the European Parliament, dimensionality (EUP 2012), the Basic Arithmetic of legislative decisions (AJPS 2015)
4. **Electoral systems and institutions:** Electoral Laws as Political Consequences (ARPS 2007), Models of Electoral System Change, Duverger, Hungary, Poland
5. **Campaign spending and elections:** Benoit & Marsh, AJPS 2008, PRQ 2010, Party Politics 2003
6. **Open-source software for text analysis:** quanteda (JOSS 2018), tokenizers, readtext, spacyr, quallmer

Tag each publication with one or more area slugs listed in `data/research_areas.json`.

### 6.4 Featured publications

- **Six to eight items,** set by `featured: true` in front matter.
- **Each shows:** venue, year, an award badge where applicable, title and authors.

**Suggested items:**
- AJPS 2026 (LLMs)
- APSR 2016 (crowd-sourcing)
- AJPS 2019 (sophistication)
- JOSS 2018 (quanteda)
- APSR 2003 (Wordscores)
- AJPS 2009 (words as data with error)
- JOP 2009 (Gulbenkian Prize)
- ARPS 2007

---

## 7. Publications

### 7.1 Inventory (from the old `content/cvs/publications.md`)

| Old section | Count | `publication_types` | Tab |
|---|---:|---|---|
| Articles | 59 | `journal_article` | Articles |
| Books | 2 | `book` | Books |
| Book Chapters | 15 | `book_chapter` | Chapters |
| Software and Datasets | 4 | `software` / `data` | Software & Data |
| Other | 9 | `report` / `other` | Other |
| Working Papers | 5 | `report` | Working Papers |
| Conference/unpublished | a few | `report` | Working Papers |

Tabs, each showing a live count as on Brandon's site: **All · Articles · Books · Chapters · Software & Data · Working Papers · Other**

### 7.2 One page per item, at `/publication/<slug>/`

- **Slug:** `<firstauthor>-<year>-<short-title>` in kebab-case, e.g. `benoit-2026-llms-political-texts`. Once live, a slug never changes.
- **Front matter,** following mysite's shared shape:
  - `title`, `date`, `authors` (full names, owner as `Kenneth Benoit`), `publication_types`, `publication` (venue, volume(issue): pages), `abstract`
  - `links`, `tags`, `research_areas`, `featured`, `award`
- **Abstracts:** fetch from Crossref where available; otherwise leave blank. **Do not write abstracts.**
- **DOIs:** the old site's DOIs were checked against Crossref in October 2026; reuse them.

**`links` buttons, in this order:**
1. **PDF:** the existing local file at `/pdfs/<filename>`. **Do not move or rename it.**
2. **Publisher's Version:** `https://doi.org/<doi>`
3. **Replication:** the Dataverse DOI, or a local `/files/<zip>`
4. **Appendix** and **Slides,** where they exist

**Award badges:**
- Gulbenkian Prize 2011 (JOP 2009, Wiesehomeier & Benoit)
- APSA Best Research Software Award 1998 (EzI)
- APSA Best Research Web Site Award 1999 (ROAD)

### 7.3 List-page features

Implement all of mysite's required list-page features:
- sticky tabs
- sidebar search
- research-area filter
- year filter
- sort
- "X of Y results"
- BibTeX export of the visible results
- URL hash sync
- dense citation rows
- server-rendered HTML

Add Brandon's per-entry theme-tag chips.

### 7.4 Cover images

**Override of mysite.** Do not scrape journal cover images.

- Use **book covers only** (*Party Policy in Modern Democracies*; *Intra-Party Politics and Coalition Governments*).
- Use the publisher's image, credited in the page's front matter.

---

## 8. Other content

### 8.1 Bio page

Merge these old pages:
- `content/authors/admin/_index.md` (bio)
- `content/cvs/qualifications.md`
- `content/cvs/service.md`
- `content/cvs/grants-and-awards.md`

Put them under headings: Positions · Education · Service · Grants · Awards.

**Do not** bring back the Conferences and Presentations page. It is archived on purpose (`archive/conferences.md` in the old repo).

### 8.2 Software

Cards, each with a description, links (site · GitHub · CRAN) and its related paper:
- **quanteda,** with its companion packages quanteda.textmodels, .textstats and .textplots: <https://quanteda.io>
- **readtext:** <https://readtext.quanteda.io>
- **spacyr:** <https://spacyr.quanteda.io>
- **quallmer** (with Seraphine F. Maerz): <https://quallmer.github.io/quallmer/>
- **Legacy:** Wordscores (Stata, no longer hosted) and EzI (<https://gking.harvard.edu/ezi>), in a compact "Earlier software" list

### 8.3 People

**Override of mysite.** The People page must exist, but don't build it purely from co-authors.

1. **Current post-doc:** Jinshuai Ma
2. **PhD alumni:** from `content/associates/associates.md`, keeping its links and affiliations, which were checked in October 2026
3. **Post-doc alumni:** from the same file
4. **Co-authors:** generated automatically from publication `authors:` lists, as mysite describes. Show names only, with no guessed links.

The agent must **not** add guessed links for co-authors without showing the owner a list to approve.

### 8.4 Blog

- **Migrate all 58 posts** from `content/post/*.md`.
- **Keep each post's `url:` front matter exactly,** e.g. `/quantitative-text-analysis-tcd-2018/`.
- **Preserve each post's date, title and categories.**
- **Don't migrate the `.rmd` source files.** The Markdown versions are the published ones.
- **Course pages** (e.g. `essex2013qta`, `tcd2018qta`) are blog posts: keep them, and link to them from the Teaching page under "Course materials (archive)".

---

## 9. URL preservation: hard requirement

### 9.1 Static files: copy verbatim, same paths

| Path | Size | Notes |
|---|---|---|
| `/pdfs/**` | 161 MB | Paper PDFs and the CV; keep every filename, including oddities like `fistful30nov2007.pdf.pdf` |
| `/files/**` | 6 MB | Replication zips, restored October 2026. Note that the old repo's `.gitignore` ignores `*.zip`, so these were added with `git add -f`; don't inherit that rule. |
| `/assets/**` | 200 MB | Course materials and blog images. A candidate for archiving to Zenodo or OSF later, but not part of this build. |
| `/cmp/**` | | CMP `.dta` files |
| `/post/**` | | R Markdown figure output used by the blog |

### 9.2 Page redirects (301, in `data/redirects.yaml` → `_redirects`)

| Old | New |
|---|---|
| `/cv/` | `/bio/` |
| `/cvs/qualifications/`, `/cvs/service/`, `/cvs/grants-and-awards/`, `/cvs/teaching/` | `/bio/` (with an anchor for each section), `/teaching/` |
| `/cvs/publications/` | `/publication/` |
| `/cvs/conferences/` | `/bio/` |
| `/associates/` | `/people/` |
| `/current/` | `/#research-areas` |
| `/author/ken-benoit/` | `/bio/` |
| `/software/`, `/posts/`, blog post URLs | Unchanged |

### 9.3 Acceptance test

1. Crawl the **old** site's built output: every HTML page plus every file under `static/`.
2. Request each path from the new site's deploy preview.
3. **Each must return 200, or 301 to a page that returns 200.**
4. Include the script in the repo as `_automation/check_legacy_urls.py`, and run it in CI on every deploy preview.

---

## 10. Search and AI visibility

Implement mysite's "AI & Search Visibility" section in full:
- `https://` everywhere
- `robots.txt` with the sitemap
- `llms.txt`
- Google Scholar `citation_*` tags and `ScholarlyArticle` JSON-LD on every publication page
- all content in the HTML
- crawler verification with `curl`

`citation_pdf_url` must point to the existing `/pdfs/` path, so Google Scholar keeps its existing "[PDF] kenbenoit.net" associations.

---

## 11. Explicitly excluded

- **Disqus** or any comments
- **Analytics,** unless the owner chooses a privacy-friendly option (Stefan uses Plausible)
- **Netlify CMS** or Decap
- **The mysite design quest**
- **The "Record this build with the mysite team" step:** the owner's choice; skip unless asked
- **Third-party copyrighted readings,** already removed from the old site
- **Participant email addresses** in the 2013 workshop post, already stripped

---

## 12. Overrides of the mysite prompt (summary)

| mysite says | This build does | Why |
|---|---|---|
| Host on GitHub Pages | **Netlify** | Existing domain, headers and deploy previews; avoids moving DNS |
| Run the design quest (random draw) | **Skip it**; use §5 | Owner supplied reference sites |
| PDFs in `static/files/` | **Keep `/pdfs/` and `/files/` paths as they are** | URL preservation (mysite §14.4 agrees) |
| Scrape journal cover images | **Book covers only** | Copyright and visual noise |
| People page from co-authors only | **Students and post-docs first,** then co-authors (names only) | Matches the old Associates page; avoids wrong guessed links |
| "Match the legacy site's structure" (scraping section) | **New structure** (§4), old URLs redirected | Owner asked for a redesign |
| "Commit and push to main" | **Phase branches and pull requests;** the owner merges (§2.1) | Each phase is reviewed on a preview before going live |

---

## 13. Build phases and review points

| Phase | Work | Owner review |
|---|---|---|
| 0 | New repo, Hugo and Blox vendored, Netlify site wired to a deploy-preview URL (not the domain) | n/a |
| 1 | Design tokens, navbar, home hero, one sample publication page | **Screenshots, desktop and 375px mobile.** Approve the look before going further. |
| 2 | Publication records for all ~94 items, list page with filters | Spot-check 10 entries; confirm research-area tags |
| 3 | Bio, Software, Teaching, People, Blog migration, static files | Review People and Bio |
| 4 | Redirects, legacy URL check, search and AI checks, accessibility check | Read the URL check report |
| 5 | **Cut-over:** point kenbenoit.net at the new Netlify site, then re-run the URL check against production | Owner gives the go-ahead |

Rollback means pointing the domain back to the old Netlify site.

---

## 14. Decisions needed from the owner before Phase 1

1. **Research areas (§6.3):** accept, rename, merge or add.
2. **Spotlight default (§6.2):** the LLM programme or quanteda.
3. **Featured publications (§6.4):** confirm the list.
4. **Photo shape:** circle (Brandon) or rounded square (Stefan).
5. **SMU institution colour:** use it as a subtle second accent, or don't use it.
6. **Analytics:** none, or Plausible.
7. **Repository name,** and whether it is public or private. Netlify builds either; your current site repo is public.
