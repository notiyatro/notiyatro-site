// Kurulum kontrolü: hiçbir gizli değeri göstermez, sadece ayarların varlığını söyler.
export default async () => {
  const pw = process.env.ADMIN_PASSWORD;
  const body = {
    functions: 'ok',
    admin_password: !pw ? 'missing' : pw.length < 10 ? 'too_short' : pw.trim() !== pw ? 'has_spaces' : 'ok',
    tosla: process.env.TOSLA_CLIENT_ID ? 'set' : 'not_set',
    time: new Date().toISOString(),
  };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
};
export const config = { path: '/api/health' };
