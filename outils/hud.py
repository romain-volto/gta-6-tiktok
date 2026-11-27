#!/usr/bin/env python3
"""Rendu des carrousels TikTok GTA 6 au style « HUD · Roue des récompenses » (style choisi par Romain le 26/11).

Usage : python3 outils/hud.py posts/<dossier>/spec.json
Sortie : posts/<dossier>/slide-01.jpg ... (1080x1920, JPEG), plus /tmp/<dossier>-planche.jpg

Fond : plage de Vice City au coucher du soleil, floutée (outils/assets/plage-vice-city.svg).
Couleurs chaudes : ambre #FFB13D, orange #FF5A36, magenta #E8336D. Titres Barlow Condensed italique.
Dans tous les textes, <g>mot</g> met le mot en dégradé chaud.

Types de slides (champ "type") :
- "hook"  : accroche. Champs : label, sub (petit texte en haut à gauche), hud {plus, amount, stars} (facultatif, en haut à droite),
            chip, title, title_size, puis UN visuel au choix : wheel {left:{icon,l1,l2}, right:{icon,l1,l2}, center:[l1,l2], hint}
            | bignum {num, text} | image "img/x.jpg" (+ image_top, image_height, image_fit "cover" ou "contain",
            badge = pastille bien visible sur la miniature, ex. « Partie 2 ») | icon "nom"
            | memo {points [texte, 3 à 5], warn {title, text}} (fiche mémo : les étapes numérotées lisibles
            sur la miniature, placées juste sous le titre ; titre court conseillé, title_size 120 à 150).
            Puis pill (pastille en bas, ex. « L'ASTUCE EN 3 ÉTAPES → »).
- "steps" : étape. Champs : tag (ex. MISSION), step (ex. ÉTAPE 1/3), title, points [{icon, text}] (3 max conseillé,
            le dernier est mis en avant), warn {title, text} (facultatif), next (pastille du bas, facultatif).
- "photo" : photo du jeu. Champs : tag, title, image, caption (facultatif), next (facultatif).
- "versus": deux photos. Champs : tag, title, photos [{src, label}, {src, label}], caption (facultatif).
- "rows"  : liste. Champs : tag, title, rows [{k, v}] (ex. code et effet), next (facultatif).
- "cta"   : fin. Champs : title (question qui divise), comment, share.
- "meme"  : mème 100 % maison (sans capture). Champs : setup (bulle blanche en haut, ex. « POV : … »), variant :
            "echec" (gros MISSION ÉCHOUÉE + reason), "notifs" (notifs [{app, text}] façon téléphone),
            "stars" (étoiles de recherche : stars 1-5, label, reason), "wheel" (wheel comme dans hook),
            "objectif" (liste d'objectifs de mission : label, objectifs [texte], faits = nb cochés, note en dégradé
            dessous, ex. « Lucia va apprécier. »).
Icônes : moon, heli, fox, cash, smg, star, pin, car, key, eye, trophy, flame, lock, map, phone.
"""
import json, math, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
FONTS = (HERE / "fonts").as_uri()
BG = (HERE / "assets" / "plage-vice-city.svg").as_uri()
A, B, C = "#FFB13D", "#FF5A36", "#E8336D"
GLASS, LINE, GLOW = "rgba(42,8,14,.52)", "rgba(255,200,160,.32)", "rgba(255,90,54,.6)"
SAFE_BOTTOM = 1500

CSS = f"""
@font-face{{font-family:Inter;font-weight:800;src:url({FONTS}/inter-latin-800-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:800;src:url({FONTS}/inter-latin-ext-800-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:Inter;font-weight:900;src:url({FONTS}/inter-latin-900-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:900;src:url({FONTS}/inter-latin-ext-900-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:Barlow;font-weight:900;font-style:italic;src:url({FONTS}/barlow-condensed-latin-900-italic.woff2)}}
@font-face{{font-family:Barlow;font-weight:900;font-style:italic;src:url({FONTS}/barlow-condensed-latin-ext-900-italic.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:Bebas;src:url({FONTS}/bebas-neue-latin-400-normal.woff2)}}
@font-face{{font-family:Anton;src:url({FONTS}/anton-latin-400-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#1E0806}}
body{{position:relative;font-family:Inter;color:#fff;-webkit-font-smoothing:antialiased}}
.abs{{position:absolute}}
.bg{{position:absolute;inset:-40px;width:1160px;height:2000px;filter:blur(5px) saturate(1.25)}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,4,12,.6),rgba(26,4,12,.12) 42%,rgba(26,4,12,.38) 72%,rgba(26,4,12,.72))}}
.leak{{position:absolute;inset:0;background:radial-gradient(60% 40% at 100% 0%,rgba(255,170,80,.35),transparent 70%),radial-gradient(55% 35% at 0% 100%,rgba(255,80,60,.28),transparent 70%)}}
.vig{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 45%,transparent 55%,rgba(25,5,0,.5))}}
.grad{{background:linear-gradient(100deg,{A} 0%,{B} 50%,{C} 100%);-webkit-background-clip:text;background-clip:text;color:transparent;padding-right:.08em;filter:drop-shadow(2px 0 0 #3A0408) drop-shadow(-2px 0 0 #3A0408) drop-shadow(0 2px 0 #3A0408) drop-shadow(0 -2px 0 #3A0408) drop-shadow(0 7px 0 rgba(40,4,6,.8)) drop-shadow(0 0 18px rgba(255,140,90,.3))}}
.gbg{{background:linear-gradient(90deg,{A},{B} 50%,{C})}}
.glass{{background:{GLASS};border:2px solid {LINE};border-radius:30px;backdrop-filter:blur(16px)}}
.lab{{font:900 24px Inter;letter-spacing:5px;color:{A};text-transform:uppercase}}
.big{{font-family:Barlow;font-weight:900;font-style:italic;text-transform:uppercase;line-height:.9;letter-spacing:1px;text-shadow:0 10px 40px rgba(40,8,0,.5)}}
.chip{{display:inline-flex;align-items:center;gap:14px;padding:12px 24px;border-radius:999px;background:rgba(255,240,225,.14);border:2px solid rgba(255,230,200,.35);font:900 26px Inter;letter-spacing:4px;text-transform:uppercase}}
.dot{{width:16px;height:16px;border-radius:50%;background:{B};box-shadow:0 0 12px {B}}}
b,.hl{{color:{A};font-weight:900}}
.content{{position:absolute;left:70px;right:70px}}
.bub{{display:inline;background:#fff;color:#111;font:800 52px/1.34 Inter;padding:6px 18px;border-radius:18px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
"""

# ------------------------------------------------------------------ icônes (blanches, viewBox 0 0 64 64)
W = "#FFF6EC"
ICONS = {
    "moon": f'<defs><mask id="mm"><rect width="64" height="64" fill="#fff"/><circle cx="44" cy="20" r="20" fill="#000"/></mask></defs><circle cx="30" cy="34" r="24" fill="{W}" mask="url(#mm)"/>',
    "heli": f'<g fill="{W}"><ellipse cx="26" cy="34" rx="18" ry="11"/><rect x="36" y="30" width="26" height="6"/><rect x="2" y="14" width="50" height="5" rx="2"/><rect x="24" y="17" width="5" height="8"/><rect x="12" y="48" width="28" height="4"/></g>',
    "fox": f'<polygon points="10,26 16,6 27,18" fill="{W}"/><polygon points="54,26 48,6 37,18" fill="{W}"/><path d="M8 24 Q 32 10 56 24 Q 50 52 32 58 Q 14 52 8 24 Z" fill="{W}"/><circle cx="23" cy="34" r="4" fill="#B3261E"/><circle cx="41" cy="34" r="4" fill="#B3261E"/>',
    "cash": f'<rect x="4" y="16" width="56" height="32" rx="6" fill="{W}"/><circle cx="32" cy="32" r="9" fill="#B3261E"/><text x="32" y="37" text-anchor="middle" font-family="Anton" font-size="15" fill="{W}">$</text>',
    "smg": f'<path d="M3 24 L 42 24 L 42 20 L 56 20 L 56 25 L 62 25 L 62 29 L 42 29 L 42 32 L 34 32 L 31 48 L 24 48 L 27 32 L 19 32 L 17 36 L 9 36 L 8 32 L 3 32 Z" fill="{W}"/><path d="M35 32 L 40 32 L 43 46 L 38 46 Z" fill="{W}"/>',
    "star": f'<polygon points="32,4 40,24 61,24 44,37 50,58 32,45 14,58 20,37 3,24 24,24" fill="{W}"/>',
    "pin": f'<path d="M32 4 C 18 4 10 14 10 26 C 10 42 32 60 32 60 C 32 60 54 42 54 26 C 54 14 46 4 32 4 Z" fill="{W}"/><circle cx="32" cy="26" r="9" fill="#B3261E"/>',
    "car": f'<path d="M6 40 L 10 26 Q 12 20 20 20 L 44 20 Q 52 20 54 26 L 58 40 L 58 48 L 6 48 Z" fill="{W}"/><circle cx="18" cy="48" r="7" fill="#B3261E" stroke="{W}" stroke-width="4"/><circle cx="46" cy="48" r="7" fill="#B3261E" stroke="{W}" stroke-width="4"/>',
    "key": f'<circle cx="20" cy="32" r="13" fill="none" stroke="{W}" stroke-width="7"/><rect x="31" y="29" width="28" height="7" fill="{W}"/><rect x="48" y="35" width="6" height="10" fill="{W}"/>',
    "eye": f'<path d="M4 32 Q 32 6 60 32 Q 32 58 4 32 Z" fill="{W}"/><circle cx="32" cy="32" r="10" fill="#B3261E"/>',
    "trophy": f'<path d="M18 8 L 46 8 L 46 24 Q 46 40 32 40 Q 18 40 18 24 Z" fill="{W}"/><rect x="28" y="40" width="8" height="10" fill="{W}"/><rect x="18" y="50" width="28" height="7" rx="3" fill="{W}"/><path d="M18 14 L 8 14 Q 8 28 20 30" stroke="{W}" stroke-width="5" fill="none"/><path d="M46 14 L 56 14 Q 56 28 44 30" stroke="{W}" stroke-width="5" fill="none"/>',
    "flame": f'<path d="M32 4 C 36 18 50 24 50 40 C 50 52 42 60 32 60 C 22 60 14 52 14 40 C 14 30 22 24 24 14 C 28 22 30 26 32 28 C 34 20 34 12 32 4 Z" fill="{W}"/>',
    "lock": f'<rect x="12" y="28" width="40" height="30" rx="6" fill="{W}"/><path d="M20 28 L 20 20 Q 20 8 32 8 Q 44 8 44 20 L 44 28" stroke="{W}" stroke-width="7" fill="none"/>',
    "map": f'<polygon points="4,12 22,6 42,12 60,6 60,52 42,58 22,52 4,58" fill="{W}"/><path d="M22 6 L 22 52 M 42 12 L 42 58" stroke="#B3261E" stroke-width="3"/>',
    "phone": f'<rect x="16" y="4" width="32" height="56" rx="7" fill="{W}"/><rect x="21" y="11" width="22" height="38" rx="2" fill="#B3261E"/>',
}


def icon(name, size=56):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 64 64">{ICONS.get(name, ICONS["star"])}</svg>'


def esc_g(t):
    return t or ""


def star_points(cx, cy, n, r1, r2, rot=-90):
    return " ".join(f"{cx + (r1 if i % 2 == 0 else r2) * math.cos(math.radians(rot + i * 180 / n)):.1f},"
                    f"{cy + (r1 if i % 2 == 0 else r2) * math.sin(math.radians(rot + i * 180 / n)):.1f}" for i in range(n * 2))


def hud_top(s):
    out = ""
    if s.get("label") or s.get("sub"):
        out += (f'<div class="abs" style="top:86px;left:70px;max-width:560px"><div class="lab">{s.get("label", "")}</div>'
                f'<div style="font:800 40px Inter;margin-top:8px;text-shadow:0 2px 10px rgba(0,0,0,.5)">{s.get("sub", "")}</div></div>')
    h = s.get("hud")
    if h:
        stars = ""
        for i in range(5):
            on = i < h.get("stars", 0)
            stars += (f'<svg width="46" height="46" viewBox="0 0 100 100" style="opacity:{1 if on else .55}"><polygon points="{star_points(50, 54, 5, 48, 20)}" '
                      f'fill="{"#FFF3E0" if on else "none"}" stroke="#FFF3E0" stroke-width="7" stroke-linejoin="round"/></svg>')
        out += (f'<div class="abs" style="top:78px;right:70px;text-align:right">'
                + (f'<div style="font:900 34px Inter;color:{A};text-shadow:0 0 16px {GLOW}">{h["plus"]}</div>' if h.get("plus") else "")
                + (f'<div style="font:900 80px/1 Barlow;font-style:italic;color:{A};-webkit-text-stroke:4px #3A1204;paint-order:stroke fill">{h["amount"]}</div>' if h.get("amount") else "")
                + (f'<div style="display:flex;gap:8px;justify-content:flex-end;margin-top:6px">{stars}</div>' if "stars" in h else "") + "</div>")
    return out


def sector(cx, cy, r1, r2, a0, a1):
    a0, a1 = math.radians(a0), math.radians(a1)
    p = lambda r, a: f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}"
    return f"M{p(r1, a0)} L{p(r2, a0)} A{r2},{r2} 0 0 1 {p(r2, a1)} L{p(r1, a1)} A{r1},{r1} 0 0 0 {p(r1, a0)} Z"


def wheel(w):
    cx = cy = 380
    r1, r2 = 150, 340
    o = ['<svg width="760" height="760" viewBox="0 0 760 760" style="overflow:visible"><defs>'
         f'<linearGradient id="wg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{A}"/><stop offset=".5" stop-color="{B}"/><stop offset="1" stop-color="{C}"/></linearGradient>'
         '<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
         f'<circle cx="{cx}" cy="{cy}" r="{r2 + 22}" fill="none" stroke="rgba(255,230,200,.18)" stroke-width="3"/>']
    for i in range(6):
        c = i * 60
        d = sector(cx, cy, r1, r2, c - 28, c + 28)
        if i in (0, 3):
            o.append(f'<path d="{d}" fill="url(#wg)" stroke="#FFE8C8" stroke-width="4" filter="url(#gl)"/>'
                     f'<path d="{sector(cx, cy, r2 + 12, r2 + 26, c - 26, c + 26)}" fill="#FFE8C8"/>')
        else:
            mx, my = cx + 245 * math.cos(math.radians(c)), cy + 245 * math.sin(math.radians(c))
            o.append(f'<path d="{d}" fill="{GLASS}" stroke="{LINE}" stroke-width="3"/><circle cx="{mx:.0f}" cy="{my:.0f}" r="9" fill="rgba(255,240,225,.35)"/>')
    for side, sx in (("left", -245), ("right", 245)):
        it = w.get(side, {})
        o.append(f'<g transform="translate({cx + sx - 40},{cy - 88}) scale(1.25)">{ICONS.get(it.get("icon", "star"), ICONS["star"])}</g>')
        o.append(f'<text x="{cx + sx}" y="{cy + 34}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#fff">{it.get("l1", "")}</text>')
        o.append(f'<text x="{cx + sx}" y="{cy + 68}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="26" fill="#fff" opacity=".9">{it.get("l2", "")}</text>')
    l1, l2 = (w.get("center") or ["", ""])[:2]
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r1 - 14}" fill="rgba(34,6,10,.82)" stroke="url(#wg)" stroke-width="10"/>'
             f'<text x="{cx}" y="{cy - 22}" text-anchor="middle" font-family="Barlow" font-style="italic" font-weight="900" font-size="64" fill="#fff">{l1}</text>'
             f'<text x="{cx}" y="{cy + 40}" text-anchor="middle" font-family="Barlow" font-style="italic" font-weight="900" font-size="64" fill="url(#wg)">{l2}</text>')
    if w.get("hint"):
        o.append(f'<circle cx="{cx - 70}" cy="{cy + 84}" r="18" fill="#FFF8F0"/><text x="{cx - 70}" y="{cy + 92}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="22" fill="#1C9B3A">A</text>'
                 f'<text x="{cx - 44}" y="{cy + 91}" font-family="Inter" font-weight="800" font-size="20" fill="#FFF3E0" opacity=".85">{w["hint"]}</text>')
    return "".join(o) + "</svg>"


def img_uri(base, src):
    return (base / src).resolve().as_uri()


def pill(text, top):
    return f'<div class="abs" style="top:{top}px;left:0;right:0;text-align:center"><span class="chip" style="font-size:28px;letter-spacing:3px">{text}</span></div>' if text else ""


def head(s, top=86, size=176):
    tag = s.get("tag", "")
    step = s.get("step", "")
    out = f'<div class="content fitbox" style="top:{top}px">'
    if tag or step:
        out += ('<div style="display:flex;align-items:center;gap:18px">'
                + (f'<span class="gbg" style="color:#fff;font:900 26px Inter;letter-spacing:4px;padding:10px 18px;border-radius:10px;text-transform:uppercase">{tag}</span>' if tag else "")
                + (f'<span class="lab" style="color:#FFF3E0;opacity:.85">{step}</span>' if step else "") + "</div>")
    out += f'<div class="big fit" style="font-size:{s.get("title_size", size)}px;margin-top:22px">{s.get("title", "")}</div>'
    if step:
        out += '<div style="display:flex;gap:12px;margin-top:26px"><div class="gbg" style="width:160px;height:12px;border-radius:6px"></div><div style="width:160px;height:12px;border-radius:6px;background:rgba(255,240,225,.25)"></div></div>'
    return out + "</div>"


def warn_box(w):
    if not w:
        return ""
    return ('<div style="position:relative;margin-top:34px;border-radius:28px;overflow:hidden;background:linear-gradient(100deg,#FF5A36,#B3261E);box-shadow:0 0 50px rgba(255,90,54,.45)">'
            '<div style="position:absolute;inset:0;background:repeating-linear-gradient(-45deg,rgba(255,255,255,.08) 0 18px,transparent 18px 36px)"></div>'
            '<div style="position:relative;display:flex;gap:26px;align-items:center;padding:26px 32px">'
            '<svg width="84" height="76" viewBox="0 0 92 84" style="flex:0 0 84px"><path d="M46 6 L 88 78 L 4 78 Z" fill="#FFF3E0" stroke="#FFF3E0" stroke-width="6" stroke-linejoin="round"/>'
            '<rect x="42" y="30" width="8" height="26" rx="4" fill="#B3261E"/><circle cx="46" cy="66" r="5" fill="#B3261E"/></svg>'
            f'<div><div class="big" style="font-size:56px;text-shadow:none">{w.get("title", "Attention")}</div>'
            f'<div style="font:800 34px/1.3 Inter;margin-top:8px">{w.get("text", "")}</div></div></div></div>')


def photo_box(base, src, h, label=None, first=True, fit="cover"):
    lab = ""
    if label:
        bgc = "linear-gradient(90deg,#FFB13D,#FF5A36)" if first else "rgba(42,8,14,.85)"
        lab = f'<div style="position:absolute;left:22px;top:22px;background:{bgc};color:#fff;font:900 28px Inter;letter-spacing:3px;padding:10px 18px;border-radius:12px;text-transform:uppercase">{label}</div>'
    return (f'<div style="position:relative;height:{h}px;border-radius:30px;overflow:hidden;border:3px solid rgba(255,230,200,.55);box-shadow:0 0 50px rgba(255,90,54,.35)">'
            f'<img src="{img_uri(base, src)}" style="width:100%;height:100%;object-fit:{fit};display:block;background:rgba(20,4,8,.6)">{lab}</div>')


def body(s, base, n, total):
    t = s.get("type", "steps")
    out = f'<img class="bg" src="{BG}"><div class="shade"></div><div class="leak"></div><div class="vig"></div>'
    if t == "hook":
        out += hud_top(s)
        memo_html = ""
        if s.get("memo"):
            # Fiche mémo : toutes les infos utiles sur la miniature (étapes numérotées + alerte), sous le titre
            m = s["memo"]
            memo_html = '<div class="glass" style="margin-top:44px;padding:10px 34px 14px;text-align:left">'
            for k, p in enumerate(m.get("points", [])[:5]):
                sep = "border-top:2px solid rgba(255,230,200,.14);" if k else ""
                memo_html += (f'<div style="display:flex;gap:24px;align-items:center;padding:18px 0;{sep}">'
                              f'<div class="gbg" style="flex:0 0 60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;'
                              f'font:900 34px Inter;color:#fff;box-shadow:0 0 24px {GLOW}">{k + 1}</div>'
                              f'<div style="font:800 40px/1.25 Inter">{p}</div></div>')
            memo_html += "</div>" + warn_box(m.get("warn"))
        out += (f'<div class="content fitbox" style="top:{s.get("title_top", 300 if memo_html else 330)}px;text-align:center">'
                + (f'<div class="chip"><span class="dot"></span>{s["chip"]}</div>' if s.get("chip") else "")
                + f'<div class="big fit" style="font-size:{s.get("title_size", 168)}px;margin-top:30px">{s.get("title", "")}</div>'
                + memo_html + "</div>")
        if s.get("wheel"):
            out += f'<div class="abs" style="top:690px;left:160px">{wheel(s["wheel"])}</div>' + pill(s.get("pill"), 1430)
        elif s.get("image"):
            top, h = s.get("image_top", 740), s.get("image_height", 620)
            out += f'<div class="content" style="top:{top}px">{photo_box(base, s["image"], h, fit=s.get("image_fit", "cover"))}</div>'
            if s.get("badge"):
                # Pastille bien visible sur la miniature (ex. « Partie 2 » d'une série)
                out += (f'<div class="abs" style="top:{top - 46}px;right:84px;transform:rotate(-4deg);background:#FFF3E0;color:#2A0608;'
                        f'font:900 italic 74px/1 Barlow;text-transform:uppercase;padding:14px 30px 10px;border-radius:20px;'
                        f'box-shadow:0 10px 0 #3A0408,0 0 40px {GLOW}">{s["badge"]}</div>')
            out += pill(s.get("pill"), 1410) if top + h <= 1390 else ""
        elif s.get("memo"):
            pass
        elif s.get("bignum"):
            bn = s["bignum"]
            out += (f'<div class="content" style="top:800px;display:flex;align-items:center;justify-content:center;gap:34px">'
                    f'<div class="big" style="font-size:400px;line-height:.8"><span class="grad">{bn["num"]}</span></div>'
                    f'<div class="big" style="font-size:96px;text-align:left">{bn.get("text", "")}</div></div>' + pill(s.get("pill"), 1330))
        else:
            out += (f'<div class="abs" style="top:820px;left:390px;width:300px;height:300px;border-radius:50%;background:linear-gradient(135deg,{A},{B} 55%,{C});'
                    f'display:flex;align-items:center;justify-content:center;box-shadow:0 0 80px {GLOW};border:6px solid #FFF3E0">{icon(s.get("icon", "star"), 170)}</div>'
                    + pill(s.get("pill"), 1250))
    elif t == "steps":
        out += head(s)
        pts = s.get("points", [])
        out += '<div class="content fitbox" style="top:620px"><div style="position:relative">'
        if len(pts) > 1:
            out += '<div class="abs" style="left:44px;top:60px;bottom:60px;width:8px;background:repeating-linear-gradient(180deg,#FFF3E0 0 22px,transparent 22px 40px);opacity:.75"></div>'
        for k, p in enumerate(pts):
            last = k == len(pts) - 1 and len(pts) > 1
            border = f"border-color:{A};box-shadow:0 0 34px {GLOW}" if last else ""
            out += (f'<div style="display:flex;gap:30px;align-items:center;margin-bottom:26px">'
                    f'<div style="flex:0 0 96px;height:96px;border-radius:50%;background:linear-gradient(135deg,{A},{B} 55%,{C});border:5px solid #FFF3E0;display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px {GLOW};position:relative;z-index:2">{icon(p.get("icon", "pin"), 54)}</div>'
                    f'<div class="glass" style="flex:1;padding:24px 30px;font:800 40px/1.25 Inter;{border}">{p.get("text", "")}</div></div>')
        out += "</div>" + warn_box(s.get("warn")) + "</div>"
        out += pill(s.get("next"), 1430)
    elif t == "photo":
        out += head(s, size=150)
        out += f'<div class="content" style="top:520px">{photo_box(base, s["image"], 760)}'
        if s.get("caption"):
            out += f'<div class="glass" style="margin-top:26px;padding:24px 30px;font:800 38px/1.3 Inter">{s["caption"]}</div>'
        out += "</div>" + pill(s.get("next"), 1430)
    elif t == "versus":
        out += head(s, size=150)
        ph = s.get("photos", [])[:2]
        h = s.get("photo_height", 400)
        out += '<div class="content" style="top:500px">'
        for k, p in enumerate(ph):
            out += f'<div style="margin-top:{0 if k == 0 else 24}px">{photo_box(base, p["src"], h, p.get("label"), k == 0)}</div>'
        if s.get("caption"):
            out += f'<div class="glass" style="margin-top:24px;padding:22px 30px;font:800 36px/1.3 Inter">{s["caption"]}</div>'
        out += "</div>"
    elif t == "rows":
        out += head(s, size=150)
        out += '<div class="content glass fitbox" style="top:540px;padding:16px 36px">'
        for k, r in enumerate(s.get("rows", [])):
            sep = "border-top:2px solid rgba(255,230,200,.14);" if k else ""
            out += (f'<div style="display:flex;gap:24px;align-items:center;padding:22px 0;{sep}">'
                    f'<div class="gbg" style="flex:0 0 auto;min-width:120px;text-align:center;font:900 34px Inter;padding:12px 18px;border-radius:14px">{r.get("k", "")}</div>'
                    f'<div style="font:800 38px/1.25 Inter">{r.get("v", "")}</div></div>')
        out += "</div>" + pill(s.get("next"), 1430)
    elif t == "cta":
        out += (f'<div class="content" style="top:300px;text-align:center"><div class="chip"><span class="dot"></span>À GARDER</div>'
                f'<div class="big fit" style="font-size:{s.get("title_size", 150)}px;margin-top:34px">{s.get("title", "")}</div>'
                '<div style="margin-top:60px;text-align:left">'
                f'<div class="glass" style="display:flex;gap:24px;align-items:center;padding:30px 34px">{icon("phone", 64)}<div style="font:800 40px/1.3 Inter">{s.get("comment", "Dis-moi en commentaire ce que tu en penses.")}</div></div>'
                f'<div class="gbg" style="display:flex;gap:24px;align-items:center;padding:30px 34px;border-radius:30px;margin-top:26px;box-shadow:0 0 50px {GLOW}">'
                '<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22 11 13 2 9z"/></svg>'
                f'<div style="font:900 42px/1.25 Inter">{s.get("share", "Envoie-le à ton pote qui joue à GTA 6")}</div></div>'
                '<div style="display:flex;gap:24px;margin-top:26px"><div class="glass" style="flex:1;text-align:center;padding:26px;font:900 38px Inter">Enregistre</div>'
                '<div class="glass" style="flex:1;text-align:center;padding:26px;font:900 38px Inter">Abonne-toi</div></div></div></div>')
    elif t == "meme":
        out += f'<div class="content fitbox" style="top:250px;text-align:center"><span class="bub">{s.get("setup", "")}</span></div>'
        v = s.get("variant", "echec")
        if v == "echec":
            out += ('<div class="content" style="top:820px;text-align:center">'
                    '<div style="height:10px;background:linear-gradient(90deg,transparent,#FF5A36,transparent)"></div>'
                    '<div class="big fit" style="font-size:150px;margin:40px 0 30px;color:#FF5A36;-webkit-text-stroke:5px #3A0408;paint-order:stroke fill">Mission échouée</div>'
                    f'<div style="font:800 52px/1.3 Inter;text-shadow:0 3px 14px rgba(0,0,0,.6)">{s.get("reason", "")}</div>'
                    '<div style="height:10px;margin-top:40px;background:linear-gradient(90deg,transparent,#FF5A36,transparent)"></div></div>')
        elif v == "notifs":
            out += '<div class="content" style="top:720px">'
            for k, nt in enumerate(s.get("notifs", [])[:4]):
                out += ('<div style="display:flex;gap:22px;align-items:center;padding:24px 26px;border-radius:30px;background:rgba(255,246,238,.92);color:#2A0E08;margin-bottom:22px;box-shadow:0 14px 40px rgba(40,6,0,.35)">'
                        f'<div class="gbg" style="flex:0 0 76px;height:76px;border-radius:20px;display:flex;align-items:center;justify-content:center">{icon(nt.get("icon", "phone"), 46)}</div>'
                        f'<div style="flex:1"><div style="display:flex;justify-content:space-between;font:900 22px Inter;letter-spacing:2px;opacity:.6;text-transform:uppercase"><span>{nt.get("app", "")}</span><span>maintenant</span></div>'
                        f'<div style="font:800 36px/1.25 Inter;margin-top:6px">{nt.get("text", "")}</div></div></div>')
            out += "</div>"
        elif v == "stars":
            n = s.get("stars", 5)
            st = "".join(f'<svg width="150" height="150" viewBox="0 0 100 100" style="{"filter:drop-shadow(0 0 22px rgba(255,220,170,.9))" if i < n else "opacity:.4"}"><polygon points="{star_points(50, 54, 5, 48, 20)}" fill="{"#FFF3E0" if i < n else "none"}" stroke="#FFF3E0" stroke-width="6" stroke-linejoin="round"/></svg>' for i in range(5))
            out += (f'<div class="content" style="top:820px;text-align:center"><div class="lab" style="font-size:34px">{s.get("label", "Niveau de recherche")}</div>'
                    f'<div style="display:flex;justify-content:center;gap:16px;margin-top:30px">{st}</div>'
                    f'<div style="font:800 50px/1.3 Inter;margin-top:44px;text-shadow:0 3px 14px rgba(0,0,0,.6)">{s.get("reason", "")}</div></div>')
        elif v == "wheel" and s.get("wheel"):
            out += f'<div class="abs" style="top:700px;left:160px">{wheel(s["wheel"])}</div>'
        elif v == "objectif":
            # Écran d'objectifs de mission (format « Lucia va apprécier »)
            out += ('<div class="content" style="top:640px"><div class="chip"><span class="dot"></span>'
                    f'{s.get("label", "Nouvel objectif")}</div><div class="glass" style="margin-top:28px;padding:16px 38px 30px">')
            for k, o in enumerate(s.get("objectifs", [])[:4]):
                done = k < s.get("faits", 0)
                box = ('<div class="gbg" style="flex:0 0 54px;height:54px;border-radius:12px;display:flex;align-items:center;justify-content:center">'
                       '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg></div>'
                       if done else '<div style="flex:0 0 54px;height:54px;border-radius:12px;border:4px solid rgba(255,240,225,.75)"></div>')
                sep = "border-top:2px solid rgba(255,230,200,.14);" if k else ""
                deco = "text-decoration:line-through;text-decoration-thickness:4px;opacity:.85;" if done else ""
                out += (f'<div style="display:flex;gap:26px;align-items:center;padding:24px 0;{sep}">{box}'
                        f'<div style="font:800 42px/1.25 Inter;{deco}">{o}</div></div>')
            out += "</div>"
            if s.get("note"):
                out += (f'<div class="big fit" style="font-size:{s.get("note_size", 96)}px;margin-top:40px;text-align:center">'
                        f'<span class="gbg" style="display:inline-block;padding:8px 40px 14px;border-radius:28px;color:#fff;box-shadow:0 0 50px {GLOW}">{s["note"]}</span></div>')
            out += "</div>"
    # points de progression
    dots = "".join(f'<div style="flex:1;height:8px;border-radius:4px;{"background:linear-gradient(90deg,#FFB13D,#FF5A36)" if i < n else "background:rgba(255,240,225,.25)"}"></div>' for i in range(total))
    out += f'<div class="abs" style="top:1520px;left:70px;right:70px;display:flex;gap:10px">{dots}</div>'
    return out


FIT_JS = """() => {
  let shrunk = 0;
  document.querySelectorAll('.fit').forEach(el => {
    let fs = parseFloat(getComputedStyle(el).fontSize);
    const max = el.parentElement.clientWidth;
    while ((el.scrollWidth > max + 2) && fs > 60) { fs -= 4; el.style.fontSize = fs + 'px'; shrunk++; }
  });
  let bottom = 0, right = 0;
  document.querySelectorAll('.content, .abs').forEach(el => {
    if (el.classList.contains('bg') || el.classList.contains('shade') || el.classList.contains('leak') || el.classList.contains('vig')) return;
    const r = el.getBoundingClientRect();
    if (r.top < 1500 && r.bottom > bottom && r.height < 1500) bottom = r.bottom;
    if (r.right > right && r.width < 1080) right = r.right;
  });
  return {bottom: Math.round(bottom), right: Math.round(right), shrunk, limit: %d};
}""" % SAFE_BOTTOM


def nbsp(t):
    """Typographie française : pas de retour à la ligne dans « 205 000 $ » ni avant « ? ! : $ % »."""
    t = re.sub(r"(\d) (?=\d{3}\b)", "\\1&nbsp;", t)
    t = re.sub(r" (?=[?!:;$%€»])", "&nbsp;", t)
    return re.sub(r"(«) ", "\\1&nbsp;", t)


def grad_tags(v):
    if isinstance(v, str):
        return nbsp(v).replace("<g>", '<span class="grad">').replace("</g>", "</span>")
    if isinstance(v, list):
        return [grad_tags(x) for x in v]
    if isinstance(v, dict):
        return {k: grad_tags(x) for k, x in v.items()}
    return v


def page(s, n, total, base):
    html = body(grad_tags(s), base, n, total)
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>'


def render(spec_path):
    spec_path = pathlib.Path(spec_path).resolve()
    base = spec_path.parent
    slides = json.loads(spec_path.read_text())["slides"]
    total = len(slides)
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path("/tmp") / f"hud-{base.name}"
    tmp.mkdir(parents=True, exist_ok=True)
    for old in base.glob("slide-*.jpg"):
        old.unlink()
    problems = []
    with sync_playwright() as p:
        kw = {"args": ["--allow-file-access-from-files"]}
        if pathlib.Path("/usr/bin/google-chrome").exists():
            kw["executable_path"] = "/usr/bin/google-chrome"
        br = p.chromium.launch(**kw)
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for i, s in enumerate(slides, 1):
            f = tmp / f"s{i}.html"
            f.write_text(page(s, i, total, base))
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            r = pg.evaluate(FIT_JS); pg.wait_for_timeout(100)
            if r["bottom"] > r["limit"] or r["right"] > 1012:
                problems.append((i, r))
            png = tmp / f"s{i}.png"
            pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").save(base / f"slide-{i:02d}.jpg", quality=92)
            print(f"slide {i:02d}: bas={r['bottom']}px droite={r['right']}px réduit={r['shrunk']}")
        br.close()
    from PIL import Image
    ims = [Image.open(base / f"slide-{i:02d}.jpg").resize((360, 640)) for i in range(1, total + 1)]
    cols = min(total, 4)
    rows = (total + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 370 + 10, rows * 650 + 10), "#160806")
    for k, im in enumerate(ims):
        sheet.paste(im, (10 + (k % cols) * 370, 10 + (k // cols) * 650))
    sheet_path = pathlib.Path("/tmp") / f"{base.name}-planche.jpg"
    sheet.save(sheet_path, quality=88)
    print("planche :", sheet_path)
    for i, r in problems:
        print(f"ATTENTION slide {i:02d} : contenu trop bas ou trop à droite ({r}) - raccourcis le texte")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(render(sys.argv[1]))
