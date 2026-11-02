"""Embed the reviewed static output, preserving the existing Site identity."""
from pathlib import Path
import base64,hashlib,json,mimetypes
BASE=Path(__file__).resolve().parents[1];DIST=BASE/'dist';PUBLIC=BASE/'public';assets={}
for path in sorted(PUBLIC.rglob('*')):
 if not path.is_file() or any(part in ['server','.openai'] for part in path.relative_to(PUBLIC).parts):continue
 if path.name.startswith('qa-'):raise RuntimeError('Remove QA-only pages before packaging')
 raw=path.read_bytes();mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
 if mime.startswith('text/') or mime=='image/svg+xml':mime+='; charset=utf-8'
 assets['/'+path.relative_to(PUBLIC).as_posix()]={'type':mime,'data':base64.b64encode(raw).decode(),'etag':'"'+hashlib.sha256(raw).hexdigest()[:24]+'"'}
source=(BASE/'worker/index.mjs').read_text().replace('/* ASSETS_MAP */{}',json.dumps(assets,separators=(',',':')))
assert len(source.encode())<10_000_000,'Reduce assets to keep the Worker compact'
(DIST/'server').mkdir(exist_ok=True);(DIST/'server/index.js').write_text(source)
manifest=json.loads((BASE/'.openai/hosting.json').read_text());manifest.pop('static',None)
(DIST/'.openai').mkdir(exist_ok=True);(DIST/'.openai/hosting.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built self-contained Worker:',len(assets),'assets,',round(len(source.encode())/1e6,2),'MB. Canonical-host redirects use HTTP 301.')
