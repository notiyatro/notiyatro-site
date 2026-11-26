// Yönetim paneli: başvuruları listele, onayla/reddet/ödendi işaretle
import { apps, tokens, newToken, authorized, json, payLink, clean } from './lib/apps.mjs';
import { sendMail, mailReady } from './lib/mail.mjs';
import { T as M } from './lib/templates.mjs';


export default async (req) => {
  if (!authorized(req)) { await new Promise((r) => setTimeout(r, 800)); return json(401, { error: 'unauthorized' }); }
  const store = apps();
  if (req.method === 'GET') {
    const { blobs } = await store.list();
    const list = (await Promise.all(blobs.map((x) => store.get(x.key, { type: 'json' })))).filter(Boolean);
    list.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)));
    return json(200, { applications: list.map((a) => ({ ...a, payLink: a.token ? payLink(req, a) : null })), mail: mailReady() });
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
    const notify = b.notify !== false;
    if (action === 'approve') {
      if (!a.token) { a.token = newToken(); await tokens().set(a.token, a.id); }
      a.approvedAt = now;
      if (notify) mailed = await sendMail(a.email, M.approved(a, payLink(req, a)));
    }
    if (action === 'reject' && notify) mailed = await sendMail(a.email, M.rejected(a));
    if (action === 'paid') { a.paidAt = now; if (notify) mailed = await sendMail(a.email, M.paid(a)); }
    if (mailed) a.mails = [...(a.mails || []), { at: now, type: action }];
    await store.setJSON(a.id, a);
    return json(200, { application: { ...a, payLink: a.token ? payLink(req, a) : null }, mailed });
  }
  return json(405, { error: 'method' });
};
export const config = { path: '/api/admin/applications' };
