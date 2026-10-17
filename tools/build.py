# -*- coding: utf-8 -*-
"""مولّد موقع يدير للتسويق الإلكتروني.

الاستخدام:
    SITE_URL=https://example.com python3 tools/build.py
ينتج مجلد site/ جاهزاً للنشر (ملفات ثابتة)، وصور OG من tools/og.mjs.
"""
import json, os, shutil, sys
from datetime import date
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from layout import Page, render
from content_misc import SITE, TOOLS, TOOL_BY_SLUG, POSTS, POST_BY_SLUG, GLOSSARY, HOME_FAQ, PRIVACY, TERMS
from content_services import SERVICES, BY_SLUG, GROUPS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "site")
OGTMP = os.path.join(ROOT, "tools", "_og")
PAGES = []
OG_JOBS = []   # (key, h1, eyebrow, svg)

fmt_legal = lambda t: t.format(cr=SITE["cr"], vat=SITE["vat"], phone=SITE["phone_local"])


def add(p):
    PAGES.append(p)
    return p


def sec(inner, cls="", id_="", pad=True, fl=None, word=None):
    extra = (floaters(fl, 7) if fl else "") + (f'<div class="bigword" aria-hidden="true"><span class="lat">{word}</span></div>' if word else "")
    return f'<section class="sec {cls}"{f" id={id_}" if id_ else ""}>{extra}<div class="wrap">{inner}</div></section>'


def head(eyebrow, title, lead="", extra=""):
    return (f'<div class="sec-head rv"><div><p class="eyebrow">{eyebrow}</p><h2 class="h2">{title}</h2></div>'
            f'{f"<div class=side><p class=lead>{lead}</p></div>" if lead else ""}{extra}</div>')


def og_job(key, h1, eyebrow, icon, chips, scheme):
    OG_JOBS.append(dict(key=key, h1=h1, eyebrow=eyebrow, svg=art_svg(key, icon, chips, scheme, "og" + key)))


def service_card(pg, s, delay=0):
    tags = "".join(f'<span class="tag{" lat" if s_.isascii() else ""}">{esc(s_)}</span>' for s_ in s["tags"])
    return (f'<a class="card svc tilt rv" data-g="{s["group"]}" href="{pg.rel("/الخدمات/" + s["slug"] + "/")}" style="--d:{delay}s">'
            f'<div class="card-top"><span class="card-icon">{ico(s["icon"], 26)}</span><span class="go">{ico("arrow", 18)}</span></div>'
            f'<h3 class="h3">{esc(s["title"])}</h3><p>{esc(s["short"])}</p><div class="tags">{tags}</div></a>')


def tool_card(pg, t, delay=0):
    return (f'<a class="card tool-card tilt rv" href="{pg.rel("/مختبر-النمو/" + t["slug"] + "/")}" style="--d:{delay}s">'
            f'<div class="card-top"><span class="card-icon alt">{ico(t["icon"], 26)}</span><span class="go">{ico("arrow", 18)}</span></div>'
            f'<h3 class="h3">{esc(t["title"])}</h3><p>{esc(t["short"])}</p><span class="free">مجاني · بدون تسجيل</span></a>')


def cta_band(pg, title, text, wa_text):
    return (f'<section class="sec cta-sec"><div class="wrap"><div class="cta rv"><span class="rip r1"></span><span class="rip r2"></span><span class="rip r3"></span>'
            f'<svg class="cta-art" viewBox="0 0 200 200" aria-hidden="true"><path d="{SYMBOL_PATH}" fill="none" stroke="#B8E5DF" stroke-opacity=".4" stroke-width="1.5"/></svg>'
            f'<div><p class="eyebrow">الخطوة التالية <span class="lat">Next step</span></p><h2 class="h2">{title}</h2><p class="lead">{text}</p>'
            f'<div class="actions">{btn(wa_link(wa_text), "تحدّث معنا على واتساب", "mint", "arrow", "target=_blank rel=noopener")}'
            f'{btn(tel(), "اتصل " + SITE["phone_local"], "ghost-light", "call")}</div></div></div></div></section>')


# ───────────────────────── واجهات الأدوات ─────────────────────────
def fld(id_, label, val, unit="", mn=0, mx=100000, step=1, hint="", rng=True):
    r = (f'<input class="rng" type="range" tabindex="-1" aria-hidden="true" data-for="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}">' if rng else "")
    return (f'<div class="fld"><label for="{id_}">{label}</label><div class="inp"><input id="{id_}" type="number" inputmode="decimal" '
            f'value="{val}" min="{mn}" step="any"><span class="unit">{unit}</span></div>{r}{f"<small>{hint}</small>" if hint else ""}</div>')


def sld(id_, label, val, unit, mn, mx, step):
    return (f'<div class="sld"><div class="sld-h"><label for="{id_}">{label}</label><output class="lat" for="{id_}" data-o="{id_}" data-u="{unit}">{val}</output></div>'
            f'<input class="rng" id="{id_}" type="range" min="{mn}" max="{mx}" step="{step}" value="{val}"></div>')


def sel(id_, label, opts):
    o = "".join(f'<option value="{v}">{esc(t)}</option>' for v, t in opts)
    return f'<div class="fld"><label for="{id_}">{label}</label><div class="inp sel"><select id="{id_}">{o}</select></div></div>'


def metric(id_, label, sub="", cls=""):
    return f'<div class="metric {cls}"><span class="m-l">{label}</span><strong class="m-v lat" id="{id_}">—</strong>{f"<small>{sub}</small>" if sub else ""}</div>'


def tool_ui(kind):
    if kind == "roas":
        return f'''<div class="tool" data-tool="roas"><div class="tool-in card"><h2 class="h3">مدخلاتك</h2>
{fld("r-spend", "الإنفاق الإعلاني", 5000, "ر.س", 0, 200000, 100)}
{fld("r-rev", "المبيعات الناتجة عن الحملة", 18000, "ر.س", 0, 600000, 500)}
{fld("r-margin", "هامش الربح على المبيعات (قبل الإعلان)", 30, "%", 1, 95, 1, "ما يتبقى من كل 100 ريال بعد تكلفة المنتج والشحن والدفع.")}
<hr><div class="fld"><label for="r-lift">ماذا لو رفعنا نسبة التحويل؟</label><div class="inp"><input id="r-lift" type="number" value="20" min="0" step="any"><span class="unit">%</span></div>
<input class="rng" type="range" tabindex="-1" aria-hidden="true" data-for="r-lift" min="0" max="100" step="5" value="20"><small>بنفس الإنفاق، يزيد عدد الطلبات بهذه النسبة (تبسيط مفيد للتقدير).</small></div></div>
<div class="tool-out card" aria-live="polite"><div class="verdict" id="r-verdict" role="status">—</div>
<div class="metrics">{metric("r-roas", "العائد على الإنفاق (ROAS)", "ضعف", "")}{metric("r-be", "عائد التعادل", "الحد الأدنى لعدم الخسارة")}{metric("r-profit", "صافي الربح بعد الإعلان", "ر.س")}{metric("r-roi", "العائد على الاستثمار", "")}</div>
<div class="bars" aria-hidden="true"><div class="bar-row"><span>عائدك</span><div class="bar"><i id="r-b1"></i></div></div><div class="bar-row"><span>التعادل</span><div class="bar be"><i id="r-b2"></i></div></div></div>
<div class="whatif" id="r-what"></div>
<div class="out-actions"><button class="btn btn-ghost btn-sm" type="button" data-copy="roas">{ico("copy", 16)} نسخ الملخص</button><a class="btn btn-ghost btn-sm" data-wa-share="roas" href="#" target="_blank" rel="noopener">{ico("whatsapp", 16)} أرسل النتيجة لفريقنا</a></div></div></div>'''
    if kind == "cpa":
        return f'''<div class="tool" data-tool="cpa"><div class="tool-in card"><h2 class="h3">مدخلاتك</h2>
{fld("c-price", "متوسط سعر البيع للطلب", 250, "ر.س", 1, 5000, 5)}
{fld("c-cost", "تكلفة المنتج والتشغيل لكل طلب", 120, "ر.س", 0, 5000, 5, "تكلفة المنتج + الشحن + رسوم الدفع + التغليف.")}
{fld("c-cpc", "تكلفة النقرة (CPC)", 1.2, "ر.س", 0.1, 20, 0.1)}
{fld("c-cvr", "نسبة التحويل", 2, "%", 0.1, 20, 0.1, "من كل 100 زائر كم اشتروا؟")}
{fld("c-target", "ربح شهري مستهدف", 10000, "ر.س", 0, 500000, 500)}</div>
<div class="tool-out card" aria-live="polite"><div class="verdict" id="c-verdict" role="status">—</div>
<div class="metrics">{metric("c-unit", "ربح الطلب قبل الإعلان", "ر.س")}{metric("c-cpa", "تكلفة الطلب الحالية", "ر.س")}{metric("c-max", "أقصى تكلفة مسموحة", "ر.س")}{metric("c-after", "ربح الطلب بعد الإعلان", "ر.س")}{metric("c-becvr", "نسبة التحويل للتعادل", "")}{metric("c-becpc", "تكلفة النقرة للتعادل", "ر.س")}</div>
<div class="plan-box"><h3 class="h4">للوصول إلى ربحك المستهدف</h3><p id="c-need">—</p></div>
<div class="out-actions"><button class="btn btn-ghost btn-sm" type="button" data-copy="cpa">{ico("copy", 16)} نسخ الملخص</button><a class="btn btn-ghost btn-sm" data-wa-share="cpa" href="#" target="_blank" rel="noopener">{ico("whatsapp", 16)} أرسل النتيجة لفريقنا</a></div></div></div>'''
    if kind == "ltv":
        return f'''<div class="tool" data-tool="ltv"><div class="tool-in card"><h2 class="h3">مدخلاتك</h2>
{fld("l-aov", "متوسط قيمة الطلب", 400, "ر.س", 1, 10000, 10)}
{fld("l-freq", "عدد الطلبات للعميل في السنة", 2.5, "طلب", 0.5, 24, 0.5)}
{fld("l-margin", "هامش الربح", 35, "%", 1, 95, 1)}
{fld("l-years", "سنوات بقاء العميل معك", 2, "سنة", 0.5, 10, 0.5, "قدّرها من بيانات عملائك السابقين.")}
{fld("l-cac", "تكلفة اكتساب العميل (CAC)", 90, "ر.س", 1, 5000, 5)}</div>
<div class="tool-out card" aria-live="polite"><div class="verdict" id="l-verdict" role="status">—</div>
<div class="metrics">{metric("l-ltv", "القيمة الدائمة (ربحاً)", "ر.س")}{metric("l-ratio", "نسبة LTV إلى CAC", "الشائع ≥ 3")}{metric("l-pay", "طلبات استرداد التكلفة", "طلب")}{metric("l-max", "أقصى CAC آمن", "عند نسبة 3 إلى 1")}</div>
<div class="out-actions"><button class="btn btn-ghost btn-sm" type="button" data-copy="ltv">{ico("copy", 16)} نسخ الملخص</button><a class="btn btn-ghost btn-sm" data-wa-share="ltv" href="#" target="_blank" rel="noopener">{ico("whatsapp", 16)} أرسل النتيجة لفريقنا</a></div></div></div>'''
    if kind == "budget":
        return f'''<div class="tool" data-tool="budget"><div class="tool-in card"><h2 class="h3">مدخلاتك</h2>
{fld("b-total", "الميزانية الشهرية", 10000, "ر.س", 500, 300000, 500)}
{sel("b-goal", "هدفك الرئيسي", [("sales", "مبيعات مباشرة"), ("leads", "عملاء محتملون / استفسارات"), ("aware", "وعي بالعلامة")])}
{sel("b-stage", "مرحلة نشاطك", [("new", "نشاط جديد"), ("run", "قائم ويحتاج نمواً")])}
<hr><p class="note">افتراضات التقدير (عدّلها من بيانات حسابك):</p>
{fld("b-cpc", "متوسط تكلفة النقرة", 1.3, "ر.س", 0.1, 20, 0.1, rng=False)}
{fld("b-cvr", "نسبة التحويل", 2, "%", 0.1, 20, 0.1, rng=False)}</div>
<div class="tool-out card" aria-live="polite"><h2 class="h3">التوزيع المقترح <small class="muted">(اسحب لتعديله)</small></h2>
<div class="stack" id="b-stack" aria-hidden="true"></div><div id="b-rows" class="b-rows"></div>
<div class="b-sum" id="b-sum" role="status"></div>
<div class="metrics">{metric("b-clicks", "نقرات متوقعة (إعلانات مدفوعة)", "تقدير")}{metric("b-orders", "نتائج متوقعة", "تقدير")}{metric("b-cpa", "تكلفة النتيجة التقريبية", "ر.س")}</div>
<div class="out-actions"><button class="btn btn-ghost btn-sm" type="button" data-b-reset>{ico("refresh", 16)} العودة للمقترح</button><button class="btn btn-ghost btn-sm" type="button" data-b-norm>تطبيع المجموع إلى 100%</button>
<a class="btn btn-ghost btn-sm" data-wa-share="budget" href="#" target="_blank" rel="noopener">{ico("whatsapp", 16)} أرسل التوزيع لفريقنا</a></div></div></div>'''
    if kind == "plan":
        return '<div class="tool wizard" data-tool="plan"><noscript><p class="card pad">تحتاج هذه الأداة إلى تفعيل جافاسكربت في المتصفح.</p></noscript></div>'
    if kind == "audit":
        return '<div class="tool wizard" data-tool="audit"><noscript><p class="card pad">تحتاج هذه الأداة إلى تفعيل جافاسكربت في المتصفح.</p></noscript></div>'
    return ""


# ───────────────────────── الصفحة الرئيسية ─────────────────────────
def orbit_diagram(pg):
    import math
    nodes = [
        ("compass", "خطة واستشارة", "نبدأ من الهدف", "الاستشارات-وخطط-التسويق"),
        ("shapes", "هوية ومحتوى", "علامة تُعرف", "الهوية-البصرية-والتصميم"),
        ("target", "إعلان وتأثير", "وصول يُقاس", "ادارة-الحملات-الاعلانية"),
        ("browser", "موقع ومتجر", "وجهة تحوّل الزائر", "تصميم-وبرمجة-المواقع-الالكترونية"),
        ("mail", "عميل يعود", "واتساب وبريد", "التسويق-بالبريد-والواتساب"),
        ("chart", "قياس وقرار", "أرقام تُقرأ", "تحليل-البيانات-والتتبع"),
    ]
    lines, items = [], []
    for i, (ic, t, sub, slug) in enumerate(nodes):
        a = math.radians(-90 + i * 60)
        x, y = 50 + 37 * math.cos(a), 50 + 37 * math.sin(a)
        lines.append(f'<line x1="50" y1="50" x2="{x:.1f}" y2="{y:.1f}" style="--i:{i}"/>')
        items.append(f'<a class="onode" style="left:{x:.1f}%;top:{y:.1f}%;--i:{i}" href="{pg.rel("/الخدمات/" + slug + "/")}"><span class="oi">{ico(ic, 24)}</span><b>{t}</b><small>{sub}</small></a>')
    return (f'<div class="orbit-wrap rv"><svg class="orbit-svg" viewBox="0 0 100 100" aria-hidden="true"><circle class="r1" cx="50" cy="50" r="37"/><circle class="r2" cx="50" cy="50" r="47"/>'
            f'<g class="olines">{"".join(lines)}</g></svg><div class="ocore" aria-hidden="true"><span class="pulse p1"></span><span class="pulse p2"></span>'
            f'<img src="{pg.asset("img/symbol.svg")}" alt="" width="88" height="84"></div>{"".join(items)}</div>')


MARQUEE = ["إدارة الحملات", "سيو", "محتوى عربي", "هوية بصرية", "فيديو وموشن", "مؤثرون", "واتساب", "متاجر إلكترونية", "مواقع سريعة", "تطبيقات جوال", "أنظمة", "أتمتة", "تتبّع وقياس"]


def build_home():
    pg = Page("/", f"{SITE['name']} | وكالة تسويق إلكتروني وحلول تقنية في السعودية",
              "وكالة تسويق إلكتروني وحلول تقنية في السعودية: حملات إعلانية، سيو، محتوى، مواقع، متاجر، تطبيقات وأنظمة، مع أدوات تفاعلية مجانية لحساب العائد قبل أن تصرف.",
              "", og="home", priority="1.0")
    rel = pg.rel
    paths = [
        ("لدي متجر ولا أعرف هل إعلاناتي رابحة", "حاسبة-العائد-على-الانفاق-الاعلاني", "ادارة-الحملات-الاعلانية", "target"),
        ("أريد أن يظهر موقعي في جوجل", "تشخيص-الحضور-الرقمي", "تحسين-محركات-البحث", "search"),
        ("أصرف على الإعلانات بلا نتائج واضحة", "حاسبة-تكلفة-اكتساب-العميل", "تحليل-البيانات-والتتبع", "chart"),
        ("أبدأ مشروعاً ولا أعرف من أين أبدأ", "مصمم-خطة-النمو", "الاستشارات-وخطط-التسويق", "route"),
        ("عملائي لا يعودون للشراء", "حاسبة-القيمة-الدائمة-للعميل", "التسويق-بالبريد-والواتساب", "loop"),
        ("أحتاج نظاماً أو تطبيقاً لعملي", "مصمم-خطة-النمو", "الاستشارات-التقنية-والتحول-الرقمي", "chip"),
    ]
    path_cards = "".join(
        f'<div class="path rv" style="--d:{i * .06}s"><span class="path-n lat">0{i + 1}</span><span class="card-icon">{ico(ic, 24)}</span><h3 class="h4">{esc(t)}</h3>'
        f'<div class="path-links"><a href="{rel("/مختبر-النمو/" + tl + "/")}">{ico("pulse", 16)} جرّب: {esc(TOOL_BY_SLUG[tl]["title"].split(" (")[0])}</a>'
        f'<a href="{rel("/الخدمات/" + sv + "/")}">{ico("arrow", 16)} {esc(BY_SLUG[sv]["title"])}</a></div></div>'
        for i, (t, tl, sv, ic) in enumerate(paths))
    principles = [
        ("target", "مؤشر نجاح قبل التنفيذ", "نكتب لكل خدمة المؤشر الذي سنحكم به عليها قبل أن نبدأ، فلا نختلف بعد ذلك على معنى «نجح»."),
        ("calc", "أدوات تحسب بها بنفسك", "حاسبات ومخططات مفتوحة في مختبر النمو. تعرف رقمك التقريبي قبل أي عرض سعر."),
        ("pulse", "شفافية في الأرقام", "تقارير تربط الإنفاق بالنتائج، وتتبّع يُركَّب أولاً، وحسابات إعلانية باسمك."),
        ("browser", "تسويق وتقنية تحت سقف واحد", "الحملة تحتاج موقعاً سريعاً وتتبّعاً سليماً. نبنيهما معاً فلا تضيع المسؤولية بين مورّدين."),
    ]
    pr = "".join(f'<div class="princ rv" style="--d:{i * .07}s"><span class="card-icon">{ico(ic, 24)}</span><h3 class="h4">{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(principles))
    svc_cards = "".join(service_card(pg, s, (i % 3) * .07).replace('class="card svc rv"', f'class="card svc tilt rv" data-g="{s["group"]}"') for i, s in enumerate(SERVICES))
    tools = "".join(tool_card(pg, t, (i % 3) * .07).replace('class="card tool-card rv"', 'class="card tool-card tilt rv"') for i, t in enumerate(TOOLS))
    steps = [("استشارة مجانية", "نسمع منك عن مشروعك وهدفك وما جرّبته من قبل."), ("خطة وعرض سعر", "نرسل خطة مختصرة وعرضاً مكتوباً بكل البنود."),
             ("تنفيذ وإطلاق", "ننفّذ ما اتفقنا عليه ونطلعك على كل مرحلة."), ("قياس وتحسين", "تقرير دوري بالأرقام، وقرار بما نغيّره بعده.")]
    st = "".join(f'<li class="step rv" style="--d:{i * .12}s"><span class="node">{i + 1}</span><h3 class="h4">{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps))
    posts = "".join(
        f'<a class="card post tilt rv" href="{rel("/المدونة/" + p["slug"] + "/")}" style="--d:{i * .07}s"><span class="pill">{esc(p["cat"])}</span><h3 class="h3">{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><span class="meta">{p["read"]} دقائق قراءة</span></a>'
        for i, p in enumerate(POSTS[:3]))
    mq = "".join(f'<span>{t}</span><i aria-hidden="true"></i>' for t in MARQUEE)
    chips = "".join(f'<li>{ico("check", 16)} {t}</li>' for t in ("تسويق وتقنية تحت سقف واحد", "خطة مكتوبة قبل التنفيذ", "نتائج تُقاس بالأرقام"))
    hero = f'''<section class="hero" id="top">{network_bg("yadeer-hero")}{floaters("hero", 8)}<div class="bigword hero-word" aria-hidden="true"><span class="lat">GROW FURTHER.</span></div><div class="wrap hero-in">
<div class="hero-copy"><p class="eyebrow">وكالة تسويق إلكتروني وحلول تقنية <span class="lat">Grow further.</span></p>
<h1><span class="h1-l">نُدير <span class="rot" data-words="حضورك الرقمي|تسويقك|متجرك|إعلانك|مشروعك"><span class="rot-w">حضورك الرقمي</span></span></span><span class="h1-l hl">ليصل أبعد</span></h1>
<p class="lead">نبدأ من رقم هدفك لا من قالب جاهز: خطة مكتوبة، تتبّع يُركَّب أولاً، وأدوات حساب مفتوحة تجرّبها بنفسك قبل أن تلتزم بأي شيء.</p>
<div class="actions">{btn(rel("/مختبر-النمو/مصمم-خطة-النمو/"), "ابنِ خطة نموّك في دقيقة", "mint magnetic", "arrow")}{btn(wa_link("مرحباً يدير، أرغب في الاستفسار عن خدماتكم."), "تحدّث معنا على واتساب", "ghost-light", "whatsapp", "target=_blank rel=noopener")}</div>
<ul class="vchips">{chips}</ul></div>
<div class="hero-side"><div class="float-badge" aria-hidden="true"><span class="lat" id="m-roas-badge">4.0×</span><small>العائد</small></div>
<div class="mini card" data-tool="mini"><div class="mini-h"><span class="dot"></span><strong>جرّبها الآن</strong><small>كم يعود عليك إعلانك؟</small></div>
{sld("m-spend", "ميزانية الإعلان الشهرية", 8000, "ر.س", 500, 100000, 500)}
{sld("m-roas", "العائد المتوقع (ROAS)", 4, "ضعف", 1, 10, 0.5)}
{sld("m-margin", "هامش ربحك", 30, "%", 5, 90, 1)}
<div class="mini-out"><div><span>المبيعات المتوقعة</span><strong class="lat" id="m-rev">—</strong></div><div><span>صافي الربح</span><strong class="lat" id="m-profit">—</strong></div></div>
<p class="mini-note" id="m-note" role="status"></p>
<a class="mini-link" href="{rel("/مختبر-النمو/حاسبة-العائد-على-الانفاق-الاعلاني/")}">الحاسبة الكاملة {ico("arrow", 16)}</a></div>
<div class="float-chart" aria-hidden="true"><div class="bars3"><div><i id="mb-spend"></i><span>الإنفاق</span></div><div><i id="mb-rev"></i><span>المبيعات</span></div><div><i id="mb-profit"></i><span>الربح</span></div></div></div></div></div></section>'''
    body = hero
    body += sec(head("لمن يبدأ من مشكلته <span class=lat>Start here</span>", "ابدأ من مشكلتك، لا من قائمة الخدمات", "اختر ما يشبه وضعك، وسنأخذك إلى الأداة والخدمة المناسبتين.") + f'<div class="paths">{path_cards}</div>', "soft deco-y sheet", "start", fl="paths")
    body += sec(f'<div class="orbit-sec"><div class="orbit-copy">{head("لماذا يدير <span class=lat>Approach</span>", "حلقات تغذّي بعضها حول رقم واحد", "")}'
                '<p class="lead">الحملة بلا موقع سريع تُهدر، والموقع بلا تتبّع يُخمَّن، والمحتوى بلا خطة يضيع. نبني الحلقات معاً حتى تعمل كشبكة واحدة، كما يعمل رمز يدير: إطار منظّم، شبكة اتصال، ووصول أبعد.</p>'
                f'<div class="actions">{btn(rel("/من-نحن/"), "اعرف فكرة العلامة", "secondary", "arrow")}</div></div>{orbit_diagram(pg)}</div>', "sheet", "approach", fl="orbit")
    body += sec(f'<div class="princs">{pr}</div>', "alt sheet", fl="princ")
    body += sec(head("خدماتنا <span class=lat>Services</span>", "كل ما يحتاجه حضورك الرقمي", "تسويق يوصلك إلى عميلك، وتقنية تبني ما يصل إليه.")
                + f'<div class="tabs" role="tablist" aria-label="تصفية الخدمات"><button type="button" class="tab on" data-f="all" role="tab" aria-selected="true">الكل</button><button type="button" class="tab" data-f="marketing" role="tab" aria-selected="false">خدمات تسويقية</button><button type="button" class="tab" data-f="tech" role="tab" aria-selected="false">خدمات تقنية</button></div>'
                + f'<div class="cards svc-grid" data-tabs>{svc_cards}</div>', "sheet", "services", fl="svc")
    body += sec(head("مختبر النمو <span class=lat>Growth Lab</span>", "جرّب قبل أن تتواصل", "أدوات تفاعلية مجانية تحسب لك العائد والتكلفة والقيمة وتبني لك خطة مبدئية.") + f'<div class="cards">{tools}</div>'
                + f'<p class="center"><a class="btn btn-mint" href="{rel("/مختبر-النمو/")}"><span>كل أدوات المختبر</span>{ico("arrow", 18, "arw")}</a></p>', "dark lab-sec", "lab", fl="lab", word="LAB")
    body += sec(head("طريقة العمل <span class=lat>Process</span>", "الطريقة نفسها في كل خدمة", "مهما كانت الخدمة، نمرّ بالخطوات الأربع نفسها.") + f'<ol class="steps" data-draw>{st}</ol>', "soft sheet", "process", fl="proc")
    body += sec(head("المدونة <span class=lat>Insights</span>", "محتوى يساعدك على القرار", "مقالات عملية تجيب عن أسئلة الميزانية والقياس والسيو.") + f'<div class="cards">{posts}</div>', "sheet", "blog")
    body += sec(head("أسئلة شائعة <span class=lat>FAQ</span>", "قبل أن تسأل") + faq_html(HOME_FAQ), "alt sheet", "faq")
    body += cta_band(pg, "لنُدِر مشروعك نحو الأعلى.", "راسلنا على واتساب أو اتصل بنا، ونرسل لك خطة مختصرة وعرض سعر واضحاً.", "مرحباً يدير، أرغب في خطة وعرض سعر.")
    pg.body = body
    pg.bodycls = "home"
    pg.scripts = ("tools.js",)
    pg.schema = [{"@type": "WebPage", "@id": SITE_URL + "/#webpage", "url": SITE_URL + "/", "name": pg.title, "inLanguage": "ar", "isPartOf": {"@id": SITE_URL + "/#website"}, "about": {"@id": ORG_ID}},
                 faq_schema(HOME_FAQ)]
    og_job("home", "نُدير حضورك الرقمي ليصل أبعد", "وكالة تسويق إلكتروني وحلول تقنية", "target", ["Meta", "Google", "TikTok"], "teal")
    add(pg)


# ───────────────────────── الخدمات ─────────────────────────
def build_services_hub():
    pg = Page("/الخدمات/", f"خدمات التسويق الإلكتروني والحلول التقنية | يدير",
              "خدمات تسويقية وتقنية من يدير: إدارة حملات، سيو، محتوى، هوية، فيديو، مؤثرون، مواقع، متاجر، تطبيقات، أنظمة وأتمتة، ولكل خدمة صفحة مفصّلة.",
              "", og="services", priority="0.9")
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("الخدمات", None)]
    b = banner(rel, trail, 'خدماتنا <span class="lat">Services</span>', "تسويق وتقنية، وإدارة واحدة", "خدمات تسويقية وتقنية متكاملة. اختر واحدة أو اجمع بينها، ونبدأ دائماً من هدفك.",
               "dashboard", ["تسويق", "تقنية", "قياس"], "teal", seed="services", uid="sv",
               actions=btn(wa_link("مرحباً يدير، أرغب في معرفة الخدمة الأنسب لي."), "اسألنا عن الأنسب لك", "mint", "arrow", "target=_blank rel=noopener"))
    body = b
    for g in ("marketing", "tech"):
        cards = "".join(service_card(pg, s, (i % 3) * .07) for i, s in enumerate([x for x in SERVICES if x["group"] == g]))
        body += sec(head(f'{GROUPS[g]["title"]} <span class=lat>{GROUPS[g]["en"]}</span>', GROUPS[g]["title"], GROUPS[g]["lead"]) + f'<div class="cards">{cards}</div>', "alt" if g == "marketing" else "", g)
    steps = [("استشارة مجانية", "نسمع منك عن مشروعك وهدفك."), ("خطة وعرض سعر", "خطة مختصرة وعرض مكتوب بكل البنود."), ("تنفيذ وإطلاق", "ننفّذ ونطلعك على كل مرحلة."), ("قياس وتحسين", "تقرير بالأرقام وقرار بما نغيّره.")]
    st = "".join(f'<li class="step rv"><span class="node">{i + 1}</span><h3 class="h4">{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps))
    body += sec(head("طريقة العمل <span class=lat>Process</span>", "الطريقة نفسها في كل خدمة") + f'<ol class="steps">{st}</ol>', "soft")
    body += cta_band(pg, "لا تعرف الخدمة المناسبة؟", "ابدأ بمصمم خطة النمو، أو اكتب لنا ونرشّح لك الأنسب.", "مرحباً يدير، أريد ترشيح الخدمة الأنسب لمشروعي.")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "CollectionPage", "name": "خدمات يدير", "url": abs_url(pg.path), "inLanguage": "ar"},
                 {"@type": "ItemList", "name": "خدمات يدير", "itemListElement": [
                     {"@type": "ListItem", "position": i + 1, "name": s["title"], "url": abs_url("/الخدمات/" + s["slug"] + "/")} for i, s in enumerate(SERVICES)]}]
    og_job("services", "تسويق وتقنية، وإدارة واحدة", "خدماتنا · Services", "dashboard", ["تسويق", "تقنية", "قياس"], "teal")
    add(pg)


def build_service(s, idx):
    path = f"/الخدمات/{s['slug']}/"
    pg = Page(path, f"{s['title']} | يدير", s["meta"], "", og="svc-" + str(idx + 1), priority="0.8")
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("الخدمات", "/الخدمات/"), (s["title"], None)]
    scheme = "teal" if s["group"] == "marketing" else "mint"
    wa_txt = f"مرحباً يدير، أرغب في الاستفسار عن خدمة: {s['title']}."
    b = banner(rel, trail, f'{GROUPS[s["group"]]["title"]} <span class="lat">{GROUPS[s["group"]]["en"]}</span>', esc(s["h1"]), esc(s["lead"]),
               s["icon"], s["tags"], scheme, seed=s["slug"], uid="s" + str(idx),
               actions=btn(wa_link(wa_txt), "اطلب عرض سعر", "mint", "arrow", "target=_blank rel=noopener") + btn(tel(), SITE["phone_local"], "ghost-light", "call"))
    body = b
    incl = "".join(f'<li class="inc rv" style="--d:{(i % 3) * .06}s"><span class="num lat">{i + 1:02d}</span><p>{esc(t)}</p></li>' for i, t in enumerate(s["includes"]))
    who = "".join(f'<li>{ico("check", 18)}<span>{esc(t)}</span></li>' for t in s["for"])
    body += sec(f'<div class="two"><div>{head("ما الذي تشمله الخدمة", "ماذا تحصل عليه")}<ul class="incs">{incl}</ul></div>'
                f'<aside class="aside card"><h2 class="h4">لمن تناسب هذه الخدمة؟</h2><ul class="checks">{who}</ul>'
                f'<hr><p class="muted">لا تعرف إن كانت تناسبك؟ اكتب لنا ونجيبك بصراحة.</p>{btn(wa_link(wa_txt), "اسألنا الآن", "primary", "whatsapp", "target=_blank rel=noopener")}</aside></div>', "alt")
    st = "".join(f'<li class="step rv" style="--d:{i * .08}s"><span class="node">{i + 1}</span><h3 class="h4">{esc(t)}</h3><p>{esc(d)}</p></li>' for i, (t, d) in enumerate(s["steps"]))
    body += sec(head("طريقة العمل", "كيف ننفّذ هذه الخدمة", "") + f'<ol class="steps">{st}</ol>', "soft")
    kp = "".join(f'<div class="kpi rv" style="--d:{i * .06}s"><span class="kpi-i">{ico("pulse", 22)}</span><h3 class="h4">{esc(n)}</h3><p>{esc(d)}</p></div>' for i, (n, d) in enumerate(s["kpis"]))
    body += sec(head("مؤشرات النجاح <span class=lat>KPIs</span>", "كيف نحكم على النتيجة", "هذه المؤشرات نكتبها معك قبل البدء، فيكون الحكم على العمل بالأرقام لا بالانطباع.") + f'<div class="kpis">{kp}</div>')
    t = TOOL_BY_SLUG[s["tool"]]
    body += sec(f'<div class="try card rv"><span class="card-icon alt">{ico(t["icon"], 28)}</span><div><p class="eyebrow">جرّب قبل أن تتواصل <span class="lat">Try it</span></p>'
                f'<h2 class="h3">{esc(t["title"])}</h2><p>{esc(t["short"])}</p></div>{btn(rel("/مختبر-النمو/" + t["slug"] + "/"), "افتح الأداة", "secondary", "arrow")}</div>', "alt", pad=False)
    body += sec(head("أسئلة شائعة", f'أسئلة عن {esc(s["title"])}') + faq_html(s["faq"]))
    rel_cards = "".join(service_card(pg, BY_SLUG[r], i * .07) for i, r in enumerate(s["related"]))
    body += sec(head("خدمات مرتبطة", "قد تحتاج أيضاً") + f'<div class="cards two-c">{rel_cards}</div>', "soft")
    body += cta_band(pg, f"جاهز لبدء {esc(s['title'])}؟", "راسلنا ونرسل لك خطة مختصرة وعرض سعر مكتوباً بكل البنود.", wa_txt)
    pg.body = body
    pg.schema = [breadcrumb_schema(trail),
                 {"@type": "Service", "name": s["title"], "serviceType": s["title"], "description": s["meta"], "url": abs_url(path),
                  "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "المملكة العربية السعودية"}, "inLanguage": "ar"},
                 faq_schema(s["faq"])]
    og_job("svc-" + str(idx + 1), s["h1"], f'{GROUPS[s["group"]]["title"]} · {GROUPS[s["group"]]["en"]}', s["icon"], s["tags"], scheme)
    add(pg)


# ───────────────────────── مختبر النمو ─────────────────────────
def build_lab_hub():
    pg = Page("/مختبر-النمو/", f"مختبر النمو: أدوات تسويقية تفاعلية مجانية | يدير",
              "مختبر النمو من يدير: حاسبة ROAS، تكلفة اكتساب العميل، القيمة الدائمة، موزّع الميزانية، تشخيص الحضور الرقمي ومصمم خطة النمو. مجانية بلا تسجيل.",
              "", og="lab", priority="0.9")
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("مختبر النمو", None)]
    b = banner(rel, trail, 'مختبر النمو <span class="lat">Growth Lab</span>', "جرّب أرقامك قبل أن تصرف", "أدوات تفاعلية مجانية تحسب لك العائد والتكلفة والقيمة، وتبني خطة مبدئية، وتشخّص حضورك الرقمي.",
               "calc", ["ROAS", "CPA", "LTV"], "mint", seed="lab", uid="lb",
               actions=btn(rel("/مختبر-النمو/مصمم-خطة-النمو/"), "ابدأ بمصمم الخطة", "mint", "arrow"))
    tools = "".join(tool_card(pg, t, (i % 3) * .07) for i, t in enumerate(TOOLS))
    why = [("ما لا يُحسب لا يُحسَّن", "كل أداة تجيب عن سؤال تسويقي حقيقي بصيغة رياضية بسيطة."),
           ("بلا تسجيل ولا بيانات", "الحسابات تجري داخل متصفحك، ولا ترسل لنا شيئاً إلا إذا اخترت ذلك."),
           ("تقدير لا وعد", "النتائج استرشادية مبنية على مدخلاتك، ونوضّح ذلك في كل أداة.")]
    w = "".join(f'<div class="princ rv"><h3 class="h4">{t}</h3><p>{d}</p></div>' for t, d in why)
    body = b + sec(f'<div class="cards">{tools}</div>', "alt")
    body += sec(head("لماذا مختبر النمو", "أدوات تقرأ معك لا عنك") + f'<div class="princs three">{w}</div>', "soft")
    body += sec(f'<div class="try card rv"><span class="card-icon alt">{ico("book", 28)}</span><div><p class="eyebrow">تعلّم المصطلح <span class="lat">Glossary</span></p><h2 class="h3">قاموس التسويق الإلكتروني</h2>'
                f'<p>تعريفات مختصرة بصيغها الحسابية لأشهر المصطلحات: CPM وCPC وROAS وLTV وغيرها.</p></div>{btn(rel("/قاموس-التسويق/"), "افتح القاموس", "secondary", "arrow")}</div>', "", pad=False)
    body += cta_band(pg, "النتيجة تحتاج قراءة؟", "أرسل لنا ما حسبته ونقرأه معك ونحوّله إلى خطة.", "مرحباً يدير، جرّبت أدوات مختبر النمو وأريد قراءة النتيجة معكم.")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "CollectionPage", "name": "مختبر النمو", "url": abs_url(pg.path), "inLanguage": "ar"},
                 {"@type": "ItemList", "name": "أدوات مختبر النمو", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["title"], "url": abs_url("/مختبر-النمو/" + t["slug"] + "/")} for i, t in enumerate(TOOLS)]}]
    og_job("lab", "جرّب أرقامك قبل أن تصرف", "مختبر النمو · Growth Lab", "calc", ["ROAS", "CPA", "LTV"], "mint")
    add(pg)


def build_tool(t, idx):
    path = f"/مختبر-النمو/{t['slug']}/"
    pg = Page(path, f"{t['title']} | يدير", t["meta"], "", og="tool-" + str(idx + 1), priority="0.8", scripts=("tools.js",))
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("مختبر النمو", "/مختبر-النمو/"), (t["title"].split(" (")[0], None)]
    b = banner(rel, trail, 'مختبر النمو <span class="lat">Growth Lab</span>', esc(t["h1"]), esc(t["lead"]), t["icon"], ["مجاني", "فوري", "بلا تسجيل"], "teal" if idx % 2 == 0 else "mint",
               seed=t["slug"], uid="t" + str(idx), kind="tool")
    body = b + sec(tool_ui(t["kind"]), "alt tool-sec")
    body += sec(f'<div class="two"><div>{head("كيف تقرأ النتائج", "فهم الأرقام")}<p class="prose">{esc(t["reads"])}</p></div>'
                f'<aside class="aside card"><h2 class="h4">اقرأ أيضاً</h2><ul class="links">'
                + "".join(f'<li><a href="{rel("/الخدمات/" + sv + "/")}">{ico("arrow", 16)} {esc(BY_SLUG[sv]["title"])}</a></li>' for sv in t["services"])
                + f'<li><a href="{rel("/قاموس-التسويق/")}">{ico("book", 16)} قاموس التسويق</a></li></ul></aside></div>')
    body += sec(head("أسئلة شائعة", "عن هذه الأداة") + faq_html(t["faq"]), "soft")
    others = "".join(tool_card(pg, o, i * .07) for i, o in enumerate([x for x in TOOLS if x is not t][:3]))
    body += sec(head("أدوات أخرى", "جرّب أيضاً") + f'<div class="cards">{others}</div>')
    body += cta_band(pg, "تحتاج قراءة النتيجة مع مختص؟", "أرسل لنا ما حسبته ونحوّله إلى خطة بخطوات وأرقام.", f"مرحباً يدير، جرّبت أداة «{t['title']}» وأريد قراءة النتيجة معكم.")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail),
                 {"@type": "WebApplication", "name": t["title"], "url": abs_url(path), "description": t["meta"], "applicationCategory": "BusinessApplication",
                  "operatingSystem": "Web", "inLanguage": "ar", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SAR"},
                  "provider": {"@id": ORG_ID}},
                 faq_schema(t["faq"])]
    og_job("tool-" + str(idx + 1), t["h1"], "مختبر النمو · Growth Lab", t["icon"], ["مجاني", "فوري", "بلا تسجيل"], "teal" if idx % 2 == 0 else "mint")
    add(pg)


def build_glossary():
    pg = Page("/قاموس-التسويق/", f"قاموس التسويق الإلكتروني: معاني CPM وCPC وROAS وLTV | يدير",
              "قاموس عربي لأشهر مصطلحات التسويق الإلكتروني مع الصيغ الحسابية: CPM وCPC وCTR وCPA وROAS وLTV والسيو والبكسل وغيرها.", "", og="glossary", priority="0.7", scripts=("tools.js",))
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("مختبر النمو", "/مختبر-النمو/"), ("قاموس التسويق", None)]
    b = banner(rel, trail, 'قاموس <span class="lat">Glossary</span>', "قاموس التسويق الإلكتروني", "تعريفات مختصرة بصيغها الحسابية لأشهر المصطلحات، بحث فوري واختصار كل ما يُقال في الاجتماعات.",
               "book", ["CPM", "ROAS", "SEO"], "mint", seed="glossary", uid="gl", kind="tool")
    rows = "".join(f'<div class="term" data-t="{esc(a + " " + b_ + " " + c)}" id="t-{i}"><dt><span class="lat">{esc(a)}</span><em>{esc(b_)}</em></dt><dd>{esc(c)}</dd></div>' for i, (a, b_, c) in enumerate(GLOSSARY))
    body = b + sec('<div class="gl-search"><label class="sr" for="gl-q">ابحث في القاموس</label>' + ico("search", 20) + '<input id="gl-q" type="search" placeholder="ابحث: ROAS، التحويل، سيو…" autocomplete="off"><span id="gl-n" class="muted" aria-live="polite"></span></div>'
                   f'<dl class="terms" id="gl-list">{rows}</dl><p class="empty" id="gl-empty" hidden>لا توجد نتائج مطابقة. جرّب كلمة أخرى.</p>', "alt")
    body += cta_band(pg, "مصطلح غير واضح؟", "اسألنا وسنشرحه بمثال من نشاطك.", "مرحباً يدير، لدي سؤال عن مصطلح تسويقي.")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "DefinedTermSet", "name": "قاموس التسويق الإلكتروني", "inLanguage": "ar", "url": abs_url(pg.path),
                 "hasDefinedTerm": [{"@type": "DefinedTerm", "name": f"{a} — {b_}", "description": c} for a, b_, c in GLOSSARY]}]
    og_job("glossary", "قاموس التسويق الإلكتروني", "مختبر النمو · Glossary", "book", ["CPM", "ROAS", "SEO"], "mint")
    add(pg)


# ───────────────────────── المدونة ─────────────────────────
AR_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]


def ar_date(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d} {AR_MONTHS[m - 1]} {y}"


def build_blog_hub():
    pg = Page("/المدونة/", f"المدونة: مقالات عملية في التسويق الإلكتروني والسيو والقياس | يدير",
              "مقالات عربية عملية من يدير عن حساب العائد الإعلاني، الميزانية، قوائم فحص الحملات، السيو، الواتساب والتتبّع.", "", og="blog", priority="0.8")
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("المدونة", None)]
    b = banner(rel, trail, 'المدونة <span class="lat">Insights</span>', "محتوى يساعدك على القرار", "مقالات قصيرة وعملية، كل منها يرتبط بأداة تجرّبها وخدمة تفصّلها.", "pen", ["ROAS", "SEO", "تتبّع"], "mint", seed="blog", uid="bg", kind="tool")
    cards = "".join(
        f'<a class="card post rv" href="{rel("/المدونة/" + p["slug"] + "/")}" style="--d:{(i % 3) * .07}s"><span class="pill">{esc(p["cat"])}</span><h2 class="h3">{esc(p["title"])}</h2><p>{esc(p["desc"])}</p>'
        f'<span class="meta">{ar_date(p["date"])} · {p["read"]} دقائق قراءة</span></a>' for i, p in enumerate(POSTS))
    body = b + sec(f'<div class="cards">{cards}</div>', "alt") + cta_band(pg, "تريد مقالاً عن موضوع محدد؟", "اكتب لنا السؤال الذي يشغلك، وقد يكون مقالنا القادم.", "مرحباً يدير، أقترح موضوعاً للمدونة: ")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "Blog", "name": "مدونة يدير", "url": abs_url(pg.path), "inLanguage": "ar", "publisher": {"@id": ORG_ID},
                 "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": abs_url("/المدونة/" + p["slug"] + "/"), "datePublished": p["date"]} for p in POSTS]}]
    og_job("blog", "محتوى يساعدك على القرار", "المدونة · Insights", "pen", ["ROAS", "SEO", "تتبّع"], "mint")
    add(pg)


def build_post(p, idx):
    path = f"/المدونة/{p['slug']}/"
    pg = Page(path, f"{p['title']} | يدير", p["desc"], "", og="post-" + str(idx + 1), og_type="article", priority="0.7", lastmod=p["date"])
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("المدونة", "/المدونة/"), (p["title"], None)]
    b = banner(rel, trail, f'{esc(p["cat"])} · {ar_date(p["date"])} · {p["read"]} دقائق قراءة', esc(p["title"]), esc(p["desc"]), "pen", [p["cat"], "مقال", "عملي"], "mint", seed=p["slug"], uid="p" + str(idx), kind="tool")
    sections = ""
    toc = ""
    for i, (h, paras) in enumerate(p["body"]):
        toc += f'<li><a href="#s{i + 1}">{esc(h)}</a></li>'
        body_html = ""
        for para in paras:
            if len(paras) > 1 and para[:2] in ("١.", "٢.", "٣.", "٤.", "٥.", "٦.", "٧.", "٨.", "٩.") or para.startswith("١٠."):
                body_html += f'<p class="item">{esc(para)}</p>'
            else:
                body_html += f'<p>{esc(para)}</p>'
        sections += f'<h2 id="s{i + 1}">{esc(h)}</h2>{body_html}'
    t = TOOL_BY_SLUG[p["tool"]]
    s = BY_SLUG[p["service"]]
    art = (f'<article class="article"><div class="art-grid"><aside class="toc card"><h2 class="h4">في هذا المقال</h2><ol>{toc}</ol></aside><div class="prose long">{sections}'
           f'<div class="try card"><span class="card-icon alt">{ico(t["icon"], 26)}</span><div><h3 class="h4">طبّق ما قرأت</h3><p>{esc(t["title"])}: {esc(t["short"])}</p></div>{btn(rel("/مختبر-النمو/" + t["slug"] + "/"), "افتح الأداة", "secondary", "arrow")}</div>'
           f'<div class="try card"><span class="card-icon">{ico(s["icon"], 26)}</span><div><h3 class="h4">تحتاج من ينفّذ؟</h3><p>{esc(s["title"])}: {esc(s["short"])}</p></div>{btn(rel("/الخدمات/" + s["slug"] + "/"), "تفاصيل الخدمة", "primary", "arrow")}</div>'
           f'</div></div></article>')
    body = b + sec(art, "alt")
    others = "".join(f'<a class="card post" href="{rel("/المدونة/" + o["slug"] + "/")}"><span class="pill">{esc(o["cat"])}</span><h3 class="h3">{esc(o["title"])}</h3><span class="meta">{o["read"]} دقائق قراءة</span></a>' for o in [x for x in POSTS if x is not p][:3])
    body += sec(head("اقرأ أيضاً", "مقالات أخرى") + f'<div class="cards">{others}</div>')
    body += cta_band(pg, "هل أفادك المقال؟", "ناقش مشروعك معنا ونحوّل ما قرأته إلى خطة.", f"مرحباً يدير، قرأت مقال «{p['title']}» وأريد مناقشة مشروعي.")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "inLanguage": "ar", "datePublished": p["date"], "dateModified": p["date"],
                 "mainEntityOfPage": abs_url(path), "image": f"{SITE_URL}/assets/img/og/post-{idx + 1}.png", "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "articleSection": p["cat"]},
                 faq_schema(p["faq"])]
    pg.bodycls = "is-article"
    og_job("post-" + str(idx + 1), p["title"], f'المدونة · {p["cat"]}', "pen", [p["cat"], "مقال", "عملي"], "mint")
    add(pg)


# ───────────────────────── من نحن / تواصل / قانونية ─────────────────────────
def info_box():
    soc = "".join(f'<a class="soc dark" href="{u}" target="_blank" rel="noopener me" aria-label="{n}">{ico(i, 20)}</a>' for n, u, i in
                  (("تيك توك", SITE["tiktok"], "tiktok"), ("إكس", SITE["x"], "x"), ("إنستغرام", SITE["instagram"], "instagram")))
    return (f'<div class="idbox card"><h2 class="h4">بيانات المنشأة</h2><dl><div><dt>الاسم التجاري</dt><dd>{SITE["name"]}</dd></div><div><dt>السجل التجاري</dt><dd class="lat">{SITE["cr"]}</dd></div>'
            f'<div><dt>الرقم الضريبي</dt><dd class="lat">{SITE["vat"]}</dd></div><div><dt>رقم التواصل</dt><dd class="lat"><a href="{tel()}">{SITE["phone_local"]}</a></dd></div></dl><div class="socials">{soc}</div></div>')


def build_about():
    pg = Page("/من-نحن/", f"من نحن: وكالة تسويق إلكتروني تُدير بالأرقام | يدير",
              "تعرّف على يدير للتسويق الإلكتروني: فكرة العلامة، طريقة عملنا، وبيانات المنشأة. وكالة تسويق وحلول تقنية في السعودية تبدأ من هدفك وتقيس النتائج.", "", og="about", priority="0.7")
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("من نحن", None)]
    b = banner(rel, trail, 'من نحن <span class="lat">About</span>', "نُدير حضورك الرقمي ليصل أبعد", "وكالة تسويق إلكتروني وحلول تقنية. نختصر الطريق بين فكرتك وعميلك بخطة واضحة وأرقام تُراجع باستمرار.",
               "compass", ["إطار", "شبكة", "وصول"], "teal", seed="about", uid="ab", kind="tool")
    concept = [("الإطار", "مربع بزوايا دائرية: مساحة منظّمة ومدارة، هي هويتك وخطتك وبنيتك الرقمية."),
               ("الشبكة", "حرف Y بأطراف دائرية كأيقونة المشاركة: نقاط اتصال بين علامتك وجمهورها."),
               ("الوصول", "النقطة الخارجة عن المربع: وصول العلامة أبعد من حدودها إلى جمهور جديد.")]
    cc = "".join(f'<div class="princ rv"><h3 class="h4">{t}</h3><p>{d}</p></div>' for t, d in concept)
    vals = [("وضوح", "نكتب الخطة والأرقام قبل التنفيذ ونشرح ما نفعله بلغة بسيطة."), ("قياس", "لا نحكم على عمل دون رقم، ولا نركّب حملة دون تتبّع."), ("صراحة", "إن كان الأنسب لك حلاً أبسط أو أقل كلفة نقوله، حتى لو لم نكن المنفّذ.")]
    vv = "".join(f'<div class="princ rv"><h3 class="h4">{t}</h3><p>{d}</p></div>' for t, d in vals)
    body = b + sec(f'<div class="two"><div>{head("من نحن", "وكالة تبدأ من رقمك")}<div class="prose"><p>يدير للتسويق الإلكتروني وكالة تجمع التسويق والتقنية تحت سقف واحد. نخطّط الحملة، ونبني الموقع أو المتجر الذي تصل إليه، ونركّب التتبّع الذي يقيسها، ثم نقرأ الأرقام معك ونحسّن.</p>'
                   f'<p>نؤمن أن العميل يستحق أن يعرف ماذا يدفع ولماذا وماذا عاد عليه. لهذا نكتب مؤشر النجاح لكل خدمة قبل أن نبدأ، ونفتح لك أدوات الحساب في مختبر النمو لتتحقق بنفسك.</p></div></div>{info_box()}</div>', "alt")
    body += sec(head("فكرة العلامة <span class=lat>Brand idea</span>", "ماذا يعني شعارنا؟", "اسم «يدير» يعني يقود ويشغّل وينظّم. والرمز يحمل ثلاث دلالات.") + f'<div class="princs three">{cc}</div>', "soft")
    body += sec(head("قيمنا", "كيف نعمل") + f'<div class="princs three">{vv}</div>')
    body += cta_band(pg, "لنبدأ بحديث قصير؟", "اكتب لنا عن مشروعك وهدفك ونردّ عليك.", "مرحباً يدير، أود التعرّف عليكم أكثر.")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "AboutPage", "name": "من نحن", "url": abs_url(pg.path), "inLanguage": "ar", "about": {"@id": ORG_ID}}]
    og_job("about", "نُدير حضورك الرقمي ليصل أبعد", "من نحن · About", "compass", ["إطار", "شبكة", "وصول"], "teal")
    add(pg)


def build_contact():
    pg = Page("/تواصل-معنا/", f"تواصل معنا: اتصال وواتساب وطلب عرض سعر | يدير",
              "تواصل مع يدير للتسويق الإلكتروني: اتصال أو واتساب على 0534644498، نموذج طلب عرض سعر، وحساباتنا على تيك توك وإنستغرام وإكس.", "", og="contact", priority="0.8", scripts=("tools.js",))
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("تواصل معنا", None)]
    b = banner(rel, trail, 'تواصل معنا <span class="lat">Contact</span>', "لنتحدّث عن مشروعك", "اتصال أو واتساب أو نموذج قصير. نرد عليك ونرسل خطة مختصرة وعرض سعر مكتوباً.", "phone", ["اتصال", "واتساب", "نموذج"], "teal", seed="contact", uid="ct", kind="tool")
    opts = '<option value="">اختر الخدمة (اختياري)</option>' + "".join(f'<option>{esc(s["title"])}</option>' for s in SERVICES)
    cards = (f'<a class="c-card" href="{tel()}">{ico("call", 26)}<strong>اتصال مباشر</strong><span class="lat">{SITE["phone_local"]}</span></a>'
             f'<a class="c-card" href="{wa_link("مرحباً يدير، أرغب في الاستفسار.")}" target="_blank" rel="noopener">{ico("whatsapp", 26)}<strong>واتساب</strong><span>ردّ سريع على استفسارك</span></a>'
             f'<a class="c-card" href="{SITE["instagram"]}" target="_blank" rel="noopener me">{ico("instagram", 26)}<strong>إنستغرام</strong><span class="lat">@yadeer_agency</span></a>'
             f'<a class="c-card" href="{SITE["tiktok"]}" target="_blank" rel="noopener me">{ico("tiktok", 26)}<strong>تيك توك</strong><span class="lat">@yadeer_agency</span></a>'
             f'<a class="c-card" href="{SITE["x"]}" target="_blank" rel="noopener me">{ico("x", 26)}<strong>إكس</strong><span class="lat">@Yadeer_Agency</span></a>')
    form = f'''<form class="card form" data-wa-form id="book"><h2 class="h3">اطلب عرض سعر</h2><p class="muted">عند الإرسال تُفتح محادثة واتساب بالرسالة جاهزة، فتراجعها ثم ترسلها.</p>
<div class="fld"><label for="f-name">الاسم</label><div class="inp"><input id="f-name" name="name" type="text" autocomplete="name" required></div></div>
<div class="fld"><label for="f-phone">رقم الجوال</label><div class="inp"><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="05xxxxxxxx"></div></div>
<div class="fld"><label for="f-svc">الخدمة</label><div class="inp sel"><select id="f-svc" name="svc">{opts}</select></div></div>
<div class="fld"><label for="f-msg">عن مشروعك</label><div class="inp"><textarea id="f-msg" name="msg" rows="4" placeholder="نشاطك، هدفك، وما جرّبته من قبل"></textarea></div></div>
<button class="btn btn-primary" type="submit"><span>أرسل عبر واتساب</span>{ico("whatsapp", 18)}</button>
<p class="note">بإرسالك تقرّ بالاطلاع على <a href="{rel("/سياسة-الخصوصية/")}">سياسة الخصوصية</a>.</p></form>'''
    body = b + sec(f'<div class="c-cards">{cards}</div>', "alt") + sec(f'<div class="two">{form}<div>{info_box()}</div></div>')
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "ContactPage", "name": "تواصل معنا", "url": abs_url(pg.path), "inLanguage": "ar", "about": {"@id": ORG_ID}}]
    og_job("contact", "لنتحدّث عن مشروعك", "تواصل معنا · Contact", "phone", ["اتصال", "واتساب", "نموذج"], "teal")
    add(pg)


def build_legal(slug, title, h1, desc, data, icon, key):
    pg = Page(f"/{slug}/", f"{title} | يدير", desc, "", og=key, priority="0.3")
    rel = pg.rel
    trail = [("الرئيسية", "/"), (title, None)]
    b = plain_banner(rel, trail, f'آخر تحديث: {SITE["updated_ar"]}', h1, desc, icon, key, key)
    toc = "".join(f'<li><a href="#l{i + 1}">{esc(h)}</a></li>' for i, (h, _) in enumerate(data))
    secs = ""
    for i, (h, paras) in enumerate(data):
        ps = [fmt_legal(x) for x in paras]
        if len(ps) > 1 and all(len(x) < 260 for x in ps) and h not in ("مقدمة", "القبول"):
            body = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in ps) + "</ul>"
        else:
            body = "".join(f"<p>{esc(x)}</p>" for x in ps)
        secs += f'<h2 id="l{i + 1}">{i + 1}. {esc(h)}</h2>{body}'
    body = b + sec(f'<div class="art-grid"><aside class="toc card"><h2 class="h4">المحتويات</h2><ol>{toc}</ol></aside><div class="prose long legal">{secs}'
                   f'<p class="note">هذه الوثيقة تعريفية عامة، ويُنصح بمراجعتها مع مستشار قانوني مرخّص قبل الاعتماد عليها في نزاع أو عقد.</p></div></div>', "alt")
    pg.body = body
    pg.schema = [breadcrumb_schema(trail), {"@type": "WebPage", "name": title, "url": abs_url(pg.path), "inLanguage": "ar", "dateModified": SITE["updated"]}]
    og_job(key, h1, title, icon, [], "mint")
    add(pg)


def build_sitemap_page():
    pg = Page("/خريطة-الموقع/", f"خريطة الموقع | يدير", "خريطة موقع يدير: كل الصفحات والخدمات والأدوات والمقالات في مكان واحد.", "", og="sitemap", priority="0.3")
    rel = pg.rel
    trail = [("الرئيسية", "/"), ("خريطة الموقع", None)]
    b = plain_banner(rel, trail, "Sitemap", "خريطة الموقع", "كل صفحات الموقع في مكان واحد.", "map", "sitemap", "sm")
    li = lambda items: "<ul>" + "".join(f'<li><a href="{rel(p)}">{esc(t)}</a></li>' for t, p in items) + "</ul>"
    cols = [("الصفحات", [("الرئيسية", "/"), ("من نحن", "/من-نحن/"), ("تواصل معنا", "/تواصل-معنا/"), ("المدونة", "/المدونة/"), ("سياسة الخصوصية", "/سياسة-الخصوصية/"), ("شروط الاستخدام", "/شروط-الاستخدام/")]),
            ("خدمات تسويقية", [(s["title"], f"/الخدمات/{s['slug']}/") for s in SERVICES if s["group"] == "marketing"]),
            ("خدمات تقنية", [(s["title"], f"/الخدمات/{s['slug']}/") for s in SERVICES if s["group"] == "tech"]),
            ("مختبر النمو", [("كل الأدوات", "/مختبر-النمو/")] + [(t["title"], f"/مختبر-النمو/{t['slug']}/") for t in TOOLS] + [("قاموس التسويق", "/قاموس-التسويق/")]),
            ("المدونة", [(p["title"], f"/المدونة/{p['slug']}/") for p in POSTS])]
    grid = "".join(f'<div><h2 class="h4">{h}</h2>{li(i)}</div>' for h, i in cols)
    pg.body = b + sec(f'<div class="sm-grid">{grid}</div>', "alt")
    pg.schema = [breadcrumb_schema(trail)]
    og_job("sitemap", "خريطة الموقع", "Sitemap", "map", [], "mint")
    add(pg)


def build_404():
    pg = Page("/404.html", f"الصفحة غير موجودة | يدير", "الصفحة المطلوبة غير موجودة. عُد إلى الرئيسية أو تصفّح خدماتنا وأدواتنا.", "", og="home", noindex=True, in_sitemap=False)
    rel = pg.rel
    pg.body = (f'<section class="sec"><div class="wrap center nf"><p class="big lat">404</p><h1 class="h2">هذه الصفحة غير موجودة</h1><p class="lead">ربما تغيّر الرابط أو حُذفت الصفحة. جرّب إحدى الوجهات التالية.</p>'
               f'<div class="actions">{btn(rel("/"), "الرئيسية", "primary")}{btn(rel("/الخدمات/"), "الخدمات", "secondary")}{btn(rel("/مختبر-النمو/"), "مختبر النمو", "secondary")}</div></div></section>')
    add(pg)


# ───────────────────────── الإخراج ─────────────────────────
def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


KW = {
    "ادارة-الحملات-الاعلانية": "اعلان اعلانات حملات حملة ممول ممولة ميتا فيسبوك انستقرام انستغرام جوجل سناب تيك توك اعلاني",
    "ادارة-حسابات-التواصل-الاجتماعي": "سوشيال ميديا تواصل اجتماعي حسابات نشر منشورات ستوري انستقرام تويتر اكس",
    "صناعة-المحتوى": "محتوى كتابة نصوص مقالات تصميم كوبي",
    "تحسين-محركات-البحث": "سيو seo جوجل ارشفة فهرسة ترتيب كلمات مفتاحية بحث",
    "الهوية-البصرية-والتصميم": "هوية شعار لوجو تصميم الوان خطوط براند",
    "انتاج-الفيديو-والموشن-جرافيك": "فيديو موشن جرافيك مونتاج ريلز تصوير مقاطع",
    "التسويق-عبر-المؤثرين": "مؤثرين مشاهير بلوقر انفلونسر اعلان مشهور",
    "التسويق-بالبريد-والواتساب": "بريد ايميل واتساب رسائل sms قوائم سلة متروكة",
    "الاستشارات-وخطط-التسويق": "استشارة خطة تسويق دراسة سوق منافسين",
    "تصميم-وبرمجة-المواقع-الالكترونية": "موقع مواقع ويب صفحة هبوط برمجة موقع شركة",
    "تصميم-المتاجر-الالكترونية": "متجر متاجر سلة زد شوبيفاي ووكومرس بيع اونلاين",
    "برمجة-تطبيقات-الجوال": "تطبيق تطبيقات جوال ايفون اندرويد موبايل",
    "الانظمة-ولوحات-التحكم": "نظام انظمة لوحة تحكم crm موظفين موارد بشرية حضور رواتب",
    "الاتمتة-والذكاء-الاصطناعي": "اتمتة ذكاء اصطناعي بوت شات بوت ربط api ai",
    "تصميم-واجهات-وتجربة-المستخدم": "واجهات تجربة مستخدم ux ui تصميم واجهة",
    "الاستضافة-والدعم-الفني": "استضافة دومين دعم فني ssl نسخ احتياطي صيانة",
    "تحليل-البيانات-والتتبع": "تتبع تحليل بيانات جي ايه ga4 بكسل tag manager لوحة مؤشرات",
    "الاستشارات-التقنية-والتحول-الرقمي": "استشارة تقنية تحول رقمي خارطة طريق",
}


def write_kb():
    kb = {
        "phone": SITE["phone_local"], "tel": tel(), "wa": SITE["wa"], "cr": SITE["cr"], "vat": SITE["vat"],
        "social": {"tiktok": SITE["tiktok"], "x": SITE["x"], "instagram": SITE["instagram"]},
        "services": [{"t": s["title"], "u": f"الخدمات/{s['slug']}/", "d": s["short"], "k": KW.get(s["slug"], ""), "g": s["group"]} for s in SERVICES],
        "tools": [{"t": t["title"].split(" (")[0], "u": f"مختبر-النمو/{t['slug']}/", "d": t["short"]} for t in TOOLS],
        "posts": [{"t": p["title"], "u": f"المدونة/{p['slug']}/"} for p in POSTS],
    }
    write("assets/data/kb.json", json.dumps(kb, ensure_ascii=False, separators=(",", ":")))


def write_sitemap_files():
    urls = []
    for p in PAGES:
        if not p.in_sitemap:
            continue
        urls.append(f"<url><loc>{abs_url(p.path)}</loc><lastmod>{p.lastmod}</lastmod><priority>{p.priority}</priority></url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": SITE["name"], "short_name": "يدير", "lang": "ar", "dir": "rtl", "start_url": "/", "display": "standalone",
        "background_color": "#FAFAFA", "theme_color": "#008F82",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
        ensure_ascii=False, indent=2))
    write("_headers", "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n"
                      "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n")
    write(".nojekyll", "")
    write(".htaccess", """# استضافة Apache / LiteSpeed (هوستنجر)
DirectoryIndex index.html
ErrorDocument 404 /404.html
Options -Indexes
AddDefaultCharset UTF-8
AddType image/svg+xml .svg
AddType application/manifest+json .webmanifest
# لتفعيل التحويل الإجباري إلى HTTPS بعد تفعيل شهادة SSL: أزل علامة # من الأسطر الثلاثة التالية
# RewriteEngine On
# RewriteCond %{HTTPS} off
# RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [L,R=301]
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml application/xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
</IfModule>
""")


def og_html(job):
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:Cairo;font-weight:300 900;src:url(file://{OUT}/assets/fonts/cairo-arabic.woff2) format('woff2');unicode-range:U+0600-06FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE80-FEFC}}
@font-face{{font-family:Cairo;font-weight:300 900;src:url(file://{OUT}/assets/fonts/cairo-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;background:#303032;font-family:Cairo,sans-serif;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:56px 64px;position:relative;overflow:hidden}}
.t{{width:560px;display:flex;flex-direction:column;gap:26px;z-index:2}}.eb{{color:#B8E5DF;font-size:24px;font-weight:700}}h1{{font-size:{54 if len(job["h1"]) < 40 else 46}px;line-height:1.3;font-weight:800}}
.logo{{width:240px}}.art{{width:520px;height:auto;z-index:2}}.art svg{{width:100%;height:auto;display:block}}.bg{{position:absolute;inset:auto auto -120px -80px;opacity:.12}}
.u{{position:absolute;bottom:34px;right:64px;color:#B8E5DF;font-size:20px;direction:ltr;font-weight:600}}
</style></head><body><div class="t"><img class="logo" src="file://{OUT}/assets/img/logo-white.svg" alt=""><p class="eb">{job["eyebrow"]}</p><h1>{esc(job["h1"])}</h1></div>
<div class="art">{job["svg"]}</div><div class="u">YADEER · Grow further.</div></body></html>'''


def main():
    if os.path.exists(OGTMP):
        shutil.rmtree(OGTMP)
    os.makedirs(OGTMP)
    # صفحات
    build_home()
    build_services_hub()
    for i, s in enumerate(SERVICES):
        build_service(s, i)
    build_lab_hub()
    for i, t in enumerate(TOOLS):
        build_tool(t, i)
    build_glossary()
    build_blog_hub()
    for i, p in enumerate(POSTS):
        build_post(p, i)
    build_about()
    build_contact()
    build_legal("سياسة-الخصوصية", "سياسة الخصوصية", "سياسة الخصوصية", "كيف نجمع بياناتك الشخصية ونستخدمها ونحميها عند استخدام موقع يدير، وحقوقك بموجب نظام حماية البيانات الشخصية.", PRIVACY, "shield", "privacy")
    build_legal("شروط-الاستخدام", "شروط الاستخدام", "شروط وأحكام الاستخدام", "الشروط والأحكام المنظّمة لاستخدام موقع يدير وأدواته التفاعلية وخدماته، بما فيها حدود المسؤولية والملكية الفكرية.", TERMS, "scale", "terms")
    build_sitemap_page()
    build_404()
    for p in PAGES:
        out = "404.html" if p.path == "/404.html" else p.path.strip("/") + "/index.html" if p.path != "/" else "index.html"
        write(out, render(p))
    write_sitemap_files()
    write_kb()
    for j in OG_JOBS:
        with open(os.path.join(OGTMP, j["key"] + ".html"), "w", encoding="utf-8") as f:
            f.write(og_html(j))
    print(f"✓ {len(PAGES)} صفحة · {len(OG_JOBS)} صورة OG · SITE_URL={SITE_URL}")


if __name__ == "__main__":
    main()
