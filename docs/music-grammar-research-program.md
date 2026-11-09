# AnaMu Grammar — programme d'analyse musicologique formelle

**Direction proposée le 9 novembre 2026.** Statut : **spécification de recherche**, pas moteur grammatical déjà implémenté ni résultat expérimental. Ce document complète les expériences antérieures (émotion, tension, attente) et définit désormais le **cœur recherché** d'AnaMu : expliquer l'organisation d'une œuvre, sa partition, sa réalisation et sa matière sonore par des relations hiérarchiques vérifiables, avec le minimum d'apprentissage statistique.

## 1. Ambition et critères scientifiques

AnaMu doit produire, pour un morceau nouveau, une **analyse universitaire inspectable** : événements, voix, métrique, rythmes, hauteurs, harmonie, motifs, variations, phrases, forme, instrumentation, orchestration, dynamique, tempo, articulation et expression. La grammaire n'est **ni** un classificateur d'émotions **ni** une seule succession d'accords. Elle décrit les objets et opérations musicales, et les preuves qui soutiennent les interprétations concurrentes.

Règles de conception non négociables :

1. **Fidélité des sources** : les événements reçus sont conservés et référencés ; chaque dérivation est réversible vers les événements d'origine ou signalée comme non réversible.
2. **Observation ≠ hypothèse ≠ annotation** : MIDI vélocité, nuance *forte* écrite, niveau acoustique et intensité perçue sont quatre objets distincts. Une hypothèse harmonique ne devient jamais un fait MIDI.
3. **Temps pluriel** : temps de partition (positions métriques en fractions exactes), temps interprété (secondes, changements de tempo, rubato), temps du signal (échantillons). Conserver des alignements avec incertitude, pas une conversion universelle inventée.
4. **Polyphonie native** : événements successifs, simultanés, chevauchants et voix indépendantes. Un morceau n'est pas par défaut une liste monophonique.
5. **Variantes d'analyse** : préserver les interprétations candidates et leurs preuves dans une forêt/graphe ; `unknown` est une sortie valide. Ne pas fabriquer de confiance probabiliste si aucun calibrage n'existe.
6. **Règles formulées comme des données** : pas de handlers spécifiques à Bach, au jazz ou à un genre. Schémas abstraits et opérateurs musicaux portés par un moteur réutilisable.
7. **Théorie et algorithme séparés** : chaque règle identifie sa publication primaire, son domaine de validité, les équations effectivement exécutées et les écarts d'implémentation.
8. **Évaluation par capacité** : une annotation de segmentation ne valide pas la tonalité ; une vélocité MIDI ne valide pas le volume entendu ; la surprise d'une note ne valide pas l'émotion.

## 2. Trois représentations compatibles, jamais fusionnées aveuglément

| Vue | Ce qui y est effectivement observé | Ce qui manque fréquemment |
|---|---|---|
| **Partition** : MusicXML, MEI, notation | Voix/portées, hauteurs orthographiées, métrique, durées, silences, liaisons, articulations et indications `p`, `f`, cresc., rit., instrumentation écrite | Timing exact d'exécution, acoustique, dosage réel de la nuance |
| **Interprétation** : MIDI de performance | Onset/offset, vélocités, pédales, contrôleurs, parfois tempo, microdécalages et synchronisation des voix | Niveau sonore réel, identité certaine du timbre ; un `set_tempo` n'est pas automatiquement un *rubato* musical |
| **Enregistrement** : audio | Intensité acoustique mesurée, enveloppes, spectre, réverbération, texture et durées réelles | Notes, voix, instruments et causes exactes des sons sans transcription/alignement incertains |

Chaque item porte `source_id`, `source_kind`, `span`, `timebase`, `provenance`, `method_version`, `parameters`, `status` (`measured`, `encoded`, `annotated`, `inferred`, `unknown`) et les références aux observations justificatives.

**Conséquence immédiate** : la nouvelle direction inclut une **branche acoustique future**, mais aucun modèle de timbre ou outil audio coûteux n'est requis pour bâtir la grammaire de partition. Les couches reconnaissent explicitement les entrées absentes.

## 3. Ontologie des aspects : ne pas confondre disponibilité et vérité

| Famille | Éléments grammaticaux et opérateurs envisagés | Sources et validation admissibles |
|---|---|---|
| Événements | Note, silence, attaque, relâchement, tenue, ornement, simultanéité | MIDI, MusicXML, MEI ; tests de conservation des événements |
| Hauteur et registre | Intervalle, direction, contour, registres, enharmonie, classes de hauteur | Notation et MIDI ; transposition contrôlée |
| Rythme et métrique | Pulsation, mètre, accent, syncope, polymètre, polymétrie, polyrythmie, tuplets | MusicXML/MEI, GTTM métrique, ASAP beats |
| Tempo et mouvement | Courbe BPM, ritardando, accelerando, rubato, césure, fermata, *agogique* | MEI/partition pour directives, MIDI de performance ou alignement ASAP/MazurkaBL pour réalisation |
| Nuances et volume | `p`/`mf`/`ff`, cresc./dim., vélocité, CC7/CC11, dynamique locale, amplitude/loudness | MEI + MIDI pour indications et contrôles ; audio/MazurkaBL pour volume mesuré |
| Articulation et toucher | Staccato, legato, accent, slur, pédale, détaché, durée relative et chevauchement | MEI, MusicXML, score ↔ performance ASAP/MAESTRO |
| Harmonie | Ensemble vertical, accord candidat, renversement, fonction, progression, modulation, dissonance | `music21`, DCML ; distinguer analyse experte et hypothèses automatiques |
| Conduite des voix | Voix distinctes, parallélismes, croisements, mouvements contraires, suspensions | Partitions multi-voix ; contrôles théoriques `music21.voiceLeading` |
| Motifs | Identité, imitation, transposition, inversion, rétrogradation, fragmentation, augmentation/diminution | Égalité/transformation structurelle vérifiable, puis annotations de motifs si acquises |
| Regroupement | Cellule, geste, motif, proposition, phrase, période, frontières concurrentes | GTTM GroupingXML, LBDM, SALAMI à l'échelle audio |
| Hiérarchie | Accents métriques, importance des événements, branches de prolongation, développements | GTTM Metrical/Time-span/ProlongationalXML |
| Forme longue | Répétition, variation, contraste, reprise, exposition, développement, refrain, coda | Analyse de structures répétées, SALAMI pour frontières ; noms de forme = hypothèses |
| Texture et densité | Monodie, homophonie, polyphonie, couches, doublures, entrée/sortie des parties | Partition/MIDI pour organisation ; audio pour mixture réelle |
| Instrumentation et orchestration | Programmes MIDI, instruments notés, registres, rôles, combinaisons d'ensembles | MusicXML/MEI, MIDI programmes comme indices, audio et OpenMIC pour présence de familles instrumentales |
| Timbre et enveloppe | Attaque/décroissance/sustain/release, spectre, brillance, rugosité, bruit, vibrato | Audio/Essentia ; **pas** fiable depuis la seule étiquette MIDI `program_change` |
| Expression et interactions | Décalages entre voix, microtiming, arcs dynamiques, expression de phrase, pédales | ASAP, MAESTRO, MazurkaBL ; comparaison score ↔ interprétation |
| Style et langage | Régularités harmoniques, métriques, mélodiques, instrumentales par répertoire | Métadonnées vérifiées, règles et comptages sur œuvres distinctes ; ne pas déduire un genre comme vérité intrinsèque |
| Production et espace | Balance, panorama, réverbération, dynamique de mixage, distance, spatialisation | Enregistrement/multitracks, si disponibles ; hors portée du MIDI de partition |
| Voix chantée et texte | Prosodie, syllabes, articulation textuelle, relation accents/rythme | Notation paroles/phonèmes et sources vocales séparées ; pas supposées présentes |

**Exhaustivité contrôlée** : cette ontologie est un inventaire des domaines à traiter, **pas** l'affirmation qu'ils sont déjà implémentés. On peut enrichir les familles sans changer les opérations primitives.

## 4. Grammaire formelle : graphe d'événements et arbres coexistants

Une simple CFG sur une chaîne de notes serait inadéquate : le temps musical comporte des chevauchements, plusieurs voix et des dépendances non emboîtées. Proposer une **grammaire typée à contraintes**, produisant un **graphe temporel d'évidence** et plusieurs **arbres d'analyse** spécifiques à chaque axe.

### 4.1 Primitives indépendantes du style

- `SEQUENCE(a,b,...)` — ordre temporel, sans supposer de silence entre événements.
- `PARALLEL(a,b,...)` — simultanéité ou chevauchement, avec offsets exacts.
- `ALIGN(a,b,relation)` — relation entre pulsation, score, performance, son et voix.
- `GROUP(span, members, role)` — unité pouvant inclure d'autres groupes.
- `TRANSFORM(source, target, operation, parameters)` — transposition, inversion, compression/augmentation rythmique, fragmentation, ornementation, déplacement d'accent, changement dynamique ou timbral, selon les attributs disponibles.
- `DEPEND(a,b,relation)` — lien structurel non nécessairement adjacent : prolongation, réponse, préparation, résolution, parenté motivique, fonction de voix.

Les **rôles** (cadence, phrase, thème, contrechant, tension, réponse) sont des *hypothèses dérivées* avec justification, non des terminaux toujours imposés. Les arbres de groupement, de métrique et de réduction ne sont pas nécessairement le même arbre.

### 4.2 Esquisse de représentation, illustrative seulement

```text
observed:
  notes: [...]                        # IDs et horodatages sources
  tempo_events: [...]                 # directives écrites ou MIDI natif
  controllers: [...]                  # CC7, CC11, CC64, vélocités

hypotheses:
  - id: motif_A
    type: GROUP
    members: [n11, n12, n13]
    evidence: [intervals_2_2, rhythmic_ratio_1_1_2]
  - id: motif_A_prime
    type: TRANSFORM
    source: motif_A
    operation: transpose
    parameters: {semitones: 7}
    target: [n29, n30, n31]
    evidence: [same_intervals, same_relative_durations]
  - id: phrase_candidate_1
    type: GROUP
    members: [motif_A, motif_A_prime, closing_event]
    evidence: [metrical_boundary, rest, cadence_candidate]
    alternatives: [phrase_candidate_2]
```

### 4.3 Grammaire induite : minimalisme, pas ML opaque

1. Générer des candidats par règles publiées et transformations exactes : suffixes répétés, intervalles normalisés, rythmes proportionnels, similarité de groupes, seuils explicités.
2. Réunir des contextes équivalents et abstraire des variables typées : `Motif(x)`, `Transpose(x,n)`, `Phrase(children)`.
3. Choisir les règles qui raccourcissent une description selon un coût **MDL** explicite (bits de grammaire + bits d'encodage résiduel), avec pénalité de complexité.
4. Vérifier sur des œuvres *exclues* de l'induction, des permutations contrôlées et des genres variés. Une compression sur le corpus d'apprentissage ne suffit pas.
5. Préserver les conflits et les analyses de rechange dans une forêt partagée, avec budget de calcul borné. Les scores d'économie descriptive ne sont pas des probabilités psychologiques.

Cette approche accepte des règles déclaratives académiques, des heuristiques vérifiables et des statistiques de fréquence simples, **sans réseau neuronal comme cœur du moteur**. Les extensions ML éventuelles restent interchangeables et clairement identifiées.

## 5. Fondements académiques et contrats de validation

| Référence primaire / corpus | Ce qu'elle apporte | Ce qu'elle **ne** valide **pas** |
|---|---|---|
| [Lerdahl & Jackendoff, *A Generative Theory of Tonal Music*](https://mitpress.mit.edu/9780262620499/a-generative-theory-of-tonal-music/) | Structure de groupement, métrique, réduction temporelle et prolongationnelle, règles de préférence | Ni toute la musique mondiale ni toute la musique populaire enregistrée |
| [Rohrmeier (2011), *Towards a generative syntax of tonal harmony*](https://doi.org/10.1080/17459737.2011.573676) | Règles de phrase et hiérarchie/recursion de l'harmonie diatonique | Pas une grammaire universelle du rythme, du timbre ou de l'interprétation |
| [GTTM Database — 300 analyses XML](https://gttm.jp/gttm/wp-content/uploads/2015/12/index.html) | Référence pour groupement, métrique, arbres *time-span* et prolongation ; MusicXML/HarmonicXML | Extraits, principalement monophoniques dans la conception de cette base ; ni grand format complet ni émotions |
| [Cambouropoulos (2001), LBDM](https://quod.lib.umich.edu/cgi/p/pod/dod-idx/local-boundary-detection-model-lbdm-and-its-application.pdf?c=icmc%3Bidno%3Dbbp2372.2001.021%3Bformat%3Dpdf) | Hypothèses locales de segmentation fondées sur l'écart/changement des paramètres mélodiques, lien étudié avec timing expressif | Pas une analyse complète des sections ni vérité harmonique |
| [DCML — corpus et conventions analytiques](https://doi.org/10.1038/s41597-025-04976-z) | Harmonie, fonctions, cadences structurées ; déjà exploré dans AnaMu | Pas de notes d'humeur ni d'analyse du son |
| [music21, analyse d'accords et de conduite des voix](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html) | Algorithmes et structures musicologiques réutilisables | Le résultat d'un appel de bibliothèque n'est pas automatiquement une annotation humaine |
| [MEI 5, expression, tempo et nuances](https://music-encoding.org/guidelines/v5/content/shared.html) | Modèle d'encodage de *tempo*, *dynam*, articulation, phrasé et directives d'interprétation | Une indication écrite n'est pas le mouvement sonore réellement exécuté |
| [ASAP (2020), 222 partitions / 1068 interprétations](https://zenodo.org/records/4245490) | Alignement MusicXML–MIDI–audio partiel, beats et downbeats ; étudier le tempo et le rubato relatif | Piano classique, et pas un jugement humain de « qualité grammaticale » |
| [MAESTRO, enregistrements et MIDI alignés](https://magenta.withgoogle.com/datasets/maestro) | Attaque, vélocité, pédales et son de piano, environ 200 h | Pas d'annotations de structure grammaticale et pas d'orchestration multi-instrument |
| [MazurkaBL, 2000 enregistrements de 44 œuvres](https://zenodo.org/records/1290763) | Trajectoires de temps, loudness et indications expressives alignées sur partitions | Famille limitée : mazurkas de Chopin ; enregistrements ≠ interprétations indépendantes d'œuvres |
| [SALAMI, annotations de structure](https://ddmal.ca/research/salami/annotation/) | Frontières/formes à deux granularités sur audio annoté | Pas de MIDI symbolique aligné garanti, ni labels de timbre/émotion |
| [OpenMIC-2018, instruments audio](https://research.atspotify.com/publications/openmic-2018-an-open-dataset-for-multiple-instrument-recognition) | Présence annotée de catégories d'instruments dans des extraits audio | Catégorie instrumentale ≠ fonction orchestrale, attaque, nuance ou forme |
| [Essentia, descripteurs du signal](https://essentia.upf.edu/documentation.html) | Spectre, enveloppe, loudness, rythme et descripteurs audio reproductibles | Un descripteur spectral n'est pas une catégorie émotionnelle ni instrumentale prouvée |

Avant toute acquisition : relever licence, disponibilité effective, structure des annotations, version, coût de calcul et partitions sûres. **Ne pas redistribuer les enregistrements ou les analyses sous une licence incompatible.** Les corpus sont des instruments de mesure sur des questions **distinctes**.

## 6. Tests de niveau universitaire : échecs explicites et témoins négatifs

**Invariants de représentation**

- Round-trip : conserver identités, offsets, parties, pistes, contrôleurs et tempo variable ; ne pas déplacer une note entre voix silencieusement.
- Deux notes simultanées et deux notes successives doivent produire des relations différentes ; traiter correctement les chevauchements partiels.
- Transposition uniforme : même schéma intervallique/transformation mais hauteurs absolues différentes.
- Changement global de tempo : la structure métrique en beats reste stable tandis que la durée physique change.
- Ralentissement *local* dans une performance : détecter la courbure temporelle sans prétendre qu'un simple méta-événement MIDI de tempo décrit les intentions musicales.
- Vélocité × gain MIDI × son : ne jamais les fusionner en un « volume » universel. Une partition sans audio garde `measured_loudness = unknown`.
- Instruments sans programmes, audio sans stems, tonalité ambiguë et voix non séparables : retourner explicitement `unknown` ou des candidats.

**Évaluations ciblées**

- GTTM : précision/rappel des frontières de groupement et mesures de correspondance entre arbres, regroupées par pièce, avec une base triviale (frontières de mesures, découpage uniforme).
- DCML : accords/fonctions/cadences seulement si la cible et les notes d'entrée correspondent exactement ; partitions par composition, pas par note.
- ASAP/MazurkaBL : déviation temporelle, arcs de tempo/dynamique et alignement contre données de performance, regroupés par œuvre et interprète ; témoin à tempo constant et dynamique constante.
- SALAMI : frontières grossières et fines, contre témoin périodique ; effets de l'audio manquant explicitement rapportés.
- OpenMIC : instrument présent/absent sur clips audio, pas inférence depuis General MIDI.
- Grammaire induite : compression **sur œuvres exclues**, sensibilité aux permutations contrôlées, transpositions et modifications de rythme ; stabilité des règles d'un corpus à l'autre et coûts de recherche mesurés.

**Rapports obligatoires** : nombres de *compositions parentes*, sources et licences, alignement, disponibilité, baselines, tests aveugles, intervalles par groupes indépendants, erreurs typiques, ambiguïtés conservées, phénomènes volontairement non testés. Un taux sur 10 000 notes d'une seule œuvre n'est pas 10 000 cas indépendants.

## 7. Ordre de réalisation : exhaustivité du modèle, incréments vérifiables

| Étape | Livrable testable | Éviter |
|---|---|---|
| **G0 — fondation** | IR commun typé à trois vues, horloges et provenance ; règles de conservation, tests MIDI polyphonique/tempo/CC/vélocité | Un objet `Note` qui mélange partitions, performance et audio |
| **G1 — relations/transformations** | Opérateurs `SEQUENCE`, `PARALLEL`, `ALIGN`, `GROUP`, `TRANSFORM`, `DEPEND` et exemples déterministes vérifiés | Heuristiques propres à une composition |
| **G2 — groupements** | Parseur à analyses multiples, métrique, motifs, frontières/arbres confrontés à GTTM et LBDM | Prétendre que le premier arbre trouvé est le vrai |
| **G3 — harmonie/polyphonie** | Conduite des voix, fonctions et progressions évaluées sur DCML ; règles harmoniques déclaratives inspirées de Rohrmeier | Étiqueter des accords sans tonalité locale ni voix identifiées |
| **G4 — expression** | Courbes de tempo, microtiming, nuances et articulation sur partitions/performance alignées ASAP et MazurkaBL | Assimiler la vélocité à la loudness |
| **G5 — son/orchestration** | Vues audio optionnelles, timbre/enveloppe/volume et instruments avec preuves, corpus audio adaptés | Inventer l'enveloppe sonore d'un programme MIDI |
| **G6 — grammaire acquise** | Induction MDL de constructions/rôles, contrôle sur répertoires exclus ; forme longue et comparaison SALAMI | Confondre capacité de compression et signification/perception universelle |

**Politique de travail** : le projet traite *tous* les aspects dans la conception des données et de l'API, mais ne déclare chaque mécanisme « implémenté » qu'après une extraction conservatrice et une vérification pertinente. Les explorations historiques de « mystérieux » restent archivées comme études séparées, et ne dictent plus la structure de la grammaire.

## 8. Première décision architecturale à valider

La grammaire est **multi-axe** et **multi-échelle**. Elle ne suppose pas que toute pièce admet un unique arbre total ; plutôt :

```text
Source(s) préservées
  → Graphe temporel d'événements observés
  → Relations candidates locales (simultanéité, intervalle, métrique, etc.)
  → Plusieurs hiérarchies : motifs, phrases, harmonie, voix, expression
  → Grammaire de règles typées / équivalences / transformations
  → Analyse justifiée + alternatives + zones inconnues
```

On ne commence **pas** par une nouvelle fonction qui renvoie un score émotionnel global. La première démonstration réussie sera une phrase ou un extrait polyphonique analysé de manière explicable avec des tempos/dynamiques correctement préservés, puis évalué sur une source académiquement annotée.
