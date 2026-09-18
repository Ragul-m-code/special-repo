// Vercel Serverless Function: PayU Payment Initiation & Demo Flow Handler
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { generateSanctumToken } = require('../token-utils.js');

function loadEnv() {
  try {
    const envPath = path.resolve(process.cwd(), '.env');
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, 'utf-8');
      content.split('\n').forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const idx = trimmed.indexOf('=');
          if (idx !== -1) {
            const key = trimmed.substring(0, idx).trim();
            const val = trimmed.substring(idx + 1).trim().replace(/^["']|["']$/g, '');
            if (!process.env[key]) {
              process.env[key] = val;
            }
          }
        }
      });
    }
  } catch (e) {}
}

loadEnv();

function sendJson(res, statusCode, data) {
  res.setHeader('Content-Type', 'application/json');
  if (res.status && res.json) {
    return res.status(statusCode).json(data);
  }
  res.statusCode = statusCode;
  return res.end(JSON.stringify(data));
}

module.exports = async (req, res) => {
  loadEnv();

  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    return res.end();
  }

  // Parse Body
  let body = req.body || {};
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) { body = {}; }
  }

  const name = (body.name || (req.query && req.query.name) || 'Private Collector').trim();
  const email = (body.email || (req.query && req.query.email) || 'collector@confidential.net').trim();
  const phone = (body.phone || (req.query && req.query.phone) || '9999999999').trim();

  const productName = process.env.PRODUCT_NAME || 'Secret to Dream';
  const amount = parseFloat(process.env.PRODUCT_AMOUNT || '29.00').toFixed(2);
  const demoMode = (process.env.DEMO_MODE || 'on').toLowerCase() === 'on';

  // Determine Base URL
  const host = (req.headers && (req.headers['x-forwarded-host'] || req.headers.host)) || 'localhost:8080';
  const proto = (req.headers && req.headers['x-forwarded-proto']) || (host.includes('localhost') ? 'http' : 'https');
  const baseUrl = process.env.BASE_URL || `${proto}://${host}`;

  // DEMO MODE = ON: Bypass PayU and issue instant access
  if (demoMode) {
    const txnid = `DEMO_${Date.now()}`;
    const token = generateSanctumToken(txnid + email);

    return sendJson(res, 200, {
      success: true,
      demo: true,
      token: token,
      txnid: txnid,
      name: name,
      email: email,
      productName: productName,
      amount: amount,
      currency: process.env.PRODUCT_CURRENCY || 'INR',
      currencySymbol: '₹',
      redirectUrl: `/vault?token=${encodeURIComponent(token)}&txnid=${encodeURIComponent(txnid)}&name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&demo=1`
    });
  }

  // DEMO MODE = OFF: Real PayU Gateway Integration
  const key = process.env.PAYU_MERCHANT_KEY;
  const salt = process.env.PAYU_MERCHANT_SALT;
  const payuEnv = process.env.PAYU_ENV || 'test';

  if (!key || !salt || key === 'your_payu_merchant_key_here') {
    return sendJson(res, 400, {
      success: false,
      error: "PayU credentials are not configured in .env. Please set PAYU_MERCHANT_KEY and PAYU_MERCHANT_SALT or enable DEMO_MODE=on."
    });
  }

  // Generate unique transaction ID
  const txnid = `STD_${Date.now()}_${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

  // Callbacks
  const surl = `${baseUrl}/api/payu/callback`;
  const furl = `${baseUrl}/api/payu/callback`;

  // PayU SHA-512 Hash Generation:
  // sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)
  const firstname = name.split(' ')[0] || 'Member';
  const udf1 = '';
  const udf2 = '';
  const udf3 = '';
  const udf4 = '';
  const udf5 = '';

  const hashString = `${key}|${txnid}|${amount}|${productName}|${firstname}|${email}|${udf1}|${udf2}|${udf3}|${udf4}|${udf5}||||||${salt}`;
  const hash = crypto.createHash('sha512').update(hashString).digest('hex');

  const actionUrl = payuEnv === 'production' 
    ? 'https://secure.payu.in/_payment' 
    : 'https://test.payu.in/_payment';

  return sendJson(res, 200, {
    success: true,
    demo: false,
    actionUrl: actionUrl,
    params: {
      key: key,
      txnid: txnid,
      amount: amount,
      productinfo: productName,
      firstname: firstname,
      email: email,
      phone: phone,
      surl: surl,
      furl: furl,
      hash: hash,
      service_provider: 'payu_paisa'
    }
  });
};
