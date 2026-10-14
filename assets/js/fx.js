/* يدير — حركات وتأثيرات الواجهة (تُعطَّل تلقائياً عند تفضيل تقليل الحركة) */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* رأس الصفحة: ظل عند التمرير */
  var hd = $('.header');
  var onScroll = function () { if (hd) hd.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (reduce) { $$('.rot').forEach(function (r) { r.classList.add('static'); }); return; }

  /* بقعة ضوء تتبّع المؤشر في الأقسام الداكنة */
  if (fine) {
    $$('[data-spot], .sec.dark').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px'); el.style.setProperty('--my', (e.clientY - r.top) + 'px');
        el.classList.add('lit');
      });
      el.addEventListener('pointerleave', function () { el.classList.remove('lit'); });
    });
    /* توهّج داخل البطاقات */
    $$('.glow').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--gx', (e.clientX - r.left) + 'px'); el.style.setProperty('--gy', (e.clientY - r.top) + 'px');
      });
    });
    /* إمالة ثلاثية الأبعاد خفيفة */
    $$('.tilt').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        el.style.transform = 'perspective(800px) rotateY(' + (-x * 7) + 'deg) rotateX(' + (y * 7) + 'deg) translateY(-4px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
    /* أزرار مغناطيسية */
    $$('.magnetic').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * .18) + 'px,' + ((e.clientY - r.top - r.height / 2) * .28) + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
    /* حركة منظور للرسم في البنر */
    $$('.banner').forEach(function (b) {
      var art = $('.banner-art .art', b); if (!art) return;
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        art.style.transform = 'translate(' + (x * -14) + 'px,' + (y * -10) + 'px) rotate(' + (x * 1.2) + 'deg)';
      });
      b.addEventListener('pointerleave', function () { art.style.transform = ''; });
    });
  }

  /* كلمة متبدّلة في العنوان */
  $$('.rot').forEach(function (r) {
    var w = $('.rot-w', r), list = (r.getAttribute('data-words') || '').split('|'), i = 0;
    if (!w || list.length < 2) return;
    setInterval(function () {
      w.classList.add('out');
      setTimeout(function () { i = (i + 1) % list.length; w.textContent = list[i]; w.classList.remove('out'); w.classList.add('pre'); void w.offsetWidth; w.classList.remove('pre'); }, 380);
    }, 2800);
  });

  /* تصفية الخدمات */
  var tabs = $$('.tab');
  if (tabs.length) {
    var cards = $$('.svc-grid .svc');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (x) { x.classList.toggle('on', x === t); x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
        var f = t.getAttribute('data-f'), n = 0;
        cards.forEach(function (c) {
          var show = f === 'all' || c.getAttribute('data-g') === f;
          c.hidden = !show;
          if (show) { c.classList.remove('in'); c.style.setProperty('--d', (n++ * .04) + 's'); void c.offsetWidth; c.classList.add('in'); }
        });
      });
    });
  }

  /* رسم خط الخطوات عند الظهور */
  $$('[data-draw]').forEach(function (el) {
    if (!('IntersectionObserver' in window)) { el.classList.add('drawn'); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { el.classList.add('drawn'); io.disconnect(); } }); }, { threshold: .35 });
    io.observe(el);
  });

  /* انزياح بطيء للشبكة في الخلفية */
  var net = $('.hero-net');
  if (net) {
    var t = false;
    window.addEventListener('scroll', function () {
      if (t) return; t = true;
      requestAnimationFrame(function () { net.style.transform = 'translateY(' + (window.scrollY * .18) + 'px)'; t = false; });
    }, { passive: true });
  }
})();
