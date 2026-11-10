# AnaMu — objectifs scientifiques et contrat du projet

**Statut : référence normative du projet à compter du 10 novembre 2026.**
Une modification de cet objectif doit être explicite et documentée. Les
anciennes études sur les émotions ne constituent plus la feuille de route.

## 1. Finalité

Construire un moteur capable d'analyser une composition musicale inconnue
avec le soin d'un **cours universitaire d'analyse musicale**, en produisant
des objets, relations et hypothèses **inspectables**, sans classificateur
opaque comme moteur principal.

Le moteur doit notamment comprendre comment une œuvre :

1. organise notes et silences dans des durées et métriques ;
2. superpose et sépare ses voix, instruments et couches ;
3. répète, varie, transforme et développe des motifs ;
4. construit accords, régions tonales, fonctions et conduites des voix ;
5. forme des gestes, phrases, périodes, sections et architectures longues ;
6. utilise tempo, ralentissements, nuances, articulation et instrumentation ;
7. réalise ces éléments différemment selon la partition, l'interprétation et
   l'enregistrement.

**Critère supplémentaire de pertinence compositionnelle :** une régularité
ne mérite une règle de grammaire que si l'on peut formuler son rôle dans
l'écriture et tester sa réutilisation constructive ou sa suppression.
L'objectif final est de produire des arrangements **musicalement cohérents
et audibles**, et non d'optimiser uniquement une représentation mathématique.
La justesse des notes ne remplace pas une écoute indépendante.

Cette analyse doit pouvoir dire **« inconnu »**, conserver plusieurs
hypothèses et expliquer la preuve en faveur de chacune. Le but n'est pas de
faire correspondre mécaniquement une musique à un adjectif d'humeur.

## 2. Couverture : tout modéliser, ne rien prétendre déjà maîtriser

| Domaine | Exemples de phénomènes à représenter |
|---|---|
| Événements, hauteur, rythme, métrique | Notes/silences, registre, intervalles, attaques, syncope, polymétrie |
| Tempo et mouvement | Courbes de tempo, accélération, ritardando, rubato, fermates |
| Nuances et articulation | `p`, `f`, crescendos, accents, legato, pédales, enveloppe d'attaque |
| Harmonie et conduite des voix | Accords candidats, fonctions, tonalités, tensions, mouvements contraires, suspensions |
| Motifs et organisation | Imitations, transformations, répétitions, groupements, phrases, sections, forme |
| Instrumentation et texture | Pupitres, rôles, doublures, entrée/sortie des couches, densité et registre |
| Timbre et audio | Spectre, enveloppes, brillance, rugosité, volume acoustique, mixage |
| Style, voix chantée et texte | Régularités de répertoire, prosodie, relation musique/paroles |

Voir les **19 familles d'observables et les sources propres à chacune** dans
[le programme musicologique](music-grammar-research-program.md). L'exhaustivité
est une propriété du **contrat de données**, pas du taux d'implémentation.

## 3. Types de preuve

- **Source encodée** : une note MusicXML, un message MIDI, un changement CC7
  ou une indication de tempo. Dire précisément ce que la source encode.
- **Mesure** : un temps, une fréquence ou une amplitude effectivement mesurée
  dans le signal. Conserver méthode, paramètres et limites.
- **Annotation humaine** : phrase, rôle, harmonie, tension, etc., avec son
  auteur, sa définition opérationnelle, sa licence et ses désaccords possibles.
- **Hypothèse algorithmique** : accord, voix, motif, geste ou fonction inférés.
  Fournir les observations justifiant l'hypothèse et les alternatives.
- **Inconnu / ambigu** : résultat acceptable et requis lorsque la source ne
  permet pas une réponse fiable.

Exemples de distinctions obligatoires :

- Une valeur de **vélocité MIDI** n'est pas un niveau en décibels.
- `set_tempo` n'établit pas l'intention d'un **ritardando expressif**.
- Un nom d'instrument MIDI n'est pas une **preuve d'orchestration**.
- Un accord vertical n'est pas automatiquement une **fonction harmonique**.
- Des notes répétées ne sont pas automatiquement le **même thème perçu**.

## 4. Grammaire générique et interprétations concurrentes

AnaMu utilisera un graphe temporel d'événements, des relations typées et des
arbres de groupement potentiellement concurrents. Une grammaire qui déroule
simplement une chaîne de notes n'est pas suffisante pour la polyphonie.

Primitives prévues : `SEQUENCE`, `PARALLEL`, `ALIGN`, `GROUP`, `TRANSFORM`,
`DEPEND`. Les relations sont fondées sur des preuves, jamais sur des règles
spéciales pour Beethoven ou sur un nom de piste supposé fiable.

La préférence d'implémentation est : **règles déclaratives, contraintes,
invariants et induction structurelle vérifiable**. ML/probabilités peuvent
servir aux tâches réellement incertaines ou à des baselines, mais jamais
masquer la provenance ou remplacer l'évaluation humaine indépendante.

## 5. Feuille de développement et critères de sortie

| Couche | Objectif | État actuel / seuil de validation |
|---|---|---|
| **G0 — preuves** | Conserver MIDI, notation, performance et audio comme vues distinctes | MIDI fiable ; preuves partielles de notes MusicXML, hauteurs sonnantes et métrique locale. Alignement des deux vues et audio encore absents |
| **G1 — relations** | Ordre, simultanéité, alignement, transformations et dépendances explicites | Relations d'Allen et transformations exactes vérifiées ; `ALIGN`, `DEPEND` et `GROUP` hiérarchique non implémentés |
| **G2 — groupements et motifs** | Détecter répétitions, variantes, voix et frontières concurrentes | Prototype de répétitions exactes MIDI et de doublures orchestrales notées ; essais de reconstruction masquée. **Candidats structuraux** seulement ; voix, frontières, arbres, contrôle humain et écoute manquants |
| **G3 — harmonie et voix** | Accords, tonalité, fonctions, conduite des voix et couches orchestrales | Quartets entre voix **notées**, variantes d'une note, verticalités avec tenues et formes exactes de triades/septièmes, effets harmoniques **structurels** d'une variante. Fonctions, notes étrangères, conduites non synchronisées et grammaire évaluée manquantes |
| **G4 — phrases et forme** | Hiérarchies musicales, développement et reprise | Non implémenté |
| **G5 — interprétation et son** | Tempo expressif, articulations, nuances, timbres et enveloppes | Sources et limites spécifiées ; pas d'inférence audio/partition alignée validée |
| **G6 — synthèse analytique** | Analyses multi-axes cohérentes avec contradictions et preuves traçables | Non implémenté |

Chaque couche doit livrer une API stable, des tests de conservation, des
invariants, des cas positifs/négatifs et **des résultats par source réellement
indépendante** avant de prétendre au niveau universitaire.

## 6. Corpus, qualité et protocole

- **Ne pas confondre œuvre, mouvement, enregistrement et transposition** dans
  les découpages d'évaluation.
- Garder les **annotations de vérité** séparées des variables lues par le
  mécanisme testé ; pas de fuite des étiquettes dans l'algorithme.
- Comparer aux baselines triviales et à des témoins mélangés ; rapporter les
  échecs et les écarts hors répertoire.
- Préférer quelques **partitions orchestrales auditées** à des milliers de
  MIDI aux licences ou aux instruments incertains.
- Documenter licences de **chaque fichier**, source primaire, SHA-256,
  transformations, sélection et reproductibilité.
- Ne jamais présenter une étude exploratoire comme une réplication confirmée.

Premier jeu réel : Beethoven 5/I et 7/II avec MIDI multipiste et partition
MusicXML indépendante. La discordance des déclarations instrumentales montre
pourquoi une **comparaison de parties** ne peut devenir un **alignement de
notes** sans preuve supplémentaire. Voir
[l'audit du corpus orchestral](orchestral-corpus-audit.md).

## 7. Hors objectif immédiat

1. Construire un prédicteur générique d'émotions ou du mot « mystérieux ».
2. Entraîner un grand réseau neuronal pour remplacer la grammaire.
3. Générer automatiquement des pièces avant d'avoir analysé les structures.
4. Faire passer un programme MIDI pour une performance ou un audio réel.
5. Atteindre artificiellement un volume de corpus ou un score sans vérité
   expertisée de la capacité concernée.

Chaque règle d'arrangement devra passer les contre-épreuves du
[contrat de composition et d'orchestration](composition-grammar.md).

Les publications et annotations d'attente, de rythme, d'harmonie et de
segmentation peuvent servir de **contrôles indépendants** lorsqu'elles
évaluent réellement une capacité grammaticale. Voir
[l'index des documents](README.md).

## 8. Décision de conception à revisiter

L'ontologie demeure ouverte : nous ne savons pas à l'avance quelles règles
de groupement seront suffisamment génériques. Pour chaque proposition,
consigner **hypothèse, publication, algorithme, épreuve indépendante, limites
et décision**. Si une caractéristique n'est pas observable dans le format
disponible, améliorer la source ou laisser le résultat inconnu.
