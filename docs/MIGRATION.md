# Migration to local development and GitHub Pages

## Imported source

The initial export was Sites version 4. The live site changed during the migration; versions 5 and 6 were then imported before publishing to GitHub. The final baseline is version 6, commit `dd27f93e100b7377c2825927511e7465ee2c1be1`, retained at `sites-original-v6`. Version 4 remains at `sites-original-v4`.

All 88 original public files, source assets, content and Git history are copied. Original public files are byte-for-byte unchanged; `docs/original-public-sha256.json` records their hashes. GitHub's `CNAME` and `.nojekyll` are the only added public files. The original source README is retained in `docs/original-sites-readme.md`.

The site now builds with Python's standard library. `make dev`, `make build`, `make check` and equivalent npm commands use the static files. Optional PDF/image dependencies are pinned in `requirements.txt` and installed in `.venv`; DejaVu fonts are bundled with their license for portability. Existing PDF and images were not regenerated.

## Verification before first push

- Browser comparison of all 12 routes at desktop (1280 × 720) and mobile (390 × 844): rendered text, every link and download attribute, images/srcsets/alt text, head metadata, and layout geometry all match the live site.
- Home, Projects, all eight project detail pages, Résumé and Contact are covered, including the two older project URLs absent from the Projects index.
- Local navigation, project Previous/Next links and the résumé download work. The downloaded PDF matches the original file hash.
- All 90 local public files return their exact file bytes over HTTP. PDF MIME/HEAD, missing-page 404, unique metadata, internal assets/links, skip targets and sitemap pass.
- `make build` regenerates the same original pages without changing their hashes.

Detailed local Browser evidence is retained in ignored `.artifacts/browser/`; the compact result is in `docs/migration-checks.json`. Direct automated requests to the former Sites host return 403, so the live rendered comparison uses Browser rather than treating those responses as page content.

## Hosting

GitHub Actions builds and checks the site, then uploads only `public/` with the official GitHub Pages actions. Pull requests validate without deploying; pushes to `main` deploy. Sites/Worker files are retained as original source and are not part of the active build or published artifact.

The custom domain is `www.jyotib.com`, matching the original canonical URLs. Configure GitHub Pages with GitHub Actions as its source. Configure the domain in GitHub before pointing DNS to it, following [GitHub's custom-domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

| DNS type | Host | Target |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | yogi-miraje.github.io |

Preserve mail and unrelated verification records. Enable Enforce HTTPS after GitHub issues the certificate. GitHub provides apex-to-www and directory-path redirects. Its cache headers, ETags and default 404 page differ from the old Worker; HTML, CSS, images, PDF and visitor features are preserved. The old ChatGPT hostname continues to redirect through its existing Sites publication.

## Rollback

Before migration, apex DNS returned `172.66.3.26` and `162.159.143.30`; `www` pointed to `custom-domains.chatgpt.site`. The former publication is retained during cutover. Reverting DNS restores it while propagation completes. To revert a future content change on GitHub, revert the corresponding commit and push to `main`.

## Cutover status

Local parity passed. [GitHub Pages build and deployment succeeded](https://github.com/yogi-miraje/jyotib/actions/runs/41539525048) on November 2, 2026. GitHub Actions is the configured publishing source and `www.jyotib.com` is the configured custom domain.

Namecheap's session expired before DNS could be edited. Domain cutover and GitHub's HTTPS certificate/enforcement remain pending sign-in. The existing live domain continues serving the original Sites publication in the meantime.
