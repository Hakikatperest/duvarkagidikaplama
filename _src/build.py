# -*- coding: utf-8 -*-
"""
duvarkagidikaplama.com — statik site üreticisi.

    python3 _src/build.py

⛔ Üretilen HTML dosyalarını ELLE DÜZENLEME. Her çalıştırmada üzerine yazılır;
düzeltme buraya ya da data.py'ye yapılır. (yanimdaevdesaglik ve seyrannakliyat
ile aynı düzen.)

Sayfa tipleri: anasayfa · 39 ilçe · 17 kullanım alanı · 6 rehber.
"""
import html
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D  # noqa: E402

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = D.SITE


def e(t):
    return html.escape(str(t), quote=True)


def tl(n):
    return f"{n:,.0f}".replace(",", ".") + " ₺"


# ── Ortak parçalar ──────────────────────────────────────────────────────────

def gorsel(taban, alt, sinif="", boy="(min-width:1000px) 560px, 100vw", oncelik=False):
    """srcset'li görsel. Kaynaklar 2 MB; sayfaya hep türevler girer."""
    yukleme = 'loading="eager" fetchpriority="high"' if oncelik else 'loading="lazy" decoding="async"'
    return (f'<img src="/assets/img/{taban}-900.webp" '
            f'srcset="/assets/img/{taban}-500.webp 500w, /assets/img/{taban}-900.webp 900w'
            + (f', /assets/img/{taban}-1600.webp 1600w' if os.path.exists(os.path.join(KOK, "assets", "img", f"{taban}-1600.webp")) else '')
            + f'" sizes="{boy}" alt="{e(alt)}" class="{sinif}" width="900" height="600" {yukleme}>')


def tel_btn(sinif="btn btn-altin", metin=None):
    return (f'<a class="{sinif}" href="tel:{S["tel_link"]}">'
            f'<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 '
            f'2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.1a2 2 0 0 1 '
            f'2.1-.5c.9.3 1.9.6 2.9.7A2 2 0 0 1 22 16.9z"/></svg>'
            f'{metin or S["tel"]}</a>')


def wa_btn(mesaj="Merhaba, duvar kağıdı kaplama için bilgi almak istiyorum.", sinif="btn btn-wa"):
    m = mesaj.replace(" ", "%20").replace(",", "%2C")
    return (f'<a class="{sinif}" href="https://wa.me/{S["wa"]}?text={m}" rel="nofollow noopener" target="_blank">'
            f'<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
            f'<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.8 14.2c-.2.7-1.2 1.3-1.9 1.4-.5.1-1.1.1-1.8-.1'
            f'-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.5-1.2-2.9s.7-2 1-2.3c.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 2'
            f'c.1.2.1.3 0 .5l-.4.5-.3.3c-.1.1-.2.3 0 .5.2.3.8 1.3 1.7 2.1 1.1 1 2 1.3 2.3 1.4.2.1.4.1.5-.1l.8-.9c.2-.2.3-.2.5-.1'
            f'l1.9.9c.2.1.4.2.4.3.1.1.1.6-.1 1.5z"/></svg>WhatsApp</a>')


def head(baslik, aciklama, yol, gorsel_taban="duvar-kagidi-kaplama", schema=""):
    kanonik = S["alan"] + yol
    og = f'{S["alan"]}/assets/img/{gorsel_taban}-1600.webp' if os.path.exists(
        os.path.join(KOK, "assets", "img", f"{gorsel_taban}-1600.webp")
    ) else f'{S["alan"]}/assets/img/{gorsel_taban}-900.webp'
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(baslik)}</title>
<meta name="description" content="{e(aciklama)}">
<link rel="canonical" href="{kanonik}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0d1826">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{e(S["ad"])}">
<meta property="og:title" content="{e(baslik)}">
<meta property="og:description" content="{e(aciklama)}">
<meta property="og:url" content="{kanonik}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/duvarkagidikaplama-500.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap">
<link rel="stylesheet" href="/assets/style.css">
{schema}
</head>
<body>'''


def ust_header(aktif=""):
    m = [("/", "Ana Sayfa"), ("/duvar-kagidi-fiyatlari/", "Fiyatlar"),
         ("/duvar-kagidi-cesitleri/", "Çeşitler"), ("/duvar-kagidi-kaplama-nedir/", "Rehber"),
         ("/#hizmet-bolgeleri", "Hizmet Bölgeleri"), ("/#iletisim", "İletişim")]
    baglar = "".join(f'<a href="{u}">{e(a)}</a>' for u, a in m)
    return f'''
<div class="ust"><div class="kap">
  <span>📍 <b>İstanbul'un 39 ilçesinde</b> yerinde uygulama</span>
  <span>📐 <b>Ücretsiz keşif</b> ve yazılı fiyat</span>
  <span>🧾 Fiyatlar rulo bazında, <b>net</b></span>
</div></div>
<header><div class="kap">
  <a class="logo" href="/" aria-label="{e(S["ad"])} ana sayfa">
    <img src="/assets/img/duvarkagidikaplama-500.webp" alt="{e(S["ad"])} logosu" width="120" height="43">
  </a>
  <button class="mnu" aria-label="Menü" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="ana">{baglar}{tel_btn("btn btn-altin btn-sm")}</nav>
</div></header>'''


def kirinti(parcalar):
    """parcalar: [(url|None, ad)] — son eleman linksiz."""
    ic = []
    for i, (u, a) in enumerate(parcalar):
        ic.append(f'<a href="{u}">{e(a)}</a>' if u else f'<span aria-current="page">{e(a)}</span>')
    return '<div class="kap"><div class="kirinti">' + '<span>›</span>'.join(ic) + '</div></div>'


def guven_seridi():
    ikon = {
        "kalkan": '<path d="M12 2 4 6v6c0 5 3.4 9.4 8 10 4.6-.6 8-5 8-10V6l-8-4z"/><path d="m9 12 2 2 4-4"/>',
        "kisi": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
        "bas": '<path d="M7 11v9H3v-9h4z"/><path d="M7 11l4-8a2.5 2.5 0 0 1 3 3l-1 5h5a2 2 0 0 1 2 2.4l-1.3 6A2 2 0 0 1 16.7 21H7"/>',
        "ev": '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-9.5z"/><path d="M12 16c-2-1.4-3-2.4-3-3.5a1.6 1.6 0 0 1 3-.8 1.6 1.6 0 0 1 3 .8c0 1.1-1 2.1-3 3.5z"/>',
    }
    ogeler = [("kalkan", "Kaliteli Malzeme"), ("kisi", "Uzman Ekip"),
              ("bas", "Titiz İşçilik"), ("ev", "%100 Müşteri Memnuniyeti")]
    ic = "".join(
        f'<div class="g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ikon[k]}</svg>{e(a)}</div>'
        for k, a in ogeler)
    return f'<div class="guven"><div class="kap">{ic}</div></div>'


def fiyat_tablosu(baslik="Güncel Fiyat Listesi", alt=None):
    kartlar = []
    for g in D.FIYATLAR:
        satirlar = "".join(
            f'<div class="fsatir"><div class="ad">{e(ad)}</div>'
            f'<div class="tutar">{e(tutar)}</div><div class="aciklama">{e(acik)}</div></div>'
            for ad, tutar, acik in g["kalemler"])
        kartlar.append(f'<div class="fkart"><div class="fbas"><h3>{e(g["grup"])}</h3></div>'
                       f'<div class="fgovde">{satirlar}</div></div>')
    altyazi = alt or (f'{D.FIYAT_GUNCELLEME} itibarıyla geçerli fiyatlar. '
                      f'1 rulo duvar kağıdı {str(D.RULO_M2).replace(".", ",")} m²\'ye kadar alan kaplar, '
                      f'rulo genişliği {D.RULO_EN_CM} cm.')
    maddeler = "".join(f"<li>{e(m)}</li>" for m in D.FIYAT_MADDELER)
    return f'''<div class="bolum-bas">
  <span class="etiket">Fiyat Listesi</span>
  <h2>{e(baslik)}</h2>
  <p>{e(altyazi)}</p>
</div>
<div class="fiyatlar gel">{"".join(kartlar)}</div>
<div class="fiyat-not gel">
  <strong>Fiyatlar hakkında</strong>
  <ul style="margin:10px 0 0;padding-left:1.2em">{maddeler}</ul>
</div>


def hesaplayici():
    return f'''<div class="hesap gel">
  <h3>Kaç rulo gider, ne kadar tutar?</h3>
  <p style="color:#c3d0e0;margin-bottom:0">Kaplatmak istediğiniz duvarın enini ve yüksekliğini yazın —
  gereken rulo sayısını ve yaklaşık tutarı anında görün.</p>
  <form id="hesapForm" data-rulo-m2="{D.RULO_M2}" data-rulo-satis="{D.RULO_SATIS}"
        data-rulo-iscilik="{D.RULO_ISCILIK}" data-tavan-satis="{D.TAVAN_SATIS}"
        data-tavan-iscilik="{D.TAVAN_ISCILIK}" onsubmit="return false">
    <div class="hesap-form">
      <div><label for="en">Duvar eni (metre)</label>
        <input id="en" name="en" type="number" min="0" step="0.1" value="4" inputmode="decimal"></div>
      <div><label for="yukseklik">Yükseklik (metre)</label>
        <input id="yukseklik" name="yukseklik" type="number" min="0" step="0.1" value="2.7" inputmode="decimal"></div>
      <div><label for="tur">Ürün</label>
        <select id="tur" name="tur">
          <option value="duvar">Duvar kağıdı</option>
          <option value="tavan">Tavan duvar kağıdı</option>
          <option value="poster">Dijital özel baskı poster</option>
          <!-- poster: sabit m² fiyatı YOK, keşifle belirlenir (JS ayrı mesaj basar) -->
        </select></div>
    </div>
    <div class="hesap-sonuc" id="hesapSonuc">
      <div class="satir"><span>Gereken miktar</span><b id="sonucAdet">—</b></div>
      <div class="satir"><span>Ürün bedeli</span><b id="sonucUrun">—</b></div>
      <div class="satir"><span>İşçilik</span><b id="sonucIscilik">—</b></div>
      <div class="satir toplam"><span>Yaklaşık toplam</span><b id="sonucToplam">—</b></div>
    </div>
    <div class="hesap-sonuc" id="posterNot" hidden>
      <p style="margin:0;color:#e6c96b;font-weight:700">Dijital özel baskı, özel tasarım ve ölçüye göre fiyatlandırılır.</p>
      <p style="margin:8px 0 0;color:#c9d6e6;font-size:15px">Ölçünüzü ve kullanmak istediğiniz görseli
      konuşalım; ücretsiz keşifte çözünürlüğü kontrol edip net fiyatı yazılı vereyim.</p>
    </div>
    <p class="hesap-not">Rulo sayısı yukarı yuvarlanır; yarım rulo satılmaz. Desen raporu olan
    ürünlerde kesim firesi rulo sayısını bir artırabilir. Net rakam için ücretsiz keşif isteyin.</p>
  </form>
  <div style="display:flex;gap:11px;flex-wrap:wrap;margin-top:18px">
    {tel_btn("btn btn-altin", "Hemen Ara: " + S["tel"])}{wa_btn()}
  </div>
</div>'''


def galeri(baslik="Duvar Kağıdı Modelleri"):
    modeller = [(f"model-duvarkagidi{i}", ad) for i, ad in enumerate(
        ["Salon için desenli duvar kağıdı", "Yatak odası duvar kağıdı modeli",
         "Modern geometrik duvar kağıdı", "Doğal doku duvar kağıdı",
         "Çiçek desenli duvar kağıdı", "Klasik desen duvar kağıdı",
         "3D görünümlü duvar kağıdı"], start=1)]
    mevcut = [(t, a) for t, a in modeller if os.path.exists(os.path.join(KOK, "assets", "img", f"{t}-500.webp"))]
    ic = "".join(f'<figure>{gorsel(t, a, boy="(min-width:820px) 270px, 45vw")}'
                 f'<figcaption>{e(a)}</figcaption></figure>' for t, a in mevcut)
    return f'''<div class="bolum-bas"><span class="etiket">Modeller</span><h2>{e(baslik)}</h2>
  <p>Binlerce desen arasından mekânınıza uyanı birlikte seçiyoruz. Kataloğun tamamını keşifte gösteriyorum.</p></div>
<div class="galeri gel">{ic}</div>'''


def sss_bolum(sorular, baslik="Sık Sorulan Sorular"):
    ic = "".join(f'<details><summary>{e(s)}</summary><div class="cevap">{c}</div></details>'
                 for s, c in sorular)
    return f'<div class="bolum-bas"><span class="etiket">SSS</span><h2>{e(baslik)}</h2></div><div class="sss gel">{ic}</div>'


def sss_schema(sorular):
    import json
    d = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": s,
         "acceptedAnswer": {"@type": "Answer", "text": html.unescape(
             c.replace("<p>", "").replace("</p>", " ").replace("<strong>", "").replace("</strong>", "")).strip()}}
        for s, c in sorular]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def cta_band(baslik, metin):
    return f'''<div class="cta gel" id="iletisim">
  <h2>{e(baslik)}</h2><p>{e(metin)}</p>
  <div class="dugmeler">{tel_btn("btn btn-altin", S["tel"])}{wa_btn()}</div>
</div>'''


def sabit_ara():
    return f'''<div class="sabit-ara">{tel_btn("btn btn-altin", "Hemen Ara")}{wa_btn(sinif="btn btn-wa")}</div>'''


def alt_bilgi():
    ilce_link = "".join(f'<li><a href="/{i["slug"]}-duvar-kagidi-kaplama/">{e(i["ad"])}</a></li>'
                        for i in D.ILCELER[:10])
    alan_link = "".join(f'<li><a href="/{a["slug"]}/">{e(a["ad"])}</a></li>' for a in D.ALANLAR[:8])
    rehber_link = "".join(f'<li><a href="/{r["slug"]}/">{e(r["ad"])}</a></li>' for r in D.REHBERLER)
    return f'''<footer>
  <div class="kap">
    <div class="fust">
      <div>
        <h4>{e(S["marka"])}</h4>
        <p style="font-size:14.5px">{e(S["aciklama"])}</p>
        <p style="margin-bottom:6px"><a href="tel:{S["tel_link"]}" style="color:#e6c96b;font-weight:800;font-size:19px">{e(S["tel"])}</a></p>
        <p style="font-size:14px">İstanbul geneli · Ücretsiz keşif</p>
      </div>
      <div><h4>Hizmet Bölgeleri</h4><ul>{ilce_link}
        <li><a href="/#hizmet-bolgeleri"><strong>Tüm 39 ilçe →</strong></a></li></ul></div>
      <div><h4>Kullanım Alanları</h4><ul>{alan_link}</ul></div>
      <div><h4>Rehber</h4><ul>{rehber_link}</ul></div>
    </div>
    <div class="falt">
      <span>© 2026 {e(S["ad"])} · Tüm hakları saklıdır.</span>
      <span class="w4">Tasarım <a href="https://www.web4medya.com" target="_blank" rel="noopener">Web4Medya</a></span>
    </div>
  </div>
</footer>
{sabit_ara()}
<script src="/assets/app.js" defer></script>
</body></html>'''


# ── Anasayfa ────────────────────────────────────────────────────────────────

ANA_SSS = [
    ("Duvar kağıdı kaplama ne kadar sürer?",
     "<p>Tek duvar işi çoğu zaman 2-3 saatte biter. Bir odanın tamamı yarım gün, "
      "salon + koridor gibi geniş alanlar tam gün sürer. Duvarda düzeltme gerekiyorsa "
      "(çatlak, eski kağıt sökümü, alçı tamiri) bir gün de ona gider. Keşifte bunu "
      "baştan söylerim; işi başladıktan sonra 'bir gün daha lazım' demem.</p>"),
    ("1 rulo duvar kağıdı kaç m² kaplar?",
     f"<p>1 rulo {str(D.RULO_M2).replace('.', ',')} m² alan kaplar, rulo genişliği {D.RULO_EN_CM} cm'dir. "
      "Ama bu teorik rakam: desenli ürünlerde kesim firesi çıkar, tavanı yüksek odalarda "
      "her şeritten artan parça kullanılamaz. Pratikte 4 metre eninde ve 2,7 metre yüksekliğinde "
      "bir duvar (10,8 m²) 1 rulo ile bitmez, 2 rulo hesaplarız.</p>"),
    ("Duvar kağıdı boyaya göre daha mı pahalı?",
     "<p>Metrekare başına ilk maliyeti boyadan yüksek, evet. Ama boya 2-3 yılda bir yenilenir, "
      "duvar kağıdı 8-10 yıl durur. Uzun vadede aradaki fark kapanıyor. Bir de şu var: "
      "boyayla elde edemeyeceğiniz doku ve desen duvar kağıdında var — ikisi aynı işi yapmıyor.</p>"),
    ("Eski duvar kağıdının üzerine yenisi yapıştırılır mı?",
     "<p>Yapıştırılır ama yapmam. Eski kağıt zamanla nem çeker, altındaki yapıştırıcı gevşer; "
      "üstüne yeni kağıt koyduğunuzda ikisi birlikte kalkar. Sökme işçiliği bir gün fazladan sürer "
      "ama on yıl fark eder. Bunu keşifte açıkça söylüyorum.</p>"),
    ("Ücretsiz keşif gerçekten ücretsiz mi?",
     "<p>Evet. İstanbul'un 39 ilçesinin tamamına gidiyorum, ölçüyü alıyorum, kaç rulo gideceğini "
      "ve toplam tutarı yazılı olarak bırakıyorum. İş bende kalmasa da keşif ücreti istemiyorum. "
      "Tek ricam: randevuyu telefonla netleştirelim.</p>"),
    ("Duvar kağıdı kaç yıl dayanır?",
     "<p>Evde normal kullanımda 8-10 yıl, iyi malzemeyle 12 yıla kadar çıkar. Ofis ve mağazada "
      "5-7 yıl, otel koridoru gibi çok yoğun yerlerde 3-5 yıl. Ömrü kısaltan şey ürün değil, "
      "çoğu zaman nemli duvara yapıştırılmış olması.</p>"),
]


def anasayfa():
    ilce_gruplari = []
    for yaka in ("Avrupa", "Anadolu"):
        liste = [i for i in D.ILCELER if i["yaka"] == yaka]
        ic = "".join(f'<a href="/{i["slug"]}-duvar-kagidi-kaplama/">{e(i["ad"])}</a>' for i in liste)
        ilce_gruplari.append(f'<div class="yaka-bas">{yaka} Yakası · {len(liste)} ilçe</div>'
                             f'<div class="ilceler gel">{ic}</div>')

    alan_kartlari = "".join(
        f'<a href="/{a["slug"]}/"><span>›</span>{e(a["ad"])}</a>' for a in D.ALANLAR)

    schema = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness",
"name":"{S["marka"]}","url":"{S["alan"]}","telephone":"{S["tel_link"]}",
"image":"{S["alan"]}/assets/img/duvar-kagidi-kaplama-1600.webp",
"description":"{S["aciklama"]}",
"address":{{"@type":"PostalAddress","addressLocality":"İstanbul","addressCountry":"TR"}},
"areaServed":[{",".join('{"@type":"City","name":"%s"}' % i["ad"] for i in D.ILCELER)}],
"priceRange":"₺₺",
"makesOffer":[
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Duvar kağıdı kaplama"}},"priceCurrency":"TRY","price":"{D.RULO_SATIS}"}},
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Tavan duvar kağıdı kaplama"}},"priceCurrency":"TRY","price":"{D.TAVAN_SATIS}"}},
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Dijital özel baskı poster"}},"priceCurrency":"TRY","description":"Özel tasarım ve ölçüye göre fiyatlandırılır"}}]}}
</script>''' + sss_schema(ANA_SSS)

    return head(
        "Duvar Kağıdı Kaplama | İstanbul Duvar Kağıdı Ustası — " + S["ad"],
        "İstanbul'un 39 ilçesinde duvar kağıdı kaplama. 1 rulo 3.000 ₺'den başlar, işçilik 1.500 ₺. "
        "Ücretsiz keşif, yazılı fiyat, temiz işçilik. Hemen arayın: " + S["tel"],
        "/", "duvar-kagidi-kaplama", schema) + ust_header() + f'''
<div class="hero">
  <div class="kap">
    <div class="yazi">
      <span class="ust-etiket">İstanbul'un 39 ilçesinde</span>
      <h1><span class="el-yazi altin-yazi">Evinize</span>Değer Katan <span class="altin-yazi">Duvarlar</span></h1>
      <p class="giris">Duvar kağıdı kaplama, tavan kaplama ve dijital özel baskı poster.
      Ölçüyü yerinde alıyorum, kaç rulo gideceğini ve toplam tutarı <strong style="color:#fff">yazılı</strong>
      veriyorum. Sürpriz fiyat yok.</p>
      <div class="dugmeler">
        {tel_btn("btn btn-altin", "Ücretsiz Keşif İste")}
        {wa_btn()}
        <a class="btn btn-hat" style="color:#e6e9ef;border-color:rgba(255,255,255,.28)" href="#fiyatlar">Fiyat Listesi</a>
      </div>
      <a class="tel-buyuk" href="tel:{S["tel_link"]}">
        <span class="yuvarlak"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2
          19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.1a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7A2 2 0 0 1 22 16.9z"/></svg></span>
        <span><small>Hemen Ara</small><b>{e(S["tel"])}</b></span>
      </a>
    </div>
    <div class="hero-gorsel">
      <figure>{gorsel("duvar-kagidi-kaplama", "İstanbul'da salon duvarına uygulanmış desenli duvar kağıdı", boy="(min-width:1000px) 520px, 100vw", oncelik=True)}</figure>
      <div class="hero-rozet">
        <div class="b1">Profesyonel</div><div class="b2">DOKUNUŞ</div>
        <div class="b3">Uzun ömürlü, şık görünüm</div>
      </div>
    </div>
  </div>
</div>
{guven_seridi()}

<section class="acik">
  <div class="kap dar icerik">
    <h2 id="nedir">Duvar Kağıdı Kaplama Nedir, Ne İşe Yarar?</h2>
    <p>Duvar kağıdı kaplama, hazır desenli ya da dokulu bir yüzey malzemesinin özel yapıştırıcıyla
    duvara uygulanmasıdır. Boyadan farkı şu: boya duvarın rengini değiştirir, duvar kağıdı duvarın
    <strong>karakterini</strong> değiştirir. Doku, kabartma, desen, mermer ya da ahşap görünümü —
    bunların hiçbirini boyayla elde edemezsiniz.</p>
    <p>Bir işe daha yarıyor, bunu az kişi söyler: duvar kağıdı, duvardaki küçük kusurları kapatır.
    İnce çatlaklar, badana izleri, eski dübel delikleri düzgün bir hazırlıktan sonra kağıdın altında
    kalır. Bu yüzden eski binalarda kaplama, boyadan daha temiz bir sonuç verir.</p>
    <div class="vurgu"><p><strong>Dürüst uyarı:</strong> Duvar kağıdı mucize değil. Duvarda
    <em>nem</em> varsa kağıt o nemi kapatmaz, sadece gizler — ve altı küflenir. Nemli duvara kağıt
    yapıştıran ustadan uzak durun. Ben keşifte nem görürsem önce onun çözülmesini isterim,
    işi almamayı göze alırım.</p></div>

    <h2>Duvar Kağıdı Kaplama Türleri</h2>
    <p>Piyasada onlarca isim dolaşıyor ama pratikte karar verdiğiniz şey beş başlık:</p>
    <ul>
      <li><strong>Vinil (PVC) duvar kağıdı:</strong> Silinebilir, dayanıklı. Mutfak, çocuk odası,
      kuaför, klinik gibi temizlenmesi gereken yerlerin ürünü.</li>
      <li><strong>Non-woven (dokusuz yüzey):</strong> Yapıştırıcı duvara sürülür, kağıt kuru gider.
      Uygulaması temiz, sökülmesi kolay. Bugün evlerde en çok kullandığım tür.</li>
      <li><strong>Tekstil / kumaş kaplama:</strong> Yatak odası ve otel odalarında sıcak bir doku
      verir. Ama toz tutar, silinmez. Nerede kullanılacağını iyi seçmek gerekir.</li>
      <li><strong>Cam elyaf (boyanabilir):</strong> Çatlak kapatma gücü yüksek, üzerine boya atılır.
      Dönüşüm binalarında ve ofislerde işe yarar.</li>
      <li><strong>Dijital özel baskı:</strong> Kendi görselinizi ölçüye göre bastırırsınız.
      m² üzerinden fiyatlanır, tek parça duvar resmi gibi durur.</li>
    </ul>
    <p>Hangisi olacağına katalogdan değil, <strong>odanın kendisinden</strong> karar veriyoruz:
    duvar nem alıyor mu, güneş görüyor mu, çocuk eli değiyor mu. Bunlar sorulmadan verilen
    tavsiye satış konuşmasıdır.</p>
    <p><a href="/duvar-kagidi-cesitleri/">Duvar kağıdı çeşitlerinin tamamını ayrıntılı anlattığım sayfa →</a></p>
  </div>
</section>

<section id="fiyatlar">
  <div class="kap">{fiyat_tablosu("Duvar Kağıdı Fiyatları")}</div>
</section>

<section class="acik">
  <div class="kap">{hesaplayici()}</div>
</section>

<section>
  <div class="kap">{galeri()}</div>
</section>

<section class="acik">
  <div class="kap dar icerik">
    <h2>Duvar Kağıdı İşçilik Fiyatları</h2>
    <p>İşçiliği metrekare üzerinden değil <strong>rulo bazında</strong> hesaplıyorum ve bunun
    sebebi var: bir ustanın emeği duvarın kaç metrekare olduğuna değil, kaç şerit kesip kaç kez
    hizalayacağına bağlı. 10 m²'lik düz bir duvarla, 10 m²'lik ama üç pencereli bir duvar aynı
    iş değil — rulo hesabı bu farkı daha adil yansıtıyor.</p>
    <ul>
      <li>Duvar kağıdı işçiliği: <strong>{tl(D.RULO_ISCILIK)} / rulo</strong></li>
      <li>Tavan duvar kağıdı işçiliği: <strong>{tl(D.TAVAN_ISCILIK)} / rulo</strong> — baş üstü çalışma, iki kişilik ekip</li>
      <li>Dijital özel baskı / poster: <strong>özel tasarım ve ölçüye göre fiyatlandırılır</strong> — keşifte netleşir</li>
    </ul>
    <p>Eski kağıt sökümü, alçı tamiri ve astar gerekiyorsa bunları ayrı kalem olarak, keşifte
    yazılı veriyorum. İş sırasında çıkan "bir de şu var" sürprizini sevmiyorum.</p>
    <p><a href="/duvar-kagidi-iscilik-fiyatlari/">İşçilik fiyatlarını ayrıntılı anlattığım sayfa →</a></p>

    <h2>Duvar Kağıdının Ömrü Ne Kadardır?</h2>
    <p>Evde normal kullanımda <strong>8-10 yıl</strong>. İyi malzeme ve düzgün uygulamayla 12 yıla
    çıktığını gördüm. Ofis ve mağazada 5-7 yıl, otel koridoru gibi çok yoğun yerlerde 3-5 yıl.</p>
    <p>Ömrü kısaltan şey neredeyse hiçbir zaman ürün olmuyor. En çok gördüğüm üç sebep:
    nemli duvara yapıştırılması, astarsız uygulama ve alçı kurumadan işe başlanması.
    Üçü de ustadan kaynaklanıyor, malzemeden değil.</p>
    <p><a href="/duvar-kagidi-omru/">Duvar kağıdı ömrü ve ömrü kısaltan hatalar →</a></p>
  </div>
</section>

<section>
  <div class="kap">
    <div class="bolum-bas"><span class="etiket">Uygulama</span><h2>İşi Yaparken Nasıl Çalışıyorum?</h2>
      <p>Kısa bir video: hazırlıktan teslime kadar bir duvar kağıdı uygulaması.</p></div>
    <div class="video-kutu gel">
      <video controls preload="none" playsinline
             poster="/assets/img/duvar-kagidi-kaplama-900.webp">
        <source src="/video/duvar-kagidi-kaplama.mp4" type="video/mp4">
        Tarayıcınız video oynatmayı desteklemiyor.
      </video>
    </div>
  </div>
</section>

<section class="acik" id="kullanim-alanlari">
  <div class="kap">
    <div class="bolum-bas"><span class="etiket">Kullanım Alanları</span><h2>Nerelere Duvar Kağıdı Yapıyorum?</h2>
      <p>Evden otele, klinikten kuaföre. Her mekânın duvarı farklı ürün istiyor — hangisinin
      nerede işe yaradığını ayrı ayrı yazdım.</p></div>
    <div class="baglar gel">{alan_kartlari}</div>
  </div>
</section>

<section id="hizmet-bolgeleri">
  <div class="kap">
    <div class="bolum-bas"><span class="etiket">Hizmet Bölgeleri</span><h2>İstanbul'un 39 İlçesinde Hizmet</h2>
      <p>Bulunduğunuz ilçeye tıklayın: o ilçede nasıl çalıştığımı, güncel fiyatları ve
      örnek hesapları orada bulacaksınız.</p></div>
    {"".join(ilce_gruplari)}
  </div>
</section>

<section class="acik">
  <div class="kap dar">{sss_bolum(ANA_SSS)}</div>
</section>

<section>
  <div class="kap">{cta_band("Duvarınızı Konuşalım",
      "Ücretsiz keşif için arayın. Ölçüyü alayım, kaç rulo gideceğini ve toplam tutarı "
      "yazılı bırakayım. İş bende kalmasa da keşif ücreti yok.")}</div>
</section>
''' + alt_bilgi()


# ── İlçe sayfası ────────────────────────────────────────────────────────────

def ilce_sss(i):
    ad = i["ad"]
    return [
        (f"{ad}'de duvar kağıdı yaptırmak için kimi aramalıyım?",
         f"<p>Beni arayabilirsiniz: <strong>{S['tel']}</strong>. {ad} ve çevresine ücretsiz keşfe "
         f"geliyorum. Duvarı ölçüyorum, kaç rulo gideceğini ve toplam tutarı yazılı bırakıyorum. "
         f"Telefonda tahmini rakam da söylerim ama net fiyat için duvarı görmem gerekiyor.</p>"),
        (f"{ad}'de duvar kağıdı ustası numarası nedir?",
         f"<p><strong>{S['tel']}</strong>. Telefonu ben açıyorum, çağrı merkezi değil. "
         f"Ne zaman gelebileceğimi ve işin kaç sürede biteceğini konuşurken söylerim.</p>"),
        (f"{ad}'de duvar kağıdı kaplama ne kadar tutar?",
         f"<p>Malzeme {tl(D.RULO_SATIS)}'den başlıyor, işçilik rulo başına {tl(D.RULO_ISCILIK)}. "
         f"Salonda 4 metrelik bir TV duvarı genelde 2 rulo ile bitiyor; yani yaklaşık "
         f"{tl(2 * (D.RULO_SATIS + D.RULO_ISCILIK))} civarı. Yukarıdaki hesaplayıcıya kendi "
         f"duvarınızın ölçüsünü yazıp anında görebilirsiniz.</p>"),
        (f"{ad}'e keşif ücretli mi?",
         f"<p>Hayır. {ad}'e keşfe gelmek ücretsiz. İş bende kalmasa da keşif için para istemiyorum. "
         f"Tek ricam randevuyu telefonla netleştirmemiz — boşuna yol olmasın.</p>"),
        (f"{ad}'de duvar kağıdı satan yer arıyorum, sadece ürün alabilir miyim?",
         "<p>Alabilirsiniz ama açık konuşayım: duvar kağıdının yarısı üründür, yarısı uygulamadır. "
         "İyi ürünü kötü uygulama bir yılda bitirir. Yine de kendiniz yapmak istiyorsanız hangi "
         "ürünün size uygun olduğunu söylerim, ölçüyü birlikte hesaplarız.</p>"),
        (f"{ad}'de iş ne kadar sürede biter?",
         f"<p>Tek duvar 2-3 saat, bir oda yarım gün, salon + koridor bir gün. {i['vurgu'].split(';')[0]} "
         f"— bunu keşifte görüp süreyi baştan söylüyorum.</p>"),
    ]


def ilce_sayfasi(i):
    ad, slug = i["ad"], i["slug"]
    yol = f"/{slug}-duvar-kagidi-kaplama/"
    mahalle = ", ".join(i["mahalle"])
    komsular = [k for k in D.ILCELER if k["slug"] in i["komsu"]]
    komsu_link = "".join(
        f'<a href="/{k["slug"]}-duvar-kagidi-kaplama/"><span>›</span>{e(k["ad"])} duvar kağıdı</a>'
        for k in komsular)
    alan_link = "".join(f'<a href="/{a["slug"]}/"><span>›</span>{e(a["ad"])}</a>' for a in D.ALANLAR[:9])
    sorular = ilce_sss(i)

    ornek2 = 2 * (D.RULO_SATIS + D.RULO_ISCILIK)
    ornek4 = 4 * (D.RULO_SATIS + D.RULO_ISCILIK)

    schema = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","serviceType":"Duvar kağıdı kaplama",
"name":"{ad} Duvar Kağıdı Kaplama","url":"{S["alan"]}{yol}",
"areaServed":{{"@type":"City","name":"{ad}","containedInPlace":{{"@type":"City","name":"İstanbul"}}}},
"provider":{{"@type":"HomeAndConstructionBusiness","name":"{S["marka"]}","telephone":"{S["tel_link"]}","url":"{S["alan"]}"}},
"offers":{{"@type":"Offer","priceCurrency":"TRY","price":"{D.RULO_SATIS}","description":"1 rulo duvar kağıdı, {D.RULO_M2} m²"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"{S["alan"]}/"}},
{{"@type":"ListItem","position":2,"name":"Hizmet Bölgeleri","item":"{S["alan"]}/#hizmet-bolgeleri"}},
{{"@type":"ListItem","position":3,"name":"{ad} Duvar Kağıdı Kaplama","item":"{S["alan"]}{yol}"}}]}}
</script>''' + sss_schema(sorular)

    return head(
        f"{ad} Duvar Kağıdı Kaplama | {ad} Duvar Kağıdı Ustası — {S['tel']}",
        f"{ad}'de duvar kağıdı kaplama, duvar kaplama ve duvar kağıdı ustası. Rulo {tl(D.RULO_SATIS)}'den, "
        f"işçilik {tl(D.RULO_ISCILIK)}. Ücretsiz keşif, yazılı fiyat. Hemen arayın: {S['tel']}",
        yol, "duvar-kagidi-kaplama", schema) + ust_header() + f'''
<div class="hero" style="padding:44px 0 52px">
  <div class="kap">
    <div class="yazi">
      <span class="ust-etiket">{e(ad)} · İstanbul</span>
      <h1>{e(ad)} <span class="altin-yazi">Duvar Kağıdı Kaplama</span></h1>
      <p class="giris">{e(ad)}'de duvar kağıdı mı yaptırmak istiyorsunuz? Size en yakın duvar kağıdı
      ustasını mı arıyorsunuz? Uygun fiyata duvar kaplatmak mı istiyorsunuz? Doğru sayfadasınız.
      Ölçüyü yerinde alıyorum, rakamı yazılı veriyorum.</p>
      <div class="dugmeler">{tel_btn("btn btn-altin", "Hemen Ara: " + S["tel"])}{wa_btn()}</div>
    </div>
    <div class="hero-gorsel">
      <figure>{gorsel("duvar-kagidi-firmasi", f"{ad}'de duvar kağıdı kaplama uygulaması",
                      boy="(min-width:1000px) 520px, 100vw", oncelik=True)}</figure>
      <div class="hero-rozet"><div class="b1">{e(ad)}</div><div class="b2">ÜCRETSİZ KEŞİF</div>
        <div class="b3">Ölçü + yazılı fiyat</div></div>
    </div>
  </div>
</div>
{guven_seridi()}
{kirinti([("/", "Ana Sayfa"), ("/#hizmet-bolgeleri", "Hizmet Bölgeleri"), (None, ad + " Duvar Kağıdı Kaplama")])}

<section class="acik">
  <div class="kap dar icerik">
    <h2>{e(ad)}'de Duvar Kağıdı Yaptırmak İçin Kimi Aramalısınız?</h2>
    <p>Kısa cevap: <a href="tel:{S["tel_link"]}"><strong>{e(S["tel"])}</strong></a>. Telefonu ben
    açıyorum. {e(ad)}'e keşfe geliyorum, duvarı ölçüyorum, kaç rulo gideceğini ve toplam tutarı
    yazılı bırakıyorum. İş bende kalmasa da keşif ücreti istemiyorum.</p>

    <div class="vurgu">
      <p><strong>{e(ad)}'de duvar kağıdı ustası numarası:</strong>
      <a href="tel:{S["tel_link"]}" style="font-size:22px;font-weight:800">{e(S["tel"])}</a></p>
      <p style="margin-bottom:0">Aradığınızda konuşacağımız üç şey: hangi odayı kaplatacaksınız,
      duvarın kabaca ölçüsü ne, ne zaman uygun olursunuz. Bu üçünü konuşunca size telefonda bile
      yaklaşık bir rakam söyleyebilirim.</p>
    </div>

    <h2>{e(ad)}'de Nasıl Çalışıyorum?</h2>
    <p>{e(ad)}'de yapı stoğu ağırlıkla {e(i["doku"])}. Bu ilçede işin pratikte değişen tarafı şu:
    {e(i["vurgu"])}.</p>
    <p>{e(mahalle)} ve çevresindeki bütün mahallelere gidiyorum. {e(ad)} merkezine yakın işlerde
    çoğu zaman aynı hafta içinde randevu verebiliyorum; keşif ile uygulama arasında ürün seçimi
    için birkaç gün bırakıyoruz.</p>

    <h2>{e(ad)} Duvar Kağıdı Satan Yerler</h2>
    <p>{e(ad)}'de duvar kağıdı satan yer ararken şuna dikkat edin: ürünü satan yer ile uygulayan
    kişi çoğu zaman aynı değil. Mağazadan rulo alırsınız, sonra usta ararsınız, iki taraf birbirini
    suçlar. Ben ikisini birlikte veriyorum — ürünü de ben getiriyorum, uygulamayı da ben yapıyorum.
    Bir sorun çıkarsa muhatap tek kişi.</p>
    <p>Katalogda binlerce desen var. Keşifte tabletten gösteriyorum, beğendiğiniz üründen numune
    getiriyorum. Duvarda gerçek ışıkta görmeden karar vermeyin; ekranda gri görünen kağıt duvarda
    bej çıkabiliyor.</p>

    <h2>{e(ad)} Duvar Kaplama Seçenekleri</h2>
    <p>Duvar kaplama denince akla sadece duvar kağıdı gelmesin. {e(ad)}'de üç iş yapıyorum:</p>
    <ul>
      <li><strong>Duvar kağıdı kaplama</strong> — en yaygın çözüm, rulo bazında fiyatlanır.</li>
      <li><strong>Tavan duvar kağıdı</strong> — tavana uygulanan özel kaplama; işçiliği duvarın
      yaklaşık iki katı, çünkü baş üstü çalışma ve iki kişi gerektiriyor.</li>
      <li><strong>Dijital özel baskı poster</strong> — kendi görselinizi m² üzerinden bastırıp
      duvara uygulamak. Çocuk odası ve iş yerlerinde çok tercih ediliyor.</li>
    </ul>

    <h2>{e(ad)} Duvar Kağıdı Ustası Ararken Nelere Dikkat Edin?</h2>
    <p>Dürüst olayım, bu işi yapan çok kişi var ve hepsi aynı işi yapmıyor. {e(ad)}'de usta
    ararken bakmanız gereken dört şey:</p>
    <ol>
      <li><strong>Keşfe geliyor mu?</strong> Duvarı görmeden telefonda kesin fiyat veren kişi,
      iş sırasında o fiyatı değiştirir.</li>
      <li><strong>Duvar hazırlığını konuşuyor mu?</strong> Astar, çatlak tamiri, eski kağıt sökümü —
      bunları hiç açmıyorsa muhtemelen yapmıyor demektir.</li>
      <li><strong>Rakamı yazılı veriyor mu?</strong> Sözlü fiyat, iş bitiminde tartışma demek.</li>
      <li><strong>Nem konusunda ne diyor?</strong> Nemli duvara "olur abi kapatırız" diyen ustadan
      uzak durun. O duvar altı ay sonra küflenir.</li>
    </ol>
  </div>
</section>

<section>
  <div class="kap">{fiyat_tablosu(f"{ad} Duvar Kağıdı Fiyatları",
    f"{D.FIYAT_GUNCELLEME} itibarıyla {ad} ve İstanbul geneli için geçerli fiyatlar. "
    f"1 rulo {str(D.RULO_M2).replace('.', ',')} m² kaplar, rulo eni {D.RULO_EN_CM} cm.")}</div>
</section>

<section class="acik">
  <div class="kap">{hesaplayici()}</div>
</section>

<section>
  <div class="kap dar icerik">
    <h2>{e(ad)} İçin Örnek Hesaplar</h2>
    <p>Rakamı somutlaştıralım. {e(ad)}'de en sık karşılaştığım iki iş:</p>
    <ul>
      <li><strong>Salonda tek duvar (TV arkası, ~4 m × 2,7 m):</strong> 10,8 m² → 2 rulo.
      Ürün {tl(2 * D.RULO_SATIS)} + işçilik {tl(2 * D.RULO_ISCILIK)} =
      <strong>yaklaşık {tl(ornek2)}</strong>.</li>
      <li><strong>Yatak odasının tamamı (~14 m² duvar alanı):</strong> 4 rulo.
      Ürün {tl(4 * D.RULO_SATIS)} + işçilik {tl(4 * D.RULO_ISCILIK)} =
      <strong>yaklaşık {tl(ornek4)}</strong>.</li>
    </ul>
    <p>Bunlar {tl(D.RULO_SATIS)}'den başlayan giriş seviyesi ürün üzerinden hesaplandı. Daha üst segment
    bir desen seçerseniz ürün bedeli artar, işçilik aynı kalır. Eski kağıt sökümü ya da alçı
    tamiri gerekiyorsa bunu ayrı kalem olarak keşifte yazılı veriyorum.</p>
    <div class="vurgu"><p style="margin-bottom:0"><strong>Şunu da söyleyeyim:</strong> çoğu evde
    odanın dört duvarını da kaplatmaya gerek yok. Tek duvar kaplaması hem daha ucuz hem çoğu zaman
    daha şık duruyor. {e(ad)}'de keşfe geldiğimde bunu size açıkça söylerim — dört duvar satıp
    gitmek işime gelirdi ama öyle çalışmıyorum. :)</p></div>
  </div>
</section>

<section class="acik">
  <div class="kap">
    <div class="bolum-bas"><span class="etiket">Kullanım Alanları</span>
      <h2>{e(ad)}'de Hangi Mekânlara Duvar Kağıdı Yapıyorum?</h2>
      <p>Evden iş yerine, klinikten kuaföre. Her mekânın duvarı farklı ürün istiyor.</p></div>
    <div class="baglar gel">{alan_link}</div>
  </div>
</section>

<section>
  <div class="kap dar">{sss_bolum(sorular, f"{ad} Duvar Kağıdı — Sık Sorulan Sorular")}</div>
</section>

<section class="acik">
  <div class="kap">
    <div class="bolum-bas"><span class="etiket">Yakın İlçeler</span><h2>{e(ad)} Çevresinde Hizmet Verdiğim İlçeler</h2>
      <p>Aynı gün içinde komşu ilçelere de gidebiliyorum.</p></div>
    <div class="baglar gel">{komsu_link}</div>
    <p style="text-align:center;margin-top:22px"><a href="/#hizmet-bolgeleri"><strong>İstanbul'un 39 ilçesinin tamamı →</strong></a></p>
  </div>
</section>

<section>
  <div class="kap">{cta_band(f"{ad}'de Duvar Kağıdı mı Yaptıracaksınız?",
    f"Arayın, {ad}'e ücretsiz keşfe geleyim. Ölçüyü alayım, kaç rulo gideceğini ve toplam tutarı "
    f"yazılı bırakayım. Karar sizin.")}</div>
</section>
''' + alt_bilgi()
