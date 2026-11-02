"""Check static output, local links, metadata and optional HTTP/source parity."""
import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree

BASE = Path(__file__).resolve().parents[1]
PUBLIC = BASE / 'public'
ORIGIN = json.loads((BASE / 'content.json').read_text())['origin']


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.refs, self.ids = path, [], set()
        self.title, self.description, self.canonical = '', '', ''
        self.in_title, self.headings, self.mains = False, 0, 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'title':
            self.in_title = True
        if tag == 'h1':
            self.headings += 1
        if tag == 'main':
            self.mains += 1
        if tag == 'meta' and a.get('name') == 'description':
            self.description = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href', '')
        for key in ['href', 'src']:
            if a.get(key):
                self.refs.append(a[key])
        if a.get('srcset'):
            self.refs.extend(item.strip().split()[0] for item in a['srcset'].split(','))
        if tag == 'meta' and a.get('property') == 'og:image':
            self.refs.append(a.get('content', ''))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def route(path):
    name = path.relative_to(PUBLIC).as_posix()
    return '/' + (name[:-10] if name.endswith('index.html') else name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', action='store_true', help='also require all imported public files to be unchanged')
    parser.add_argument('--url', help='compare every public file with the running server at this base URL')
    args = parser.parse_args()
    errors = []
    pages = {p.resolve(): Page(p) for p in PUBLIC.rglob('index.html')}
    titles, descriptions = set(), set()
    for path, page in pages.items():
        label = route(path)
        if not page.title or page.title in titles:
            errors.append(label + ': missing or duplicate title')
        titles.add(page.title)
        if not page.description or page.description in descriptions:
            errors.append(label + ': missing or duplicate description')
        descriptions.add(page.description)
        if page.canonical != ORIGIN + label:
            errors.append(label + ': incorrect canonical')
        if page.headings != 1 or page.mains != 1 or 'main' not in page.ids:
            errors.append(label + ': expected one h1, one main and a skip-link target')
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme in ['mailto', 'tel', 'data']:
                continue
            if url.netloc and url.netloc not in ['www.jyotib.com', 'jyotib.com']:
                continue
            decoded = unquote(url.path)
            target = (PUBLIC / decoded.lstrip('/')) if decoded.startswith('/') else path.parent / decoded
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            if not target.is_relative_to(PUBLIC.resolve()) or not target.is_file():
                errors.append(label + ': missing local target ' + ref)
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(label + ': missing fragment ' + ref)
    sitemap = ElementTree.parse(PUBLIC / 'sitemap.xml')
    locations = {e.text for e in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    if locations != {p.canonical for p in pages.values()}:
        errors.append('Sitemap does not match the generated page URLs')
    if args.original:
        original = json.loads((BASE / 'docs/original-public-sha256.json').read_text())
        for name, expected in original['sha256'].items():
            path = PUBLIC / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append('Original file changed: ' + name)
        print('Checked original source parity: {} files.'.format(len(original['sha256'])))
    if args.url:
        files = sorted(p for p in PUBLIC.rglob('*') if p.is_file())

        def check_http(path):
            try:
                with urlopen(args.url.rstrip('/') + route(path), timeout=30) as response:
                    if response.status != 200 or response.read() != path.read_bytes():
                        return route(path) + ': served bytes differ'
            except Exception as error:
                return route(path) + ': ' + str(error)

        with ThreadPoolExecutor(max_workers=8) as pool:
            errors.extend(error for error in pool.map(check_http, files) if error)
        pdf = args.url.rstrip('/') + '/assets/jyoti-bhadrashetti-resume.pdf'
        with urlopen(Request(pdf, method='HEAD'), timeout=30) as response:
            if response.headers.get_content_type() != 'application/pdf' or response.read():
                errors.append('PDF HEAD/MIME check failed')
        try:
            with urlopen(args.url.rstrip('/') + '/missing-page-migration-check/', timeout=30):
                errors.append('Missing URL did not return 404')
        except HTTPError as error:
            if error.code != 404:
                errors.append('Unexpected missing-page status: ' + str(error.code))
        print('Checked HTTP parity: {} files, PDF HEAD/MIME and missing-page 404.'.format(len(files)))
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Site checks passed: {} pages, unique metadata, internal links/assets, skip targets and sitemap.'.format(len(pages)))


if __name__ == '__main__':
    main()
