// E-posta gönderimi: hello@notiyatro.com (Google Workspace) üzerinden SMTP ile.
// Netlify'da gereken anahtarlar: SMTP_USER (hello@notiyatro.com) ve SMTP_PASS (Google "uygulama şifresi").
// Ayar yoksa e-posta gönderilmez, sistem çalışmaya devam eder.
import nodemailer from 'nodemailer';

let transport = null;
export const mailReady = () => !!(process.env.SMTP_PASS || process.env.MAIL_TEST);

function getTransport() {
  if (transport) return transport;
  if (process.env.MAIL_TEST) transport = nodemailer.createTransport({ jsonTransport: true });
  else transport = nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.gmail.com', port: Number(process.env.SMTP_PORT || 465), secure: true,
    auth: { user: process.env.SMTP_USER || 'hello@notiyatro.com', pass: (process.env.SMTP_PASS || '').replace(/\s+/g, '') },
  });
  return transport;
}

export async function sendMail(to, { subject, text, html }) {
  if (!to || !mailReady()) return false;
  const from = process.env.SMTP_USER || 'hello@notiyatro.com';
  try {
    const info = await getTransport().sendMail({ from: `NO Tiyatro <${from}>`, to, replyTo: from, subject, text, html });
    if (process.env.MAIL_TEST) console.log('[mail]', to, '|', subject);
    return !!info;
  } catch (e) {
    console.error('mail failed', to, subject, e.message);
    return false;
  }
}
