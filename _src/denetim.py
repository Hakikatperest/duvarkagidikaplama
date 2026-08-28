# -*- coding: utf-8 -*-
"""Üretilen siteyi denetler: kırık iç link, eksik görsel, tekrar eden başlık/açıklama."""
import os, re, sys, collections, html as H
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sayfalar, hata = [], []
for kok, _, dosyalar in os.walk(KOK):
    if "/.git" in kok or "/_src" in kok:
        continue
    for d in dosyalar:
        if d.endswith(".html"):
            sayfalar.append(os.path.join(kok, d))

def var_mi(yol):
    yol = yol.split("#")[0].split("?")[0]
    if not yol.startswith("/"):
        return True
    t = os.path.join(KOK, yol.strip("/"))
    return os.path.exists(t) or os.path.exists(os.path.join(t, "index.html")) or os.path.exists(t + ".html")

basliklar, aciklamalar = collections.Counter(), collections.Counter()
for s in sayfalar:
    ic = open(s, encoding="utf-8").read()
    rel = "/" + os.path.relpath(s, KOK)

    for u in set(re.findall(r'href="(/[^"]*)"', ic)) | set(re.findall(r'src="(/[^"]*)"', ic)):
        if not var_mi(u):
            hata.append(f"KIRIK  {rel} → {u}")
    for u in set(re.findall(r'srcset="([^"]+)"', ic)):
        for p in [x.strip().split(" ")[0] for x in u.split(",")]:
            if p.startswith("/") and not var_mi(p):
                hata.append(f"KIRIK GÖRSEL  {rel} → {p}")

    # Uzunluk HTML kaçışı ÇÖZÜLDÜKTEN sonra ölçülür: "Şile'de" kaynakta
    # "Şile&#x27;de" olarak duruyor ve ham ölçüm 6 karakter fazla sayıyor.
    t = re.search(r"<title>(.*?)</title>", ic, re.S)
    a = re.search(r'<meta name="description" content="(.*?)"', ic, re.S)
    t = re.match(r"(.*)", H.unescape(t.group(1)), re.S) if t else None
    a = re.match(r"(.*)", H.unescape(a.group(1)), re.S) if a else None
    if t: basliklar[t.group(1)] += 1
    if a: aciklamalar[a.group(1)] += 1
    if t and len(t.group(1)) > 70: hata.append(f"UZUN TITLE ({len(t.group(1))})  {rel}")
    if a and not (110 <= len(a.group(1)) <= 175): hata.append(f"DESC UZUNLUK ({len(a.group(1))})  {rel}")
    if 'rel="canonical"' not in ic: hata.append(f"CANONICAL YOK  {rel}")
    if ic.count("<h1") != 1: hata.append(f"H1 SAYISI {ic.count('<h1')}  {rel}")

for b, n in basliklar.items():
    if n > 1: hata.append(f"TEKRAR TITLE ×{n}: {b[:70]}")
for b, n in aciklamalar.items():
    if n > 1: hata.append(f"TEKRAR DESC ×{n}: {b[:70]}")

print(f"{len(sayfalar)} sayfa denetlendi")
if hata:
    ozet = collections.Counter(h.split("  ")[0].split(" (")[0] for h in hata)
    for k, v in ozet.most_common(): print(f"  {v:4d} × {k}")
    print()
    for h in hata[:25]: print("   ", h)
    if len(hata) > 25: print(f"    … {len(hata)-25} tane daha")
    sys.exit(1)
print("✓ hata yok")
