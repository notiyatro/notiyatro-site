// Sertifika doğrulama: /api/cert?code=ISL-GLB-IST-2026-0001
// Veriler sunucu tarafında tutulur; liste herkese açık değildir, sadece tam kodla tek kayıt döner.
import data from './data/certificates.json' with { type: 'json' };
const json = (s, b) => new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
export default async (req) => {
  const raw = new URL(req.url).searchParams.get('code') || '';
  const code = raw.toUpperCase().replace(/[\s_]+/g, '').replace(/[–—]/g, '-').slice(0, 40);
  if (!/^[A-Z0-9-]{6,40}$/.test(code)) return json(400, { valid: false, error: 'format' });
  const c = data[code];
  if (!c || c.status !== 'VALID') { await new Promise((r) => setTimeout(r, 500)); return json(200, { valid: false }); }
  return json(200, { valid: true, code, name: c.name, programme: c.programme, focus: c.focus, group: c.group, dates: c.dates, hours: c.hours, issued: c.issued, by: c.by });
};
export const config = { path: '/api/cert' };
