# AnaMu — Analyse Musicale

AnaMu est un projet de recherche visant à comprendre **comment les
enchaînements de notes, d'accords, de rythmes et de motifs produisent des
attentes, des surprises, des tensions et des résolutions**, puis à étudier
leur relation avec les émotions **réellement annotées par des humains**.

**Direction scientifique (v1.0, 7 novembre 2026) :** développer d'abord les
algorithmes issus des théories musicales et psychologiques sur le **MIDI
symbolique brut**. Déterminer ensuite le corpus nécessaire à la validation
de chaque mécanisme. Les rapprochements MIDI↔audio et **Demucs sont reportés**.

**8 novembre — nouveaux corpus réellement annotés :**
[étude IsoVAT + CP-WTC + PercePiano sur les cas difficiles](reports/midi-human-emotion-hard-benchmarks-2026-11-08.md).
**[Suite : partition contre interprétation, 1 072 + 288 MIDI](reports/score-aligned-expression-transfer-2026-11-08.md)** :
14 descripteurs d'expression alignés sur les notes écrites, évaluation hors
œuvre parente, témoin mélangé, sélection imbriquée et transfert sur 48 œuvres.
Un gain brut de +4,55 points sur l'axe *Dramatique* s'écroule en grande partie
quand le choix de modèle se fait sans consulter l'œuvre test ; aucun grand
gain robuste, **aucune intégration de cette branche au modèle principal**.
Les tests comparent explicitement les ordres humains de tension et les différences
**sombre / imaginatif / dramatique** entre interprétations MIDI d'une même partition.
Les algorithmes sont testables, mais **aucun gain sur PIAST Dark/Epic/Tense/Mysterious/Happy
n'est encore confirmé** : les taxonomies et les corpus sont distincts.
**Audit indépendant de l'œuvre :** le 68,1 % « sombre » de PercePiano
retombe à **59,5 %** lorsque chaque composition parente est entièrement
absente de l'entraînement ; deux familles supplémentaires de caractéristiques
rythmiques/expressives, avec témoins mélangés, **n'ont pas produit de gain
fiable**. Voir §4.1–4.2 du rapport, avant de citer les résultats initiaux.

- **[Feuille de route v1.1](docs/roadmap.md)** — priorités, jalons et état réel.
- **[Théorie → algorithmes](docs/theory-to-algorithms.md)** — références
  académiques, entrées/sorties, modèles, expériences et critères de preuve.
- **[PIAST-AT : premier vrai test d'humeurs humaines sur MIDI](reports/piast-at-pilot.md)** —
  extraits de piano annotés par des experts sur **16 humeurs/traits**
  distincts des genres/styles, consensus humain exigé (≥2/3),
  apprentissage et test séparés par source et comparaison à la fréquence
  des classes. [Comparaison avec Partitura/music21 sur les mêmes extraits](reports/piast-at-academic-240.md) :
  le surcroît de complexité n'a **pas** encore amélioré le petit test.
  **C'est de l'émotion perçue, pas une émotion ressentie prouvée.**
- **[PIAST-AT : hypothèses issues des recherches et résultats sur 850 MIDI](docs/piast-research-experiments.md)** —
  étude expérimentale de Micallef Grimaud & Eerola, modes/tempo/articulation
  calculés directement dans le MIDI, et ablations chiffrées :
  **AP des 15 humeurs 0,528 → 0,548** sur 91 extraits nouvellement réservés ;
  les interactions supplémentaires redescendent à **0,539**. L'amélioration
  est modeste et ne prouve pas la cause psychologique d'une émotion.
- **[Moteur émotionnel et couverture des algorithmes](docs/emotion-engine.md)** —
  23 mécanismes distincts étudiés, logiciels de recherche disponibles,
  intégration, expérience EMOPIA sans fuite et critères de validité.
- **[Comparaison réelle sur dix thèmes connus de piano VGMIDI](reports/vgmidi-temporal-ten.md)** —
  humains (environ 30 évaluations *à chaque mesure*) vs **estimations
  émotionnelles d'AnaMu sur les morceaux existants**, courbes SVG et
  [résultats détaillés](reports/vgmidi-temporal-ten.json). Il ne s'agit pas de
  prévoir les notes ou émotions futures ; les dix titres étaient simplement
  exclus de l'apprentissage du modèle.
- **[Fusion académique — reprise sur ces mêmes dix pièces](reports/vgmidi-temporal-ten-full.md)** —
  Partitura, music21, **melody-features**, **jSymbolic original**, familles
  théoriques distinctes, mémoire et attentes symboliques ; audit de couverture
  et ablations. Cette reprise est **exploratoire** : les titres avaient déjà
  été examinés dans le premier pilote.
- **[Vérification sur dix autres morceaux connus](reports/vgmidi-temporal-ten-confirmatory.md)** —
  pièces choisies par identités MIDI **avant examen de leurs annotations**,
  sans recoupement avec les dix précédentes, mêmes courbes humaines et AnaMu.
  Ce second ensemble est un test interne VGMIDI, **pas** une validation externe.
- **[Audits historiques](docs/audit-p0.md)** ·
  [jointure exacte](docs/p1-exact-join.md) ·
  [audit instrumental XMIDI](docs/p1-instrument-audit.md) ·
  [protocole audio reporté](docs/p1-drum-audio-validation-plan.md).

## Objectifs

1. Analyser la composition de pièces connues (Bach, Chopin, puis pop)
   par des mécanismes musicaux explicables.
2. Étudier **les transformations musicales dans le temps**, et non seulement
   des associations simplistes « mineur / lent / triste ».
3. À terme, générer des compositions symboliques originales à partir de
   contraintes d'émotions, d'instrumentation, de forme et de traits stylistiques.

## Premier noyau expérimental

La base `anamu/` comporte :

- `midi_views.py` : lit directement des octets MIDI et extrait **uniquement
  les parties monophoniques non ambiguës comme candidates**, sans les déclarer
  automatiquement « mélodie principale ».
- `expectation.py` : baseline probabiliste à ordre variable calculant la
  probabilité conditionnelle d'un événement symbolique, sa surprise et
  l'entropie *avant* cet événement. **Ce n'est pas une implémentation d'IDyOM
  ni un détecteur d'émotions déjà validé.**
- `tests/test_symbolic_expectation.py` : fixtures contrôlées, invariants et
  rejets des parties MIDI ambiguës.
- `theory_features.py` : adaptateurs pour les **vrais outils** Partitura
  (tension tonale Herremans/Chew), music21 (tonalité Krumhansl-Schmuckler,
  sonorités et degrés romains hypothétiques), lecture d'export IDyOM **original**.
- `tempo_map.py` : conversion MIDI beats → secondes de performance, avec
  prise en compte des changements de tempo **dans les deux sens**, y compris
  pour aligner les sorties d'outils en secondes sur les mesures MIDI.
- `academic_fusion.py` : fusion **par mesure** des moteurs originaux et des
  familles théoriques complémentaires. Sépare la provenance (logiciel publié
  réellement exécuté, approximation explicitée, simple cadre psychologique),
  les valeurs absentes et les observations globales des séries temporelles.
- `academic_expectations.py` : deux modèles symboliques distincts entraînés
  sur les **MIDI du lot d'entraînement uniquement** : attentes de mouvements
  mélodiques candidats et attentes de sonorités harmoniques. Entropie préalable,
  surprise réalisée et interaction des deux ; **ce ne sont ni IDyOM original
  ni une prévision d'émotions futures**.
- `academic_idyom.py` : intégration facultative de fichiers `.dat` obtenus
  en faisant tourner **IDyOM original**, avec vérification du manifeste, des
  SHA-256 des MIDI et résultats, et exclusion de tout MIDI test/validation
  de l'ensemble de formation IDyOM déclaré. Si le Lisp ne tourne pas,
  ses caractéristiques restent manquantes.
- `emotion_pipeline.py` : **même extraction académique pour le banc VGMIDI
  et pour tout nouveau MIDI connu**. Exporte au format JSON sûr les poids
  de calibration Ridge, l'imputation, les échelles et les n-grammes de
  l'entraînement (sans charger de `pickle`). Analyse valence/activation
  par mesure, avec couverture et signalement des moteurs indisponibles.
- `scripts/analyze_known_midi.py` : applique le modèle sauvegardé à un ou
  plusieurs MIDI, avec jSymbolic Java original en option.
- `scripts/analyze_known_scores.py` : exemple reproductible de la chaîne
  sur **Bach BWV 66.6** et **Chopin, Mazurka op. 6 no 2**, deux œuvres connues
  distribuées avec `music21` ; résultats inférés, **sans annotations humaines
  locales** permettant de les valider.
- **[Bach et Chopin : trajectoires émotionnelles exécutées](reports/bach-chopin-emotions.md)**
  — courbes et scores mesure par mesure, avec provenance et couverture des moteurs.
- **[Cinq compositions classiques : analyses et couverture par moteur](reports/known-classics-emotions.md)**
  — les trajectoires de deux pièces de Bach, Chopin, Mozart et Beethoven,
  générées par une run Java réelle sur les MIDI issus des partitions écrites.
  Les [18 mécanismes temporels confrontés aux mêmes estimations](reports/known-classics-mechanisms.json)
  sont disponibles séparément, sans faire passer une association pour une cause.
- **[Expérience rapide sur la mémoire de valence (20 morceaux humains)](reports/vgmidi-valence-memory-experiment.md)**
  — même MIDI, mêmes estimations existantes, simple persistance de la valence
  d'une mesure à la suivante. Les erreurs moyennes baissent légèrement, **mais
  l'effet n'est pas robuste sur seulement dix pièces par groupe**. Technique
  disponible uniquement sur demande avec `analyze_known_midi
  --valence-memory-alpha 0.2`, pas imposée par défaut.
- `models/vgmidi-piano-ridge.json.gz` : modèle de recherche numérique calibré
  sur VGMIDI, enregistré au format JSON gzip et **directement réutilisable** ;
  `analyze_known_midi` et `analyze_known_scores` le prennent par défaut.
  Les paramètres apprennent une association dans VGMIDI, pas une loi universelle
  des émotions ; aucune pièce du test n'est incluse dans sa calibration.
- `melody_toolbox.py` : **bibliothèque universitaire réelle**
  [`melody-features` 1.3.3](https://dmwhyatt.github.io/melody-features/),
  qui rassemble des centaines de descripteurs de mélodie issus de théories
  diverses. Sur neuf notes de test : **278 valeurs/structures, 12 familles** ;
  courbe temporelle des **cinq mesures Narmour** par triplet. Rejette les
  pistes polyphoniques sans séparation de voix fiable, sauf si on demande
  expressément une **hypothèse de ligne supérieure**, jamais présentée comme
  la véritable mélodie. Ce ne sont pas des
  étiquettes émotionnelles ni une exécution d'IDyOM original.
- `emopia.py` : inventaire du corpus EMOPIA directement à partir de ses noms
  de fichiers, hash, rejets, séparation reproductible de **chansons**.
- `piast_at.py` : lecture vérifiée des **2 023 annotations PIAST-AT**, trois
  niveaux d'accord entre les experts et distinction explicite entre
  **16 humeurs**, 11 genres et quatre traits de style ; identification des
  MIDI réellement disponibles, sélection reproductible des vidéos disjointes.
- `scripts/fetch_piast_at.py` : téléchargement **uniquement des MIDI et du CSV**
  depuis la révision officielle figée, sans traitement des enregistrements
  audio (1 900 correspondances exactes sur 2 023 annotations).
- `scripts/piast_at_benchmark.py` : classification supervisée de chaque humeur
  sur les seules caractéristiques extraites des MIDI, test séparé avec
  comparaison à une prédiction constante ; version légère, ou mécanismes
  académiques Partitura et music21 en option. Ne pas confondre la performance
  d'un classificateur et la preuve d'un mécanisme psychologique.
- `piast_research_cues.py` : **hypothèse tirée de recherches expérimentales**,
  et non d'un logiciel universitaire : profils majeurs/mineurs, tempo réel,
  articulation estimée, arc dynamique, plus six interactions optionnelles ;
  [comparaison H0/H1/H2](docs/piast-research-experiments.md).
- `emotion_evaluation.py` : baselines sur entraînement seulement et score sur
  test réservé, macro-F1 quatre classes, couverture, abstentions, confusion.
- `vgmidi_temporal.py` et `scripts/vgmidi_temporal_benchmark.py` : **première
  véritable comparaison humaine (version initiale à 24 signaux)**, sur 200 pièces de piano évaluées par ~30
  auditeurs *mesure par mesure*. À partir de 141 MIDI chronologiquement
  fiables, 111 pièces entraînent le lien entre 24 caractéristiques MIDI
  explicables (dont **Partitura tonal tension** et **music21 harmonies**)
  et les médianes valence/activation humaines. 20 pièces servent au choix du
  modèle et **10 thèmes connus du public sont réservés au test et exclus de
  l'apprentissage**.
  **MAE test sur −1..+1 : 0,236 valence / 0,172 activation**, contre
  **0,289 / 0,208** pour la baseline constante. La corrélation temporelle
  *à l'intérieur de chaque pièce* demeure faible (+0,08 / +0,23) : cette
  première amélioration **ne prouve pas** la compréhension des montées
  d'émotion. Le [rapport](reports/vgmidi-temporal-ten.md) montre aussi les
  erreurs, les refus et la dispersion des réponses humaines.
  **La reprise complète** utilise maintenant **1 203 variables normalisées**
  dans neuf groupes de provenances, avec de réelles courbes académiques
  temporelles. Partitura, music21 et `melody-features` ont fonctionné sur
  **141/141 pièces admissibles** ; jSymbolic original sur **137/141**.
  Sur les dix pièces historiques : **MAE V/A = 0,263 / 0,150** ; corrélations
  temporelles **+0,20 / +0,41**. Sur les **dix autres** pièces sélectionnées
  avant inspection : **MAE V/A = 0,177 / 0,193**, comparé à la moyenne constante
  **0,340 / 0,263** ; corrélations temporelles **+0,16 / +0,30**. L'exactitude
  temporelle reste **modeste** malgré le gain sur la valeur moyenne.
- `scripts/run_original_idyom.py` : configuration/lancement *optionnel* de
  l'outil IDyOM via py2lispIDyOM et SBCL. Le module
  `idyom_guardrails.py` vérifie les empreintes de toutes les pistes de
  préentraînement/test, refuse les doublons exacts et bloque EMOPIA dans le
  préentraînement. Aucun résultat IDyOM publié pour le moment.
- `idyom_dat.py` et `scripts/import_idyom_dat.py` : lecture du **format
  original `.dat` d'IDyOM** et conversion JSON sans recalculer ses modèles.
  Les surprises, entropies, probabilités de continuations, gains d'information,
  vues mélodiques/rythmiques et valeurs absentes sont conservés par note et
  par morceau. Lecture testée sur le schéma d'un exemple des auteurs, mais
  **aucun moteur Lisp original n'a encore tourné dans notre infrastructure**.
- `jsymbolic_ace.py` : parseur du **format ACE XML original 1.1** de
  jSymbolic, avec fonctions multi-valeurs, fenêtres temporelles natives et
  **dictionnaire original de définitions** (description/dimensions de chaque
  caractéristique) pour documenter la non-redondance.
  **Le moteur Java original 2.2 a réellement tourné** dans le workflow
  habituel : [run 42415633459](https://github.com/leye0/AnaMu/actions/runs/42415633459),
  **6 fenêtres et 226 caractéristiques**, autant de définitions officielles,
  sur MIDI polyphonique synthétique. Archive vérifiée par SHA-256 et mise en
  cache ; aucune extraction audio ni validation émotionnelle humaine.
- `scripts/batch_jsymbolic_vgmidi.py` : exécution **en lots du JAR Java 2.2
  non modifié** sur les pièces temporellement admissibles de VGMIDI. Les
  échecs individuels restent connus ; un `NaN` émis par jSymbolic pour une
  statistique indéfinie reste **manquant**, jamais artificiellement zéro.
  Les fenêtres de performance sont fusionnées par recouvrement temporel avec
  les mesures MIDI.
- `scripts/extract_tonal_tension.py`, `scripts/extract_harmony.py`,
  `scripts/emopia_benchmark.py` : exécutions locales et reproductibles.

Exécuter localement les tests légers :

```bash
python -m pip install 'mido>=1.3,<2'
python -m unittest tests.test_symbolic_expectation -v
```

Pour tester les **moteurs publiés** et préparer l'évaluation EMOPIA :

```bash
python -m pip install 'partitura>=1.8,<2' 'music21>=9,<12'
python -m unittest discover -s tests -p 'test_emotion_research.py' -v
python -m scripts.extract_tonal_tension /chemin/piano.mid
python -m scripts.extract_harmony /chemin/piano.mid
python -m scripts.emopia_benchmark /chemin/EMOPIA_2.2 --manifest-out emopia-split.jsonl
```

Pour extraire les mesures mélodiques académiques directement d'un MIDI :

```bash
python -m pip install 'melody-features==1.3.3'
python -m scripts.extract_melody_features /chemin/melodie.mid > melodia.json
python -m unittest discover -s tests -p 'test_melody_toolbox.py' -v
python -m scripts.import_idyom_dat /chemin/resultats-idyom.dat --json-out idyom-events.json
```

Le corpus de référence implicite de `melody-features` et la fidélité des
réimplémentations sont à auditer avant exploitation statistique. Le résultat
JSON garde ses valeurs inconnues et la provenance de chaque piste.

Le workflow GitHub Actions `symbolic-theory-tests.yml` exécute ces tests sur
des MIDI synthétiques, **sans télécharger de corpus ni traiter d'audio**.
La vérification Java originale peut être activée manuellement avec le
paramètre `jsymbolic_smoke` ; elle télécharge **seulement l'outil publié**,
dans une exécution séparée et plafonnée. Cette vérification plus coûteuse
n'est pas lancée à chaque modification de code.
Une **comparaison humaine VGMIDI** plus longue est disponible dans **le même
workflow**, à déclencher avec `vgmidi_temporal=true` (ou un commit explicitement
marqué `[vgmidi-run]`). Le job ne publie que des rapports dérivés, jamais les
MIDI téléchargés. Le test unitaire des conventions VGMIDI roule normalement.
L'option complète utilise `melody-features`, Partitura, music21, **le vrai
jSymbolic Java**, la théorie rythmique/harmonique additionnelle et les deux
modèles d'attentes MIDI, puis montre séparément les résultats par morceau,
la couverture de chaque moteur et les ablations sur validation. Par défaut,
**IDyOM Lisp original reste manquant** tant que ses propres fichiers de
sortie validés ne sont pas fournis ; il n'est pas remplacé subrepticement.
Le job facultatif exporte désormais aussi un **modèle JSON déployable** et
analyse séparément un thème connu, Bach et Chopin à l'aide de ce modèle ;
la mesure des émotions des auditeurs n'existe pas pour ces deux classiques.
**Bilan du 7 novembre 2026 : 100 tests locaux réussis**, y compris les nouveaux
adaptateurs académiques. Deux jobs GitHub Actions antérieurs ont réussi
(tests symboliques et analyse Java originale), sur
[l'exécution 42415633459](https://github.com/leye0/AnaMu/actions/runs/42415633459).

Pour analyser **directement** une autre composition connue, avec le modèle
calibré de 1 198 variables maintenant inclus dans le dépôt :

```bash
python -m scripts.analyze_known_midi \
  --jsymbolic-jar /chemin/jSymbolic2.jar \
  --json-out ./emotion-par-mesure.json /chemin/oeuvre-connue.mid
```

Sans le JAR, les observations jSymbolic manquent et sont **signalées** au
lieu d'être inventées. Le transfert d'une calibration VGMIDI à d'autres
styles n'est pas encore prouvé.
Pour reproduire les trajectoires Bach/Chopin déjà publiées avec leur partition
intégrée à music21 : `python -m scripts.analyze_known_scores --out ./analyses`.
Pour étendre le traitement à **cinq œuvres identifiées de Bach, Chopin,
Mozart et Beethoven**, utiliser `python -m scripts.analyze_known_scores
--expanded --out ./analyses` (ajouter `--jsymbolic-jar ...` pour l'original
Java). Le moteur réessaie **avec de véritables fenêtres Java plus longues**
après un timeout ; il signale explicitement cette résolution temporelle
différente de celle de l'apprentissage, ou l'absence persistante de Java.
La même analyse élargie est disponible via le workflow habituel avec
`classics_analysis=true` ou `[classics-run]`, sans réapprendre VGMIDI.
`scripts/trace_known_mechanisms.py` aligne, **mesure par mesure**, 18
descripteurs explicites (Partitura, music21, Narmour, attentes entraînées,
rythme, texture et répétition) sur les émotions inférées. Le MIDI source et
le modèle doivent correspondre **par SHA-256** au rapport d'analyse. Ces
juxtapositions montrent des mécanismes observés, **pas des causes prouvées**.
Pour les partitions longues, `--jsymbolic-segment-threshold 48` déclenche
l'exécution du **jSymbolic Java original** sur des extraits bornés de 16
mesures. Ses seules fenêtres temporelles sont replacées sur le temps de la
pièce complète ; les descripteurs globaux restent manquants (ils ne sont
jamais recomposés artificiellement). Le rapport chiffre les segments réussis,
les échecs et les éventuelles anomalies de couplage note-on/note-off du MIDI.
L'[audit de la run segmentée](reports/segmented-classics-coverage-audit.md)
montre des couvertures insuffisantes (Chopin 1/5, Beethoven 1/10) ; le moteur
rend désormais un statut `partial`, et les essais lourds sont suspendus.

## Corpus et qualité

- **Qualité avant quantité** : même 500 ou 2 000 MIDI corrects peuvent suffire
  à un protocole ; **10 000 n'est pas un minimum**.
- **Corpus à la demande** : chaque algorithme explicite d'abord ses besoins ;
  ne pas retraiter les MIDI s'il peut les consommer directement.
- **Annotation humaine séparée de l'inférence** : XMIDI (label global),
  EMOPIA (extraits piano), DEAM (émotions temporelles, surtout audio), PMEmo
  (annotations et physiologie). Ne pas inventer de vérités temporelles.
- **Précision plutôt que couverture** : conserver les refus, niveaux
  d'incertitude, provenances et contrôles négatifs.
- **Théories documentées** : Meyer, Huron, Narmour, Schellenberg, Pearce/IDyOM,
  Lerdahl/Krumhansl, Farbood, Herremans/Chew, Steinbeis, Egermann, Cheung.
- **Validation honnête** : séparer les œuvres entre entraînement et test,
  mesurer l'apport de l'ordre des événements, comparer aux baselines statiques,
  publier les échecs ; jamais de causalité déclarée sur simple corrélation.

## État préexistant (conservé)

- XMIDI : ZIP de **449 632 771 octets**, accès partiel par requêtes HTTP Range.
- Une correspondance MD5 XMIDI↔GigaMIDI confirmée sur le pilote ; aucune
  identité d'artiste, aucun taux de couverture global démontré.
- Audit de 200 XMIDI, **199 analysés**. Dans l'échantillon aléatoire de 100,
  **64** avaient au moins 16 notes dans chacune des parties guitare,
  basse et batterie. Cette richesse instrumentale **ne prouve pas** la
  fidélité de l'arrangement à un enregistrement.
- Ancien protocole Demucs/ADTOF/Omnizart écrit, **jamais exécuté** ; ses
  scripts et rapports restent consultables à titre historique.

**Important :** ce premier score sur **VGMIDI** est une validation *interne* à
ce corpus et avec un sous-ensemble de nos mécanismes, pas une preuve externe.
**Aucun score de prédiction sur les annotations humaines d'EMOPIA n'a encore été
mesuré.** IDyOM Lisp, jSymbolic Java en fusion, de nombreuses familles
théoriques, les ablations et une validation externe restent à construire.
