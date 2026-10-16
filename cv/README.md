# The C.V.

`Kenneth_Benoit_CV.docx` is the master copy of the C.V. The PDF on the website,
`static/pdfs/KenBenoitCV.pdf` (served at <https://kenbenoit.net/pdfs/KenBenoitCV.pdf>), is made from it.
This folder sits outside `static/`, so Netlify does not publish the Word file.

To update the C.V.:

1. Edit `cv/Kenneth_Benoit_CV.docx` in Word and change the "Updated" date at the end.
2. Export to PDF (File > Save As > PDF) and replace `static/pdfs/KenBenoitCV.pdf`.
3. Commit the Word file and the PDF together, so the two never drift apart.

Facts that also appear on the website (grants, awards, service, positions) live in
`content/projects/_index.md`, `content/service/index.md`, `content/bio/index.md` and
`data/leadership.yaml`. Change them in both places when they change.
