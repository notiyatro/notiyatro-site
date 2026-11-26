// Onaylanan başvurunun ödeme sayfası için bilgi + "ödemeyi yaptım" bildirimi
import { byToken, apps, program, json, siteUrl } from './lib/apps.mjs';
import { sendMail } from './lib/mail.mjs';
import { T } from './lib/templates.mjs';

export default async (req) => {
  const url = new URL(req.url);
  if (req.method === 'GET') {
    const a = await byToken(url.searchParams.get('b'));
    if (!a || !['approved', 'payment_reported', 'paid'].includes(a.status)) return json(404, { error: 'not_found' });
    const p = program(a.programId) || {};
    const tosla = !!(process.env.TOSLA_CLIENT_ID && process.env.TOSLA_API_USER && process.env.TOSLA_API_PASS);
    return json(200, {
      id: a.id, name: a.name, status: a.status, programId: a.programId,
      title: p.title || { tr: a.program, en: a.program }, date: p.date || null, priceText: p.priceText || null,
      price: typeof p.price === 'number' ? p.price : null, net: p.net ?? null, vat: p.vat ?? null, currency: p.currency || 'TRY',
      // Banka bilgileri: Netlify ortam değişkeniyle değiştirilebilir, yoksa aşağıdaki şirket hesabı kullanılır.
      iban: process.env.IBAN || 'TR32 0004 6001 9888 8000 1427 30', ibanName: process.env.IBAN_NAME || 'NO YAPIM VE ORGANİZASYON LTD. ŞTİ.', bank: process.env.IBAN_BANK || 'Akbank',
      desc: process.env.IBAN_DESC || 'Atölye Eğitim ve Organizasyon Hizmet Bedeli',
      card: tosla && typeof p.price === 'number' && p.price > 0,
    });
  }
  if (req.method === 'POST') {
    let b; try { b = await req.json(); } catch { return json(400, { error: 'bad_json' }); }
    const a = await byToken(b.b);
    if (!a || a.status !== 'approved') return json(a ? 200 : 404, { status: a?.status || 'not_found' });
    a.status = 'payment_reported'; a.reportedAt = new Date().toISOString();
    a.history = [...(a.history || []), { at: a.reportedAt, status: 'payment_reported' }];
    await apps().setJSON(a.id, a);
    await sendMail(process.env.ADMIN_EMAIL || 'hello@notiyatro.com', T.adminReported(a, siteUrl(req)));
    return json(200, { status: a.status });
  }
  return json(405, { error: 'method' });
};
export const config = { path: '/api/application' };
