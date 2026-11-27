// Tosla 3D doğrulamasından sonra tarayıcıyı buraya POST eder.
// Hash doğrulanır, sipariş durumu güncellenir, kullanıcı sonuç sayfasına yönlendirilir.
import { config as tosla, verifyCallbackHash } from './lib/tosla.mjs';
import { orders } from './lib/store.mjs';
import { apps } from './lib/apps.mjs';
import { sendMail } from './lib/mail.mjs';
import { T } from './lib/templates.mjs';

async function readBody(req) {
  const type = req.headers.get('content-type') || '';
  if (type.includes('application/json')) return req.json();
  const text = await req.text();
  return Object.fromEntries(new URLSearchParams(text));
}

export default async (req) => {
  const origin = process.env.URL || new URL(req.url).origin;
  const go = (lang, status, orderId, programId) => {
    const path = lang === 'en' ? '/en/payment/result/' : '/odeme/sonuc/';
    const q = new URLSearchParams({ status, ...(orderId ? { order: orderId } : {}), ...(programId ? { p: programId } : {}) });
    return Response.redirect(`${origin}${path}?${q}`, 303);
  };

  if (req.method !== 'POST') return go('tr', 'error');
  let d;
  try { d = await readBody(req); } catch { return go('tr', 'error'); }

  const orderId = String(d.OrderId || '').slice(0, 40);
  const store = orders();
  const order = orderId ? await store.get(orderId, { type: 'json' }) : null;
  const lang = order?.lang || 'tr';
  if (!order) { console.error('callback for unknown order', orderId); return go(lang, 'error'); }

  let c;
  try { c = tosla(); } catch { return go(lang, 'error', orderId); }

  const hashOk = verifyCallbackHash(c, d);
  const paid = hashOk && String(d.MdStatus) === '1' && String(d.BankResponseCode) === '00' && String(d.RequestStatus) === '1';

  // Bir kez "paid" olan sipariş tekrar eden/sahte bir callback ile geri alınmaz.
  if (order.status !== 'paid') {
    await store.setJSON(orderId, {
      ...order,
      status: paid ? 'paid' : hashOk ? 'failed' : 'hash_error',
      bankCode: d.BankResponseCode || null,
      bankMessage: String(d.BankResponseMessage || '').slice(0, 200) || null,
      mdStatus: d.MdStatus ?? null,
      updatedAt: new Date().toISOString(),
    });
  }
  if (paid && order.appId) {
    const a = await apps().get(order.appId, { type: 'json' });
    if (a && a.status !== 'paid') {
      const now = new Date().toISOString();
      await apps().setJSON(a.id, { ...a, status: 'paid', paidAt: now, paidBy: 'card', orderId, history: [...(a.history || []), { at: now, status: 'paid', by: 'card' }] });
      await sendMail(a.email, T.paid(a));
    }
  }
  if (paid && order.type === 'shop' && order.status !== 'paid') {
    const list = (order.items || []).map((i) => `${i.qty}× ${i.name}${i.size ? ' (' + i.size + ')' : ''}`).join('<br>');
    await sendMail(order.email, { subject: `NO Tiyatro · Ödemen alındı (${orderId})`, html: `<p>Merhaba ${order.name},</p><p>Ödemen başarıyla alındı. Siparişin hazırlanıyor.</p><p>${list}</p><p>Kargo: ${order.shipping ? order.shipping + ' TL' : '-'}<br><b>Toplam: ${order.amount} TL</b></p><p>NO Tiyatro & Vajra Theatre</p>` });
    await sendMail(process.env.ADMIN_EMAIL || 'hello@notiyatro.com', { subject: `Hediye siparişi: kartla ödendi ${orderId} · ${order.amount} TL`, html: `<p>${list}</p><p>${order.name} · ${order.email} · ${order.phone}<br>${order.delivery === 'pickup' ? 'Atölyede elden teslim' : 'Kargo (' + (order.delivery === 'ist' ? 'İstanbul içi' : 'şehir dışı') + ', ' + order.shipping + ' TL): ' + order.address + ', ' + order.city}</p>` });
  }
  if (!hashOk) console.error('callback hash mismatch', orderId);
  return go(lang, paid || order.status === 'paid' ? 'ok' : 'fail', orderId, order.programId);
};

export const config = { path: '/api/pay-callback' };
