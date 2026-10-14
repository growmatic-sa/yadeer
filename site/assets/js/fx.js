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

  /* عناوين تظهر كلمة كلمة */
  $$('.sec-head .h2, .cta .h2, .banner-copy h1').forEach(function (el) {
    if (el.children.length) return;
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.innerHTML = words.map(function (w, i) { return '<span class="wd" aria-hidden="true"><span style="--i:' + i + '">' + w.replace(/[&<>]/g, '') + '</span></span> '; }).join('');
  });

  /* مؤشر: سلسلة نقاط مأخوذة من نقطة الشعار */
  if (fine) {
    var N = 4, dots = [], mx = -100, my = -100, shown = false;
    for (var i = 0; i < N; i++) {
      var d = document.createElement('i'); d.className = 'cdot d' + (i + 1); d.setAttribute('aria-hidden', 'true');
      d.style.width = d.style.height = (12 - i * 2.2) + 'px'; d.style.margin = (-(12 - i * 2.2) / 2) + 'px 0 0 ' + (-(12 - i * 2.2) / 2) + 'px';
      d.style.opacity = ''; document.body.appendChild(d); dots.push({ el: d, x: -100, y: -100 });
    }
    var dark = false, hv = false;
    window.addEventListener('pointermove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (!shown) { shown = true; dots.forEach(function (o) { o.x = mx; o.y = my; o.el.classList.add('show'); }); }
      var t = e.target.closest ? e.target : null;
      var nd = !!(t && t.closest('.hero,.banner,.cta,.footer,.lab-sec,.chat-h,.dock-call'));
      var nh = !!(t && t.closest('a,button,[role=tab],summary,input,select,textarea,label'));
      if (nd !== dark || nh !== hv) {
        dark = nd; hv = nh;
        dots.forEach(function (o) { o.el.classList.toggle('dk', dark); o.el.classList.toggle('hv', hv); });
      }
    }, { passive: true });
    document.documentElement.addEventListener('pointerleave', function () { dots.forEach(function (o) { o.el.classList.remove('show'); }); shown = false; });
    (function loop() {
      var px = mx, py = my;
      dots.forEach(function (o, i) {
        var k = i === 0 ? .42 : .3 - i * .04;
        o.x += (px - o.x) * k; o.y += (py - o.y) * k; px = o.x; py = o.y;
        o.el.style.transform = 'translate3d(' + o.x + 'px,' + o.y + 'px,0)';
      });
      requestAnimationFrame(loop);
    })();

    /* إمالة ثلاثية الأبعاد خفيفة للبطاقات */
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
    /* منظور رسم البنر */
    $$('.banner').forEach(function (b) {
      var art = $('.banner-art .art', b); if (!art) return;
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        art.style.transform = 'translate(' + (x * -14) + 'px,' + (y * -10) + 'px) rotate(' + (x * 1.2) + 'deg)';
      });
      b.addEventListener('pointerleave', function () { art.style.transform = ''; });
    });
  }

  /* عناصر عائمة: انزياح بحسب التمرير والمؤشر + كلمات عملاقة */
  var fls = $$('.fl'), words = $$('.bigword span'), mvx = 0, mvy = 0, ticking = false;
  var frame = function () {
    ticking = false;
    var vh = window.innerHeight;
    fls.forEach(function (f) {
      var p = f.parentNode.parentNode, r = p.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var dy = (r.top + r.height / 2 - vh / 2), sp = parseFloat(f.getAttribute('data-sp')) || 0;
      f.style.transform = 'translate3d(' + (mvx * sp * 40) + 'px,' + (dy * sp * .45 + mvy * sp * 40) + 'px,0) rotate(' + (dy * sp * .06) + 'deg)';
    });
    words.forEach(function (w) {
      var r = w.parentNode.getBoundingClientRect(); if (r.bottom < -100 || r.top > vh + 100) return;
      var prog = (vh - r.top) / (vh + r.height);
      w.style.transform = 'translateX(' + ((prog - .5) * -260) + 'px)';
    });
  };
  var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  window.addEventListener('scroll', req, { passive: true }); window.addEventListener('resize', req);
  if (fine) window.addEventListener('pointermove', function (e) { mvx = e.clientX / window.innerWidth - .5; mvy = e.clientY / window.innerHeight - .5; req(); }, { passive: true });
  frame();

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

  /* شبكة الخلفية تتحرك ببطء */
  var net = $('.hero-net');
  if (net) window.addEventListener('scroll', function () { net.style.transform = 'translateY(' + (window.scrollY * .18) + 'px)'; }, { passive: true });

  /* شريط الأقسام الجانبي (الرئيسية فقط) */
  if (document.body.classList.contains('home') && 'IntersectionObserver' in window) {
    var map = [['top', 'البداية'], ['start', 'ابدأ من مشكلتك'], ['approach', 'فكرتنا'], ['services', 'الخدمات'], ['lab', 'مختبر النمو'], ['process', 'طريقة العمل'], ['blog', 'المدونة'], ['faq', 'أسئلة']];
    var nav = document.createElement('nav'); nav.className = 'rail'; nav.setAttribute('aria-label', 'أقسام الصفحة');
    var ul = document.createElement('ul'), links = {};
    map.forEach(function (m) {
      var el = document.getElementById(m[0]); if (!el) return;
      var li = document.createElement('li'), a = document.createElement('a'); a.href = '#' + m[0];
      a.innerHTML = '<i></i><span>' + m[1] + '</span>'; li.appendChild(a); ul.appendChild(li); links[m[0]] = a;
    });
    nav.appendChild(ul); document.body.appendChild(nav);
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { Object.keys(links).forEach(function (k) { links[k].classList.toggle('on', k === e.target.id); }); } });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(links).forEach(function (k) { so.observe(document.getElementById(k)); });
  }
})();
