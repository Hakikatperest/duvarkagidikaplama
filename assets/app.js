/* duvarkagidikaplama.com — tek dosya, bağımlılıksız.
   Üç iş yapar: mobil menü, görünürlük animasyonu, fiyat hesaplayıcı. */
(function () {
  'use strict';

  /* ── Mobil menü ─────────────────────────────────────────────────────────── */
  var mnu = document.querySelector('.mnu'), nav = document.querySelector('nav.ana');
  if (mnu && nav) {
    mnu.addEventListener('click', function () {
      var acik = nav.classList.toggle('acik');
      mnu.setAttribute('aria-expanded', acik ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('acik'); mnu.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* ── Görünürlük animasyonu ──────────────────────────────────────────────── */
  var hedefler = document.querySelectorAll('.gel');
  if (hedefler.length) {
    if (!('IntersectionObserver' in window)) {
      hedefler.forEach(function (el) { el.classList.add('acik'); });
    } else {
      var izle = new IntersectionObserver(function (girisler) {
        girisler.forEach(function (g) {
          if (g.isIntersecting) { g.target.classList.add('acik'); izle.unobserve(g.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: .06 });
      hedefler.forEach(function (el) { izle.observe(el); });
    }
  }

  /* ── Fiyat hesaplayıcı ──────────────────────────────────────────────────────
     Rulo sayısı YUKARI yuvarlanır: yarım rulo diye bir şey yok, 15,6 m²'lik
     duvar için 2 rulo alınır. Sonuç "yaklaşık" olarak sunulur — desen raporu
     olan ürünlerde kesim firesi rulo sayısını bir artırabiliyor.             */
  var form = document.getElementById('hesapForm');
  if (form) {
    var d = form.dataset;
    var RULO_M2 = parseFloat(d.ruloM2), RULO = parseFloat(d.ruloSatis), ISC = parseFloat(d.ruloIscilik);
    var TAV = parseFloat(d.tavanSatis), TAVI = parseFloat(d.tavanIscilik);

    var tl = function (n) { return n.toLocaleString('tr-TR', { maximumFractionDigits: 0 }) + ' ₺'; };

    function hesapla() {
      var en = parseFloat(form.en.value) || 0;
      var yuk = parseFloat(form.yukseklik.value) || 0;
      var tur = form.tur.value;
      var m2 = en * yuk;
      var kutu = document.getElementById('hesapSonuc');
      var posterNot = document.getElementById('posterNot');

      /* Dijital özel baskının SABİT m² fiyatı yok: özel tasarım ve ölçüye göre
         belirleniyor. Uydurma rakam göstermek yerine keşfe yönlendiriyoruz. */
      if (tur === 'poster') {
        kutu.hidden = true;
        if (posterNot) posterNot.hidden = false;
        return;
      }
      if (posterNot) posterNot.hidden = true;

      if (m2 <= 0) { kutu.hidden = true; return; }
      kutu.hidden = false;

      var rulo = Math.ceil(m2 / RULO_M2);
      var satis = rulo * (tur === 'tavan' ? TAV : RULO);
      var iscilik = rulo * (tur === 'tavan' ? TAVI : ISC);
      var adetMetni = rulo + ' rulo (' + m2.toFixed(1).replace('.', ',') + ' m²)';

      document.getElementById('sonucAdet').textContent = adetMetni;
      document.getElementById('sonucUrun').textContent = tl(satis);
      document.getElementById('sonucIscilik').textContent = tl(iscilik);
      document.getElementById('sonucToplam').textContent = tl(satis + iscilik);
    }

    form.addEventListener('input', hesapla);
    form.addEventListener('change', hesapla);
    hesapla();
  }
})();
