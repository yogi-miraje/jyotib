// The build embeds the static documents and images to keep this Worker self-contained.
const assets = /* ASSETS_MAP */{};
const legacyHost = 'jyoti-bhadrashetti.yogimiraje.chatgpt.site';
const canonicalHost = 'www.jyotib.com';

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.hostname === legacyHost || url.hostname === 'jyotib.com' || (url.hostname === canonicalHost && url.protocol !== 'https:')) {
      url.hostname = canonicalHost;
      url.protocol = 'https:';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', {status: 405, headers: {'Allow': 'GET, HEAD'}});
    }
    let pathname;
    try { pathname = decodeURIComponent(url.pathname); }
    catch { return new Response('Invalid URL', {status: 400}); }
    let key = pathname;
    if (key.endsWith('/')) key += 'index.html';
    let asset = assets[key];
    if (!asset && assets[key + '/index.html']) {
      url.pathname += '/';
      return Response.redirect(url.toString(), 301);
    }
    if (!asset) return new Response('Page not found', {status: 404, headers: {'Content-Type': 'text/plain; charset=utf-8'}});
    const headers = {
      'Content-Type': asset.type,
      'Cache-Control': key.endsWith('.html') ? 'public, max-age=0, must-revalidate' : 'public, max-age=3600',
      'ETag': asset.etag,
      'X-Content-Type-Options': 'nosniff',
    };
    if (request.headers.get('If-None-Match') === asset.etag) return new Response(null, {status:304, headers});
    if (request.method === 'HEAD') return new Response(null, {status:200, headers});
    const binary = atob(asset.data);
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    return new Response(bytes, {status:200, headers});
  }
};
