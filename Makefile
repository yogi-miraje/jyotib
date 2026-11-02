PYTHON ?= python3
PORT ?= 8000

.PHONY: build dev check check-original setup resume assets

build:
	$(PYTHON) build_site.py

dev: build
	$(PYTHON) -m http.server $(PORT) --bind 127.0.0.1 --directory public

check: build
	$(PYTHON) scripts/check-site.py

check-original:
	$(PYTHON) scripts/check-site.py --original

# Optional tools for regenerating the PDF and portfolio images.
setup:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

resume:
	.venv/bin/python scripts/build-resume.py

assets:
	@test -n "$(PORTFOLIO)" || (echo 'Use: make assets PORTFOLIO=/absolute/path/portfolio.pdf'; exit 1)
	.venv/bin/python scripts/build-assets.py "$(PORTFOLIO)"
