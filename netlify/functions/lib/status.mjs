// Kontenjan durumu: ödenen + onaylanan (ödeme bekleyen) başvurular + panelden girilen "site dışı kayıt" sayısı
import { getStore } from '@netlify/blobs';
import data from '../../../data/programs.json' with { type: 'json' };
import { apps } from './apps.mjs';

export const settings = () => getStore({ name: 'settings', consistency: 'strong' });
export const MODES = ['auto', 'open', 'few', 'full', 'closed'];
const HOLD = ['approved', 'payment_reported', 'paid'];

export async function readCfg() { return (await settings().get('capacity', { type: 'json' })) || {}; }

export async function computeStatus() {
  const cfg = await readCfg();
  const store = apps();
  const { blobs } = await store.list();
  const list = (await Promise.all(blobs.map((b) => store.get(b.key, { type: 'json' })))).filter(Boolean);
  const out = {};
  for (const p of data.programs) {
    const c = cfg[p.id] || {};
    const cap = Number(c.capacity ?? p.capacity) || 0;
    const mine = list.filter((a) => a.programId === p.id);
    const paid = mine.filter((a) => a.status === 'paid').length;
    const held = mine.filter((a) => HOLD.includes(a.status) && a.status !== 'paid').length;
    const offline = Math.max(0, Number(c.offline) || 0);
    const taken = paid + held + offline;
    const left = cap ? Math.max(0, cap - taken) : null;
    const mode = MODES.includes(c.mode) ? c.mode : 'auto';
    let state = 'open';
    if (p.open === false) state = 'closed';
    else if (mode !== 'auto') state = mode;
    else if (cap && left === 0) state = 'full';
    else if (cap && left <= Math.max(3, Math.ceil(cap * 0.2))) state = 'few';
    out[p.id] = { state, left: state === 'few' && mode === 'auto' ? left : null, cap, paid, held, offline, taken, mode };
  }
  return out;
}
