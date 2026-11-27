// Hediye siparişi: fiyatlar sunucudaki katalogdan hesaplanır.
// Tosla yapılandırılmışsa 3D oturumu açılır (kart formu doğrudan Tosla'ya gider);
// değilse sipariş "ödeme bekliyor" olarak kaydedilir ve ekibe e-posta gider.
import { config as tosla, post, signed, CURRENCY, timeSpan } from './lib/tosla.mjs';
import { orders } from './lib/store.mjs';
import { sendMail } from './lib/mail.mjs';
import { customerMail } from './lib/shopmail.mjs';
import data from '../../data/products.json' with { type: 'json' };

const json = (s, b) => new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
const clean = (v, max) => String(v ?? '').replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, max);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tl = (n) => `${n.toLocaleString('tr-TR')} TL`;

export default async (req) => {
  if (req.method !== 'POST') return json(405, { error: 'method' });
  let b; try { b = await req.json(); } catch { return json(400, { error: 'bad_json' }); }
  const cat = Object.fromEntries(data.products.filter((p) => p.active).map((p) => [p.id, p]));
  const items = [];
  for (const it of Array.isArray(b.items) ? b.items.slice(0, 20) : []) {
    const p = cat[clean(it.id, 40)]; const qty = Math.max(1, Math.min(10, parseInt(it.qty, 10) || 1));
    if (!p) return json(400, { error: 'item' });
    const size = p.sizes.length ? clean(it.size, 5) : '';
    if (p.sizes.length && !p.sizes.includes(size)) return json(400, { error: 'size' });
    items.push({ id: p.id, name: p.name, size, qty, price: p.price, line: p.price * qty });
  }
  if (!items.length) return json(400, { error: 'empty' });
  const name = clean(b.name, 100), email = clean(b.email, 120).toLowerCase(), phone = clean(b.phone, 25);
  const delivery = ['ist', 'out', 'pickup'].includes(b.delivery) ? b.delivery : 'out';
  const shipFee = delivery === 'pickup' ? 0 : (data.shipping?.[delivery] ?? 0);
  const address = clean(b.address, 300), city = clean(b.city, 80);
  const lang = /^(tr|en|de|ru|fr|es|it|el)$/.test(b.lang) ? b.lang : 'tr';
  if (name.length < 3 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || phone.replace(/\D/g, '').length < 7) return json(400, { error: 'fields' });
  if (delivery !== 'pickup' && (address.length < 8 || city.length < 2)) return json(400, { error: 'fields' });
  if (b.consent !== true) return json(400, { error: 'consent' });
  const subtotal = items.reduce((s, i) => s + i.line, 0), total = subtotal + shipFee;
  const orderId = `SH${timeSpan().slice(2)}${Math.random().toString(36).slice(2, 6).toUpperCase()}`;
  const summary = items.map((i) => `${i.qty}× ${i.name}${i.size ? ' (' + i.size + ')' : ''}`).join(', ');
  const base = { orderId, type: 'shop', program: `Hediyeler: ${summary} · ${delivery === 'pickup' ? 'Elden teslim' : (delivery === 'ist' ? 'Kargo İstanbul içi: ' : 'Kargo şehir dışı: ') + address + ', ' + city}`, items, subtotal, shipping: shipFee, amount: total, currency: 'TRY', installment: 1, name, email, phone, delivery, address, city, lang, createdAt: new Date().toISOString() };

  let c = null; try { c = tosla(); } catch { c = null; }
  if (c && b.card !== true) return json(409, { error: 'card_required' });
  if (c && b.card === true) {
    const origin = process.env.URL || new URL(req.url).origin;
    const res = await post(c, 'threeDPayment', signed(c, { callbackUrl: `${origin}/api/pay-callback`, orderId, amount: Math.round(total * 100), currency: CURRENCY.TRY, installmentCount: 0 })).catch((e) => ({ Code: -1, Message: String(e) }));
    if (res.Code !== 0 || !res.ThreeDSessionId) { console.error('shop threeDPayment failed', orderId, res.Code, res.Message); return json(502, { error: 'gateway' }); }
    await orders().setJSON(orderId, { ...base, status: 'pending', env: c.env });
    return json(200, { orderId, sessionId: res.ThreeDSessionId, gateway: `${c.base}/ProcessCardForm` });
  }
  await orders().setJSON(orderId, { ...base, status: 'awaiting_payment' });
  const rows = items.map((i) => `<tr><td>${i.qty}× ${esc(i.name)}${i.size ? ' (' + esc(i.size) + ')' : ''}</td><td align="right">${tl(i.line)}</td></tr>`).join('');
  const html = `<p><b>Yeni dükkân siparişi ${orderId}</b></p><table cellpadding="4">${rows}<tr><td>Kargo</td><td align="right">${shipFee ? tl(shipFee) : '-'}</td></tr><tr><td><b>Toplam</b></td><td align="right"><b>${tl(total)}</b></td></tr></table><p>${esc(name)} · ${esc(email)} · ${esc(phone)}<br>${delivery === 'pickup' ? 'Atölyede elden teslim' : (delivery === 'ist' ? 'Kargo (İstanbul içi): ' : 'Kargo (şehir dışı): ') + esc(address) + ', ' + esc(city)}</p><p>Kartla ödeme henüz açık değil; müşteriyle iletişime geçin.</p>`;
  await sendMail(process.env.ADMIN_EMAIL || 'hello@notiyatro.com', { subject: `Hediye siparişi ${orderId} · ${tl(total)}`, html }).catch(() => {});
  await sendMail(email, customerMail('received', { ...base, status: 'awaiting_payment' })).catch(() => {});
  return json(200, { orderId, mode: 'manual' });
};
export const config = { path: '/api/shop-order' };
