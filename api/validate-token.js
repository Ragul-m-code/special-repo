// API Route: Validate Sanctum Token Key
const { verifySanctumToken } = require('./token-utils.js');

function parseBody(req) {
  return new Promise((resolve) => {
    if (req.body && typeof req.body === 'object') {
      return resolve(req.body);
    }
    if (typeof req.body === 'string') {
      try {
        return resolve(JSON.parse(req.body));
      } catch (e) {
        return resolve({});
      }
    }
    let data = '';
    req.on('data', chunk => { data += chunk; });
    req.on('end', () => {
      try {
        resolve(JSON.parse(data || '{}'));
      } catch (e) {
        resolve({});
      }
    });
  });
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  });
  res.end(JSON.stringify(payload));
}

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(200, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    return res.end();
  }

  const body = await parseBody(req);
  const token = (body.token || (req.query && req.query.token) || '').trim().toUpperCase();

  if (!token) {
    return sendJson(res, 400, {
      success: false,
      valid: false,
      error: "No token provided. Please enter your private access key."
    });
  }

  const isValid = verifySanctumToken(token);

  if (isValid) {
    return sendJson(res, 200, {
      success: true,
      valid: true,
      token: token,
      message: "Authorization verified. Clearance granted to Sovereign Sanctum."
    });
  } else {
    return sendJson(res, 401, {
      success: false,
      valid: false,
      error: "Access Denied: Invalid or unverified Sanctum key. Only genuine purchased keys grant clearance."
    });
  }
};
