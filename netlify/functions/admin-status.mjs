// Panel: kontenjan ayarları (kapasite, site dışı kayıt sayısı, durum modu)
import { authorized, json, clean } from './lib/apps.mjs';
import { computeStatus, readCfg, settings, MODES } from './lib/status.mjs';
import data from '../../data/programs.json' with { type: 'json' };

export default async (req) => {
  if (!authorized(req)) { await new Promise((r) => setTimeout(r, 800)); return json(401, { error: 'unauthorized' }); }
  if (req.method === 'POST') {
    let b; try { b = await req.json(); } catch { return json(400, { error: 'bad_json' }); }
    const id = clean(b.id, 60);
    if (!data.programs.some((p) => p.id === id)) return json(404, { error: 'not_found' });
    const cfg = await readCfg();
    const n = (v) => Math.max(0, Math.min(9999, parseInt(v, 10) || 0));
    cfg[id] = { capacity: n(b.capacity), offline: n(b.offline), mode: MODES.includes(b.mode) ? b.mode : 'auto' };
    await settings().setJSON('capacity', cfg);
  }
  const st = await computeStatus();
  return json(200, { programs: data.programs.map((p) => ({ id: p.id, title: p.title.tr, ...st[p.id] })) });
};
export const config = { path: '/api/admin/status' };
