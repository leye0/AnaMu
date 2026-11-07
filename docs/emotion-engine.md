# AnaMu — Moteur d'émotion : inventaire académique et protocole de preuve

**7 novembre 2026 — document vivant, à couverture maximale sans doublons conceptuels.**

## Position scientifique

Nous voulons réunir **tous les mécanismes algorithmiques distincts** et
raisonnablement exploitables en musique symbolique, plutôt qu'élire une unique
« théorie des émotions ». On conserve plusieurs **modèles concurrents** d'un
même mécanisme pour les comparer et mesurer leur complémentarité. On ne
multiplie pas artificiellement les signaux en donnant des noms émotionnels à
des statistiques corrélées. Le MIDI brut est une entrée directe ; Demucs et
le traitement audio sont reportés.

Les mécanismes et les **émotions déclarées par des humains** sont deux étages
différents : une progression modulante, une surprise élevée ou une dissonance
ne prouvent pas qu'un auditeur ressent la peur, la tristesse ou la joie.

## Inventaire exhaustif **de départ** (à enrichir par veille bibliographique)

Statuts : **actif** = code + test de fonctionnement local ; **adaptateur** =
lecture de sorties/configuration, moteur original non exécuté localement ;
**candidat** = recherche/implémentation ou reproduction à réaliser. Les noms
de bibliothèques ne suffisent pas à valider un mécanisme psychologique.

| Mécanisme non redondant | Théories / outils existants | Observables apportés | Statut |
|---|---|---|---|
| **M1 — attentes mélodiques statistiques** | Pearce, **IDyOM original** + [py2lispIDyOM](https://github.com/xinyiguan/py2lispIDyOM) | Entropie *avant* la note, contenu informationnel *après*, adaptation/style, points d'attente | **adaptateur** CSV + lanceur officiel optionnel ; Lisp non exécuté |
| **M2 — attentes mélodiques structurelles** | Narmour, Schellenberg, Implication-Realization ; **melody-features 1.3.3** | Taille/direction d'intervalles, continuation, inversion, fermeture | **actif partiellement** : cinq scores Narmour calculés sur triplets temporels ; pas encore de prédiction avant la note ni de validation perceptive |
| M3 — attente harmonique | IDyOM multi-viewpoints, apprentissage sur séquences d'accords | Surprise harmonique **distincte de** surprise mélodique | candidat ; exige accord/voix validés |
| **M4 — distance et déplacement tonal** | Chew Spiral Array, Herremans & Chew *Tension Ribbons*, **Partitura** | Cloud diameter, momentum, tensile strain en **courbe temporelle** | **actif** sur MIDI de piano polyphonique de test |
| **M5 — tonalité/statut modal** | Krumhansl–Schmuckler (implémenté par **music21**), alternatives Temperley | Hypothèses de tonique, mode, accord tonal estimé | **actif** K-S global ; modèles alternatifs candidats |
| **M6 — fonctions et transitions d'accords** | music21 `chordify`, `romanNumeralFromChord`, Harmonic Function | Sonorités, degrés romains hypothétiques, fonctions, séquences | **actif** sonorités + degrés ; fonctions et cadences à valider |
| M7 — attraction/prolongation hiérarchique | Lerdahl *Tonal Pitch Space*, Lerdahl & Krumhansl | Attraction tonale, distance régionale, force des résolutions | candidat ; ne pas confondre avec M4 |
| M8 — cadences et résolutions | Règles tonales, analyse de fonction, modèles de clôture | Préparation, dominantisation, retard, résolution, stabilité restaurée | candidat ; gold set manuel nécessaire |
| M9 — motifs et transformations | Analyses de motifs, séquences, Lerdahl–Jackendoff ; descripteurs FANTASTIC/SIMILE/MUST de `melody-features` | Retour attendu, identité/variation, inversion, augmentation, diminution | **partiel** : descripteurs mélodiques globaux ; détection structurelle complète candidate |
| M10 — groupes, phrases et forme | GTTM (Lerdahl–Jackendoff), arbres de structure | Segmentation, regroupement, anacrouses, apogées, clôtures | candidat ; ambiguïtés autorisées |
| M11 — métrique et accents | Théorie métrique, outils `music21.meter`, `jSymbolic` et `melody-features` | Accent fort/faible, synchronisme des entrées, changements de mètre | **partiel** : mesures mélodiques ; polyphonie à intégrer |
| M12 — syncopation / groove | Longuet-Higgins/Lee, métrique, `jSymbolic` et `melody-features` | Déplacement d'accent, tension rythmique locale, swing | **partiel** : descripteurs rythmiques monophoniques ; groove polyphonique candidat |
| **M13 — densité / polyphonie / texture** | **jSymbolic original 2.2** (analyse MIDI/MEI) | Couplage des voix, onsets/s, épaisseur, registre, instrumentation | **extraction réelle exécutée** sur MIDI polyphonique fictif ; validité perceptive à tester |
| M14 — dynamique / accent / jeu | Vélocité, notes tenues, articulation, `jSymbolic`/Partitura | Croissance, accent, contraste, nuances, respiration | candidat ; vélocité MIDI ≠ volume acoustique |
| M15 — dissonance / rugosité symbolique | Théories de consonance, classes d'intervalles | Intervalles verticaux instables, changements de dissonance | candidat ; timbre et acoustique peuvent manquer |
| M16 — conduite des voix / contrepoint | `music21.voiceLeading`, règles contrapuntiques | Continuité, voix contraires, retards, résolutions internes | candidat ; exige séparation de voix fiable |
| M17 — tension multimodale *au cours du temps* | Farbood (2012), modèles de mémoire temporelle | Accumulation, pics, pente, relâchement, inertie | candidat ; distinct des rubans purement tonals M4 |
| M18 — interaction incertitude × surprise | Cheung et al. (2019) | `H(t−) × IC(t)`, dépendances non linéaires | candidat ; étude du **plaisir**, pas un décodeur émotionnel universel |
| M19 — psychologie des attentes | Meyer (1956), Huron ITPRA (2006) | Hypothèses sur événements prévus, différés, violés, évalués | **cadre** ; états mentaux non directement observables |
| M20 — mémoire et familiarité stylistique | IDyOM long/short-term, réexposition, apprentissage de style | Modèles pré-entraînés vs adaptation causale, familiarité locale | candidat ; ne pas préentraîner sur test |
| M21 — styles et signatures de compositeurs | jSymbolic, music21, comparaisons normalisées | Profil stylistique, contraintes et références interprétables | candidat ; identité ≠ émotion |
| M22 — trajectoires affectives | Circumplex valence/activation, études de tension et plaisir | Courbe et résumé émotionnels **appris à partir de labels humains** | futur ; aucun modèle validé |
| M23 — désaccord et pluralité d'annotateurs | Psychométrie, modèles ordinal/probabilistes | Distribution des jugements et incertitude inter-humains | futur ; dépend des votes publiés |

**Critère de non-redondance :** deux sorties portant sur *le même signal*
(p. ex. moyenne et maximum de `cloud_diameter`) sont des agrégations
différentes d'une seule famille ; deux implémentations d'attente mélodique
sont des modèles à comparer, **pas** automatiquement deux causes
émotionnelles indépendantes. Éliminer les duplications d'information avec
tests d'ablation et corrélation conditionnelle **sur validation**, jamais sur
test. Tous les candidats demeurent au registre tant qu'ils n'ont pas été
examinés et rejetés avec justification.

## Logiciels libres existants d'abord

1. **[Partitura](https://partitura.readthedocs.io/en/latest/_modules/partitura/musicanalysis/tonal_tension.html)** : `estimate_tonaltension` **réel**. Notre adaptateur `anamu.theory_features.partitura_tension()` lit le MIDI local et retourne trois rubans temporels en secondes, paramètres, provenance, limites. Risques : tonalité et orthographe de notes estimées ; pas de localisation validée de modulation.
2. **[music21](https://music21.org/music21docs/)** : `KrumhanslSchmuckler`, `chordify`, `romanNumeralFromChord`, depuis un vrai fichier MIDI. Notre adaptateur `music21_harmonic_hypotheses()` renvoie les sonorités et les hypothèses romaines. Attention aux notes de passage et aux temps de performance convertis en partition estimée.
3. **[IDyOM](https://github.com/mtpearce/idyom)** : moteur original Common Lisp, GPLv3 ; [py2lispIDyOM](https://github.com/xinyiguan/py2lispIDyOM), interface Python MIT, publiée dans JOSS (2022). `scripts/run_original_idyom.py` prépare/lance **facultativement** une expérience réelle ; `read_idyom_export()` importe ses exports CSV, et le nouvel **`anamu.idyom_dat.read_idyom_dat()` importe directement le `.dat` natif** (séparé par espaces) : toutes les familles de *surprisal*/entropie réellement présentes (ex. conjoint, hauteur, onset), distributions de prédiction événementielles, gain d'information, groupement par morceau, noms cités et `NA` conservés. Le convertisseur `scripts/import_idyom_dat.py` exporte du JSON analysable ; `--keep-original-fields` conserve en option **toutes les colonnes originales** sans supposer leurs unités. Le parseur a été confronté au schéma et à deux lignes du [vrai `.dat` de référence fourni par les auteurs](https://github.com/xinyiguan/py2lispIDyOM/tree/master/tests/experiment_history/25-05-22_14.10.29/experiment_output_data_folder) ; **cela n'est pas une exécution Lisp locale**. Les onsets d'IDyOM sont en unités natives de 24 par noire : les convertir aveuglément en secondes à tempo constant serait erroné si le tempo change. **Aucune exécution SBCL ni validation des résultats IDyOM n'a encore été réalisée.** Le lissage n-gramme local est une simple baseline indépendante. `anamu.idyom_guardrails` refuse dorénavant les recouvrements SHA-256 exacts train/test, les échantillons EMOPIA dans le préentraînement et les lots démesurés ; un test d'EMOPIA explicite exige un opt-in. Cela ne détecte pas **les reprises ou transpositions** et ne transforme pas des données de test en données d'entraînement autorisées. Le lanceur demande également de nouveaux résultats `.dat` non vides avant de déclarer une exécution réussie.

   **Blocage de l'exécution locale IDyOM :** cet environnement ne dispose pas de SBCL, de Quicklisp ni de la base SQLite IDyOM initialisée. La fonction `melody_features.idyom.interface.install_idyom()` existe, mais dans la *wheel* 1.3.3 vérifiée ici le script `install_idyom.sh` qu'elle référence n'est pas distribué au chemin attendu. Ne pas la considérer comme une installation reproductible réussie sans contrôle et sans consulter l'installateur source. L'installation Lisp restera isolée d'EMOPIA et exécutée dans un environnement borné.
4. **[jSymbolic](https://jmir.sourceforge.net/jSymbolic.html)** (Java) :
   **246 caractéristiques uniques / 1 497 valeurs possibles** en version 2.2,
   dont rythme, dynamique, texture, polyphonie, instrumentation, mélodie,
   accords et registre. `scripts/run_jsymbolic.py` appelle le **vrai** Java
   avec mémoire/temps bornés pour calculer des descripteurs **fenêtrés**.
   **La CLI stable 2.2 exige explicitement deux chemins XML** (valeurs et
   définitions), comme prouvé par `java -jar jSymbolic2.jar -help` dans
   [l'essai réel 42415157374](https://github.com/leye0/AnaMu/actions/runs/42415157374).
   Le [manuel GitHub de la branche de développement 2.3](https://github.com/DDMAL/jSymbolic2/blob/master/manual/commandline_files/commandline.html)
   n'en exige qu'un : **les deux syntaxes ne sont pas interchangeables**.
   Notre adaptateur a été remis en conformité avec le binaire stable 2.2.

   `anamu.jsymbolic_ace` lit les vrais formats **ACE XML 1.1** pour les valeurs
   **et les définitions** : trajectoires, mesures globales, vecteurs,
   description d'origine de chaque feature et nombre de dimensions. Il
   conserve les timestamps manquants comme `null`. Les DTD internes
   rencontrées dans les [exemples originaux](https://github.com/DDMAL/jSymbolic2/blob/master/manual/api_files/ExtractedFeatureValues.xml)
   sont acceptées **uniquement si elles correspondent à une déclaration connue**,
   retirées avant analyse ; les entités et DTD arbitraires sont refusées.

   Le workflow standard permet un test Java facultatif sur MIDI fictif.
   L'archive stable officielle de 19,6 Mo est [vérifiée par SHA-256](https://sourceforge.net/projects/jmir/files/jSymbolic/jSymbolic%202.2/jSymbolic_2_2_user.zip/download)
   (`e1686a6bb1133cc21fb4678185d81e5e0a322b371ac713cbaf5fd9b69e2396cb`).
   Deux premiers essais ont échoué par transfert ; les deux suivants ont
   téléchargé et validé l'archive. Le cache GitHub est désormais alimenté.
   **Résultat réel confirmé :** [exécution GitHub Actions 42415633459](https://github.com/leye0/AnaMu/actions/runs/42415633459),
   rapport `original_java_executed` : **6 fenêtres temporelles**, **226 noms
   de features observés**, **226 définitions officielles lues** sur le MIDI
   synthétique original. Les 226 correspondent aux features effectivement
   extraites sous cette configuration et non à la totalité théorique des
   246 features disponibles. Le rapport `jsymbolic-original-smoke-summary`
   est conservé comme artefact pendant sept jours. **Aucune prédiction
   émotionnelle ni validation humaine n'a été effectuée par cet essai.**
5. **[EMOPIA_cls](https://github.com/SeungHeonDoh/EMOPIA_cls)** : code d'un classificateur sur EMOPIA. À comparer comme **baseline externe**, avec vérification impérative des morceaux d'entraînement utilisés par ses poids. Pas de garantie de test disjoint pour un modèle pré-entraîné inconnu.
6. **[melody-features 1.3.3](https://dmwhyatt.github.io/melody-features/)**, Whyatt (*Computational Features for Symbolic Melody Analysis*, [prépublication 2026](https://arxiv.org/abs/2608.19061)) : boîte à outils Python publiée regroupant et **réimplémentant** des familles de FANTASTIC, SIMILE, MUST, MIDI Toolbox, jSymbolic, Partitura, Narmour et d'autres. Notre adaptateur `anamu.melody_toolbox.extract_melody_toolbox()` exécute **réellement** `get_all_features(..., skip_idyom=True)` sur les pistes MIDI monophoniques admissibles. Sur une fixture de neuf notes : **278 colonnes de descripteurs**, rangées dans **12 familles** ; ce nombre ne correspond **ni à 278 mécanismes indépendants**, ni à une évaluation des émotions. La bibliothèque fournit aussi cinq règles de Narmour, que nous invoquons sur chaque **triplet successif** pour obtenir une trajectoire d'observations musicales datées. C'est une implémentation publiée *consolidée*, **pas** une exécution des outils originaux FANTASTIC, IDyOM ou jSymbolic Java. Les sources et paramètres doivent être comparés aux implémentations originales avant toute revendication de fidélité. **Uniquement monophonie non chevauchante** : elle ne convertit pas magiquement un piano polyphonique en mélodie principale.

### Passage exact des notes MIDI à l'axe temporel

- `anamu.tempo_map.MidiTempoMap` lit les métaévénements MIDI `set_tempo` sur toutes les pistes, calcule des segments de vitesse et convertit correctement **quarts de mesure / beats → secondes de performance**, y compris lorsque le tempo change pendant une phrase. Aucun arrondi fixe à « 120 BPM ».
- Chaque candidat conserve piste, canal, nombre de notes, début/fin, 12 familles de descripteurs et valeurs absentes explicites (`null`), avec provenance et **la mention que la mélodie principale n'est pas vérifiée**.
- `narmour_triplet_realizations` est daté au **début de la troisième note** de chaque triplet. Ces cinq scores sont des **mesures rétrospectives d'une réalisation**, pas une anticipation psychologique prouvée ni une prédiction émotionnelle.
- Les caractéristiques dépendant du corpus utilisent par défaut la collection de **903 mélodies traditionnelles** distribuée avec `melody-features` ; son contenu, ses droits et d'éventuels recouvrements doivent être audités avant entraînement ou publication. `skip_idyom=True` empêche de prétendre avoir exécuté IDyOM original.
- **Droits à conserver séparés :** le code `melody-features` est principalement MIT (certains composants hérités sont Apache-2.0), tandis que la conversion MIDI **Essen Folksong Collection** distribuée dans le paquet est **CC BY-SA 4.0**. Ne pas confondre les licences du logiciel, des corpus embarqués et des MIDI de notre étude ; voir le [NOTICE et le tableau des licences du dépôt officiel](https://github.com/dmwhyatt/melody-features#license).
- La grande quantité de variables corrélées exige une sélection par **familles scientifiques**, un regroupement des doublons et des ablations **sur validation** ; conserver les variables brutes pour rendre cette sélection contrôlable.

## Chaîne de preuve et contrats

```text
MIDI brut + empreinte + droits + provenance
    ├─ Partitura  → trajectoires de tension tonale
    ├─ music21    → sonorités, tonalité et accords hypothétiques
    ├─ melody-features → ~278 caractéristiques monophoniques et Narmour triplets
    ├─ IDyOM réel → attente, surprisal et entropie
    ├─ jSymbolic original → rythme, articulation, texture, dynamique (Java réel vérifié sur fixture)
    └─ modèles théoriques ciblés → modèles de motifs, cadences, mémoire (à venir)
             ↓ (chaque moteur conserve version, unités, paramètres, `unknown`)
      alignement temporel + fusion + ablations (à construire)
             ↓
      estimateur émotionnel entraîné sur des œuvres autorisées (à construire)
             ↓
      **test EMOPIA tenu hors entraînement** — labels humains seulement ici
```

Les sorties devraient être : événements temporels natifs, valeurs numériques
avec leurs unités, hypothèses incertaines, flags d'échec, **aucune classe
émotionnelle déduite implicitement**. Ne pas créer une « courbe valence à
chaque note » depuis un label unique d'extrait.

## EMOPIA : notre banc d'essai, pas une oracle

- Source officielle : [EMOPIA](https://github.com/annahung31/EMOPIA) ; 1 087
  extraits de 387 titres de piano pop, quadrants d'émotion perçue assignés
  au **niveau de l'extrait** par quatre annotateurs dans l'étude. Les clips
  ne fournissent pas une vérité temporelle seconde par seconde.
- La convention de fichiers `Q{1..4}_{youtube_id}_{segment}.mid`, utilisée
  aussi dans le lecteur MusPy, permet de récupérer **label, chanson et
  segment**. `anamu.emopia.inventory_emopia()` conserve empreinte, provenance,
  rejets et doublons.
- **Protocole principal, externe** : `hold_out_entire_emopia()` garde **100 %
  des clips EMOPIA pour le test**. Entraîner et figer le système sur d'autres
  sources indépendantes. Ni les labels, ni les MIDI, ni les mêmes compositions
  dans d'autres arrangements ne doivent contaminer l'apprentissage.
- **Protocole secondaire, interne** : `assign_song_splits()` permet des
  expériences dédiées à EMOPIA, en séparant toutes les sections d'une même
  vidéo entre train/validation/test (seed reproductible). Le score résultant
  est une validation **interne sur un sous-ensemble**, pas une preuve externe.
- Une *œuvre reprise deux fois* peut posséder plusieurs YouTube IDs : le split
  par vidéo ne prouve pas une séparation parfaite **des compositions**. Il
  faudra détecter les reprises et versions doublées avant la publication de
  scores définitifs.
- `anamu.emotion_evaluation.evaluate_quadrants()` score **seulement** validation
  ou test : précision, macro-F1 quatre classes fixes, couverture, abstentions,
  matrice de confusion et précision moyenne par chanson. La baseline naïve
  n'apprend que les classes du split train ; pas de fuite par clip.
- Pour le protocole interne, une répartition aléatoire des groupes n'est pas
  nécessairement stratifiée :
  regarder les effectifs **par quadrant et split** ; répéter sur des seeds
  préenregistrées pour robustesse, sans choisir le meilleur seed après coup.
- Les sorties des moteurs (sans label) doivent être calculées **avant**
  l'association aux annotations émotionnelles. Pour le protocole externe,
  toute calibration et sélection d'hyperparamètres s'effectue **hors EMOPIA**.
  En interne, les choix s'arrêtent à la partition **validation**. Ne toucher
  au test que pour un rapport final unique et versionné.
- EMOPIA est réservé à la recherche non commerciale par sa licence
  [CC BY-NC-SA 4.0](https://github.com/annahung31/EMOPIA#license).
  Si le générateur devient commercial, revoir l'admissibilité des données
  d'entraînement, des poids préentraînés et des dérivés.

### Premières commandes reproductibles

```bash
python -m pip install 'mido>=1.3,<2' 'partitura>=1.8,<2' 'music21>=9,<12'
python -m unittest discover -s tests -p 'test_emotion_research.py' -v
python -m scripts.extract_tonal_tension ./piano.mid > tension.json
python -m scripts.extract_harmony ./piano.mid > harmony.json
python -m pip install 'melody-features==1.3.3'
python -m scripts.extract_melody_features ./midi-avec-piste-monophonique.mid > melodia.json
python -m unittest discover -s tests -p 'test_melody_toolbox.py' -v
python -m scripts.run_original_idyom --test ./test-midis --pretrain ./train-midis --history ./idyom-history
python -m scripts.run_original_idyom --test ./test-midis --pretrain ./train-midis --history ./idyom-history --execute
python -m scripts.import_idyom_dat ./idyom-history/experiment_output_data_folder/original.dat --json-out ./idyom-events.json --keep-original-fields
python -m scripts.run_jsymbolic ./piano.mid --jar ./jSymbolic/jSymbolic2.jar --out ./jsymbolic-results --window-seconds 5 --overlap 0.5
python -m scripts.run_jsymbolic ./piano.mid --jar ./jSymbolic/jSymbolic2.jar --out ./jsymbolic-results --window-seconds 5 --overlap 0.5 --execute --json-out ./jsymbolic-results/parsed.json
python -m scripts.emopia_benchmark ./EMOPIA_2.2 --protocol external --manifest-out ./emopia-external.jsonl
python -m scripts.emopia_benchmark ./EMOPIA_2.2 --protocol external --predictions ./predictions.jsonl
python -m scripts.emopia_benchmark ./EMOPIA_2.2 --protocol internal --seed 2026
```

### Ce qu'il faut encore prouver

- **Dès maintenant :** tester la stabilité des rubans et analyses harmoniques
  sur diverses pièces, valider la détection des accords sur un gold set
  indépendant, **étudier les 226 caractéristiques jSymbolic réellement
  extraites et leur robustesse**, et **faire réellement tourner IDyOM**
  original avec préentraînement sans fuite. Le *smoke test* Java n'établit
  pas l'exactitude musicale ni émotionnelle de ces caractéristiques.
  Vérifier sur mélodies annotées les mesures Narmour et les 278 colonnes
  réimplémentées par `melody-features` ; documenter les familles qui se
  recouvrent avec Partitura ou jSymbolic avant leur fusion.
- **Puis :** aligner mélodie, accords, tension, groove, motifs et variables
  dynamiques sur une grille temporelle sans masquer les erreurs de conversion.
- **Puis :** apprendre un lien entre mécanismes et émotion, avec ablations,
  interaction, refus (`unknown`) et une vraie comparaison avec EMOPIA_cls.
- **Enfin :** évaluer une version figée sur des chansons et reprises inédites ;
  Bach/Chopin illustreront les mécanismes mais n'apporteront des labels
  affectifs que si des humains les annotent.

**État réel de la recherche :** prototypes de mécanismes existants et protocole
d'évaluation testés sur fixtures, et bibliothèque académique `melody-features`
réellement exécutée sur MIDI monophonique avec chronologie Narmour ; **aucun
score empirique d'émotion humaine** et
aucune « super-machine validée » annoncés à ce stade.
