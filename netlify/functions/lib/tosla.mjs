// Tosla İşim (AKÖde) Sanal POS yardımcıları.
// Kimlik bilgileri yalnızca Netlify ortam değişkenlerinden okunur, koda yazılmaz:
//   TOSLA_CLIENT_ID, TOSLA_API_USER, TOSLA_API_PASS, TOSLA_ENV ("live" ya da "test")
import crypto from 'node:crypto';

const BASES = {
  live: 'https://entegrasyon.tosla.com/api/Payment',
  test: 'https://prepentegrasyon.tosla.com/api/Payment',
};

export const CURRENCY = { TRY: 949, EUR: 978, USD: 840, GBP: 826 };

export function config() {
  const env = process.env.TOSLA_ENV === 'live' ? 'live' : 'test';
  const c = {
    env,
    clientId: process.env.TOSLA_CLIENT_ID || '',
    apiUser: process.env.TOSLA_API_USER || '',
    secret: process.env.TOSLA_API_PASS || '',
    base: process.env.TOSLA_BASE_URL || BASES[env],
  };
  if (!c.clientId || !c.apiUser || !c.secret) throw new Error('TOSLA_NOT_CONFIGURED');
  return c;
}

export const sha512b64 = (s) => crypto.createHash('sha512').update(s, 'utf8').digest('base64');

// YYYYMMDDHHmmss, İstanbul saatiyle
export function timeSpan(d = new Date()) {
  const p = Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23',
    }).formatToParts(d).map((x) => [x.type, x.value]),
  );
  return `${p.year}${p.month}${p.day}${p.hour}${p.minute}${p.second}`;
}

export const randomToken = () => crypto.randomBytes(12).toString('hex').toUpperCase(); // 24 karakter

// İstek imzası: base64(sha512(apiPass + clientId + apiUser + rnd + timeSpan))
export const requestHash = (c, rnd, ts) => sha512b64(c.secret + c.clientId + c.apiUser + rnd + ts);

// Tosla'nın callback'te gönderdiği Hash'i doğrular.
// HashParameters (ör. "ClientId,ApiUser,OrderId,MdStatus,BankResponseCode,BankResponseMessage,RequestStatus")
// alanlarının değerleri sırayla birleştirilir, başına apiPass eklenir.
export function verifyCallbackHash(c, data) {
  if (!data || !data.Hash || !data.HashParameters) return false;
  const d = { ...data, ClientId: c.clientId, ApiUser: c.apiUser };
  const str = c.secret + data.HashParameters.split(',').map((k) => d[k.trim()] ?? '').join('');
  const a = Buffer.from(sha512b64(str));
  const b = Buffer.from(String(data.Hash));
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

export async function post(c, path, body, timeoutMs = 15000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(`${c.base}/${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
    const text = await r.text();
    try { return JSON.parse(text); } catch { return { Code: -1, Message: `HTTP ${r.status}: ${text.slice(0, 200)}` }; }
  } finally {
    clearTimeout(t);
  }
}

export function signed(c, extra = {}) {
  const rnd = randomToken();
  const ts = timeSpan();
  return { clientId: c.clientId, apiUser: c.apiUser, rnd, timeSpan: ts, hash: requestHash(c, rnd, ts), ...extra };
}
