// Ödeme başlatma: fiyatı sunucudaki katalogdan alır, Tosla'da 3D oturumu açar,
// tarayıcıya ThreeDSessionId döner. Kart bilgisi bu fonksiyona hiç gelmez;
// tarayıcı kart formunu doğrudan Tosla'ya gönderir.
import { config as tosla, post, signed, CURRENCY, timeSpan } from './lib/tosla.mjs';
import { findProgram } from './lib/catalog.mjs';
import { orders } from './lib/store.mjs';
import { byToken } from './lib/apps.mjs';

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
const clean = (v, max) => String(v ?? '').replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, max);

export default async (req) => {
  if (req.method !== 'POST') return json(405, { error: 'method' });
  let b;
  try { b = await req.json(); } catch { return json(400, { error: 'bad_json' }); }

  // Onaylı başvurudan gelen ödeme: kişi bilgileri başvurudan alınır
  const app = b.b ? await byToken(String(b.b)) : null;
  if (b.b && (!app || app.status !== 'approved')) return json(403, { error: 'application' });
  const program = findProgram(app ? app.programId : clean(b.program, 60));
  const name = app ? app.name : clean(b.name, 100);
  const email = app ? app.email : clean(b.email, 120).toLowerCase();
  const phone = app ? app.phone : clean(b.phone, 25);
  const lang = b.lang === 'en' ? 'en' : 'tr';
  const installment = Math.max(1, Math.min(Number.parseInt(b.installment, 10) || 1, program?.maxInstallment || 1));

  if (!program) return json(400, { error: 'program' });
  if (name.length < 3) return json(400, { error: 'name' });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json(400, { error: 'email' });
  if (phone.replace(/\D/g, '').length < 7) return json(400, { error: 'phone' });
  if (b.consent !== true) return json(400, { error: 'consent' });

  let c;
  try { c = tosla(); } catch { return json(503, { error: 'not_configured' }); }

  const orderId = `NO${timeSpan().slice(2)}${Math.random().toString(36).slice(2, 6).toUpperCase()}`;
  const origin = process.env.URL || new URL(req.url).origin;
  const res = await post(c, 'threeDPayment', signed(c, {
    callbackUrl: `${origin}/api/pay-callback`,
    orderId,
    amount: Math.round(program.price * 100),
    currency: CURRENCY[program.currency] || CURRENCY.TRY,
    installmentCount: installment > 1 ? installment : 0,
  })).catch((e) => ({ Code: -1, Message: String(e) }));

  if (res.Code !== 0 || !res.ThreeDSessionId) {
    console.error('threeDPayment failed', orderId, res.Code, res.Message);
    return json(502, { error: 'gateway', message: res.Message || '' });
  }

  await orders().setJSON(orderId, {
    orderId, programId: program.id, program: program.title.tr, amount: program.price, currency: program.currency,
    installment, name, email, phone, lang, appId: app ? app.id : null, marketing: b.marketing === true, status: 'pending', env: c.env, createdAt: new Date().toISOString(),
  });

  return json(200, { orderId, sessionId: res.ThreeDSessionId, gateway: `${c.base}/ProcessCardForm` });
};

export const config = { path: '/api/pay-start' };
