/* يدير — أدوات مختبر النمو (تعمل بالكامل داخل المتصفح) */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var ROOT = document.body.getAttribute('data-root') || './';
  var WA = document.body.getAttribute('data-wa') || '966534644498';
  var nf = function (n, d) { d = d || 0; return isFinite(n) ? Number(n).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }) : '—'; };
  var val = function (id) { var e = document.getElementById(id); return e ? (parseFloat(e.value) || 0) : 0; };
  var set = function (id, t) { var e = document.getElementById(id); if (e) e.textContent = t; };
  var waUrl = function (t) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(t); };
  var href = function (p) { return ROOT + encodeURI(p); };

  var IC = {
    cart: '<path d="M3 4h3l2.4 11h10.2L21 7H7"/><circle cx="9.5" cy="19" r="1.5"/><circle cx="17.5" cy="19" r="1.5"/>',
    food: '<path d="M6 3v8a3 3 0 003 3v7M10 3v6M6 7h4M17 21V3c-2.5 1.5-3 4.5-3 8h3"/>',
    clinic: '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M12 8v8M8 12h8"/>',
    home: '<path d="M3 11l9-7 9 7v9a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1z"/>',
    edu: '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c3 2.5 9 2.5 12 0v-4.5"/>',
    b2b: '<rect x="3" y="7" width="18" height="13" rx="3"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/>',
    shop: '<path d="M4 9l1.5-5h13L20 9M4 9v11h16V9M4 9a3 3 0 006 0 3 3 0 006 0 3 3 0 004 0"/>',
    target: '<circle cx="11" cy="13" r="8"/><circle cx="11" cy="13" r="3.8"/><path d="M11 13l9.5-9.5M20.5 3.5h-4.2M20.5 3.5v4.2"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    cal: '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    coin: '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.6 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6.5V8M12 16v1.5"/>',
    new: '<path d="M12 3l2.2 5.3 5.8.5-4.4 3.8 1.4 5.6L12 15l-5 3.2 1.4-5.6L4 8.8l5.8-.5z"/>',
    tool: '<path d="M14.5 6.5a4 4 0 005 5L21 13l-8 8-5-5 8-8zM5 15l4 4"/>',
    up: '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    arrow: '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
    browser: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18"/>',
    chat: '<path d="M4 5.5h16v11H10.5L6 20.5v-4H4z"/>',
    pulse: '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>'
  };
  var ico = function (n, s) {
    s = s || 22;
    return '<svg width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (IC[n] || '') + '</svg>';
  };

  /* مزامنة المنزلقات مع الحقول الرقمية */
  $$('.rng[data-for]').forEach(function (r) {
    var inp = document.getElementById(r.getAttribute('data-for'));
    if (!inp) return;
    r.addEventListener('input', function () { inp.value = r.value; inp.dispatchEvent(new Event('input', { bubbles: true })); });
    inp.addEventListener('input', function () { var v = parseFloat(inp.value); if (isFinite(v)) r.value = v; });
  });

  /* نسخ الملخص ومشاركته على واتساب */
  function wire(root, getSummary) {
    $$('[data-copy]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        var t = getSummary(), old = b.innerHTML;
        var done = function () { b.textContent = 'تم النسخ ✓'; setTimeout(function () { b.innerHTML = old; }, 1600); };
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, done); else done();
      });
    });
    $$('[data-wa-share]', root).forEach(function (a) {
      var upd = function () { a.href = waUrl('مرحباً يدير، حسبتُ هذه الأرقام في مختبر النمو وأريد قراءتها معكم:\n\n' + getSummary()); };
      a.addEventListener('mouseenter', upd); a.addEventListener('focus', upd); a.addEventListener('touchstart', upd, { passive: true }); a.addEventListener('click', upd);
      upd();
    });
  }
  function bindInputs(root, fn) { $$('input,select', root).forEach(function (i) { i.addEventListener('input', fn); i.addEventListener('change', fn); }); fn(); }
  function verdict(id, cls, title, sub) {
    var e = document.getElementById(id); if (!e) return;
    e.className = 'verdict ' + cls; e.innerHTML = title + (sub ? '<small>' + sub + '</small>' : '');
  }

  var TOOLS = {};

  /* ───── الحاسبة المصغّرة في الرئيسية ───── */
  TOOLS.mini = function (root) {
    function run() {
      $$('[data-o]', root).forEach(function (o) { var e = document.getElementById(o.getAttribute('data-o')); o.textContent = nf(parseFloat(e.value), parseFloat(e.value) % 1 ? 1 : 0) + ' ' + o.getAttribute('data-u'); });
      var s = val('m-spend'), r = val('m-roas'), m = val('m-margin') / 100;
      var rev = s * r, profit = rev * m - s, be = m > 0 ? 1 / m : Infinity;
      var mx = Math.max(s, rev, Math.abs(profit), 1);
      var setH = function (id, v, neg) { var e = document.getElementById(id); if (e) { e.style.height = Math.max(6, Math.abs(v) / mx * 100) + '%'; e.className = neg ? 'neg' : ''; } };
      setH('mb-spend', s); setH('mb-rev', rev); setH('mb-profit', profit, profit < 0);
      set('m-roas-badge', nf(r, 1) + '×');
      set('m-rev', nf(rev) + ' ر.س'); set('m-profit', (profit < 0 ? '−' : '') + nf(Math.abs(profit)) + ' ر.س');
      var p = document.getElementById('m-profit'); if (p) p.style.color = profit < 0 ? '#8A1C14' : '#00634F';
      set('m-note', profit >= 0 ? 'عائدك ' + nf(r, 1) + ' أعلى من عائد التعادل ' + nf(be, 1) + ': الحملة رابحة بهذه الافتراضات.'
        : 'تحتاج عائداً لا يقل عن ' + nf(be, 1) + ' ضعفاً لتتعادل مع هامش ربحك.');
    }
    bindInputs(root, run);
  };

  /* ───── ROAS ───── */
  TOOLS.roas = function (root) {
    var sum = '';
    function run() {
      var s = val('r-spend'), rev = val('r-rev'), m = val('r-margin') / 100, lift = val('r-lift') / 100;
      var roas = s > 0 ? rev / s : 0, be = m > 0 ? 1 / m : Infinity, profit = rev * m - s, roi = s > 0 ? profit / s * 100 : 0;
      set('r-roas', nf(roas, 2) + '×'); set('r-be', nf(be, 2) + '×'); set('r-profit', (profit < 0 ? '−' : '') + nf(Math.abs(profit))); set('r-roi', nf(roi, 0) + '%');
      if (s <= 0) verdict('r-verdict', '', 'أدخل الإنفاق الإعلاني لنبدأ الحساب', '');
      else if (roas >= be * 1.15) verdict('r-verdict', 'good', 'حملتك رابحة', 'عائدك ' + nf(roas, 2) + '× أعلى من عائد التعادل ' + nf(be, 2) + '×، وربحك الصافي بعد الإعلان ' + nf(profit) + ' ر.س.');
      else if (roas >= be * .95) verdict('r-verdict', 'warn', 'قريبة من التعادل', 'تربح قليلاً أو تتعادل. أي ارتفاع في التكلفة قد يقلبها إلى خسارة.');
      else verdict('r-verdict', 'bad', 'حملتك تخسر بهذه الأرقام', 'لتتعادل تحتاج مبيعات بنحو ' + nf(s * be) + ' ر.س مقابل نفس الإنفاق، أي عائداً ' + nf(be, 2) + '×.');
      var mx = Math.max(roas, be === Infinity ? 1 : be, 1) * 1.08;
      document.getElementById('r-b1').style.width = (roas / mx * 100) + '%';
      document.getElementById('r-b2').style.width = ((be === Infinity ? mx : be) / mx * 100) + '%';
      var np = rev * (1 + lift) * m - s;
      set('r-what', '');
      document.getElementById('r-what').innerHTML = 'لو زادت الطلبات <strong>' + nf(lift * 100) + '%</strong> بنفس الإنفاق: مبيعاتك <strong class="lat">' + nf(rev * (1 + lift)) + '</strong> ر.س وربحك الصافي <strong class="lat">' + (np < 0 ? '−' : '') + nf(Math.abs(np)) + '</strong> ر.س (بدل ' + (profit < 0 ? '−' : '') + nf(Math.abs(profit)) + ').';
      sum = 'الإنفاق الإعلاني: ' + nf(s) + ' ر.س\nالمبيعات: ' + nf(rev) + ' ر.س\nهامش الربح: ' + nf(m * 100) + '%\nROAS: ' + nf(roas, 2) + '× (التعادل ' + nf(be, 2) + '×)\nصافي الربح بعد الإعلان: ' + nf(profit) + ' ر.س';
    }
    wire(root, function () { return sum; }); bindInputs(root, run);
  };

  /* ───── CPA ───── */
  TOOLS.cpa = function (root) {
    var sum = '';
    function run() {
      var price = val('c-price'), cost = val('c-cost'), cpc = val('c-cpc'), cvr = val('c-cvr') / 100, target = val('c-target');
      var unit = price - cost, cpa = cvr > 0 ? cpc / cvr : Infinity, after = unit - cpa;
      var becvr = unit > 0 ? cpc / unit * 100 : Infinity, becpc = unit * cvr;
      set('c-unit', nf(unit, 1)); set('c-cpa', nf(cpa, 1)); set('c-max', nf(Math.max(unit, 0), 1)); set('c-after', (after < 0 ? '−' : '') + nf(Math.abs(after), 1));
      set('c-becvr', becvr === Infinity ? '—' : nf(becvr, 2) + '%'); set('c-becpc', nf(Math.max(becpc, 0), 2));
      if (price <= 0) verdict('c-verdict', '', 'أدخل سعر البيع لنبدأ', '');
      else if (unit <= 0) verdict('c-verdict', 'bad', 'تكلفة المنتج تساوي أو تفوق سعر البيع', 'قبل أي إعلان، راجع التسعير أو التكلفة.');
      else if (after > unit * .15) verdict('c-verdict', 'good', 'تربح على الطلب الأول', 'تدفع ' + nf(cpa, 1) + ' ر.س لكل طلب مقابل ربح ' + nf(unit, 1) + ' ر.س قبل الإعلان.');
      else if (after >= 0) verdict('c-verdict', 'warn', 'هامش ضيق جداً', 'ربحك بعد الإعلان قليل، وأي زيادة في تكلفة النقرة ستخسّرك.');
      else verdict('c-verdict', 'bad', 'تخسر على كل طلب جديد', 'تكلفة الطلب ' + nf(cpa, 1) + ' ر.س أعلى من ربحه ' + nf(unit, 1) + ' ر.س.');
      var need;
      if (after > 0 && target > 0) {
        var orders = Math.ceil(target / after), vis = cvr > 0 ? Math.ceil(orders / cvr) : 0, bud = orders * cpa;
        need = 'تحتاج نحو <strong class="lat">' + nf(orders) + '</strong> طلباً شهرياً، أي ما يقارب <strong class="lat">' + nf(vis) + '</strong> زائراً وميزانية إعلانية بحدود <strong class="lat">' + nf(bud) + '</strong> ر.س.';
      } else if (after > 0) need = 'حدّد ربحاً شهرياً مستهدفاً لنحسب عدد الطلبات والميزانية.';
      else need = 'الربح بعد الإعلان صفر أو سالب. جرّب رفع نسبة التحويل إلى <strong class="lat">' + (becvr === Infinity ? '—' : nf(becvr, 2) + '%') + '</strong> على الأقل، أو خفض تكلفة النقرة إلى <strong class="lat">' + nf(Math.max(becpc, 0), 2) + '</strong> ر.س، أو رفع هامش الربح.';
      document.getElementById('c-need').innerHTML = need;
      sum = 'سعر البيع: ' + nf(price) + ' ر.س | تكلفة الطلب (منتج وتشغيل): ' + nf(cost) + ' ر.س\nCPC: ' + nf(cpc, 2) + ' ر.س | نسبة التحويل: ' + nf(cvr * 100, 2) + '%\nتكلفة الطلب الحالية: ' + nf(cpa, 1) + ' ر.س | أقصى تكلفة مسموحة: ' + nf(Math.max(unit, 0), 1) + ' ر.س\nربح الطلب بعد الإعلان: ' + nf(after, 1) + ' ر.س';
    }
    wire(root, function () { return sum; }); bindInputs(root, run);
  };

  /* ───── LTV ───── */
  TOOLS.ltv = function (root) {
    var sum = '';
    function run() {
      var aov = val('l-aov'), f = val('l-freq'), m = val('l-margin') / 100, y = val('l-years'), cac = val('l-cac');
      var gp = aov * m, ltv = gp * f * y, ratio = cac > 0 ? ltv / cac : 0, pay = gp > 0 ? cac / gp : Infinity;
      set('l-ltv', nf(ltv)); set('l-ratio', nf(ratio, 1) + ' : 1'); set('l-pay', pay === Infinity ? '—' : nf(pay, 1)); set('l-max', nf(ltv / 3));
      if (cac <= 0) verdict('l-verdict', '', 'أدخل تكلفة اكتساب العميل لنبدأ', '');
      else if (ratio >= 3) verdict('l-verdict', 'good', 'اكتساب العميل مجدٍ', 'كل ريال تدفعه لاكتساب عميل يعود بنحو ' + nf(ratio, 1) + ' ريالاً ربحاً على مدى علاقته بك.');
      else if (ratio >= 1) verdict('l-verdict', 'warn', 'ربح محدود', 'تسترد تكلفة الاكتساب لكن بهامش ضيق. ارفع تكرار الشراء أو خفّض التكلفة.');
      else verdict('l-verdict', 'bad', 'تخسر على العميل حتى مدى علاقته', 'القيمة الدائمة ' + nf(ltv) + ' ر.س أقل من تكلفة الاكتساب ' + nf(cac) + ' ر.س.');
      sum = 'متوسط الطلب: ' + nf(aov) + ' ر.س | الطلبات سنوياً: ' + nf(f, 1) + ' | الهامش: ' + nf(m * 100) + '% | مدة العلاقة: ' + nf(y, 1) + ' سنة\nالقيمة الدائمة (ربحاً): ' + nf(ltv) + ' ر.س\nCAC: ' + nf(cac) + ' ر.س → النسبة ' + nf(ratio, 1) + ' : 1';
    }
    wire(root, function () { return sum; }); bindInputs(root, run);
  };

  /* ───── موزّع الميزانية ───── */
  TOOLS.budget = function (root) {
    var CH = [
      { id: 'google', n: 'جوجل (بحث وخرائط وتسوق)', c: '#008F82', paid: 1 }, { id: 'meta', n: 'ميتا (إنستغرام وفيسبوك)', c: '#303032', paid: 1 },
      { id: 'tiktok', n: 'تيك توك', c: '#5CC4B8', paid: 1 }, { id: 'snap', n: 'سناب شات', c: '#8A8A8F', paid: 1 },
      { id: 'influ', n: 'المؤثرون', c: '#B8E5DF', paid: 0 }, { id: 'prod', n: 'الإنتاج والتصميم', c: '#00766B', paid: 0 }, { id: 'test', n: 'ميزانية الاختبار', c: '#C9CED1', paid: 1 }
    ];
    var P = {
      sales_new: [30, 25, 12, 8, 5, 10, 10], sales_run: [32, 28, 12, 8, 6, 6, 8], leads_new: [38, 28, 6, 6, 2, 10, 10],
      leads_run: [40, 30, 6, 6, 2, 6, 10], aware_new: [10, 25, 25, 15, 10, 10, 5], aware_run: [10, 25, 25, 15, 12, 8, 5]
    };
    var pct = [], rows = $('#b-rows'), stack = $('#b-stack'), sum = '';
    function preset() { pct = P[$('#b-goal').value + '_' + $('#b-stage').value].slice(); build(); }
    function build() {
      rows.innerHTML = '';
      CH.forEach(function (c, i) {
        var d = document.createElement('div'); d.className = 'b-row';
        d.innerHTML = '<label for="bp-' + c.id + '"><span class="sw" style="background:' + c.c + '"></span>' + c.n + '</label><span class="pct lat" id="bpp-' + c.id + '"></span><span class="amt" id="bpa-' + c.id + '"></span>' +
          '<input id="bp-' + c.id + '" type="range" min="0" max="100" step="1" value="' + pct[i] + '" aria-label="نسبة ' + c.n + '">';
        rows.appendChild(d);
        d.querySelector('input').addEventListener('input', function (e) { pct[i] = +e.target.value; calc(); });
      });
      calc();
    }
    function calc() {
      var total = val('b-total'), cpc = val('b-cpc'), cvr = val('b-cvr') / 100, s = pct.reduce(function (a, b) { return a + b; }, 0), paid = 0;
      stack.innerHTML = '';
      CH.forEach(function (c, i) {
        var amt = total * pct[i] / 100; if (c.paid) paid += amt;
        set('bpp-' + c.id, pct[i] + '%'); set('bpa-' + c.id, nf(amt) + ' ر.س');
        var seg = document.createElement('i'); seg.style.cssText = 'width:' + (s > 0 ? pct[i] / s * 100 : 0) + '%;background:' + c.c; seg.title = c.n; stack.appendChild(seg);
      });
      var bs = document.getElementById('b-sum');
      bs.className = 'b-sum' + (s === 100 ? '' : ' bad');
      bs.textContent = s === 100 ? 'المجموع 100% ✓' : 'المجموع ' + s + '% — اضغط «تطبيع المجموع إلى 100%» أو عدّل النسب.';
      var clicks = cpc > 0 ? paid / cpc : 0, orders = clicks * cvr;
      set('b-clicks', nf(clicks)); set('b-orders', nf(orders, 1)); set('b-cpa', orders > 0 ? nf(paid / orders, 1) : '—');
      sum = 'الميزانية الشهرية: ' + nf(total) + ' ر.س\n' + CH.map(function (c, i) { return '• ' + c.n + ': ' + pct[i] + '% (' + nf(total * pct[i] / 100) + ' ر.س)'; }).join('\n') + '\nتقدير: ' + nf(clicks) + ' نقرة ≈ ' + nf(orders, 1) + ' نتيجة (CPC ' + nf(cpc, 2) + '، تحويل ' + nf(cvr * 100, 1) + '%)';
    }
    $('#b-goal').addEventListener('change', preset); $('#b-stage').addEventListener('change', preset);
    ['b-total', 'b-cpc', 'b-cvr'].forEach(function (id) { document.getElementById(id).addEventListener('input', calc); });
    $('[data-b-reset]', root).addEventListener('click', preset);
    $('[data-b-norm]', root).addEventListener('click', function () {
      var s = pct.reduce(function (a, b) { return a + b; }, 0); if (!s) return;
      pct = pct.map(function (v) { return Math.round(v / s * 100); });
      var d = 100 - pct.reduce(function (a, b) { return a + b; }, 0); pct[pct.indexOf(Math.max.apply(null, pct))] += d; build();
    });
    wire(root, function () { return sum; }); preset();
  };

  /* ───── معالج: بناء المعالج العام ───── */
  function wizard(root, steps, onDone) {
    var ans = [], i = 0;
    function render() {
      var s = steps[i], pctDone = Math.round(i / steps.length * 100);
      var opts = s.opts.map(function (o, k) {
        return '<button type="button" class="opt" data-k="' + k + '" aria-pressed="' + (ans[i] === k) + '">' + (o.ic ? '<span class="oi">' + ico(o.ic) + '</span>' : '') + '<span>' + o.t + (o.d ? '<small>' + o.d + '</small>' : '') + '</span></button>';
      }).join('');
      root.innerHTML = '<div class="wiz"><div class="wiz-top"><span>' + (s.tag || 'السؤال') + ' ' + (i + 1) + ' من ' + steps.length + '</span><span class="lat">' + pctDone + '%</span></div>' +
        '<div class="wiz-bar"><i style="width:' + pctDone + '%"></i></div><h2>' + s.q + '</h2><div class="opts' + (s.one ? ' one' : '') + '" role="group" aria-label="' + s.q + '">' + opts + '</div>' +
        '<div class="wiz-nav"><button type="button" class="btn btn-ghost btn-sm" data-back' + (i === 0 ? ' disabled style="visibility:hidden"' : '') + '>رجوع</button></div></div>';
      $$('.opt', root).forEach(function (b) {
        b.addEventListener('click', function () {
          ans[i] = +b.getAttribute('data-k'); b.setAttribute('aria-pressed', 'true');
          setTimeout(function () { if (i < steps.length - 1) { i++; render(); focusTop(); } else onDone(ans.slice(), function () { i = 0; ans = []; render(); }); }, 160);
        });
      });
      var bk = $('[data-back]', root); if (bk) bk.addEventListener('click', function () { if (i > 0) { i--; render(); } });
    }
    function focusTop() { var h = $('h2', root); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } }
    render();
  }

  /* ───── مصمم خطة النمو ───── */
  TOOLS.plan = function (root) {
    var SEC = [
      { id: 'store', t: 'متجر إلكتروني', ic: 'cart', w: { meta: 3, google: 3, tiktok: 2, snap: 2, influ: 2 } },
      { id: 'food', t: 'مطعم أو كافيه', ic: 'food', w: { tiktok: 3, snap: 3, meta: 3, influ: 3, google: 2 } },
      { id: 'clinic', t: 'عيادة أو خدمة صحية', ic: 'clinic', w: { google: 3, meta: 3, snap: 1, tiktok: 1 } },
      { id: 'real', t: 'عقارات', ic: 'home', w: { snap: 3, meta: 3, google: 3, tiktok: 1, influ: 1 } },
      { id: 'edu', t: 'تعليم وتدريب', ic: 'edu', w: { meta: 3, tiktok: 2, google: 2, snap: 1 } },
      { id: 'b2b', t: 'شركة خدمات (B2B)', ic: 'b2b', w: { google: 4, meta: 1, influ: 0 } },
      { id: 'local', t: 'محل أو نشاط محلي', ic: 'shop', w: { google: 3, snap: 3, meta: 2, tiktok: 1 } }
    ];
    var GOAL = [
      { id: 'sales', t: 'مبيعات مباشرة', ic: 'cart', k: ['العائد على الإنفاق (ROAS)', 'تكلفة الطلب (CPA)', 'متوسط قيمة الطلب'] },
      { id: 'leads', t: 'استفسارات وعملاء محتملون', ic: 'chat', k: ['تكلفة العميل المحتمل (CPL)', 'نسبة الاستفسارات الجادّة', 'زمن أول رد'] },
      { id: 'aware', t: 'وعي بالعلامة', ic: 'eye', k: ['الوصول الفعلي', 'تكلفة المشاهدة', 'نمو المتابعين المهتمين'] },
      { id: 'book', t: 'حجوزات وزيارات', ic: 'cal', k: ['تكلفة الحجز', 'نسبة الحضور', 'عدد المكالمات والرسائل'] }
    ];
    var BUD = [{ t: 'أقل من 3,000 ر.س شهرياً', n: 1, v: 2000 }, { t: 'من 3,000 إلى 10,000 ر.س', n: 2, v: 6500 }, { t: 'من 10,000 إلى 30,000 ر.س', n: 3, v: 20000 }, { t: 'أكثر من 30,000 ر.س', n: 4, v: 40000 }];
    var STG = [
      { t: 'لا يوجد موقع أو متجر بعد', ic: 'new', d: 'نبدأ من الأساس' }, { t: 'موجود لكن التتبّع غير واضح', ic: 'tool', d: 'لا أعرف من أين تأتي الطلبات' }, { t: 'موجود ومتتبَّع، أريد توسّعاً', ic: 'up', d: 'جاهز للنمو' }
    ];
    var CHN = { google: 'إعلانات جوجل (بحث وخرائط وتسوق)', meta: 'إعلانات ميتا (إنستغرام وفيسبوك)', tiktok: 'تيك توك', snap: 'سناب شات', influ: 'مؤثرون' };
    var steps = [
      { q: 'ما نوع نشاطك؟', tag: 'السؤال', opts: SEC },
      { q: 'ما هدفك الأهم الآن؟', tag: 'السؤال', opts: GOAL },
      { q: 'كم ميزانيتك الإعلانية الشهرية التقريبية؟', tag: 'السؤال', opts: BUD, one: true },
      { q: 'ما وضع موقعك أو متجرك اليوم؟', tag: 'السؤال', opts: STG, one: true }
    ];
    wizard(root, steps, function (a, restart) {
      var sec = SEC[a[0]], goal = GOAL[a[1]], bud = BUD[a[2]], stg = a[3];
      var score = {}; Object.keys(CHN).forEach(function (k) { score[k] = (sec.w[k] || 0) + .2; });
      if (goal.id === 'aware') { score.tiktok += 2; score.snap += 2; score.influ += 2; }
      if (goal.id === 'leads') { score.google += 2; }
      if (goal.id === 'book') { score.google += 2; score.snap += 1; }
      if (goal.id === 'sales') { score.google += 1; score.meta += 1; }
      if (bud.n < 3) score.influ = 0;
      var top = Object.keys(score).sort(function (x, y) { return score[y] - score[x]; }).slice(0, bud.n);
      var tot = top.reduce(function (s, k) { return s + score[k]; }, 0), media = bud.n < 2 ? 85 : 80, used = 0;
      var split = top.map(function (k, i) { var p = i === top.length - 1 ? media - used : Math.round(score[k] / tot * media); used += p; return [CHN[k], p]; });
      split.push(['إنتاج وتصميم واختبار زوايا', 100 - media]);
      var svc = [], add = function (slug, t, why) { if (!svc.some(function (x) { return x[0] === slug; })) svc.push([slug, t, why]); };
      if (stg === 0) add(sec.id === 'store' ? 'تصميم-المتاجر-الالكترونية' : 'تصميم-وبرمجة-المواقع-الالكترونية', sec.id === 'store' ? 'تصميم المتجر الإلكتروني' : 'تصميم وبرمجة الموقع', 'الحملة تحتاج وجهة سريعة تحوّل الزائر؛ نبدؤها قبل الإعلان.');
      if (stg <= 1) add('تحليل-البيانات-والتتبع', 'تحليل البيانات والتتبّع', 'نركّب GA4 والبكسل أولاً حتى تُنسب كل نتيجة إلى مصدرها.');
      add('ادارة-الحملات-الاعلانية', 'إدارة الحملات الإعلانية', 'نختبر الزوايا والجمهور ونراقب الإنفاق يومياً.');
      if (goal.id === 'aware') { add('انتاج-الفيديو-والموشن-جرافيك', 'إنتاج الفيديو القصير', 'المنصات القصيرة تحتاج مقاطع بخطّافات قوية.'); add('التسويق-عبر-المؤثرين', 'التسويق عبر المؤثرين', 'نقيس كل مؤثر برابط وكود.'); }
      else if (goal.id === 'leads' || sec.id === 'b2b' || sec.id === 'clinic') add('تحسين-محركات-البحث', 'تحسين محركات البحث', 'من يبحث عن خدمتك عميل جاهز؛ نظهر له في البحث والخرائط.');
      else add('التسويق-بالبريد-والواتساب', 'التسويق عبر البريد والواتساب', 'إعادة العميل أرخص من اكتساب عميل جديد.');
      if (bud.n < 2 && svc.length < 4) add('ادارة-حسابات-التواصل-الاجتماعي', 'إدارة حسابات التواصل', 'مع ميزانية صغيرة، المحتوى المنتظم يعوّض جزءاً من الإنفاق.');
      svc = svc.slice(0, 4);
      var p1 = stg === 0 ? 'بناء الموقع أو المتجر وصفحة الهبوط، وتركيب التتبّع قبل الإطلاق.' : stg === 1 ? 'تدقيق التتبّع وإصلاحه (GA4 + البكسل) وتحديد خط الأساس: كم نتيجة وبأي تكلفة اليوم.' : 'مراجعة الحسابات الحالية وتحديد أفضل ما يعمل وما يُهدر.';
      var phases = [['الأسابيع 1–2', p1], ['الأسابيع 3–6', 'إطلاق الحملات على ' + top.map(function (k) { return CHN[k].split(' (')[0]; }).join(' و') + '، مع اختبار ثلاث زوايا إعلانية على الأقل.'],
        ['الأسابيع 7–12', 'قراءة الأرقام، ورفع الميزانية على الأفضل، وإضافة مسار جديد (' + (goal.id === 'aware' ? 'مؤثرون أو فيديو' : 'بريد أو واتساب أو سيو') + ').']];
      var txt = 'خطة نمو مبدئية (90 يوماً)\nالنشاط: ' + sec.t + ' | الهدف: ' + goal.t + ' | الميزانية: ' + bud.t + '\nالقنوات: ' + split.map(function (s) { return s[0] + ' ' + s[1] + '%'; }).join('، ') + '\nالخدمات: ' + svc.map(function (s) { return s[1]; }).join('، ');
      root.innerHTML = '<div class="wiz res"><p class="eyebrow">خطتك المبدئية <span class="lat">90 days</span></p><h2>خطة نمو لـ ' + sec.t + ' بهدف «' + goal.t + '»</h2>' +
        '<p class="muted">توصية استرشادية مبنية على قواعد عامة وليست بديلاً عن دراسة سوقك.</p>' +
        '<div class="plan-grid"><div class="pg-card"><h3>القنوات وتوزيع الميزانية</h3><ul>' + split.map(function (s) { return '<li>' + ico('check', 18) + '<span>' + s[0] + ' — <strong class="lat">' + s[1] + '%</strong> (≈ <span class="lat">' + nf(bud.v * s[1] / 100) + '</span> ر.س)</span></li>'; }).join('') + '</ul></div>' +
        '<div class="pg-card"><h3>مؤشراتك للمتابعة</h3><ul>' + goal.k.map(function (k) { return '<li>' + ico('pulse', 18) + '<span>' + k + '</span></li>'; }).join('') + '</ul></div></div>' +
        '<div class="pg-card"><h3>الخدمات المقترحة</h3><ul>' + svc.map(function (s) { return '<li>' + ico('arrow', 18) + '<span><a href="' + href('الخدمات/' + s[0] + '/') + '"><strong>' + s[1] + '</strong></a> — ' + s[2] + '</span></li>'; }).join('') + '</ul></div>' +
        '<div class="pg-card" style="margin-top:16px"><h3>خارطة الطريق</h3>' + phases.map(function (p) { return '<div class="phase"><span class="ph">' + p[0] + '</span><p>' + p[1] + '</p></div>'; }).join('') + '</div>' +
        '<div class="out-actions" style="margin-top:20px"><a class="btn btn-primary" target="_blank" rel="noopener" href="' + waUrl('مرحباً يدير، بنيتُ خطة النمو المبدئية في موقعكم وأريد مناقشتها:\n\n' + txt) + '"><span>ناقش الخطة مع فريقنا</span>' + ico('chat', 18) + '</a>' +
        '<button type="button" class="btn btn-ghost" data-cp>نسخ الملخص</button><button type="button" class="btn btn-ghost" data-rs>أعد المحاولة</button></div></div>';
      $('[data-rs]', root).addEventListener('click', restart);
      $('[data-cp]', root).addEventListener('click', function (e) { var b = e.currentTarget; if (navigator.clipboard) navigator.clipboard.writeText(txt); b.textContent = 'تم النسخ ✓'; });
      root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  };

  /* ───── تشخيص الحضور الرقمي ───── */
  TOOLS.audit = function (root) {
    var PIL = [
      { id: 'search', n: 'الظهور في البحث', svc: ['تحسين-محركات-البحث', 'تحسين محركات البحث'], tip: 'أنشئ صفحة مستقلة لكل خدمة، وسجّل نشاطك في خرائط جوجل ببيانات محدّثة.' },
      { id: 'site', n: 'الموقع والتحويل', svc: ['تصميم-وبرمجة-المواقع-الالكترونية', 'تصميم وبرمجة المواقع'], tip: 'اجعل الموقع سريعاً على الجوال، وضع زر اتصال وواتساب واضحاً في كل صفحة.' },
      { id: 'content', n: 'المحتوى والتواصل', svc: ['ادارة-حسابات-التواصل-الاجتماعي', 'إدارة حسابات التواصل'], tip: 'اكتب خطة محتوى شهرية وحدّد من يردّ على الرسائل والتعليقات.' },
      { id: 'measure', n: 'القياس والتتبّع', svc: ['تحليل-البيانات-والتتبع', 'تحليل البيانات والتتبّع'], tip: 'ركّب GA4 والبكسل واحسب تكلفة اكتساب العميل قبل رفع الإنفاق.' }
    ];
    var Q = [
      [0, 'عند البحث باسم نشاطك ومدينتك في جوجل، هل يظهر موقعك؟'], [0, 'هل لكل خدمة أو منتج رئيسي صفحة مستقلة بعنوان واضح؟'], [0, 'هل نشاطك مسجّل في خرائط جوجل ببيانات محدّثة؟'],
      [1, 'هل يفتح موقعك بسرعة على الجوال (نحو ثلاث ثوانٍ أو أقل)؟'], [1, 'هل زر الاتصال أو الواتساب ظاهر في كل صفحة؟'], [1, 'هل تشرح كل صفحة عرضك وما الخطوة التالية للزائر؟'],
      [2, 'هل لديك خطة محتوى شهرية مكتوبة؟'], [2, 'هل تنشر بانتظام على منصتين على الأقل؟'], [2, 'هل يُردّ على الرسائل والتعليقات خلال ساعات؟'],
      [3, 'هل تتبّع الزيارات والتحويلات (GA4 أو البكسل)؟'], [3, 'هل تعرف تكلفة اكتساب العميل الواحد؟'], [3, 'هل تراجع تقريراً شهرياً بالأرقام؟']
    ];
    var OPT = [{ t: 'نعم', d: 'متحقق بشكل جيد' }, { t: 'جزئياً', d: 'موجود لكن ناقص' }, { t: 'لا', d: 'غير موجود' }];
    var steps = Q.map(function (q) { return { q: q[1], tag: 'السؤال', opts: OPT.map(function (o) { return { t: o.t, d: o.d }; }), one: true }; });
    wizard(root, steps, function (a, restart) {
      var sc = [0, 0, 0, 0], total = 0;
      a.forEach(function (v, i) { var pts = 2 - v; sc[Q[i][0]] += pts; total += pts; });
      var pctT = Math.round(total / 24 * 100), lvl = pctT >= 80 ? 'متقدم' : pctT >= 60 ? 'جيد' : pctT >= 35 ? 'ناشئ' : 'مبتدئ';
      var order = [0, 1, 2, 3].sort(function (x, y) { return sc[x] - sc[y]; });
      var pil = PIL.map(function (p, i) { var pc = Math.round(sc[i] / 6 * 100); return '<div class="pillar"><span>' + p.n + '</span><div class="bar"><i style="width:' + pc + '%"></i></div><span class="lat">' + pc + '%</span></div>'; }).join('');
      var recs = order.slice(0, 3).filter(function (i) { return sc[i] < 6; }).map(function (i) {
        var p = PIL[i], pc = Math.round(sc[i] / 6 * 100);
        return '<div class="rec"><span class="oi">' + ico(['search', 'browser', 'chat', 'pulse'][i], 20) + '</span><div><h3>' + p.n + ' — ' + (pc < 50 ? 'أولوية عالية' : 'يحتاج تحسيناً') + '</h3><p>' + p.tip + ' <a href="' + href('الخدمات/' + p.svc[0] + '/') + '">خدمة ' + p.svc[1] + '</a></p></div></div>';
      }).join('') || '<div class="rec"><span class="oi">' + ico('check', 20) + '</span><div><h3>وضع ممتاز</h3><p>حافظ على ما أنجزته وابدأ بتوسيع القنوات.</p></div></div>';
      var txt = 'نتيجة تشخيص الحضور الرقمي: ' + pctT + '/100 (' + lvl + ')\n' + PIL.map(function (p, i) { return '• ' + p.n + ': ' + Math.round(sc[i] / 6 * 100) + '%'; }).join('\n');
      root.innerHTML = '<div class="wiz res"><p class="eyebrow">نتيجتك <span class="lat">Score</span></p><h2>مستوى حضورك الرقمي: ' + lvl + '</h2>' +
        '<div class="score"><div class="ring" style="--v:' + pctT + '"><b>' + pctT + '</b></div><div class="pillars">' + pil + '</div></div>' +
        '<h3 class="h4">أولوياتك المقترحة</h3><div class="recs">' + recs + '</div><p class="muted">تقدير ذاتي سريع، وليس فحصاً تقنياً لموقعك.</p>' +
        '<div class="out-actions"><a class="btn btn-primary" target="_blank" rel="noopener" href="' + waUrl('مرحباً يدير، أجريتُ تشخيص الحضور الرقمي وأريد خطة لتحسينه:\n\n' + txt) + '"><span>اطلب خطة التحسين</span>' + ico('chat', 18) + '</a>' +
        '<button type="button" class="btn btn-ghost" data-rs>أعد الاختبار</button></div></div>';
      $('[data-rs]', root).addEventListener('click', restart);
      root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  };

  $$('[data-tool]').forEach(function (el) { var f = TOOLS[el.getAttribute('data-tool')]; if (f) f(el); });
})();
