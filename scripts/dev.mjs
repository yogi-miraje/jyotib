// Preview the same self-contained Worker used for production, without dependencies.
import http from 'node:http';
import worker from '../dist/server/index.js';
const port = Number(process.env.PORT || 4173);
http.createServer(async (req,res) => {
 try {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const response = await worker.fetch(new Request(url,{method:req.method,headers:req.headers}));
  res.writeHead(response.status,Object.fromEntries(response.headers));
  res.end(Buffer.from(await response.arrayBuffer()));
 } catch {
  res.writeHead(500,{'Content-Type':'text/plain'});res.end('Preview error');
 }
}).listen(port,'0.0.0.0',()=>console.log(`Worker preview on ${port}`));
