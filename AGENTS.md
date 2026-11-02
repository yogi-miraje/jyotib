# Jyoti's website

- Keep responses succinct. This is a GitHub Pages website maintained in this repository.
- Preserve the existing appearance, text, routes, résumé and images unless a change is requested.
- Edit shared content in `content.json`, page templates in `build_site.py`, and styling in `public/styles.css`. Regenerate HTML with `make build`.
- Run `make check` before pushing. Preview with `make dev` at http://127.0.0.1:8000.
- Only `public/` is published by `.github/workflows/pages.yml`. Do not use Sites tools or Worker builds for routine development or publication.
- The imported Sites source is preserved in Git history at tag `sites-original-v4`. The existing `.openai/`, `worker/`, `dist/server/` and Worker scripts are retained as historical source; they are inactive on GitHub Pages.
- Keep the existing PDF/image files unless regeneration is requested. Optional authoring tools use `make setup`; original private uploads are not stored in this repository.
- Retain factual/permission review notes in `REVIEW.md`; migration does not authorize new claims or photographs.
- Use Obsidian CLI and vault `Life` when asked to refer to or save notes.
