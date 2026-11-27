# Guide de style des carrousels GTA6France

Compte TikTok : grand_theft_auto_6vi (marque Metricool 8328564, fuseau Europe/Paris).
Créateur : Romain. Public : 76 % d'hommes, francophones, joueurs de GTA 6 (sorti le 19 novembre 2026).

## Règles fixes

- Tout en français. **Aucun emoji**, ni sur les slides ni dans les descriptions.
- **Aucune mention @** d'un autre créateur sur les slides. On peut citer un découvreur par son nom dans la description, sans @.
- Format 1080 × 1920, export JPEG (TikTok refuse le PNG pour les posts photo).
- Le contenu reste au-dessus de 1 500 px (l'interface TikTok couvre le bas). `hud.py` le vérifie, réduit les titres trop larges et signale ce qui dépasse.
- **Style « HUD · Roue des récompenses »** (choisi par Romain le 26/11) : on dirait l'écran du jeu. Fond de plage de Vice City au coucher du soleil, flouté (palmiers, poste de surveillance) ; par-dessus, des éléments d'interface de jeu : compteur d'argent et étoiles de recherche en haut à droite, cartes en verre fumé, roue de sélection, repères d'itinéraire, bandeau d'alerte rouge. Titres en Barlow Condensed italique majuscule, textes en Inter. Ne pas changer ce décor.
- Couleurs chaudes : ambre #FFB13D, orange #FF5A36, magenta #E8336D (dégradé pour les mots forts : `<g>mot</g>`).
- Jamais de personnage, logo ou pochette protégés dessinés ou copiés. Pas de photo de personne réelle.
- Chaque info de jeu doit être vérifiée dans au moins deux sources récentes. Si une info vient seulement de joueurs, l'écrire (« selon les joueurs »).

## Structure d'un carrousel (5 à 8 slides)

1. **Accroche** (`hook`) : un secret ou un gain chiffré, en haut le contexte (`label`, `sub`) et si utile le compteur (`hud`), un titre qui pose une question, puis UN visuel : la roue (`wheel`) quand le post oppose deux choix, un gros chiffre (`bignum`), une photo du jeu (`image`) ou une icône. Finir par une pastille (`pill`) qui donne envie de swiper.
2. **Étapes** (`steps`, `rows`, `photo`, `versus`) : « MISSION » + « ÉTAPE x/y », titre court (2-3 mots, un mot en `<g>`), 3 repères maximum avec icône, mots clés en `<b>`, alerte rouge (`warn`) si un piège existe, pastille `next` vers la suite.
3. **Dernière slide** (`cta`) : question qui divise en titre, commentaire, partage, « Enregistre » et « Abonne-toi ».

Format qui marche le mieux sur le compte (stats du 24/11) : **une astuce précise avec un gain chiffré** (la maison de Jason +5 000 $ : 8,6 % de j'aime, 301 enregistrements). Les listes générales (« 10 astuces ») marchent moins. Sujets porteurs : braquages, argent, secrets et easter eggs, voitures rares.

## Types de slides (spec.json)

Exemple complet : `outils/exemple-hud/spec.json`. La liste détaillée des champs est en tête de `outils/hud.py`.

- `hook` : label, sub, hud {plus, amount, stars}, chip, title, puis wheel {left, right, center, hint} | bignum {num, text} | image | icon, et pill.
- `steps` : tag, step, title, points [{icon, text}], warn {title, text}, next.
- `rows` : tag, step, title, rows [{k, v}] (ex. code et effet, rang et voiture), next.
- `photo` : tag, title, image, caption, next.
- `versus` : tag, title, photos [{src, label}, {src, label}], caption (comparaisons GTA / vraie vie, 2002 / 2026).
- `cta` : title, comment, share.
- Icônes : moon, heli, fox, cash, smg, star, pin, car, key, eye, trophy, flame, lock, map, phone.

Rendu : `python3 outils/hud.py posts/<dossier>/spec.json`, puis vérifier `/tmp/<dossier>-planche.jpg`. L'ancien style néon (`neon.py`) n'est plus utilisé pour les nouveaux posts.

## Publication (Metricool)

- Heures : **10 h, 12 h et 18 h** (heure de Paris).
- **Maximum 3 posts par jour au total**, séries comprises. Avant de créer les posts du jour, compter dans historique.md les posts déjà programmés ce jour-là (ex. une partie de série à 15 h) et ne créer que ce qui reste pour arriver à 3. Avec une série à 15 h : seulement 10 h et 18 h. Au-delà de 3 par jour, l'engagement par post baisse.
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

**Description courte (environ 300 à 500 caractères, hashtags non compris)**
- Le mot-clé principal est tout au début, dans les 50 premiers caractères, tel qu'on le tape dans la recherche : « Codes de triche GTA 6 : … », « Argent facile GTA 6 : … », « GTA 6 secret : … ».
- Ensuite, en 2 ou 3 phrases courtes : la promesse concrète, le nom propre clé du jeu (lieu, véhicule, mission ou personnage), et une variante du mot-clé (GTA VI, PS5, Xbox) si elle vient naturellement.
- Termine par une question simple pour les commentaires et un appel court : « Enregistre ce post et abonne-toi pour d'autres astuces GTA 6. »
- Pas de liste d'étapes dans la description : les étapes sont sur les slides.
- 10 à 12 hashtags à la fin : 3 larges (#gta6 #gtavi #gaming), 5 à 7 liés au sujet (#gta6argent, #gta6cheat, #gta6secret, #gta6braquage, #gta6voiture…), 2 francophones (#gta6fr #gamingfr).

**Slides**
- La slide 1 affiche le mot-clé exact en gros (« CODES DE TRICHE GTA 6 », « ARGENT FACILE »), car TikTok lit aussi le texte des images.
- Recherches qui amènent déjà des vues au compte (TikTok Studio, 24/11) : « braquage gta 6 », « phamas chap 2 gta », « bf bandito gta6 ». Les privilégier comme sujets et mots-clés.

## Méthode virale (à appliquer à chaque post)

Ce qui compte pour TikTok en 2026, dans l'ordre : temps passé et taux de complétion (pour un carrousel, le % qui swipe après la slide 1, puis le % qui va jusqu'au bout), puis **partages en message privé** et **enregistrements**, puis commentaires, puis j'aime. La vitesse des réactions dans la première heure décide si le post est poussé plus loin.

**Slide 1 = 80 % du résultat**
- Nommer le sujet tout de suite (mot-clé en gros) ET ouvrir une question sans y répondre.
- Un chiffre précis plutôt que rond (« 2 140 $ », « 61 codes », « 7 secondes »). **Jamais de chiffre inventé** : chaque chiffre vient des sources vérifiées.
- Formules qui marchent : « Personne n'y pense : … », « Rockstar a caché … », « Ne fais pas … avant d'avoir vu ça », « Le secret à +2 000 $ caché à Key Lento », « J'ai trouvé … à Key Lento », « Si tu as raté ça, recommence ta partie ».
- La pastille blanche annonce la récompense et sa slide (« LE CODE ARGENT EN SLIDE 4 »).

**Slides 2 et suivantes**
- La slide 2 relance (petit suspense ou première info choc), pas une intro molle.
- Au milieu, une relance avec le champ `next` (« Le meilleur arrive en slide 5 → »).
- Une idée par slide, 3 ou 4 lignes maximum, mots clés en `<b>`. 5 à 8 slides au total.

**Slide finale**
- `share` : une phrase qui pousse à envoyer le post à quelqu'un de précis (« Envoie-le à ton pote qui est encore à Key Lento »). C'est le signal le plus fort.
- `comment` : une question facile ou qui divise (« Jason ou Lucia ? », « Tu l'avais trouvé ? Réponds oui ou non »), car les posts photo reçoivent beaucoup de commentaires.

**Description**
- La première ligne est visible avant « plus » : elle doit accrocher ET contenir le mot-clé dans les 50 premiers caractères.

**Mélange des 3 posts du jour**
- 1 post « utile à garder » (argent, braquage, codes, emplacements) : vise les enregistrements.
- 1 post « découverte à partager » (secret, easter egg, détail fou du jeu, voiture rare) : vise les partages.
- 1 post « réaction » (mème, situation que tous les joueurs vivent, Jason et Lucia, classement ou « top 5 ») : vise les commentaires. Ça reste dans la même charte HUD.
- Séries numérotées quand un sujet marche (« Braquage n°2 », « Secret n°3 ») : ça fait visiter le profil.

**Inspiration**
- Les plus gros comptes GTA 6 postent des découvertes à la première personne (« J'ai volé la voiture de Paul Walker dans GTA 6 », « J'ai trouvé un ours polaire ») et des « pro tips » très courts. Reprendre ce ton dans les accroches, en français.
- Suivre ce qui buzze sur GTA 6 (presse jeu vidéo, YouTube, X, TikTok) et réagir dans les 24 à 48 h.

## Formats qui marchent (veille du 27/11 : les faire tourner)
Chaque format fait monter un chiffre différent. Mesures relevées sur TikTok après la sortie : les guides font 59 à 92 enregistrements pour 100 j'aime, les situations drôles 31 à 42 partages pour 100 j'aime.
1. Guide pas à pas (enregistrements) : c'est l'astuce de 10 h. Un objectif chiffré, les étapes, l'endroit exact. Slide finale et description : « Enregistre-le pour ta partie ».
2. Découverte inattendue (vues) : « GTA 6 te laisse faire ça ? ». Une découverte par slide, les plus folles d'abord (exemples relevés par la presse : l'aéroport où l'on peut entrer, repeindre les murs de sa maison au rouleau).
3. Liste « Ce que tu ne savais pas sur GTA 6 » (commentaires) : 5 à 8 détails cachés, un par slide. Slide finale : « Ajoute celui que j'ai oublié en commentaire ».
4. Personnage qui fait débat (commentaires) : en ce moment Mandy (la locataire de Brian, mission Pipework). On présente la théorie, les indices relevés par les joueurs et une question qui divise. On parle de l'histoire et de la théorie, jamais du physique du personnage, rien de sexuel.
5. Situation drôle (partages) : c'est le mème du jour.
6. Vice City contre le vrai Miami (commentaires) : « Devine lequel est le vrai ». Il faut des photos du vrai Miami envoyées par Romain dans banque/ ; sans elles, ne pas faire ce format.
7. Fiche mémo (à tester sur les guides) : toutes les infos utiles lisibles sur la slide 1 (titre, récompense en gros, 3 ou 4 étapes numérotées, une alerte), puis 1 ou 2 slides de détail ou de photos. Rendu : slide hook avec le champ `memo` de hud.py (points + warn). C'est la forme du post « Retourne chez Jason +5 000 $ », le meilleur du compte (14 060 vues, 62 % des gens vont à la slide 2, 6,2 % des vues par la recherche). Titre et récompense doivent rester lisibles sur la grille du profil ; les étapes peuvent être plus petites. Comparer au bilan avec les guides classiques.
- Rotation : 10 h = guide (ou une idée prioritaire de historique.md), 12 h = mème, 18 h = un des formats 2, 3, 4 ou 6, jamais le même deux jours de suite.
- Photos d'un carrousel : uniquement les captures de banque/ qui correspondent au sujet (les regarder avec Read pour les reconnaître). S'il n'y en a pas, faire une version sans photo (hook icon ou bignum, steps, rows) ou choisir un autre format, et demander à Romain dans le message du matin les captures précises qui manquent pour les prochains sujets.
- Fins du jeu : pas de gros spoiler sur la miniature ni dans le titre (Rockstar fait retirer les spoilers). Si le post parle de la fin, slide 1 « Spoilers » et rien de révélé avant la slide 2.
- Dates à ne pas rater : 10/12 (GTA 6 a 8 nominations aux Game Awards) et le lendemain matin pour les résultats.

## Miniature (slide 1)
- La slide 1 est la miniature (photoCoverIndex 0). Sur le profil, TikTok la recadre au centre en 3:4 : environ 240 px coupés en haut et en bas. Tout ce qui compte (titre, chiffre, partie, visage ou voiture) doit être entre 300 et 1600 px de haut. Le petit label tout en haut n'apparaît pas sur la grille.
- À la taille d'une case du profil (un tiers de la largeur du téléphone), il faut lire le titre en une seconde : 3 lignes maximum, mots courts, gros, contrasté. Les mots en dégradé ont un contour sombre pour rester lisibles.
- Une série montre son numéro en gros sur la miniature : champ `badge` du hook (« Partie 2 »). Deux miniatures voisines ne doivent pas se ressembler (image, couleur dominante ou titre différents).
- Vérification obligatoire avant publication : `python3 outils/grille.py posts/<dossier>` puis ouvrir /tmp/grille.jpg avec Read. Si le titre ne se lit pas, si la miniature se confond avec ses voisines ou si quelque chose d'important est coupé, corriger et relancer.

## Musique
- Publication manuelle (choix de Romain, 27/11) : les posts sont programmés dans Metricool avec `autoPublish: false` et `autoAddMusic: false`. À l'heure prévue, Romain reçoit une notification de l'appli Metricool : les images sont enregistrées dans sa galerie, le texte est copié, et il termine le post dans TikTok en choisissant lui-même la musique (toute la bibliothèque TikTok est disponible).
- Chaque matin, on propose pour chaque post un son tendance qui colle à GTA 6 et à l'ambiance du post.
  - Mème : le son drôle ou le son de trend du moment.
  - Astuce argent, braquage : rap ou trap qui monte.
  - Comparaison Vice City, nostalgie : son années 80 ou musique des trailers.
- Repères fin novembre 2026 : « Suzuki » de Fuerza Regida (BO de GTA 6, plus de 3,5 millions de vidéos TikTok), « Run Away With Me » de Carly Rae Jepsen (dans le jeu, écoutes en forte hausse depuis la sortie), « But I Think It's A Dream » de Captain & Tennille (bande-annonce longue, écoutes en forte hausse), « Love Is a Long Road » de Tom Petty (trailer 1), « Hot Together » des Pointer Sisters (trailer 2), « Go Easy » de Dua Lipa et « Crazy for You » de Lana Del Rey (BO du jeu).
- Comment choisir dans TikTok : prendre le son dans la bibliothèque TikTok (pas un son importé), vérifier sur la page du son qu'il est utilisé par beaucoup de vidéos récentes, et qu'il colle à l'ambiance de la slide 1 (drôle, tension, nostalgie).
- Vidéos de gameplay (quand Romain filmera sa Xbox) : couper la radio du jeu avant d'enregistrer. Les chansons sous licence des radios peuvent faire couper le son de la vidéo ; on ajoute la musique dans TikTok.

## Mèmes (post réaction)

- Format TikTok classique : une capture du jeu, une légende dans une bulle blanche arrondie au-dessus, une petite réplique entre parenthèses en bas à droite (« (je suis foutu) »). Rendu : `python3 outils/meme.py posts/<dossier>/spec.json` (exemple : `outils/exemple-meme/spec.json`).
- Un post mème = un seul mème (une seule image), demandé par Romain. On choisit la meilleure idée du jour plutôt que plusieurs moyennes.
- Choix du mème (demandé par Romain le 27/11, après un mème jugé pas assez drôle) : chaque matin, préparer 2 ou 3 mèmes différents (chacun dans son dossier posts/AAAA-MM-JJ-meme-<sujet>), mettre le plus drôle en brouillon dans Metricool, et envoyer les autres avec SendUserFile dans le message du matin, numérotés (« Mème 1 : … (en brouillon), Mème 2 : …, Mème 3 : … »). Romain répond « oui » pour garder le mème 1, ou « oui, mème 2 » pour l'échanger : on remplace alors l'image, le titre et la description du brouillon avant de le programmer. Seul le mème choisi est noté dans banque/utilisees.txt.
- Images : celles que Romain envoie, rangées dans `banque/` (ses captures ou des images qu'il a trouvées). Une image utilisée est ajoutée à `banque/utilisees.txt`.
- Mentions et crédits (règle de Romain) : les pseudos et mentions de l'interface (TikTok, X, Instagram : @pseudo, nom du compte, boutons) sont retirés en recadrant sur l'image. Romain crédite lui-même le créateur en description et en commentaire : on n'écrit pas de crédit dans la description, on lui donne le nom du créateur (visible sur la capture, dans `banque/credits.txt` ou après « __ » dans le nom du fichier) dans le message du matin. Une signature ou un filigrane que le créateur a dessiné sur son image reste en place (on ne l'efface pas) ; seules les marques de Romain (haveNV, TAS, et Game Hero, son compte Instagram selon Romain le 27/11) peuvent être retirées.
- Sans capture : mèmes 100 % maison avec le type `meme` de `hud.py` (variantes `echec` « MISSION ÉCHOUÉE », `notifs` notifications de téléphone, `stars` niveau de recherche, `wheel` roue de choix). Exemple : `outils/exemple-meme-hud/spec.json`. On ne dessine jamais Jason, Lucia ni un autre personnage du jeu.
- Légendes (règle de Romain) :
  - Image sans texte : on écrit la blague nous-mêmes, courte (2 à 3 lignes), sur des situations que tous les joueurs vivent (Jason et Lucia en couple, la police, les voitures, l'attente de 13 ans, les quêtes ratées).
  - Image avec un texte en anglais (mème trouvé par Romain) : on le traduit en français naturel, en adaptant l'expression pour que la blague marche en français (pas de mot à mot). On refait le mème à notre format avec `meme.py` : on recadre l'image pour retirer l'ancien texte, puis on met la traduction dans notre bulle. On crédite le créateur si son nom est visible ou connu. Si l'ancien texte ne peut pas être retiré proprement, on n'utilise pas l'image.
  - Image avec un texte déjà en français (règle de Romain) : on reposte le mème avec son texte, recadré sur le mème lui-même (sans l'interface de l'appli) et mis au format 1080 x 1920 avec `meme.py`, layout `contain` et sans bulle (`text` vide).
- Images à ne pas utiliser, même traduites : une vraie personne dans un contexte d'accusation, de crime ou de sexe ; les personnages de dessins animés des grandes marques (Disney, etc.), souvent retirés pour droits d'auteur ; tout ce qui se moque d'une communauté.
- Pas d'emoji, pas de @, rien de sexuel ni d'humiliant sur une vraie personne.

### Recette d'un mème qui fait rire
- Une seule idée, compréhensible en 2 secondes. Légende de 15 mots maximum.
- Le décalage : la vraie vie d'un côté, GTA 6 de l'autre (« Mon boss qui pense que je suis au lit avec 40 de fièvre » sur une image de Jason tranquille au barbecue).
- La chute arrive en dernier (réplique entre parenthèses ou note en bas) et retourne la situation.
- Un détail précis rend la blague crédible : « 40 de fièvre », « il est 4 h du matin », « GTA 6 est sorti il y a 8 jours ».
- Une situation que tous les joueurs vivent, pour qu'ils taguent un pote. Pas de blague qu'il faut expliquer.

### Thèmes qui marchent le mieux en ce moment (fin novembre 2026, à mettre à jour avec la veille)
- Arrêt maladie, boss et collègues depuis la sortie du 19 novembre (« tout le bureau malade le même jour »).
- La copine et la vie de couple : disparaître un mois, « juste une mission », elle qui te voit faire la vaisselle dans le jeu.
- « Lucia va apprécier » : les objectifs du début du jeu (réparer la maison, faire les courses, acheter des fleurs) détournés. On le fait avec la variante `objectif` de `hud.py` (ex. « Ma copine : « tu fais jamais rien à la maison » » + objectifs cochés + « Lucia va apprécier. »).
- Faire dans le jeu ce qu'on ne fait pas dans la vraie vie (courses, ménage, réparer la maison).
- Jason impassible, quoi qu'il arrive.
- Les galères de joueur : stockage plein le jour J, 5 étoiles pour un klaxon, la voiture tunée crashée en sortant du garage.
- Les clips absurdes du jeu (PNJ, portière ouverte sur un cycliste, accidents qui finissent en figure).
- À éviter : « We got X before GTA 6 » (mort depuis la sortie), le débat « woke » autour de Lucia, les vraies personnes et les polémiques.
