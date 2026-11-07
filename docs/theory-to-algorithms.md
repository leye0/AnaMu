# AnaMu — Programme scientifique : des théories musicales aux émotions

**Statut :** plan de recherche, non validation expérimentale. **Date :** 7 novembre 2026.

## Principe directeur

La musique n'est pas réduite à « mineur + lent = triste ». AnaMu étudie ce qui
arrive *entre* les événements : prédiction, incertitude, violation, mouvement
tonal, attente de résolution, confirmation, réinterprétation d'un motif et
intégration temporelle. La prédiction d'une note ou d'une tension **n'est pas**
encore la prédiction d'une émotion. L'émotion **perçue** doit être distinguée
de celle **ressentie**, du plaisir, de l'activation et de la tension.

L'architecture débute par la théorie et des expériences sur **MIDI déjà
disponible**. Ne pas imposer l'identification d'une chanson, la comparaison
audio, Demucs, la transcription d'instruments ni un corpus massif avant de
démontrer qu'un algorithme en a besoin.

## 1. Inventaire théorique exploitable

Chaque source comporte (a) un phénomène, (b) un algorithme candidat,
(c) une expérience falsifiable. *Inspiré de* ne signifie jamais *réplique
validée des résultats publiés*.

| Référence primaire | Hypothèse ou mécanisme | Module et observations calculables | Test et précaution |
|---|---|---|---|
| Leonard Meyer (1956), *Emotion and Meaning in Music* | Attente, inhibition, satisfaction et structure temporelle du sens musical | Taxonomie d'événements `expected`, `deferred`, `violated`, `resolved` sur une représentation explicite des attentes | Cadre théorique, **pas** un classificateur numérique ni une preuve universelle |
| David Huron (2006), *Sweet Anticipation* (ITPRA) | Réponses distinctes : imagination, tension, prédiction, réaction, évaluation | Séparer état *avant* l'événement (`entropy`), réaction à l'événement (`surprisal`) et conséquences différées | Les cinq systèmes ne sont pas directement observables dans un MIDI ; distinguer proxy et réponse psychologique |
| Eugene Narmour (1990), *The Analysis and Cognition of Basic Melodic Structures* | Attentes liées à la taille et la direction des intervalles | Extracteur de directions, tailles, symétries, réversals et continuations | Tester sur continuations humaines et styles hors entraînement |
| E. Glenn Schellenberg (1996, 1997), tests et simplification du modèle I-R | Modèle mélodique plus parcimonieux testé psychologiquement | Baseline à règles pour la probabilité de continuation d'une ligne monophonique | Comparer au modèle Narmour complet et à des prédicteurs naïfs ; éviter la pseudo-universalité |
| Marcus Pearce (2005, 2018), IDyOM | Apprentissage statistique des attentes à court et long terme, dépendant du style | Modèle des probabilités conditionnelles des événements, information content et entropie, multi-viewpoints | Privilégier IDyOM original, versions fixes et tests de reproduction ; un petit n-gramme maison n'est qu'une **baseline** |
| Fred Lerdahl (2001), *Tonal Pitch Space* ; Lerdahl & Krumhansl (2007) | Distance tonale, attraction, hiérarchie prolongationnelle et tension | Distance entre régions tonales, attraction, structure des cadences, trajectoire de tension | Exige tonalité locale et analyses harmoniques fiables ; hypothèses souvent tonales occidentales |
| Steinbeis, Koelsch & Sloboda (2006) | Un accord inattendu change tension subjective, physiologie et réponse neurale | Perturbation contrôlée d'un accord dans une séquence | Distinguer tension locale, impact affectif global et émotion locale |
| Egermann, Pearce, Wiggins & McAdams (2013) | Modèles d'attente probabiliste et réactions psychophysiologiques en concert | Corrélation surprise/entropie avec réponse humaine temporelle | Ne pas inférer une causalité universelle d'une corrélation en concert |
| Morwaread Farbood (2012), *A Parametric, Temporal Model of Musical Tension* | Tension intégrant plusieurs paramètres et une mémoire/fenêtre temporelle | Fusion temporelle harmonie, hauteur, rythme, densité, vélocité, synchronie, pentes et pics | Les fenêtres et poids doivent être calibrés sur données humaines, pas réglés pour XMIDI global |
| Dorien Herremans & Elaine Chew (2016), *Tension Ribbons* | Géométrie tonale (*Spiral Array*) | Cloud diameter, cloud momentum, tensile strain, séparés puis combinés | Tester robustesse aux voicings, inversions et changement de tonalité |
| Cheung et al. (2019), *Uncertainty and Surprise Jointly Predict Musical Pleasure* | Interaction non linéaire entre incertitude **préalable** et surprise **observée** | Interaction `H_t × IC_t` et sa relation avec les évaluations de plaisir | Les résultats portent sur le **plaisir d'accords**, pas toutes les émotions et tous les styles |
| Lerdahl & Jackendoff (1983), *A Generative Theory of Tonal Music* | Regroupement, métrique et hiérarchies des événements musicaux | Segmentation des phrases et niveaux structurels, signaux de clôture | Les règles de préférence donnent parfois plusieurs analyses ; conserver ambiguïté |

### Références vérifiables pour démarrer

- Pearce, IDyOM (auteur, logiciel et bibliographie) : https://www.marcus-pearce.com/idyom/
- Huron, *Sweet Anticipation* (MIT Press) : https://mitpress.mit.edu/9780262303309/sweet-anticipation/
- Schellenberg (1996), *Cognition* : https://pubmed.ncbi.nlm.nih.gov/8808327/
- Schellenberg (1997), *Music Perception* : https://doi.org/10.2307/40285723
- Lerdahl & Krumhansl (2007) : https://doi.org/10.1525/mp.2007.24.4.329
- Farbood (2012), PDF de recherche : https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/f/11865/files/2020/08/Farbood_2012_Musical_Tension.pdf
- Steinbeis et al. (2006), PDF auteur : https://stefan-koelsch.de/papers/Steinbeis_2006JOCN18_expectancy%2Bemotion.pdf
- Egermann et al. (2013) : https://pubmed.ncbi.nlm.nih.gov/23605956/
- Herremans & Chew (2016), publication auteur : https://www.dorienherremans.com/content/tension-ribbons-quantifying-and-visualising-tonal-tension
- Cheung et al. (2019), PDF auteur : https://www.marcus-pearce.com/assets/papers/CheungEtAl2019.pdf

**Étape bibliographique obligatoire avant chaque module :** lire l'algorithme
original, les variables manipulées, l'expérience, les échecs, la population
étudiée et les éventuelles licences. Documenter les écarts de notre
implémentation. Les auteurs ci-dessus constituent des points de départ, non un
consensus unique ni une garantie de reproduction.

## 2. Contrat de représentation musicale

Un MIDI brut est une entrée admissible ; aucun traitement audio obligatoire.
Conserver les événements natifs et exposer des *vues dérivées*, plutôt que
réécrire le fichier et perdre l'information. Les modules déclarent les vues
dont ils ont besoin. Le besoin en corpus sera déduit de ces contrats.

### 2.1 Entrée et provenance

`asset_id`, source, empreinte, droits, ticks/beat, mesures, tempo map,
channels, programs, note_on/note_off, vélocités, contrôleurs et éventuelles
annotations humaines. Format 0/1, partitions polyphoniques et tempo variable
ne doivent pas être aplatis silencieusement.

### 2.2 Vues dérivées et statut

| Vue | Algorithme / méthode candidate | Confidence et cas indéterminés |
|---|---|---|
| Notes par partie | `mido` ou `pretty_midi`, appariement des onsets/offsets | Retriggers, notes non closes, pédale, canal partagé |
| Lignes mélodiques | Lignes monophoniques explicites ; plus tard séparation de voix polyphonique | Ne pas déclarer « mélodie principale » une piste arbitraire |
| Harmonie | Segments d'ensembles de notes, candidats d'accords, basse, renversement | Arpèges, notes étrangères, pédales, accords incomplets, ambiguïtés |
| Tonalité | Hypothèses locales et globales, profils chromatiques, modulations | Plusieurs tonalités plausibles, atonalité, changement de style |
| Syntaxe d'accords | Degrés, fonctions, cadences, transitions, tonalité locale | Dépend de l'analyse harmonique ; ne jamais masquer la faible confiance |
| Mélodie relative | Intervalles, contour, registre, durées, figures, motifs | Variantes/ornementations vs événements structurels |
| Structure | Fenêtres, mesures, phrases, répétitions, sections, clôtures | Segmentation probabiliste, non vérité automatique |
| Rythme | Métrique, syncopes, densité, changements, polyrythmie | Beat/mètre parfois mal encodés |

Chaque observation doit fournir : `start_tick`, `end_tick`, `beat`,
`feature_type`, `value`, `hypotheses`, `confidence`, `unknown_reason`,
`engine_name`, `engine_version`, `parameters` et provenance d'entrée.
On ne doit **pas** attribuer une probabilité calibrée si elle n'a pas été
calibrée. Une note peut servir à un modèle même si les accords sont incertains.

## 3. Moteurs de recherche — ordre d'implémentation

### M0 — Ingestion MIDI conservatrice (priorité immédiate)

1. Construire une chronologie fiable de notes par piste/canal et beats.
2. Conserver les pistes polyphoniques en entrée ; ne pas forcer l'extraction
   d'une mélodie lorsque la séparation de voix est indéterminée.
3. Offrir des fixtures synthétiques avec erreurs volontaires : note absente,
   voix superposées, retrigger, changements de tempo, percussion canal 10.
4. Première validation : invariance à une transposition simple pour les
   intervalles et stabilité sous changement de tempo pour les coordonnées
   en beats.

### M1 — Expectation mélodique probabiliste

1. Baseline explicable n-gramme à ordre variable sur intervalles relatifs ;
   probabilités normalisées, `P(event | contexte)`, information en bits,
   entropie avant l'événement. Pas de prédiction d'émotion.
2. Comparer IDyOM original et l'approche Narmour/Schellenberg.
3. Ajouter progressivement durées, positions métriques, contour et styles
   sous forme de *viewpoints* indépendants.
4. Distinguer *long-term style model*, prédiction sur morceau inconnu et
   adaptation strictement **causale** au début du morceau.
5. Tests de prédiction sur corpus tenu hors entraînement et erreurs analysées.

### M2 — Harmonie, progressions et relations tonales

1. Produire plusieurs hypothèses d'accords et une option `unknown` ; évaluer
   d'abord sur suites d'accords **déjà annotées**, avant d'inférer les accords
   de grands arrangements MIDI.
2. Prédire les accords suivants par style et contexte ; entropie et surprise
   indépendantes du modèle mélodique.
3. Calculer Tonal Pitch Space / Spiral Array et mesurer éloignement, retour,
   attraction, instabilité et mouvement tonals.
4. Étudier les cadences et résolutions en tenant compte du contexte local
   *et* de l'arbre hiérarchique des phrases.
5. Contrôles : transposition, renversement, voicing, accélération, accords
   incomplets, tonalités ambiguës, changements de mode et de genre.

### M3 — Motifs, formes et temps longs

1. Représenter un motif par intervalles, rythme relatif et placement.
2. Détecter répétition, transposition, séquence, inversion, augmentation,
   diminution et altération ; distinguer similarité faible et identité.
3. Relier apparition, attente de retour, variation, section et cadence.
4. Conserver des échelles simultanées : événements, 1–4 mesures,
   phrases, sections et morceau, sans choisir arbitrairement une seule fenêtre.

### M4 — Fusion tension / attente / résolution

1. Calibrer séparément les composantes reconnues dans les études originales :
   mélodie, harmonie, dissonance, rythme, densité et dynamiques.
2. Fenêtres temporelles, dérivées, intégrales, pics et temps depuis la
   dernière résolution ; modèles de Farbood et alternatives simples.
3. Mesurer l'interaction entre surprises mélodiques et harmoniques ;
   décomposer tension mélodique, harmonique et conjointe.
4. Comparer une fusion additive avec interactions non linéaires (`H × IC`)
   inspirées de Cheung, sans assimiler plaisir et émotion.

### M5 — Hypothèses émotionnelles **après** les mécanismes

1. Représenter séparément valence, activation, tension, plaisir et classes
   émotionnelles lorsque les annotations les mesurent effectivement.
2. Apprendre à relier des trajectoires M1–M4 aux jugements **humains**.
3. Apprentissage faible pour XMIDI : label global seulement, pas une courbe
   émotionnelle seconde par seconde reconstruite artificiellement.
4. Conserver désaccords inter-annotateurs, diversité stylistique et calibration
   par type d'émotion. Autoriser `inconclusive`.
5. Audit de règles : aucune association « mineur = tristesse » ne doit être
   présentée comme une explication suffisante. Les caractéristiques statiques
   restent des **baselines de contrôle**.

## 4. Corpus déterminé par les questions des modèles

**Ne pas construire d'abord un corpus omnivore.** Pour chaque module, écrire
`required_input`, `optional_input`, `human_ground_truth`,
`evaluation_protocol`, `unsupported_cases`, puis sélectionner la plus petite
quantité de données utile.

| Besoin | Corpus / données de départ | Ce qu'il ne faut pas prétendre |
|---|---|---|
| Parser des MIDI et tester invariants | Fixtures MIDI synthétiques en mémoire | Une fixture ne valide pas une émotion réelle |
| Tester les continuations mélodiques | Partitions/MIDI monophoniques de styles variés ; continuations humaines si accessibles | Probabilité sous un corpus ≠ probabilité universelle |
| Tester progressions/cadences | Séquences d'accords connues et annotées ; extraits de chorals analysés | Inférence d'accords d'un arrangement ≠ vérité d'annotation |
| Relier symbolique à émotions par extrait | EMOPIA, 1 087 extraits audio+MIDI de piano, classes par quadrant | L'étiquette d'un extrait n'est pas un événement local exact |
| Relier symbolique à émotion globale | XMIDI, 108 023 MIDI avec annotations globales | Pas de label temporel ni titre/artiste garanti |
| Valence / activation temporelles | DEAM (audio, annotations continues) | Aucun MIDI aligné fourni par défaut |
| Réponses physiologiques | PMEmo (audio + EDA, 794 chansons) | EDA ≠ étiquette émotionnelle spécifique |
| Études de cas célèbres | MIDI de Bach, Chopin, puis pop identifiée et autorisée | Les œuvres du domaine public n'impliquent pas que chaque fichier MIDI est libre ; ni annotation humaine implicite |

**Seuils d'admission dépendants du module**, pas quotas universels. Un bon
MIDI monophonique sans batterie est parfaitement valable pour M1 ; un fichier
polyphonique sans mélodie isolable peut être étudié en M2/M3. Si seulement
500–2 000 pièces conviennent, cela peut suffire pour des pilotes rigoureux.

Toujours conserver les *rejets et raisons*, empreintes et provenance.
Séparer œuvres/arrangements/versions et entraînement/validation/test par
composition, jamais par fichier seulement. Mesurer les biais de genres,
époques et émotions. Respecter la licence de chaque corpus et arrangement.

## 5. Protocoles de vérification falsifiables

### 5.1 Tests de vérité structurelle

- Fixtures ciblées avec sorties exactes pour lecture et normalisation MIDI.
- Golden sets annotés manuellement pour accords, cadences, mélodies et motifs ;
  mesurer précision, rappel, taux `unknown` et calibration.
- Cas négatifs : notes d'ornement, notes de passage, polyphonie, erreurs
  volontaires, accords partiels, changements de tempo et transpositions.

### 5.2 Tests de théorie musicale

- Prédiction de note/accord : log-loss bits/événement, perplexité,
  calibration, précision top-k comparées à unigramme et n-gramme.
- Tension : corrélation et erreur avec jugements temporels **pertinents**,
  validation par œuvre, et reproduction de contrastes des études originales.
- Contrôles contrefactuels : même pièce avec un accord ou une résolution
  remplacés ; prédire *direction du changement*, sans bricoler les sorties.

### 5.3 Tests émotionnels

- Comparer : (A) métadonnées/statique, (B) trajectoires isolées,
  (C) attentes et tensions, (D) interactions et hiérarchie.
- Ablations : ordre temporel mélangé, motifs détruits, accord modifié, rythme
  conservé, progression transposée ; mesurer ce qui change et pourquoi.
- Métriques adaptées aux annotations : macro-F1 + calibration pour classes,
  erreurs/corrélations temporelles pour valence/activation, accord humain
  lorsque disponible ; rapport par genre et famille d'instruments.
- **Interdiction** d'utiliser les étiquettes émotionnelles pendant
  l'extraction de la « vérité » musicale ou de choisir les paramètres en
  regardant les morceaux de test.

### 5.4 Critères de preuve

Une théorie implémentée n'est considérée validée que si : (1) sa définition et
ses limites sont documentées ; (2) la reproduction ou la différence avec la
publication est explicitée ; (3) les observations peuvent être recalculées ;
(4) les baselines sont comparées ; (5) les erreurs et les contrôles négatifs
sont publiés. Ne pas annoncer une détection émotionnelle réussie à partir
d'une seule démonstration agréable à écouter.

## 6. Premier incrément de code et état réel

**Baselines expérimentales initiées, non validées contre des humains :**

- `anamu/midi_views.py` : conversion directe d'octets MIDI en vues de pistes
  monophoniques candidates, avec refus des chevauchements ambigus, sans
  prétendre identifier la véritable ligne mélodique.
- `anamu/expectation.py` : modèle n-gramme hiérarchique lissé calculant
  `P(event | historique)`, entropie préalable et surprise en bits. Il n'est
  **pas** IDyOM et n'émet aucune étiquette émotionnelle.
- `tests/test_symbolic_expectation.py` : tests de normalisation,
  continuité attendue, données inconnues, invariance aux transpositions,
  exclusion des percussions et refus de polyphonie ambiguë.

**Prochains jalons :** confronter M1 à IDyOM et aux données de continuation
humaine ; implémenter M2 sur des suites d'accords de référence indépendantes ;
puis seulement concevoir un corpus émotionnel adapté aux besoins mesurés.

## 7. Suite lointaine, non bloquante

1. Analyses de morceaux connus de Bach et Chopin : choix de pièces,
   édition MIDI licite, provenance, comparaison avec analyses musicales
   publiées, annotation humaine de tension si objectif affectif.
2. Analyse comparative pop sur œuvres vraiment identifiées, sans rendre leur
   identification préalable obligatoire pour les expériences M0–M5.
3. Générateur MIDI symbolique piloté par trajectoires émotionnelles,
   instrumentation et traits stylistiques mesurables ; sortie soumise aux
   **mêmes évaluateurs explicables** et à l'écoute humaine.
4. Beaucoup plus tard : audio, paroles, MIDI↔audio et séparation Demucs,
   uniquement si un protocole concret démontre le gain attendu.
