# -*- coding: utf-8 -*-
"""
Görsel türevleri.

Kaynak görseller images/ altında 1536×1024 ve ~2,2 MB — bu hâlleriyle sayfaya
konulamaz: tek görsel, sayfanın tamamının olması gereken ağırlığın on katı.
Burada her görselin 3 genişlikte WebP türevi üretilir ve sayfada srcset ile
verilir; tarayıcı ekran genişliğine göre doğru boyutu indirir.

⚠️ cwebp'in varsayılan ayarları (-m 6 -pass 10) görsel başına saniyeler harcayıp
bazı görselleri BÜYÜTEBİLİYOR (zkolay'da yaşandı). Bu yüzden dönüşüm Pillow ile,
sabit kalite 80 ve method 4 ile yapılıyor.
"""
import os
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, "images")
HEDEF = os.path.join(KOK, "assets", "img")

# (sonek, genişlik) — hero geniş, kart orta, küçük görsel dar.
BOYLAR = [("1600", 1600), ("900", 900), ("500", 500)]


def uret(log=print):
    os.makedirs(HEDEF, exist_ok=True)
    sonuc = []

    for ad in sorted(os.listdir(KAYNAK)):
        if ad.startswith("."):
            continue
        yol = os.path.join(KAYNAK, ad)
        taban, uzanti = os.path.splitext(ad)

        with Image.open(yol) as im:
            im = im.convert("RGBA") if im.mode == "RGBA" else im.convert("RGB")

            for sonek, genislik in BOYLAR:
                # Kaynaktan BÜYÜTME yok ama türev de atlanmaz: kaynak dar ise
                # dosya kendi genişliğinde bu adla yazılır. Atlanırsa şablonun
                # beklediği -900 türevi oluşmuyor ve sayfada kırık görsel çıkıyor.
                if im.width < genislik and sonek == "1600":
                    continue
                oran = min(1.0, genislik / im.width)
                yeni = im.resize((round(im.width * oran), round(im.height * oran)), Image.LANCZOS)
                cikti = os.path.join(HEDEF, f"{taban}-{sonek}.webp")
                yeni.save(cikti, "WEBP", quality=80, method=4)
                sonuc.append((os.path.basename(cikti), os.path.getsize(cikti)))

    for ad, boyut in sonuc:
        log(f"  {ad:48s} {boyut/1024:7.0f} KB")
    log(f"  toplam {len(sonuc)} türev")
    return sonuc


if __name__ == "__main__":
    uret()
