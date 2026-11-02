# Jyoti Bhadrashetti

A four-page professional website with individual project documents and a downloadable résumé.

## Editing and building

- `content.json`: shared website and PDF content; pending confirmations are in `REVIEW.md`.
- `build_site.py`: generates Home, Projects, Résumé, Contact and existing project URLs, unique metadata, sitemap and robots.txt.
- `public/styles.css`: responsive typography, colors and layout.
- `scripts/build-resume.py`: regenerates the two-page PDF at the existing URL with embedded fonts and no phone number. Uses ReportLab.
- `scripts/build-assets.py <portfolio.pdf>`: extracts recorded images from the supplied portfolio, creates responsive WebP variants, social previews and favicons. Uses PyMuPDF and Pillow. No artificial upscaling.
- `asset-records.json`: source URL, PDF page, embedded image reference, credit, caption and permission status for each portfolio image.
- `worker/index.mjs`: host redirects, document/asset serving, HEAD and cache handling.
- `scripts/build-worker.py`: embeds generated pages and assets in a self-contained Worker under `dist/server/index.js`.
- `scripts/check-worker.mjs`: verifies redirect status/location, canonical-host routes, PDF MIME/HEAD and missing-page handling.

Generate content with `python3 build_site.py`, regenerate the PDF with `python3 scripts/build-resume.py`, then run `python3 scripts/build-worker.py` and `node scripts/check-worker.mjs`. The source hosting manifest preserves the existing project ID and uses the Worker build. All main navigation uses separate URLs and works without JavaScript.

## Sources and publication

The supplied 2026 résumé and earlier Drive portfolio are source documents. The original uploads are not modified. Confirmed public project references and unresolved facts are recorded in `REVIEW.md`. Existing private phone numbers are not retained in the rebuilt PDF or public output.

**Save this revision without deployment until Jyoti’s factual review and SRM’s photo/financial permissions are complete.** The previous live version remains published in the meantime. No permission is inferred from an image being visible on a public website.
