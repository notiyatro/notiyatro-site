# Extra languages (de, ru, fr, es, it, el) are produced from the EN pages by string replacement,
# then a language switcher is placed on every page of the site.
# Translation sources: i18n/tx_*.py. tx_a/b/c hold (de, ru) tuples; tx_<lang>.py hold {EN: text} dicts.
import re, os, sys, json, glob, importlib.util
ROOT = '/home/claude/notiyatro'
I18N = os.path.dirname(os.path.abspath(__file__)) + '/i18n'
NAMES = {'tr': 'Türkçe', 'en': 'English', 'de': 'Deutsch', 'ru': 'Русский', 'fr': 'Français', 'es': 'Español', 'it': 'Italiano', 'el': 'Ελληνικά'}
LOCALE = {'de': 'de-DE', 'ru': 'ru-RU', 'fr': 'fr-FR', 'es': 'es-ES', 'it': 'it-IT', 'el': 'el-GR'}
PAGES = {'': 'index.html', 'workshops/': 'workshops/index.html', 'camps/': 'camps/index.html', 'apply/': 'apply/index.html'}

def load(name):
    p = f'{I18N}/{name}.py'
    if not os.path.exists(p): return {}
    spec = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def tables():
    out = {}
    for n in ('tx_a', 'tx_b', 'tx_c'):
        m = load(n)
        for k, v in m.T.items():
            for i, lg in enumerate(('de', 'ru')): out.setdefault(lg, ({}, {}))[0][k] = v[i]
        for k, v in getattr(m, 'SEG', {}).items():
            for i, lg in enumerate(('de', 'ru')): out.setdefault(lg, ({}, {}))[1][k] = v[i]
    keys = json.load(open(f'{I18N}/keys.json'))
    longk = list(load('tx_b').T.keys())
    Q4 = ('fr', 'es', 'it', 'el')
    for n in ('tx_q1', 'tx_q2'):
        m = load(n)
        for i, v in m.Q.items():
            for j, lg in enumerate(Q4): out.setdefault(lg, ({}, {}))[0][keys[i]] = v[j]
        for k, v in getattr(m, 'SEGQ', {}).items():
            for j, lg in enumerate(Q4): out.setdefault(lg, ({}, {}))[1][k] = v[j]
    m = load('tx_q3')
    if m:
        for i, v in m.L.items():
            for j, lg in enumerate(Q4): out.setdefault(lg, ({}, {}))[0][longk[i]] = v[j]
    mx = load('tx_x')
    for k, v in (getattr(mx, 'X', {}) if mx else {}).items():
        for lg, t in v.items(): out.setdefault(lg, ({}, {}))[0][k] = t
    for lg in ('fr', 'es', 'it', 'el', 'de', 'ru'):
        m = load('tx_' + lg)
        if not m: continue
        t, s = out.setdefault(lg, ({}, {}))
        t.update(m.T); s.update(getattr(m, 'SEG', {}))
    return out

def jsq(s): return s.replace('\\', '\\\\').replace('\n', '\\n')

def translate(h, lg, T, SEG):
    for k, v in SEG.items(): h = h.replace(k, v)
    for k in sorted(T, key=len, reverse=True):
        v = T[k]
        if v == k: continue
        assert '"' not in v and "'" not in v, (lg, v)
        kj, vj = jsq(k), jsq(v)
        h = re.sub(r'(>\s*)' + re.escape(k) + r'(\s*<)', lambda m: m.group(1) + v + m.group(2), h)
        h = h.replace('="' + k + '"', '="' + v + '"')
        h = h.replace("'" + kj + "'", "'" + vj + "'").replace('"' + kj + '"', '"' + vj + '"')
    return h

def build_lang(lg, T, SEG):
    for rel, f in PAGES.items():
        h = open(f'{ROOT}/en/{f}').read()
        h = translate(h, lg, T, SEG)
        h = h.replace('<html lang="en">', f'<html lang="{lg}">').replace("'en-GB'", f"'{LOCALE[lg]}'")
        # pages that exist only in TR/EN
        h = h.replace("PAYURL='payment/'", "PAYURL='../en/payment/'").replace("PAYU='../payment/'", "PAYU='../../en/payment/'")
        os.makedirs(os.path.dirname(f'{ROOT}/{lg}/{f}'), exist_ok=True)
        open(f'{ROOT}/{lg}/{f}', 'w').write(h)

# ---- language switcher on every page
EQUIV = {
    'home': {'tr': '/', 'en': '/en/', '*': '/{l}/'},
    'ws': {'tr': '/atolyeler/', 'en': '/en/workshops/', '*': '/{l}/workshops/'},
    'camps': {'tr': '/kamplar/', 'en': '/en/camps/', '*': '/{l}/camps/'},
    'apply': {'tr': '/basvuru/', 'en': '/en/apply/', '*': '/{l}/apply/'},
    'pay': {'tr': '/odeme/', 'en': '/en/payment/', '*': '/en/payment/'},
    'res': {'tr': '/odeme/sonuc/', 'en': '/en/payment/result/', '*': '/en/payment/result/'},
}
def page_of(rel):
    parts = rel.strip('/').split('/') if rel.strip('/') else []
    cur = 'tr'
    if parts and parts[0] in NAMES and parts[0] != 'tr': cur = parts.pop(0)
    p = '/'.join(parts)
    key = {'': 'home', 'atolyeler': 'ws', 'workshops': 'ws', 'kamplar': 'camps', 'camps': 'camps', 'basvuru': 'apply', 'apply': 'apply',
           'odeme': 'pay', 'payment': 'pay', 'odeme/sonuc': 'res', 'payment/result': 'res'}.get(p, 'home')
    return cur, key

SWITCH_CSS = '<style id="langs-css">.langs{position:relative}.langs summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:5px;min-width:44px;min-height:42px;padding:0 10px;font-weight:800;font-size:14px;border-radius:999px}.langs summary::-webkit-details-marker{display:none}.langs summary::after{content:"";width:6px;height:6px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translateY(-2px)}.langs summary:hover,.langs[open] summary{background:rgba(0,0,0,.06)}.langm{position:absolute;right:0;top:calc(100% + 6px);z-index:80;background:#fff;color:#000;border:1.5px solid #000;border-radius:14px;padding:6px;display:grid;min-width:150px;box-shadow:0 12px 30px rgba(0,0,0,.18)}.langm a{padding:9px 12px;border-radius:9px;font-weight:700;font-size:14px;text-decoration:none;color:inherit;white-space:nowrap}.langm a:hover{background:#F6F4EA}.langm a[aria-current]{background:#000;color:#fff}@media(max-width:600px){.langm{position:fixed;left:12px;right:12px;top:66px;grid-template-columns:1fr 1fr}}@media(max-width:420px){.langs summary{min-width:36px;padding:0 6px;font-size:12px}}</style>'
SWITCH_JS = '<script id="langs-js">document.addEventListener("click",e=>{document.querySelectorAll("details.langs[open]").forEach(d=>{if(!d.contains(e.target))d.open=false})});addEventListener("keydown",e=>{if(e.key==="Escape")document.querySelectorAll("details.langs[open]").forEach(d=>d.open=false)});</script>'

def switcher(cur, key, langs):
    eq = EQUIV[key]
    links = ''.join(f'<a href="{eq.get(l, eq["*"]).format(l=l)}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == cur else ""}>{NAMES[l]}</a>' for l in langs)
    return f'<details class="langs"><summary aria-label="Language · Dil">{cur.upper()}</summary><div class="langm">{links}</div></details>'


CART_TX = {'tr':'Sepet','en':'Cart','de':'Warenkorb','ru':'Корзина','fr':'Panier','es':'Carrito','it':'Carrello','el':'Καλάθι'}
SHOP_TX = {'tr':'Hediyeler','en':'Gifts','de':'Geschenke','ru':'Подарки','fr':'Cadeaux','es':'Regalos','it':'Regali','el':'Δώρα'}
def hright(cur, sw):
    home = EQUIV['home'].get(cur, EQUIV['home']['*']).format(l=cur)
    return f'<div class="hright"><a class="hshop" href="{home}#hediyeler">{SHOP_TX.get(cur, "Shop")}</a>{cart_link(cur)}{sw}</div>'
CART_CSS = '<style id="hcart-css">.hright{display:flex;align-items:center;gap:4px;margin-left:auto}.hright+.menu,.hright~.menu{margin-left:6px}.hshop{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border:1.5px solid #E4452F;border-radius:999px;background:#E4452F;font-weight:800;font-size:14px;color:#fff;text-decoration:none;white-space:nowrap;transition:background .2s,border-color .2s}.hshop:hover{background:#c23620;border-color:#c23620;color:#fff}@media(max-width:420px){.hshop{padding:0 9px;min-height:34px;font-size:12px}.hright{gap:0}}.hcart{position:relative;display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:999px;color:inherit;text-decoration:none}.hcart:hover{background:rgba(0,0,0,.06)}.hcart svg{width:22px;height:22px}.hcart b{position:absolute;top:2px;right:0;min-width:18px;height:18px;padding:0 5px;border-radius:999px;background:#E4452F;color:#fff;font:800 11px/18px Urbanist,system-ui,sans-serif;text-align:center;transform:scale(0);transition:transform .2s}.hcart.has b{transform:scale(1)}.hcart.pop b{animation:hcp .4s}@keyframes hcp{50%{transform:scale(1.35)}}@media(max-width:420px){.hcart{width:36px}}</style>'
CART_JS = '<script id="hcart-js">(()=>{const a=document.getElementById("hcart");if(!a)return;const b=a.querySelector("b");let last=-1;const u=()=>{let n=0;try{n=JSON.parse(localStorage.getItem("no-cart")||"[]").reduce((s,x)=>s+(+x.qty||0),0)}catch(_){}b.textContent=n;a.classList.toggle("has",n>0);if(last>=0&&n>last){a.classList.remove("pop");void a.offsetWidth;a.classList.add("pop")}last=n};u();addEventListener("cart",u);addEventListener("storage",u);a.addEventListener("click",e=>{const s=document.querySelector("#hediyeler .scart");if(s){e.preventDefault();s.click()}})})()</script>'
def cart_link(cur):
    home = EQUIV['home'].get(cur, EQUIV['home']['*']).format(l=cur)
    lab = CART_TX.get(cur, 'Cart')
    return f'<a class="hcart" id="hcart" href="{home}#sepet" aria-label="{lab}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.4 11h10.2L20 7H6.2" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="9" cy="19" r="1.6" fill="currentColor"/><circle cx="17" cy="19" r="1.6" fill="currentColor"/></svg><b>0</b></a>'

# ---- dropdowns under Atölyeler / Kamplar in the main nav (all pages, all languages)
DD_TX = {'tr':('Tüm atölyeler','Tüm kamplar'),'en':('All workshops','All camps'),'de':('Alle Workshops','Alle Camps'),'ru':('Все мастер-классы','Все лагеря'),
         'fr':('Tous les ateliers','Tous les camps'),'es':('Todos los talleres','Todos los campamentos'),'it':('Tutti i workshop','Tutti i campi'),'el':('Όλα τα εργαστήρια','Όλες οι κατασκηνώσεις')}
DD_SHORT = {'pfs-2027-01':'Prague Film School — Acting for Film','central-2027-02':'Royal Central — Audition Bootcamp','frantic-2027-03':'Frantic Assembly — Scott Graham',
            'isc-winter-2027':'ISC — Winter Edition','isc-summer-2027':'ISC — Summer Edition'}
DD_CSS = '<style id="ddm-css">nav.main .dd{position:relative;display:flex;flex-direction:column}nav.main .dd>a{display:inline-flex;align-items:center;gap:6px}nav.main .dd>a::after{content:"";display:inline-block;flex:none;box-sizing:border-box;width:8px;height:8px;border:0;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translate(-1px,-1px);transition:transform .2s;margin-left:2px}nav.main .dd.open>a::after{transform:rotate(-135deg) translate(-2px,-2px)}.ddp{display:none;position:absolute;top:calc(100% + 6px);left:0;min-width:240px;background:#fff;color:#000;border:1px solid rgba(0,0,0,.1);border-radius:16px;box-shadow:0 18px 50px rgba(0,0,0,.18);padding:8px;z-index:90}.dd.open .ddp{display:block;animation:ddin .18s ease}@keyframes ddin{from{opacity:0;transform:translateY(-4px)}}.ddp a{display:flex!important;flex-direction:column;align-items:flex-start!important;gap:2px;padding:10px 12px!important;border-radius:10px!important;border:0!important;color:#000!important;text-decoration:none;font-size:15px!important;white-space:normal!important}.ddp a::after{display:none!important}.ddp a:hover{background:#f3efd8!important}.ddp a small{font-size:12px;font-weight:600;color:#666}.ddp a.ddall{margin-top:4px;border-top:1px solid #eee!important;border-radius:0 0 10px 10px!important;color:#E4452F!important}nav.main.ddcol .ddp{position:static;min-width:0;box-shadow:none;border:0;border-radius:0;padding:0 0 8px 12px;background:transparent}nav.main.ddcol .ddp a{color:inherit!important;font-size:16px!important;padding:10px 4px!important}nav.main.ddcol .ddp a small{color:inherit;opacity:.65}</style>'
def dd_js(cur, root):
    import json as _j, re as _r
    paths = {'tr': ('atolyeler/', 'kamplar/'), 'en': ('en/workshops/', 'en/camps/')}.get(cur, (f'{cur}/workshops/', f'{cur}/camps/'))
    hs = ('siradaki', 'gecmis') if cur == 'tr' else ('upcoming', 'past')
    menu = {}
    for kind, path in zip(('atolye', 'kamp'), paths):
        h = open(f'{root}/{path}index.html').read()
        up = _r.search(r'data-tab="up"[^>]*>([^<]+)', h).group(1).strip()
        past = _r.search(r'data-tab="past"[^>]*>([^<]+)', h).group(1).strip()
        menu[kind] = [[up, '/' + path + '#' + hs[0]], [past, '/' + path + '#' + hs[1]]]
    return ('<script id="ddm-js">(()=>{const M=' + _j.dumps(menu, ensure_ascii=False) + ';'
      'const nav=document.querySelector("nav.main");if(!nav)return;'
      'const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]));'
      'const kindOf=a=>{const h=a.getAttribute("href")||"";return /(atolyeler|workshops)\\/?$/.test(h)?"atolye":/(kamplar|camps)\\/?$/.test(h)?"kamp":null};'
      '[...nav.querySelectorAll(":scope > a")].forEach(a=>{const k=kindOf(a);if(!k)return;const w=document.createElement("div");w.className="dd";a.replaceWith(w);w.appendChild(a);a.setAttribute("aria-haspopup","true");a.setAttribute("aria-expanded","false");'
      'const pn=document.createElement("div");pn.className="ddp";pn.innerHTML=M[k].map(([t,u])=>`<a href="${u}">${esc(t)}</a>`).join("");w.appendChild(pn);'
      'const set=o=>{nav.querySelectorAll(".dd.open").forEach(x=>{if(x!==w){x.classList.remove("open");x.firstChild.setAttribute("aria-expanded","false")}});w.classList.toggle("open",o);a.setAttribute("aria-expanded",String(o))};'
      'const fine=matchMedia("(hover:hover) and (pointer:fine)");let tm,hv=0;'
      'a.addEventListener("click",e=>{e.preventDefault();nav.classList.toggle("ddcol",getComputedStyle(nav).flexDirection==="column");set(Date.now()-hv<700?true:!w.classList.contains("open"))});'
      'w.addEventListener("mouseenter",()=>{if(!fine.matches||getComputedStyle(nav).flexDirection==="column")return;clearTimeout(tm);nav.classList.remove("ddcol");if(!w.classList.contains("open"))hv=Date.now();set(true)});w.addEventListener("mouseleave",()=>{if(!fine.matches||getComputedStyle(nav).flexDirection==="column")return;tm=setTimeout(()=>set(false),180)});'
      'pn.addEventListener("click",e=>{if(e.target.closest("a"))set(false)})});'
      'document.addEventListener("click",e=>{if(!e.target.closest(".dd"))nav.querySelectorAll(".dd.open").forEach(x=>{x.classList.remove("open");x.firstChild.setAttribute("aria-expanded","false")})});'
      'addEventListener("keydown",e=>{if(e.key==="Escape")nav.querySelectorAll(".dd.open").forEach(x=>{x.classList.remove("open");x.firstChild.setAttribute("aria-expanded","false")})})})()</script>')

# ---- card logos (Visa, Mastercard, Troy) in every footer + price chips on programme lists
PAY_TX = {'tr':'Güvenli ödeme · 3D Secure','en':'Secure payment · 3D Secure','de':'Sichere Zahlung · 3D Secure','ru':'Безопасная оплата · 3D Secure','fr':'Paiement sécurisé · 3D Secure','es':'Pago seguro · 3D Secure','it':'Pagamento sicuro · 3D Secure','el':'Ασφαλής πληρωμή · 3D Secure'}
PAY_LOGOS = ('<span class="pl visa" aria-label="Visa"><svg viewBox="0 0 64 22" aria-hidden="true"><text x="32" y="17" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-style="italic" font-size="19" fill="#1A1F71" letter-spacing="1">VISA</text></svg></span>'
  '<span class="pl mc" aria-label="Mastercard"><svg viewBox="0 0 40 24" aria-hidden="true"><circle cx="15" cy="12" r="10" fill="#EB001B"/><circle cx="25" cy="12" r="10" fill="#F79E1B"/><path d="M20 3.3a10 10 0 0 1 0 17.4a10 10 0 0 1 0-17.4z" fill="#FF5F00"/></svg></span>'
  '<span class="pl troy" aria-label="Troy"><svg viewBox="0 0 60 22" aria-hidden="true"><text x="30" y="17" text-anchor="middle" font-family="Arial,sans-serif" font-weight="800" font-size="18" fill="#00264D">tr<tspan fill="#00B6C8">o</tspan>y</text></svg></span>')
PAY_CSS = '<style id="pay-css">.paylogos{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:18px auto 0;padding:14px max(5vw,18px) 4px;max-width:1240px;font-size:12px;opacity:.85}.paylogos .pl{display:inline-flex;align-items:center;justify-content:center;background:#fff;border-radius:6px;height:30px;padding:0 8px;box-shadow:0 0 0 1px rgba(0,0,0,.12)}.paylogos .pl svg{height:20px;width:auto}.paylogos .pl.mc svg{height:22px}.paylogos small{font-weight:700;letter-spacing:.02em}.prcrow{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.prcrow .prc{margin-right:0}.prc{display:inline-flex;align-items:center;font-weight:800;font-size:14px;white-space:nowrap;margin-right:auto}.prc small{font-weight:600;opacity:.7;margin-left:4px;font-size:12px}</style>'
VAT_W = {'tr':'KDV','en':'VAT','de':'MwSt.','ru':'НДС','fr':'TVA','es':'IVA','it':'IVA','el':'ΦΠΑ'}
def price_js(cur, root):
    import json as _j
    progs = _j.load(open(f'{root}/data/programs.json'))['programs']
    data = {p['id']: p['net'] for p in progs if p.get('net') and p.get('open', True)}
    loc = 'tr-TR' if cur == 'tr' else LOCALE.get(cur, 'en-GB')
    return ('<script id="price-js">(()=>{const N=' + _j.dumps(data) + ',V=' + _j.dumps(VAT_W.get(cur, 'VAT'), ensure_ascii=False) + ',LC=' + _j.dumps(loc) + ';'
      'const f=n=>n.toLocaleString(LC)+" TL";const chip=id=>{const s=document.createElement("span");s.className="prc";s.innerHTML=f(N[id])+"<small>+ "+V+"</small>";return s};'
      'const run=()=>{document.querySelectorAll("a[href*=\\"?p=\\"],[data-ap]").forEach(a=>{const id=a.dataset.ap||new URL(a.href,location.href).searchParams.get("p");if(!N[id])return;const box=a.parentElement;if(box.querySelector(":scope > .prc"))return;if(box.classList.contains("acts"))return;{const r=document.createElement("div");r.className="prcrow";r.appendChild(chip(id));a.before(r);r.appendChild(a)}})};'
      'run();new MutationObserver(run).observe(document.body,{childList:true,subtree:true})})()</script>')

# ---- header auto-fit: tighten, then collapse to the Menu button when nav items do not fit (long languages)
NAVFIT_CSS = ('<style id="navfit-css">@media(min-width:1500px){header .bar{max-width:1680px}}@media(min-width:1301px){header .bar>*,.portals>*,.hright>*{flex-shrink:0}nav.main{flex-shrink:0}nav.main>a,nav.main>.dd{flex-shrink:0}nav.main>a,nav.main>.dd>a{white-space:nowrap}'
  'header.nv-tight nav.main{gap:0}header.nv-tight nav.main>a,header.nv-tight nav.main>.dd>a{padding:10px 7px;font-size:14px}'
  'header.nv-compact nav.main{display:none}header.nv-compact .menu{display:block;margin-inline-start:6px}'
  'header.nv-compact.open nav.main{display:flex;position:absolute;top:100%;left:0;right:0;flex-direction:column;background:#fff;padding:8px max(5vw,18px) 18px;border-bottom:1px solid var(--lineK,#ddd)}'
  'header.nv-compact.open nav.main>a,header.nv-compact.open nav.main>.dd>a{font-size:18px;padding:14px 4px;border-bottom:1px solid var(--lineK,#ddd)}}</style>')
NAVFIT_JS = ('<script id="navfit-js">(()=>{const h=document.querySelector("header"),nav=h&&h.querySelector("nav.main");if(!nav)return;const bar=nav.parentElement;'
  'const vis=e=>e&&e.offsetWidth&&getComputedStyle(e).display!=="none";'
  'const fits=()=>{if(!vis(nav))return true;const kids=[...nav.children].filter(vis);if(!kids.length)return true;const last=kids[kids.length-1].getBoundingClientRect().right;'
  'let nx=nav.nextElementSibling;while(nx&&!vis(nx))nx=nx.nextElementSibling;const lim=nx?nx.getBoundingClientRect().left:bar.getBoundingClientRect().right;'
  'const tail=[...bar.children].filter(vis).pop();const br=bar.getBoundingClientRect().right;'
  'const squeezed=[...bar.querySelectorAll("a,button")].some(e=>vis(e)&&!e.closest(".ddp")&&e.scrollWidth>e.clientWidth+1);return !squeezed&&last<=lim-6&&(!tail||tail.getBoundingClientRect().right<=br+1)&&bar.scrollWidth<=bar.clientWidth+1};'
  'const fit=()=>{h.classList.remove("nv-tight","nv-compact");if(innerWidth<=1300||fits())return;h.classList.add("nv-tight");if(fits())return;h.classList.remove("nv-tight");h.classList.add("nv-compact")};'
  'let t;addEventListener("resize",()=>{clearTimeout(t);t=setTimeout(fit,80)});if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);fit();setTimeout(fit,400)})()</script>')

WA_NUM = '905304808292'
WA_TX = {'tr': ('WhatsApp Canlı Destek', 'Merhaba, atölyeleriniz ve kamplarınız hakkında bilgi almak istiyorum.'), 'en': ('WhatsApp Live Support', 'Hello, I’d like some information about your workshops and camps.'),
         'de': ('WhatsApp Live-Support', 'Hallo, ich hätte gerne Informationen zu Ihren Workshops und Camps.'), 'ru': ('Онлайн-поддержка WhatsApp', 'Здравствуйте, я хотел(а) бы узнать о ваших мастер-классах и лагерях.'),
         'fr': ('Assistance WhatsApp en direct', 'Bonjour, je souhaiterais des informations sur vos ateliers et stages.'), 'es': ('Soporte en vivo por WhatsApp', 'Hola, me gustaría recibir información sobre vuestros talleres y campamentos.'),
         'it': ('Assistenza live su WhatsApp', 'Ciao, vorrei ricevere informazioni sui vostri workshop e campus.'), 'el': ('Ζωντανή υποστήριξη στο WhatsApp', 'Γεια σας, θα ήθελα πληροφορίες για τα εργαστήρια και τις κατασκηνώσεις σας.')}
WA_CSS = '<style id="wa-css">.wa-fab{position:fixed;right:18px;bottom:18px;z-index:90;display:flex;align-items:center;gap:10px;background:#25D366;color:#fff;text-decoration:none;font:800 15px/1 Urbanist,system-ui,sans-serif;padding:0 20px 0 14px;height:56px;border-radius:999px;box-shadow:0 10px 28px rgba(0,0,0,.22);transition:transform .2s,box-shadow .2s}.wa-fab:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,.28)}.wa-fab svg{width:30px;height:30px;flex:0 0 auto}.wa-fab .wa-dot{position:absolute;top:6px;left:40px;width:11px;height:11px;border-radius:50%;background:#b8ffcf;border:2px solid #25D366;animation:wap 1.8s ease-out infinite}@keyframes wap{0%{box-shadow:0 0 0 0 rgba(255,255,255,.7)}70%{box-shadow:0 0 0 8px rgba(255,255,255,0)}100%{box-shadow:0 0 0 0 rgba(255,255,255,0)}}@media(max-width:700px){.wa-fab{padding:0;width:56px;justify-content:center;right:14px;bottom:14px}.wa-fab span.wa-l{display:none}.wa-fab .wa-dot{left:36px}}@media(prefers-reduced-motion:reduce){.wa-fab .wa-dot{animation:none}}@media print{.wa-fab{display:none}}.wa-fab.wa-off{opacity:0;pointer-events:none;transform:translateY(12px)}.wa-fab{transition:opacity .25s,transform .25s,box-shadow .2s}</style>'
WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.4c-2.1 0-4.1-.6-5.9-1.6l-.4-.3-3.8 1.2 1.2-3.7-.3-.4a10.4 10.4 0 0 1-1.7-5.8C5.1 9.9 10 5.2 16 5.2s10.9 4.7 10.9 10.6S22 26.4 16 26.4zm6-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6.3-.5c.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.1 1.1-1.1 2.7s1.2 3.2 1.3 3.4c.2.2 2.3 3.5 5.6 4.9 2.8 1.1 3.3.9 3.9.8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
from urllib.parse import quote
def wa_fab(cur):
    lab, msg = WA_TX.get(cur, WA_TX['en'])
    return f'<a class="wa-fab" id="wa-fab" href="https://wa.me/{WA_NUM}?text={quote(msg)}" target="_blank" rel="noopener" aria-label="{lab}">{WA_SVG}<span class="wa-dot" aria-hidden="true"></span><span class="wa-l">{lab}</span></a><script id="wa-js">(()=>{{const f=document.getElementById("wa-fab"),s=document.querySelector(".slider");if(!f||!s)return;const u=()=>{{const r=s.getBoundingClientRect();f.classList.toggle("wa-off",r.bottom>innerHeight-90&&r.top<innerHeight)}};u();addEventListener("scroll",u,{{passive:true}});addEventListener("resize",u)}})()</script>'

def place_switchers(langs):
    files = [f for f in glob.glob(f'{ROOT}/**/index.html', recursive=True) if '/node_modules/' not in f and '/tools/' not in f and '/dist/' not in f]
    n = 0
    for f in files:
        rel = os.path.relpath(os.path.dirname(f), ROOT); rel = '' if rel == '.' else rel
        cur, key = page_of(rel)
        h = open(f).read()
        sw = switcher(cur, key, langs)
        h2 = re.sub(r'<div class="hright">.*?</details></div>', '<a class="lang" href="#">X</a>', h, flags=re.S)
        h2 = re.sub(r'<a class="hcart" id="hcart".*?</a>', '', h2, flags=re.S)
        if not rel.startswith('yonetim'): sw = hright(cur, sw)
        tok = r'<a class="lang"[^>]*>[^<]*</a>|<details class="langs">.*?</details>'
        if not rel.startswith('yonetim') and '<button class="menu"' in h2:
            h2 = re.sub(tok, '', h2, count=1, flags=re.S).replace('<button class="menu"', sw + '\n    <button class="menu"', 1)
        else:
            h2 = re.sub(tok, lambda m: sw, h2, flags=re.S)
        h2 = re.sub(r'<style id="hcart-css">.*?</style>', '', h2, flags=re.S)
        h2 = re.sub(r'<script id="hcart-js">.*?</script>', '', h2, flags=re.S)
        if not rel.startswith('yonetim'): h2 = h2.replace('</head>', CART_CSS + '</head>', 1).replace('</body>', CART_JS + '</body>', 1)
        h2 = re.sub(r'<style id="navfit-css">.*?</style>', '', h2, flags=re.S)
        h2 = re.sub(r'<script id="navfit-js">.*?</script>', '', h2, flags=re.S)
        if not rel.startswith('yonetim') and '<nav class="main"' in h2: h2 = h2.replace('</head>', NAVFIT_CSS + '</head>', 1).replace('</body>', NAVFIT_JS + '</body>', 1)
        h2 = re.sub(r'<style id="pay-css">.*?</style>', '', h2, flags=re.S)
        h2 = re.sub(r'<script id="price-js">.*?</script>', '', h2, flags=re.S)
        h2 = re.sub(r'<div class="paylogos" id="paylogos">.*?</div>', '', h2, flags=re.S)
        if not rel.startswith('yonetim'):
            h2 = h2.replace('</head>', PAY_CSS + '</head>', 1)
            if '</footer>' in h2: h2 = h2.replace('</footer>', '<div class="paylogos" id="paylogos">' + PAY_LOGOS + '<small>' + PAY_TX.get(cur, PAY_TX['en']) + '</small></div></footer>', 1)
            h2 = h2.replace('</body>', price_js(cur, ROOT) + '</body>', 1)
        h2 = re.sub(r'<style id="ddm-css">.*?</style>', '', h2, flags=re.S)
        h2 = re.sub(r'<script id="ddm-js">.*?</script>', '', h2, flags=re.S)
        if not rel.startswith('yonetim') and '<nav class="main"' in h2: h2 = h2.replace('</head>', DD_CSS + '</head>', 1).replace('</body>', dd_js(cur, ROOT) + '</body>', 1)
        h2 = re.sub(r'<style id="langs-css">.*?</style>', '', h2, flags=re.S).replace('</head>', SWITCH_CSS + '</head>', 1)
        h2 = re.sub(r'<script id="langs-js">.*?</script>', '', h2, flags=re.S).replace('</body>', SWITCH_JS + '</body>', 1)
        h2 = re.sub(r'<style id="wa-css">.*?</style>', '', h2, flags=re.S)
        h2 = re.sub(r'<a class="wa-fab" id="wa-fab".*?</a>', '', h2, flags=re.S)
        h2 = re.sub(r'<script id="wa-js">.*?</script>', '', h2, flags=re.S)
        if not rel.startswith('yonetim'):
            h2 = h2.replace('</head>', WA_CSS + '</head>', 1).replace('</body>', wa_fab(cur) + '</body>', 1)
        if h2 != h: open(f, 'w').write(h2); n += 1
    return n

if __name__ == '__main__':
    TB = tables()
    built = []
    for lg in ('de', 'ru', 'fr', 'es', 'it', 'el'):
        if lg in TB and len(TB[lg][0]) > 100:
            build_lang(lg, *TB[lg]); built.append(lg)
    langs = ['tr', 'en'] + built
    print('languages:', langs, 'switchers updated:', place_switchers(langs))
