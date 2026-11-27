// Hediyeler siparişlerinde müşteriye giden e-postalar (8 dil).
// kind: 'received' (kartla ödeme açık değilken sipariş alındı) | 'paid' (kartla ödeme onaylandı)
const T = {
  tr: {
    subj_received: 'Siparişini aldık · {id}', subj_paid: 'Ödemen alındı, siparişin hazırlanıyor · {id}',
    hello: 'Merhaba {name},',
    received: 'NO Tiyatro Hediyeler’den verdiğin sipariş bize ulaştı, teşekkür ederiz. Ödeme ve teslimat ayrıntıları için en kısa sürede seninle iletişime geçeceğiz. Ödeme tamamlanmadan ürün gönderimi yapılmaz.',
    paid: 'Ödemen başarıyla alındı, teşekkür ederiz. Siparişin özenle hazırlanıyor; kargoya verildiğinde takip numarasını ayrıca ileteceğiz.',
    summary: 'Sipariş özeti', order: 'Sipariş no', subtotal: 'Ara toplam', shipping: 'Kargo', total: 'Toplam', vat: 'KDV dahil', free: 'Ücretsiz',
    delivery: 'Teslimat', ship: 'Yurtiçi Kargo ile şu adrese gönderilecek:', pickup: 'Atölyede elden teslim edilecek. Teslim günü ve yeri sana ayrıca bildirilecek.',
    eta: 'Siparişler ödeme onayından sonra genellikle 5 iş günü içinde kargoya verilir.',
    rights: 'Ürünü teslim aldığın tarihten itibaren 14 gün içinde cayma hakkın bulunur. Ayrıntılar için:', pre: 'Ön Bilgilendirme Formu', contract: 'Mesafeli Satış Sözleşmesi',
    help: 'Herhangi bir soru ya da sorunda bu e-postayı yanıtlayabilir veya WhatsApp’tan bize yazabilirsin:',
    bye: 'Sevgiyle,', team: 'NO Tiyatro ekibi',
  },
  en: {
    subj_received: 'We’ve received your order · {id}', subj_paid: 'Payment received, your order is being prepared · {id}',
    hello: 'Hello {name},',
    received: 'Thank you for your order from NO Tiyatro Gifts. We have received it and will contact you shortly about payment and delivery. Orders are dispatched only once payment is complete.',
    paid: 'Thank you, your payment has been received. Your order is now being carefully prepared, and we will send you the tracking number as soon as it ships.',
    summary: 'Order summary', order: 'Order no', subtotal: 'Subtotal', shipping: 'Shipping', total: 'Total', vat: 'VAT included', free: 'Free',
    delivery: 'Delivery', ship: 'Will be sent with Yurtiçi Kargo to:', pickup: 'To be collected at a workshop. We will let you know the date and place.',
    eta: 'Orders are usually dispatched within 5 working days of payment confirmation.',
    rights: 'You may withdraw from the purchase within 14 days of receiving the item. Details:', pre: 'Pre-Information Form', contract: 'Distance Sales Contract',
    help: 'If you have any questions, simply reply to this email or message us on WhatsApp:',
    bye: 'Warm regards,', team: 'The NO Tiyatro team',
  },
  de: {
    subj_received: 'Wir haben Ihre Bestellung erhalten · {id}', subj_paid: 'Zahlung erhalten, Ihre Bestellung wird vorbereitet · {id}',
    hello: 'Hallo {name},',
    received: 'vielen Dank für Ihre Bestellung bei NO Tiyatro Geschenke. Sie ist bei uns eingegangen; wir melden uns in Kürze wegen Zahlung und Lieferung. Der Versand erfolgt erst nach Zahlungseingang.',
    paid: 'vielen Dank, Ihre Zahlung ist eingegangen. Ihre Bestellung wird nun sorgfältig vorbereitet; die Sendungsnummer schicken wir Ihnen, sobald das Paket unterwegs ist.',
    summary: 'Bestellübersicht', order: 'Bestellnr.', subtotal: 'Zwischensumme', shipping: 'Versand', total: 'Gesamt', vat: 'inkl. MwSt.', free: 'Kostenlos',
    delivery: 'Lieferung', ship: 'Versand mit Yurtiçi Kargo an:', pickup: 'Abholung beim Workshop. Datum und Ort teilen wir Ihnen mit.',
    eta: 'Bestellungen werden in der Regel innerhalb von 5 Werktagen nach Zahlungsbestätigung versandt.',
    rights: 'Sie haben ab Erhalt der Ware ein 14-tägiges Widerrufsrecht. Einzelheiten (auf Türkisch):', pre: 'Vorabinformationen', contract: 'Fernabsatzvertrag',
    help: 'Bei Fragen antworten Sie einfach auf diese E-Mail oder schreiben Sie uns auf WhatsApp:',
    bye: 'Herzliche Grüße', team: 'Ihr NO-Tiyatro-Team',
  },
  ru: {
    subj_received: 'Ваш заказ получен · {id}', subj_paid: 'Оплата получена, заказ готовится · {id}',
    hello: 'Здравствуйте, {name}!',
    received: 'Благодарим за заказ в разделе «Подарки» NO Tiyatro. Мы его получили и в ближайшее время свяжемся с вами по поводу оплаты и доставки. Заказ отправляется только после оплаты.',
    paid: 'Спасибо, ваша оплата получена. Мы бережно готовим заказ и пришлём трек-номер, как только передадим его в доставку.',
    summary: 'Состав заказа', order: 'Номер заказа', subtotal: 'Подытог', shipping: 'Доставка', total: 'Итого', vat: 'с НДС', free: 'Бесплатно',
    delivery: 'Доставка', ship: 'Будет отправлен службой Yurtiçi Kargo по адресу:', pickup: 'Получение на мастер-классе. Дату и место мы сообщим отдельно.',
    eta: 'Обычно заказы передаются в доставку в течение 5 рабочих дней после подтверждения оплаты.',
    rights: 'Вы можете отказаться от покупки в течение 14 дней с момента получения товара. Подробнее (на турецком):', pre: 'Предварительная информация', contract: 'Договор дистанционной продажи',
    help: 'Если у вас есть вопросы, просто ответьте на это письмо или напишите нам в WhatsApp:',
    bye: 'С теплом,', team: 'команда NO Tiyatro',
  },
  fr: {
    subj_received: 'Nous avons bien reçu votre commande · {id}', subj_paid: 'Paiement reçu, votre commande est en préparation · {id}',
    hello: 'Bonjour {name},',
    received: 'Merci pour votre commande sur NO Tiyatro Cadeaux. Nous l’avons bien reçue et vous contacterons très prochainement pour le paiement et la livraison. L’envoi n’a lieu qu’après réception du paiement.',
    paid: 'Merci, votre paiement a bien été reçu. Votre commande est préparée avec soin ; nous vous enverrons le numéro de suivi dès son expédition.',
    summary: 'Récapitulatif', order: 'N° de commande', subtotal: 'Sous-total', shipping: 'Livraison', total: 'Total', vat: 'TVA incluse', free: 'Gratuit',
    delivery: 'Livraison', ship: 'Envoi par Yurtiçi Kargo à l’adresse :', pickup: 'Retrait lors d’un atelier. Nous vous indiquerons la date et le lieu.',
    eta: 'Les commandes sont généralement expédiées sous 5 jours ouvrés après confirmation du paiement.',
    rights: 'Vous disposez d’un droit de rétractation de 14 jours à compter de la réception. Détails (en turc) :', pre: 'Information préalable', contract: 'Contrat de vente à distance',
    help: 'Pour toute question, répondez simplement à cet e-mail ou écrivez-nous sur WhatsApp :',
    bye: 'Bien chaleureusement,', team: 'L’équipe NO Tiyatro',
  },
  es: {
    subj_received: 'Hemos recibido tu pedido · {id}', subj_paid: 'Pago recibido, estamos preparando tu pedido · {id}',
    hello: 'Hola, {name}:',
    received: 'Gracias por tu pedido en NO Tiyatro Regalos. Lo hemos recibido y te contactaremos en breve para el pago y la entrega. El envío se realiza solo cuando el pago está completado.',
    paid: 'Gracias, hemos recibido tu pago. Estamos preparando tu pedido con cuidado y te enviaremos el número de seguimiento en cuanto salga.',
    summary: 'Resumen del pedido', order: 'N.º de pedido', subtotal: 'Subtotal', shipping: 'Envío', total: 'Total', vat: 'IVA incluido', free: 'Gratis',
    delivery: 'Entrega', ship: 'Se enviará con Yurtiçi Kargo a:', pickup: 'Recogida en un taller. Te indicaremos la fecha y el lugar.',
    eta: 'Los pedidos suelen enviarse en un plazo de 5 días laborables tras confirmar el pago.',
    rights: 'Tienes 14 días desde la recepción para desistir de la compra. Detalles (en turco):', pre: 'Información previa', contract: 'Contrato de venta a distancia',
    help: 'Si tienes alguna pregunta, responde a este correo o escríbenos por WhatsApp:',
    bye: 'Un abrazo,', team: 'El equipo de NO Tiyatro',
  },
  it: {
    subj_received: 'Abbiamo ricevuto il tuo ordine · {id}', subj_paid: 'Pagamento ricevuto, stiamo preparando il tuo ordine · {id}',
    hello: 'Ciao {name},',
    received: 'grazie per il tuo ordine su NO Tiyatro Regali. L’abbiamo ricevuto e ti contatteremo a breve per pagamento e consegna. La spedizione avviene solo a pagamento completato.',
    paid: 'grazie, abbiamo ricevuto il tuo pagamento. Stiamo preparando il tuo ordine con cura e ti invieremo il numero di tracciamento appena partirà.',
    summary: 'Riepilogo ordine', order: 'N. ordine', subtotal: 'Subtotale', shipping: 'Spedizione', total: 'Totale', vat: 'IVA inclusa', free: 'Gratuita',
    delivery: 'Consegna', ship: 'Sarà spedito con Yurtiçi Kargo a:', pickup: 'Ritiro a un workshop. Ti comunicheremo data e luogo.',
    eta: 'Gli ordini vengono di solito spediti entro 5 giorni lavorativi dalla conferma del pagamento.',
    rights: 'Hai 14 giorni dal ricevimento per recedere dall’acquisto. Dettagli (in turco):', pre: 'Informazioni precontrattuali', contract: 'Contratto di vendita a distanza',
    help: 'Per qualsiasi domanda, rispondi a questa e-mail o scrivici su WhatsApp:',
    bye: 'Un caro saluto,', team: 'Il team di NO Tiyatro',
  },
  el: {
    subj_received: 'Λάβαμε την παραγγελία σας · {id}', subj_paid: 'Η πληρωμή ελήφθη, η παραγγελία σας ετοιμάζεται · {id}',
    hello: 'Γεια σας {name},',
    received: 'σας ευχαριστούμε για την παραγγελία σας από τα Δώρα του NO Tiyatro. Τη λάβαμε και θα επικοινωνήσουμε σύντομα μαζί σας για την πληρωμή και την παράδοση. Η αποστολή γίνεται μόνο μετά την ολοκλήρωση της πληρωμής.',
    paid: 'σας ευχαριστούμε, η πληρωμή σας ελήφθη. Η παραγγελία σας ετοιμάζεται με φροντίδα και θα σας στείλουμε τον αριθμό αποστολής μόλις αναχωρήσει.',
    summary: 'Σύνοψη παραγγελίας', order: 'Αρ. παραγγελίας', subtotal: 'Μερικό σύνολο', shipping: 'Μεταφορικά', total: 'Σύνολο', vat: 'με ΦΠΑ', free: 'Δωρεάν',
    delivery: 'Παράδοση', ship: 'Θα αποσταλεί με Yurtiçi Kargo στη διεύθυνση:', pickup: 'Παραλαβή σε εργαστήριο. Θα σας ενημερώσουμε για ημερομηνία και τόπο.',
    eta: 'Οι παραγγελίες συνήθως αποστέλλονται εντός 5 εργάσιμων ημερών από την επιβεβαίωση της πληρωμής.',
    rights: 'Έχετε δικαίωμα υπαναχώρησης 14 ημερών από την παραλαβή. Λεπτομέρειες (στα τουρκικά):', pre: 'Προσυμβατική ενημέρωση', contract: 'Σύμβαση εξ αποστάσεως πώλησης',
    help: 'Για οποιαδήποτε ερώτηση, απαντήστε σε αυτό το email ή γράψτε μας στο WhatsApp:',
    bye: 'Με εκτίμηση,', team: 'Η ομάδα του NO Tiyatro',
  },
};

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tl = (n) => `${Number(n).toLocaleString('tr-TR')} TL`;
const SITE = 'https://notiyatro.com';
const WA = '+90 530 480 82 92', WA_URL = 'https://wa.me/905304808292';

export function customerMail(kind, o) {
  const t = T[o.lang] || T.en;
  const first = String(o.name || '').trim().split(/\s+/)[0] || '';
  const items = o.items || [];
  const subtotal = o.subtotal ?? items.reduce((s, i) => s + i.line, 0);
  const ship = o.shipping ?? 0;
  const row = (l, r, b) => `<tr><td style="padding:8px 0;border-bottom:1px solid #eee;${b ? 'font-weight:800;font-size:16px;border-bottom:0;' : ''}">${l}</td><td align="right" style="padding:8px 0;border-bottom:1px solid #eee;white-space:nowrap;${b ? 'font-weight:800;font-size:16px;border-bottom:0;' : ''}">${r}</td></tr>`;
  const lines = items.map((i) => row(`${i.qty} × ${esc(i.name)}${i.size ? ' · ' + esc(i.size) : ''}`, tl(i.line))).join('');
  const deliv = o.delivery === 'pickup' ? esc(t.pickup)
    : `${esc(t.ship)}<br><span style="color:#333">${esc(o.name)}<br>${esc(o.address)}<br>${esc(o.city)}</span><br><span style="color:#666;font-size:13px">${esc(t.eta)}</span>`;
  const html = `<!doctype html><html lang="${esc(o.lang || 'tr')}"><body style="margin:0;background:#F3EFD8;padding:24px 12px;font-family:Helvetica,Arial,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden">
<tr><td style="background:#000;padding:22px 28px"><span style="font:900 30px/1 Helvetica,Arial,sans-serif;color:#F3EFD8;letter-spacing:-1px">n<span style="color:#E4452F">*</span></span><span style="font:700 13px Helvetica,Arial,sans-serif;color:#F3EFD8;margin-left:12px;vertical-align:6px">NO Tiyatro</span></td></tr>
<tr><td style="padding:28px">
<p style="margin:0 0 14px;font-size:16px">${esc(t.hello.replace('{name}', first))}</p>
<p style="margin:0 0 24px;font-size:15px;line-height:1.6">${esc(t[kind])}</p>
<p style="margin:0 0 6px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#E4452F">${esc(t.summary)}</p>
<p style="margin:0 0 8px;font-size:13px;color:#666">${esc(t.order)}: <b style="color:#111">${esc(o.orderId)}</b></p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:14px">${lines}${row(esc(t.subtotal), tl(subtotal))}${row(esc(t.shipping), ship ? tl(ship) : esc(t.free))}${row(`${esc(t.total)} <span style="font-weight:400;font-size:12px;color:#666">(${esc(t.vat)})</span>`, tl(o.amount), true)}</table>
<p style="margin:24px 0 6px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#E4452F">${esc(t.delivery)}</p>
<p style="margin:0;font-size:14px;line-height:1.6">${deliv}</p>
<p style="margin:24px 0 0;font-size:13px;line-height:1.6;color:#444">${esc(t.rights)} <a href="${SITE}/yasal/urun-on-bilgilendirme/" style="color:#111">${esc(t.pre)}</a> · <a href="${SITE}/yasal/mesafeli-satis-sozlesmesi/" style="color:#111">${esc(t.contract)}</a></p>
<p style="margin:14px 0 0;font-size:13px;line-height:1.6;color:#444">${esc(t.help)} <a href="${WA_URL}" style="color:#111">${WA}</a></p>
<p style="margin:28px 0 0;font-size:15px;line-height:1.5">${esc(t.bye)}<br><b>${esc(t.team)}</b></p>
</td></tr>
<tr><td style="background:#111;padding:18px 28px;font-size:12px;line-height:1.6;color:#bbb">NO Tiyatro · NO Yapım ve Organizasyon Ltd. Şti.<br>Hüseyinağa Mah., İstiklal Cad., Grand Pera No: 56/58 Kat 3 Daire 5, Beyoğlu, İstanbul<br><a href="${SITE}" style="color:#F3EFD8">notiyatro.com</a> · <a href="https://instagram.com/notiyatro" style="color:#F3EFD8">@notiyatro</a> · <a href="mailto:hello@notiyatro.com" style="color:#F3EFD8">hello@notiyatro.com</a></td></tr>
</table></body></html>`;
  const text = [t.hello.replace('{name}', first), '', t[kind], '', `${t.order}: ${o.orderId}`,
    ...items.map((i) => `${i.qty} × ${i.name}${i.size ? ' · ' + i.size : ''} — ${tl(i.line)}`),
    `${t.subtotal}: ${tl(subtotal)}`, `${t.shipping}: ${ship ? tl(ship) : t.free}`, `${t.total} (${t.vat}): ${tl(o.amount)}`, '',
    `${t.delivery}: ${o.delivery === 'pickup' ? t.pickup : `${t.ship} ${o.address}, ${o.city}`}`, '',
    `${t.rights} ${SITE}/yasal/urun-on-bilgilendirme/`, `${t.help} ${WA}`, '', t.bye, t.team, 'notiyatro.com'].join('\n');
  return { subject: `NO Tiyatro · ${t['subj_' + kind].replace('{id}', o.orderId)}`, html, text };
}
