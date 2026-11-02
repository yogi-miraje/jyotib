# Jyoti Bhadrashetti

Jyoti's existing website, maintained locally and on GitHub Pages. The original HTML, CSS, images, résumé, content and project URLs are preserved. No Sites account, Node packages, database or Worker is needed to build or serve it.

## Build and preview

Requires Python 3.9+ and `make` (already available on this Mac).

```sh
make dev
```

Open http://127.0.0.1:8000. Stop with Ctrl+C. Use `make dev PORT=8001` for another port. The server binds to this computer only.

```sh
make build           # regenerate the 12 HTML pages, sitemap and robots.txt
make check           # build; check metadata, internal links, images and sitemap
make check-original  # verify every original public file is unchanged
python3 scripts/check-site.py --url http://127.0.0.1:8000
```

## Edit and publish

| File | Purpose |
| --- | --- |
| `content.json` | Shared content, projects and résumé data |
| `build_site.py` | Page templates and generated metadata |
| `public/styles.css` | Existing responsive layout and typography |
| `public/assets/` | Portrait, project images, social previews and original PDF |
| `asset-records.json`, `REVIEW.md` | Image provenance and factual/permission review notes |
| `.github/workflows/pages.yml` | Build/check on pull requests; deploy `public/` on pushes to `main` |

After edits, run `make check`, review the local website, commit both source and generated output, and push to `main`. GitHub Actions builds and publishes automatically. The workflow rejects uncommitted generated-page differences. PDF/image regeneration is deliberately separate so ordinary deployments preserve the exact existing binary assets.

GitHub Pages uses custom domain `www.jyotib.com`. Its domain setting lives in **Settings → Pages**; `public/CNAME` records the intended domain. Paths are rooted at `/`, matching the custom domain. The repository's `/jyotib/` project URL is not a separate preview environment.

## Optional PDF and image authoring

```sh
make setup
make resume
make assets PORTFOLIO=/absolute/path/to/original-portfolio.pdf
```

`make setup` installs pinned ReportLab, Pillow and PyMuPDF into `.venv`. Bundled DejaVu fonts remove the original Linux font-path dependency. These commands replace the corresponding assets; run them only when intentionally updating those assets. The original private source uploads were not present in Sites' source repository and are not required for everyday maintenance.

## Migration and original source

The complete Sites source history is retained, with imported version 6 at tag `sites-original-v6` (`dd27f93e100b7377c2825927511e7465ee2c1be1`). The original deployment files (`.openai/`, `worker/`, `dist/server/` and Worker scripts) remain as historical source; GitHub Pages does not execute or publish them. The original README is in `docs/original-sites-readme.md`.

See `docs/MIGRATION.md` for parity checks, hosting differences and DNS configuration. Historical draft/publication notes in `REVIEW.md` remain available for future content changes; this migration copies the version already live on November 2, 2026.
