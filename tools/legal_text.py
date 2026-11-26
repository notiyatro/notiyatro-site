"""Yasal metinler. Katılım sözleşmeleri Serkan Ortaç'ın gönderdiği PDF'lerden alınmıştır
(ISCW-2026 Katılımcı Sözleşmesi = atölye; ISCE Sözleşme = kamp). İade süresi Kasım 2026’dan itibaren
atölye ve kamplar için aynıdır: programdan 45 gün öncesine kadar.
Online kayıt için yapılan değişiklikler: program adı/tarihi ödeme sayfasından gelir,
imza/onay kutuları yerine ödeme sayfasındaki elektronik onay kullanılır."""

SELLER = '''<dl class="lg-firm">
<div><dt>Unvan</dt><dd>NO Yapım ve Organizasyon Limited Şirketi</dd></div>
<div><dt>Adres</dt><dd>Hüseyinağa Mah., İstiklal Cad., Grand Pera No: 56/58 Kat 3 Daire 5, Beyoğlu, İstanbul, Türkiye</dd></div>
<div><dt>Vergi dairesi / no</dt><dd>Beyoğlu / 6311925259</dd></div>
<div><dt>E-posta</dt><dd><a href="mailto:hello@notiyatro.com">hello@notiyatro.com</a></dd></div>
<div><dt>Telefon / WhatsApp</dt><dd>+90 530 480 82 92</dd></div>
</dl>'''

def contract(kind):
    camp = kind == 'kamp'
    days = 45
    ev = 'kamp' if camp else 'atölye'
    Ev = 'Kamp' if camp else 'Atölye'
    return f'''
<p class="lg-meta">Mesafeli hizmet sözleşmesi · Kendi isteğinle iptalde iade süresi: <b>programdan {days} gün öncesine kadar</b></p>
<p>No Yapım ve Organizasyon Limited Şirketi tarafından düzenlenen International Stage Lab. programları, uluslararası sanatçılar ile katılımcılar arasında kültürel ve sanatsal paylaşımı teşvik etmeyi amaçlayan eğitim ve etkileşim programlarıdır. İşbu sözleşme, katılımcının kayıt olduğu programa katılımına ilişkin hak ve yükümlülükleri düzenlemektedir.</p>
<p>İşbu {Ev} Katılım Sözleşmesi, Aydınlatma ve Açık Rıza Metni (“Sözleşme”), katılımcı ile organizasyonu gerçekleştiren No Yapım ve Organizasyon Limited Şirketi (“Organizasyon”) arasında akdedilmiştir. Katılımcı, notiyatro.com üzerindeki kayıt ve ödeme formunu doldurup işbu metni elektronik ortamda onaylamak suretiyle aşağıdaki hüküm ve şartları okuduğunu, anladığını ve kabul ettiğini beyan eder.</p>
<h2>Organizasyon</h2>
{SELLER}
<h2>Katılımcı</h2>
<p>Katılımcının ad-soyad, e-posta ve telefon bilgileri ile kayıt olunan programın adı, tarihleri ve katılım bedeli, notiyatro.com ödeme sayfasında katılımcı tarafından girilen ve gösterilen bilgilerdir. Bu bilgiler sözleşmenin ayrılmaz parçasıdır.</p>
<h2>1. Konu</h2>
<p>İşbu sözleşmenin konusu, katılımcının ödeme sayfasında adı ve tarihleri belirtilen {ev} programına katılımına ilişkin hak, yükümlülük ve koşulların düzenlenmesidir.</p>
<h2>2. Genel katılım koşulları</h2>
<p>2.1. Katılımcı, etkinlik süresince organizasyon tarafından belirlenen kurallara, çalışma disiplinine ve eğitmenlerin yönlendirmelerine uygun davranacağını kabul eder.</p>
<p>2.2. Diğer katılımcıların güvenliğini, çalışma ortamını veya etkinliğin düzenini olumsuz etkileyen davranışlarda bulunulması halinde Organizasyon, herhangi bir tazminat yükümlülüğü doğmaksızın katılımcının etkinlikle ilişiğini sonlandırma hakkını saklı tutar.</p>
<p>2.3. Katılımcı, etkinlik süresince üçüncü kişilerin haklarını ihlal edecek, ayrımcı, saldırgan veya hukuka aykırı davranışlarda bulunmayacağını kabul eder.</p>
<h2>3. Program değişikliği, erteleme ve iptal</h2>
<p>3.1. Organizasyon; eğitmenin sağlık durumu, ulaşım problemleri, vize süreçleri, doğal afet, savaş, salgın hastalık, pandemi, grev, resmi makam kararları, teknik aksaklıklar, mücbir sebepler veya Organizasyonun makul kontrolü dışında gelişen benzeri nedenlerle etkinliğin tarihini değiştirme, erteleme, çevrim içi formata dönüştürme veya iptal etme hakkını saklı tutar.</p>
<p>3.2. Bu gibi durumlarda Organizasyonun sorumluluğu, katılımcı tarafından ödenmiş olan etkinlik katılım bedeli ile sınırlıdır.</p>
<p>3.3. Katılımcı; uçak bileti, konaklama, transfer, vize, sigorta, araç kiralama veya üçüncü kişilerden alınan hizmetlerden kaynaklanan masraf, zarar veya kayıplardan Organizasyonun sorumlu olmadığını kabul eder.</p>
<p>3.4. Organizasyon, gerekli gördüğü takdirde eğitmen, program içeriği, saatler veya etkinlik mekanında değişiklik yapabilir.</p>
<h2>4. Ücret ve iade koşulları</h2>
<p>4.1. Katılımcının kendi isteğiyle kayıt iptalinde bulunması halinde;</p>
<ul><li>Etkinlik başlangıç tarihinden {days} gün veya daha önce yapılan iptallerde, ödenmiş katılım bedelinin tamamı iade edilir.</li>
<li>Etkinlik başlangıç tarihine {days} günden daha az süre kala yapılan iptallerde ücret iadesi yapılmaz.</li>
<li>Etkinlik başlangıç tarihine {days} günden daha az süre kala kayıt yaptıran katılımcı için, kaydın kesinleştiği andan itibaren ücret iadesi hakkı doğmaz. Katılımcı, bu süre içinde kayıt yaptırdığını, iade yapılmayacağı konusunda ödeme öncesinde açıkça bilgilendirildiğini ve kaydını bu koşulu bilerek ve kabul ederek tamamladığını kabul, beyan ve taahhüt eder.</li></ul>
<p>4.1.1. Katılım bedelini ödeyerek kaydını tamamlayan katılımcı, işbu maddede yer alan iptal ve iade koşullarının tamamını okuduğunu, anladığını ve kabul ettiğini beyan eder; kaydın tamamlanması, bu koşulların kabulü anlamına gelir.</p>
<p>4.2. Organizasyon, tamamen kendi takdirine bağlı olarak katılımcıya kredi tanımlayabilir, kayıt hakkını erteleyebilir veya başka bir etkinlikte kullanım imkanı sunabilir.</p>
<p>4.3. Katılımcının hastalık, kaza, aile bireyine refakat zorunluluğu, seyahat engeli veya kendi şahsından kaynaklanan diğer kişisel nedenlerle etkinliğe katılamaması ya da etkinliği yarıda bırakması halinde ücret iadesi talep edilemez. Organizasyon, tamamen kendi takdirine bağlı olarak katılımcıya başka bir etkinlikte kullanılmak üzere kredi tanımlayabilir veya kayıt hakkını erteleyebilir.</p>
<p>4.4. Katılımcının kişisel sebeplerine ilişkin sağlık raporu, belge veya benzeri evrak sunulması Organizasyon açısından ücret iadesi yükümlülüğü doğurmaz.</p>
<p>4.5. İptal talepleri <a href="mailto:hello@notiyatro.com">hello@notiyatro.com</a> adresine yazılı olarak iletilir. İade, ödemenin yapıldığı karta, Tosla İşim (AKÖde Elektronik Para ve Ödeme Hizmetleri A.Ş.) altyapısı üzerinden yapılır; iadenin karta yansıma süresi kartı çıkaran bankaya bağlıdır.</p>
<h2>5. Sağlık ve kişisel sorumluluk</h2>
<p>5.1. Katılımcı, etkinliğe katılmasına engel teşkil eden fiziksel veya psikolojik bir sağlık sorunu bulunmadığını beyan eder.</p>
<p>5.2. Katılımcı, {ev} süresince gerçekleştireceği fiziksel çalışmaların kendi sorumluluğunda olduğunu kabul eder. Etkinlik sırasında meydana gelebilecek kişisel sağlık sorunları, yaralanmalar veya mevcut rahatsızlıkların ağırlaşması nedeniyle Organizasyonun herhangi bir hukuki veya cezai sorumluluğu bulunmadığını katılımcı kabul eder.</p>
<p>5.3. Katılımcı, gerekli görmesi halinde sağlık sigortası yaptırmakla yükümlüdür.</p>
<h2>6. Fotoğraf ve görüntü kullanım izni</h2>
<p>6.1. Katılımcı, etkinlik kapsamında çekilen fotoğraf, ses ve video kayıtlarının; sosyal medya hesaplarında, internet sitelerinde, basılı ve dijital tanıtım materyallerinde, basın çalışmaları ve arşiv faaliyetlerinde herhangi bir süre sınırlaması olmaksızın kullanılabileceğini kabul eder.</p>
<p>6.2. Katılımcı, söz konusu kullanım nedeniyle Organizasyondan herhangi bir ücret, telif veya sair hak talebinde bulunmayacağını kabul eder.</p>
<h2>7. Mücbir sebep</h2>
<p>Doğal afet, yangın, salgın hastalık, savaş, terör eylemleri, ulaşım engelleri, resmi makam kararları, grev, internet ve iletişim altyapısı sorunları ile tarafların kontrolü dışında gelişen benzeri durumlar mücbir sebep olarak kabul edilir. Mücbir sebep halinde Organizasyonun yükümlülükleri askıya alınır ve katılımcı Organizasyondan herhangi bir dolaylı zarar, kar kaybı veya ek masraf talebinde bulunamaz.</p>
<h2>8. Kişisel verilerin korunması</h2>
<p>Kişisel verilerin işlenmesine ilişkin bilgilendirme <a href="../kvkk/">KVKK Aydınlatma Metni</a>'nde yer alır.</p>
<h2>9. Açık rıza</h2>
<p>Kişisel verilerin duyuru, bilgilendirme ve tanıtım amaçlarıyla işlenmesine ve gelecekte düzenlenecek etkinlikler hakkında bilgilendirme yapılmasına ilişkin açık rıza, ödeme sayfasında ayrı ve isteğe bağlı bir onay kutusuyla alınır. Bu onayın verilmemesi kayıt ve katılımı etkilemez; verilen onay her zaman <a href="mailto:hello@notiyatro.com">hello@notiyatro.com</a> adresine yazılarak geri alınabilir.</p>
<h2>10. Uygulanacak hukuk ve yetkili mahkeme</h2>
<p>İşbu sözleşmeden doğabilecek uyuşmazlıklarda Türk Hukuku uygulanır. Tüketici mevzuatından kaynaklanan zorunlu yetki hükümleri saklı kalmak kaydıyla İstanbul Merkez (Çağlayan) Mahkemeleri ve İcra Daireleri yetkilidir.</p>
<h2>11. Onay ve kabul</h2>
<p>Katılımcı, ödeme sayfasındaki onay kutusunu işaretleyerek işbu {Ev} Katılım Sözleşmesi'ni ve <a href="../on-bilgilendirme/">Ön Bilgilendirme Formu</a>'nu okuduğunu, anladığını ve kabul ettiğini beyan eder. 18 yaşından küçük katılımcıların kaydı, yasal temsilcinin onayıyla yapılır; yasal temsilcinin adı ve soyadı Organizasyon tarafından ayrıca istenir.</p>
'''

PREINFO = f'''
<p class="lg-meta">Mesafeli olarak kurulan katılım sözleşmesinden önce okunması gereken bilgiler</p>
<h2>1. Hizmet sağlayıcı</h2>
{SELLER}
<h2>2. Hizmetin konusu ve temel nitelikleri</h2>
<p>NO Tiyatro / International Stage Lab. kapsamında düzenlenen atölye veya kamp programına katılım hizmetidir. Programın adı, tarihleri, yeri ve eğitmenleri ilgili program sayfasında ve ödeme sayfasında gösterilir.</p>
<h2>3. Toplam bedel ve ödeme</h2>
<p>Katılım bedeli, vergiler dahil toplam tutar olarak ödeme sayfasında gösterilir. Ödeme kredi veya banka kartıyla, 3D Secure doğrulamasıyla, AKÖde Elektronik Para ve Ödeme Hizmetleri A.Ş.'nin Tosla İşim Sanal POS altyapısı üzerinden alınır. Kart bilgileri NO Yapım ve Organizasyon Ltd. Şti. tarafından görülmez ve saklanmaz. Taksit seçeneği sunulan programlarda taksit sayısı ödeme sayfasında seçilir.</p>
<h2>4. Hizmetin ifası</h2>
<p>Hizmet, programın ilan edilen tarihlerinde ve yerinde (ya da Organizasyonun duyurduğu çevrim içi formatta) ifa edilir. Kayıt onayı ve program bilgileri katılımcının verdiği e-posta adresine ve/veya telefon numarasına gönderilir.</p>
<h2 id="iptal">5. İptal ve iade koşulları</h2>
<ul>
<li><b>Atölyeler ve kamplar:</b> Programın başlangıç tarihinden 45 gün veya daha önce yapılan iptallerde ödenen bedelin tamamı iade edilir; 45 günden daha az süre kala yapılan iptallerde iade yapılmaz. Başlangıca 45 günden daha az süre kala yapılan kayıtlarda iade hakkı bulunmamaktadır.</li>
</ul>
<p>Ödemeyi yaparak kaydını tamamlayan katılımcı, iptal ve iade koşullarını okumuş ve kabul etmiş sayılır.</p>
<p>Ayrıntılar ve Organizasyon kaynaklı değişiklik, erteleme ve iptal halleri için <a href="../atolye-sozlesmesi/">Atölye Katılım Sözleşmesi</a> ve <a href="../kamp-sozlesmesi/">Kamp Katılım Sözleşmesi</a>'ne bakınız. İptal talepleri <a href="mailto:hello@notiyatro.com">hello@notiyatro.com</a> adresine yazılı olarak iletilir. Cayma hakkına ilişkin hususlarda 6502 sayılı Tüketicinin Korunması Hakkında Kanun ve Mesafeli Sözleşmeler Yönetmeliği hükümleri saklıdır.</p>
<h2>6. Şikâyet ve başvuru</h2>
<p>Talep ve şikâyetler için <a href="mailto:hello@notiyatro.com">hello@notiyatro.com</a> adresine yazabilirsiniz. Tüketiciler, ilgili mevzuatta belirlenen parasal sınırlar dahilinde Tüketici Hakem Heyetlerine veya Tüketici Mahkemelerine başvurabilir.</p>
'''

KVKK = f'''
<p class="lg-meta">6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında aydınlatma metni</p>
<h2>Veri sorumlusu</h2>
{SELLER}
<h2>İşlenen kişisel veriler</h2>
<ul><li>Ad-soyad, telefon numarası, e-posta adresi</li><li>Fatura bilgileri</li><li>Kayıt olunan program, ödeme tutarı ve ödeme durumu (kart bilgileri hariç)</li><li>Etkinlik sırasında alınan görsel ve işitsel kayıtlar</li><li>Katılım bilgileri</li></ul>
<p>Kart numarası, son kullanma tarihi ve güvenlik kodu NO Yapım ve Organizasyon Ltd. Şti. tarafından işlenmez; bu bilgiler doğrudan ödeme kuruluşuna iletilir.</p>
<h2>İşleme amaçları</h2>
<ul><li>Etkinlik organizasyonunun yürütülmesi ve kaydın oluşturulması</li><li>Katılımcı ile iletişim kurulması</li><li>Ödemenin alınması, iade ve faturalandırma süreçlerinin yürütülmesi</li><li>Hukuki yükümlülüklerin yerine getirilmesi</li><li>Açık rıza verilmesi halinde, gelecekte düzenlenecek etkinlikler hakkında bilgilendirme yapılması</li></ul>
<h2>Aktarım</h2>
<p>Kişisel veriler; ödeme işlemleri için AKÖde Elektronik Para ve Ödeme Hizmetleri A.Ş.'ye (Tosla İşim), muhasebe ve faturalandırma için hizmet alınan mali müşavirlik ve e-fatura sağlayıcılarına, internet sitesinin ve kayıt sisteminin barındırılması için hizmet alınan barındırma sağlayıcısına ve yasal zorunluluk halinde yetkili kamu kurumlarına, yukarıdaki amaçlarla sınırlı olarak aktarılabilir.</p>
<h2>Toplama yöntemi ve hukuki sebep</h2>
<p>Veriler, notiyatro.com üzerindeki kayıt ve ödeme formu, e-posta ve WhatsApp yoluyla elektronik ortamda toplanır. Hukuki sebepler: sözleşmenin kurulması ve ifası (KVKK m. 5/2-c), hukuki yükümlülük (m. 5/2-ç), meşru menfaat (m. 5/2-f) ve tanıtım ile bilgilendirme amaçları bakımından açık rıza (m. 5/1).</p>
<h2>Haklarınız</h2>
<p>KVKK'nın 11. maddesi uyarınca kişisel verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, düzeltilmesini veya silinmesini isteme, aktarıldığı üçüncü kişileri öğrenme ve itiraz etme haklarına sahipsiniz. Başvurularınızı <a href="mailto:hello@notiyatro.com">hello@notiyatro.com</a> adresine ya da yukarıdaki adrese yazılı olarak iletebilirsiniz.</p>
'''

PAGES = {
    'atolye-sozlesmesi': ('Atölye Katılım Sözleşmesi', lambda: contract('atolye')),
    'kamp-sozlesmesi': ('Kamp Katılım Sözleşmesi', lambda: contract('kamp')),
    'on-bilgilendirme': ('Ön Bilgilendirme Formu', lambda: PREINFO),
    'kvkk': ('KVKK Aydınlatma Metni', lambda: KVKK),
}
