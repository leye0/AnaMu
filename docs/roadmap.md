# AnaMu — Feuille de route scientifique et technique

**Mise à jour du 9 novembre 2026 :** le nouveau cap est la
**[grammaire musicale multi-axes](music-grammar-research-program.md)**,
fondée sur des observations de partition, interprétation et audio, des
relations hiérarchiques explicables, des règles déclaratives et des tests
académiques propres à chaque capacité. Les passages ci-dessous détaillent
**l'historique du programme sur les émotions**, et non la priorité
d'implémentation après ce changement de direction. Le noyau grammatical
doit préserver tempo variable, nuances et instruments dès le contrat des
données ; l'analyse audio proprement dite peut rester une étape ultérieure.

**Version : 1.1 — 7 novembre 2026.**  
**Décision :** théorie musicale algorithmisée → mécanismes temporels → étude
des émotions humaines → corpus construit selon les besoins prouvés → analyses
de compositions connues → génération expérimentale. **Audio/Demucs reportés.**

Le programme scientifique détaillé, les références primaires et les
critères de chaque algorithme se trouvent dans
**[theory-to-algorithms.md](theory-to-algorithms.md)**. Ce document constitue
la référence d'implémentation pour les prochaines étapes.

**Garde-fou additionnel (8 novembre 2026) :** consulter les
[contrats scientifiques exécutables](research-evidence-gates.md) avant de
choisir un corpus, d'affirmer qu'un outil académique original a été exécuté
ou de présenter un test déjà exploré comme une confirmation indépendante.

**Progrès S2 (8 novembre 2026) :** un premier [test de cadences
expertisées sur 198 partitions symboliques](dcml-cadence-study.md) trouve
un apport mesurable de l'harmonie sur le rythme seul, avec contrôle
permuté et validation par œuvre parente et par compositeur. **Il ne valide
aucune émotion**, et il reste exploratoire. Le chantier des cadences est
**mis en pause** pour ne pas recycler le même axe indéfiniment.

**Progrès S1 (8 novembre 2026) :** le [test de continuation mélodique sur
les réponses humaines de Cuddy et Lunney (1995)](cudlun-human-expectancy-study.md)
observe, en sortie de huit contextes tenus à l'écart successivement,
**ρ 0,724 → 0,795** lorsqu'un modèle de contour/tonalité corrige le résidu
d'une référence relative de notes. Gain de **+0,071 sur 8/8 contextes**,
également positif avec exclusions plus larges (direction et taille des
intervalles). Ce modèle a été formulé après la première inspection des
scores : **exploratoire uniquement ; contre-épreuve externe ci-dessous**.

**Transfert S1 (8 novembre 2026) :** [contre-épreuve sur les 120 continuations
de huit mélodies réelles de Schellenberg (1996)](schellenberg-external-transfer-study.md),
notées par **20 autres auditeurs**. Le modèle fixé uniquement sur Cuddy
apporte encore un gain contextuel (ρ **0,560 → 0,650**), mais le **contour
seul atteint 0,770**. Ainsi le gagnant de Cuddy **n'est pas** le meilleur
hors étude : privilégier la robustesse du contour plutôt que la complexité
à ajuster. Données externes non utilisées pour le réentraînement ; une
troisième étude préenregistrée demeure nécessaire.

**Troisième jeu de mesures S1 (9 novembre 2026) :**
[Manzara/Witten/Conklin (1992)](manzara-cross-target-study.md) mesure une
**autre variable** : le nombre de bits de surprise de **chaque vraie note**
obtenu à partir de paris humains. Sur **82 notes réparties en deux chorales**,
le contour appris sur Cuddy ne se transfère **pas** : ρ **+0,013 / −0,094**
par chorale, contre **+0,449 / +0,481** pour des scores IDyOM publiés dans
une thèse (import seulement ; corpus d'apprentissage tiers non vérifié).
Cette **limite** interdit d'appeler le 0,770 de Schellenberg « performance
sur la surprise musicale continue ». Deux chorales ne suffisent pas à la
validation générale. Voir aussi [l'audit du benchmark MEX 2026](mex-2026-source-audit.md)
sur timbre audio, segmentation annotée et EEG, distincts des émotions.

**Nouvelle règle :** chercher et intégrer systématiquement les **outils
académiques existants**, maximiser la diversité des mécanismes non redondants
et mesurer chacun séparément. Voir [l'inventaire de 23 mécanismes et le banc
EMOPIA](emotion-engine.md). EMOPIA sert de **vérification hors entraînement**,
pas de générateur de pseudo-règles émotionnelles.

## 1. Vision et objectifs

**AnaMu étudie comment les événements musicaux créent, déplacent, déçoivent,
confirment et résolvent des attentes, et comment ces transformations peuvent
être reliées aux émotions perçues par des auditeurs.** L'ambition n'est pas
de réapprendre que le mineur et le tempo lent sont souvent associés à la
tristesse, mais d'identifier des mécanismes temporels explicables.

Trois objectifs successifs et complémentaires :

1. Comprendre la composition symbolique, les mélodies, les harmonies, les
   motifs, les relations et l'organisation des chansons connues.
2. Découvrir et tester les relations entre ces mécanismes **en séquence** et
   les annotations émotionnelles humaines, avec incertitude et limites.
3. Plus tard, concevoir un générateur MIDI piloté par trajectoires
   émotionnelles, instruments, structures et références stylistiques.

Une corrélation ne prouve pas un mécanisme causal. La **tension**, le
**plaisir**, l'**activation**, la **valence**, l'émotion **perçue** et l'émotion
**ressentie** sont des concepts distincts.

## 2. Ordre des travaux décidé

| Priorité | Phase | Livrable / condition de sortie | Statut |
|---|---|---|---|
| **Maintenant** | **S0 — Laboratoire MIDI brut** | Lecteur conservateur, vues sans pertes, fixtures et contrats de données. Aucune extraction audio. | **Premier incrément en cours** |
| **Maintenant** | **S1 — Attentes mélodiques** | Baseline probabiliste puis comparaison IDyOM + Narmour/Schellenberg, vraies mesures de prédiction hors entraînement. | **Cuddy puis Schellenberg : contour jusqu'à ρ 0,770 pour les notes candidates. Mais Manzara : contour ρ +0,013 / −0,094 pour la surprise réelle (82 notes, deux chorales). IDyOM tiers ~0,45–0,48 ; original non exécuté. Prochaine priorité : modèle statistique réellement probabiliste entraîné sur corpus distinct.** |
| **En cours** | **S2 — Harmonie et enchaînements** | Hypothèses d'accords, progression, fonction, tonalité locale, cadences, Tonal Pitch Space, Spiral Array ; tests sur vérité musicale annotée. | **music21 + Partitura actifs ; 1 992 cadences de 198 partitions expertes testées sur notes MIDI-compatibles. Gain harmonique exploratoire, pas de score émotionnel ni validation de résolution atypique.** |
| **En cours** | **S3 — Motifs, formes, tension** | Répétitions/transformations, structure hiérarchique, mémoire et modèles temporels Lerdahl/Farbood. | **Motifs/récurrences, cadences et mémoire multicadence en approximation calculable ; hiérarchie perceptive et modèles originaux complets à étudier.** |
| **En cours** | **S4 — Fusion des mécanismes** | Entropie avant l'événement, surprise à l'événement, tension/résolution et interactions, ablations. | **Fusion temporelle réelle des originaux music21/Partitura/melody-features/jSymbolic, deux n-grammes de contrôle, mémoire/interaction et ablations. Extraction mutualisée et export de calibration JSON ajoutés ; IDyOM original non exécuté.** |
| **En cours** | **S5 — Émotions humaines** | Relations calibrées aux labels et courbes **humaines** avec baselines, séparations d'œuvres et contrôles négatifs. | **20 morceaux connus comparés mesure par mesure aux humains en deux expériences : fusion de 1 203 variables de neuf familles, moteur Java original jSymbolic sur 137/141 MIDI, études de contribution par ablation. Corrélations temporelles modestes ; EMOPIA externe intact.** |
| **Après preuve de besoin** | **S6 — Corpus ciblé** | Sélection par requirements de S0–S5, peu de MIDI fiables, couverture/erreurs/biais documentés. | Études de sources déjà réalisées ; sélection à redéfinir |
| **Recherche appliquée** | **S7 — Bach, Chopin, puis pop** | Analyses explicables de pièces identifiées, confrontées à la théorie et aux évaluations humaines quand elles existent. | **Premier pipeline réellement exécuté sur Bach BWV 66.6 (9 mesures) et Chopin Mazurka op. 6 no 2 (72 mesures), avec modèles calibrés sur VGMIDI. Pas de vérité affective humaine disponible sur ces deux œuvres ; transfert de style non prouvé.** |
| **Long terme** | **S8 — Génération symbolique** | Génération + révision sous contraintes, rendus MIDI multipistes, évaluation humaine et musicale. | À faire |
| **Ultérieur, conditionnel** | **S9 — Audio, paroles, Demucs** | Un cas d'usage démontre que l'observation audio améliore S0–S8, avec coûts et erreurs mesurés. | **Reporté explicitement** |

Les phases ne sont pas des murs : S5 peut tester un mécanisme de S1 sur un
petit dataset avant la fin de S3. Mais il est interdit de déclarer un détecteur
émotionnel validé tant que l'annotation humaine et les contrôles requis
n'existent pas.

## 3. Pourquoi les algorithmes précèdent le corpus

Le plan précédent imposait catalogue identitaire et rapprochement MIDI↔audio
avant la grammaire. **Cette dépendance est supprimée.**

1. Définir un mécanisme théorique à étudier et l'observation attendue.
2. Écrire le contrat des données **strictement nécessaires** au module.
3. Tester sur MIDI bruts ou séquences symboliques contrôlées. Conserver les
   données originales ; ne préparer que les vues demandées.
4. Identifier où une vérité terrain humaine ou musicale devient nécessaire.
5. Sélectionner alors un petit corpus pertinent, avec critères adaptés à
   cette question. Élargir **uniquement** si la preuve scientifique le justifie.

Exemples : une étude des intervalles peut utiliser directement des pistes
MIDI monophoniques ; une étude des fonctions harmoniques a besoin de vérité
terrain d'accords/tonalités ; XMIDI permet des tests émotionnels **globaux**
mais pas des courbes temporelles ; DEAM fournit des évaluations émotionnelles
temporelles **audio** mais pas un MIDI aligné par défaut.

**Qualité avant quantité** : 10 000 MIDI n'est ni une cible obligatoire ni un
minimum ; 500 ou 2 000 excellents cas peuvent suffire. Garder aussi un index
des refus et de leurs motifs. Ne pas favoriser les seuls styles plus faciles
à analyser sans mesurer le biais.

## 4. Architecture d'analyse

### Entrée et vues, sans conversion audio forcée

Un fichier MIDI valide est un *asset brut*. On doit pouvoir le soumettre
directement à un module qui sait lire les événements nécessaires.

- **Événements natifs** : notes, pistes, canaux, programmes, durées, tempo,
  vélocités, mètre, contrôleurs ; conserver source et checksum.
- **Vues** : lignes monophoniques candidates, ensembles simultanés de notes,
  hypothèses d'accords, modes et tonalités, structure, motifs, positions.
- **Indicateurs** : `confidence`, `unknown`, ambiguïtés, qualité de segmentation,
  hypothèses concurrentes, provenance de chaque dérivation.
- **Moteurs purs** : consommant les vues dont ils ont besoin, retournant
  des événements mesurés, non des étiquettes émotionnelles improvisées.

### Moteurs à algorithmiser et comparer

1. **Attente mélodique** : Narmour, Schellenberg, IDyOM/Pearce,
   continuations conditionnelles et adaptation au morceau.
2. **Harmonie tonale** : Lerdahl/Krumhansl, attraction, contexte local,
   fonctions, cadences, relations hiérarchiques.
3. **Géométrie tonale** : Herremans/Chew (cloud diameter, momentum,
   tensile strain), hypothèses de tonalité et stabilité.
4. **Intégration temporelle** : Farbood, tendances, fenêtres, densité,
   crescendos, pente de tension et relaxation.
5. **Réponses aux attentes** : Meyer/Huron ; différence entre prédiction,
   incertitude, surprise, suspension, réaction et appréciation.
6. **Interaction attente/plaisir** : Cheung et al. ; mesurer les interactions
   *avant/après* l'événement sans les prendre pour toutes les émotions.
7. **Structure et motif** : hiérarchie Lerdahl/Jackendoff, transformations,
   récurrence, segmentation et attentes de retour.

Les études de Steinbeis et d'Egermann fournissent des protocoles humains
pertinents pour vérifier certaines prédictions de tension/réaction. Chaque
module doit posséder définition, référence, limites, tests négatifs,
baselines et mesures de calibration dans
[le programme scientifique](theory-to-algorithms.md).

## 5. Protocole scientifique : quatre couches de preuve

1. **Exactitude informatique** : notes, temps, intervalles, fréquences,
   probabilités et invariances contrôlées par des tests unitaires.
2. **Justesse musicale** : accord/voix/tonalité/structure comparés à des
   analyses humaines, sans maquiller `unknown` en précision artificielle.
3. **Théorie de la perception** : probabilités comparées à des continuations
   humaines ; tension comparée à des évaluations temporelles.
4. **Émotion** : corrélations et prédictions sur labels humains, avec
   contextes, styles et groupes d'œuvres séparés de l'apprentissage.

Baselines indispensables : caractéristiques statiques (mode/tempo),
unigramme, modèle sans ordre, modèles séquentiels simples, versions sans
interactions. Contrefactuels : permuter l'ordre des événements, retarder une
cadence, modifier un accord, transposer une progression, retirer un motif.

Ne jamais déduire « tristesse prouvée » d'une courbe de tension. Une classe
humaine globale ne prouve pas la cause locale d'une émotion.

## 6. Sources et annotation humaine — choisies par besoin

| Source | Atout principal | Limitation importante |
|---|---|---|
| [PIAST-AT (Bang et al., 2024)](https://huggingface.co/datasets/Hayeonbang/PIAST) | **2 023 extraits de piano** annotés par trois musiciens parmi 16 termes d'humeur, avec niveaux d'accord 3/2/1 et MIDI transcrits publiés | **1 900 correspondances exactes CSV↔MIDI** à la révision vérifiée ; humeur perçue plutôt qu'émotion ressentie ; 11 catégories de genre et quatre de style à exclure des cibles ; piano seul |
| [XMIDI / XMusic](https://github.com/xmusic-project/XMIDI_Dataset) | 108 023 MIDI, 11 classes émotionnelles humaines et genre | Étiquette du **morceau**, titre/artiste non fournis dans les noms |
| [EMOPIA](https://annahung31.github.io/EMOPIA/) | 1 087 extraits de piano, MIDI et audio, quadrants émotionnels annotés | Piano pop, classes par **extrait**, pas secondes individuelles |
| [VGMIDI](https://github.com/lucasnfe/vgmidi) | 200 pièces de piano de jeux vidéo, environ 30 annotations humaines valence/activation **par mesure**, MIDI originaux | Droits des arrangements à vérifier ; 59 des 200 MIDI refusés dans notre premier parseur de mesure, couverture partielle ; protocole interne et transfert de style non prouvé |
| [DEAM](https://cvml.unige.ch/databases/DEAM/) | 1 802 extraits/chansons, valence/activation dans le temps | Principalement audio, appariement MIDI à créer prudemment si nécessaire |
| [PMEmo](https://github.com/HuiZhangDB/PMEmo) | 794 chansons, annotations et activité électrodermale | Audio ; physiologie et émotion déclarée distinctes |
| MIDI Bach/Chopin autorisés | Analyses de tonalité, motifs, cadences et forme, études de cas compréhensibles | Domaine public de la composition ≠ licence de chaque transcription MIDI |
| [MetaMIDI](https://github.com/Metacreation-Lab/MetaMIDI-Dataset), [GigaMIDI](https://github.com/Metacreation-Lab/GigaMIDI-Dataset) | Identités et caractéristiques déjà calculées, pour phase d'enrichissement | Accès/licences, identité de l'arrangement et qualité non garantis |

**Priorité opérationnelle (8 novembre 2026) : PIAST-AT**, plutôt que déduire
des noms d'émotions de la seule valence/activation numérique de VGMIDI ou des
quatre quadrants d'EMOPIA. Les labels de genre/style ne sont **pas** des
émotions. Un premier banc MIDI seul compare humeurs humaines majoritaires et
prédictions du modèle à la fréquence de chaque humeur, sur des sources vidéo
disjointes. [Protocole et résultats du pilote](../reports/piast-at-pilot.md).
**Première hypothèse scientifique évaluée** : les indices mode, tempo,
articulation et nuances issus de l'étude expérimentale de Micallef Grimaud
et Eerola (2022) améliorent modestement le classement des 15 humeurs nommées
sur 91 nouveaux extraits, **AP 0,528 → 0,548**, tandis que six produits
d'interaction redescendent à 0,539. [Hypothèses, ablations et limites](piast-research-experiments.md).

L'unité d'entraînement est le **morceau/œuvre** lorsque des versions peuvent
fuir d'un jeu à l'autre. Conserver les annotations originales, leurs
désaccords et les différences émotion perçue/ressentie. Enregistrer dates,
versions et droits. Ne jamais utiliser des labels inférés comme vérité humaine.

## 7. État des travaux antérieurs (préservés, mais non bloquants)

La version 0.8 a accompli des audits utiles, qui demeurent vérifiables :

- **XMIDI** : ZIP distant **449 632 771 octets** et 108 024 entrées ZIP ;
  lecture ciblée HTTP Range possible. [Audit de sources](audit-p0.md).
- **Jointure XMIDI↔GigaMIDI** : une première correspondance MD5 exacte
  `quiet`/`traditional` parmi 100 XMIDI choisis et 5 200 MD5 lus dans **un seul
  shard** ; pas de titre/artiste validé, aucun taux de couverture général.
  [Rapport](p1-exact-join.md) ; [exécution](https://github.com/leye0/AnaMu/actions/runs/42336949364).
- **Instrumentation** : 200 XMIDI sélectionnés, 199 lus. Dans l'échantillon
  aléatoire de 100, 64 avaient au moins 16 notes de guitare, basse et
  batterie chacune ; cela ne prouve pas la fidélité de l'arrangement à un
  enregistrement. [Rapport](p1-instrument-audit.md).
- **Audio/batterie** : [protocole Demucs/ADTOF/Omnizart](p1-drum-audio-validation-plan.md)
  documenté, **non exécuté**, maintenant **archivé comme piste future**. Ne
  pas le laisser dans la liste des tâches immédiates.
- Les scripts de sondage et audits historiques restent en place ; ne pas
  les supprimer, mais **ne pas lancer leurs workflows lourds par défaut**.

Depuis le pilote VGMIDI, le projet a **une première comparaison réelle des
émotions annotées par des humains et estimées par AnaMu** sur des thèmes
connus mis de côté pour le test. Le résultat reste modeste, surtout pour la
forme temporelle ; une jointure MD5 ou un audit instrumental ne valent toujours
pas validation psychologique.

### Reprise académique mesurée — 7 novembre 2026

- [Dix mêmes thèmes, analyse exploratoire](../reports/vgmidi-temporal-ten-full.md) :
  **MAE V/A 0,263 / 0,150**, corrélations temporelles intra-pièce
  **+0,20 / +0,41**. Le pilote antérieur sur ces mêmes pièces reposait sur
  24 variables ; la reprise en utilise 1 203. Les titres avaient déjà été
  inspectés : ce n'est **pas** un test indépendant.
- [Dix autres œuvres sélectionnées avant examen de leurs annotations](../reports/vgmidi-temporal-ten-confirmatory.md) :
  **MAE V/A 0,177 / 0,193** contre la constante **0,340 / 0,263** ;
  corrélations temporelles **+0,16 / +0,30**. Test interne VGMIDI,
  pas de généralisation prouvée à Bach, Chopin ou à la pop.
- Les résultats viennent de **Partitura, music21, melody-features, Narmour et
  jSymbolic Java réellement exécutés**, complétés par des approximations
  algorithmiques identifiées par famille et deux modèles d'attente formés
  uniquement sur les œuvres d'entraînement. **IDyOM Lisp original n'a pas
  été exécuté** ; les phénomènes cognitifs non observables ne sont pas
  présentés comme des moteurs existants. Quatre MIDI ont échoué chez jSymbolic.
- Les ablations sont effectuées **sur validation** : certaines familles
  apportent un gain, d'autres non. L'agrégation des 1 203 colonnes n'est pas
  une preuve que chacune contribue ni que les 23 théories sont reproduites.

### Pipeline réutilisable — incrément suivant

Le benchmark VGMIDI et la nouvelle inférence autonome passent par le **même
extracteur académique** `anamu.emotion_pipeline.extract_academic_rows()`.
Après apprentissage supervisé, `--model-out` exporte l'imputation, les
échelles et les poids Ridge ainsi que les statistiques d'attente entraînées
sur les seules pièces d'apprentissage, en **JSON sans désérialisation de code**.
Chaque nouveau MIDI obtient des estimations valence/activation par mesure,
les moteurs réellement disponibles et des avertissements d'extrapolation.
Un script applique la chaîne à Bach BWV 66.6 et Chopin Mazurka op. 6 no 2
distribués avec music21. **Ce sont des analyses de compositions connues,
mais pas des évaluations humaines de leurs émotions**.
Le modèle JSON rechargé reproduit exactement les estimations sur les
**136 mesures de *Chrono Trigger*** déjà tenues hors apprentissage : écart
numérique maximal **0** entre l'extraction de référence et l'analyse
autonome. Le premier pilote local du modèle sauvegardé n'avait pas les
sorties Java jSymbolic. La run GitHub Actions complète a maintenant réussi
et son **modèle de 1 198 variables**, comprenant jSymbolic original,
est versionné sous `models/vgmidi-piano-ridge.json.gz` : il se recharge
directement sans apprendre de nouveau sur les œuvres analysées.

- [Analyse concrète Bach/Chopin](../reports/bach-chopin-emotions.md) : les
  estimations pour 9 mesures de Bach et 72 mesures de Chopin, leurs séries
  temporelles SVG et la couverture explicite des vrais moteurs.
- La suite étendue (Bach BWV 140.7, Mozart K. 545 et Beethoven op. 18 no 1)
  utilise **l'ordre écrit de la partition** : le lecteur MIDI ne développe
  pas de reprises hypothétiques. Exemple vérifié : Beethoven, mouvement 3,
  représente **145 mesures écrites**, et non les 456 mesures de l'export
  initial qui développait implicitement des reprises.
- La première [run indépendante de la phase d'apprentissage pour cinq
  classiques](../reports/known-classics-emotions.md) a réussi : jSymbolic
  **original exécuté sur les deux Bach et Mozart (3/5)**, mais timeout pour
  Chopin et Beethoven (2/5), même après une seconde tentative à fenêtres
  plus longues. Ce n'est donc **pas encore** une couverture académique
  complète sur ces deux œuvres ; les données manquantes sont imputées.
- [Traces de 18 mécanismes musicaux](../reports/known-classics-mechanisms.json)
  alignées sur les mêmes MIDI et mesures, avec contrôles SHA-256 des sources.
  Les observations de tension, harmonie, mélodie, attentes, rythme et texture
  décrivent la composition ; elles ne démontrent aucune cause émotionnelle.
- [Expérience sans nouvelle extraction sur 20 morceaux annotés](../reports/vgmidi-valence-memory-experiment.md)
  : mémoire causale courte de valence, testée à paramètres fixes sur deux
  groupes déjà inspectés. La MAE moyenne baisse légèrement dans les deux,
  mais les intervalles bootstrap par morceau couvrent zéro ; garder cette
  voie **expérimentale et désactivée par défaut**. Prochaine étape scientifique :
  sélection exclusive sur validation puis nouvelles œuvres intactes.
- La reprise contrôlée de jSymbolic à fenêtres de 30 secondes a été exécutée
  dans la run des cinq classiques. Elle n'a pas suffi pour Chopin et Beethoven :
  ces deux sorties Java demeurent **absentes puis imputées**. Le pipeline doit
  désormais utiliser un **découpage en extraits MIDI de 16 mesures** dès que
  l'œuvre dépasse 48 mesures. Ce découpage conserve les canaux, les pistes,
  le tempo et les notes traversant les frontières, puis rétablit les secondes
  absolues dans les fenêtres Java. Les caractéristiques globales sont exclues,
  les éventuels segments manquants ne sont pas interpolés, et les anomalies
  d'appariement MIDI sont quantifiées. L'[audit de la run segmentée](../reports/segmented-classics-coverage-audit.md)
  a confirmé des résultats **insuffisants** : Chopin 1/5 extraits et Beethoven
  1/10. Un statut `ok` sur un seul extrait était trompeur ; le statut est
  désormais `partial` et la priorité revient à l'évaluation des émotions.
- Avec jSymbolic original, la réanalyse autonome des **136 mesures de Chrono
  Trigger** reproduit les sorties du banc académique avec une erreur numérique
  maximale inférieure à `3e-15` ; la chaîne entraînement → export → rechargement
  → extraction du même morceau est donc cohérente.
- Les deux œuvres classiques restent **hors validation humaine**, alors que
  [les dix pièces VGMIDI](../reports/vgmidi-temporal-ten-full.md) comparent
  réellement les annotations et les sorties du système.

## 8. État du premier incrément S0/S1

Le code expérimental introduit :

- `anamu/midi_views.py` : pistes/canaux monophoniques *candidats*, avec
  rejet explicite des recouvrements, sans supposer identifier la vraie mélodie.
- `anamu/expectation.py` : baseline probabiliste à ordre variable lissé,
  renvoyant `P(event|contexte)`, surprise en bits et entropie **avant**
  l'événement. **Ce n'est pas IDyOM.**
- `anamu/tempo_map.py` : conversion exacte des événements MIDI vers les
  secondes, même avec changement de tempo.
- `anamu/jsymbolic_ace.py` : réception des vrais vecteurs ACE XML 1.1
  jSymbolic, sections temporelles, dimensions, empreinte du fichier. Le
  parseur accepte exclusivement la DTD interne **officielle** après contrôle
  et la retire sans en interpréter les entités ; les DTD étrangères sont
  refusées. Le **dictionnaire original des features** `feature_key_file` peut
  aussi être importé : noms, descriptions de l'auteur, caractère séquentiel,
  dimensions attendues. Ces métadonnées aident à classer les mécanismes sans
  confondre 1 497 valeurs avec 1 497 causes émotionnelles. Le lecteur est
  testé sans présenter une fixture comme résultat Java réel.
- `anamu/idyom_guardrails.py` : séparation stricte des répertoires,
  empreintes SHA-256 pour éviter les doublons exacts, blocage des MIDI EMOPIA
  en préentraînement, budget de fichiers et manifestes vérifiables.
- `anamu/idyom_dat.py` : lecture du **format `.dat` original** d'IDyOM,
  groupement par mélodie, surprise/entropie pour chaque point de vue, vecteurs
  de probabilités des continuations, informations manquantes explicites et
  conservation facultative de toutes les colonnes non normalisées. L'axe
  temporel reste en unités natives, sans secondes inventées.
- `anamu/melody_toolbox.py` : exécution de `melody-features==1.3.3` sur les
  pistes monophoniques admissibles. 278 colonnes sur la fixture de neuf notes,
  **12 familles descriptives**, et cinq mesures de Narmour à chaque triplet.
  Les pistes polyphoniques ambiguës sont rejetées, pas devinées.
- `tests/test_symbolic_expectation.py` : tests locaux sur fixtures MIDI et
  séquences contrôlées ; il reste à mesurer la validité perceptuelle.

### Prochaines actions vérifiables

- [x] Reprioriser théorie / MIDI direct / émotion humaine, repousser l'audio.
- [x] Mettre sur papier les références, modules, entrées, sorties et tests.
- [x] Créer le tout premier noyau S0/S1 et tests synthétiques.
- [x] Exécuter la **véritable** méthode *Tension Ribbons* via Partitura sur
  un MIDI piano polyphonique fictif ; mesurer la courbe tonale sans attribuer
  d'émotion par décret.
- [x] Exécuter Krumhansl–Schmuckler et des hypothèses de degrés romains via
  music21 ; noter les incertitudes de l'analyse harmonique.
- [x] Préparer un manifeste EMOPIA vérifiable : **100 % hors entraînement**
  pour le test externe principal, ou splits par YouTube ID pour diagnostic
  interne ; une baseline train-only et des métriques test-only ; **aucun score
  émotionnel réel n'est encore revendiqué**.
- [x] Fournir un adaptateur de sorties et un lanceur optionnel pour **IDyOM
  original** avec py2lispIDyOM, sans prétendre l'avoir exécuté.
- [x] Fournir un lanceur des caractéristiques **jSymbolic original**
  (sorties en fenêtres temporelles), puis prouver son exécution réelle.
- [x] Intégrer **la bibliothèque publiée `melody-features`** (FANTASTIC,
  SIMILE, MUST, jSymbolic réimplémenté, MIDI Toolbox, Narmour, etc.) sur MIDI
  monophonique seulement, avec changements de tempo, sortie JSON et tests
  de non-invention des mélodies ; les 278 sorties sont des *descripteurs* et
  pas 278 causes d'émotions.
- [x] Produire une chronologie datée de cinq scores Narmour sur triplets
  en réutilisant les fonctions publiées ; ce sont des réalisations observées,
  pas des probabilités d'attentes validées.
- [x] Lire le format **ACE 1.1 jSymbolic original** en conservant les
  dimensions et les fenêtres sans inventer de coordonnées temporelles ; tester
  le refus des données corrompues.
- [x] Ajouter des garde-fous anti-fuites dans le lanceur IDyOM original,
  notamment les SHA-256 entre train et test et le refus d'EMOPIA dans le
  préentraînement.
- [x] Lire **les vrais fichiers `.dat` d'IDyOM** selon le format fourni dans
  le dépôt officiel `py2lispIDyOM`, conserver les vues concurrentes,
  distributions et valeurs inconnues ; ajouter des tests de non-corruption.
- [x] Ajouter au **workflow existant** un test Java facultatif de la
  distribution jSymbolic 2.2 officielle, avec contrôle SHA-256 public et
  artefact de résultats, sans télécharger l'outil à chaque push.
- [x] **Exécuter réellement jSymbolic 2.2** dans le workflow existant :
  [run 42415633459](https://github.com/leye0/AnaMu/actions/runs/42415633459),
  SHA-256 officiel vérifié, **6 fenêtres, 226 types de descripteurs observés,
  226 définitions importées**, fichier de résultats conservé en artefact,
  binaire mis en cache. Fixture MIDI synthétique, non-validation émotionnelle.
- [ ] Faire réellement tourner l'IDyOM upstream (SBCL, Quicklisp, SQLite),
  sur un apprentissage séparé du jeu de test, et analyser les résultats.
- [ ] **Inventorier et dédoublonner** les features temporelles jSymbolic
  effectivement extraites (rythme, expression, densité, texture,
  instrumentation), puis vérifier leur fidélité sur musique réelle.
- [ ] Aligner les mécanismes dans le temps et réaliser une première fusion
  explicable, avec indicateur d'incertitude et tests d'ablation.
- [ ] Auditer la fidélité des réimplémentations de `melody-features`, son
  corpus de référence embarqué (903 mélodies), les redondances entre familles
  et le comportement des mesures sur des mélodies humaines externes.
- [ ] Apprendre un estimateur d'émotions sur un **autre corpus** pour le test
  EMOPIA externe (ou sur EMOPIA train pour le protocole secondaire clairement
  identifié) ; sélectionner les paramètres en validation, mesurer les scores
  externes une seule fois sur une version figée.
- [ ] Définir un petit jeu de continuations monophoniques externes avec
  référence humaine (et sans fuite entre entraînement et test).
- [ ] Exécuter et comparer **IDyOM réel** et la baseline explicable ; rapporter
  les échecs, coûts, versions et hypothèses de style.
- [ ] Définir la première vérité terrain d'accords et implémenter les vues
  harmoniques S2 sans forcer de solution lorsqu'elles sont ambiguës.
- [ ] Choisir 2–5 pièces attribuées de Bach/Chopin pour études de cas
  musicales, sans inventer leurs émotions ni leurs versions MIDI.
- [ ] Choisir ensuite le sous-corpus émotionnel selon les sorties S1–S4,
  puis comparer sur EMOPIA et XMIDI avec précautions de granularité.
- [ ] Faire la première étude contrefactuelle et ablation complète.

## 9. Conditions de travail et budget

Les études commencent sur **fixtures en mémoire, puis petits lots bornés**.
Les workflows GitHub Actions restent des contrôles explicites : tests
automatiques légers, opérations lourdes seulement sur déclenchement et avec
plafonds de temps/volume. Aucun téléchargement de corpus massif ni de modèles
sans nécessité expérimentale. Garder dans Git les scripts, configurations,
résultats compacts et manifestes permis, pas les chansons protégées.

Une phase est **terminée** seulement quand code, données de test, validation
et limites sont reproductibles. L'état documenté ne doit pas masquer une
absence d'évaluation humaine.
