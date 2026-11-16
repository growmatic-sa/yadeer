# -*- coding: utf-8 -*-
"""يولّد اتفاقية سرية معلومات (متبادلة، مختصرة) PDF بهوية يدير. الاستخدام: python3 tools/nda.py <ملف_json> <خرج.pdf>"""
import json, os, subprocess, sys, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
e = html.escape
q = json.load(open(sys.argv[1], encoding="utf-8")); out = os.path.abspath(sys.argv[2])
cl = "".join(f'<div class="cl"><span class="n">{i+1}</span><div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>' for i, (t, b) in enumerate(q["clauses"]))
FONT = f"file://{ROOT}/site/assets/fonts"
page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:Cairo;font-weight:300 900;src:url({FONT}/cairo-arabic.woff2) format('woff2');unicode-range:U+0600-06FF,U+200C-200E,U+2010-2011,U+FB50-FDFF,U+FE70-FEFC}}
@font-face{{font-family:Cairo;font-weight:300 900;src:url({FONT}/cairo-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+2000-206F,U+20AC}}
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0}}
body{{font-family:Cairo,sans-serif;color:#303032;font-size:11.5px;line-height:1.75;width:210mm}}
.pg{{padding:11mm 15mm 12mm;height:296.5mm;overflow:hidden;position:relative}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px solid #008F82;padding-bottom:10px}}
.top img{{width:180px}}.meta{{font-size:11px}}.meta h1{{font-size:22px;font-weight:900;color:#008F82;line-height:1.25;margin-bottom:3px}}.meta b{{font-weight:800}}
.lat{{direction:ltr;unicode-bidi:isolate}}
.parties{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}}
.box{{border:1px solid #D8E4E1;border-radius:12px;padding:8px 13px;background:#FAFAFA}}
.box h4{{font-size:11px;color:#008F82;font-weight:800;margin-bottom:2px}}.box p{{font-size:12px}}.box small{{display:block;color:#5A5A5E;font-size:10.5px;line-height:1.55}}
.intro{{margin-bottom:8px}}
.cl{{display:flex;gap:9px;margin-bottom:6px;break-inside:avoid}}
.n{{flex:none;width:22px;height:22px;border-radius:7px;background:#008F82;color:#fff;font-weight:800;display:grid;place-items:center;font-size:11.5px;margin-top:2px}}
.cl h3{{font-size:12.5px;font-weight:800;line-height:1.5}}.cl p{{font-size:11.2px;line-height:1.65}}
.sign{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}}.sign div{{border:1px dashed #9DB7B2;border-radius:12px;height:92px;padding:7px 12px;font-size:11px;color:#5A5A5E;line-height:1.9}}.sign b{{color:#303032}}
.foot{{position:absolute;inset-inline:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:10px;color:#5A5A5E;border-top:1px solid #E3EBE9;padding-top:5px}}
</style></head><body><div class="pg">
<div class="top"><img src="file://{ROOT}/site/assets/img/logo-ink.svg" alt=""><div class="meta"><h1>اتفاقية سرية معلومات</h1><div>رقم الاتفاقية: <b class="lat">{e(q["ref"])}</b></div><div>التاريخ: <b class="lat">{e(q["date"])}</b></div></div></div>
<div class="parties"><div class="box"><h4>الطرف الأول</h4><p><b>يدير للتسويق الإلكتروني</b></p><small>السجل التجاري: <span class="lat">7028759400</span> · الرقم الضريبي: <span class="lat">311270053300003</span></small><small>جوال: <span class="lat">0534644498</span></small><small>يمثلها: ..........................</small></div>
<div class="box"><h4>الطرف الثاني</h4><p><b>{e(q["client"])}</b></p><small>السجل التجاري: ..........................</small><small>العنوان: ..........................</small><small>يمثلها: ..........................</small></div></div>
<p class="intro">{e(q["intro"])}</p>
{cl}
<div class="sign"><div><b>الطرف الأول: يدير للتسويق الإلكتروني</b><br>الاسم: ......................<br>الصفة: ......................<br>التوقيع والختم:</div><div><b>الطرف الثاني: {e(q["client"])}</b><br>الاسم: ......................<br>الصفة: ......................<br>التوقيع والختم:</div></div>
<div class="foot"><span>اتفاقية سرية معلومات — يدير للتسويق الإلكتروني</span><span class="lat">YADEER · Grow further.</span></div>
</div></body></html>'''
tmp = out + ".html"; open(tmp, "w", encoding="utf-8").write(page)
open("/tmp/q/pdf2.js", "w").write(f"""const {{chromium}}=require('/opt/node22/lib/node_modules/playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{tmp}');await p.evaluate(()=>document.fonts.ready);await p.pdf({{path:'{out}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close()}})()""")
subprocess.run(["node", "/tmp/q/pdf2.js"], check=True); os.remove(tmp); print("ok", out)
