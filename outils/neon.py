#!/usr/bin/env python3
"""Rendu des carrousels TikTok GTA6France dans le style néon Vice City.

Usage :
    python3 outils/neon.py posts/2026-11-25-exemple/spec.json

Le fichier spec.json décrit les slides (voir outils/STYLE.md et posts/exemple-spec.json).
Sortie : posts/<dossier>/slide-01.jpg ... (1080x1920, JPEG), plus /tmp/<dossier>-planche.jpg
pour vérifier le rendu d'un coup d'œil.
"""
import json, pathlib, sys, html as H

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
PINK, TEAL, YEL, NIGHT = "#FF3D8B", "#2DE2C8", "#FFD23F", "#0E0524"
SAFE_BOTTOM = 1500  # le contenu doit rester au-dessus (interface TikTok en dessous)

def font_face(name, files):
    srcs = ",".join(f"url('{(FONTS / f).as_uri()}') format('woff2')" for f in files)
    return f"@font-face{{font-family:{name};src:{srcs}}}"

CSS = font_face("Anton", ["anton-latin-400-normal.woff2", "anton-latin-ext-400-normal.woff2"]) + \
      font_face("Pacifico", ["pacifico-latin-400-normal.woff2", "pacifico-latin-ext-400-normal.woff2"]) + f"""
*{{box-sizing:border-box}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#fff;background:{NIGHT}}}
.slide{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.sky{{position:absolute;inset:0 0 auto 0;height:1460px;background:linear-gradient(180deg,#0E0524 0%,#1E0A44 34%,#4A1468 56%,#9B2179 72%,#FF4F8B 86%,#FF9A3D 100%)}}
.stars{{position:absolute;inset:0;height:900px;background-image:radial-gradient(2px 2px at 120px 300px,#fff8,transparent),radial-gradient(2px 2px at 860px 220px,#fff9,transparent),radial-gradient(3px 3px at 640px 520px,#fff6,transparent),radial-gradient(2px 2px at 300px 700px,#fff5,transparent),radial-gradient(2px 2px at 960px 640px,#fff7,transparent),radial-gradient(2px 2px at 480px 160px,#fff8,transparent)}}
.sun{{position:absolute;left:50%;top:960px;width:760px;height:760px;margin-left:-380px;border-radius:50%;background:linear-gradient(180deg,#FFE45C 0%,#FFB13D 38%,#FF5E8E 72%,#FF3D8B 100%);-webkit-mask-image:linear-gradient(180deg,#000 0 26%,transparent 26% 29%,#000 29% 37%,transparent 37% 41%,#000 41% 48%,transparent 48% 53%,#000 53%);box-shadow:0 0 140px 40px rgba(255,90,140,.45)}}
.glow{{position:absolute;left:50%;top:900px;width:1100px;height:700px;margin-left:-550px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,120,120,.45),transparent)}}
.floor{{position:absolute;left:0;top:1460px;width:1080px;height:460px;background:#12052B;overflow:hidden;perspective:500px;perspective-origin:50% 0}}
.grid{{position:absolute;left:-1500px;top:-1140px;width:4080px;height:1600px;transform-origin:50% 100%;transform:rotateX(72deg);background-image:repeating-linear-gradient(90deg,rgba(255,61,139,.85) 0 4px,transparent 4px 120px),repeating-linear-gradient(0deg,rgba(45,226,200,.7) 0 4px,transparent 4px 120px)}}
.floorfade{{position:absolute;left:0;top:1460px;width:1080px;height:460px;background:linear-gradient(180deg,rgba(18,5,43,.55) 0%,rgba(18,5,43,0) 45%,rgba(18,5,43,.35) 100%)}}
.horizon{{position:absolute;left:0;top:1456px;width:1080px;height:8px;background:{PINK};box-shadow:0 0 30px 6px {PINK}}}
.palm{{position:absolute;fill:#13062C}}
.content{{position:relative;z-index:5;padding:120px 90px 0 90px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.sticker{{display:inline-block;background:{YEL};color:#14062E;font-family:Anton;font-size:46px;letter-spacing:3px;padding:14px 30px 12px;border-radius:14px;transform:rotate(-4deg);box-shadow:8px 8px 0 {PINK}}}
.logo{{font-family:Anton;font-size:56px;letter-spacing:2px;color:#fff;text-shadow:0 0 18px {PINK},0 0 40px {PINK}}}
.logo b{{color:{TEAL};font-weight:400}}
h2{{margin:6px 0 0;font-family:Anton;font-weight:400;font-size:120px;line-height:.98;text-transform:uppercase;text-shadow:6px 6px 0 {PINK};white-space:nowrap}}
h2.wrap{{white-space:normal}}
.y{{color:{YEL};text-shadow:6px 6px 0 #7A1F7A}}
.pac{{font-family:Pacifico;color:{PINK};transform:rotate(-4deg);transform-origin:left;text-shadow:0 0 12px {PINK},0 0 38px {PINK};margin-top:40px;font-size:60px}}
.place{{display:inline-flex;align-items:center;gap:12px;background:{YEL};color:#14062E;font-weight:800;font-size:36px;padding:12px 24px 12px 16px;border-radius:16px;box-shadow:6px 6px 0 {PINK}}}
.card{{margin-top:36px;background:rgba(14,5,36,.86);border:2px solid rgba(255,255,255,.16);border-radius:40px;padding:38px 42px;display:flex;flex-direction:column;gap:28px;box-shadow:0 30px 80px rgba(0,0,0,.45)}}
.steps{{display:flex;flex-direction:column;gap:26px}}
.st{{display:flex;gap:24px;align-items:flex-start;font-size:40px;line-height:1.32;font-weight:600;color:#fff}}
.st i{{flex:none;font-style:normal;width:62px;height:62px;border-radius:50%;background:{TEAL};color:#14062E;font-family:Anton;font-size:36px;display:flex;align-items:center;justify-content:center;margin-top:-2px}}
b,strong{{color:{TEAL};font-weight:800}}
.body{{margin:0;font-size:40px;line-height:1.36;color:#EDE6FF}}
.warn{{display:flex;gap:20px;align-items:flex-start;background:linear-gradient(90deg,rgba(70,10,60,.95),rgba(14,5,36,.95));border:2px solid rgba(255,61,139,.8);border-radius:24px;padding:22px 26px;font-size:33px;line-height:1.33;font-weight:600}}
.warn em{{flex:none;font-style:normal;font-family:Anton;font-size:30px;letter-spacing:2px;color:#14062E;background:{YEL};border-radius:10px;padding:6px 14px 4px}}
.warn b{{color:{YEL}}}
.row{{display:flex;align-items:center;gap:22px;padding:18px 24px;border-radius:24px;background:rgba(14,5,36,.88);border:2px solid rgba(255,255,255,.14)}}
.rn{{flex:none;width:70px;font-family:Anton;font-size:58px;color:{YEL};text-shadow:4px 4px 0 #7A1F7A;text-align:center}}
.rl{{flex:1;min-width:0}}
.rl div{{font-size:38px;font-weight:800;line-height:1.2}}
.rl small{{display:block;font-size:30px;color:#D9CFF7;font-weight:600;margin-top:6px;line-height:1.3}}
.reward{{flex:1;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;background:rgba(14,5,36,.88);border:2px solid rgba(255,210,63,.6);border-radius:28px;padding:26px 14px 24px;box-shadow:0 0 30px rgba(255,210,63,.2)}}
.reward div{{font-family:Anton;font-size:40px;line-height:1.05;text-transform:uppercase}}
.reward small{{font-size:26px;font-weight:600;color:#CFC4F2;line-height:1.25}}
.photo{{width:900px;border-radius:26px;overflow:hidden;border:3px solid rgba(255,255,255,.85);box-shadow:0 0 44px rgba(45,226,200,.32),0 20px 50px rgba(0,0,0,.5)}}
.photo img{{width:100%;height:100%;object-fit:cover;display:block}}
.pill{{display:flex;align-items:center;gap:18px;background:#fff;color:#14062E;font-family:Anton;font-size:46px;letter-spacing:1px;padding:18px 34px 16px;border-radius:999px;box-shadow:0 0 40px rgba(255,255,255,.35)}}
.bubble{{display:inline-block;background:#2A1650;border-radius:30px 30px 30px 8px;padding:22px 32px;font-family:Anton;font-size:60px;letter-spacing:2px;color:#fff}}
.k{{display:inline-flex;width:50px;height:50px;border-radius:12px;background:{TEAL};align-items:center;justify-content:center;margin:3px 3px;vertical-align:middle;box-shadow:0 4px 0 #128f80}}
.k svg{{width:62%;height:62%}}
.codes{{display:flex;flex-wrap:wrap;align-items:center;margin-top:10px}}
.big .k{{width:92px;height:92px;border-radius:18px;margin:6px}}
.teaser{{position:absolute;z-index:6;left:90px;right:90px;top:1440px;display:flex;justify-content:flex-end}}
.teaser span{{display:inline-flex;align-items:center;gap:12px;background:{PINK};color:#fff;font-family:Anton;font-size:40px;letter-spacing:1px;padding:12px 26px 10px;border-radius:999px;box-shadow:0 0 30px rgba(255,61,139,.6)}}
.dots{{position:absolute;z-index:6;left:90px;top:1545px;display:flex;gap:12px}}
.dot{{height:12px;border-radius:6px;background:rgba(255,255,255,.22)}}
.dot.on{{background:{YEL};box-shadow:0 0 14px {YEL}}}
"""

def palm(x, y, s, flip=False):
    sx = -s if flip else s
    fr = "".join(f'<path transform="rotate({a})" d="M0 0 C 40 -46 120 -60 190 -20 C 150 -36 90 -30 40 -6 C 70 -10 110 0 150 30 C 90 6 40 4 0 0Z"/>'
                 for a in (-170, -140, -105, -60, -25, 5, 35))
    return (f'<svg class="palm" aria-hidden="true" style="left:{x}px;top:{y}px" width="600" height="900" viewBox="-300 -200 600 900">'
            f'<g transform="scale({sx},{s})"><path d="M-6 680 C 0 480 30 250 0 0 L 16 2 C 48 250 26 480 22 680Z"/>'
            f'<g transform="translate(6,0)">{fr}</g></g></svg>')

SCENE = ('<div class="sky"></div><div class="stars"></div><div class="glow"></div><div class="sun"></div>'
         '<div class="floor"><div class="grid"></div></div><div class="floorfade"></div><div class="horizon"></div>'
         + palm(-170, 780, 1.15) + palm(700, 860, 0.95, flip=True) + palm(820, 1040, 0.6))

ICONS = {
 "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 9.5v5M18 9.5v5"/>',
 "shirt": '<path d="M8 3 3 6l2 4 3-1v12h8V9l3 1 2-4-5-3c-.6 1.5-2.2 2.5-4 2.5S8.6 4.5 8 3z"/>',
 "bike": '<circle cx="5.5" cy="16" r="3.5"/><circle cx="18.5" cy="16" r="3.5"/><path d="M5.5 16 9.5 9h5l4 7M9.5 9 8 6H6M14.5 9l1-3h2.5"/>',
 "car": '<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11"/><rect x="3" y="11" width="18" height="6" rx="2"/><circle cx="7.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>',
 "paint": '<rect x="3" y="4" width="13" height="5" rx="1.5"/><path d="M16 6.5h3v5h-8v3"/><rect x="9.5" y="14.5" width="3" height="6" rx="1"/>',
 "gift": '<rect x="3" y="8" width="18" height="5" rx="1"/><path d="M5 13v8h14v-8"/><path d="M12 8v13"/><path d="M12 8C10 4 6 4 7 7c.5 1 5 1 5 1zM12 8c2-4 6-4 5-1-.5 1-5 1-5 1z"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
 "heart": '<path d="M12 20s-7-4.4-9-9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c-2 4.6-9 9-9 9z"/>',
 "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3 20 3M16 7l3 3M14 9l2 2"/>',
 "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
 "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "trophy": '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"/>',
}
PIN = ('<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#14062E" stroke-width="2.4" '
       'stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>')
ARROW = ('<svg aria-hidden="true" width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="#14062E" stroke-width="2.8" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg>')

def svg(name, size=84, col=YEL):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{col}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, ICONS["star"])}</svg>')

LOGO = '<span class="logo">GTA <b>VI</b></span>'

def header(s):
    out = f'<div class="top"><span class="sticker">{s.get("sticker","")}</span>{LOGO}</div>'
    if s.get("pac"):
        out += f'<div class="pac">{s["pac"]}</div>'
    if s.get("title"):
        cls = "fit wrap" if s.get("title_wrap") else "fit"
        out += f'<h2 class="{cls}" style="font-size:{s.get("title_size",120)}px">{s["title"]}</h2>'
    if s.get("place"):
        out += f'<div style="margin-top:22px"><span class="place">{PIN}{s["place"]}</span></div>'
    return out

def steps_html(items, start=1):
    return '<div class="steps">' + "".join(f'<div class="st"><i>{i+start}</i><div>{t}</div></div>' for i, t in enumerate(items)) + '</div>'

def warn_html(w):
    return f'<div class="warn"><em>{w.get("label","ATTENTION")}</em><div>{w["text"]}</div></div>' if w else ""

def visual_html(v, base):
    if not v:
        return ""
    k = v.get("kind")
    if k == "ring":
        return f"""<div style="position:relative;width:560px;height:560px;margin:54px auto 0">
  <div style="position:absolute;inset:-40px;border-radius:50%;background:conic-gradient({PINK},#8A2BE2,{TEAL},#8A2BE2,{PINK});filter:blur(46px);opacity:.75"></div>
  <div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 40deg,{PINK},#B23CFF,{TEAL},#B23CFF,{PINK});padding:22px">
  <div style="width:100%;height:100%;border-radius:50%;background:radial-gradient(circle,#1A0638 0 40%,#3A0F70 62%,#7A2BD8 86%,#C04BFF 100%);box-shadow:inset 0 0 90px rgba(255,61,139,.7);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
  <div style="font-family:Pacifico;font-size:70px;color:{PINK};text-shadow:0 0 14px {PINK},0 0 40px {PINK}">{v.get("small","")}</div>
  <div style="font-family:Anton;font-size:{v.get("big_size",150)}px;line-height:.9;color:#fff;text-shadow:0 0 24px {TEAL},0 0 60px {TEAL}">{v.get("big","")}</div>
  </div></div></div>"""
    if k == "bignum":
        return f"""<div style="margin-top:30px;display:flex;align-items:flex-end;gap:24px">
  <span style="font-family:Anton;font-size:250px;line-height:.86;color:{YEL};text-shadow:10px 10px 0 {PINK},20px 20px 0 #7A1F7A">{v["num"]}</span>
  <span style="font-family:Anton;font-size:{v.get("text_size",104)}px;line-height:.95;text-transform:uppercase;text-shadow:7px 7px 0 {PINK}">{v.get("text","")}</span></div>"""
    if k == "image":
        src = (base / v["src"]).resolve().as_uri()
        return f'<div class="photo" style="margin-top:40px;height:{v.get("height",520)}px"><img src="{src}" alt=""></div>'
    if k == "icon":
        return f'<div style="margin:60px auto 0;width:320px;height:320px;border-radius:50%;background:rgba(14,5,36,.7);border:4px solid {TEAL};display:flex;align-items:center;justify-content:center;box-shadow:0 0 60px rgba(45,226,200,.5)">{svg(v.get("name","star"),200,"#fff")}</div>'
    return ""

SHARE_ICON = ('<svg aria-hidden="true" width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#14062E" stroke-width="2.4" '
              'stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></svg>')

def share_html(s):
    if not s.get("share"):
        return ""
    return (f'<div style="margin-top:30px;align-self:flex-start;display:flex;align-items:center;gap:18px;background:{YEL};color:#14062E;'
            f'font-weight:800;font-size:38px;line-height:1.25;border-radius:24px;padding:20px 30px;box-shadow:6px 6px 0 {PINK}">{SHARE_ICON}<span>{s["share"]}</span></div>')

def body(s, base):
    t = s.get("type", "steps")
    if t == "hook":
        out = f'<div class="top"><span class="sticker">{s.get("sticker","")}</span>{LOGO}</div>'
        if s.get("pac"):
            out += f'<div class="pac" style="margin-top:58px;font-size:72px">{s["pac"]}</div>'
        if s.get("title"):
            out += f'<h2 class="wrap" style="margin-top:10px;font-size:{s.get("title_size",150)}px;line-height:.95">{s["title"]}</h2>'
        out += visual_html(s.get("visual"), base)
        if s.get("pill"):
            out += f'<div style="margin-top:56px;display:flex;justify-content:center"><span class="pill">{s["pill"]}{ARROW}</span></div>'
        return out
    if t == "cta":
        return f"""<div class="top"><span class="sticker">{s.get("sticker","À GARDER")}</span>{LOGO}</div>
<div class="pac" style="margin-top:90px;font-size:78px">{s.get("pac","Ça t'a aidé ?")}</div>
<div style="margin-top:40px;font-family:Anton;font-size:150px;line-height:.95;text-transform:uppercase;text-shadow:8px 8px 0 {PINK}">Enregistre<br><span class="y" style="text-shadow:8px 8px 0 #7A1F7A">et partage</span></div>
<div style="margin-top:36px;align-self:flex-start;font-size:42px;line-height:1.35;font-weight:600;background:rgba(14,5,36,.82);border:2px solid rgba(255,255,255,.16);border-radius:28px;padding:24px 34px">{s.get("comment","Dis-moi en commentaire quel secret<br>tu veux voir ensuite.")}</div>
{share_html(s)}<div style="margin-top:44px;display:flex"><span style="display:flex;align-items:center;gap:22px;background:#FF3B5C;color:#fff;font-weight:800;font-size:54px;padding:22px 52px 22px 26px;border-radius:999px;box-shadow:0 16px 50px rgba(255,59,92,.55)"><span style="width:72px;height:72px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center"><svg aria-hidden="true" width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="#FF3B5C" stroke-width="3.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span>S'abonner</span></div>"""
    out = header(s)
    if s.get("intro"):
        out += f'<p class="body" style="margin:26px 0 0">{s["intro"]}</p>'
    if s.get("visual"):
        out += visual_html(s["visual"], base)
    if t == "steps":
        inner = steps_html(s.get("steps", []), s.get("start", 1)) + warn_html(s.get("warn"))
        out += f'<div class="card">{inner}</div>'
    elif t == "rows":
        out += '<div style="margin-top:30px;display:flex;flex-direction:column;gap:16px">' + "".join(
            f'<div class="row"><div class="rn">{r.get("n", i+1)}</div><div class="rl"><div>{r["title"]}</div>'
            + (f'<small>{r["text"]}</small>' if r.get("text") else "") + '</div></div>'
            for i, r in enumerate(s.get("rows", []))) + '</div>'
        if s.get("warn"):
            out += f'<div style="margin-top:22px">{warn_html(s["warn"])}</div>'
    elif t == "message":
        out += (f'<div style="margin-top:36px;background:#0B0420;border:3px solid rgba(255,255,255,.25);border-radius:40px;padding:26px 30px 34px;box-shadow:0 0 50px rgba(45,226,200,.3)">'
                f'<div style="font-size:38px;font-weight:800;padding-bottom:20px;border-bottom:2px solid rgba(255,255,255,.12)">{s.get("sender","Inconnu")}</div>'
                f'<div style="margin-top:26px"><span class="bubble">{s["message"]}</span></div></div>')
        if s.get("steps"):
            out += f'<div class="card">{steps_html(s["steps"])}</div>'
    elif t == "rewards":
        if s.get("steps"):
            out += f'<div class="card">{steps_html(s["steps"])}</div>'
        out += f'<div style="margin-top:46px"><span class="sticker" style="font-size:42px">{s.get("rewards_label","CE QUE TU GAGNES")}</span></div>'
        out += '<div style="margin-top:18px;display:flex;gap:20px">' + "".join(
            f'<div class="reward">{svg(r.get("icon","star"))}<div>{r["title"]}</div><small>{r.get("text","")}</small></div>'
            for r in s.get("rewards", [])) + '</div>'
    elif t == "photo":
        if s.get("text"):
            out += f'<div class="card" style="margin-top:24px"><p class="body" style="font-size:36px">{s["text"]}</p></div>'
    elif t == "custom":
        out += s.get("html", "")
    return out

ARROW_ROT = {"↑": 0, "→": 90, "↓": 180, "←": 270}
def keycaps(html):
    """Remplace les flèches ↑ → ↓ ← par des touches de croix directionnelle dessinées."""
    out = []
    for ch in html:
        if ch in ARROW_ROT:
            out.append(f'<span class="k" aria-label="{ch}"><svg viewBox="0 0 24 24" style="transform:rotate({ARROW_ROT[ch]}deg)">'
                       '<path d="M12 3 4 13h5v8h6v-8h5z" fill="#14062E"/></svg></span>')
        else:
            out.append(ch)
    return "".join(out)

def dots(n, total):
    w = (900 - 12 * (total - 1)) // total
    return '<div class="dots" aria-hidden="true">' + "".join(
        f'<div class="dot{" on" if i < n else ""}" style="width:{w}px"></div>' for i in range(total)) + '</div>'

TEASER_ARROW = ('<svg aria-hidden="true" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" '
                'stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg>')

def page(s, n, total, base):
    teaser = f'<div class="teaser"><span>{s["teaser"]}{TEASER_ARROW}</span></div>' if s.get("teaser") else ""
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Slide {n}</title><style>{CSS}</style></head>'
            f'<body><div class="slide">{SCENE}<div class="content">{keycaps(body(s, base))}</div>{teaser}{dots(n, total)}</div></body></html>')

FIT_JS = """() => {
  const out = {shrunk:0};
  document.querySelectorAll('h2.fit').forEach(h => { let f = parseFloat(getComputedStyle(h).fontSize);
    while ((h.scrollWidth > 900) && f > 60) { f -= 2; h.style.fontSize = f + 'px'; } });
  const bottom = () => { let m = 0; document.querySelectorAll('.content *').forEach(e => { const r = e.getBoundingClientRect(); if (r.bottom > m) m = r.bottom; }); return m; };
  const limit = document.querySelector('.teaser') ? 1420 : %d;
  let guard = 0;
  while (bottom() > limit && guard < 14) {
    document.querySelectorAll('.st,.body,.warn,.rl div,.rl small').forEach(e => { const f = parseFloat(getComputedStyle(e).fontSize); e.style.fontSize = Math.max(26, f - 2) + 'px'; });
    document.querySelectorAll('.card').forEach(e => { e.style.gap = '20px'; e.style.padding = '30px 36px'; });
    guard++; out.shrunk = guard; }
  out.bottom = Math.round(bottom()); out.limit = limit;
  let right = 0; document.querySelectorAll('.content *').forEach(e => { const r = e.getBoundingClientRect(); if (r.right > right) right = r.right; });
  out.right = Math.round(right);
  return out; }""" % SAFE_BOTTOM

def render(spec_path):
    spec_path = pathlib.Path(spec_path).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text())
    slides = spec["slides"]
    total = len(slides)
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path("/tmp") / f"neon-{base.name}"
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
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            r = pg.evaluate(FIT_JS); pg.wait_for_timeout(100)
            if r["bottom"] > r["limit"] or r["right"] > 1000:
                problems.append((i, r))
            png = tmp / f"s{i}.png"
            pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").save(base / f"slide-{i:02d}.jpg", "JPEG", quality=90, optimize=True)
            print(f"slide {i:02d}: bas={r['bottom']}px droite={r['right']}px réduit={r['shrunk']}")
        br.close()
    ims = [Image.open(base / f"slide-{i:02d}.jpg").resize((270, 480)) for i in range(1, total + 1)]
    cols = min(total, 6); rows = (total + cols - 1) // cols
    sheet = Image.new("RGB", (276 * cols, 486 * rows), "white")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * 276, (k // cols) * 486))
    sheet_path = pathlib.Path("/tmp") / f"{base.name}-planche.jpg"
    sheet.save(sheet_path, quality=85)
    print("planche :", sheet_path)
    if problems:
        print("ATTENTION, contenu trop bas ou trop large (raccourcis le texte) :", problems)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(render(sys.argv[1]))
