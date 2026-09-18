// Vercel Serverless Function: Runtime Configuration Endpoint
const fs = require('fs');
const path = require('path');

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

module.exports = (req, res) => {
  loadEnv();

  // Allow CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') {
    if (res.status) return res.status(200).end();
    res.statusCode = 200;
    return res.end();
  }

  const demoMode = (process.env.DEMO_MODE || 'on').toLowerCase() === 'on';

  const data = {
    success: true,
    demo: demoMode,
    productName: process.env.PRODUCT_NAME || 'Secret to Dream',
    amount: parseFloat(process.env.PRODUCT_AMOUNT || '29.00').toFixed(2),
    currency: process.env.PRODUCT_CURRENCY || 'INR',
    currencySymbol: '₹',
    payuEnv: process.env.PAYU_ENV || 'test',
    notionUrl: process.env.NOTION_VAULT_URL || 'https://notion.so'
  };

  if (res.json) {
    if (res.status) res.status(200);
    return res.json(data);
  }

  res.statusCode = 200;
  return res.end(JSON.stringify(data));
};
