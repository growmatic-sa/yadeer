# -*- coding: utf-8 -*-
"""هيكل الصفحة: head، الرأس، التذييل، شريط الاتصال، المساعد."""
import json
from urllib.parse import quote
from lib import *
from content_misc import SITE, TOOLS
from content_services import SERVICES, GROUPS

SITE_NAME = SITE["name"]


class Page:
    def __init__(self, path, title, desc, body, og="home", og_type="website", schema=None, noindex=False,
                 scripts=(), bodycls="", priority="0.6", lastmod=None, in_sitemap=True):
        self.path, self.title, self.desc, self.body, self.og, self.og_type = path, title, desc, body, og, og_type
        self.schema, self.noindex, self.scripts, self.bodycls = schema or [], noindex, scripts, bodycls
        self.priority, self.lastmod, self.in_sitemap = priority, lastmod or SITE["updated"], in_sitemap
        self.abs_links = path == "/404.html"
        segs = [s for s in path.strip("/").split("/") if s] if path != "/404.html" else []
        self.depth = len(segs)

    def rel(self, target):
        """رابط نسبي من هذه الصفحة إلى مسار هدف داخل الموقع."""
        up = "../" * self.depth if self.depth else "./"
        if self.abs_links:
            up = "/"
        if target in ("/", ""):
            return up
        t = target.lstrip("/")
        parts = t.split("/")
        enc = "/".join(quote(p) if p else "" for p in parts)
        return up + enc

    def asset(self, p):
        return self.rel("/assets/" + p)


def nav_html(pg):
    svc_cols = []
    for g in ("marketing", "tech"):
        links = "".join(f'<a href="{pg.rel("/الخدمات/" + s["slug"] + "/")}">{esc(s["title"])}</a>' for s in SERVICES if s["group"] == g)
        svc_cols.append(f'<div><p class="dd-title">{GROUPS[g]["title"]}</p>{links}</div>')
    cur = lambda p: ' aria-current="page"' if pg.path.startswith(p) else ""
    wa = wa_link("مرحباً يدير، أرغب في حجز استشارة مجانية.")
    return f'''<header class="header"><div class="wrap header-in">
<a class="brand" href="{pg.rel("/")}" aria-label="{SITE_NAME} — الصفحة الرئيسية"><img src="{pg.asset("img/logo-ink.svg")}" alt="{SITE_NAME} — Yadeer digital marketing agency" width="148" height="55"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" data-menu-btn><span class="sr">القائمة</span>{ico("menu", 26, "i-open")}{ico("close", 26, "i-close")}</button>
<nav class="nav" id="nav" aria-label="التنقل الرئيسي">
<div class="dd" data-dd><button class="nav-link" type="button" aria-expanded="false"{cur("/الخدمات")}>الخدمات {ico("chev", 14, "chev")}</button>
<div class="dd-panel"><div class="dd-cols">{"".join(svc_cols)}</div><a class="dd-all" href="{pg.rel("/الخدمات/")}">كل الخدمات {ico("arrow", 16)}</a></div></div>
<a class="nav-link" href="{pg.rel("/مختبر-النمو/")}"{cur("/مختبر-النمو")}>مختبر النمو</a>
<a class="nav-link" href="{pg.rel("/المدونة/")}"{cur("/المدونة")}>المدونة</a>
<a class="nav-link" href="{pg.rel("/من-نحن/")}"{cur("/من-نحن")}>من نحن</a>
<a class="nav-link" href="{pg.rel("/تواصل-معنا/")}"{cur("/تواصل-معنا")}>تواصل معنا</a>
<a class="btn btn-primary btn-sm nav-cta" href="{wa}" target="_blank" rel="noopener">احجز استشارة مجانية</a>
</nav></div></header>'''


def footer_html(pg):
    def col(g):
        return "".join(f'<li><a href="{pg.rel("/الخدمات/" + s["slug"] + "/")}">{esc(s["title"])}</a></li>' for s in SERVICES if s["group"] == g)
    labs = "".join(f'<li><a href="{pg.rel("/مختبر-النمو/" + t["slug"] + "/")}">{esc(t["title"].split(" (")[0])}</a></li>' for t in TOOLS)
    social = "".join(
        f'<a class="soc" href="{u}" target="_blank" rel="noopener me" aria-label="{n}">{ico(i, 20)}</a>'
        for n, u, i in (("تيك توك", SITE["tiktok"], "tiktok"), ("إكس", SITE["x"], "x"), ("إنستغرام", SITE["instagram"], "instagram")))
    return f'''<footer class="footer"><div class="wrap">
<div class="foot-top"><div class="foot-about">
<a class="brand" href="{pg.rel("/")}" aria-label="{SITE_NAME}"><img src="{pg.asset("img/logo-white.svg")}" alt="{SITE_NAME}" width="170" height="63" loading="lazy"></a>
<p>وكالة تسويق إلكتروني وحلول تقنية تُدير حضورك الرقمي بخطة واضحة وأرقام تُراجع باستمرار.</p>
<div class="socials">{social}</div></div>
<div class="foot-grid">
<div><h2>خدمات تسويقية</h2><ul>{col("marketing")}</ul></div>
<div><h2>خدمات تقنية</h2><ul>{col("tech")}</ul></div>
<div><h2>مختبر النمو</h2><ul>{labs}<li><a href="{pg.rel("/قاموس-التسويق/")}">قاموس التسويق</a></li></ul></div>
<div><h2>الموقع</h2><ul>
<li><a href="{pg.rel("/من-نحن/")}">من نحن</a></li><li><a href="{pg.rel("/المدونة/")}">المدونة</a></li>
<li><a href="{pg.rel("/تواصل-معنا/")}">تواصل معنا</a></li><li><a href="{pg.rel("/سياسة-الخصوصية/")}">سياسة الخصوصية</a></li>
<li><a href="{pg.rel("/شروط-الاستخدام/")}">شروط الاستخدام</a></li><li><a href="{pg.rel("/خريطة-الموقع/")}">خريطة الموقع</a></li></ul>
<h2 class="mt">تواصل</h2><ul>
<li><a href="{tel()}"><bdi class="lat">{SITE["phone_local"]}</bdi></a></li>
<li><a href="{wa_link("مرحباً يدير، أرغب في الاستفسار.")}" target="_blank" rel="noopener">واتساب</a></li></ul></div>
</div></div>
<div class="legal-box"><div><span>السجل التجاري</span><strong class="lat">{SITE["cr"]}</strong></div><div><span>الرقم الضريبي</span><strong class="lat">{SITE["vat"]}</strong></div>
<div><span>الاتصال</span><strong class="lat"><a href="{tel()}">{SITE["phone_local"]}</a></strong></div></div>
<div class="foot-bottom"><span>© <span data-year>2026</span> {SITE_NAME}. جميع الحقوق محفوظة.</span><span class="lat">YADEER · Grow further.</span></div>
</div></footer>'''


def dock_html(pg):
    wa = wa_link("مرحباً يدير، أرغب في الاستفسار عن خدماتكم.")
    return f'''<div class="dock" role="group" aria-label="أزرار التواصل السريع">
<a class="dock-btn dock-call" href="{tel()}" aria-label="اتصل بنا {SITE["phone_local"]}">{ico("call", 24)}<span>اتصال</span></a>
<a class="dock-btn dock-wa" href="{wa}" target="_blank" rel="noopener" aria-label="تواصل عبر واتساب">{ico("whatsapp", 26)}<span>واتساب</span></a>
<button class="dock-btn dock-chat" type="button" aria-expanded="false" aria-controls="yd-chat" data-chat-open>{ico("chat", 24)}<span>مساعد شركة يدير</span></button>
</div>
<section class="chat" id="yd-chat" role="dialog" aria-labelledby="chat-title" hidden>
<header class="chat-h"><span class="av"><img src="{pg.asset("img/symbol.svg")}" alt="" width="26" height="26"></span>
<div><strong id="chat-title">مساعد شركة يدير</strong><small>يجيب عن الخدمات والأدوات والتواصل</small></div>
<button class="chat-x" type="button" aria-label="إغلاق المساعد" data-chat-close>{ico("close", 20)}</button></header>
<div class="chat-log" role="log" aria-live="polite"></div>
<div class="chat-chips" aria-label="اقتراحات"></div>
<form class="chat-f" autocomplete="off"><label class="sr" for="chat-in">اكتب سؤالك</label><input id="chat-in" type="text" placeholder="اكتب سؤالك هنا…" maxlength="300">
<button type="submit" aria-label="إرسال">{ico("send", 20)}</button></form>
<div class="chat-ft"><a href="{wa}" target="_blank" rel="noopener" data-chat-wa>{ico("whatsapp", 16)} تحدّث مع فريقنا على واتساب</a></div>
</section>'''


def render(pg, root_hint=True):
    url = abs_url(pg.path) if pg.path != "/404.html" else SITE_URL + "/404.html"
    title = esc(pg.title)
    desc = esc(pg.desc)
    og_img = f"{SITE_URL}/assets/img/og/{pg.og}.png"
    robots = "noindex, follow" if pg.noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    graph = [org_schema(), website_schema()] + pg.schema
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    head_scripts = "".join(f'<script src="{pg.asset("js/" + s)}" defer></script>' for s in ("main.js", "fx.js", "chat.js", *pg.scripts))
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar-SA" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#008F82">
<meta name="author" content="{SITE_NAME}">
<meta property="og:type" content="{pg.og_type}">
<meta property="og:locale" content="ar_SA">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="{pg.asset("img/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{pg.asset("img/favicon-32.png")}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{pg.asset("img/apple-touch-icon.png")}">
<link rel="manifest" href="{pg.rel("/site.webmanifest")}">
<link rel="preload" href="{pg.asset("fonts/cairo-arabic.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pg.asset("css/style.css")}">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">{ld}</script>
</head>
<body data-root="{pg.rel("/")}" data-wa="{SITE["wa"]}" class="{pg.bodycls}">
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<div class="progress" aria-hidden="true"></div>
{nav_html(pg)}
<main id="main">
{pg.body}
</main>
{footer_html(pg)}
{dock_html(pg)}
{head_scripts}
</body>
</html>
'''
