// Başvuru formundan CV yükleme (PDF, DOC, DOCX; en fazla 4 MB). Dönen anahtar başvuruya eklenir.
import crypto from 'node:crypto';
import { getStore } from '@netlify/blobs';
import { json } from './lib/apps.mjs';

const MAX = 4 * 1024 * 1024;
const TYPES = [
  { ext: 'pdf', mime: 'application/pdf', magic: [0x25, 0x50, 0x44, 0x46] },
  { ext: 'docx', mime: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', magic: [0x50, 0x4b, 0x03, 0x04] },
  { ext: 'doc', mime: 'application/msword', magic: [0xd0, 0xcf, 0x11, 0xe0] },
];

export default async (req) => {
  if (req.method !== 'POST') return json(405, { error: 'method' });
  const len = Number(req.headers.get('content-length') || 0);
  if (len > MAX) return json(413, { error: 'too_big' });
  const buf = Buffer.from(await req.arrayBuffer());
  if (!buf.length) return json(400, { error: 'empty' });
  if (buf.length > MAX) return json(413, { error: 'too_big' });
  const t = TYPES.find((x) => x.magic.every((b, i) => buf[i] === b));
  if (!t) return json(415, { error: 'type' });
  const name = String(req.headers.get('x-file-name') || `cv.${t.ext}`).replace(/[^\p{L}\p{N}._ -]/gu, '').slice(0, 80) || `cv.${t.ext}`;
  const key = `${new Date().toISOString().slice(0, 10)}/${crypto.randomBytes(12).toString('hex')}.${t.ext}`;
  await getStore({ name: 'cvs', consistency: 'strong' }).set(key, buf, { metadata: { mime: t.mime, name, size: buf.length, at: new Date().toISOString() } });
  return json(200, { key, name, size: buf.length });
};
export const config = { path: '/api/cv' };
