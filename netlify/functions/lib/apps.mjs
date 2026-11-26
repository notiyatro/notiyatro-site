// Başvurular: "applications" deposu (anahtar = başvuru no), "app-tokens" (ödeme linki jetonu -> başvuru no)
import crypto from 'node:crypto';
import { getStore } from '@netlify/blobs';
import data from '../../../data/programs.json' with { type: 'json' };

export const apps = () => getStore({ name: 'applications', consistency: 'strong' });
export const tokens = () => getStore({ name: 'app-tokens', consistency: 'strong' });
export const program = (id) => data.programs.find((p) => p.id === id);
export const newToken = () => crypto.randomBytes(18).toString('base64url');
export const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
export const clean = (v, max) => String(v ?? '').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f<>]/g, '').trim().slice(0, max);

export function authorized(req) {
  const want = (process.env.ADMIN_PASSWORD || '').trim();
  const got = (req.headers.get('authorization') || '').replace(/^Bearer\s+/i, '').trim();
  if (want.length < 10 || !got) return false;
  const a = crypto.createHash('sha256').update(want).digest();
  const b = crypto.createHash('sha256').update(got).digest();
  return crypto.timingSafeEqual(a, b);
}

export async function byToken(t) {
  if (!t || t.length < 16) return null;
  const id = await tokens().get(String(t).slice(0, 64));
  return id ? apps().get(id, { type: 'json' }) : null;
}

export const siteUrl = (req) => process.env.URL || new URL(req.url).origin;
export const payLink = (req, a) => `${siteUrl(req)}${a.lang === 'en' ? '/en/payment/' : '/odeme/'}?b=${a.token}`;

// İsteğe bağlı e-posta (Resend). RESEND_API_KEY ve MAIL_FROM yoksa sessizce atlanır.
export async function sendMail(to, subject, text) {
  const key = process.env.RESEND_API_KEY, from = process.env.MAIL_FROM;
  if (!key || !from || !to) return false;
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to: [to], subject, text, reply_to: process.env.ADMIN_EMAIL || undefined }),
    });
    return r.ok;
  } catch { return false; }
}
