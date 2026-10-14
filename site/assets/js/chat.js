/* مساعد شركة يدير — مساعد محادثة يعمل بالكامل داخل المتصفح (قواعد + قاعدة معرفة)
   لا يرسل أي نص إلى خادم. عند الحاجة يحوّل المحادثة إلى واتساب برسالة جاهزة. */
(function () {
  'use strict';
  var root = document.getElementById('yd-chat');
  var opener = document.querySelector('[data-chat-open]');
  if (!root || !opener) return;
  var ROOT = document.body.getAttribute('data-root') || './';
  var log = root.querySelector('.chat-log'), chips = root.querySelector('.chat-chips'), form = root.querySelector('.chat-f'), input = root.querySelector('#chat-in');
  var KB = null, started = false, flow = null;

  var norm = function (s) {
    return (s || '').toLowerCase().replace(/[ً-ْـ]/g, '').replace(/[أإآٱ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/[^؀-ۿa-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  };
  var link = function (u, t) { return '<a href="' + ROOT + encodeURI(u) + '">' + t + '</a>'; };
  var waUrl = function (t) { return 'https://wa.me/' + (KB ? KB.wa : '966534644498') + '?text=' + encodeURIComponent(t); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  function loadKB(cb) {
    if (KB) return cb();
    fetch(ROOT + 'assets/data/kb.json').then(function (r) { return r.json(); }).then(function (j) { KB = j; cb(); }).catch(function () {
      KB = { phone: '0534644498', tel: 'tel:+966534644498', wa: '966534644498', cr: '7028759400', vat: '311270053300003', social: { tiktok: 'https://www.tiktok.com/@yadeer_agency', x: 'https://x.com/Yadeer_Agency', instagram: 'https://www.instagram.com/yadeer_agency/' }, services: [], tools: [], posts: [] }; cb();
    });
  }

  function add(kind, html, isText) {
    var d = document.createElement('div'); d.className = 'msg ' + kind;
    if (isText) d.textContent = html; else d.innerHTML = html;
    log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
  }
  function setChips(list) {
    chips.innerHTML = '';
    list.forEach(function (c) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = c; b.addEventListener('click', function () { ask(c); }); chips.appendChild(b);
    });
  }
  function bot(html, next, delay) {
    var t = add('bot', '<span class="typing" aria-label="يكتب"><i></i><i></i><i></i></span>');
    setTimeout(function () { t.innerHTML = html; log.scrollTop = log.scrollHeight; if (next) setChips(next); }, delay || 380);
  }

  var HOME = ['الخدمات', 'الأدوات المجانية', 'اطلب عرض سعر', 'التواصل'];

  function svcList(group) {
    var l = KB.services.filter(function (s) { return !group || s.g === group; });
    return '<ul>' + l.map(function (s) { return '<li>' + link(s.u, esc(s.t)) + '</li>'; }).join('') + '</ul>';
  }
  function findServices(n) {
    var hits = [];
    KB.services.forEach(function (s) {
      var sc = 0, words = norm(s.k + ' ' + s.t).split(' ');
      words.forEach(function (w) { if (w.length > 2 && n.indexOf(w.replace(/^ال/, '')) > -1) sc++; });
      if (sc) hits.push([sc, s]);
    });
    hits.sort(function (a, b) { return b[0] - a[0]; });
    return hits.slice(0, 2).map(function (h) { return h[1]; });
  }
  var has = function (n, words) { return words.some(function (w) { return n.indexOf(w) > -1; }); };

  function answer(text) {
    var n = norm(text);
    if (flow) return runFlow(text, n);
    if (has(n, ['شكرا', 'مشكور', 'يعطيك العافيه', 'تسلم'])) return bot('العفو، يسعدنا خدمتك. إن احتجت شيئاً آخر فأنا هنا.', HOME);
    if (has(n, ['عرض سعر', 'عرض اسعار', 'اطلب عرض', 'طلب عرض', 'عرض مالي'])) return startQuote();
    if (has(n, ['سعر', 'اسعار', 'تكلفه', 'كم تكلف', 'كم يكلف', 'بكم', 'ثمن', 'باقه', 'باقات']))
      return bot('<p>السعر يعتمد على نطاق العمل والمدة وعدد القنوات، لذلك نرسل <strong>عرضاً مكتوباً بكل البنود</strong> بعد جلسة قصيرة معك.</p><p>لتقدير تقريبي لميزانيتك الإعلانية جرّب ' + link('مختبر-النمو/موزع-الميزانية-الاعلانية/', 'موزّع الميزانية') + '.</p>', ['اطلب عرض سعر', 'الأدوات المجانية', 'التواصل']);
    if (has(n, ['واتس', 'اتصال', 'اتصل', 'جوال', 'رقم', 'تواصل', 'كلمني', 'اكلمكم', 'ايميل', 'بريد']) && !has(n, ['رقم ضريب', 'رقم تجاري', 'سجل'])) return contact();
    if (has(n, ['تيك توك', 'تيكتوك', 'انستقرام', 'انستغرام', 'تويتر', 'حساباتكم', 'سوشيال']) && has(n, ['حساب', 'رابط', 'تابع', 'اين', 'وين', 'تيك', 'انست', 'تويتر', 'اكس'])) return social();
    if (has(n, ['سجل', 'ضريب', 'تجاري', 'موثق', 'رسمي', 'رخصه', 'توثيق']))
      return bot('<p>بيانات المنشأة الرسمية:</p><ul><li>السجل التجاري: <strong class="lat">' + KB.cr + '</strong></li><li>الرقم الضريبي: <strong class="lat">' + KB.vat + '</strong></li></ul>', HOME);
    if (has(n, ['ضمان', 'تضمن', 'مضمون', 'نتيجه مضمونه']))
      return bot('<p>لا يصحّ ضمان مبيعات أو ترتيب في البحث لأنها تتأثر بالسوق والمنافسة.</p><p>ما نلتزم به: <strong>خطة واضحة، تتبّع دقيق، وتقارير شفافة</strong> تربط الإنفاق بالنتائج.</p>', ['اطلب عرض سعر', 'طريقة العمل']);
    if (has(n, ['طريقه العمل', 'كيف تعمل', 'خطوات', 'مراحل', 'كيف نبدا', 'كيف ابدا'])) return bot('<p>نعمل بأربع خطوات:</p><ul><li>استشارة مجانية</li><li>خطة وعرض سعر مكتوب</li><li>تنفيذ وإطلاق</li><li>قياس وتحسين بتقرير دوري</li></ul>', ['اطلب عرض سعر', 'الأدوات المجانية']);
    if (has(n, ['خصوصيه', 'بياناتي', 'سياسه']) ) return bot('<p>نحترم خصوصيتك. اطّلع على ' + link('سياسة-الخصوصية/', 'سياسة الخصوصية') + ' و' + link('شروط-الاستخدام/', 'شروط الاستخدام') + '. ما تكتبه هنا يبقى في متصفحك ولا يُرسل إلا إذا اخترت واتساب.</p>', HOME);
    if (has(n, ['ادوات', 'اداه', 'حاسبه', 'حاسبات', 'مختبر', 'احسب', 'roas', 'cpa', 'ltv', 'تشخيص', 'خطه نمو', 'خطه تسويق']) && !has(n, ['اتمته']))
      return bot('<p>مختبر النمو يضم أدوات مجانية بلا تسجيل:</p><ul>' + KB.tools.map(function (t) { return '<li>' + link(t.u, esc(t.t)) + '</li>'; }).join('') + '</ul>', ['اطلب عرض سعر', 'الخدمات']);
    if (has(n, ['مقال', 'مدونه', 'اقرا', 'نصيحه', 'نصائح'])) return bot('<p>من المدونة:</p><ul>' + KB.posts.slice(0, 4).map(function (p) { return '<li>' + link(p.u, esc(p.t)) + '</li>'; }).join('') + '</ul><p>' + link('المدونة/', 'كل المقالات') + '</p>', HOME);
    if (has(n, ['من انتم', 'من نحن', 'عن الشركه', 'عنكم', 'تعريف', 'ماهي يدير', 'ما هي يدير'])) return bot('<p><strong>يدير للتسويق الإلكتروني</strong> وكالة تسويق إلكتروني وحلول تقنية. نبدأ من هدفك ورقمك، ونجمع التسويق والتقنية تحت سقف واحد.</p><p>' + link('من-نحن/', 'المزيد عنا') + '</p>', HOME);
    if (has(n, ['موظف', 'مختص', 'شخص', 'مستشار', 'بشري', 'انسان'])) return bot('<p>بالتأكيد. يمكنك مراسلة فريقنا مباشرة:</p><p><a href="' + waUrl('مرحباً يدير، أرغب في التحدث مع مختص.') + '" target="_blank" rel="noopener">فتح محادثة واتساب</a> أو الاتصال على <a href="' + KB.tel + '"><span class="lat">' + KB.phone + '</span></a></p>', HOME);
    if (has(n, ['ساعات', 'دوام', 'مواعيد', 'متى ترد', 'وقت الرد'])) return bot('<p>اكتب لنا على واتساب في أي وقت ونردّ عليك في أقرب فرصة.</p>', ['التواصل', 'اطلب عرض سعر']);
    if (has(n, ['خدمات', 'خدماتكم', 'ماذا تقدمون', 'وش تقدمون', 'ايش تقدمون', 'تقدمون', 'عندكم', 'تسوقون']) && !findServices(n).length) return services();
    var f = findServices(n);
    if (f.length) return bot('<p>هذا أقرب ما يخدم سؤالك:</p><ul>' + f.map(function (s) { return '<li>' + link(s.u, '<strong>' + esc(s.t) + '</strong>') + ' — ' + esc(s.d) + '</li>'; }).join('') + '</ul>', ['اطلب عرض سعر', 'الخدمات', 'الأدوات المجانية']);
    if (has(n, ['مرحبا', 'اهلا', 'السلام', 'هلا', 'صباح', 'مساء', 'هاي', 'hello', 'hi'])) return bot('أهلاً وسهلاً بك. كيف أساعدك اليوم؟', HOME);
    if (has(n, ['خدمات', 'خدماتكم'])) return services();
    if (has(n, ['ابغي', 'ابي', 'اريد', 'احتاج', 'ابدا', 'ودي', 'عندي مشروع', 'مشروع'])) return bot('<p>يسعدنا ذلك. أخبرني بالخدمة التي تحتاجها (مثل: إعلانات، موقع، متجر، سيو…) أو اطلب عرض سعر مباشرة.</p>', ['اطلب عرض سعر', 'الخدمات', 'الأدوات المجانية']);
    bot('<p>لم أفهم سؤالك تماماً. يمكنني مساعدتك في الخدمات والأدوات المجانية وطلب عرض السعر والتواصل.</p><p>أو تحدّث مع فريقنا: <a href="' + waUrl('مرحباً يدير، لدي سؤال: ' + text) + '" target="_blank" rel="noopener">واتساب</a></p>', HOME);
  }

  function services() {
    return bot('<p>خدماتنا في مجموعتين:</p><p><strong>تسويقية</strong></p>' + svcList('marketing') + '<p><strong>تقنية</strong></p>' + svcList('tech'), ['اطلب عرض سعر', 'الأدوات المجانية', 'التواصل'], 450);
  }
  function contact() {
    return bot('<p>يسعدنا تواصلك:</p><ul><li>اتصال: <a href="' + KB.tel + '"><strong class="lat">' + KB.phone + '</strong></a></li><li><a href="' + waUrl('مرحباً يدير، أرغب في الاستفسار.') + '" target="_blank" rel="noopener">واتساب</a></li><li>' + link('تواصل-معنا/', 'صفحة التواصل ونموذج الطلب') + '</li></ul>', ['حساباتكم', 'اطلب عرض سعر']);
  }
  function social() {
    return bot('<p>حساباتنا:</p><ul><li><a href="' + KB.social.instagram + '" target="_blank" rel="noopener me">إنستغرام</a></li><li><a href="' + KB.social.tiktok + '" target="_blank" rel="noopener me">تيك توك</a></li><li><a href="' + KB.social.x + '" target="_blank" rel="noopener me">إكس</a></li></ul>', HOME);
  }

  /* تدفق طلب عرض السعر */
  function startQuote() { flow = { step: 'name', d: {} }; return bot('بكل سرور. ما اسمك؟', ['إلغاء']); }
  function runFlow(text, n) {
    if (n === 'الغاء' || n === 'إلغاء') { flow = null; return bot('تم الإلغاء. كيف أساعدك؟', HOME); }
    if (flow.step === 'name') {
      flow.d.name = text.trim().slice(0, 60); flow.step = 'svc';
      var pop = KB.services.slice(0, 4).map(function (s) { return s.t; }).concat(['خدمة أخرى']);
      return bot('أهلاً ' + esc(flow.d.name) + '. ما الخدمة التي تهمّك؟ اختر أو اكتبها.', pop.concat(['إلغاء']));
    }
    if (flow.step === 'svc') { flow.d.svc = text.trim().slice(0, 100); flow.step = 'note'; return bot('وما هدفك باختصار؟ (مثال: زيادة مبيعات متجر، موقع جديد…) أو اكتب «تخطّي».', ['تخطّي', 'إلغاء']); }
    if (flow.step === 'note') {
      var note = /^(تخطي|تخطّي)$/.test(norm(text)) ? '' : text.trim().slice(0, 300), d = flow.d; flow = null;
      var msg = 'مرحباً يدير، اسمي ' + d.name + '. أرغب في عرض سعر لخدمة: ' + d.svc + '.' + (note ? '\nهدفي: ' + note : '');
      return bot('<p>شكراً ' + esc(d.name) + '. أصبحت رسالتك جاهزة:</p><p><a class="btn btn-primary btn-sm" style="color:#fff" href="' + waUrl(msg) + '" target="_blank" rel="noopener"><span>أرسلها عبر واتساب</span></a></p><p class="muted">نردّ عليك بخطة مختصرة وعرض مكتوب.</p>', HOME);
    }
  }

  function ask(text) {
    if (!text) return;
    add('me', text, true);
    if (text === 'الخدمات') return services();
    if (text === 'التواصل') return contact();
    if (text === 'حساباتكم') return social();
    if (text === 'اطلب عرض سعر' && !flow) return startQuote();
    if (text === 'طريقة العمل') return answer('طريقة العمل');
    if (text === 'الأدوات المجانية') return answer('ادوات');
    answer(text);
  }

  function start() {
    if (started) return; started = true;
    loadKB(function () {
      add('bot', '<p><strong>أهلاً بك في مساعد شركة يدير.</strong></p><p>أجيب عن الخدمات والأدوات المجانية، وأجهّز لك طلب عرض سعر، وأحوّلك إلى فريقنا عند الحاجة.</p>');
      setChips(HOME);
    });
  }
  function open() {
    root.hidden = false; root.classList.add('pop'); opener.setAttribute('aria-expanded', 'true'); start();
    setTimeout(function () { input.focus(); }, 60);
  }
  function close() { root.hidden = true; opener.setAttribute('aria-expanded', 'false'); opener.focus(); }

  opener.addEventListener('click', function () { if (root.hidden) open(); else close(); });
  root.querySelector('[data-chat-close]').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !root.hidden) close(); });
  form.addEventListener('submit', function (e) {
    e.preventDefault(); var t = input.value.trim(); if (!t) return; input.value = '';
    loadKB(function () { ask(t); });
  });
  window.addEventListener('hashchange', function () { if (location.hash === '#chat') open(); });
  if (location.hash === '#chat') open();
})();
