import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';

const source = new URL('../docs/index.html', import.meta.url);
const server = createServer(async (request, response) => {
  const path = new URL(request.url, 'http://127.0.0.1').pathname;
  if (path !== '/' && path !== '/index.html') {
    response.writeHead(404).end('Not found');
    return;
  }
  try {
    const html = await readFile(source);
    response.writeHead(200, {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
    }).end(html);
  } catch (error) {
    console.error('Cannot read site source:', error);
    response.writeHead(500).end('Site source unavailable');
  }
});

server.on('error', error => {
  console.error('Cannot start site test server:', error);
  process.exitCode = 1;
});
server.listen(4173, '127.0.0.1');
