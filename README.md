# موقع يدير للتسويق الإلكتروني

موقع ثابت (Static) عربي RTL، جاهز للفهرسة، بصفحة لكل خدمة، ومختبر أدوات تفاعلية، ومساعد محادثة.
الهوية: Teal `#008F82` · Charcoal `#303032` · Light Teal `#B8E5DF` · Off-white `#FAFAFA` — خطوط Cairo وOutfit (مستضافة محلياً).

## البنية
```
site/                 ← مجلد النشر (انشره كما هو على أي استضافة ثابتة)
  index.html …        ← صفحات بروابط عربية: /الخدمات/<خدمة>/ ، /مختبر-النمو/<أداة>/ ، /المدونة/<مقال>/
  sitemap.xml · robots.txt · site.webmanifest · _headers
  assets/{css,js,img,fonts,data}
tools/                ← المولّد (Python) وصور OG (Node + Playwright)
  content_services.py ← محتوى 18 خدمة
  content_misc.py     ← بيانات المنشأة، الأدوات، المقالات، القاموس، الصفحات القانونية
  build.py · lib.py · layout.py
```

## إعادة البناء
```bash
SITE_URL=https://your-domain.com python3 tools/build.py      # يولّد كل الصفحات و sitemap و canonical بنطاقك
NODE_PATH=/opt/node22/lib/node_modules node tools/og.mjs      # يولّد صور المشاركة OG والأيقونات
```
> **مهم:** غيّر `SITE_URL` إلى نطاقك الفعلي قبل النشر (الافتراضي `https://yadeer.sa` مثال فقط)، ثم أعد البناء.

## بعد النشر
1. أضف الموقع إلى Google Search Console وأرسل `https://نطاقك/sitemap.xml`.
2. أضف Google Analytics / Pixel عند الجاهزية (ويُحدَّث نص سياسة الخصوصية وموافقة ملفات الارتباط حسب ما يُفعَّل).
3. راجع نصوص الخصوصية والشروط مع مستشار قانوني.

## التعديل
- أرقام التواصل والسجل والضريبة وروابط السوشيال: `tools/content_misc.py` (قاموس `SITE`).
- نصوص الخدمات: `tools/content_services.py`. المقالات والقاموس: `tools/content_misc.py`.
- مساعد الموقع: قواعد ومعرفة داخل `site/assets/js/chat.js` و `site/assets/data/kb.json` (يُولَّد تلقائياً).

## الاختبار
```bash
npx http-server site -p 8099 -s &
NODE_PATH=/opt/node22/lib/node_modules node tools/test.mjs    # أدوات، مساعد، روابط، أخطاء كونسول لكل الصفحات
```
