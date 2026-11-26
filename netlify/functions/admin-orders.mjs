// Yönetim paneli için sipariş listesi. ADMIN_PASSWORD ortam değişkeniyle korunur.
import crypto from 'node:crypto';
import { orders } from './lib/store.mjs';

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

function authorized(req) {
  const want = (process.env.ADMIN_PASSWORD || '').trim();
  const got = (req.headers.get('authorization') || '').replace(/^Bearer\s+/i, '').trim();
  if (want.length < 10 || !got) return false;
  const a = crypto.createHash('sha256').update(want).digest();
  const b = crypto.createHash('sha256').update(got).digest();
  return crypto.timingSafeEqual(a, b);
}

export default async (req) => {
  if (!authorized(req)) {
    await new Promise((r) => setTimeout(r, 800)); // tahmin denemelerini yavaşlat
    return json(401, { error: 'unauthorized' });
  }
  const store = orders();
  const { blobs } = await store.list();
  const list = (await Promise.all(blobs.map((x) => store.get(x.key, { type: 'json' })))).filter(Boolean);
  list.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)));
  return json(200, { orders: list });
};

export const config = { path: '/api/admin/orders' };
