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
        h2 = re.sub(r'<a class="lang"[^>]*>[^<]*</a>|<details class="langs">.*?</details>', lambda m: sw, h, flags=re.S)
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
