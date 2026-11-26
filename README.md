# notiyatro.com

Statik site + Netlify Functions: başvuru formu, onay paneli, IBAN ile ödeme, Tosla İşim Sanal POS ile kartla ödeme.

## Akış
Bilgi → Başvur (/basvuru/) → Panelde onay (/yonetim/) → Kişiye özel ödeme linki (/odeme/?b=...) → Havale/EFT (ve Tosla açıksa kart) → Ödendi.

## Netlify ortam değişkenleri (Site configuration → Environment variables)
Zorunlu:
- ADMIN_PASSWORD — /yonetim/ paneli şifresi (en az 10 karakter)
- IBAN — ödeme sayfasında gösterilecek IBAN
- IBAN_NAME — alıcı adı (varsayılan: NO Yapım ve Organizasyon Ltd. Şti.)
- IBAN_BANK — banka adı (isteğe bağlı)
İsteğe bağlı (otomatik e-posta, resend.com):
- RESEND_API_KEY, MAIL_FROM (ör. NO Tiyatro <hello@notiyatro.com>), ADMIN_EMAIL (yeni başvuru bildirimleri)
Kartla ödeme (Tosla İşim):
- TOSLA_CLIENT_ID, TOSLA_API_USER, TOSLA_API_PASS, TOSLA_ENV (test / live)

## Programlar ve fiyatlar
data/programs.json — priceText (gösterilen fiyat), price (kartla ödeme için KDV dahil tutar), open (başvuru açık/kapalı).
