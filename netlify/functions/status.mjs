// Herkese açık kontenjan durumu: { programId: { state: open|few|full|closed, left } }
import { computeStatus } from './lib/status.mjs';
export default async () => {
  const all = await computeStatus().catch(() => ({}));
  const pub = Object.fromEntries(Object.entries(all).map(([k, v]) => [k, { state: v.state, left: v.left }]));
  return new Response(JSON.stringify(pub), { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=30' } });
};
export const config = { path: '/api/status' };
