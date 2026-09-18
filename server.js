// Local Development Server (Emulates Vercel Serverless Functions + Static Hosting)
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 8080;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.pdf': 'application/pdf',
  '.zip': 'application/zip',
  '.mp3': 'audio/mpeg',
  '.md': 'text/markdown; charset=utf-8',
  '.csv': 'text/csv; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8'
};

// Polyfill Vercel Response Helpers (res.status, res.json) on native Node res
function polyfillVercelResponse(res) {
  if (!res.status) {
    res.status = function(code) {
      res.statusCode = code;
      return res;
    };
  }
  if (!res.json) {
    res.json = function(data) {
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(data));
    };
  }
}

async function requestHandler(req, res) {
  polyfillVercelResponse(res);
  const parsedUrl = url.parse(req.url, true);
  let pathname = parsedUrl.pathname;

  // 1. API Route: /api/config
  if (pathname === '/api/config') {
    const configHandler = require('./api/config.js');
    req.query = parsedUrl.query;
    return configHandler(req, res);
  }

  // 2. API Route: /api/payu/initiate
  if (pathname === '/api/payu/initiate') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      req.body = body;
      req.query = parsedUrl.query;
      const initiateHandler = require('./api/payu/initiate.js');
      initiateHandler(req, res);
    });
    return;
  }

  // 3. API Route: /api/payu/callback
  if (pathname === '/api/payu/callback') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      req.body = body;
      req.query = parsedUrl.query;
      const callbackHandler = require('./api/payu/callback.js');
      callbackHandler(req, res);
    });
    return;
  }

  // 4. Static Files
  if (pathname === '/') pathname = '/index.html';
  const rawPath = pathname.replace(/^\/+/, '');
  const cleanPath = !path.extname(rawPath) ? rawPath + '.html' : rawPath;

  const candidatePaths = [
    path.join(__dirname, cleanPath),
    path.join(process.cwd(), cleanPath),
    path.resolve(__dirname, cleanPath),
    path.resolve(process.cwd(), cleanPath),
    path.join(__dirname, rawPath),
    path.join(process.cwd(), rawPath)
  ];

  let filePath = null;
  let stats = null;

  for (const p of candidatePaths) {
    try {
      const s = fs.statSync(p);
      if (s.isFile()) {
        filePath = p;
        stats = s;
        break;
      }
    } catch (e) {}
  }

  if (!filePath || !stats) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    return res.end('404 Not Found');
  }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    const filename = path.basename(filePath);

    const headers = {
      'Content-Type': contentType,
      'Access-Control-Allow-Origin': '*'
    };

    // If served from downloads or is a downloadable file, force attachment download
    if (pathname.startsWith('/downloads/') || ext === '.zip' || ext === '.pdf') {
      headers['Content-Disposition'] = `attachment; filename="${filename}"`;
      headers['Cache-Control'] = 'no-cache';
    }

    // Support HTTP Range requests for smooth audio scrubbing
    const range = req.headers.range;
    if (range && ext === '.mp3') {
      const parts = range.replace(/bytes=/, "").split("-");
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stats.size - 1;
      const chunksize = (end - start) + 1;
      headers['Content-Range'] = `bytes ${start}-${end}/${stats.size}`;
      headers['Accept-Ranges'] = 'bytes';
      headers['Content-Length'] = chunksize;
      res.writeHead(206, headers);
      const stream = fs.createReadStream(filePath, { start, end });
      stream.pipe(res);
      return;
    }

    headers['Content-Length'] = stats.size;
    res.writeHead(200, headers);

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
}

const server = http.createServer(requestHandler);

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Secret to Dream server running at http://localhost:${PORT}`);
  });
}

module.exports = requestHandler;
module.exports.server = server;
