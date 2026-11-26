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

def place_switchers(langs):
    files = [f for f in glob.glob(f'{ROOT}/**/index.html', recursive=True) if '/node_modules/' not in f and '/tools/' not in f and '/dist/' not in f]
    n = 0
    for f in files:
        rel = os.path.relpath(os.path.dirname(f), ROOT); rel = '' if rel == '.' else rel
        cur, key = page_of(rel)
        h = open(f).read()
        sw = switcher(cur, key, langs)
        h2 = re.sub(r'<a class="lang"[^>]*>[^<]*</a>|<details class="langs">.*?</details>', lambda m: sw, h, flags=re.S)
        if h2 == h and sw not in h: continue
        h2 = re.sub(r'<style id="langs-css">.*?</style>', '', h2, flags=re.S).replace('</head>', SWITCH_CSS + '</head>', 1)
        h2 = re.sub(r'<script id="langs-js">.*?</script>', '', h2, flags=re.S).replace('</body>', SWITCH_JS + '</body>', 1)
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
