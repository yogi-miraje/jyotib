import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../dist/server/index.js',import.meta.url),'utf8');
const {default:worker}=await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
for (const host of ['jyoti-bhadrashetti.yogimiraje.chatgpt.site','jyotib.com']) {
 const r=await worker.fetch(new Request(`https://${host}/portfolio/gridline/?ref=test`));
 assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://www.jyotib.com/portfolio/gridline/?ref=test');
}
for (const path of ['/','/portfolio/','/portfolio/gridline/','/portfolio/altaire-jackson/','/resume/','/contact/','/robots.txt','/sitemap.xml','/favicon.ico','/assets/jyoti-bhadrashetti-resume.pdf']) {
 const r=await worker.fetch(new Request('https://www.jyotib.com'+path));assert.equal(r.status,200,path);
 assert.ok((await r.arrayBuffer()).byteLength>0,path);
}
let r=await worker.fetch(new Request('https://www.jyotib.com/unknown/'));assert.equal(r.status,404);
r=await worker.fetch(new Request('https://www.jyotib.com/resume'));assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://www.jyotib.com/resume/');
r=await worker.fetch(new Request('https://www.jyotib.com/assets/jyoti-bhadrashetti-resume.pdf',{method:'HEAD'}));assert.equal(r.status,200);assert.equal(r.headers.get('content-type'),'application/pdf');assert.equal((await r.arrayBuffer()).byteLength,0);
console.log('Worker checks passed: host/path redirects, pages/assets, PDF MIME/HEAD, and 404.');
