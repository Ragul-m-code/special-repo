// Vercel Serverless Function: PayU Response Callback & Verification
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

module.exports = async (req, res) => {
  loadEnv();

  // Parse Body (PayU posts form URL-encoded or JSON)
  let params = req.body || {};
  if (typeof params === 'string') {
    const querystring = require('querystring');
    params = querystring.parse(params);
  }

  const status = params.status;
  const txnid = params.txnid || '';
  const amount = params.amount || '';
  const productinfo = params.productinfo || process.env.PRODUCT_NAME || 'Secret to Dream';
  const firstname = params.firstname || '';
  const email = params.email || '';
  const receivedHash = (params.hash || '').toLowerCase();
  const additionalCharges = params.additionalCharges;

  const key = process.env.PAYU_MERCHANT_KEY;
  const salt = process.env.PAYU_MERCHANT_SALT;

  // PayU Reverse Verification Hash Sequence:
  // sha512(SALT|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key)
  const udf1 = params.udf1 || '';
  const udf2 = params.udf2 || '';
  const udf3 = params.udf3 || '';
  const udf4 = params.udf4 || '';
  const udf5 = params.udf5 || '';

  let hashSequence = `${salt}|${status}||||||${udf5}|${udf4}|${udf3}|${udf2}|${udf1}|${email}|${firstname}|${productinfo}|${amount}|${txnid}|${key}`;
  if (additionalCharges) {
    hashSequence = `${additionalCharges}|${hashSequence}`;
  }

  const calculatedHash = crypto.createHash('sha512').update(hashSequence).digest('hex').toLowerCase();

  // Verification Check
  const isHashValid = (calculatedHash === receivedHash);

  if (status === 'success' && isHashValid) {
    // Generate verified token
    const token = generateSanctumToken(txnid + salt);

    // Redirect directly to the member vault
    res.writeHead(302, {
      Location: `/vault?token=${encodeURIComponent(token)}&txnid=${encodeURIComponent(txnid)}&name=${encodeURIComponent(firstname)}&email=${encodeURIComponent(email)}`
    });
    return res.end();
  } else {
    // Redirect to index with error notification
    const errorReason = !isHashValid ? 'tampered_or_invalid_hash' : (params.error_Message || 'transaction_declined');
    res.writeHead(302, {
      Location: `/index.html?payment=failed&reason=${encodeURIComponent(errorReason)}`
    });
    return res.end();
  }
};
