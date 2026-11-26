// E-posta metinleri (TR / EN). Hepsi hello@notiyatro.com'dan gider.
const WA = '+90 530 480 82 92';
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const first = (n) => String(n || '').trim().split(/\s+/)[0];

function wrap(lang, paras, button) {
  const html = `<!doctype html><html><body style="margin:0;background:#f4f2ea;font-family:Helvetica,Arial,sans-serif;color:#111">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f2ea;padding:28px 12px"><tr><td align="center">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#fff;border-radius:16px;overflow:hidden">
<tr><td style="background:#000;color:#D9D4B3;padding:20px 28px;font-size:22px;font-weight:800;letter-spacing:-.5px">n*tiyatro</td></tr>
<tr><td style="padding:28px;font-size:16px;line-height:1.6">
${paras.map((p) => `<p style="margin:0 0 16px">${p}</p>`).join('')}
${button ? `<p style="margin:24px 0"><a href="${esc(button.href)}" style="display:inline-block;background:#000;color:#fff;text-decoration:none;font-weight:700;padding:14px 24px;border-radius:999px">${esc(button.label)}</a></p><p style="margin:0 0 16px;font-size:13px;color:#666">${lang === 'en' ? 'If the button does not work, copy this link:' : 'Buton çalışmazsa bu linki kopyalayabilirsin:'}<br><a href="${esc(button.href)}" style="color:#666;word-break:break-all">${esc(button.href)}</a></p>` : ''}
</td></tr>
<tr><td style="padding:18px 28px;border-top:1px solid #eee;font-size:13px;color:#666">NO Tiyatro · International Stage Lab.<br>hello@notiyatro.com · WhatsApp ${WA}<br>Hüseyinağa Mah., İstiklal Cad., Grand Pera No: 56/58 Kat 3 Daire 5, Beyoğlu, İstanbul</td></tr>
</table></td></tr></table></body></html>`;
  const strip = (s) => s.replace(/<[^>]+>/g, '');
  const text = paras.map(strip).join('\n\n') + (button ? `\n\n${button.label}: ${button.href}` : '') + `\n\nNO Tiyatro · International Stage Lab.\nhello@notiyatro.com · WhatsApp ${WA}`;
  return { html, text };
}

export const T = {
  received(a, list) {
    const items = list.map((x) => `<b>${esc(x.program)}</b> (${esc(x.id)})`).join('<br>');
    return a.lang === 'en'
      ? { subject: 'We have received your application · NO Tiyatro', ...wrap('en', [`Hi ${esc(first(a.name))},`, `Thank you for applying. We have received your application for:<br>${items}`, 'Our team will review it carefully and get back to you by email and WhatsApp as soon as possible.', 'Warm regards,<br>NO Tiyatro'], null) }
      : { subject: 'Başvurun bize ulaştı · NO Tiyatro', ...wrap('tr', [`Merhaba ${esc(first(a.name))},`, `Başvurun için teşekkür ederiz. Aşağıdaki program(lar) için başvurun bize ulaştı:<br>${items}`, 'Ekibimiz başvurunu dikkatle inceleyip en kısa sürede e-posta ve WhatsApp üzerinden sana dönüş yapacak.', 'Sevgiyle,<br>NO Tiyatro'], null) };
  },
  approved(a, link) {
    return a.lang === 'en'
      ? { subject: `Your application has been approved · ${a.program}`, ...wrap('en', [`Hi ${esc(first(a.name))},`, `Good news: your application for <b>${esc(a.program)}</b> has been approved.`, 'To secure your place, please complete your payment using the link below. Your registration is confirmed once the payment reaches us. Places are limited, so we recommend completing it soon.', 'We look forward to seeing you,<br>NO Tiyatro'], { href: link, label: 'Complete registration' }) }
      : { subject: `Başvurun onaylandı · ${a.program}`, ...wrap('tr', [`Merhaba ${esc(first(a.name))},`, `Güzel bir haberimiz var: <b>${esc(a.program)}</b> başvurun onaylandı.`, 'Yerini ayırmak için aşağıdaki linkten ödemeni tamamlayabilirsin. Ödemen bize ulaştığında kaydın kesinleşir. Kontenjan sınırlı olduğu için ödemeyi kısa sürede yapmanı öneririz.', 'Görüşmek üzere,<br>NO Tiyatro'], { href: link, label: 'Kaydımı tamamla' }) };
  },
  rejected(a) {
    return a.lang === 'en'
      ? { subject: `About your application · ${a.program}`, ...wrap('en', [`Hi ${esc(first(a.name))},`, `Thank you for your interest in <b>${esc(a.program)}</b> and for the time you put into your application.`, 'Taking into account the limited number of places and the profile of this programme, we are unable to offer you a place this time.', 'This is not a judgement of your potential. We would be delighted to see your application again for our upcoming workshops and camps, which we announce on Instagram @notiyatro and on our WhatsApp channel.', 'Warm regards,<br>NO Tiyatro'], null) }
      : { subject: `Başvurun hakkında · ${a.program}`, ...wrap('tr', [`Merhaba ${esc(first(a.name))},`, `<b>${esc(a.program)}</b> için gösterdiğin ilgi ve başvuruna ayırdığın zaman için teşekkür ederiz.`, 'Programın sınırlı kontenjanı ve katılımcı profili göz önünde bulundurulduğunda, bu dönem başvurunu olumlu değerlendiremedik.', 'Bu karar senin potansiyelinle ilgili bir değerlendirme değil. Instagram @notiyatro hesabımızda ve WhatsApp kanalımızda duyurduğumuz yeni atölye ve kamplarımızda başvurunu yeniden görmekten mutluluk duyarız.', 'Sevgiyle,<br>NO Tiyatro'], null) };
  },
  paid(a) {
    return a.lang === 'en'
      ? { subject: `Your registration is confirmed · ${a.program}`, ...wrap('en', [`Hi ${esc(first(a.name))},`, `We have received your payment and your place on <b>${esc(a.program)}</b> is confirmed.`, 'Before the programme starts, we will send you the schedule, venue details and everything you need to know by email and WhatsApp.', 'See you soon,<br>NO Tiyatro'], null) }
      : { subject: `Kaydın kesinleşti · ${a.program}`, ...wrap('tr', [`Merhaba ${esc(first(a.name))},`, `Ödemen bize ulaştı; <b>${esc(a.program)}</b> kaydın kesinleşti.`, 'Program başlamadan önce program akışını, mekân bilgilerini ve bilmen gereken her şeyi e-posta ve WhatsApp üzerinden paylaşacağız.', 'Görüşmek üzere,<br>NO Tiyatro'], null) };
  },
  adminNew(a, list, url) {
    const t = `${a.name} (${a.email}, ${a.phone}) başvurdu:\n${list.map((x) => `- ${x.program} (${x.id})`).join('\n')}\n\nPanel: ${url}/yonetim/`;
    return { subject: `Yeni başvuru: ${a.name}`, text: t, html: `<pre style="font-family:Helvetica,Arial,sans-serif;font-size:15px">${esc(t)}</pre>` };
  },
  adminReported(a, url) {
    const t = `${a.name} (${a.program}) havale/EFT yaptığını bildirdi. Başvuru no: ${a.id}\nHesabı kontrol edip panelden "Ödendi" olarak işaretle: ${url}/yonetim/`;
    return { subject: `Ödeme bildirimi: ${a.name}`, text: t, html: `<pre style="font-family:Helvetica,Arial,sans-serif;font-size:15px">${esc(t)}</pre>` };
  },
};
