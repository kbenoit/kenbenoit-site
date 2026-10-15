# kenbenoit.net Rebuild: Build Specification

**Status:** v0.2, 15 October 2026. Owner decisions in §14 are settled; ready for Phase 1.
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

1. **Structure like <https://brandonstewart.org>:** a name-first hero, a projects section, featured publications, a dense filterable publications page with one page per item, and Bio / Projects / Teaching / People pages.
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

`KENNETH BENOIT` · Bio · Projects · Publications · Teaching · People · CV · 🔍

- **CV** links straight to `/pdfs/KenBenoitCV.pdf`, as on Stefan's site.
- **Research Areas** isn't a separate page; it is a section of the home page, reachable at `/#research-areas` (the anchor is kept for the old `/current/` redirect). Owner decision (15 October 2026): no jump link from the hero.

### 4.2 Pages

| Page | URL | Content |
|---|---|---|
| Home | `/` | Hero (§6.1), projects (§6.2), research areas (§6.3), featured publications (§6.4) |
| Bio | `/bio/` | Full bio, academic positions, education, service, grants and awards (merging the old `/cv/` sub-pages) |
| Publications | `/publication/` | Filterable list (§7), plus `/publication/<slug>/` for each item |
| Projects | `/projects/` | Four project pages, plus an "Other software" list (§8.2). Replaces the old `/software/` page. |
| Teaching | `/teaching/` | From the CV teaching section, plus links to course pages in the blog archive |
| People | `/people/` | PhD alumni, post-doc alumni, then co-authors (§8.3) |
| Blog (archive) | `/posts/` (keep the existing path) | 58 posts with their original URLs (§8.4). Owner decision (15 October 2026): not in the menu and not in site search, but every URL stays live. |

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
- **No institutional colour.** Don't use SMU's brand colours: the site should outlast any one appointment. The SMU name and link in the hero are enough.

---

## 6. Home page (modelled on brandonstewart.org)

### 6.1 Hero

- **Layout:** photo on the left, as a **rounded square** (about 200px, modest corner radius, as on Stefan's site; not a circle, which would crop the shoulders of the headshot), with text on the right.
- **Text, in order:**
  1. An eyebrow line with the institution, `SINGAPORE MANAGEMENT UNIVERSITY`
  2. The name, as the `h1`
  3. The title
  4. A 3–4 sentence bio
- **Buttons, all in one style:** Download CV · Email · Google Scholar · GitHub
- **Mobile:** the photo stacks above the text.

### 6.2 Projects (three cards)

Owner decision (15 October 2026): the home page shows three projects as equal cards, set in `data/projects.yaml`, replacing the featured band and four cards originally planned:

1. **AI-Assisted Content Analysis:** the owner's book under contract with Sage, building on quallmer and the work using LLMs.
2. **quanteda:** the quanteda family of R packages for text analysis.
3. **Expert surveys (PPMD):** the Party Policy in Modern Democracies expert survey dataset.

Each card has a thumbnail (64px high, from `assets/projects/`, set per project in the data file), a title, a one-sentence description and a link. The images are the quallmer logo (used for the book), the quanteda logo and the cover of *Party Policy in Modern Democracies*, all supplied by the owner. Until the Projects pages exist (Phase 3), the links go to the projects' own sites. The `/projects/` page (§8.2) should list these three and the other projects (quallmer, LLM research).

### 6.3 Research areas

Owner decision (15 October 2026): research areas and selected publications are one section, **Selected publications**, in the style of Stefan Müller's home page. Each area is a small uppercase heading with three featured items (a monogram tile, the venue in bold italics with the year, and the title as a link) and a "View all N →" link to the publications list filtered to that area. This replaces mysite's accordions and the separate six-item featured list in §6.4. The section keeps the anchor `#research-areas`.

**Areas (decided), in this order:**

| # | Area (slug) | Core items |
|---|---|---|
| 1 | **LLMs and AI** (`llms-ai`) | AJPS 2026, WEP 2026, quallmer, *LSE Public Policy Review* 2024, *Asian Management Insights* 2025 |
| 2 | **Text as data** (`text-as-data`) | Wordscores (APSR 2003), crowd-sourcing (APSR 2016), sophistication (AJPS 2019), validating latent traits (PA 2013), natural sentences (BJPS 2012), social media in the 2014 EP elections (ES 2016), Brexit Twitter (SPP 2017), quanteda (JOSS 2018), tokenizers (JOSS 2018), "Text analysis in R" (CMM 2017), Wordscoring Irish speeches and positions (IPS 2002, 2003) |
| 3 | **Measuring party positions** (`measuring-positions`) | Expert surveys vs. hand coding (ES 2007), *Party Policy in Modern Democracies* (2006), Treating Words as Data with Error (AJPS 2009), coder reliability (PA 2012), scaling coded texts (LSQ 2011), Latin America (JOP 2009), Japan (JJPS 2005), dimensionality (EUP 2012), scaling hand-coded texts (PP 2022), Benchmarks, "Compared to What?", the open-access document archive (GP 2009) |
| 4 | **Party competition** (`party-competition`) | Including the European Parliament and legislatures: EP party groups (BJPS 2010, PP 2007, EUP 2012), Basic Arithmetic (AJPS 2015), evolution of party systems (AJPS 2003), intra-party preferences (PSRM 2017), speaker selection (JOP 2015), France 2002 (EJPR 2006), Irish policy space (ESR 2005), Irish parties and Europe (IPS 2009), *Intra-Party Politics and Coalition Governments* (2008), the EU Convention (EUP 2005) |
| 5 | **Electoral systems** (`electoral-systems`) | Electoral Laws as Political Consequences (ARPS 2007), Models of Electoral System Change (ES 2004), Duverger (FP 2006, ES 2002), district magnitude (EJPR 2001), most proportional formula (PA 2000), voter strategies (BJPS 2006) |
| 6 | **Campaign spending** (`campaign-spending`) | The Campaign Value of Incumbency (AJPS 2008), PRQ 2010, *Party Politics* 2003, IPS 2003 |
| 7 | **Post-communist politics** (`hungary-postcommunist`; renamed from "Hungary and post-communist politics" by the owner, 15 October 2026; the slug is unchanged so links keep working) | Hungary's 1989 electoral law (JTP 2001), Hungary's two-vote system (1996), Hungarian elections 2002 (JCSTP), Hungarian chapters and forecasts, Poland (JOP 2004) |

- **Many items carry two tags,** e.g. Wordscores is both `text-as-data` and `measuring-positions`. List the slugs in `data/research_areas.json`.
- **Some items fit no area** (for example the democratic-peace paper, JCR 1996, and the impact-ranking paper). Leave them untagged; they still appear in the full list.
- **The agent proposes tags for every item,** and the owner spot-checks them in Phase 2.

### 6.4 Featured publications

- **Six items (decided),** set by `featured: true` in front matter, shown in this order.
- **Each shows:** venue, year, an award badge where applicable, title and authors.

1. AJPS 2026: Using Large Language Models to Analyze Political Texts Through Natural Language Understanding
2. WEP 2026: Measuring issue salience for political parties using LLMs
3. APSR 2003: Extracting Policy Positions from Political Texts Using Words as Data
4. LSQ 2011: Scaling Policy Preferences From Coded Political Texts
5. ES 2007: Estimating party policy positions: Comparing expert surveys and hand-coded content analysis
6. APSR 2016: Crowd-Sourced Text Analysis: Reproducible and Agile Production of Political Data

quanteda (JOSS 2018) is not featured here because the quanteda project card already highlights it.

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
3. **Data and Code:** the Dataverse DOI, or a local `/files/<zip>` (a separate **Data** and **Code** link where both exist)
4. **Appendix** and **Slides,** where they exist

**Award badges:**
- Gulbenkian Prize 2011 (JOP 2009, Wiesehomeier & Benoit)
- APSA Best Research Software Award 1998 (EzI)
- APSA Best Research Web Site Award 1999 (ROAD)

### 7.3 List-page features

Modelled on Stefan Müller's list (owner decision, 15 October 2026), replacing mysite's sidebar:
- **Citation lines in the old CV style:** `2026. “Title.” **Journal** 70(4): 1589–1605 (with Co-author, Co-author).` The journal or book title is bold italic at the same size as the title; the owner's name is omitted and co-authors follow as "(with …)".
- **A row of small action links under each citation:** an expandable **Abstract** (where one exists), **PDF**, **Publisher's Version**, **Data and Code**, **Appendix**, and anything else worth linking (for example press coverage such as The Conversation). Any link in the front matter `links:` list appears here.
- Sticky type tabs with live counts, and a strip of **topic pills** (the seven research areas) with live counts. No sidebar and no dropdowns.
- A search field, an "X of Y results" count, and BibTeX export of the visible results.
- URL hash sync (for example `#articles&area=text-as-data`), and server-rendered HTML so the list works without JavaScript.

### 7.4 Cover images

Owner decision (15 October 2026), replacing the original book-covers-only rule:
- The home page's Selected publications show a small portrait thumbnail (48×64px, cropped from the top) for each journal, as on Stefan Müller's site. Covers are the publishers' own images, stored in `assets/covers/` and mapped by venue in `data/journal_covers.yaml` with the publisher credited.
- A journal logo that is square (for example the LSE Public Policy Review, supplied by the owner) is shown 48×48 instead of 48×64. A journal with no usable cover (or only a "cover not available" placeholder) gets a monogram tile of the same size. Delete a mapping to fall back to the monogram.
- Book covers for the two books are still to be added from the publisher, credited in the page's front matter.

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

### 8.2 Projects

The `/projects/` list page shows five projects as cards (the three on the home page first, then quallmer and LLM research, set in `data/projects.yaml`), then an "Other software" list.

**Each project page** (`/projects/<slug>/`) has a short description, links, related publications (pulled automatically from publications that share the project's tag) and an image if available.

| Project (slug) | Content and links |
|---|---|
| **LLM research** (`llm-research`) | The research programme on using LLMs to analyse political texts. AJPS 2026 and WEP 2026, plus *LSE Public Policy Review* 2024 and *Asian Management Insights* 2025 as related writing. Collaborators: Scott De Marchi, Conor Laver, Michael Laver, Jinshuai Ma. |
| **quallmer** (`quallmer`) | R package for qualitative analysis with LLMs, with Seraphine F. Maerz. Site <https://quallmer.github.io/quallmer/> · CRAN <https://cran.r-project.org/package=quallmer>. Related: the 2026 POAL methods brief "Application of LLMs to Qualitative Coding Tasks Using quallmer". |
| **quanteda** (`quanteda`) | The quanteda family: quanteda <https://quanteda.io>, with quanteda.textmodels, .textstats and .textplots; readtext <https://readtext.quanteda.io>; spacyr <https://spacyr.quanteda.io>. Related: JOSS 2018 (quanteda), "Text analysis in R" (CMM 2017). |
| **Party Policy in Modern Democracies** (`ppmd`) | The expert survey of party policy positions in 47 countries and the 2006 Routledge book with Michael Laver. Data: <https://www.tcd.ie/Political_Science/ppmd/>. Related: ES 2007 (expert surveys vs. hand coding), JJPS 2005, JOP 2009, EJPR 2006. |

**Other software** (a compact list at the bottom):
- tokenizers, with Lincoln Mullen et al. (JOSS 2018)
- Wordscores (Stata; no longer hosted)
- EzI, with Gary King: <https://gking.harvard.edu/ezi> (1998 APSA Best Research Software Award)

### 8.3 People

**Override of mysite.** The People page must exist, but don't build it purely from co-authors.

1. **PhD alumni:** from `content/associates/associates.md`, keeping its links and affiliations, which were checked in October 2026
2. **Post-doc alumni:** from the same file, with Jinshuai Ma added (he is no longer a current post-doc; owner decision, 15 October 2026)
3. **Co-authors:** generated automatically from publication `authors:` lists, as mysite describes. Show names only, with no guessed links.

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
| `/software/` | `/projects/` |
| `/posts/`, blog post URLs | Unchanged |

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
- **Analytics** (decided: none at launch). If wanted later, use a cookie-free option such as Plausible.
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
| 3 | Bio, Projects, Teaching, People, Blog migration, static files | Review Projects, People and Bio |
| 4 | Redirects, legacy URL check, search and AI checks, accessibility check | Read the URL check report |
| 5 | **Cut-over:** point kenbenoit.net at the new Netlify site, then re-run the URL check against production | Owner gives the go-ahead |

Rollback means pointing the domain back to the old Netlify site.

---

## 14. Owner decisions (settled 15 October 2026)

| # | Decision | Outcome |
|---|---|---|
| 1 | Research areas | Seven areas, in the order in §6.3 (campaign spending moved ahead of post-communist politics, 15 October 2026) |
| 2 | Spotlight | A Projects section (§6.2): LLM research featured, then quallmer, quanteda and Party Policy in Modern Democracies. A Projects page replaces Software (§8.2). |
| 3 | Featured publications | The six in §6.4 |
| 4 | Photo shape | Rounded square, about 200px |
| 5 | SMU institution colour | Not used (§5) |
| 6 | Analytics | None at launch (§11) |
| 7 | Repository | `kbenoit/kenbenoit-site`, public; Netlify project `kenbenoit-site` |
