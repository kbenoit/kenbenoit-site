# Accessibility check

Tool: axe-core (WCAG 2.0 and 2.1, levels A and AA, plus best practices), run in the browser against a local build.

Pages: home, publications list, a publication page, Projects, a project page, Bio, Teaching, People, Blog list, a blog post,
a category page, the categories list, the tags list and the 404 page. Each was tested at 1280px and 375px wide.
The search dialog and the open mobile menu were tested separately.

**Result: no violations on all 28 page and width combinations, plus the open search dialog and the open mobile menu.**

## Problems found and fixed

| Problem | Where | Fix |
|---|---|---|
| Links in running text told apart from the text only by colour (about 2.5:1) | Citation lines, project descriptions | Underline added |
| Heading levels skipped (h1 then h3) | Projects page cards | Card titles are h2 on that page |
| Visible text "Esc" not in the accessible name | Search dialog close button | Label now begins with "Esc" |
| Menu toggle skipped by the keyboard on narrow screens | Navbar | The toggle is a real focusable control with a label and a visible focus ring; hidden at desktop width |
| `aria-label` not allowed on the burger `label` element | Navbar | Removed (the checkbox carries the name) |
| Taxonomy pages unreadable (blue text on blue buttons) | /tags/, /categories/, /publication_types/ | Replaced with plain list pages |

## Also in place

- Skip-to-content link on every page, a visible focus ring, `prefers-reduced-motion` respected, light mode only.
- Contrast: body text 18.7:1, muted text 5.2 to 5.7:1, accent text 6.7 to 7.3:1 on white and the grey surface. The text hover colour is 5.4:1.
- All images have `alt` text, or `alt=""` where they are decorative next to a text label.

## Not covered

axe checks about a third of WCAG automatically. Not tested: screen-reader reading order on the publications filters, and keyboard use of the expandable abstracts beyond what axe reports.
