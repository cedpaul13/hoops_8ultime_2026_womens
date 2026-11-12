import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';

const files = {
  '/': ['../docs/index.html', 'text/html; charset=utf-8'],
  '/index.html': ['../docs/index.html', 'text/html; charset=utf-8'],
  '/usports-logo.svg': ['../docs/usports-logo.svg', 'image/svg+xml'],
};
const server = createServer(async (request, response) => {
  const path = new URL(request.url, 'http://127.0.0.1').pathname;
  const file = files[path];
  if (!file) {
    response.writeHead(404).end('Not found');
    return;
  }
  try {
    const content = await readFile(new URL(file[0], import.meta.url));
    response.writeHead(200, {
      'Content-Type': file[1],
      'Cache-Control': 'no-store',
    }).end(content);
  } catch (error) {
    console.error(`Cannot read site file ${path}:`, error);
    response.writeHead(500).end('Site source unavailable');
  }
});

server.on('error', error => {
  console.error('Cannot start site test server:', error);
  process.exitCode = 1;
});
server.listen(4173, '127.0.0.1');
