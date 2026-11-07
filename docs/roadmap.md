# AnaMu — Feuille de route scientifique et technique

**Version : 1.1 — 7 novembre 2026.**  
**Décision :** théorie musicale algorithmisée → mécanismes temporels → étude
des émotions humaines → corpus construit selon les besoins prouvés → analyses
de compositions connues → génération expérimentale. **Audio/Demucs reportés.**

Le programme scientifique détaillé, les références primaires et les
critères de chaque algorithme se trouvent dans
**[theory-to-algorithms.md](theory-to-algorithms.md)**. Ce document constitue
la référence d'implémentation pour les prochaines étapes.

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
| **Maintenant** | **S1 — Attentes mélodiques** | Baseline probabiliste puis comparaison IDyOM + Narmour/Schellenberg, vraies mesures de prédiction hors entraînement. | **Baseline et Narmour (outil `melody-features` + triplets datés) actifs ; IDyOM original et validation perceptive à faire** |
| **Prochain** | **S2 — Harmonie et enchaînements** | Hypothèses d'accords, progression, fonction, tonalité locale, cadences, Tonal Pitch Space, Spiral Array ; tests sur vérité musicale annotée. | **music21 + Partitura actifs sur fixtures ; vérité musicale externe à venir** |
| **Prochain** | **S3 — Motifs, formes, tension** | Répétitions/transformations, structure hiérarchique, mémoire et modèles temporels Lerdahl/Farbood. | À faire |
| **Après** | **S4 — Fusion des mécanismes** | Entropie avant l'événement, surprise à l'événement, tension/résolution et interactions, ablations. | À faire |
| **Après** | **S5 — Émotions humaines** | Relations calibrées aux labels et courbes **humaines** avec baselines, séparations d'œuvres et contrôles négatifs. | **Protocole EMOPIA et évaluateur construits ; pas de classificateur entraîné ni de score humain** |
| **Après preuve de besoin** | **S6 — Corpus ciblé** | Sélection par requirements de S0–S5, peu de MIDI fiables, couverture/erreurs/biais documentés. | Études de sources déjà réalisées ; sélection à redéfinir |
| **Recherche appliquée** | **S7 — Bach, Chopin, puis pop** | Analyses explicables de pièces identifiées, confrontées à la théorie et aux évaluations humaines quand elles existent. | À faire |
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
| [XMIDI / XMusic](https://github.com/xmusic-project/XMIDI_Dataset) | 108 023 MIDI, 11 classes émotionnelles humaines et genre | Étiquette du **morceau**, titre/artiste non fournis dans les noms |
| [EMOPIA](https://annahung31.github.io/EMOPIA/) | 1 087 extraits de piano, MIDI et audio, quadrants émotionnels annotés | Piano pop, classes par **extrait**, pas secondes individuelles |
| [DEAM](https://cvml.unige.ch/databases/DEAM/) | 1 802 extraits/chansons, valence/activation dans le temps | Principalement audio, appariement MIDI à créer prudemment si nécessaire |
| [PMEmo](https://github.com/HuiZhangDB/PMEmo) | 794 chansons, annotations et activité électrodermale | Audio ; physiologie et émotion déclarée distinctes |
| MIDI Bach/Chopin autorisés | Analyses de tonalité, motifs, cadences et forme, études de cas compréhensibles | Domaine public de la composition ≠ licence de chaque transcription MIDI |
| [MetaMIDI](https://github.com/Metacreation-Lab/MetaMIDI-Dataset), [GigaMIDI](https://github.com/Metacreation-Lab/GigaMIDI-Dataset) | Identités et caractéristiques déjà calculées, pour phase d'enrichissement | Accès/licences, identité de l'arrangement et qualité non garantis |

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

Le projet n'a actuellement **aucune** preuve de prédiction émotionnelle
locale validée. Ne pas confondre les audits d'instrumentation, une jointure
MD5 et une validation psychologique.

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
  parseur est testé sans présenter une fixture comme résultat Java réel.
- `anamu/idyom_guardrails.py` : séparation stricte des répertoires,
  empreintes SHA-256 pour éviter les doublons exacts, blocage des MIDI EMOPIA
  en préentraînement, budget de fichiers et manifestes vérifiables.
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
- [x] Fournir un lanceur des 246 caractéristiques **jSymbolic original**
  (sorties en fenêtres temporelles), sans prétendre l'avoir exécuté.
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
- [x] Ajouter au **workflow existant** un test Java facultatif de la
  distribution jSymbolic 2.2 officielle, avec contrôle SHA-256 public et
  artefact de résultats, sans télécharger l'outil à chaque push.
- [ ] Faire réellement tourner l'IDyOM upstream (SBCL, Quicklisp, SQLite),
  sur un apprentissage séparé du jeu de test, et analyser les résultats.
- [ ] **Exécuter jSymbolic réel**, puis inventorier et dédoublonner ses
  features temporelles (rythme, expression, densité, texture, instrumentation).
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
