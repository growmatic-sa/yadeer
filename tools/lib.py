# -*- coding: utf-8 -*-
"""مكتبة عناصر الموقع: أيقونات، بنرات، رأس وتذييل، مساعد الصفحة."""
import html, json, os, re
from urllib.parse import quote
from content_misc import SITE
from content_services import SERVICES, GROUPS

SITE_URL = os.environ.get("SITE_URL", "https://yadeer.sa").rstrip("/")

# ───────────────────────── أيقونات ─────────────────────────
S = "stroke"
ICONS = {
    "target": (S, '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12l7.5-7.5M19.5 4.5v4M19.5 4.5h-4"/>'),
    "chat": (S, '<path d="M4 5.5h16v11H10.5L6 20.5v-4H4z"/><path d="M8 9.5h8M8 12.5h5"/>'),
    "pen": (S, '<path d="M4 20l1-5L16 4l4 4L9 19z"/><path d="M13.5 6.5l4 4"/>'),
    "search": (S, '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>'),
    "shapes": (S, '<rect x="3" y="3" width="8" height="8" rx="2"/><circle cx="17" cy="7" r="4"/><path d="M12 21l4.5-8 4.5 8z"/><path d="M3 21l4-7 4 7z"/>'),
    "video": (S, '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9v6l5-3z"/>'),
    "users": (S, '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M16 4.6a3.5 3.5 0 010 6.8M18 14.5c2.2.8 3.5 2.6 3.5 5.5"/>'),
    "mail": (S, '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/>'),
    "compass": (S, '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>'),
    "browser": (S, '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M6.5 6.5h.01M9.5 6.5h.01"/>'),
    "cart": (S, '<path d="M3 4h3l2.4 11h10.2L21 7H7"/><circle cx="9.5" cy="19" r="1.5"/><circle cx="17.5" cy="19" r="1.5"/>'),
    "phone": (S, '<rect x="6" y="2.5" width="12" height="19" rx="3"/><path d="M10.5 18h3"/>'),
    "dashboard": (S, '<rect x="3" y="3" width="8" height="10" rx="2"/><rect x="13" y="3" width="8" height="6" rx="2"/><rect x="13" y="11" width="8" height="10" rx="2"/><rect x="3" y="15" width="8" height="6" rx="2"/>'),
    "bolt": (S, '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'),
    "layout": (S, '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M9 9v11"/>'),
    "server": (S, '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>'),
    "chart": (S, '<path d="M4 20V11M10 20V7M16 20v-6M22 20H2"/><path d="M4 7l6-4 6 5 5-4"/>'),
    "chip": (S, '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>'),
    "route": (S, '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 000-6H9a3 3 0 010-6h6.5"/>'),
    "calc": (S, '<rect x="5" y="3" width="14" height="18" rx="3"/><path d="M8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01"/>'),
    "loop": (S, '<path d="M20 12a8 8 0 01-14 5.3M4 12a8 8 0 0114-5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>'),
    "split": (S, '<path d="M12 4v7M12 11l-7 8M12 11l7 8"/><circle cx="12" cy="3.5" r="1.5"/><circle cx="5" cy="20" r="1.5"/><circle cx="19" cy="20" r="1.5"/>'),
    "pulse": (S, '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>'),
    "book": (S, '<path d="M5 4h11a3 3 0 013 3v13H8a3 3 0 01-3-3z"/><path d="M5 17a3 3 0 013-3h11"/>'),
    "shield": (S, '<path d="M12 3l8 3v6c0 4.5-3.2 7.8-8 9-4.8-1.2-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5L15.5 10"/>'),
    "scale": (S, '<path d="M12 3v18M6 21h12M5 7h14"/><path d="M5 7l-3 7a3 3 0 006 0zM19 7l-3 7a3 3 0 006 0z"/>'),
    "info": (S, '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>'),
    "map": (S, '<path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
    "arrow": (S, '<path d="M19 12H5M11 6l-6 6 6 6"/>'),
    "check": (S, '<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    "plus": (S, '<path d="M12 5v14M5 12h14"/>'),
    "menu": (S, '<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": (S, '<path d="M6 6l12 12M18 6L6 18"/>'),
    "chev": (S, '<path d="M6 9l6 6 6-6"/>'),
    "call": (S, '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>'),
    "send": (S, '<path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/>'),
    "copy": (S, '<rect x="8" y="8" width="12" height="12" rx="3"/><path d="M16 8V6a2 2 0 00-2-2H6a2 2 0 00-2 2v8a2 2 0 002 2h2"/>'),
    "refresh": (S, '<path d="M20 12a8 8 0 10-2.3 5.7M20 5v5h-5"/>'),
    "star": (S, '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>'),
    "instagram": (S, '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".9" fill="currentColor"/>'),
    "whatsapp": ("fill", '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>'),
    "tiktok": ("fill", '<path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>'),
    "x": ("fill", '<path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/>'),
}


def ico(name, size=22, cls=""):
    kind, inner = ICONS[name]
    if kind == "stroke":
        return (f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{inner}</svg>')
    return (f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">{inner}</svg>')


SYMBOL_PATH = ("M196.737 32.234 A50 50 0 0 1 200 50 V150 A50 50 0 0 1 150 200 H50 A50 50 0 0 1 0 150 V50 A50 50 0 0 1 50 0 "
               "H150 A50 50 0 0 1 182.783 12.247 L100 95.029 L71.799 66.828 A20 20 0 1 0 54.828 83.799 L88 116.971 L88 144 "
               "A20 20 0 1 0 112 144 L112 116.971 Z")


def esc(t):
    return html.escape(str(t), quote=True)


def enc_path(path):
    """مسار عربي → مسار مرمّز (للروابط وsitemap)."""
    return "/" + "/".join(quote(p) for p in path.strip("/").split("/")) + ("/" if path.strip("/") else "")


def abs_url(path):
    if path in ("", "/"):
        return SITE_URL + "/"
    return SITE_URL + enc_path(path)


def wa_link(text):
    return f"https://wa.me/{SITE['wa']}?text={quote(text)}"


def tel():
    return f"tel:{SITE['phone_intl']}"


# ───────────────────────── خلفية الشبكة والبنرات ─────────────────────────
def _rng(seed):
    h = 2166136261
    for ch in seed:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    state = [h or 1]

    def r():
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state[0]
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + ((t ^ (t >> 7)) * (t | 61) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


SCHEMES = {
    "teal": dict(bg="#008F82", line="#B8E5DF", node="#B8E5DF", tile="#FAFAFA", ink="#303032", dot="#303032", chip="#FAFAFA", chipt="#303032"),
    "mint": dict(bg="#B8E5DF", line="#008F82", node="#008F82", tile="#FAFAFA", ink="#00766B", dot="#303032", chip="#FAFAFA", chipt="#303032"),
    "paper": dict(bg="#FAFAFA", line="#008F82", node="#008F82", tile="#303032", ink="#B8E5DF", dot="#008F82", chip="#303032", chipt="#FAFAFA"),
}


def art_svg(seed, icon, chips, scheme="teal", uid="a"):
    """بنر فني: إطار مستدير + شبكة نقاط + بلاطة أيقونة + شرائح كلمات."""
    c = SCHEMES[scheme]
    r = _rng(seed)
    W, H = 560, 440
    cx, cy = 280, 222
    kind, inner = ICONS[icon]
    nodes = []
    for ring, (rx, ry, n) in enumerate([(165, 120, 5), (225, 175, 6)]):
        base = r() * 6.28
        for i in range(n):
            import math
            a = base + i * (6.2832 / n) + (r() - .5) * .45
            nodes.append((cx + rx * math.cos(a) + (r() - .5) * 18, cy + ry * math.sin(a) + (r() - .5) * 14, 4 + r() * 5, ring))
    nodes = [(max(34, min(W - 34, x)), max(34, min(H - 34, y)), rad, rg) for x, y, rad, rg in nodes]
    lines, dots = [], []
    for i, (x, y, rad, rg) in enumerate(nodes):
        if rg == 0:
            lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')
    inner_nodes = [n for n in nodes if n[3] == 0]
    outer_nodes = [n for n in nodes if n[3] == 1]
    for i, n in enumerate(outer_nodes):
        m = inner_nodes[i % len(inner_nodes)]
        lines.append(f'<line x1="{m[0]:.1f}" y1="{m[1]:.1f}" x2="{n[0]:.1f}" y2="{n[1]:.1f}"/>')
    for i, n in enumerate(nodes):
        dots.append(f'<circle class="nd" style="--i:{i}" cx="{n[0]:.1f}" cy="{n[1]:.1f}" r="{n[2]:.1f}"/>')
    # شرائح
    pos = [(70 + (r() - .5) * 18, 70 + (r() - .5) * 14), (372 + (r() - .5) * 18, 60 + (r() - .5) * 14), (330 + (r() - .5) * 18, 372 + (r() - .5) * 10)]
    chip_svg = []
    for i, t in enumerate(chips[:3]):
        w = int(len(t) * (8.3 if re.search(r"[A-Za-z]", t) and not re.search(r"[؀-ۿ]", t) else 9.2) + 44)
        x, y = pos[i]
        if x + w > W - 18:
            x = W - 18 - w
        chip_svg.append(
            f'<g transform="translate({x:.0f} {y:.0f})"><g class="chip" style="--i:{i}"><rect width="{w}" height="38" rx="19" fill="{c["chip"]}"/>'
            f'<circle cx="{w - 20}" cy="19" r="5" fill="#008F82"/><text x="{(w - 28) / 2:.0f}" y="25" text-anchor="middle" fill="{c["chipt"]}" '
            f'font-family="Cairo,sans-serif" font-size="15" font-weight="700">{esc(t)}</text></g></g>')
    tile = (f'<g class="tile"><rect x="{cx - 80}" y="{cy - 80}" width="160" height="160" rx="42" fill="{c["tile"]}"/>'
            + (f'<g transform="translate({cx - 42} {cy - 42}) scale(3.5)" fill="none" stroke="{c["ink"]}" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round">{inner}</g>'
               if kind == "stroke" else '')
            + f'</g><circle class="acc" cx="{cx + 100}" cy="{cy - 100}" r="19" fill="{c["dot"]}"/>')
    return (f'<svg class="art" viewBox="0 0 {W} {H}" role="img" aria-label="رسم توضيحي" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><clipPath id="clip-{uid}"><rect width="{W}" height="{H}" rx="60"/></clipPath></defs>'
            f'<rect width="{W}" height="{H}" rx="60" fill="{c["bg"]}"/>'
            f'<g clip-path="url(#clip-{uid})">'
            f'<path d="{SYMBOL_PATH}" transform="translate(-40 236) scale(1.15)" fill="none" stroke="{c["line"]}" stroke-opacity=".35" stroke-width="1.6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="132" fill="none" stroke="{c["line"]}" stroke-opacity=".5" stroke-dasharray="3 9" stroke-linecap="round" class="orbit"/>'
            f'<circle cx="{cx}" cy="{cy}" r="196" fill="none" stroke="{c["line"]}" stroke-opacity=".3" stroke-dasharray="2 12" stroke-linecap="round" class="orbit o2"/>'
            f'<g stroke="{c["line"]}" stroke-opacity=".55" stroke-width="1.4">{"".join(lines)}</g>'
            f'<g fill="{c["node"]}">{"".join(dots)}</g></g>'
            f'{tile}{"".join(chip_svg)}</svg>')


def crumbs_html(trail, rel):
    items = []
    for i, (name, path) in enumerate(trail):
        if path is None:
            items.append(f'<li><span aria-current="page">{esc(name)}</span></li>')
        else:
            items.append(f'<li><a href="{rel(path)}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="مسار التنقل"><ol>{"".join(items)}</ol></nav>'


def banner(rel, trail, eyebrow, h1, lead, icon, chips, scheme="teal", actions="", seed="x", uid="b", kind="svc"):
    art = art_svg(seed, icon, chips, scheme, uid)
    return (f'<section class="banner b-{kind}"><div class="wrap banner-in"><div class="banner-copy">'
            f'{crumbs_html(trail, rel)}<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p>'
            f'<div class="actions">{actions}</div></div><div class="banner-art" aria-hidden="true">{art}</div></div></section>')


def plain_banner(rel, trail, eyebrow, h1, lead, icon, seed, uid):
    """بنر مختصر للصفحات القانونية والمعلوماتية."""
    return banner(rel, trail, eyebrow, h1, lead, icon, [], scheme="mint", seed=seed, uid=uid, kind="plain")


# ───────────────────────── عناصر مشتركة ─────────────────────────
def btn(href, label, kind="primary", icon="arrow", extra=""):
    return f'<a class="btn btn-{kind}" href="{href}" {extra}><span>{label}</span>{ico(icon, 18, "arw") if icon else ""}</a>'


def faq_html(items):
    out = []
    for q, a in items:
        out.append(f'<details class="qa"><summary><span>{esc(q)}</span>{ico("plus", 20, "plus")}</summary><div class="qa-a"><p>{esc(a)}</p></div></details>')
    return '<div class="faq">' + "".join(out) + "</div>"


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def breadcrumb_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": abs_url(p)} if p is not None else {})}
        for i, (n, p) in enumerate(trail)]}


ORG_ID = SITE_URL + "/#organization"


def org_schema():
    return {
        "@type": "ProfessionalService", "@id": ORG_ID, "name": SITE["name"], "alternateName": ["Yadeer", SITE["name_en"], "يدير"],
        "url": SITE_URL + "/", "logo": SITE_URL + "/assets/img/logo-512.png", "image": SITE_URL + "/assets/img/og/home.png",
        "description": "وكالة تسويق إلكتروني وحلول تقنية في المملكة العربية السعودية: حملات إعلانية، سيو، محتوى، مواقع، متاجر، تطبيقات، أنظمة وأتمتة.",
        "telephone": SITE["phone_intl"], "vatID": SITE["vat"], "taxID": SITE["vat"],
        "identifier": {"@type": "PropertyValue", "name": "السجل التجاري", "value": SITE["cr"]},
        "areaServed": {"@type": "Country", "name": "المملكة العربية السعودية"},
        "knowsLanguage": "ar",
        "sameAs": [SITE["tiktok"], SITE["x"], SITE["instagram"]],
        "contactPoint": [{"@type": "ContactPoint", "telephone": SITE["phone_intl"], "contactType": "customer service", "areaServed": "SA", "availableLanguage": "ar"}],
    }


def website_schema():
    return {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": SITE["name"], "inLanguage": "ar",
            "publisher": {"@id": ORG_ID}}


def network_bg(seed, w=1366, h=720, n=26):
    """شبكة نقاط وخطوط خلفية (من عناصر الهوية: سلسلة النقاط وخط الشبكة)."""
    import math
    r = _rng(seed)
    pts = [(r() * w, r() * h, 3 + r() * 5) for _ in range(n)]
    seen, lines = set(), []
    for i, (x, y, _) in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: (pts[j][0] - x) ** 2 + (pts[j][1] - y) ** 2)[1:3]
        for j in near:
            k = (min(i, j), max(i, j))
            if k in seen:
                continue
            seen.add(k)
            lines.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}"/>')
    dots = "".join(f'<circle class="nd" style="--i:{i}" cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}"/>' for i, (x, y, rad) in enumerate(pts))
    return (f'<svg class="hero-net" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<g stroke="#B8E5DF" stroke-opacity=".16" stroke-width="1.2">{"".join(lines)}</g><g fill="#B8E5DF" fill-opacity=".55">{dots}</g>'
            f'<path d="{SYMBOL_PATH}" transform="translate(60 330) scale(1.5)" fill="none" stroke="#B8E5DF" stroke-opacity=".12" stroke-width="1.6"/></svg>')
