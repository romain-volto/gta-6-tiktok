# Guide de style des carrousels GTA6France

Compte TikTok : grand_theft_auto_6vi (marque Metricool 8328564, fuseau Europe/Paris).
Créateur : Romain. Public : 76 % d'hommes, francophones, joueurs de GTA 6 (sorti le 19 novembre 2026).

## Règles fixes

- Tout en français. **Aucun emoji**, ni sur les slides ni dans les descriptions.
- **Aucune mention @** d'un autre créateur sur les slides. On peut citer un découvreur par son nom dans la description, sans @.
- Format 1080 × 1920, export JPEG (TikTok refuse le PNG pour les posts photo).
- Le contenu reste au-dessus de 1 500 px (l'interface TikTok couvre le bas). `neon.py` le vérifie et réduit le texte si besoin.
- Style néon Vice City : ciel violet-rose, soleil rayé, palmiers, sol en grille, polices Anton (titres) et Pacifico (sous-titres roses). Ne pas changer ce décor.
- Couleurs : rose #FF3D8B, turquoise #2DE2C8, jaune #FFD23F.
- Jamais de personnage, logo ou pochette protégés dessinés ou copiés. Pas de photo de personne réelle.
- Chaque info de jeu doit être vérifiée dans au moins deux sources récentes. Si une info vient seulement de joueurs, l'écrire (« selon les joueurs »).

## Structure d'un carrousel (5 à 8 slides)

1. **Accroche** (`hook`) : un secret ou un gain chiffré (« +2 000 $ », « 14 voitures »), un sous-titre Pacifico, un visuel (`ring`, `bignum`, `icon`) et une pastille blanche qui donne envie de swiper.
2. **Étapes** (`steps`, `rows`, `message`, `rewards`, `photo`, `custom`) : sticker « ÉTAPE x/y », titre court (2-3 mots), un lieu si utile, 3 ou 4 étapes de 1 à 2 lignes avec les mots clés en `<b>`.
3. **Dernière slide** (`cta`) : « Enregistre et partage », une question simple pour les commentaires, bouton S'abonner.

Format qui marche le mieux sur le compte (stats du 24/11) : **une astuce précise avec un gain chiffré** (la maison de Jason +5 000 $ : 8,6 % de j'aime, 301 enregistrements). Les listes générales (« 10 astuces ») marchent moins. Sujets porteurs : braquages, argent, secrets et easter eggs, voitures rares.

## Types de slides (spec.json)

Voir `posts/2026-11-24-perroquet-cash/spec.json` pour un exemple complet.

- `hook` : sticker, pac, title (HTML, `<span class='y'>` pour le jaune), visual {kind: ring|bignum|icon|image}, pill.
- `steps` : sticker, pac, title, place, intro, steps [..], warn {label, text}.
- `rows` : liste numérotée, rows [{n, title, text}], warn.
- `message` : sender, message (bulle SMS), steps.
- `rewards` : steps, rewards [{icon, title, text}] (icônes : cash, shirt, bike, car, paint, gift, star, heart, bolt, eye, key, map, phone, clock, trophy).
- `photo` : visual {kind: image, src, height}, text.
- `custom` : html libre sous l'en-tête.
- `cta` : pac, comment.

Rendu : `python3 outils/neon.py posts/<dossier>/spec.json`, puis vérifier `/tmp/<dossier>-planche.jpg`.

## Publication (Metricool)

- Heures : **10 h, 12 h et 18 h** (heure de Paris).
- Images : liens publics `https://raw.githubusercontent.com/romain-volto/gta-6-tiktok/medias/posts/<dossier>/slide-XX.jpg`.
- Titre et description : suivre **obligatoirement** la section « Référencement » ci-dessous.
- `autoAddMusic` : true. Confidentialité : publique.
- **Toujours créer les posts en brouillon (`draft: true`)**. Romain valide chaque post (dans Metricool ou en répondant « oui »). Ne jamais publier sans son accord.

## Référencement (titres, descriptions, slides)

Romain veut que **chaque** titre et **chaque** description soient optimisés pour la recherche TikTok et la visibilité.

**Titre (90 caractères max)**
- Commence toujours par « GTA 6 », suivi du mot-clé que les gens tapent : « codes de triche », « argent facile », « secret », « braquage », « voiture rare », « easter egg », « astuce », « emplacement ».
- Ajoute la promesse concrète : un gain chiffré, un nom de lieu ou d'objet du jeu (« 250 000 $ », « Key Lento », « chemise de Tommy Vercetti »).
- Exemples : « GTA 6 codes de triche : code argent 250 000 $ et cheats PS5 Xbox », « GTA 6 argent facile : le perroquet qui cache 2 000 $ à Key Lento ».

**Description (1 200 à 2 000 caractères)**
- La première phrase reprend la recherche telle qu'on la tape : « Codes de triche GTA 6 (cheat codes PS5 et Xbox) : … », « Argent facile GTA 6 : … », « GTA 6 secret : … ».
- Le mot-clé principal revient 2 ou 3 fois naturellement, avec des variantes (GTA 6, GTA VI, PS5, Xbox) et des tournures de question : « Comment débloquer … dans GTA 6 : », « Où trouver … dans GTA 6 : ».
- Cite les noms propres du jeu (lieux, véhicules, missions, personnages) : ce sont des recherches à part entière.
- Puis les étapes claires, une question simple pour les commentaires, « Enregistre ce post » et « Abonne-toi pour d'autres astuces GTA 6 ».
- 10 à 12 hashtags à la fin : 3 larges (#gta6 #gtavi #gaming), 5 à 7 liés au sujet (#gta6argent, #gta6cheat, #gta6secret, #gta6braquage, #gta6voiture…), 2 francophones (#gta6fr #gamingfr).

**Slides**
- La slide 1 affiche le mot-clé exact en gros (« CODES DE TRICHE GTA 6 », « ARGENT FACILE »), car TikTok lit aussi le texte des images.
- Recherches qui amènent déjà des vues au compte (TikTok Studio, 24/11) : « braquage gta 6 », « phamas chap 2 gta », « bf bandito gta6 ». Les privilégier comme sujets et mots-clés.
