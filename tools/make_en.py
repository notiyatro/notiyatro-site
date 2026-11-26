import re,sys
from langnorm import norm
src=norm(open('/home/claude/notiyatro/index.html').read())
h=src
from urllib.parse import quote
T=[
('<html lang="tr">','<html lang="en">'),
('content="NO Tiyatro — uluslararası tiyatro atölyeleri, kamplar, yaz okulları, International Stage Lab. ve NO Yapım."','content="NO Tiyatro — international theatre workshops, camps and summer schools, International Stage Lab. and NO Yapım."'),
('<a class="lang" href="en/" hreflang="en" lang="en" aria-label="English version">EN</a>','<a class="lang" href="../" hreflang="tr" lang="tr" aria-label="Türkçe sürüm">TR</a>'),
('<span><a href="en/" hreflang="en" lang="en">English</a> · notiyatro.com</span>','<span><a href="../" hreflang="tr" lang="tr">Türkçe</a> · notiyatro.com</span>'),
('aria-label="NO Tiyatro ana sayfa"','aria-label="NO Tiyatro home"'),
('aria-label="Ana menü"','aria-label="Main menu"'),
('<a href="atolyeler/">Atölyeler</a>','<a href="workshops/">Workshops</a>'),
('<a href="kamplar/">Kamplar</a>','<a href="kamplar/">Camps</a>'),
('>Tüm atölyeler: gelecek ve geçmiş<','>All workshops: upcoming and past<'),
('<a href="#danismanlik">Yurt dışı eğitim</a>','<a href="#danismanlik">Study abroad</a>'),
('<a href="#sertifika">Sertifika doğrulama</a>','<a href="#sertifika">Certificate check</a>'),
('<a href="#iletisim">İletişim</a>','<a href="#iletisim">Contact</a>'),
('>Menü</button>','>Menu</button>'),
('Tiyatro · Atölye · Yapım · Eğitim Danışmanlığı','Theatre · Workshops · Production · Education Consulting'),
('Sahnede, perdede ve hayatın içinde.','On stage, on screen and in life.'),
("2017'den bu yana NO Tiyatro, uluslararası drama okullarının ve sanatçılarının eğitmenleriyle atölyeler, kamplar ve yaz okulları düzenliyor; yapım şirketimiz NO Yapım ile tiyatro ve film prodüksiyonlarına imza atıyor. İstanbul'dan Avrupa'ya uzanan sezon programında sana uygun bir yer var.", 'Since 2017, NO Tiyatro has run workshops, camps and summer schools with tutors from international drama schools and artists, and through our production company NO Yapım we produce theatre and film. There is a place for you in a season that reaches from Istanbul to Europe.'),
('>Atölyeleri keşfet<','>Explore workshops<'),
(">Kampları keşfet<",'>Explore camps<'),
('aria-label="Atölyelerimizden kareler"','aria-label="Moments from our workshops"'),
('alt="Jasmin Vardimon dans atölyesinin katılımcıları siyah sahnede toplu fotoğrafta"','alt="Jasmin Vardimon dance workshop participants in a group photo on a black stage"'),
('>Jasmin Vardimon dans atölyesi · Ocak 2026<','>Jasmin Vardimon dance workshop · January 2026<'),
('alt="LAMDA atölyesinde katılımcılar yarım daire oturmuş eğitmeni dinliyor"','alt="Participants seated in a semicircle listening to the tutor at the LAMDA workshop"'),
('>LAMDA Audition Bootcamp · Ağustos 2026<','>LAMDA Audition Bootcamp · August 2026<'),
('alt="Konstantinos Moraitis stüdyoda havada sıçrarken"','alt="Konstantinos Moraitis leaping mid-air in the studio"'),
('>Animal Body · Haziran 2026<','>Animal Body · June 2026<'),
('alt="Lecoq tekniği atölyesinde gülerek hareket eden katılımcılar"','alt="Participants laughing as they move in a Lecoq technique workshop"'),
('>École Jacques Lecoq · Nisan 2026<','>École Jacques Lecoq · April 2026<'),
('alt="David Penn tuğla duvarlı stüdyoda katılımcılarla çalışıyor"','alt="David Penn working with participants in a brick-walled studio"'),
('>David Penn · The Naked Face · Mayıs 2026<','>David Penn · The Naked Face · May 2026<'),
('aria-label="Önceki fotoğraf"','aria-label="Previous photo"'),
('aria-label="Sonraki fotoğraf"','aria-label="Next photo"'),
('<span>Instagram takipçisi</span>','<span>Instagram followers</span>'),
('<b>177B+</b>','<b>177K+</b>'),
('<span>aylık sosyal medya görüntülenmesi</span>','<span>monthly social media views</span>'),
('<b>5B+</b><span>atölye katılımcısı</span>','<b>5K+</b><span>workshop participants</span>'),
('<span>uluslararası program</span>','<span>international programmes</span>'),
('<span>uluslararası kamp</span>','<span>international camps</span>'),

('2026–2027 sezonu','2026–2027 season'),
('Dünyanın önde gelen drama okullarından ve sahnelerinden eğitmenlerle kısa, yoğun atölyeler ve kamplar. Her program sınırlı kontenjanla açılır; gençler ve yetişkinler için ayrı gruplar oluşturulabilir.','Short, intensive workshops and camps with tutors from the world’s leading drama schools and stages. Every programme opens with limited places; separate groups may be formed for young people and adults.'),
('>Tüm duyurular için WhatsApp kanalına katıl<','>Join our WhatsApp channel for all announcements<'),
('Bu programlar International Stage Lab. tarafından, NO Tiyatro ve Vajra Theatre iş birliğiyle, ilgili okul ve sanatçıların eğitmenleriyle düzenlenir. Atölye ve kamplarda başlangıca 45 günden az süre kala yapılan iptallerde iade yapılmaz; ayrıntılar kayıt sözleşmesindedir.',
 'These programmes are run by International Stage Lab., a collaboration between NO Tiyatro and Vajra Theatre, with tutors from the schools and artists named. Cancellations made less than 45 days before the start of a workshop or camp are not refunded; full terms are in the registration contract.'),
('Bütün sezon tek bilet.','One ticket for the whole season.'),
("Premium Pass ile 31 Ağustos 2027'ye kadar duyurulan bütün atölyelere katıl, bir kampı da hediye al. Sezonu baştan sona takip etmek isteyenler için.","With the Premium Pass you can join every workshop announced until 31 August 2027, plus one camp free. For those who want to follow the whole season."),
('>Sezon bileti<','>Season ticket<'),
("<li>31 Ağustos 2027'ye kadar duyurulan tüm atölyeler</li>","<li>Every workshop announced until 31 August 2027</li>"),
('<li>1 International Stage Camp ücretsiz</li>','<li>One International Stage Camp free</li>'),
('<li>Duyurulara öncelikli erişim</li>','<li>Early access to announcements</li>'),
('?text=Premium%20Pass%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum','?text='+quote("I'd like to know more about the Premium Pass")),
('>Bilgi al<','>Ask about it<'),
('İki çatı, tek sahne','Two houses, one stage'),
('>Vajra Theatre iş birliğiyle<','>In collaboration with Vajra Theatre<'),
("Uluslararası drama okullarının ve sanatçılarının eğitmenleriyle Türkiye'de ve Avrupa'da atölyeler, International Stage Camp ve yaz okulları. Katılımcılara sertifika verilir.","Workshops, International Stage Camp and summer schools in Türkiye and Europe with tutors from international drama schools and artists. Participants receive a certificate."),
('<li>Atölyeler</li><li>Kamplar</li><li>Yaz okulları</li><li>Yurt dışı eğitim danışmanlığı</li>','<li>Workshops</li><li>Camps</li><li>Summer schools</li><li>Study abroad consulting</li>'),
('ISL programlarına git','See ISL programmes'),
("Oyunlarımızı gör","See our plays"),
('<li>Tiyatro</li><li>Film</li><li>Organizasyon</li><li>Marka iş birlikleri</li>','<li>Theatre</li><li>Film</li><li>Events</li><li>Brand partnerships</li>'),
('>NO Yapım oyunları<','>NO Yapım plays<'),
('>Prodüksiyonlarımız<','>Our productions<'),
('NO çatısı altındaki yapım şirketimiz NO Yapım, tiyatro ve film prodüksiyonları üretir. Yapımcısı ya da yürütücü yapımcısı olduğu oyunlar:', 'NO Yapım, our production company under the NO umbrella, creates theatre and film productions. Plays it has produced or executive-produced:'),
('<dt>Yazar</dt>','<dt>Writer</dt>'),
('<dt>Yönetmen</dt>','<dt>Director</dt>'),
('<dt>Oyuncular</dt>','<dt>Cast</dt>'),
('<dt>Oyuncu</dt>','<dt>Cast</dt>'),
(' oyun afişi"',' play poster"'),
('>Tiyatro ve film prodüksiyonları<','>Theatre and film productions<'),
('NO Yapım, tiyatro ve film prodüksiyonları üreten yapım şirketimiz. <i>Başka Hayat</i> ve <i>Küçük Balkon</i> gibi oyunların yapımcısıyız; organizasyon ve marka iş birliği projeleri de üretiyoruz.','NO Yapım is our theatre and film production company. We produced plays such as <i>Başka Hayat</i> and <i>Küçük Balkon</i>, and we also create events and brand partnership projects.'),
('aria-label="Vajra Theatre logosu"','aria-label="Vajra Theatre logo"'),
('<summary>Vajra Theatre hakkında</summary>','<summary>About Vajra Theatre</summary>'),
("Vajra Theatre, Karen Yazel Yivli tarafından Ocak 2025'te kurulan bağımsız bir sahne sanatları girişimidir. 2023 yılında Ankara Üniversitesi Dil ve Tarih-Coğrafya Fakültesi Tiyatro Bölümü Oyunculuk programından mezun olan Karen Yazel Yivli, mezuniyetinden bu yana İngiltere, İtalya ve Türkiye'de katıldığı uluslararası festivaller ve eğitim programlarıyla sahne pratiğini uluslararası bir zeminde geliştirmektedir.",'Vajra Theatre is an independent performing arts initiative founded by Karen Yazel Yivli in January 2025. Karen Yazel Yivli graduated in Acting from the Theatre Department of Ankara University’s Faculty of Languages, History and Geography in 2023, and has since developed her stage practice internationally through festivals and training programmes in the UK, Italy and Türkiye.'),
("Vajra Theatre'ın yıllık eğitim programı, Türkiye'den Avrupa'ya oyuncu, yönetmen ve sahne sanatçılarının gerçek ihtiyaçlarının tespitine dayanır. Her atölyenin içeriği, davet edilen eğitmenle birlikte bu ihtiyaçlara göre kurgulanır.",'Vajra Theatre’s annual training programme is built on the real needs of actors, directors and performers from Türkiye to Europe. Each workshop is designed with the invited tutor around those needs.'),
("Uzun vadeli hedef, eğitimden üretime uzanan kalıcı bir yapı kurmaktır: uluslararası ölçekte tiyatro projeleri ve oyunlar üretmek, kendi yazar ve yönetmenlerini yetiştirmek, kurulan uluslararası bağlantılarla Türkiye'de ve Avrupa'da yaratıcı çalışmalar ortaya koymak. Vajra Theatre, atölye organizasyonunun ötesinde sahne sanatlarında üretken, öğrenen ve paylaşan bir topluluk oluşturmayı amaçlar.",'Its long-term aim is a lasting structure that runs from training to production: creating theatre projects and plays on an international scale, nurturing its own writers and directors, and using its international connections to make creative work in Türkiye and across Europe. Beyond organising workshops, Vajra Theatre aims to build a performing arts community that creates, learns and shares.'),
('>Program ortağımız<','>Programme partner<'),
("International Stage Lab. (ISL), NO Tiyatro ve Vajra Theatre'ın birlikte yürüttüğü ortak bir programdır. İki kurum, uluslararası drama okullarından eğitmenleri ve sanatçıları Türkiye'den Avrupa'ya uzanan bir ağda sahne sanatçılarıyla bir araya getirir; atölyeleri, kampları ve yaz okullarını birlikte tasarlayıp hayata geçirir.", 'International Stage Lab. (ISL) is a joint programme run by NO Tiyatro and Vajra Theatre. Together, the two organisations bring tutors and artists from international drama schools together with performers across a network that reaches from Türkiye to Europe, designing and delivering workshops, camps and summer schools side by side.'),
('<li>Programların ortak tasarımı</li><li>Uluslararası eğitmen ilişkileri</li><li>Atölye ve kamp yürütücülüğü</li>','<li>Co-designed programmes</li><li>International tutor relations</li><li>Workshop and camp delivery</li>'),
('Yurt dışında drama eğitimi','Studying drama abroad'),
("Atölyelerimize katılan pek çok genç, İngiltere başta olmak üzere yurt dışında tiyatro okumak istiyor. Bu yolculuk için okul seçiminden seçmelere kadar yanında olacak bir danışmanlık hizmeti hazırlıyoruz.","Many young people in our workshops want to study theatre abroad, especially in the UK. We are preparing a consulting service to support them from choosing a school to the auditions."),
('?text=Yurt%20d%C4%B1%C5%9F%C4%B1%20e%C4%9Fitim%20dan%C4%B1%C5%9Fmanl%C4%B1%C4%9F%C4%B1%20i%C3%A7in%20bekleme%20listesine%20yaz%C4%B1lmak%20istiyorum','?text='+quote("I'd like to join the waiting list for study abroad consulting")),
('>Bekleme listesine yazıl<','>Join the waiting list<'),
('<b>Tanışma görüşmesi</b><span>Hedeflerini, yaşını ve deneyimini konuşuruz.</span>','<b>First conversation</b><span>We talk about your goals, age and experience.</span>'),
('<b>Okul ve program seçimi</b><span>Lisans, foundation ya da kısa programlar arasından sana uygun olanları belirleriz.</span>','<b>Choosing schools and courses</b><span>We find the right fit among degree, foundation and short courses.</span>'),
('<b>Seçme hazırlığı</b><span>Monolog seçimi ve prova süreci için atölyelerimizle birlikte çalışırız.</span>','<b>Audition preparation</b><span>We work on monologue choice and rehearsal alongside our workshops.</span>'),
('<b>Başvuru takvimi</b><span>Son tarihleri ve belgeleri birlikte takip ederiz.</span>','<b>Application timeline</b><span>We keep track of deadlines and documents together.</span>'),
('>Daha fazlası<','>More from us<'),
('<h3>WhatsApp kanalı</h3><p>İş ilanları, bilet paylaşımları ve atölye duyuruları tek yerde. Binlerce tiyatrosever burada.</p>','<h3>WhatsApp channel</h3><p>Job listings, ticket sharing and workshop announcements in one place, followed by thousands of theatre lovers.</p>'),
('>Kanala katıl<','>Join the channel<'),
('<p><b>@notiyatro</b>, 177 binden fazla takipçisiyle Türkiye’nin en büyük kültür-sanat sayfalarından biri. Atölyelerden kareler, sahne arkası, tiyatro prodüksiyonlarımız ve sanat gündemiyle bir medya platformu olarak yayın yapıyor. Atölye duyuruları <b>@internationalstagelab</b>, program ortağımız <b>@vajra.theatre</b> hesabında.</p>', '<p><b>@notiyatro</b> is one of Türkiye’s largest culture and arts pages, with more than 177,000 followers. It works as a media platform: moments from our workshops, behind the scenes, our theatre productions and arts news. Workshop announcements are on <b>@internationalstagelab</b>, and our programme partner is <b>@vajra.theatre</b>.</p>'),
('<p>Atölye videoları ve eğitmen söyleşileri için NO Tiyatro YouTube kanalı yakında.</p>','<p>Workshop videos and tutor interviews are coming soon to the NO Tiyatro YouTube channel.</p>'),
('>Kanala göz at<','>Visit the channel<'),
('>Sertifika doğrulama<','>Certificate check<'),
('ISL programlarından aldığın katılım sertifikasının üzerindeki kodu girerek geçerliliğini kontrol edebilirsin.','Enter the code on your ISL participation certificate to check that it is valid.'),
('>Sertifika kodu<','>Certificate code<'),
('placeholder="Örn. ISL-2026-GLB-0142"','placeholder="e.g. ISL-2026-GLB-0142"'),
('>Doğrula<','>Check<'),
('<h4>İletişim</h4>','<h4>Contact</h4>'),
('<h4>Keşfet</h4>','<h4>Explore</h4>'),
('<h4>Takip et</h4>','<h4>Follow</h4>'),
('>WhatsApp kanalı<','>WhatsApp channel<'),
('Hüseyinağa Mah., İstiklal Cad., Grand Pera No: 56/58 Kat 3 Daire 5, Beyoğlu, İstanbul','Hüseyinağa Mah., İstiklal Cad., Grand Pera No: 56/58, Floor 3, Flat 5, Beyoğlu, Istanbul, Türkiye'),
# script
(open('/home/claude/build/season_tr.txt').read(), open('/home/claude/build/season_en.txt').read()),
('<h4>Sözleşmeler</h4>','<h4>Terms</h4>'),
('>Atölye Katılım Sözleşmesi</a>','>Workshop Participation Agreement</a>'),
('>Kamp Katılım Sözleşmesi</a>','>Camp Participation Agreement</a>'),
('>Ön Bilgilendirme Formu</a>','>Pre-Information Form</a>'),
('>İptal ve İade Koşulları</a>','>Cancellation &amp; Refunds</a>'),
('>KVKK Aydınlatma Metni</a>','>Privacy Notice (KVKK)</a>'),
("const APPLY = 'basvuru/';","const APPLY = 'apply/';"),
("const PAYURL = 'odeme/';","const PAYURL = 'payment/';"),
('aria-label="Fotoğraf ${i+1}"','aria-label="Photo ${i+1}"'),
("'Doğrulama sistemi çok yakında burada olacak. Şimdilik kodunu hello@notiyatro.com adresine gönderebilirsin.'","'Online verification is coming soon. For now, please send your code to hello@notiyatro.com.'"),
("'Lütfen sertifikanın üzerindeki kodu gir.'","'Please enter the code shown on your certificate.'"),
]
for a,b in T:
    if a not in h:
        print('MISSING:',a[:90]); sys.exit(1)
    h=h.replace(a,b)
# paths
h=h.replace('src="img/','src="../img/')
h=h.replace('href="yasal/','href="../yasal/')
h=h.replace('data-full="img/','data-full="../img/')
h=h.replace('href="atolyeler/"','href="workshops/"')
h=h.replace('href="kamplar/"','href="camps/"')
# leftover Turkish check (outside address & names)
body=re.sub(r'<svg.*?</svg>','',h,flags=re.S)
txt=re.sub(r'<[^>]+>',' ',body)
for line in txt.splitlines():
    if re.search(r'[ğışĞİŞ]|Ö|ü|ö|ç',line) and not re.search(r'Hüseyinağa|Narköy|Çeşmeköy|Flöz|Türkiye|Türkçe|Beyoğlu|İstiklal|Yazel Yivli|Yivli|Başka Hayat|Küçük Balkon|Kılcıoğlu|Ankara|Gülbeyaz|Gürkan|Öngören|Taşçı|Yağcı|Ünal|Çınar|NO Yapım|Şirketi|Sürüm|sürüm|yapım|Türk',line):
        print('TR?',line.strip()[:120])
import os
os.makedirs('/home/claude/notiyatro/en',exist_ok=True)
open('/home/claude/notiyatro/en/index.html','w').write(h)
print('written')
