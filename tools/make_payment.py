"""Ödeme sayfaları, sonuç sayfaları ve yönetim paneli.
Kullanım:  python3 make_payment.py --patch   (index.html'deki PAY listesini programs.json'dan günceller)
           python3 make_payment.py           (sayfaları üretir; make_en.py'den sonra çalıştır)"""
import re, os, sys, json
ROOT = '/home/claude/notiyatro'
CAT = json.load(open(f'{ROOT}/data/programs.json'))['programs']
PAID = [p['id'] for p in CAT if isinstance(p.get('price'), (int, float)) and p['price'] > 0]

if '--patch' in sys.argv:
    p = f'{ROOT}/index.html'; s = open(p).read()
    s2 = re.sub(r"const PAY = \[[^\]]*\];", "const PAY = " + json.dumps(PAID) + ";", s)
    assert 'const PAY = ' in s2, 'PAY line missing in index.html'
    open(p, 'w').write(s2); print('patched PAY', PAID); sys.exit()

def part(src, start, end):
    i = src.index(start); j = src.index(end, i) + len(end); return src[i:j]

def shell(lang, prefix, lang_href, title, css, body, js, noindex=False):
    src = open(f'{ROOT}/index.html' if lang == 'tr' else f'{ROOT}/en/index.html').read()
    head = src[:src.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head)
    head = re.sub(r'<link rel="alternate".*?\n', '', head)
    head = re.sub(r'<link rel="canonical".*?\n', '', head)
    head = re.sub(r'<meta name="description".*?>\n?', '', head)
    if noindex: head = head.replace('<title>', '<meta name="robots" content="noindex,nofollow">\n<title>', 1)
    head = head.replace('</style>', css + '</style>', 1)
    i = src.index('<svg width="0" height="0"'); j = src.index('</defs>', i); j = src.index('</svg>', j) + 6
    defs = src[i:j]
    header = part(src, '<header id="top">', '</header>')
    footer = part(src, '<footer class="band" id="iletisim">', '</footer>')
    def fix(s):
        def rel(m):
            attr, url = m.group(1), m.group(2)
            if re.match(r'^(https?:|mailto:|tel:|/|data:|javascript:)', url): return m.group(0)
            if url == '#top': return m.group(0)
            if url.startswith('#'): return f'{attr}="{prefix}{url}"'
            return f'{attr}="{prefix}{url}"'
        s = re.sub(r'(?<![\w-])(href|src)="([^"]*)"', lambda m: m.group(0) if m.group(0).startswith('href="#') and False else rel(m), s)
        # SVG <use href="#..."> referanslarını geri al
        s = re.sub(r'(<use\b[^>]*?)href="' + re.escape(prefix) + '#', r'\1href="#', s)
        s = re.sub(r'(<a class="lang" href=")[^"]*"', r'\g<1>' + lang_href + '"', s)
        return s
    header, footer = fix(header), fix(footer)
    menu_js = '''<script>{const h=document.getElementById('top'),m=document.getElementById('menu');m&&m.addEventListener('click',()=>{const o=h.classList.toggle('open');m.setAttribute('aria-expanded',o)})}</script>'''
    return (re.sub(r'<html lang="[a-z]+">', f'<html lang="{lang}">', head) + '</head>\n<body>\n' + defs + '\n' + header +
            '\n<main>\n' + body + '\n</main>\n' + footer + '\n' + menu_js + '\n' + js + '\n</body>\n</html>\n')

T = {
 'tr': dict(
   title='Ödeme — NO Tiyatro', kick='Güvenli ödeme', h1='Kaydını tamamla',
   summary='Program', total='Toplam', inst='Taksit', single='Tek çekim', x='taksit',
   you='Bilgilerin', name='Ad soyad', email='E-posta', phone='Telefon (WhatsApp)',
   card='Kart bilgileri', holder='Kart üzerindeki isim', cardno='Kart numarası', exp='Son kullanma (AA/YY)', cvv='CVV',
   consent='<a href="{p}yasal/{c}/" target="_blank">{cn}</a>\'ni ve <a href="{p}yasal/on-bilgilendirme/" target="_blank">Ön Bilgilendirme Formu</a>\'nu okudum, kabul ediyorum. <a href="{p}yasal/kvkk/" target="_blank">KVKK Aydınlatma Metni</a>\'ni okudum.',
   cn=dict(atolye='Atölye Katılım Sözleşmesi', kamp='Kamp Katılım Sözleşmesi'),
   mkt='<b>İsteğe bağlı:</b> Gelecekteki atölye ve kamplar hakkında bilgilendirme almak ve verilerimin bu amaçla işlenmesi için açık rıza veriyorum.',
   minor='18 yaşından küçüksen kayıt veli onayıyla yapılır; ödemeden sonra velinin bilgileri için seninle iletişime geçeriz.',
   refund_ok='{d} tarihine kadar iptal edersen ücretin tamamı iade edilir.', refund_no='Programa {n} günden az kaldığı için bu kayıtta iade yapılmaz.',
   pay='öde', paying='Bankaya yönlendiriliyorsun…',
   secure='Kart bilgilerin NO Tiyatro\'nun sunucularına iletilmez. Ödeme, Akbank iştiraki AKÖde\'nin Tosla İşim altyapısında 3D Secure ile alınır.',
   notfound='Bu program için online ödeme açık değil.', notfound2='Kayıt için WhatsApp\'tan yazabilirsin.',
   wa='WhatsApp\'tan yaz', back='Tüm atölyeler', backhref='atolyeler/',
   err=dict(name='Adını ve soyadını yaz.', email='Geçerli bir e-posta adresi yaz.', phone='Telefon numaranı yaz.',
            holder='Kart üzerindeki ismi yaz.', cardno='Kart numarası geçersiz görünüyor.', exp='Son kullanma tarihini AA/YY olarak yaz.',
            expired='Kartın son kullanma tarihi geçmiş.', cvv='CVV 3 ya da 4 haneli olmalı.', consent='Devam etmek için sözleşmeleri onaylaman gerekiyor.',
            not_configured='Online ödeme şu an etkin değil. Kayıt için WhatsApp\'tan yazabilirsin.',
            gateway='Ödeme sistemi şu an yanıt vermiyor. Biraz sonra tekrar dene ya da WhatsApp\'tan yaz.',
            network='Bağlantı kurulamadı. İnternetini kontrol edip tekrar dene.', program='Bu program için online ödeme açık değil.'),
   regmsg=' programına kayıt olmak istiyorum',
   hello='Merhaba {n}, başvurun onaylandı. Kaydını tamamlamak için ödemeni yapabilirsin.', bank_h='Havale / EFT ile öde', bank_name='Alıcı', bank_bank='Banka', bank_ref='Açıklama', amount='Tutar', copy='Kopyala', copied='Kopyalandı',
   bank_note='Açıklama alanına yukarıdaki metni, başvuru numaranla birlikte yazmayı unutma. Ödemen hesabımıza geçince kaydını kesinleştirip sana haber vereceğiz.', qr='Akbank ya da mobil bankacılık uygulamanla bu kodu okutarak da ödeme yapabilirsin.', qr_alt='Akbank ödeme QR kodu',
   bank_done='Ödemeyi yaptım', bank_reported='Ödeme bildirimin bize ulaştı. Hesabımıza geçtiğinde kaydını kesinleştirip sana haber vereceğiz.',
   bank_paid='Ödemen onaylandı, kaydın tamam. Görüşmek üzere!', card_h='ya da kartla öde', badlink='Bu ödeme linki geçersiz ya da başvurun henüz onaylanmamış.',
   noiban='Banka bilgileri birazdan burada olacak. Şimdilik WhatsApp\'tan yazabilirsin.', bconsent='Devam etmek için sözleşmeyi onaylaman gerekiyor.'),
 'en': dict(
   title='Payment — NO Tiyatro', kick='Secure payment', h1='Complete your registration',
   summary='Programme', total='Total', inst='Instalments', single='Single payment', x='instalments',
   you='Your details', name='Full name', email='Email', phone='Phone (WhatsApp)',
   card='Card details', holder='Name on card', cardno='Card number', exp='Expiry (MM/YY)', cvv='CVV',
   consent='I have read and accept the <a href="{p}yasal/{c}/" target="_blank">{cn}</a> and the <a href="{p}yasal/on-bilgilendirme/" target="_blank">Pre-Information Form</a>, and I have read the <a href="{p}yasal/kvkk/" target="_blank">Privacy Notice (KVKK)</a>. <small>(Documents in Turkish.)</small>',
   cn=dict(atolye='Workshop Participation Agreement', kamp='Camp Participation Agreement'),
   mkt='<b>Optional:</b> I consent to receiving information about future workshops and camps and to my data being processed for that purpose.',
   minor='If you are under 18, registration requires a parent or guardian’s consent; we will contact you after payment for their details.',
   refund_ok='Cancel by {d} for a full refund.', refund_no='Fewer than {n} days remain before the programme, so this booking is non-refundable.',
   pay='Pay', paying='Redirecting you to your bank…',
   secure='Your card details never reach NO Tiyatro’s servers. The payment is taken with 3D Secure on Tosla İşim, run by AKÖde, a subsidiary of Akbank.',
   notfound='Online payment is not open for this programme.', notfound2='Message us on WhatsApp to register.',
   wa='Message us on WhatsApp', back='All workshops', backhref='workshops/',
   err=dict(name='Please enter your full name.', email='Please enter a valid email address.', phone='Please enter your phone number.',
            holder='Please enter the name on the card.', cardno='This card number doesn’t look right.', exp='Enter the expiry date as MM/YY.',
            expired='This card has expired.', cvv='CVV must be 3 or 4 digits.', consent='Please accept the agreements to continue.',
            not_configured='Online payment isn’t active right now. Message us on WhatsApp to register.',
            gateway='The payment system isn’t responding. Please try again shortly or message us on WhatsApp.',
            network='We couldn’t connect. Check your internet connection and try again.', program='Online payment is not open for this programme.'),
   regmsg='',
   hello='Hi {n}, your application has been approved. You can now complete your registration by paying below.', bank_h='Pay by bank transfer', bank_name='Account holder', bank_bank='Bank', bank_ref='Payment reference', amount='Amount', copy='Copy', copied='Copied',
   bank_note='Please use the reference above, including your application number, for your transfer. Once the payment reaches our account, we will confirm your place and let you know.', qr='Turkish bank customers can also scan this code in their mobile banking app.', qr_alt='Akbank payment QR code',
   bank_done='I have made the payment', bank_reported='We have received your payment notice. Once it reaches our account, we will confirm your place and let you know.',
   bank_paid='Your payment is confirmed and you are registered. See you soon!', card_h='or pay by card', badlink='This payment link is invalid, or your application has not been approved yet.',
   noiban='Bank details will appear here shortly. In the meantime, message us on WhatsApp.', bconsent='Please accept the agreement to continue.'),
}

CSS = '''
.pay-wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:48px;align-items:start;margin-top:34px}
.pay-sum{position:sticky;top:96px;background:#F6F4EA;border-radius:22px;padding:28px}
.pay-sum .lbl{font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#6b6b6b;margin:0 0 6px}
.pay-sum h2{font-size:clamp(22px,2.2vw,28px);margin:0 0 6px;line-height:1.15}
.pay-sum .dt{font-weight:700;color:#444;margin:0}
.pay-sum .tot{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid rgba(0,0,0,.15);margin-top:22px;padding-top:16px}
.pay-sum .tot b{font-size:30px;font-weight:900}
.pay-sum .sec{display:flex;gap:10px;font-size:13px;color:#555;margin:20px 0 0;line-height:1.5}
.pay-sum .sec svg{flex:0 0 18px;margin-top:2px}
.pay-form fieldset{border:0;margin:0 0 26px;padding:0}
.pay-form legend{font-size:20px;font-weight:900;margin-bottom:14px;padding:0}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.fgrid .full{grid-column:1/-1}
.fld label{display:block;font-size:14px;font-weight:800;margin-bottom:6px}
.fld input,.fld select{width:100%;box-sizing:border-box;min-height:50px;border:1.5px solid #bdbdbd;border-radius:12px;padding:0 14px;font:600 16px Urbanist,system-ui,sans-serif;background:#fff;color:#000}
.fld input:focus,.fld select:focus{outline:none;border-color:#000;box-shadow:0 0 0 3px rgba(228,69,47,.25)}
.fld input[aria-invalid=true]{border-color:var(--red)}
.fld .msg{color:var(--red);font-size:13px;font-weight:700;margin-top:5px;min-height:0}
.cardno{letter-spacing:.06em}
.consent{display:flex;gap:12px;align-items:flex-start;font-size:14px;line-height:1.55;margin:4px 0 22px}
.consent input{width:22px;height:22px;flex:0 0 22px;margin-top:1px;accent-color:#000}
.consent a{color:inherit;font-weight:800}
.paybtn{width:100%;justify-content:center;min-height:56px;font-size:18px;background:#000;color:#fff;border-color:#000;cursor:pointer}
.paybtn[disabled]{opacity:.6;cursor:progress}
.refund{font-size:14px;font-weight:700;margin:12px 0 0;color:#333}
.refund.no{color:#9b2a18}
.minor{font-size:13px;color:#555;margin:-8px 0 20px;line-height:1.5}
.consent small{color:#666}
.bank{margin-bottom:34px}
.hello{font-size:18px;font-weight:700;margin:0 0 18px;line-height:1.5}
.bh{font-size:22px;margin:0 0 14px}
.ibanbox{margin:0 0 14px;background:#F6F4EA;border-radius:16px;padding:6px 18px}
.ibanbox div{display:grid;grid-template-columns:130px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid rgba(0,0,0,.1);align-items:center}
.ibanbox div:last-child{border-bottom:0}
.ibanbox dt{font-size:13px;font-weight:800;color:#555}.ibanbox dd{margin:0;font-weight:700;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:.02em;overflow-wrap:anywhere}
.copy{border:1.5px solid #000;background:#fff;border-radius:999px;padding:4px 12px;font:800 12px Urbanist,system-ui,sans-serif;cursor:pointer}
.bnote{font-size:14px;color:#444;margin:0 0 18px;line-height:1.55}
.qr{display:flex;gap:16px;align-items:center;margin:0 0 16px}.qr img{width:120px;height:120px;border-radius:10px;border:1px solid rgba(0,0,0,.1);background:#fff}.qr p{margin:0;font-size:14px;color:#444;line-height:1.5}
.bstate{background:#e7f4ea;color:#16632b;border-radius:14px;padding:14px 16px;font-weight:700;margin-top:14px}
.bstate[hidden],#card-h[hidden],.bank[hidden],.pay-sum .sec[hidden],.qr[hidden],.ibanbox[hidden]{display:none}
@media(max-width:480px){.ibanbox div{grid-template-columns:1fr;gap:4px}}
.pay-alert{background:#fde9e6;border:1.5px solid var(--red);color:#7a1d10;border-radius:14px;padding:14px 16px;font-weight:700;margin:0 0 18px}
.pay-alert[hidden]{display:none}
.pay-empty{max-width:640px;margin-top:30px}
.pay-empty .btn{margin:18px 10px 0 0}
.res{max-width:680px;margin:20px 0 10px}
.res .ic{width:64px;height:64px;border-radius:50%;display:grid;place-items:center;margin-bottom:18px}
.res .ok{background:#e7f4ea;color:#16632b}.res .no{background:#fde9e6;color:var(--red)}
.res .ord{font-weight:800;background:#F6F4EA;border-radius:12px;padding:12px 16px;display:inline-block;margin:6px 0 16px}
.res .btn{margin:10px 10px 0 0}
@media(max-width:900px){.pay-wrap{grid-template-columns:1fr;gap:28px}.pay-sum{position:static}}
@media(max-width:480px){.fgrid{grid-template-columns:1fr 1fr}.fgrid .half-m{grid-column:1/-1}.pay-sum{padding:20px}}
'''

LOCK = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'

def pay_page(lang):
    x = T[lang]
    prefix = '../' if lang == 'tr' else '../'          # odeme/ ve en/payment/ ikisi de kendi dil kökünden bir seviye aşağıda
    root = '../' if lang == 'tr' else '../../'          # yasal sayfalar TR kökünde
    lang_href = '../en/payment/' if lang == 'tr' else '../../odeme/'
    cat = [dict(id=p['id'], t=p['title'][lang], d=p['date'][lang], price=p['price'], cur=p['currency'], max=p.get('maxInstallment', 1), type=p.get('type', 'atolye'), start=p.get('start')) for p in CAT]
    body = f'''<section class="band" aria-labelledby="h-pay">
  <div class="wrap">
    <p class="kick2">{x["kick"]}</p>
    <h1 id="h-pay">{x["h1"]}</h1>
    <div id="pay-empty" class="pay-empty" hidden>
      <p class="lede" id="empty-msg">{x["notfound"]} {x["notfound2"]}</p>
      <a class="btn solid" id="wa-link" href="https://wa.me/905304808292" target="_blank" rel="noopener">{x["wa"]}</a>
      <a class="btn ghost" href="{prefix}{x["backhref"]}">{x["back"]}</a>
    </div>
    <div class="pay-wrap" id="pay-wrap" hidden>
      <aside class="pay-sum" aria-label="{x["summary"]}">
        <p class="lbl">{x["summary"]}</p>
        <h2 id="s-title"></h2>
        <p class="dt" id="s-date"></p>
        <div class="fld" id="inst-wrap" style="margin-top:18px" hidden>
          <label for="inst">{x["inst"]}</label>
          <select id="inst"></select>
        </div>
        <div class="tot"><span>{x["total"]}</span><b id="s-total"></b></div>
        <p class="refund" id="s-refund"></p>
        <p class="sec">{LOCK}<span>{x["secure"]}</span></p>
      </aside>
      <div class="paycol">
      <div id="bank" class="bank" hidden>
        <p class="hello" id="b-hello"></p>
        <h2 class="bh">{x["bank_h"]}</h2>
        <dl class="ibanbox">
          <div><dt>{x["bank_name"]}</dt><dd id="b-name"></dd></div>
          <div id="b-bank-row"><dt>{x["bank_bank"]}</dt><dd id="b-bank"></dd></div>
          <div><dt>IBAN</dt><dd><span id="b-iban" class="mono"></span><button type="button" class="copy" data-copy="b-iban">{x["copy"]}</button></dd></div>
          <div><dt>{x["bank_ref"]}</dt><dd><span id="b-ref" class="mono"></span><button type="button" class="copy" data-copy="b-ref">{x["copy"]}</button></dd></div>
          <div><dt>{x["amount"]}</dt><dd id="b-amt"></dd></div>
        </dl>
        <div class="qr"><img src="{root}img/akbank-qr.png" alt="{x["qr_alt"]}" width="180" height="180" loading="lazy"><p>{x["qr"]}</p></div>
        <p class="bnote">{x["bank_note"]}</p>
        <label class="consent"><input type="checkbox" id="b-consent"><span id="b-consent-t"></span></label>
        <div class="msg" id="m-bconsent" style="color:var(--red);font-weight:700;font-size:13px;margin:-12px 0 14px"></div>
        <button class="btn paybtn" id="b-done" type="button">{x["bank_done"]}</button>
        <p class="bstate" id="b-state" role="status" hidden></p>
      </div>
      <h2 class="bh" id="card-h" hidden>{x["card_h"]}</h2>
      <form class="pay-form" id="pay-form" novalidate>
        <p class="pay-alert" id="alert" role="alert" hidden></p>
        <fieldset id="you-fs">
          <legend>{x["you"]}</legend>
          <div class="fgrid">
            <div class="fld full"><label for="f-name">{x["name"]}</label><input id="f-name" autocomplete="name" required><div class="msg" id="m-name"></div></div>
            <div class="fld half-m"><label for="f-email">{x["email"]}</label><input id="f-email" type="email" autocomplete="email" inputmode="email" required><div class="msg" id="m-email"></div></div>
            <div class="fld half-m"><label for="f-phone">{x["phone"]}</label><input id="f-phone" type="tel" autocomplete="tel" inputmode="tel" required><div class="msg" id="m-phone"></div></div>
          </div>
        </fieldset>
        <fieldset>
          <legend>{x["card"]}</legend>
          <div class="fgrid">
            <div class="fld full"><label for="c-holder">{x["holder"]}</label><input id="c-holder" autocomplete="cc-name" required><div class="msg" id="m-holder"></div></div>
            <div class="fld full"><label for="c-no">{x["cardno"]}</label><input id="c-no" class="cardno" autocomplete="cc-number" inputmode="numeric" maxlength="23" placeholder="0000 0000 0000 0000" required><div class="msg" id="m-cardno"></div></div>
            <div class="fld"><label for="c-exp">{x["exp"]}</label><input id="c-exp" autocomplete="cc-exp" inputmode="numeric" maxlength="5" placeholder="AA/YY" required><div class="msg" id="m-exp"></div></div>
            <div class="fld"><label for="c-cvv">{x["cvv"]}</label><input id="c-cvv" autocomplete="cc-csc" inputmode="numeric" maxlength="4" placeholder="000" required><div class="msg" id="m-cvv"></div></div>
          </div>
        </fieldset>
        <label class="consent"><input type="checkbox" id="f-consent"><span id="consent-t"></span></label>
        <div class="msg" id="m-consent" style="color:var(--red);font-weight:700;font-size:13px;margin:-12px 0 14px"></div>
        <label class="consent"><input type="checkbox" id="f-mkt"><span>{x["mkt"]}</span></label>
        <p class="minor">{x["minor"]}</p>
        <button class="btn paybtn" id="paybtn" type="submit"></button>
      </form>
      </div>
    </div>
  </div>
</section>'''
    if lang == 'en': body = body.replace('placeholder="AA/YY"', 'placeholder="MM/YY"')
    js = '''<script>
{
  const CAT = %s, T = %s, LANG = '%s';
  const $ = id => document.getElementById(id);
  const fmt = (n, cur) => new Intl.NumberFormat(LANG === 'tr' ? 'tr-TR' : 'en-GB', {style:'currency', currency:cur, maximumFractionDigits:2}).format(n);
  const Q = new URLSearchParams(location.search), BT = Q.get('b');
  let p = CAT.find(c => c.id === Q.get('p') && typeof c.price === 'number' && c.price > 0);
  const anyP = CAT.find(c => c.id === Q.get('p'));
  const legal = (el, prog) => { const CT = prog && prog.type === 'kamp' ? 'kamp' : 'atolye'; el.innerHTML = T.consent.replace('{c}', CT + '-sozlesmesi').replace('{cn}', T.cn[CT]); };
  const refundLine = prog => {
    if (!prog || !prog.start) return;
    const DAYS = prog.type === 'kamp' ? 60 : 45, st = new Date(prog.start + 'T00:00:00+03:00'), last = new Date(st.getTime() - DAYS * 864e5);
    const ok = Date.now() <= last.getTime() + 864e5 - 1;
    const ds = last.toLocaleDateString(LANG === 'tr' ? 'tr-TR' : 'en-GB', {day:'numeric', month:'long', year:'numeric', timeZone:'Europe/Istanbul'});
    $('s-refund').textContent = ok ? T.refund_ok.replace('{d}', ds) : T.refund_no.replace('{n}', DAYS);
    $('s-refund').classList.toggle('no', !ok);
  };
  let APP = null;
  if (BT) {
    (async () => {
      let d = null;
      try { const r = await fetch('/api/application?b=' + encodeURIComponent(BT)); if (r.ok) d = await r.json(); } catch {}
      if (!d) { $('pay-empty').hidden = false; $('empty-msg').textContent = T.badlink; return; }
      APP = d;
      const prog = CAT.find(c => c.id === d.programId) || {};
      $('pay-wrap').hidden = false;
      $('s-title').textContent = (d.title && d.title[LANG]) || prog.t || '';
      $('s-date').textContent = (d.date && d.date[LANG]) || prog.d || '';
      const amt = (d.priceText && d.priceText[LANG]) || (typeof prog.price === 'number' ? fmt(prog.price, prog.cur) : '');
      $('s-total').textContent = amt; refundLine(prog);
      $('b-hello').textContent = T.hello.replace('{n}', d.name.split(' ')[0]);
      $('bank').hidden = false; legal($('b-consent-t'), prog);
      if (d.iban) {
        $('b-name').textContent = d.ibanName; $('b-iban').textContent = d.iban.replace(/\\s+/g, '').replace(/(.{4})/g, '$1 ').trim();
        if (d.bank) $('b-bank').textContent = d.bank; else $('b-bank-row').hidden = true;
        $('b-ref').textContent = (d.desc || '') + ' – ' + d.id; $('b-amt').textContent = amt;
      } else { document.querySelector('.ibanbox').hidden = true; $('b-done').hidden = true; document.querySelector('.bank .consent').hidden = true; $('b-state').hidden = false; $('b-state').textContent = T.noiban; }
      const setState = st => {
        if (st === 'payment_reported') { $('b-done').hidden = true; $('b-state').hidden = false; $('b-state').textContent = T.bank_reported; }
        if (st === 'paid') { $('b-done').hidden = true; document.querySelector('.ibanbox').hidden = true; document.querySelector('.bnote').hidden = true; document.querySelector('.qr').hidden = true; document.querySelector('.bank .consent').hidden = true; $('b-state').hidden = false; $('b-state').textContent = T.bank_paid; $('pay-form').hidden = true; $('card-h').hidden = true; }
      };
      setState(d.status);
      document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', async () => {
        try { await navigator.clipboard.writeText($(b.dataset.copy).textContent.replace(/\\s+/g, b.dataset.copy === 'b-iban' ? '' : ' ')); b.textContent = T.copied; setTimeout(() => b.textContent = T.copy, 1600); } catch {}
      }));
      $('b-consent').addEventListener('change', () => { $('m-bconsent').textContent = ''; });
      $('b-done').addEventListener('click', async () => {
        if (!$('b-consent').checked) { $('m-bconsent').textContent = T.bconsent; $('b-consent').focus(); return; }
        $('b-done').disabled = true;
        try { const r = await fetch('/api/application', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({b: BT})}); const j = await r.json(); setState(j.status || 'payment_reported'); }
        catch { $('b-done').disabled = false; }
      });
      if (d.card && d.status === 'approved' && typeof prog.price === 'number') { p = prog; $('card-h').hidden = false; $('you-fs').hidden = true; CARD(); }
      else { $('pay-form').hidden = true; document.querySelector('.pay-sum .sec').hidden = true; }
    })();
  } else if (!p) {
    $('pay-empty').hidden = false;
    if (anyP) $('wa-link').href = 'https://wa.me/905304808292?text=' + encodeURIComponent(LANG === 'tr' ? anyP.t + T.regmsg : "I'd like to register for " + anyP.t);
  } else {
    $('pay-wrap').hidden = false;
    $('s-title').textContent = p.t; $('s-date').textContent = p.d; $('s-total').textContent = fmt(p.price, p.cur);
    refundLine(p);
    CARD();
  }
  function CARD() {
    legal($('consent-t'), p);
    $('paybtn').textContent = LANG === 'tr' ? fmt(p.price, p.cur) + ' ' + T.pay : T.pay + ' ' + fmt(p.price, p.cur);
    if (p.max > 1) {
      $('inst-wrap').hidden = false;
      $('inst').innerHTML = Array.from({length: p.max}, (_, i) => i + 1).map(n => `<option value="${n}">${n === 1 ? T.single : n + ' ' + T.x}</option>`).join('');
    }
    const digits = s => s.replace(/\\D/g, '');
    $('c-no').addEventListener('input', e => { e.target.value = digits(e.target.value).slice(0, 19).replace(/(.{4})/g, '$1 ').trim(); });
    $('c-exp').addEventListener('input', e => { let d = digits(e.target.value).slice(0, 4); if (d.length > 2) d = d.slice(0, 2) + '/' + d.slice(2); e.target.value = d; });
    $('c-cvv').addEventListener('input', e => { e.target.value = digits(e.target.value).slice(0, 4); });
    const luhn = n => { let s = 0, alt = false; for (let i = n.length - 1; i >= 0; i--) { let d = +n[i]; if (alt) { d *= 2; if (d > 9) d -= 9; } s += d; alt = !alt; } return s %% 10 === 0; };
    const fields = {name:'f-name', email:'f-email', phone:'f-phone', holder:'c-holder', cardno:'c-no', exp:'c-exp', cvv:'c-cvv'};
    const setErr = (k, msg) => { const el = $(fields[k] || 'f-consent'); if (el) el.setAttribute('aria-invalid', !!msg); $('m-' + k).textContent = msg || ''; };
    Object.entries(fields).forEach(([k, id]) => $(id).addEventListener('input', () => setErr(k, '')));
    $('f-consent').addEventListener('change', () => setErr('consent', ''));
    const showAlert = msg => { const a = $('alert'); a.textContent = msg; a.hidden = !msg; if (msg) a.scrollIntoView({block:'center', behavior:'smooth'}); };
    const form = $('pay-form'), btn = $('paybtn'), label = btn.textContent;
    form.addEventListener('submit', async e => {
      e.preventDefault(); showAlert('');
      const v = {name:$('f-name').value.trim(), email:$('f-email').value.trim(), phone:$('f-phone').value.trim(), holder:$('c-holder').value.trim(),
        cardno:digits($('c-no').value), exp:$('c-exp').value.trim(), cvv:$('c-cvv').value.trim()};
      const errs = {};
      if (!APP) {
      if (v.name.length < 3) errs.name = T.err.name;
      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(v.email)) errs.email = T.err.email;
      if (digits(v.phone).length < 7) errs.phone = T.err.phone;
      }
      if (v.holder.length < 3) errs.holder = T.err.holder;
      if (v.cardno.length < 13 || v.cardno.length > 19 || !luhn(v.cardno)) errs.cardno = T.err.cardno;
      const m = /^(\\d{2})\\/(\\d{2})$/.exec(v.exp);
      if (!m || +m[1] < 1 || +m[1] > 12) errs.exp = T.err.exp;
      else { const now = new Date(), y = 2000 + +m[2]; if (y < now.getFullYear() || (y === now.getFullYear() && +m[1] < now.getMonth() + 1)) errs.exp = T.err.expired; }
      if (!/^\\d{3,4}$/.test(v.cvv)) errs.cvv = T.err.cvv;
      if (!$('f-consent').checked) errs.consent = T.err.consent;
      ['name','email','phone','holder','cardno','exp','cvv','consent'].forEach(k => setErr(k, errs[k]));
      const first = Object.keys(errs)[0];
      if (first) { ($(fields[first]) || $('f-consent')).focus(); return; }
      btn.disabled = true; btn.textContent = T.paying;
      try {
        // Kart bilgileri bu isteğe EKLENMEZ; yalnızca kişi ve program bilgisi gider.
        const r = await fetch('/api/pay-start', {method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({b: BT || undefined, program:p.id, name:v.name, email:v.email, phone:v.phone, lang:LANG, consent:true, marketing:$('f-mkt').checked, installment:+($('inst').value || 1)})});
        const d = await r.json().catch(() => ({error: r.status === 404 ? 'not_configured' : 'gateway'}));
        if (!r.ok || !d.sessionId) throw new Error(d.error || 'gateway');
        // Kart bilgileri doğrudan Tosla'ya gönderilir.
        const f = document.createElement('form'); f.method = 'POST'; f.action = d.gateway; f.style.display = 'none';
        const add = (n, val) => { const i = document.createElement('input'); i.type = 'hidden'; i.name = n; i.value = val; f.appendChild(i); };
        add('ThreeDSessionId', d.sessionId); add('CardHolderName', v.holder); add('CardNo', v.cardno); add('ExpireDate', v.exp); add('Cvv', v.cvv);
        document.body.appendChild(f); f.submit();
      } catch (err) {
        const k = err && err.message in T.err ? err.message : (err instanceof TypeError ? 'network' : 'gateway');
        showAlert(T.err[k]); btn.disabled = false; btn.textContent = label;
      }
    });
    addEventListener('pageshow', ev => { if (ev.persisted) { btn.disabled = false; btn.textContent = label; } });
  }
}
</script>''' % (json.dumps(cat, ensure_ascii=False), json.dumps(dict(hello=x['hello'], copy=x['copy'], copied=x['copied'], bank_reported=x['bank_reported'], bank_paid=x['bank_paid'], badlink=x['badlink'], noiban=x['noiban'], bconsent=x['bconsent'], err=x['err'], pay=x['pay'], paying=x['paying'], single=x['single'], x=x['x'], regmsg=x['regmsg'], consent=x['consent'].format(p=root, c='{c}', cn='{cn}'), cn=x['cn'], refund_ok=x['refund_ok'], refund_no=x['refund_no']), ensure_ascii=False), lang)
    return shell(lang, prefix, lang_href, x['title'], CSS, body, js, noindex=True)


A = {
 'tr': dict(title='Başvuru — NO Tiyatro', kick='International Stage Lab.', h1='Başvuru formu',
   lede='Başvurunu inceleyip en kısa sürede sana dönüş yapacağız. Başvurun onaylanınca ödeme linkin e-posta ve WhatsApp ile gelecek.',
   prog='Başvurmak istediğin programlar', prog_hint='Birden fazla program seçebilirsin; her biri ayrı değerlendirilir.', name='Ad soyad', birth='Doğum tarihi', email='E-posta', phone='Telefon (WhatsApp)', ig='Instagram kullanıcı adı', opt='isteğe bağlı', city='Yaşadığın şehir',
   eng='İngilizce seviyen', student='Aktif öğrenci misin?', yes='Evet', no='Hayır', school='Okuduğun ya da mezun olduğun okul / bölüm', last='Son katıldığın eğitim ya da atölye', why='Bu programa neden katılmak istiyorsun?',
   kvkk='Kişisel verilerimin <a href="{r}yasal/kvkk/" target="_blank">KVKK Aydınlatma Metni</a> kapsamında başvurumun değerlendirilmesi için işlenmesini kabul ediyorum.',
   mkt='<b>İsteğe bağlı:</b> Gelecekteki atölye ve kamplar hakkında bilgilendirme almak istiyorum.', send='Başvuruyu gönder', sending='Gönderiliyor…',
   ok_h='Başvurun bize ulaştı.', ok_p='Teşekkürler {n}! Başvurunu inceleyip en kısa sürede e-posta ve WhatsApp üzerinden dönüş yapacağız.', dup_s='daha önce başvurmuşsun',
   dup_p='Bu programa daha önce başvurmuşsun (başvuru no: {id}). Sonuç e-posta ve WhatsApp ile gelecek.',
   fallback='Başvuru sistemine şu an ulaşılamıyor. Başvurunu bu formdan da yapabilirsin:', fallback_btn='Başvuru formunu aç', home='Ana sayfa',
   levels=['A1 (Başlangıç)','A2 (Temel)','B1 (Orta)','B2 (Orta üstü)','C1 (İleri)','C2 (Anadile yakın)'],
   err=dict(program='En az bir program seç.', name='Adını ve soyadını yaz.', birth='Doğum tarihini seç.', email='Geçerli bir e-posta adresi yaz.', phone='Telefon numaranı yaz.', city='Şehrini yaz.', english='İngilizce seviyeni seç.', student='Bir seçenek işaretle.', school='Okulunu ya da bölümünü yaz.', why='Birkaç cümleyle neden katılmak istediğini anlat.', kvkk='Devam etmek için KVKK onayı gerekiyor.', gateway='Bir sorun oluştu. Lütfen tekrar dene.')),
 'en': dict(title='Application — NO Tiyatro', kick='International Stage Lab.', h1='Application form',
   lede='We will review your application and get back to you as soon as possible. Once approved, your payment link will arrive by email and WhatsApp.',
   prog='Programmes you are applying for', prog_hint='You can choose more than one; each is reviewed separately.', name='Full name', birth='Date of birth', email='Email', phone='Phone (WhatsApp)', ig='Instagram username', opt='optional', city='City you live in',
   eng='Your English level', student='Are you currently a student?', yes='Yes', no='No', school='School / department you attend or graduated from', last='Most recent training or workshop you attended', why='Why do you want to join this programme?',
   kvkk='I agree to my personal data being processed to assess my application, as described in the <a href="{r}yasal/kvkk/" target="_blank">Privacy Notice (KVKK)</a> <small>(in Turkish)</small>.',
   mkt='<b>Optional:</b> I would like to receive information about future workshops and camps.', send='Submit application', sending='Sending…',
   ok_h='We have received your application.', ok_p='Thank you, {n}! We will review your application and get back to you by email and WhatsApp soon.', dup_s='already applied',
   dup_p='You have already applied for this programme (application no: {id}). We will let you know the outcome by email and WhatsApp.',
   fallback='The application system cannot be reached right now. You can also apply using this form:', fallback_btn='Open the application form', home='Home',
   levels=['A1 (Beginner)','A2 (Elementary)','B1 (Intermediate)','B2 (Upper intermediate)','C1 (Advanced)','C2 (Near native)'],
   err=dict(program='Please choose at least one programme.', name='Please enter your full name.', birth='Please select your date of birth.', email='Please enter a valid email address.', phone='Please enter your phone number.', city='Please enter your city.', english='Please select your English level.', student='Please choose an option.', school='Please enter your school or department.', why='Tell us in a few sentences why you want to join.', kvkk='Please accept the privacy notice to continue.', gateway='Something went wrong. Please try again.')),
}
GFORM = 'https://docs.google.com/forms/d/14PzXPCxvlBrst-hDBj_JiiL5kZgiGx2zQC-7AHUgRWA/viewform'

def apply_page(lang):
    x = A[lang]; root = '../' if lang == 'tr' else '../../'
    lang_href = '../en/apply/' if lang == 'tr' else '../../basvuru/'
    progs = [p for p in CAT if p.get('open', True)]
    opts = ''.join(f'<label class="pchk"><input type="checkbox" name="prog" value="{p["id"]}"><span><b>{p["title"][lang]}</b><small>{p["date"][lang]}</small></span></label>' for p in progs)
    lv = ''.join(f'<option value="{l[:2]}">{l}</option>' for l in x['levels'])
    body = f"""<section class="band" aria-labelledby="h-ap">
  <div class="wrap">
    <p class="kick2">{x['kick']}</p>
    <h1 id="h-ap">{x['h1']}</h1>
    <p class="lede" style="margin:16px 0 30px">{x['lede']}</p>
    <div class="res" id="done" hidden></div>
    <form class="pay-form apform" id="apform" novalidate>
      <p class="pay-alert" id="alert" role="alert" hidden></p>
      <div class="fgrid">
        <div class="fld full"><span class="lbl2" id="l-prog">{x['prog']}</span><p class="hint">{x['prog_hint']}</p><div class="plist2" id="a-program" role="group" aria-labelledby="l-prog" tabindex="-1">{opts}</div><div class="msg" id="m-program"></div></div>
        <div class="fld full"><label for="a-name">{x['name']}</label><input id="a-name" autocomplete="name"><div class="msg" id="m-name"></div></div>
        <div class="fld half-m"><label for="a-birth">{x['birth']}</label><input id="a-birth" type="date" min="1940-01-01" max="2015-12-31"><div class="msg" id="m-birth"></div></div>
        <div class="fld half-m"><label for="a-city">{x['city']}</label><input id="a-city" autocomplete="address-level2"><div class="msg" id="m-city"></div></div>
        <div class="fld half-m"><label for="a-email">{x['email']}</label><input id="a-email" type="email" autocomplete="email" inputmode="email"><div class="msg" id="m-email"></div></div>
        <div class="fld half-m"><label for="a-phone">{x['phone']}</label><input id="a-phone" type="tel" autocomplete="tel" inputmode="tel"><div class="msg" id="m-phone"></div></div>
        <div class="fld half-m"><label for="a-ig">{x['ig']} <small>({x['opt']})</small></label><input id="a-ig" autocomplete="off" placeholder="@"></div>
        <div class="fld half-m"><label for="a-english">{x['eng']}</label><select id="a-english"><option value=""></option>{lv}</select><div class="msg" id="m-english"></div></div>
        <div class="fld full"><span class="lbl2" id="l-student">{x['student']}</span><div class="radios" role="radiogroup" aria-labelledby="l-student"><label><input type="radio" name="student" value="yes"> {x['yes']}</label><label><input type="radio" name="student" value="no"> {x['no']}</label></div><div class="msg" id="m-student"></div></div>
        <div class="fld full"><label for="a-school">{x['school']}</label><input id="a-school"><div class="msg" id="m-school"></div></div>
        <div class="fld full"><label for="a-last">{x['last']} <small>({x['opt']})</small></label><input id="a-last"></div>
        <div class="fld full"><label for="a-why">{x['why']}</label><textarea id="a-why" rows="5"></textarea><div class="msg" id="m-why"></div></div>
        <input type="text" id="a-website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      </div>
      <label class="consent" style="margin-top:18px"><input type="checkbox" id="a-kvkk"><span>{x['kvkk'].format(r=root)}</span></label>
      <div class="msg" id="m-kvkk" style="color:var(--red);font-weight:700;font-size:13px;margin:-12px 0 14px"></div>
      <label class="consent"><input type="checkbox" id="a-mkt"><span>{x['mkt']}</span></label>
      <button class="btn paybtn" id="a-send" type="submit">{x['send']}</button>
    </form>
  </div>
</section>"""
    js = """<script>
{
  const X = %s, LANG = '%s', GFORM = '%s';
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const pre = new URLSearchParams(location.search).get('p');
  document.querySelectorAll('input[name=prog]').forEach(c => { if (c.value === pre) c.checked = true; });
  const picked = () => [...document.querySelectorAll('input[name=prog]:checked')].map(c => c.value);
  const F = {program:'a-program', name:'a-name', birth:'a-birth', city:'a-city', email:'a-email', phone:'a-phone', english:'a-english', school:'a-school', why:'a-why', kvkk:'a-kvkk'};
  const setErr = (k, m) => { const el = $(F[k]); if (el) el.setAttribute('aria-invalid', !!m); $('m-' + k).textContent = m || ''; };
  Object.entries(F).filter(([k]) => k !== 'program').forEach(([k, id]) => $(id).addEventListener(id === 'a-kvkk' ? 'change' : 'input', () => setErr(k, '')));
  document.querySelectorAll('input[name=prog]').forEach(c => c.addEventListener('change', () => setErr('program', '')));
  document.querySelectorAll('input[name=student]').forEach(r => r.addEventListener('change', () => setErr('student', '')));
  const alertBox = m => { $('alert').innerHTML = m; $('alert').hidden = !m; if (m) $('alert').scrollIntoView({block:'center', behavior:'smooth'}); };
  $('apform').addEventListener('submit', async e => {
    e.preventDefault(); alertBox('');
    const st = document.querySelector('input[name=student]:checked');
    const v = {programs:picked(), name:$('a-name').value.trim(), birth:$('a-birth').value, city:$('a-city').value.trim(), email:$('a-email').value.trim(), phone:$('a-phone').value.trim(),
      instagram:$('a-ig').value.trim(), english:$('a-english').value, student: st ? st.value : '', school:$('a-school').value.trim(), last:$('a-last').value.trim(), why:$('a-why').value.trim()};
    const er = {};
    if (!v.programs.length) er.program = X.err.program;
    if (v.name.length < 3) er.name = X.err.name;
    if (!/^\\d{4}-\\d{2}-\\d{2}$/.test(v.birth)) er.birth = X.err.birth;
    if (v.city.length < 2) er.city = X.err.city;
    if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(v.email)) er.email = X.err.email;
    if (v.phone.replace(/\\D/g, '').length < 7) er.phone = X.err.phone;
    if (!v.english) er.english = X.err.english;
    if (!v.student) er.student = X.err.student;
    if (v.school.length < 2) er.school = X.err.school;
    if (v.why.length < 10) er.why = X.err.why;
    if (!$('a-kvkk').checked) er.kvkk = X.err.kvkk;
    ['program','name','birth','city','email','phone','english','student','school','why','kvkk'].forEach(k => setErr(k, er[k]));
    const first = Object.keys(er)[0];
    if (first) { (first === 'student' ? document.querySelector('input[name=student]') : first === 'program' ? document.querySelector('input[name=prog]') : $(F[first])).focus(); return; }
    const btn = $('a-send'), label = btn.textContent; btn.disabled = true; btn.textContent = X.sending;
    try {
      const r = await fetch('/api/apply', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({...v, lang:LANG, kvkk:true, marketing:$('a-mkt').checked, website:$('a-website').value})});
      if (r.status === 404 || r.status >= 500) throw new TypeError('down');
      const d = await r.json();
      if (!r.ok) { const k = d.error in X.err ? d.error : 'gateway'; if (k in F || k === 'student') { setErr(k, X.err[k]); } else alertBox(esc(X.err[k])); btn.disabled = false; btn.textContent = label; return; }
      $('apform').hidden = true; document.querySelector('.lede').hidden = true;
      $('done').hidden = false;
      $('done').innerHTML = `<div class="ic ok"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 12l5 5 9-10"/></svg></div><h2>${esc(X.ok_h)}</h2><p class="lede" style="margin:14px 0 18px">${esc(X.ok_p.replace('{n}', v.name.split(' ')[0]))}</p><ul class="aplist">${(d.applications || []).map(a => `<li><b>${esc(a.program)}</b> · ${esc(a.id)}${a.duplicate ? ' <small>(' + esc(X.dup_s) + ')</small>' : ''}</li>`).join('')}</ul><a class="btn solid" href="../">${esc(X.home)}</a>`;
      $('done').scrollIntoView({block:'start', behavior:'smooth'});
    } catch {
      alertBox(esc(X.fallback) + ` <a href="${GFORM}" target="_blank" rel="noopener" style="color:inherit">${esc(X.fallback_btn)}</a>`);
      btn.disabled = false; btn.textContent = label;
    }
  });
}
</script>""" % (json.dumps({k: x[k] for k in ['err','sending','ok_h','ok_p','dup_s','fallback','fallback_btn','home']}, ensure_ascii=False), lang, GFORM)
    css = CSS + '.apform{max-width:820px}.hint{font-size:13px;color:#666;margin:-4px 0 10px}.plist2{display:grid;gap:8px}.pchk{display:flex;gap:12px;align-items:flex-start;border:1.5px solid #ccc;border-radius:12px;padding:12px 14px;cursor:pointer}.pchk:has(input:checked){border-color:#000;background:#F6F4EA}.pchk input{width:20px;height:20px;margin-top:2px;accent-color:#000;flex:0 0 20px}.pchk span{display:grid;gap:2px}.pchk small{color:#666;font-weight:600}.fld .pchk{display:flex;font-size:15px;font-weight:600;margin:0}.fld .pchk input,.fld .radios input{width:20px;height:20px;min-height:0;padding:0;border-radius:4px;flex:0 0 20px}.fld .pchk b{font-weight:800}.aplist{margin:0 0 20px;padding-left:20px;line-height:1.8}.apform textarea{width:100%;box-sizing:border-box;border:1.5px solid #bdbdbd;border-radius:12px;padding:12px 14px;font:600 16px Urbanist,system-ui,sans-serif;resize:vertical}.apform textarea:focus{outline:none;border-color:#000;box-shadow:0 0 0 3px rgba(228,69,47,.25)}.lbl2{display:block;font-size:14px;font-weight:800;margin-bottom:8px}.radios{display:flex;gap:22px}.radios label{display:flex;gap:8px;align-items:center;font-weight:700;cursor:pointer}.radios input{width:20px;height:20px;accent-color:#000}.fld small{font-weight:600;color:#777}.apform .paybtn{margin-top:6px}'
    return shell(lang, '../', lang_href, x['title'], css, body, js)

R = {
 'tr': dict(title='Ödeme sonucu — NO Tiyatro',
   ok_h='Ödemen alındı, kaydın tamam.', ok_p='Teşekkürler! Kayıt bilgilerini ve programın detaylarını e-posta ve WhatsApp üzerinden göndereceğiz. Sorun olursa sipariş numaranla bize yazabilirsin.',
   fail_h='Ödeme tamamlanamadı.', fail_p='Kartından ücret çekilmedi. Kart bilgilerini kontrol edip tekrar deneyebilir ya da WhatsApp\'tan bize yazabilirsin.',
   err_h='Ödemenin sonucunu doğrulayamadık.', err_p='Kartından çekim yapıldıysa merak etme, kontrol edip sana dönüş yapacağız. Sipariş numaranla WhatsApp\'tan yazabilirsin.',
   ord='Sipariş no', home='Ana sayfaya dön', ws='Tüm atölyeler', wsh='atolyeler/', retry='Tekrar dene', wa='WhatsApp\'tan yaz'),
 'en': dict(title='Payment result — NO Tiyatro',
   ok_h='Payment received — you’re registered.', ok_p='Thank you! We’ll send your registration details and the programme information by email and WhatsApp. If anything comes up, message us with your order number.',
   fail_h='The payment didn’t go through.', fail_p='Your card was not charged. Check your card details and try again, or message us on WhatsApp.',
   err_h='We couldn’t confirm the payment result.', err_p='If your card was charged, don’t worry — we’ll check and get back to you. Message us on WhatsApp with your order number.',
   ord='Order no', home='Back to home', ws='All workshops', wsh='workshops/', retry='Try again', wa='Message us on WhatsApp'),
}

def result_page(lang):
    x = R[lang]
    prefix = '../../'
    lang_href = '../../en/payment/result/' if lang == 'tr' else '../../../odeme/sonuc/'
    body = f'''<section class="band" aria-live="polite">
  <div class="wrap"><div class="res" id="res"></div></div>
</section>'''
    js = '''<script>
{
  const X = %s, q = new URLSearchParams(location.search), st = q.get('status'), ord = (q.get('order') || '').replace(/[^A-Za-z0-9-]/g, ''), prog = (q.get('p') || '').replace(/[^a-z0-9-]/g, '');
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const k = st === 'ok' ? 'ok' : st === 'fail' ? 'fail' : 'err';
  const icon = k === 'ok' ? '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 12l5 5 9-10"/></svg>'
                          : '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="3"><path d="M12 7v6M12 17h.01"/></svg>';
  const wa = 'https://wa.me/905304808292?text=' + encodeURIComponent((X.ord + ': ' + (ord || '-')));
  document.getElementById('res').innerHTML = `<div class="ic ${k === 'ok' ? 'ok' : 'no'}">${icon}</div><h1>${esc(X[k + '_h'])}</h1><p class="lede" style="margin:14px 0 18px">${esc(X[k + '_p'])}</p>`
    + (ord ? `<p class="ord">${esc(X.ord)}: ${esc(ord)}</p><br>` : '')
    + (k === 'fail' && prog ? `<a class="btn solid" href="../?p=${encodeURIComponent(prog)}">${esc(X.retry)}</a>` : '')
    + (k === 'ok' ? `<a class="btn solid" href="%s">${esc(X.home)}</a><a class="btn ghost" href="%s${X.wsh}">${esc(X.ws)}</a>`
                  : `<a class="btn ${k === 'fail' ? 'ghost' : 'solid'}" href="${wa}" target="_blank" rel="noopener">${esc(X.wa)}</a>`);
}
</script>''' % (json.dumps(x, ensure_ascii=False), '../../' if lang == 'tr' else '../../', '../../')
    return shell(lang, prefix, lang_href, x['title'], CSS, body, js, noindex=True)

ADMIN_CSS = CSS + '''
.adm-login{max-width:420px;margin-top:24px}
.adm-login .btn{margin-top:14px;cursor:pointer}
.adm-bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:24px 0 16px}
.adm-bar select,.adm-bar input{min-height:42px;border:1.5px solid #bdbdbd;border-radius:10px;padding:0 12px;font:600 14px Urbanist,system-ui,sans-serif}
.adm-bar .btn{cursor:pointer}
.adm-stats{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.adm-stats div{background:#F6F4EA;border-radius:14px;padding:12px 16px;font-size:13px;font-weight:700}
.adm-stats b{display:block;font-size:22px;font-weight:900}
.tblw{overflow-x:auto;border:1px solid rgba(0,0,0,.15);border-radius:14px}
table.adm{border-collapse:collapse;width:100%;min-width:900px;font-size:14px}
table.adm th,table.adm td{text-align:left;padding:11px 12px;border-bottom:1px solid rgba(0,0,0,.1);vertical-align:top}
table.adm th{background:#fafafa;font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.st{display:inline-block;border-radius:999px;padding:2px 10px;font-weight:800;font-size:12px}
.st.paid{background:#e7f4ea;color:#16632b}.st.pending{background:#f1f1f1;color:#555}.st.failed,.st.hash_error{background:#fde9e6;color:#9b2a18}
'''

def admin_page():
    body = """<section class="band">
  <div class="wrap">
    <p class="kick2">Yönetim</p>
    <h1>Başvurular ve ödemeler</h1>
    <form class="adm-login fld" id="login">
      <label for="pw">Yönetim şifresi</label>
      <input id="pw" type="password" autocomplete="current-password" required>
      <p class="pay-alert" id="lerr" hidden></p>
      <button class="btn solid" type="submit">Giriş yap</button>
    </form>
    <div id="panel" hidden>
      <div class="tabs adm-tabs" role="tablist">
        <button class="tab" role="tab" data-v="apps" aria-selected="true">Başvurular <span class="n" id="n-apps"></span></button>
        <button class="tab" role="tab" data-v="orders" aria-selected="false">Kartlı ödemeler <span class="n" id="n-orders"></span></button>
      </div>
      <div id="v-apps">
        <div class="adm-bar">
          <select id="ast" aria-label="Durum"><option value="">Tüm durumlar</option><option value="pending">Yeni başvuru</option><option value="approved">Onaylandı · ödeme bekleniyor</option><option value="payment_reported">Ödeme bildirildi</option><option value="paid">Ödendi</option><option value="rejected">Reddedildi</option></select>
          <select id="apr" aria-label="Program"><option value="">Tüm programlar</option></select>
          <input id="aq" type="search" placeholder="İsim, e-posta, telefon, başvuru no" aria-label="Ara">
          <button class="btn ghost" id="acsv" type="button">CSV indir</button>
          <button class="btn ghost" id="reload" type="button">Yenile</button>
          <button class="btn ghost" id="out" type="button">Çıkış</button>
        </div>
        <div class="adm-stats" id="astats"></div>
        <div id="alist" class="alist"></div>
      </div>
      <div id="v-orders" hidden>
        <div class="adm-stats" id="stats"></div>
        <div class="tblw"><table class="adm"><thead><tr><th>Tarih</th><th>Sipariş no</th><th>Program</th><th>Ad soyad</th><th>E-posta</th><th>Telefon</th><th>Tutar</th><th>Durum</th></tr></thead><tbody id="rows"></tbody></table></div>
        <p style="font-size:13px;color:#666;margin-top:14px">Kartla yapılan ödemelerin banka tarafındaki kesin kaydı Tosla İşim panelindedir. İptal ve iadeyi oradan yaparsın.</p>
      </div>
    </div>
  </div>
</section>"""
    js = r"""<script>
{
  const $ = id => document.getElementById(id);
  const AST = {pending:'Yeni başvuru', approved:'Onaylandı · ödeme bekleniyor', payment_reported:'Ödeme bildirildi', paid:'Ödendi', rejected:'Reddedildi'};
  const OST = {paid:'Ödendi', pending:'Bekliyor', failed:'Başarısız', hash_error:'Doğrulanamadı'};
  const ENG = {A1:'A1', A2:'A2', B1:'B1', B2:'B2', C1:'C1', C2:'C2'};
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const money = (n, c) => new Intl.NumberFormat('tr-TR', {style:'currency', currency:c || 'TRY'}).format(n);
  const dt = s => s ? new Date(s).toLocaleString('tr-TR', {day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit'}) : '';
  const age = b => { if (!b) return ''; const d = new Date(b), n = new Date(); let a = n.getFullYear() - d.getFullYear(); if (n < new Date(n.getFullYear(), d.getMonth(), d.getDate())) a--; return a; };
  const phoneWa = p => { let d = String(p || '').replace(/\D/g, ''); if (d.startsWith('0')) d = '90' + d.slice(1); if (d.length === 10 && d.startsWith('5')) d = '90' + d; return d; };
  let pw = ''; try { pw = sessionStorage.getItem('no_adm') || ''; } catch {}
  let APPS = [], ORDERS = [], MAIL = false;
  const api = (u, o = {}) => fetch(u, {...o, headers:{...(o.headers || {}), Authorization:'Bearer ' + pw, 'Content-Type':'application/json'}});
  async function load() {
    const [ra, ro] = await Promise.all([api('/api/admin/applications').catch(() => null), api('/api/admin/orders').catch(() => null)]);
    if (!ra || !ra.ok) {
      try { sessionStorage.removeItem('no_adm'); } catch {}
      $('panel').hidden = true; $('login').hidden = false;
      if (pw) { $('lerr').textContent = ra && ra.status === 401 ? 'Şifre yanlış.' : 'Sunucuya ulaşılamadı.'; $('lerr').hidden = false; }
      return;
    }
    const a = await ra.json(); APPS = a.applications || []; MAIL = a.mail;
    ORDERS = ro && ro.ok ? ((await ro.json()).orders || []) : [];
    $('login').hidden = true; $('panel').hidden = false;
    const progs = [...new Set(APPS.map(o => o.program))];
    const cur = $('apr').value;
    $('apr').innerHTML = '<option value="">Tüm programlar</option>' + progs.map(p => `<option${p === cur ? ' selected' : ''}>${esc(p)}</option>`).join('');
    renderApps(); renderOrders();
  }
  const filtered = () => { const s = $('ast').value, p = $('apr').value, q = $('aq').value.toLowerCase();
    return APPS.filter(o => (!s || o.status === s) && (!p || o.program === p) && (!q || [o.name, o.email, o.phone, o.id, o.city].join(' ').toLowerCase().includes(q))); };
  function waLink(o) {
    const msg = o.lang === 'en'
      ? `Hi ${o.name.split(' ')[0]}, your application for ${o.program} has been approved! You can complete your registration and see the payment details here: ${o.payLink}`
      : `Merhaba ${o.name.split(' ')[0]}, ${o.program} başvurun onaylandı! Kaydını tamamlamak için ödeme bilgilerine buradan ulaşabilirsin: ${o.payLink}`;
    return 'https://wa.me/' + phoneWa(o.phone) + '?text=' + encodeURIComponent(msg);
  }
  function card(o) {
    const acts = [];
    if (o.status === 'pending') acts.push(`<button class="btn solid" data-act="approve" data-id="${o.id}">Onayla</button>`, `<button class="btn ghost" data-act="reject" data-id="${o.id}">Reddet</button>`);
    if (o.status === 'approved' || o.status === 'payment_reported') acts.push(`<button class="btn solid" data-act="paid" data-id="${o.id}">Ödendi olarak işaretle</button>`);
    if (o.payLink && o.status !== 'paid' && o.status !== 'rejected') acts.push(`<a class="btn ghost" href="${waLink(o)}" target="_blank" rel="noopener">Ödeme linkini WhatsApp'tan gönder</a>`, `<button class="btn ghost" data-copy="${esc(o.payLink)}">Linki kopyala</button>`);
    if (o.status === 'rejected' || o.status === 'approved') acts.push(`<button class="btn ghost" data-act="pending" data-id="${o.id}">Geri al</button>`);
    const info = [['Doğum tarihi', o.birth ? `${o.birth} (${age(o.birth)} yaş)` : ''], ['Şehir', o.city], ['E-posta', `<a href="mailto:${esc(o.email)}">${esc(o.email)}</a>`, true], ['Telefon', `<a href="https://wa.me/${phoneWa(o.phone)}" target="_blank" rel="noopener">${esc(o.phone)}</a>`, true], ['Instagram', o.instagram], ['İngilizce', o.english], ['Öğrenci', o.student === 'yes' ? 'Evet' : o.student === 'no' ? 'Hayır' : ''], ['Okul / bölüm', o.school], ['Son eğitim', o.last], ['Bilgilendirme izni', o.marketing ? 'Evet' : 'Hayır']]
      .filter(r => r[1]).map(r => `<div><dt>${r[0]}</dt><dd>${r[2] ? r[1] : esc(r[1])}</dd></div>`).join('');
    const hist = (o.history || []).map(h => `${dt(h.at)} · ${AST[h.status] || h.status}${h.by === 'card' ? ' (kartla)' : ''}`).join('<br>');
    return `<details class="acard"${o.status === 'pending' ? ' open' : ''}><summary><span class="st ${o.status}">${AST[o.status] || o.status}</span><b>${esc(o.name)}</b><span class="ap">${esc(o.program)}</span><span class="ad">${dt(o.createdAt)} · ${esc(o.id)}</span></summary>
      <div class="abody"><dl class="ainfo">${info}</dl><div class="awhy"><h4>Neden katılmak istiyor?</h4><p>${esc(o.why)}</p>${o.mailedAt ? `<p class="small">Onay e-postası gönderildi: ${dt(o.mailedAt)}</p>` : ''}<p class="small">${hist}</p></div></div>
      <div class="aacts">${acts.join('')}</div></details>`;
  }
  function renderApps() {
    const list = filtered(); const c = s => APPS.filter(o => o.status === s).length;
    $('n-apps').textContent = c('pending') || '';
    $('astats').innerHTML = [['pending','Yeni'],['approved','Ödeme bekleniyor'],['payment_reported','Ödeme bildirildi'],['paid','Ödendi'],['rejected','Reddedildi']].map(([k, l]) => `<div><b>${c(k)}</b>${l}</div>`).join('') + (MAIL ? '' : '<div class="warn">Otomatik e-posta kapalı: onaydan sonra linki WhatsApp\'tan gönder.</div>');
    $('alist').innerHTML = list.map(card).join('') || '<p>Başvuru yok.</p>';
  }
  function renderOrders() {
    const paid = ORDERS.filter(o => o.status === 'paid'); const sums = {}; paid.forEach(o => { sums[o.currency] = (sums[o.currency] || 0) + o.amount; });
    $('n-orders').textContent = ORDERS.length || '';
    $('stats').innerHTML = `<div><b>${paid.length}</b>kartla ödenen</div>` + Object.entries(sums).map(([c, v]) => `<div><b>${money(v, c)}</b>tahsilat</div>`).join('');
    $('rows').innerHTML = ORDERS.map(o => `<tr><td>${esc(dt(o.createdAt))}</td><td>${esc(o.orderId)}${o.env === 'test' ? ' <small>(test)</small>' : ''}</td><td>${esc(o.program)}</td><td>${esc(o.name)}</td><td>${esc(o.email)}</td><td>${esc(o.phone)}</td><td>${esc(money(o.amount, o.currency))}</td><td><span class="st ${esc(o.status)}">${esc(OST[o.status] || o.status)}</span></td></tr>`).join('') || '<tr><td colspan="8">Kartlı ödeme yok.</td></tr>';
  }
  $('alist').addEventListener('click', async e => {
    const cp = e.target.closest('[data-copy]');
    if (cp) { try { await navigator.clipboard.writeText(cp.dataset.copy); cp.textContent = 'Kopyalandı'; setTimeout(() => cp.textContent = 'Linki kopyala', 1500); } catch {} return; }
    const b = e.target.closest('[data-act]'); if (!b) return;
    const act = b.dataset.act;
    if (act === 'reject' && !confirm('Bu başvuruyu reddetmek istediğine emin misin?')) return;
    if (act === 'paid' && !confirm('Ödemenin hesaba geçtiğini kontrol ettin mi? Kayıt "Ödendi" olarak işaretlenecek.')) return;
    b.disabled = true;
    const r = await api('/api/admin/applications', {method:'POST', body: JSON.stringify({id: b.dataset.id, action: act})}).catch(() => null);
    if (!r || !r.ok) { alert('İşlem yapılamadı, tekrar dene.'); b.disabled = false; return; }
    const d = await r.json(); APPS = APPS.map(o => o.id === d.application.id ? d.application : o); renderApps();
    if (act === 'approve') {
      const o = d.application;
      if (d.mailed) alert('Onaylandı. Ödeme linki ' + o.email + ' adresine e-postayla gönderildi. İstersen WhatsApp\'tan da gönderebilirsin.');
      else if (confirm('Onaylandı. Ödeme linkini şimdi WhatsApp\'tan göndermek ister misin?')) window.open(waLink(o), '_blank', 'noopener');
    }
  });
  document.querySelectorAll('.adm-tabs .tab').forEach(t => t.addEventListener('click', () => {
    document.querySelectorAll('.adm-tabs .tab').forEach(x => x.setAttribute('aria-selected', x === t));
    $('v-apps').hidden = t.dataset.v !== 'apps'; $('v-orders').hidden = t.dataset.v !== 'orders';
  }));
  $('login').addEventListener('submit', e => { e.preventDefault(); pw = $('pw').value; try { sessionStorage.setItem('no_adm', pw); } catch {} $('lerr').hidden = true; load(); });
  ['ast', 'apr'].forEach(id => $(id).addEventListener('change', renderApps)); $('aq').addEventListener('input', renderApps);
  $('reload').addEventListener('click', load);
  $('out').addEventListener('click', () => { pw = ''; try { sessionStorage.removeItem('no_adm'); } catch {} APPS = []; ORDERS = []; $('panel').hidden = true; $('login').hidden = false; $('pw').value = ''; });
  $('acsv').addEventListener('click', () => {
    const cols = ['createdAt','id','status','program','name','birth','city','email','phone','instagram','english','student','school','last','why','marketing','approvedAt','paidAt'];
    const csv = [cols.join(';')].concat(filtered().map(o => cols.map(c => '"' + String(o[c] ?? '').replace(/"/g, '""').replace(/\r?\n/g, ' ') + '"').join(';'))).join('\r\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob(['﻿' + csv], {type:'text/csv'})); a.download = 'notiyatro-basvurular.csv'; a.click();
  });
  if (pw) load();
  setInterval(() => { if (!$('panel').hidden && document.visibilityState === 'visible') load(); }, 60000);
}
</script>"""
    css = ADMIN_CSS + """
.adm-tabs{display:flex;gap:6px;border-bottom:2px solid #000;margin:28px 0 0}
.adm-tabs .tab{appearance:none;background:none;border:0;font:800 17px Urbanist,system-ui,sans-serif;padding:12px 16px;cursor:pointer;color:#666;border-bottom:4px solid transparent;margin-bottom:-2px}
.adm-tabs .tab[aria-selected=true]{color:#000;border-bottom-color:var(--red)}
.adm-tabs .n{display:inline-grid;place-items:center;min-width:22px;height:22px;border-radius:999px;background:var(--red);color:#fff;font-size:12px;margin-left:6px;padding:0 6px}
.adm-tabs .n:empty{display:none}
.adm-stats .warn{background:#fff4d6;color:#7a5600;font-weight:700}
.alist{display:grid;gap:12px}
.acard{border:1.5px solid rgba(0,0,0,.15);border-radius:16px;padding:0;background:#fff}
.acard summary{list-style:none;cursor:pointer;display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:16px 18px}
.acard summary::-webkit-details-marker{display:none}
.acard summary b{font-size:17px}.acard .ap{color:#333;font-weight:600}.acard .ad{margin-left:auto;color:#777;font-size:13px}
.abody{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:24px;padding:0 18px 8px}
.ainfo{margin:0;display:grid;gap:8px}.ainfo div{display:grid;grid-template-columns:140px 1fr;gap:10px}.ainfo dt{font-size:13px;font-weight:800;color:#666}.ainfo dd{margin:0;overflow-wrap:anywhere}
.awhy h4{margin:0 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:#666}.awhy p{margin:0 0 10px;line-height:1.55;white-space:pre-line}.awhy .small{font-size:13px;color:#777}
.aacts{display:flex;gap:8px;flex-wrap:wrap;padding:12px 18px 18px;border-top:1px solid rgba(0,0,0,.08)}
.aacts .btn{min-height:40px;font-size:14px;cursor:pointer;white-space:normal}
.st.approved{background:#fff4d6;color:#7a5600}.st.payment_reported{background:#e4efff;color:#1a4fa0}.st.rejected{background:#eee;color:#777}
@media(max-width:760px){.abody{grid-template-columns:1fr}.ainfo div{grid-template-columns:110px 1fr}.acard .ad{margin-left:0;width:100%}}
"""
    return shell('tr', '../', '../en/', 'Yönetim — NO Tiyatro', css, body, js, noindex=True)

from legal_text import PAGES as LEGAL
LEGAL_CSS = '''
.lg{max-width:780px}
.lg h1{margin-bottom:10px}
.lg .lg-meta{color:#555;font-weight:700;margin:0 0 26px}
.lg h2{font-size:20px;margin:30px 0 10px}
.lg p,.lg li{line-height:1.65;font-size:16px}
.lg ul{padding-left:22px}
.lg a{color:inherit;font-weight:700}
.lg-firm{display:grid;gap:8px;margin:0;background:#F6F4EA;border-radius:16px;padding:18px 20px}
.lg-firm div{display:grid;grid-template-columns:170px 1fr;gap:12px}
.lg-firm dt{font-weight:800;font-size:14px}.lg-firm dd{margin:0}
.lg-nav{display:flex;gap:8px;flex-wrap:wrap;margin:34px 0 0}
.lg-nav a{border:1.5px solid #000;border-radius:999px;padding:8px 14px;font-size:14px;text-decoration:none}
.lg-nav a[aria-current=page]{background:#000;color:#fff}
.lg-date{color:#666;font-size:14px;margin-top:30px}
@media(max-width:560px){.lg-firm div{grid-template-columns:1fr;gap:2px}}
'''
def legal_page(slug):
    title, fn = LEGAL[slug]
    nav = ''.join(f'<a href="../{k}/"' + (' aria-current="page"' if k == slug else '') + f'>{v[0]}</a>' for k, v in LEGAL.items())
    body = f'<section class="band"><div class="wrap lg"><p class="kick2">NO Tiyatro · Yasal</p><h1>{title}</h1>{fn()}<p class="lg-date">Son güncelleme: 26 Kasım 2026</p><nav class="lg-nav" aria-label="Yasal metinler">{nav}</nav></div></section>'
    return shell('tr', '../../', '../../en/', f'{title} — NO Tiyatro', LEGAL_CSS, body, '')

out = {
  'odeme/index.html': pay_page('tr'),
  'en/payment/index.html': pay_page('en'),
  'odeme/sonuc/index.html': result_page('tr'),
  'en/payment/result/index.html': result_page('en'),
  'yonetim/index.html': admin_page(),
  'basvuru/index.html': apply_page('tr'),
  'en/apply/index.html': apply_page('en'),
}
for k in LEGAL: out[f'yasal/{k}/index.html'] = legal_page(k)
_items = ''.join(f'<li><a href="{k}/">{v[0]}</a></li>' for k, v in LEGAL.items())
out['yasal/index.html'] = shell('tr', '../', '../en/', 'Sözleşmeler ve yasal metinler — NO Tiyatro', LEGAL_CSS + '.lg-list{list-style:none;padding:0;display:grid;gap:10px;margin:26px 0}.lg-list a{display:block;border:1.5px solid #000;border-radius:16px;padding:18px 20px;font-size:18px;text-decoration:none}.lg-list a:hover{background:#F6F4EA}',
  f'<section class="band"><div class="wrap lg"><p class="kick2">NO Tiyatro · Yasal</p><h1>Sözleşmeler ve yasal metinler</h1><p>notiyatro.com üzerinden yapılan atölye ve kamp kayıtlarında geçerli mesafeli hizmet sözleşmeleri, ön bilgilendirme formu, iptal-iade koşulları ve kişisel verilerin korunmasına ilişkin metinler.</p><ul class="lg-list">{_items}</ul>{__import__("legal_text").SELLER}</div></section>', '')
for path, html in out.items():
    full = f'{ROOT}/{path}'; os.makedirs(os.path.dirname(full), exist_ok=True); open(full, 'w').write(html)
print('pages ok; priced programmes:', PAID or 'none')
