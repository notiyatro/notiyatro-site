// Yönetim paneli: başvuruları listele, onayla/reddet/ödendi işaretle
import { apps, tokens, newToken, authorized, json, payLink, sendMail, clean } from './lib/apps.mjs';

const T = {
  tr: (a, link) => ({ subject: `Başvurun onaylandı: ${a.program}`, text: `Merhaba ${a.name},\n\n${a.program} başvurun onaylandı. Kaydını tamamlamak için ödeme bilgilerine aşağıdaki linkten ulaşabilirsin:\n\n${link}\n\nSorun olursa bu e-postayı yanıtlayabilir ya da WhatsApp'tan (+90 530 480 82 92) yazabilirsin.\n\nNO Tiyatro · International Stage Lab.` }),
  en: (a, link) => ({ subject: `Your application is approved: ${a.program}`, text: `Hi ${a.name},\n\nYour application for ${a.program} has been approved. To complete your registration, find the payment details here:\n\n${link}\n\nIf you have any questions, reply to this email or message us on WhatsApp (+90 530 480 82 92).\n\nNO Tiyatro · International Stage Lab.` }),
};

export default async (req) => {
  if (!authorized(req)) { await new Promise((r) => setTimeout(r, 800)); return json(401, { error: 'unauthorized' }); }
  const store = apps();
  if (req.method === 'GET') {
    const { blobs } = await store.list();
    const list = (await Promise.all(blobs.map((x) => store.get(x.key, { type: 'json' })))).filter(Boolean);
    list.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)));
    return json(200, { applications: list.map((a) => ({ ...a, payLink: a.token ? payLink(req, a) : null })), mail: !!(process.env.RESEND_API_KEY && process.env.MAIL_FROM) });
  }
  if (req.method === 'POST') {
    let b; try { b = await req.json(); } catch { return json(400, { error: 'bad_json' }); }
    const a = await store.get(clean(b.id, 40), { type: 'json' });
    if (!a) return json(404, { error: 'not_found' });
    const action = b.action, now = new Date().toISOString();
    const map = { approve: 'approved', reject: 'rejected', paid: 'paid', pending: 'pending' };
    if (!map[action]) return json(400, { error: 'action' });
    a.status = map[action];
    if (typeof b.note === 'string') a.note = clean(b.note, 500);
    a.history = [...(a.history || []), { at: now, status: a.status, by: 'panel' }];
    let mailed = false;
    if (action === 'approve') {
      if (!a.token) { a.token = newToken(); await tokens().set(a.token, a.id); }
      a.approvedAt = now;
      const m = (T[a.lang] || T.tr)(a, payLink(req, a));
      mailed = await sendMail(a.email, m.subject, m.text);
      a.mailedAt = mailed ? now : a.mailedAt;
    }
    if (action === 'paid') a.paidAt = now;
    await store.setJSON(a.id, a);
    return json(200, { application: { ...a, payLink: a.token ? payLink(req, a) : null }, mailed });
  }
  return json(405, { error: 'method' });
};
export const config = { path: '/api/admin/applications' };
