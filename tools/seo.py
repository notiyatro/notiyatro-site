# SEO: başlık, açıklama, canonical, hreflang, Open Graph, JSON-LD; sitemap.xml ve robots.txt (idempotent).
import pathlib,re,json,datetime
ROOT=pathlib.Path('/home/claude/notiyatro'); B='https://notiyatro.com'
L=['tr','en','de','ru','fr','es','it','el']
LOC={'tr':'tr_TR','en':'en_GB','de':'de_DE','ru':'ru_RU','fr':'fr_FR','es':'es_ES','it':'it_IT','el':'el_GR'}
def url(g,l):
    if g=='home': return '/' if l=='tr' else f'/{l}/'
    tr={'workshops':'/atolyeler/','camps':'/kamplar/'}[g]
    return tr if l=='tr' else f'/{l}/{g}/'
T={
'home':{
 'tr':('NO Tiyatro — Uluslararası Tiyatro Atölyeleri ve Kampları | İstanbul','2017’den beri RADA, LAMDA, Royal Central, Shakespeare’s Globe ve Frantic Assembly eğitmenleriyle İstanbul’da uluslararası oyunculuk ve tiyatro atölyeleri, kamplar ve International Stage Lab.'),
 'en':('NO Tiyatro — International Theatre Workshops & Camps | Istanbul','Since 2017: international acting and theatre workshops, camps and International Stage Lab. in Istanbul with tutors from RADA, LAMDA, Royal Central, Shakespeare’s Globe and Frantic Assembly.'),
 'de':('NO Tiyatro — Internationale Theater-Workshops & Camps | Istanbul','Seit 2017: internationale Schauspiel- und Theaterworkshops, Camps und International Stage Lab. in Istanbul mit Dozierenden von RADA, LAMDA, Royal Central, Shakespeare’s Globe und Frantic Assembly.'),
 'ru':('NO Tiyatro — международные театральные мастер-классы и лагеря | Стамбул','С 2017 года: международные мастер-классы по актёрскому мастерству, театральные лагеря и International Stage Lab. в Стамбуле с педагогами RADA, LAMDA, Royal Central, Shakespeare’s Globe и Frantic Assembly.'),
 'fr':('NO Tiyatro — Ateliers et stages internationaux de théâtre | Istanbul','Depuis 2017 : ateliers internationaux de jeu et de théâtre, stages et International Stage Lab. à Istanbul avec des intervenants de RADA, LAMDA, Royal Central, Shakespeare’s Globe et Frantic Assembly.'),
 'es':('NO Tiyatro — Talleres y campamentos internacionales de teatro | Estambul','Desde 2017: talleres internacionales de interpretación y teatro, campamentos e International Stage Lab. en Estambul con profesores de RADA, LAMDA, Royal Central, Shakespeare’s Globe y Frantic Assembly.'),
 'it':('NO Tiyatro — Workshop e campi internazionali di teatro | Istanbul','Dal 2017: workshop internazionali di recitazione e teatro, campi e International Stage Lab. a Istanbul con docenti di RADA, LAMDA, Royal Central, Shakespeare’s Globe e Frantic Assembly.'),
 'el':('NO Tiyatro — Διεθνή εργαστήρια και κατασκηνώσεις θεάτρου | Κωνσταντινούπολη','Από το 2017: διεθνή εργαστήρια υποκριτικής και θεάτρου, κατασκηνώσεις και International Stage Lab. στην Κωνσταντινούπολη με διδάσκοντες από RADA, LAMDA, Royal Central, Shakespeare’s Globe και Frantic Assembly.')},
'workshops':{
 'tr':('Oyunculuk ve Tiyatro Atölyeleri — NO Tiyatro','RADA, LAMDA, Royal Central ve Frantic Assembly eğitmenleriyle İstanbul’da sıradaki ve geçmiş uluslararası oyunculuk, fiziksel tiyatro ve ses atölyeleri. Tarihler, ücretler ve başvuru.'),
 'en':('Acting & Theatre Workshops — NO Tiyatro','Upcoming and past international acting, physical theatre and voice workshops in Istanbul with tutors from RADA, LAMDA, Royal Central and Frantic Assembly. Dates, fees and applications.'),
 'de':('Schauspiel- und Theaterworkshops — NO Tiyatro','Kommende und vergangene internationale Workshops für Schauspiel, physisches Theater und Stimme in Istanbul mit Dozierenden von RADA, LAMDA, Royal Central und Frantic Assembly. Termine, Preise und Bewerbung.'),
 'ru':('Мастер-классы по актёрскому мастерству и театру — NO Tiyatro','Ближайшие и прошедшие международные мастер-классы по актёрскому мастерству, физическому театру и голосу в Стамбуле с педагогами RADA, LAMDA, Royal Central и Frantic Assembly. Даты, стоимость и заявки.'),
 'fr':('Ateliers de jeu et de théâtre — NO Tiyatro','Ateliers internationaux à venir et passés de jeu, théâtre physique et voix à Istanbul avec des intervenants de RADA, LAMDA, Royal Central et Frantic Assembly. Dates, tarifs et candidatures.'),
 'es':('Talleres de interpretación y teatro — NO Tiyatro','Próximos y pasados talleres internacionales de interpretación, teatro físico y voz en Estambul con profesores de RADA, LAMDA, Royal Central y Frantic Assembly. Fechas, precios e inscripciones.'),
 'it':('Workshop di recitazione e teatro — NO Tiyatro','Workshop internazionali in programma e passati di recitazione, teatro fisico e voce a Istanbul con docenti di RADA, LAMDA, Royal Central e Frantic Assembly. Date, quote e candidature.'),
 'el':('Εργαστήρια υποκριτικής και θεάτρου — NO Tiyatro','Επερχόμενα και προηγούμενα διεθνή εργαστήρια υποκριτικής, σωματικού θεάτρου και φωνής στην Κωνσταντινούπολη με διδάσκοντες από RADA, LAMDA, Royal Central και Frantic Assembly. Ημερομηνίες, κόστος και αιτήσεις.')},
'camps':{
 'tr':('Uluslararası Tiyatro Kampları — NO Tiyatro','International Stage Camp: Türkiye’de doğanın içinde, uluslararası eğitmenlerle konaklamalı oyunculuk ve tiyatro kampları. Kış ve yaz dönemleri, ücretler ve başvuru.'),
 'en':('International Theatre Camps — NO Tiyatro','International Stage Camp: residential acting and theatre camps in nature in Türkiye with international tutors. Winter and summer editions, fees and applications.'),
 'de':('Internationale Theatercamps — NO Tiyatro','International Stage Camp: Schauspiel- und Theatercamps mit Unterkunft in der Natur der Türkei mit internationalen Dozierenden. Winter- und Sommerausgaben, Preise und Bewerbung.'),
 'ru':('Международные театральные лагеря — NO Tiyatro','International Stage Camp: театральные лагеря с проживанием на природе в Турции с международными педагогами. Зимние и летние сессии, стоимость и заявки.'),
 'fr':('Stages internationaux de théâtre — NO Tiyatro','International Stage Camp : stages résidentiels de jeu et de théâtre en pleine nature en Turquie avec des intervenants internationaux. Éditions d’hiver et d’été, tarifs et candidatures.'),
 'es':('Campamentos internacionales de teatro — NO Tiyatro','International Stage Camp: campamentos residenciales de interpretación y teatro en plena naturaleza en Turquía con profesores internacionales. Ediciones de invierno y verano, precios e inscripciones.'),
 'it':('Campi internazionali di teatro — NO Tiyatro','International Stage Camp: campi residenziali di recitazione e teatro nella natura in Turchia con docenti internazionali. Edizioni invernali ed estive, quote e candidature.'),
 'el':('Διεθνείς κατασκηνώσεις θεάτρου — NO Tiyatro','International Stage Camp: οικιστικές κατασκηνώσεις υποκριτικής και θεάτρου στη φύση της Τουρκίας με διεθνείς διδάσκοντες. Χειμερινές και καλοκαιρινές εκδόσεις, κόστος και αιτήσεις.')},
}
NOINDEX=['yonetim','odeme','en/payment']
ORG={"@context":"https://schema.org","@type":"PerformingArtsTheater","name":"NO Tiyatro","alternateName":["NO Theatre","notiyatro"],"url":B+"/","logo":B+"/img/icon-512.png","image":B+"/img/og.jpg","foundingDate":"2017","legalName":"NO Yapım ve Organizasyon Limited Şirketi","address":{"@type":"PostalAddress","streetAddress":"Hüseyinağa Mah., İstiklal Cad., Grand Pera No: 56/58 Kat 3 Daire 5","addressLocality":"Beyoğlu","addressRegion":"İstanbul","addressCountry":"TR"},"sameAs":["https://www.instagram.com/notiyatro/"]}
def esc(s): return s.replace('&','&amp;').replace('"','&quot;')
def head_block(g,l):
    t,d=map(esc,T[g][l]); u=B+url(g,l)
    h=[f'<link rel="canonical" href="{u}">']
    h+=[f'<link rel="alternate" hreflang="{x}" href="{B+url(g,x)}">' for x in L]
    h.append(f'<link rel="alternate" hreflang="x-default" href="{B+url(g,"en")}">')
    h+=['<meta property="og:type" content="website">','<meta property="og:site_name" content="NO Tiyatro">',f'<meta property="og:title" content="{t}">',f'<meta property="og:description" content="{d}">',f'<meta property="og:url" content="{u}">',f'<meta property="og:image" content="{B}/img/og.jpg">',f'<meta property="og:locale" content="{LOC[l]}">','<meta name="twitter:card" content="summary_large_image">']
    if g=='home': h.append('<script type="application/ld+json">'+json.dumps(ORG,ensure_ascii=False)+'</script>')
    return '<!--seo-->'+''.join(h)+'<!--/seo-->'
n=0
for g in T:
    for l in L:
        u=url(g,l); p=ROOT/('index.html' if u=='/' else u.strip('/')+'/index.html')
        if not p.exists(): print('missing',p); continue
        s=p.read_text(); t,d=map(esc,T[g][l])
        s=re.sub(r'<!--seo-->.*?<!--/seo-->','',s,flags=re.S)
        s=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?','',s)
        s=re.sub(r'<title>[^<]*</title>',f'<title>{t}</title>',s,count=1)
        s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{d}">',s,count=1)
        s=s.replace('</head>',head_block(g,l)+'</head>',1); p.write_text(s); n+=1
for p in ROOT.rglob('*.html'):
    r=str(p.relative_to(ROOT))
    if any(r.startswith(x) for x in NOINDEX):
        s=p.read_text()
        if 'name="robots"' not in s: p.write_text(s.replace('</head>','<meta name="robots" content="noindex, nofollow"></head>',1))
today=datetime.date.today().isoformat()
xs=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for g in T:
    for l in L:
        alts=''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{B+url(g,x)}"/>' for x in L)
        xs.append(f'<url><loc>{B+url(g,l)}</loc><lastmod>{today}</lastmod>{alts}<xhtml:link rel="alternate" hreflang="x-default" href="{B+url(g,"en")}"/><priority>{"1.0" if g=="home" else "0.8"}</priority></url>')
for lg in ['yasal/','yasal/kvkk/','yasal/on-bilgilendirme/','yasal/mesafeli-satis-sozlesmesi/','yasal/urun-on-bilgilendirme/','yasal/atolye-sozlesmesi/','yasal/kamp-sozlesmesi/']:
    xs.append(f'<url><loc>{B}/{lg}</loc><lastmod>{today}</lastmod><priority>0.3</priority></url>')
xs.append('</urlset>'); (ROOT/'sitemap.xml').write_text('\n'.join(xs)+'\n')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /yonetim/\nDisallow: /odeme/\nDisallow: /en/payment/\nDisallow: /api/\n\nSitemap: {B}/sitemap.xml\n')
print('seo pages:',n)
