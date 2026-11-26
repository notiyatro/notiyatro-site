import re, os, json, html as H
ROOT='/home/claude/notiyatro'
from langnorm import norm
tr_idx=norm(open(f'{ROOT}/index.html').read())
en_idx=norm(open(f'{ROOT}/en/index.html').read(),'en')

def part(src, start, end):
    i=src.index(start); j=src.index(end,i)+len(end); return src[i:j]

WA='905304808292'
FORM='https://docs.google.com/forms/d/14PzXPCxvlBrst-hDBj_JiiL5kZgiGx2zQC-7AHUgRWA/viewform'
PAID=[p['id'] for p in json.load(open(f'{ROOT}/data/programs.json'))['programs'] if isinstance(p.get('price'),(int,float)) and p['price']>0]
items=[
 # upcoming workshops
 dict(s='up',type='atolye',d_tr='22–24 Ocak 2027',d_en='22–24 Jan 2027',pid='pfs-2027-01',t_tr='Prague Film School — Acting for Film',t_en='Prague Film School — Acting for Film',place_tr='DasDas Ataşehir, İstanbul',place_en='DasDas Ataşehir, Istanbul',tags_tr=['Resmî İş Birliği','Kamera Önü Oyunculuk'],tags_en=['Official partnership','On-camera acting'],p_tr='Kamera önü oyunculuk, audition ve self-tape üzerine üç günlük yoğun atölye.',p_en='A three-day intensive on acting for camera, auditions and self-tapes.',tut='Amy Huck, Mary-Ellen O’Hara',img=''),
 dict(s='up',type='atolye',d_tr='5–7 Şubat 2027',d_en='5–7 Feb 2027',pid='central-2027-02',t_tr='Royal Central School of Speech and Drama — Audition Bootcamp',t_en='Royal Central School of Speech and Drama — Audition Bootcamp',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Seçme hazırlığı'],tags_en=['Audition preparation'],p_tr='Üç günlük monolog ve seçme hazırlığı; son gün deneme seçmesi (mock audition).',p_en='Three days of monologue and audition preparation, ending with a mock audition.',tut='Mairi Hayes',img=''),
 dict(s='up',type='atolye',d_tr='20–21 Mart 2027',d_en='20–21 Mar 2027',pid='frantic-2027-03',t_tr='Frantic Assembly — Scott Graham',t_en='Frantic Assembly — Scott Graham',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Fiziksel tiyatro'],tags_en=['Physical theatre'],p_tr='Fiziksel tiyatronun öncü topluluğu Frantic Assembly, Scott Graham ile ilk kez İstanbul’da.',p_en='Frantic Assembly comes to Istanbul for the first time with Scott Graham.',tut='Scott Graham',img=''),
 # upcoming camps
 dict(s='up',type='kamp',d_tr='28–31 Ocak 2027',d_en='28–31 Jan 2027',pid='isc-winter-2027',t_tr='International Stage Camp — Winter Edition 2027',t_en='International Stage Camp — Winter Edition 2027',place_tr='Narköy Ekolojik Otel, Kandıra',place_en='Narköy Ecological Hotel, Kandıra',tags_tr=['Kamp','Öne çıkan'],tags_en=['Camp','Featured'],p_tr='Dünya tiyatrosunun iki büyük ismi ilk kez Türkiye’de: West End’de 5 Olivier, Broadway’de 3 Tony Ödülü kazanan Life of Pi’ın yönetmeni Max Webster ile yönetmenlik; Hamilton’daki Aaron Burr rolüyle Olivier Ödülü sahibi Giles Terera ile oyunculuk.',p_en='Two giants of world theatre, in Türkiye for the first time: directing with Max Webster, director of Life of Pi (5 Olivier Awards in the West End, 3 Tony Awards on Broadway), and acting with Olivier Award winner Giles Terera, Aaron Burr in Hamilton.',tut='Max Webster, Giles Terera',img='',f=True),
 dict(s='up',type='kamp',d_tr='22–25 Temmuz 2027',d_en='22–25 Jul 2027',pid='isc-summer-2027',t_tr='International Stage Camp — Summer Edition 2027',t_en='International Stage Camp — Summer Edition 2027',place_tr='Çeşmeköy',place_en='Çeşmeköy',tags_tr=['Kamp'],tags_en=['Camp'],p_tr='Yaz kampı. Eğitmenler yakında duyurulacak.',p_en='The summer camp. Tutors to be announced soon.',tut='',img=''),
 # past camps
 dict(s='past',type='kamp',d_tr='23–26 Temmuz 2026',d_en='23–26 Jul 2026',t_tr='International Stage Camp — Ephesus Edition (II)',t_en='International Stage Camp — Ephesus Edition (II)',place_tr='Ephesus Retreat, Selçuk / İzmir',place_en='Ephesus Retreat, Selçuk / İzmir',tags_tr=['Kamp','4. edisyon'],tags_en=['Camp','4th edition'],p_tr='Kampın dördüncü edisyonu, çağdaş tiyatronun uluslararası ölçekte öne çıkan üç sanatçısını aynı platformda buluşturdu.',p_en='The fourth edition brought together three leading international theatre artists on one platform.',tut='Tim Crouch, Yaël Farber, Nassim Soleimanpour',img='isc-ekip'),
 dict(s='past',type='kamp',d_tr='23–26 Nisan 2026',d_en='23–26 Apr 2026',t_tr='International Stage Camp — Cappadocia Edition',t_en='International Stage Camp — Cappadocia Edition',place_tr='Kapadokya',place_en='Cappadocia',tags_tr=['Kamp','Shakespeare’s Globe'],tags_en=['Camp','Shakespeare’s Globe'],p_tr='Üçüncü edisyon, Shakespeare’s Globe iş birliğiyle Kapadokya’da; Globe’un eğitim yaklaşımı Türkiye’deki katılımcılarla buluştu.',p_en='The third edition, in Cappadocia in collaboration with Shakespeare’s Globe, bringing the Globe’s training approach to participants.',tut='Scott Brooksbank, Susan Vidler, Jonathan Woolf',img='w/isc-cappadocia'),
 dict(s='past',type='kamp',d_tr='29 Ocak – 1 Şubat 2026',d_en='29 Jan – 1 Feb 2026',t_tr='International Stage Camp — Winter Edition',t_en='International Stage Camp — Winter Edition',place_tr='Narköy, Kandıra / Kocaeli',place_en='Narköy, Kandıra / Kocaeli',tags_tr=['Kamp','2. edisyon'],tags_en=['Camp','2nd edition'],p_tr='İkinci edisyon; yönetmenlik, oyunculuk ve oyun yazarlığı alanlarında uluslararası sanatçılarla dört gün.',p_en='The second edition: four days of directing, acting and playwriting with international artists.',tut='Simon Godwin, Savvas Stroumpos, Eve Leigh, Simon Stephens',img='w/isc-winter'),
 dict(s='past',type='kamp',d_tr='31 Temmuz – 3 Ağustos 2025',d_en='31 Jul – 3 Aug 2025',t_tr='International Stage Camp — Ephesus Edition (I)',t_en='International Stage Camp — Ephesus Edition (I)',place_tr='Ephesus Retreat, Selçuk / İzmir',place_en='Ephesus Retreat, Selçuk / İzmir',tags_tr=['Kamp','1. edisyon'],tags_en=['Camp','1st edition'],p_tr='ISC’nin ilk edisyonu: yaratım, doğa ve disiplinlerarası üretim ekseninde dört gün.',p_en='ISC’s first edition: four days of creation, nature and interdisciplinary work.',tut='Omar Elerian, Carmen Nasr, Alex Murphy',img='w/isc-ephesus1'),
 # past workshops 2026
 dict(s='past',type='atolye',d_tr='20–22 Kasım 2026',d_en='20–22 Nov 2026',t_tr='Shakespeare’s Globe',t_en='Shakespeare’s Globe',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Shakespeare'],tags_en=['Shakespeare'],p_tr='Shakespeare’s Globe × International Stage Lab. Çocuk ve yetişkin grupları.',p_en='Shakespeare’s Globe × International Stage Lab. Children’s and adult groups.',tut='',img=''),
 dict(s='past',type='atolye',d_tr='10–16 Ağustos 2026',d_en='10–16 Aug 2026',t_tr='Prag Film Okulu ile Yaz Okulu',t_en='Summer School with Prague Film School',place_tr='',place_en='',tags_tr=['Yaz okulu','Film'],tags_en=['Summer school','Film'],p_tr='Fikir aşamasından çekim ve kurguya uzanan yoğun bir üretim süreci.',p_en='An intensive production process from idea to shoot and edit.',tut='Diego Fandos, Kaveh Daneshmand',img='w/pfs'),
 dict(s='past',type='atolye',d_tr='4–7 Ağustos 2026',d_en='4–7 Aug 2026',t_tr='LAMDA — Auditioning: Monologue Bootcamp',t_en='LAMDA — Auditioning: Monologue Bootcamp',place_tr='',place_en='',tags_tr=['Seçme hazırlığı'],tags_en=['Audition prep'],p_tr='Seçme süreçlerine hazırlık, monolog çalışması ve self-tape teknikleri.',p_en='Audition preparation, monologue work and self-tape techniques.',tut='Eric Stroud, Katie Meekison',img='w/lamda'),
 dict(s='past',type='atolye',d_tr='27–28 Haziran 2026',d_en='27–28 Jun 2026',t_tr='Anouk van Dijk — Mekânın Görünmez Yakınlığı',t_en='Anouk van Dijk — Intimacy of Space',place_tr='',place_en='',tags_tr=['Countertechnique'],tags_en=['Countertechnique'],p_tr='',p_en='',tut='Anouk van Dijk',img='w/anouk'),
 dict(s='past',type='atolye',d_tr='20–21 Haziran 2026',d_en='20–21 Jun 2026',t_tr='Constanza Macras — Metin ve Hareket Üzerinden Doğaçlama',t_en='Constanza Macras — Improvisation Through Text and Movement',place_tr='',place_en='',tags_tr=['Doğaçlama'],tags_en=['Improvisation'],p_tr='',p_en='',tut='Constanza Macras',img='w/macras'),
 dict(s='past',type='atolye',d_tr='6–9 Haziran 2026',d_en='6–9 Jun 2026',t_tr='Konstantinos Moraitis — Animal Body',t_en='Konstantinos Moraitis — Animal Body',place_tr='',place_en='',tags_tr=['Fiziksel tiyatro'],tags_en=['Physical theatre'],p_tr='',p_en='',tut='Konstantinos Moraitis',img='animal-grup'),
 dict(s='past',type='atolye',d_tr='23–24 Mayıs 2026',d_en='23–24 May 2026',t_tr='Fabian Baumgarten — Familie Flöz Maske Oyunculuğu',t_en='Fabian Baumgarten — Familie Flöz Mask Acting',place_tr='',place_en='',tags_tr=['Maske'],tags_en=['Mask'],p_tr='',p_en='',tut='Fabian Baumgarten',img='floz-maske'),
 dict(s='past',type='atolye',d_tr='16–17 Mayıs 2026',d_en='16–17 May 2026',t_tr='David Penn — The Naked Face',t_en='David Penn — The Naked Face',place_tr='',place_en='',tags_tr=['Kamera önü'],tags_en=['Screen acting'],p_tr='',p_en='',tut='David Penn',img='penn-detay'),
 dict(s='past',type='atolye',d_tr='11–12 Nisan 2026',d_en='11–12 Apr 2026',t_tr='Anne Astolfe — Hareket İçinde Oyun',t_en='Anne Astolfe — Play in Movement',place_tr='',place_en='',tags_tr=['Jacques Lecoq'],tags_en=['Jacques Lecoq'],p_tr='École Internationale de Théâtre Jacques Lecoq iş birliğiyle.',p_en='In collaboration with École Internationale de Théâtre Jacques Lecoq.',tut='Anne Astolfe',img='astolfe'),
 dict(s='past',type='atolye',d_tr='7–8 Şubat 2026',d_en='7–8 Feb 2026',t_tr='Gecko Theatre — Fiziksel Tiyatro ve Devising',t_en='Gecko Theatre — Physical Theatre and Devising',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Fiziksel tiyatro'],tags_en=['Physical theatre'],p_tr='',p_en='',tut='Madeleine Fairminer, Vanessa Guevara Flores',img='w/gecko'),
 dict(s='past',type='atolye',d_tr='24–25 Ocak 2026',d_en='24–25 Jan 2026',t_tr='Donny Beau Ferris — Jasmin Vardimon Dans Atölyesi',t_en='Donny Beau Ferris — Jasmin Vardimon Dance Workshop',place_tr='',place_en='',tags_tr=['Dans tiyatrosu'],tags_en=['Dance theatre'],p_tr='',p_en='',tut='Donny Beau Ferris',img='vardimon'),
 # past workshops 2025
 dict(s='past',type='atolye',d_tr='20–21 Aralık 2025',d_en='20–21 Dec 2025',t_tr='Anthony Meindl — Kamera Önü Oyunculuk',t_en='Anthony Meindl — Acting for Camera',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Kamera önü'],tags_en=['Screen acting'],p_tr='',p_en='',tut='Anthony Meindl',img='w/meindl'),
 dict(s='past',type='atolye',d_tr='8–9 Kasım 2025',d_en='8–9 Nov 2025',t_tr='Claudio de Maglio — Maske ve Beden',t_en='Claudio de Maglio — Mask and Body',place_tr='',place_en='',tags_tr=['Commedia dell’Arte'],tags_en=['Commedia dell’Arte'],p_tr='',p_en='',tut='Claudio de Maglio',img='w/maglio'),
 dict(s='past',type='atolye',d_tr='25–26 Ekim 2025',d_en='25–26 Oct 2025',t_tr='Carolina Pizarro — Sesin Gücü: Beden, Ses ve Duygu',t_en='Carolina Pizarro — The Power of Voice: Body, Voice and Emotion',place_tr='',place_en='',tags_tr=['Ses'],tags_en=['Voice'],p_tr='',p_en='',tut='Carolina Pizarro',img='w/pizarro'),
 dict(s='past',type='atolye',d_tr='30–31 Ağustos 2025',d_en='30–31 Aug 2025',t_tr='Elpida Skourou — Akram Khan Topluluğuyla Hareket Etmek',t_en='Elpida Skourou — Moving with Akram Khan Company',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Dans'],tags_en=['Dance'],p_tr='Ritim, hız ve hikâye.',p_en='Rhythm, speed and story.',tut='Elpida Skourou',img='w/akram'),
 dict(s='past',type='atolye',d_tr='23–24 Ağustos 2025',d_en='23–24 Aug 2025',t_tr='Mermoz Melchior — GAGA Atölyesi',t_en='Mermoz Melchior — GAGA Workshop',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Hareket'],tags_en=['Movement'],p_tr='',p_en='',tut='Mermoz Melchior',img='w/gaga'),
 dict(s='past',type='atolye',d_tr='28–29 Haziran ve 5–7 Aralık 2025',d_en='28–29 Jun and 5–7 Dec 2025',t_tr='David Glass — Sıradışının Simyası',t_en='David Glass — The Alchemy of the Extraordinary',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Devising'],tags_en=['Devising'],p_tr='',p_en='',tut='David Glass',img='w/glass'),
 dict(s='past',type='atolye',d_tr='21–22 Haziran 2025',d_en='21–22 Jun 2025',t_tr='Ruth Lerche — Buffon ve Grotesk Lab',t_en='Ruth Lerche — Buffon and Grotesque Lab',place_tr='İstanbul',place_en='Istanbul',tags_tr=['Buffon'],tags_en=['Buffon'],p_tr='The Commedia School sanat direktörü Ruth Lerche ile.',p_en='With Ruth Lerche, artistic director of The Commedia School.',tut='Ruth Lerche',img='w/lerche'),
 dict(s='past',type='atolye',d_tr='17–18 Mayıs ve 6–7 Eylül 2025',d_en='17–18 May and 6–7 Sep 2025',t_tr='Silvia Farias Heredia — Pina Bausch Lab',t_en='Silvia Farias Heredia — Pina Bausch Lab',place_tr='',place_en='',tags_tr=['Tanztheater'],tags_en=['Tanztheater'],p_tr='Pina Bausch Vakfı iş birliğiyle.',p_en='In collaboration with the Pina Bausch Foundation.',tut='Silvia Farias Heredia',img='w/pina'),
]

L={'tr':dict(back='Ana sayfa',home='../',lang_label='EN',lang_aria='English version',lang_code='en',reg='Başvur',regmsg=' programına kayıt olmak istiyorum',tut='Eğitmenler',
   empty='Bu sekmede henüz program yok.',ph='Görsel yakında',up_h='siradaki',past_h='gecmis',
   atolye=dict(slug='atolyeler',title='Atölyeler — NO Tiyatro',kick='International Stage Lab.',h1='Atölyeler',
     lede='Uluslararası drama okullarının ve sanatçılarının eğitmenleriyle yoğun atölyeler. Sıradaki atölyelere kayıt olabilir, geçmiş atölyelerimize göz atabilirsin.',
     up='Sıradaki atölyeler',past='Geçmiş atölyeler',lang_href='../en/workshops/'),
   kamp=dict(slug='kamplar',title='Kamplar — NO Tiyatro',kick='International Stage Camp',h1='Kamplar',
     lede='Birkaç gün boyunca uluslararası eğitmenlerle birlikte çalışıp birlikte yaşadığımız International Stage Camp edisyonları. Sıradaki kamplara kayıt olabilir, geçmiş kamplarımıza göz atabilirsin.',
     up='Sıradaki kamplar',past='Geçmiş kamplar',lang_href='../en/camps/')),
 'en':dict(back='Home',home='../',lang_label='TR',lang_aria='Türkçe sürüm',lang_code='tr',reg='Apply',regmsg='',tut='Tutors',
   empty='No programmes in this tab yet.',ph='Image coming soon',up_h='upcoming',past_h='past',
   atolye=dict(slug='workshops',title='Workshops — NO Tiyatro',kick='International Stage Lab.',h1='Workshops',
     lede='Intensive workshops with tutors from international drama schools and artists. Register for upcoming workshops or browse our past ones.',
     up='Upcoming workshops',past='Past workshops',lang_href='../../atolyeler/'),
   kamp=dict(slug='camps',title='Camps — NO Tiyatro',kick='International Stage Camp',h1='Camps',
     lede='International Stage Camp editions: a few days of working and living alongside international tutors. Register for upcoming camps or browse our past editions.',
     up='Upcoming camps',past='Past camps',lang_href='../../kamplar/'))}

def build(lang, kind):
    src = tr_idx if lang=='tr' else en_idx
    x=dict(L[lang]); x.update(L[lang][kind])
    head=src[:src.index('</head>')]
    head=re.sub(r'<title>.*?</title>',f'<title>{x["title"]}</title>',head)
    head=re.sub(r'<link rel="alternate".*?\n','',head)
    defs=part(src,'<svg width="0" height="0"','</svg>\n</svg>') if False else None
    i=src.index('<svg width="0" height="0"'); j=src.index('</defs>',i); j=src.index('</svg>',j)+6; defs=src[i:j]
    header=part(src,'<header id="top">','</header>')
    footer=part(src,'<footer class="band" id="iletisim">','</footer>')
    def fix(s):
        s=re.sub(r'(<a\b[^>]*?)href="#([a-z-]+)"',lambda m:m.group(1)+(f'href="{x["home"]}#{m.group(2)}"' if m.group(2)!='top' else 'href="#top"'),s)
        if lang=='tr':
            s=s.replace('href="atolyeler/"','href="../atolyeler/"').replace('href="kamplar/"','href="../kamplar/"')
            s=s.replace('href="en/"',f'href="{x["lang_href"]}"')
            s=s.replace('href="yasal/','href="../yasal/')
        else:
            s=s.replace('href="../"',f'href="{x["lang_href"]}"')
            s=s.replace('href="workshops/"','href="../workshops/"').replace('href="camps/"','href="../camps/"')
            s=s.replace('href="../yasal/','href="../../yasal/')
        s=s.replace('<a class="logo" href="./"','<a class="logo" href="../"')
        return s
    header=fix(header); footer=fix(footer)
    # active nav
    header=header.replace(f'<a href="../{x["slug"]}/">',f'<a href="../{x["slug"]}/" aria-current="page">',1)
    imgp='../img/' if lang=='tr' else '../../img/'
    data=[dict(pid=it.get('pid',''),s=it['s'],type=it['type'],d=it['d_'+lang],t=it['t_'+lang],pl=it['place_'+lang],tags=it['tags_'+lang],p=it['p_'+lang],tut=it['tut'],img=it['img'],f=it.get('f',False)) for it in items]
    css='''
.whero{padding-bottom:12px}
.tabs{display:flex;gap:6px;border-bottom:2px solid #000;margin-top:34px;flex-wrap:wrap}
.tab{appearance:none;background:none;border:0;font:800 18px Urbanist,system-ui,sans-serif;padding:14px 18px;min-height:52px;cursor:pointer;color:#666;border-bottom:4px solid transparent;margin-bottom:-2px}
.tab[aria-selected=true]{color:#000;border-bottom-color:var(--red)}
.tab .n{display:inline-grid;place-items:center;min-width:26px;height:26px;border-radius:999px;background:#eee;font-size:13px;margin-left:8px;padding:0 7px}
.tab[aria-selected=true] .n{background:#000;color:#fff}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 28px;align-items:center}
.chip{appearance:none;border:1.5px solid #000;background:#fff;border-radius:999px;padding:0 16px;min-height:40px;font:700 14px Urbanist,system-ui,sans-serif;cursor:pointer}
.chip[aria-pressed=true]{background:#000;color:#fff}
.wgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 24px}
.wcard{display:flex;flex-direction:column;border-top:2px solid #000;padding-top:16px}
.wimg{aspect-ratio:4/3;border-radius:16px;overflow:hidden;background:#111;margin-bottom:16px;position:relative}
.wimg img{width:100%;height:100%;object-fit:cover;display:block}
.wimg.ph{display:grid;place-items:center}
.wimg.ph img{width:48%;height:auto;object-fit:contain;opacity:.9}
.wimg.ph span{position:absolute;bottom:12px;left:14px;color:#888;font-size:12px;font-weight:700}
.wcard .when{font-weight:900;font-size:16px;color:var(--red)}
.wcard .pl{font-weight:700;font-size:14px;color:#555}
.wcard h3{font-size:22px;margin:6px 0 8px}
.wcard p{font-size:15px;color:#444;margin-bottom:14px}
.wcard .btn{align-self:flex-start;margin-top:auto}
.wtags{margin-bottom:6px}
.stb{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:800;padding:4px 11px 4px 9px;border-radius:999px;margin:0 6px 6px 0;vertical-align:middle;background:#e7f4ea;color:#16632b}
.stb::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.stb.few{background:#fff1d6;color:#8a5300}.stb.full{background:#fde9e6;color:#9b2a18}.stb.closed{background:#eee;color:#555}
.btn.dis{opacity:.45;cursor:not-allowed;pointer-events:none}
.wcard p.tut{font-size:14px;color:#333}
.wempty{padding:40px 0;color:#666}
.wnote{font-size:14px;color:#666;margin-top:34px}
nav.main a[aria-current=page]{background:rgba(0,0,0,.06)}
@media(max-width:980px){.wgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.wgrid{grid-template-columns:1fr}.tab{font-size:16px;padding:12px}}
'''
    head=head.replace('</style>',css+'</style>',1)
    lang_attr=f'<html lang="{lang}">'
    head=re.sub(r'<html lang="[a-z]+">',lang_attr,head)
    js=f'''<script>
{{
  const D={json.dumps(data,ensure_ascii=False)};
  const T={json.dumps(dict(reg=x['reg'],regmsg=x['regmsg'],empty=x['empty'],ph=x['ph'],tut=x['tut']),ensure_ascii=False)};
  const H={json.dumps(dict(up=x['up_h'],past=x['past_h']))}, KIND={json.dumps(kind)};
  const ALIAS={json.dumps({'gelecek':'up','upcoming':'up','siradaki':'up','gecmis':'past','past':'past'})};
  {{const h=location.hash.slice(1); if(KIND==='atolye'&&(h==='kamplar'||h==='camps')) location.replace('../'+(h==='kamplar'?'kamplar':'camps')+'/');}}
  const PAY={json.dumps(PAID)}, PAYU='{'../odeme/' if lang=='tr' else '../payment/'}', PR={json.dumps('Kayıt ol ve öde' if lang=='tr' else 'Register and pay')};
  let ST={{}}; const SL={json.dumps(dict(open='Kayıtlar devam ediyor',few='Son yerler',left='Son {n} yer',full='Kontenjan doldu',closed='Kayıtlar kapandı') if lang=='tr' else dict(open='Registration open',few='Last places',left='Last {n} places',full='Fully booked',closed='Registration closed'),ensure_ascii=False)};
  const IMG='{imgp}', WA='https://wa.me/{WA}?text=';
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
  const fromHash=()=>ALIAS[location.hash.slice(1)]||'up';
  let tab=fromHash();
  const grid=document.getElementById('wgrid');
  const card=w=>{{
    const img=w.img?`<div class="wimg"><img src="${{IMG}}${{w.img}}.jpg" alt="${{esc(w.t)}}" loading="lazy"></div>`
      :`<div class="wimg ph"><img src="${{IMG}}isl-logo.png" alt=""><span>${{esc(T.ph)}}</span></div>`;
    const x=w.s==='up'&&w.pid?ST[w.pid]:null;
    const stb=x?`<span class="stb ${{x.state}}">${{esc(x.state==='few'&&x.left?SL.left.replace('{{n}}',x.left):SL[x.state])}}</span>`:'';
    const tags=`<div class="wtags">${{stb}}${{w.tags.map((g,i)=>`<span class="tag${{w.f&&i===1?' f':''}}">${{esc(g)}}</span>`).join('')}}</div>`;
    const msg={json.dumps(lang)}==='tr'?w.t+T.regmsg:"I'd like to register for "+w.t;
    const btn=w.s!=='up'?'':x&&(x.state==='full'||x.state==='closed')?`<span class="btn solid dis" aria-disabled="true">${{esc(SL[x.state])}}</span>`:`<a class="btn solid" href="{'../basvuru/' if lang=='tr' else '../apply/'}?p=${{w.pid}}">${{esc(T.reg)}}</a>`;
    return `<article class="wcard">${{img}}${{tags}}<div class="when">${{esc(w.d)}}</div>${{w.pl?`<div class="pl">${{esc(w.pl)}}</div>`:''}}<h3>${{esc(w.t)}}</h3>${{w.p?`<p>${{esc(w.p)}}</p>`:''}}${{w.tut?`<p class="tut"><b>${{esc(T.tut)}}:</b> ${{esc(w.tut)}}</p>`:''}}${{btn}}</article>`;
  }};
  const render=()=>{{
    const list=D.filter(w=>w.s===tab&&(KIND==='kamp')===(w.type==='kamp'));
    grid.innerHTML=list.length?list.map(card).join(''):`<p class="wempty">${{esc(T.empty)}}</p>`;
    document.querySelectorAll('.tab').forEach(b=>b.setAttribute('aria-selected',b.dataset.tab===tab));
  }};
  document.querySelectorAll('.tab').forEach(b=>{{
    const t=b.dataset.tab;b.querySelector('.n').textContent=D.filter(w=>w.s===t&&(KIND==='kamp')===(w.type==='kamp')).length;
    b.addEventListener('click',()=>{{tab=b.dataset.tab;history.replaceState(null,'','#'+H[tab]);render()}});
  }});
  addEventListener('hashchange',()=>{{tab=fromHash();render()}});
  render();
  fetch('/api/status').then(r=>r.ok?r.json():{{}}).then(d=>{{ST=d;render()}}).catch(()=>{{}});
  const header=document.getElementById('top'),menu=document.getElementById('menu');
  menu.addEventListener('click',()=>{{const o=header.classList.toggle('open');menu.setAttribute('aria-expanded',o)}});
}}
</script>'''
    body=f'''<body>
{defs}
{header}
<main>
<section class="band whero" aria-labelledby="h-w">
  <div class="wrap">
    <p class="kick2">{x["kick"]}</p>
    <h1 id="h-w">{x["h1"]}</h1>
    <p class="lede" style="margin-top:18px">{x["lede"]}</p>
    <div class="tabs" role="tablist">
      <button class="tab" role="tab" data-tab="up" aria-controls="wgrid">{x["up"]}<span class="n"></span></button>
      <button class="tab" role="tab" data-tab="past" aria-controls="wgrid">{x["past"]}<span class="n"></span></button>
    </div>
    <div style="height:30px"></div>
    <div class="wgrid" id="wgrid" role="tabpanel" aria-live="polite"></div>
  </div>
</section>
</main>
{footer}
{js}
</body>
</html>
'''
    out=head+'</head>\n'+body
    # images in footer/header none; fix any src="img/
    out=out.replace('src="img/','src="'+imgp)
    return out

for lang,kind,path in [('tr','atolye','atolyeler'),('tr','kamp','kamplar'),('en','atolye','en/workshops'),('en','kamp','en/camps')]:
    os.makedirs(f'{ROOT}/{path}',exist_ok=True); open(f'{ROOT}/{path}/index.html','w').write(build(lang,kind))
print('ok')
