# AnaMu — bibliothèque web des cours

La bibliothèque AnaMu est reconstruite automatiquement depuis **386 entrées** du [registre](../docs/data/course-algorithmic-assessments.json), dont **378 cours ayant reçu une première évaluation** et **8 familles de choix**. Bilan au **12 novembre 2026 : 122 cours avec MIDI pédagogique original, 256 évaluations limitées sans MIDI, aucun cours non examiné**. Le dernier lot couvre les 100 cours encore en attente avec cinq nouveaux MIDI. Les fiches sans syllabus, notamment les leçons privées, restent explicitement partielles; les fichiers MIDI sont des exemples de savoir identifié, jamais les consignes d'une section.

## Publication sur GitHub Pages (source : Actions)

1. Ouvrir **Settings → Pages** du dépôt `leye0/AnaMu`.
2. Dans **Build and deployment**, choisir **Source : GitHub Actions** (et non « Deploy from a branch »).
3. Le workflow **AnaMu - publier la bibliothèque de cours** (`.github/workflows/pages.yml`) se déclenche automatiquement lors de modifications des fiches de cours, de leur registre, du site ou de son constructeur, sur `main`. On peut aussi le lancer depuis **Actions → workflow → Run workflow**.
4. Ouvrir l'URL affichée dans **Settings → Pages** ou dans l'environnement `github-pages` du workflow. **Ne pas supposer l'URL `username.github.io/repo/` si un domaine personnalisé est déjà configuré**.
5. La première publication peut être inaccessible pendant la propagation du domaine. Si la page affiche une ancienne version, actualiser le navigateur.

Le workflow dispose de `contents: read`, `pages: write`, `id-token: write`, utilise les actions officielles `configure-pages`, `upload-pages-artifact` et `deploy-pages`. Il **ne modifie pas** le workflow historique de documentation ni les tests.

## Structure minime

- `site/index.html` — interface responsive.
- `site/styles.css` — styles.
- `site/app.js` — recherche, navigation, lecture d'un Standard MIDI File avec Web Audio, visualisation piano-roll.
- `scripts/build_course_site.py` — constructeur **stdlib Python 3.12**, lit directement `docs/data/course-algorithmic-assessments.json` et les Markdown de `docs/courses/`. Produit les fiches HTML préformatées dans des JSON de détail et **copie les fichiers .mid réellement présents dans le dépôt** vers le site publié. Pas de double saisie des contenus universitaires.
- `.github/workflows/pages.yml` — publication.

Le dossier généré `_site/` n'est qu'un **résultat de compilation temporaire**, pas une nouvelle source de vérité à éditer.

## Aperçu local

Depuis la racine du dépôt :

```sh
python3 scripts/build_course_site.py --output _site
python3 -m http.server --directory _site 8000
```

Puis ouvrir `http://localhost:8000/`. Ne pas ouvrir le fichier HTML directement par `file://` : les requêtes JSON et MIDI utilisent `fetch`.

## Qualité et limites

- Le synthétiseur **Web Audio** joue notes, hauteurs, durées, programmes instrumentaux approximatifs et événements de batterie. Il n'utilise aucun enregistrement tiers ni bibliothèque audio externe. **C'est une interprétation synthétique d'un MIDI, non le son d'un orchestre réel**. Les programmes General MIDI ne garantissent pas une reproduction authentique de timbre.
- Le site montre aussi les cours **sans MIDI**, avec le bon état : à analyser, évalué sans MIDI pertinent, choix d'options. Une fiche « à analyser » ne doit pas être présentée comme couverte.
- Le constructeur refuse les chemins MIDI manquants et les collisions de chemins de fiches; il n'invente pas de sons ou de contenus universitaires. Les liens vers les sources sont conservés.
- Pour jouer sur iPhone, toucher **▶** : Safari exige une interaction explicite pour démarrer l'audio. Pour écouter, ne pas bloquer le son du navigateur.
- Les nouveaux MIDI doivent être des fichiers SMF compatibles (format 0/1, tempo PPQ), et leurs chemins doivent être inscrits dans le registre `docs/data/course-algorithmic-assessments.json`. La timebase SMPTE n'est pas encore prise en charge.
