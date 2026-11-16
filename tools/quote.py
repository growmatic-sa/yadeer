# -*- coding: utf-8 -*-
"""يولّد عرض سعر PDF بهوية يدير. الاستخدام: python3 tools/quote.py <ملف_json> <خرج.pdf>"""
import json, os, subprocess, sys, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
e = html.escape
q = json.load(open(sys.argv[1], encoding="utf-8"))
out = os.path.abspath(sys.argv[2])
price = q["monthly"]; vat = round(price * 0.15, 2); total = price + vat
f = lambda n: f"{n:,.2f}"
svc = "".join(
    f'<div class="svc"><div class="sh"><span class="n">{i+1}</span><h3>{e(s["title"])}</h3></div><ul>{"".join(f"<li>{e(x)}</li>" for x in s["items"])}</ul></div>'
    for i, s in enumerate(q["services"]))
notes = "".join(f"<li>{e(x)}</li>" for x in q["notes"])
FONT = f"file://{ROOT}/site/assets/fonts"
page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:Cairo;font-weight:300 900;src:url({FONT}/cairo-arabic.woff2) format('woff2');unicode-range:U+0600-06FF,U+200C-200E,U+2010-2011,U+FB50-FDFF,U+FE70-FEFC}}
@font-face{{font-family:Cairo;font-weight:300 900;src:url({FONT}/cairo-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+2000-206F,U+20AC}}
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0}}
body{{font-family:Cairo,sans-serif;color:#303032;font-size:11.5px;line-height:1.6;width:210mm}}
.pg{{padding:10mm 15mm 0;height:296.5mm;overflow:hidden;position:relative}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px solid #008F82;padding-bottom:10px}}
.top img{{width:190px}}.meta{{text-align:left;font-size:11px;direction:rtl}}
.meta h1{{font-size:24px;font-weight:900;color:#008F82;line-height:1.2;margin-bottom:4px}}.meta b{{font-weight:800}}
.lat{{font-family:Cairo;direction:ltr;unicode-bidi:isolate}}
.parties{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:9px 0}}
.box{{border:1px solid #D8E4E1;border-radius:12px;padding:9px 13px;background:#FAFAFA}}
.box h4{{font-size:11px;color:#008F82;font-weight:800;margin-bottom:3px}}.box p{{font-size:12px}}.box small{{display:block;color:#5A5A5E;font-size:10.5px}}
.title{{background:#303032;color:#fff;border-radius:12px;padding:10px 14px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}}
.title h2{{font-size:15px;font-weight:800}}.title span{{color:#B8E5DF;font-size:11px}}
.svc{{border:1px solid #D8E4E1;border-radius:12px;padding:9px 13px;margin-bottom:8px}}
.sh{{display:flex;align-items:center;gap:9px;margin-bottom:4px}}.n{{width:24px;height:24px;border-radius:8px;background:#008F82;color:#fff;font-weight:800;display:grid;place-items:center;font-size:12px}}
.svc h3{{font-size:13.5px;font-weight:800}}.svc ul{{padding-inline-start:18px;columns:2;column-gap:20px}}.svc li{{margin-bottom:1px;break-inside:avoid}}
h3.sec{{font-size:13px;font-weight:800;margin:9px 0 5px;color:#008F82}}
table{{width:100%;border-collapse:collapse;border-radius:12px;overflow:hidden;border:1px solid #D8E4E1}}
th{{background:#E6F5F2;font-weight:800;text-align:start;padding:7px 12px;font-size:11.5px}}td{{padding:7px 12px;border-top:1px solid #E3EBE9}}
td.a,th.a{{text-align:left;direction:ltr;font-weight:700;white-space:nowrap}}
tr.t td{{background:#008F82;color:#fff;font-weight:900;font-size:13.5px;border:0}}
.notes{{padding-inline-start:18px;font-size:11px}}.notes li{{margin-bottom:2px}}
.bank{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.bank .box{{background:#fff}}.bank b{{font-weight:800}}
.sign{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}}.sign div{{border:1px dashed #9DB7B2;border-radius:12px;height:58px;padding:6px 12px;font-size:11px;color:#5A5A5E}}
.foot{{position:absolute;inset-inline:15mm;bottom:9mm;display:flex;justify-content:space-between;font-size:10px;color:#5A5A5E;border-top:1px solid #E3EBE9;padding-top:6px}}
</style></head><body><div class="pg">
<div class="top"><img src="file://{ROOT}/site/assets/img/logo-ink.svg" alt="">
<div class="meta"><h1>عرض سعر</h1><div>المرجع: <b class="lat">{e(q["ref"])}</b></div><div>التاريخ: <b class="lat">{e(q["date"])}</b></div><div>صلاحية العرض: <b>{e(q["valid"])}</b></div></div></div>
<div class="parties"><div class="box"><h4>مقدَّم إلى</h4><p><b>{e(q["client"])}</b></p><small>السجل التجاري: {e(q.get("client_cr","................"))}</small><small>الرقم الضريبي: {e(q.get("client_vat","................"))}</small></div>
<div class="box"><h4>مقدِّم العرض</h4><p><b>يدير للتسويق الإلكتروني</b></p><small>السجل التجاري: <span class="lat">7028759400</span> · الرقم الضريبي: <span class="lat">311270053300003</span></small><small>جوال: <span class="lat">0534644498</span></small></div></div>
<div class="title"><h2>{e(q["subject"])}</h2><span>اشتراك شهري</span></div>
{svc}
<h3 class="sec">العرض المالي</h3>
<table><tr><th>البند</th><th class="a">المبلغ (ر.س)</th></tr>
<tr><td>{e(q["fee_label"])} (غير شاملة الضريبة)</td><td class="a">{f(price)}</td></tr>
<tr><td>ضريبة القيمة المضافة 15%</td><td class="a">{f(vat)}</td></tr>
<tr class="t"><td>الإجمالي الشهري شامل الضريبة</td><td class="a">{f(total)}</td></tr></table>
<h3 class="sec">الشروط والملاحظات</h3><ul class="notes">{notes}</ul>
<h3 class="sec">بيانات الحساب البنكي</h3><div class="bank">
<div class="box"><b>مصرف الراجحي</b><small>رقم الحساب: <span class="lat">29600-001-0006080824624</span></small><small>الآيبان: <span class="lat">SA9080000296608010824624</span></small></div>
<div class="box"><b>مصرف الإنماء</b><small>رقم الحساب: <span class="lat">68203897761000</span></small><small>الآيبان: <span class="lat">SA5405000068203897761000</span></small></div></div>
<div class="sign"><div>اعتماد يدير: الاسم / التوقيع / الختم</div><div>اعتماد العميل: الاسم / التوقيع / الختم</div></div>
<div class="foot"><span>عرض سعر — يدير للتسويق الإلكتروني</span><span class="lat">YADEER · Grow further.</span></div>
</div></body></html>'''
tmp = out + ".html"; open(tmp, "w", encoding="utf-8").write(page)
js = f"""const {{chromium}}=require('/opt/node22/lib/node_modules/playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{tmp}');await p.evaluate(()=>document.fonts.ready);await p.pdf({{path:'{out}',format:'A4',printBackground:True,preferCSSPageSize:true}});await b.close()}})()""".replace("True","true")
open("/tmp/q/pdf.js", "w").write(js); subprocess.run(["node", "/tmp/q/pdf.js"], check=True); os.remove(tmp); print("ok", out)
