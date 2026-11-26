#!/usr/bin/env python3
"""Mèmes GTA 6 au format TikTok (texte blanc arrondi sur une capture du jeu).

Usage : python3 outils/meme.py posts/<dossier>/spec.json
Spec : {"slides": [{"image": "img/x.jpg", "text": "La situation…", "punch": "(Je suis foutu)",
                    "layout": "center" ou "full", "focus": "50% 50%"}]}
- layout "center" (par défaut, pour les captures en paysage) : capture en pleine largeur au centre,
  même image floutée en fond, légende au-dessus de la capture.
- layout "full" (captures en portrait) : capture plein écran, légende en haut.
- layout "contain" (mème déjà légendé, ex. repost d'un mème en français) : image entière centrée sur fond flouté,
  sans bulle si "text" est vide.
- punch : petite réplique en bas à droite de la capture (facultatif). text vide = pas de bulle.
Règles : pas d'emoji ni de @ dans nos textes, images de la banque de Romain uniquement (dossier banque/ ou img/ du post).
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
F = (HERE / "fonts").as_uri()
CSS = f"""
@font-face{{font-family:Inter;font-weight:800;src:url({F}/inter-latin-800-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:800;src:url({F}/inter-latin-ext-800-normal.woff2);unicode-range:U+0100-024F}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
.bg{{position:absolute;inset:-60px;width:1200px;height:2040px;object-fit:cover;filter:blur(34px) brightness(.55) saturate(1.2)}}
.shot{{position:absolute;left:0;width:1080px;object-fit:cover}}
.box{{display:inline;background:#fff;color:#111;font:800 54px/1.32 Inter;padding:6px 18px;border-radius:18px;
     -webkit-box-decoration-break:clone;box-decoration-break:clone}}
.cap{{position:absolute;left:50px;right:50px;text-align:center}}
.punch{{position:absolute;right:70px;background:#fff;color:#111;font:800 50px Inter;padding:10px 24px;border-radius:16px}}
"""


def page(s, base):
    img = (base / s["image"]).resolve().as_uri()
    focus = s.get("focus", "50% 50%")
    text, punch = s.get("text", ""), s.get("punch", "")
    cap = lambda style: (f'<div class="cap" id="cap" style="{style}"><span class="box">{text}</span></div>' if text else "")
    if s.get("layout") == "contain":
        # Mème déjà légendé (repost d'un mème en français) : image entière, centrée dans la zone sûre, sans bulle ajoutée
        body = (f'<img class="bg" src="{img}"><img src="{img}" style="position:absolute;left:0;top:200px;width:1080px;height:1300px;object-fit:contain">'
                + cap("top:120px") + (f'<div class="punch" style="top:1380px">{punch}</div>' if punch else ""))
    elif s.get("layout") == "full":
        body = (f'<img class="shot" src="{img}" style="top:0;height:1920px;object-position:{focus}">'
                + cap("top:300px")
                + (f'<div class="punch" style="top:1250px">{punch}</div>' if punch else ""))
    else:
        body = (f'<img class="bg" src="{img}"><img class="shot" id="shot" src="{img}" style="top:760px;height:680px;object-position:{focus}">'
                + cap("bottom:1200px")
                + (f'<div class="punch" style="top:1330px">{punch}</div>' if punch else ""))
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


def render(spec_path):
    spec_path = pathlib.Path(spec_path).resolve()
    base = spec_path.parent
    slides = json.loads(spec_path.read_text())["slides"]
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path("/tmp") / f"meme-{base.name}"
    tmp.mkdir(parents=True, exist_ok=True)
    for old in base.glob("slide-*.jpg"):
        old.unlink()
    with sync_playwright() as p:
        kw = {"args": ["--allow-file-access-from-files"]}
        if pathlib.Path("/usr/bin/google-chrome").exists():
            kw["executable_path"] = "/usr/bin/google-chrome"
        br = p.chromium.launch(**kw)
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for i, s in enumerate(slides, 1):
            f = tmp / f"s{i}.html"
            f.write_text(page(s, base))
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            top = pg.evaluate("() => { const c = document.getElementById('cap'); return c ? Math.round(c.getBoundingClientRect().top) : 0 }")
            pg.screenshot(path=str(tmp / f"s{i}.png"))
            Image.open(tmp / f"s{i}.png").convert("RGB").save(base / f"slide-{i:02d}.jpg", quality=92)
            print(f"slide {i:02d}: haut de la légende={top}px" + ("  ATTENTION : légende trop longue, raccourcis-la" if top and top < 230 else ""))
        br.close()
    ims = [Image.open(base / f"slide-{i:02d}.jpg").resize((360, 640)) for i in range(1, len(slides) + 1)]
    sheet = Image.new("RGB", (len(ims) * 370 + 10, 660), "#111")
    for k, im in enumerate(ims):
        sheet.paste(im, (10 + k * 370, 10))
    out = pathlib.Path("/tmp") / f"{base.name}-planche.jpg"
    sheet.save(out, quality=88)
    print("planche :", out)


if __name__ == "__main__":
    render(sys.argv[1])
