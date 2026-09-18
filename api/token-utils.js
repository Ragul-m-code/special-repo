// Token Cryptographic Generation and Verification Utilities
const crypto = require('crypto');

function getSecret() {
  return process.env.PAYU_MERCHANT_SALT || process.env.VAULT_SECRET || 'SECRET_TO_DREAM_SANCTUM_2025';
}

/**
 * Generates an authentic cryptographically signed Sanctum Token:
 * Format: STD-VLT-<SEED>-<HMAC_SIG>
 */
function generateSanctumToken(seed = '') {
  const secret = getSecret();
  const rawSeed = seed || (Date.now().toString(36) + Math.random().toString(36).substring(2, 5));
  const payload = crypto.createHash('md5').update(rawSeed).digest('hex').substring(0, 4).toUpperCase();
  const sig = crypto.createHmac('sha256', secret).update(payload).digest('hex').substring(0, 6).toUpperCase();
  return `STD-VLT-${payload}-${sig}`;
}

/**
 * Validates whether a token is an authentic signed Sanctum token.
 * Prevents arbitrary text from bypassing the paywall.
 */
function verifySanctumToken(token) {
  if (!token || typeof token !== 'string') return false;
  token = token.trim().toUpperCase();

  // 1. Admin / Master Key support
  const masterKey = (process.env.MASTER_KEY || 'STD-MASTER-SANCTUM').toUpperCase();
  if (token === masterKey) return true;

  // 2. Strict format: STD-VLT-<PAYLOAD>-<SIG>
  const parts = token.split('-');
  if (parts.length === 4 && parts[0] === 'STD' && parts[1] === 'VLT') {
    const payload = parts[2];
    const sig = parts[3];
    if (payload.length >= 3 && sig.length === 6) {
      const secret = getSecret();
      const expectedSig = crypto.createHmac('sha256', secret).update(payload).digest('hex').substring(0, 6).toUpperCase();
      if (sig === expectedSig) return true;
    }
  }

  return false;
}

module.exports = {
  generateSanctumToken,
  verifySanctumToken
};
