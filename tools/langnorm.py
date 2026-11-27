# Undo the language switcher so generators see the original single-link header.
import re
def norm(h, lang='tr'):
    a = '<a class="lang" href="en/" hreflang="en" lang="en" aria-label="English version">EN</a>' if lang == 'tr' else '<a class="lang" href="../" hreflang="tr" lang="tr" aria-label="Türkçe sürüm">TR</a>'
    h = re.sub(r'<div class="hright">.*?</details></div>', '<details class="langs"></details>', h, flags=re.S)
    h = re.sub(r'<a class="hcart" id="hcart".*?</a>', '', h, flags=re.S)
    h = re.sub(r'<style id="hcart-css">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<style id="ddm-css">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<style id="pay-css">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<script id="price-js">.*?</script>', '', h, flags=re.S)
    h = re.sub(r'<div class="paylogos" id="paylogos">.*?</div>', '', h, flags=re.S)
    h = re.sub(r'<script id="ddm-js">.*?</script>', '', h, flags=re.S)
    h = re.sub(r'<script id="hcart-js">.*?</script>', '', h, flags=re.S)
    h = re.sub(r'<details class="langs">.*?</details>', a, h, flags=re.S)
    h = re.sub(r'<style id="langs-css">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<style id="wa-css">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<a class="wa-fab" id="wa-fab".*?</a>', '', h, flags=re.S)
    h = re.sub(r'<script id="wa-js">.*?</script>', '', h, flags=re.S)
    return re.sub(r'<script id="langs-js">.*?</script>', '', h, flags=re.S)
