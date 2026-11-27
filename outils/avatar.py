#!/usr/bin/env python3
"""Photo de profil TikTok du compte, dans le style HUD des carrousels (plage de Vice City, dégradé chaud).

Usage : python3 outils/avatar.py
Sortie : profil/photo-profil.jpg (1080x1080, à mettre comme photo de profil dans TikTok)
         /tmp/avatar-apercu.jpg (la photo en rond à la taille du profil, des commentaires et du fil, pour vérifier qu'elle se lit)

TikTok affiche la photo dans un rond : tout le texte reste au centre.
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hud  # noqa: E402  (polices, fond et couleurs des carrousels)

OUT = HERE.parent / "profil" / "photo-profil.jpg"
TITLE, TAG = "GTA 6", "ASTUCES FR"

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{hud.CSS}
html,body{{width:1080px;height:1080px}}
.av-bg{{position:absolute;inset:-40px;width:1160px;height:1160px;object-fit:cover;filter:blur(4px) saturate(1.3)}}
.av-dark{{position:absolute;inset:0;background:radial-gradient(48% 40% at 50% 50%,rgba(26,4,12,.55),transparent 75%)}}
</style></head><body>
<img class="av-bg" src="{hud.BG}"><div class="shade"></div><div class="leak"></div><div class="av-dark"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div class="big grad" style="font-size:330px;line-height:.86;padding-top:20px">{TITLE}</div>
  <div class="gbg" style="margin-top:34px;padding:16px 46px;border-radius:999px;font:900 74px Inter;letter-spacing:6px;box-shadow:0 0 50px {hud.GLOW}">{TAG}</div>
</div></body></html>"""


def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw
    OUT.parent.mkdir(parents=True, exist_ok=True)
    f = pathlib.Path("/tmp/avatar.html")
    f.write_text(HTML)
    png = pathlib.Path("/tmp/avatar.png")
    with sync_playwright() as p:
        kw = {"args": ["--allow-file-access-from-files"]}
        if pathlib.Path("/usr/bin/google-chrome").exists():
            kw["executable_path"] = "/usr/bin/google-chrome"
        br = p.chromium.launch(**kw)
        pg = br.new_page(viewport={"width": 1080, "height": 1080})
        pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        pg.screenshot(path=str(png))
        br.close()
    im = Image.open(png).convert("RGB")
    im.save(OUT, quality=92)
    # Aperçu : la photo en rond à 3 tailles (profil 200 px, fil 110 px, commentaires 56 px)
    sheet = Image.new("RGB", (460, 230), "#F4F1EA")
    x = 10
    for size in (200, 110, 56):
        small = im.resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        sheet.paste(small, (x, 15), mask)
        x += size + 30
    sheet.save("/tmp/avatar-apercu.jpg", quality=92)
    print("photo :", OUT)
    print("aperçu :", "/tmp/avatar-apercu.jpg")


if __name__ == "__main__":
    main()
