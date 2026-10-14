/* يدير — السلوك العام للموقع */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* السنة */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* زر المساعد: يُظهر اسمه أولاً ثم ينكمش على الشاشات الكبيرة */
  var dc = $('.dock-chat');
  if (dc && window.matchMedia('(min-width:641px)').matches) setTimeout(function () { dc.classList.add('mini'); }, 7000);

  /* قائمة الجوال */
  var btn = $('[data-menu-btn]'), nav = $('#nav');
  function setMenu(open) {
    if (!btn || !nav) return;
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  if (btn) btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });

  /* قائمة الخدمات */
  $$('[data-dd]').forEach(function (dd) {
    var b = $('.nav-link', dd);
    function set(o) { dd.classList.toggle('open', o); b.setAttribute('aria-expanded', o ? 'true' : 'false'); }
    b.addEventListener('click', function (e) { e.stopPropagation(); set(!dd.classList.contains('open')); });
    if (window.matchMedia('(hover:hover) and (min-width:921px)').matches) {
      var t;
      dd.addEventListener('mouseenter', function () { clearTimeout(t); set(true); });
      dd.addEventListener('mouseleave', function () { t = setTimeout(function () { set(false); }, 160); });
    }
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { set(false); setMenu(false); } });
  });
  if (nav) nav.addEventListener('click', function (e) { if (e.target.closest('a') && !e.target.closest('[data-dd] .nav-link')) setMenu(false); });

  /* ظهور تدريجي */
  var rv = $$('.rv');
  if ('IntersectionObserver' in window && rv.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  /* شريط التقدم */
  var bar = $('.progress');
  if (bar) {
    var tick = false;
    var upd = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty('--p', (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%');
      tick = false;
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }

  /* جدول المحتويات: تمييز القسم الحالي */
  var tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('on'); }); var a = map[e.target.id]; if (a) a.classList.add('on'); }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) so.observe(el); });
  }

  /* القاموس: بحث فوري */
  var q = $('#gl-q');
  if (q) {
    var items = $$('.term'), n = $('#gl-n'), empty = $('#gl-empty');
    var norm = function (s) { return (s || '').toLowerCase().replace(/[ً-ْـ]/g, '').replace(/[أإآ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه'); };
    var run = function () {
      var v = norm(q.value.trim()), c = 0;
      items.forEach(function (it) {
        var hit = !v || norm(it.getAttribute('data-t')).indexOf(v) > -1;
        it.hidden = !hit; if (hit) c++;
      });
      n.textContent = v ? c + ' نتيجة' : '';
      empty.hidden = c !== 0;
    };
    q.addEventListener('input', run);
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.classList.add('hit'); }
  }

  /* نموذج التواصل → واتساب */
  var form = $('[data-wa-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form), lines = ['مرحباً يدير،'];
      lines.push('اسمي: ' + (f.get('name') || '').toString().trim());
      if (f.get('phone')) lines.push('رقم جوالي: ' + f.get('phone').toString().trim());
      if (f.get('svc')) lines.push('الخدمة المطلوبة: ' + f.get('svc'));
      if (f.get('msg')) lines.push('عن مشروعي: ' + f.get('msg').toString().trim());
      var wa = document.body.getAttribute('data-wa') || '966534644498';
      window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }
})();
