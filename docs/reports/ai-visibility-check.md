# Search and AI-visibility check

Target: local build (`hugo --gc --minify`)

- PASS robots.txt exists
- PASS robots.txt has User-agent: *
- PASS robots.txt has no blocks aimed at AI crawlers
- PASS robots.txt lists an https Sitemap
- PASS robots.txt points to /llms.txt
- PASS sitemap.xml exists
- PASS sitemap has 207 URLs
- PASS every sitemap <loc> starts with https://
- PASS no sitemap URL is disallowed by robots.txt
- PASS every sitemap URL exists in the build (0 missing)
- PASS llms.txt exists with a title
- PASS llms.txt links /bio/
- PASS llms.txt links /publication/
- PASS llms.txt links /projects/
- PASS llms.txt links /teaching/
- PASS llms.txt links /pdfs/KenBenoitCV.pdf
- PASS 101 publication page(s) have valid Scholar tags and JSON-LD

**PASS**
