// Yönetim paneli: başvurudaki CV dosyasını indir (şifre gerekir)
import { getStore } from '@netlify/blobs';
import { authorized, json } from './lib/apps.mjs';

export default async (req) => {
  if (!authorized(req)) return json(401, { error: 'unauthorized' });
  const key = new URL(req.url).searchParams.get('key') || '';
  if (!/^\d{4}-\d{2}-\d{2}\/[a-f0-9]{24}\.(pdf|docx|doc)$/.test(key)) return json(400, { error: 'key' });
  const r = await getStore({ name: 'cvs', consistency: 'strong' }).getWithMetadata(key, { type: 'arrayBuffer' });
  if (!r) return json(404, { error: 'not_found' });
  return new Response(r.data, { headers: { 'Content-Type': r.metadata?.mime || 'application/octet-stream', 'Content-Disposition': `inline; filename="${encodeURIComponent(r.metadata?.name || 'cv')}"`, 'Cache-Control': 'no-store' } });
};
export const config = { path: '/api/admin/cv' };
