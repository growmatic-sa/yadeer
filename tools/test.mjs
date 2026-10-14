// اختبارات وظيفية للأدوات والمساعد وفحص الأخطاء على كل الصفحات (يتطلب خادماً على المنفذ 8099)
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const B = process.env.BASE || 'http://localhost:8099';
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
let fail = 0;
const ok = (c, m) => { if (!c) { fail++; console.log('✗', m); } else console.log('✓', m); };
const txt = (p, s) => p.$eval(s, e => e.textContent.trim());

// 1) أخطاء الكونسول وروابط مكسورة على كل الصفحات
const sm = fs.readFileSync(new URL('../site/sitemap.xml', import.meta.url), 'utf8');
const urls = [...sm.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1].replace(/^https?:\/\/[^/]+/, ''));
const bad = new Set();
for (const u of urls) {
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('requestfailed', r => errs.push('REQFAIL ' + r.url()));
  const r = await p.goto(B + u, { waitUntil: 'load' });
  if (r.status() !== 200) errs.push('HTTP ' + r.status());
  const hrefs = await p.$$eval('a[href]', a => a.map(x => x.getAttribute('href')).filter(h => h && !h.startsWith('http') && !h.startsWith('tel:') && !h.startsWith('mailto:') && !h.startsWith('#') && !h.startsWith('javascript')));
  for (const h of new Set(hrefs)) { const full = new URL(h, B + u).href; const rr = await ctx.request.get(full); if (rr.status() !== 200) bad.add(u + ' → ' + h + ' ' + rr.status()); }
  const h1 = await p.$$eval('h1', e => e.length);
  if (h1 !== 1) errs.push('h1 count ' + h1);
  if (errs.length) { fail++; console.log('✗', u, errs.slice(0, 4)); }
  await p.close();
}
console.log(`فحص ${urls.length} صفحة`); bad.forEach(x => { fail++; console.log('✗ broken', x); });

// 2) الأدوات
let p = await ctx.newPage();
await p.goto(B + '/مختبر-النمو/حاسبة-العائد-على-الانفاق-الاعلاني/');
ok((await txt(p, '#r-roas')).startsWith('3.60'), 'ROAS = 3.60 → ' + await txt(p, '#r-roas'));
ok((await txt(p, '#r-be')).startsWith('3.33'), 'break-even 3.33');
ok(await p.$eval('#r-verdict', e => e.classList.contains('warn')), 'ROAS verdict warn');
await p.fill('#r-rev', '30000'); ok(await p.$eval('#r-verdict', e => e.classList.contains('good')), 'ROAS verdict good after revenue 30000');
await p.fill('#r-rev', '10000'); ok(await p.$eval('#r-verdict', e => e.classList.contains('bad')), 'ROAS verdict bad');
await p.goto(B + '/مختبر-النمو/حاسبة-تكلفة-اكتساب-العميل/');
ok((await txt(p, '#c-cpa')).startsWith('60'), 'CPA = 60 → ' + await txt(p, '#c-cpa'));
ok((await txt(p, '#c-after')).startsWith('70'), 'profit after ads = 70');
ok(/143/.test(await txt(p, '#c-need')), 'orders needed 143 → ' + (await txt(p, '#c-need')).slice(0, 60));
await p.goto(B + '/مختبر-النمو/حاسبة-القيمة-الدائمة-للعميل/');
ok((await txt(p, '#l-ltv')).startsWith('700'), 'LTV = 700'); ok((await txt(p, '#l-ratio')).startsWith('7.8'), 'ratio 7.8');
await p.goto(B + '/مختبر-النمو/موزع-الميزانية-الاعلانية/');
ok((await txt(p, '#b-sum')).includes('100%'), 'budget sums to 100 → ' + await txt(p, '#b-sum'));
await p.selectOption('#b-goal', 'aware'); ok((await txt(p, '#bpp-tiktok')) === '25%', 'aware preset tiktok 25%');
await p.fill('#b-total', '20000'); ok((await txt(p, '#bpa-google')).startsWith('2,000'), 'google 10% of 20000 → ' + await txt(p, '#bpa-google'));
await p.goto(B + '/مختبر-النمو/مصمم-خطة-النمو/');
for (let i = 0; i < 4; i++) { await p.click('.opt >> nth=1'); await p.waitForTimeout(260); }
ok(await p.$('.plan-grid') !== null, 'plan result rendered'); ok((await p.$$('.pg-card li a')).length >= 3, 'plan lists services');
ok((await p.$$eval('.res a[href*="wa.me"]', a => a.length)) >= 1, 'plan WA link');
await p.goto(B + '/مختبر-النمو/تشخيص-الحضور-الرقمي/');
for (let i = 0; i < 12; i++) { await p.click('.opt >> nth=0'); await p.waitForTimeout(260); }
ok((await txt(p, '.ring b')) === '100', 'audit score 100 → ' + await txt(p, '.ring b'));
await p.click('[data-rs]'); await p.waitForTimeout(200);
for (let i = 0; i < 12; i++) { await p.click('.opt >> nth=2'); await p.waitForTimeout(260); }
ok((await txt(p, '.ring b')) === '0', 'audit score 0'); ok((await p.$$('.rec')).length === 3, 'audit 3 recs');
await p.goto(B + '/');
await p.fill('#m-spend', '10000'); ok((await txt(p, '#m-rev')).startsWith('40,000'), 'mini rev 40,000 → ' + await txt(p, '#m-rev'));
await p.goto(B + '/قاموس-التسويق/'); await p.fill('#gl-q', 'roas');
ok((await p.$$eval('.term:not([hidden])', e => e.length)) >= 1 && (await p.$$eval('.term:not([hidden])', e => e.length)) < 5, 'glossary filter');
await p.fill('#gl-q', 'xyzxyz'); ok(await p.$eval('#gl-empty', e => !e.hidden), 'glossary empty state');

// 3) المساعد
await p.goto(B + '/'); await p.click('[data-chat-open]'); await p.waitForTimeout(900);
ok(await p.$eval('#yd-chat', e => !e.hidden), 'chat opens'); ok((await p.$$('.chat-chips button')).length === 4, 'chat chips');
async function say(q) { await p.fill('#chat-in', q); await p.press('#chat-in', 'Enter'); await p.waitForTimeout(900); return p.$$eval('.msg.bot', m => m[m.length - 1].textContent); }
let a = await say('وش خدماتكم'); ok(a.includes('مجموعتين'), 'chat services');
a = await say('كم الاسعار'); ok(a.includes('عرضاً مكتوباً'), 'chat price');
a = await say('ابغى اعلانات سناب'); ok(a.includes('إدارة الحملات الإعلانية'), 'chat ads match → ' + a.slice(0, 60));
a = await say('ابي موقع'); ok(a.includes('المواقع') , 'chat website match → ' + a.slice(0, 80));
a = await say('رقمكم'); ok(a.includes('0534644498'), 'chat contact');
a = await say('السجل التجاري'); ok(a.includes('7028759400') && a.includes('311270053300003'), 'chat CR/VAT');
a = await say('تيك توك'); ok(a.includes('تيك توك'), 'chat social');
a = await say('اريد عرض سعر'); ok(a.includes('ما اسمك'), 'chat quote start');
await p.fill('#chat-in', 'خالد'); await p.press('#chat-in', 'Enter'); await p.waitForTimeout(900);
await p.fill('#chat-in', 'متجر'); await p.press('#chat-in', 'Enter'); await p.waitForTimeout(900);
await p.fill('#chat-in', 'زيادة مبيعات'); await p.press('#chat-in', 'Enter'); await p.waitForTimeout(900);
const wa = await p.$$eval('.msg.bot a[href*="wa.me"]', a => a.map(x => decodeURIComponent(x.href)).pop());
ok(wa && wa.includes('خالد') && wa.includes('966534644498'), 'quote WA link → ' + (wa || '').slice(0, 80));
a = await say('asdfgh'); ok(a.includes('لم أفهم'), 'chat fallback');
await p.keyboard.press('Escape'); ok(await p.$eval('#yd-chat', e => e.hidden), 'chat closes on Esc');
// نموذج التواصل
await p.goto(B + '/تواصل-معنا/'); await p.fill('#f-name', 'سارة'); await p.fill('#f-phone', '0500000000');
const [pop] = await Promise.all([ctx.waitForEvent('page'), p.click('form button[type=submit]')]);
ok(decodeURIComponent(pop.url()).includes('سارة') && pop.url().includes('966534644498'), 'contact form → WhatsApp');
await b.close(); console.log(fail ? `\n${fail} فشل` : '\nكل الاختبارات نجحت'); process.exit(fail ? 1 : 0);
