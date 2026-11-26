#!/usr/bin/env python3
"""Aperçu de la grille du profil TikTok, pour vérifier les miniatures.

Usage : python3 outils/grille.py [dossier_du_nouveau_post ...]
- Prend la slide 1 (la miniature, photoCoverIndex 0) des posts donnés, puis complète avec les posts
  les plus récents de historique.md (du plus récent au plus ancien), 9 cases en tout.
- Chaque case est recadrée comme sur le profil TikTok : centre de l'image au format 3:4
  (environ 240 px coupés en haut et en bas d'une slide 1080 x 1920).
- Écrit /tmp/grille.jpg : l'ouvrir avec Read et vérifier que, à cette petite taille,
  le titre se lit, la partie d'une série se voit, et que la miniature se distingue des voisines.
"""
import pathlib, re, sys
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H, GAP, COLS = 360, 480, 6, 3


def recents():
    rows = []
    for line in (ROOT / "historique.md").read_text().splitlines():
        m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d{2}:\d{2})\s*\|\s*(posts/[^ |]+)", line)
        if m:
            rows.append((m.group(1) + " " + m.group(2), m.group(3)))
    rows.sort(reverse=True)
    return [p for _, p in rows]


def main(args):
    wanted = [a.rstrip("/") for a in args]
    for p in recents():
        if p not in wanted:
            wanted.append(p)
    tiles = []
    for p in wanted:
        f = ROOT / p / "slide-01.jpg"
        if f.exists():
            tiles.append(f)
        if len(tiles) == 9:
            break
    rows = (len(tiles) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * W + (COLS - 1) * GAP, rows * H + (rows - 1) * GAP), "white")
    for i, f in enumerate(tiles):
        im = Image.open(f).convert("RGB")
        w, h = im.size
        ch = int(w * 4 / 3)
        top = (h - ch) // 2
        tile = im.crop((0, top, w, top + ch)).resize((W, H))
        if i < len(args):
            ImageDraw.Draw(tile).rectangle([0, 0, W - 1, H - 1], outline="#00E0FF", width=6)
        sheet.paste(tile, ((i % COLS) * (W + GAP), (i // COLS) * (H + GAP)))
    sheet.save("/tmp/grille.jpg", quality=85)
    print("grille : /tmp/grille.jpg (" + str(len(tiles)) + " miniatures, nouveaux posts encadrés en bleu)")


if __name__ == "__main__":
    main(sys.argv[1:])
