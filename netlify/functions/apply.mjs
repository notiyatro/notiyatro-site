// Başvuru formu gönderimi
import { apps, program, json, clean, sendMail } from './lib/apps.mjs';
import { timeSpan } from './lib/tosla.mjs';

const LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

export default async (req) => {
  if (req.method !== 'POST') return json(405, { error: 'method' });
  let b; try { b = await req.json(); } catch { return json(400, { error: 'bad_json' }); }
  if (clean(b.website, 50)) return json(200, { id: 'OK' }); // bot tuzağı
  const p = program(clean(b.program, 60));
  const f = {
    name: clean(b.name, 100), birth: clean(b.birth, 10), email: clean(b.email, 120).toLowerCase(), phone: clean(b.phone, 25),
    instagram: clean(b.instagram, 60), city: clean(b.city, 60), english: clean(b.english, 2), student: b.student === 'yes' ? 'yes' : b.student === 'no' ? 'no' : '',
    school: clean(b.school, 200), last: clean(b.last, 300), why: clean(b.why, 2000),
  };
  const lang = b.lang === 'en' ? 'en' : 'tr';
  const err = (k) => json(400, { error: k });
  if (!p || p.open === false) return err('program');
  if (f.name.length < 3) return err('name');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(f.birth)) return err('birth');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email)) return err('email');
  if (f.phone.replace(/\D/g, '').length < 7) return err('phone');
  if (f.city.length < 2) return err('city');
  if (!LEVELS.includes(f.english)) return err('english');
  if (!f.student) return err('student');
  if (f.school.length < 2) return err('school');
  if (f.why.length < 10) return err('why');
  if (b.kvkk !== true) return err('kvkk');

  const store = apps();
  // aynı kişi aynı programa ikinci kez başvurmasın
  const { blobs } = await store.list();
  for (const x of blobs) {
    const a = await store.get(x.key, { type: 'json' });
    if (a && a.email === f.email && a.programId === p.id && a.status !== 'rejected') return json(200, { id: a.id, duplicate: true });
  }
  const id = `B${timeSpan().slice(2, 8)}${Math.random().toString(36).slice(2, 6).toUpperCase()}`;
  const app = { id, programId: p.id, program: p.title.tr, lang, ...f, marketing: b.marketing === true, status: 'pending', history: [{ at: new Date().toISOString(), status: 'pending' }], createdAt: new Date().toISOString() };
  await store.setJSON(id, app);
  await sendMail(process.env.ADMIN_EMAIL, `Yeni başvuru: ${f.name} — ${p.title.tr}`, `${f.name} (${f.email}, ${f.phone}) ${p.title.tr} için başvurdu.\nBaşvuru no: ${id}\nPanel: ${process.env.URL || ''}/yonetim/`);
  return json(200, { id });
};
export const config = { path: '/api/apply' };
