# AnaMu — bibliothèque web des cours

La bibliothèque AnaMu est reconstruite automatiquement depuis **386 entrées** du [registre](../docs/data/course-algorithmic-assessments.json), dont **378 cours ayant reçu une première évaluation** et **8 familles de choix**. Bilan au **12 novembre 2026 : 122 cours avec MIDI pédagogique original, 256 évaluations limitées sans MIDI, aucun cours non examiné**. Le dernier lot couvre les 100 cours encore en attente avec cinq nouveaux MIDI. Les fiches sans syllabus, notamment les leçons privées, restent explicitement partielles; les fichiers MIDI sont des exemples de savoir identifié, jamais les consignes d'une section.

Les fiches Berklee Online qui disposent d'un `exemple.mid` sont affichées séparément comme **exemples hors registre**. Elles ne modifient ni le nombre d'évaluations ni les catégories de couverture. [Écouter la doublure flûte–clarinette et le violoncelle](https://www.streamlev.com/AnaMu/?cours=berklee-online%3AOCWPR-366).

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
- `site/app.js` — recherche, navigation, commandes du lecteur et visualisation piano-roll.
- `site/gm-player.js` — lecture du MIDI original via SpessaSynth et une banque General MIDI, initialisée au premier appui sur ▶.
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

- Le lecteur utilise **SpessaSynth 4.4.8** (Apache-2.0) avec la banque **GeneralUser GS de S. Christian Collins**, une banque compatible General MIDI qui associe les programmes à des instruments échantillonnés distincts, ainsi que le canal 10 aux percussions. Le séquenceur reçoit les octets MIDI d'origine, pas les notes simplifiées du piano-roll. [SpessaSynth](https://github.com/spessasus/spessasynth_lib) · [GeneralUser GS et licence](https://github.com/mrbumpy409/GeneralUser-GS).
- Le catalogue n'a pas besoin de charger la banque pour s'afficher. Le premier appui sur ▶ charge via jsDelivr le lecteur et la banque compressée d'environ **8,4 Mo**, qui est ensuite réutilisée entre les fiches dans le même onglet. Si le chargement échoue, on peut réessayer ou télécharger le MIDI. Les instruments restent ceux d'une banque GM, pas des enregistrements d'un orchestre ni une reproduction universelle du son de Windows.
- Le site montre aussi les cours **sans MIDI**, avec le bon état : à analyser, évalué sans MIDI pertinent, choix d'options. Une fiche « à analyser » ne doit pas être présentée comme couverte.
- Le constructeur refuse les chemins MIDI manquants et les collisions de chemins de fiches; il n'invente pas de sons ou de contenus universitaires. Les liens vers les sources sont conservés.
- Pour jouer sur iPhone, toucher **▶** : Safari exige une interaction explicite pour démarrer l'audio. Pour écouter, ne pas bloquer le son du navigateur.
- Les nouveaux MIDI doivent être des fichiers SMF compatibles (format 0/1, tempo PPQ). Pour les cours du registre, inscrire leur chemin dans `docs/data/course-algorithmic-assessments.json`. Pour les fiches Berklee Online hors registre, placer `exemple.mid` dans le dossier portant le code du cours. La visualisation ne prend pas en charge les timecodes SMPTE.
