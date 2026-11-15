# AnaMu — architecture de la base de connaissances musicales académiques

**DÉCISION DE PHASE (11 novembre 2026) :** [État courant](STATUS.md). La collecte publique de plans par cours (1A) est arrêtée en meilleur effort : **115 cours restent partiels, dont 22 bloqués en attente de source extérieure, mais aucun n'est une recherche active sans nouvelle preuve**. La **documentation académique des sujets identifiés (1B) est maintenant ACTIVE**; [14 mécanismes sourcés](subject-research/2026-11-11-first-14-music-theory-mechanisms-primary-educational-sources.md) sont acquis comme documentation *des sujets*, pas comme syllabus. Les développements de la base de concepts unifiés / phase 2 restent verrouillés. Les assertions plus bas disant « seule collecte par cours active » sont des instantanés historiques.

**Document de conception normatif, pas une implémentation achevée.**
L'ambition est de posséder un patrimoine **massif, structuré, traçable et
interrogeable de connaissances musicales** obtenu par la mise en commun de
plusieurs programmes universitaires avancés. Ce patrimoine doit alimenter
plus tard des **analyseurs de morceaux MIDI existants** et, **une fois les
portes académiques levées**, un éventuel système de composition musicale.
**La priorité actuelle est exclusivement la collecte de la matière des
cours**, selon [le protocole](course-material-collection.md). La conception
du patrimoine ci-dessous décrit la phase suivante, encore verrouillée.

## 1. L'actif central n'est pas un catalogue de cours

Les [catalogues UdeM, McGill, Berklee](university-curriculum.md) décrivent
**où chercher les connaissances**, pas les connaissances elles-mêmes.
Les [recommandations et spécialités voisines](optional-knowledge-audit.md)
enrichissent le périmètre ; leur statut optionnel ne réduit pas leur valeur.

Un même concept peut être enseigné dans trois cours différents sous des
noms divers. L'objectif est de **réconcilier les savoirs** dans une base
commune, en conservant les formulations, divergences, prérequis, exercices,
exemples et exceptions propres à chaque source. On ne confond jamais
« connaître le nom du concept » avec « être capable de l'identifier et de
l'expliquer correctement dans une œuvre ».

### Quatre couches à ne jamais confondre

| Couche | Produit attendu | Ce qu'elle ne prouve pas |
|---|---|---|
| **1. Sources universitaires** | Programmes, éditions, cours, syllabus, chapitres, exercices, lectures, crédits et provenance | Que le moteur comprend la matière |
| **2. Base académique unifiée** | Concepts, règles conditionnelles, exemples, relations, contre-exemples, styles et divergences | Que chaque concept est implémenté |
| **3. Moteur d'analyse MIDI** | Hypothèses sourcées sur des morceaux MIDI existants, références aux concepts utilisés, limites des observations | Que les analyses sont justes sans épreuve indépendante ou que MIDI contient le son acoustique |
| **4. Évaluation / composition future** | Compétences expertisées et, plus tard, décisions génératives cohérentes évaluées à l'écoute | Qu'une métrique isolée garantit une musique agréable |

**État actuel :** nous avons des inventaires de catalogues (couche 1
**partielle**). La matière détaillée des cours n'a pas été collectée
exhaustivement. **La grande base de concepts réconciliés (couche 2) reste
à construire.** Il n'existe plus de prototype analytique dans le dépôt
actif : les futures capacités seront décidées à partir des enseignements
réellement obtenus. La composition reste fermée.

## 2. Unité de connaissance à construire

La représentation définitive devra évoluer avec la recherche, mais toute
unité académique devra pouvoir exprimer au minimum :

| Champ conceptuel | Raison d'être |
|---|---|
| `concept_id`, `version`, intitulés et synonymes | Identité stable sans doublons dus à la terminologie |
| Définition et **fonction musicale** | Expliquer ce que le compositeur, l'orchestrateur ou l'analyste cherche à faire |
| Domaine de validité | Style, époque, formation, instrument, convention, restrictions et exceptions |
| Relations entre concepts | Prérequis, spécialisation, variante, contraste, contradiction justifiée |
| `sources[]` | Programme, cours, section de syllabus, édition, lecture et droits d'accès |
| Exemples et contre-exemples | Mesures/partitions licites, annotations d'expert, résultats attendus et cas ambigus |
| Conditions observables | Notes, voix, rythme, harmonie, notation, interprétation, timbre ou audio requis |
| Capacités d'analyse liées | Hypothèses, mécanismes, points du TODO, tests négatifs et preuves |
| Statut et incertitude | `repéré / décrit / réconcilié / implémenté / testé / validé` et limites |

Ces champs sont un **contrat de conception**, pas la description d'un
schéma de base de données déjà présent dans le dépôt. Aucun script actuel
ne doit être présenté comme un moteur complet de cette base.

## 3. Transformer plusieurs programmes en une connaissance commune

1. **Inventorier** toutes les branches pertinentes des cours obligatoires,
   optionnels, recommandés et voisins, avec statut d'admissibilité séparé.
2. **Lire la matière réelle** : objectifs, chapitres, conventions,
   exercices, œuvres et barèmes d'évaluation ; signaler ce qui est inconnu.
3. **Extraire des savoirs élémentaires** : par exemple, une doublure
   d'octave est un geste d'orchestration seulement si sa fonction, son
   registre, ses instruments et son effet perceptif sont contextualisés.
4. **Réconcilier** : associer des enseignements équivalents à un concept
   stable, conserver leurs nuances, et séparer les variantes incompatibles
   plutôt que d'inventer une règle universelle.
5. **Relier** concepts, prérequis, opérations, styles, partitions annotées
   et sous-compétences. Rendre possible la navigation dans les deux sens :
   `cours → concepts` et `concept → cours, preuves et mécanismes`.
6. **Après autorisation de passage à la phase MIDI**, exercer l'analyse
   sur l'inconnu : vérifier que le moteur peut reconnaître dans un MIDI
   des composants effectivement enseignés, expliquer leur fonction,
   garder des hypothèses concurrentes et détecter ses propres limites.
7. **Évaluer ensuite** les résultats avec des œuvres hors développement, des
   musiciens indépendants et de l'audio lorsque l'affirmation porte sur
   une qualité sonore. Le statut `validé` requiert le dossier probant.

Un cours « optionnel » peut apporter le seul enseignement disponible d'un
geste orchestral essentiel : il doit être étudié. Un cours répétitif peut
renforcer la preuve ou préciser un contexte, même si sa matière recoupe un
autre. L'exclusion doit être justifiée **par acquisition de connaissance**,
jamais par la facilité de terminer un programme de crédits.

## 4. Ce qui fait une vraie explication musicale

Exemple d'une question future : « Pourquoi le compositeur confie-t-il le
contrechant aux altos pendant que les bois doublent le thème ? »

Une analyse crédible doit pouvoir articuler : rôles et indépendance des
voix, tessitures, directions mélodiques, harmonie et dissonances, texture,
équilibre des pupitres, articulation, contexte formel, couleur audible et
alternatives d'orchestration. Chaque affirmation renvoie aux notes, aux
sources pédagogiques et à une connaissance pertinente. Elle peut conclure
qu'une partie du résultat reste **inconnue sans enregistrement**.

Une simple corrélation de pistes MIDI, un score de similarité ou une
prédiction de note correcte ne résout pas cette question. **Les
mathématiques sont des instruments de vérification du savoir musical,
pas la finalité du projet.**

## 5. Relation avec l'éventuelle composition

Le système pourrait un jour utiliser cette connaissance pour choisir un
développement de motif, une conduite des voix, une répartition orchestrale
et un geste expressif **en comprenant leurs conséquences musicales**.
Cela exigerait en plus des choix artistiques, un rendu crédible et des
évaluations auditives humaines. Une bonne analyse n'est pas une garantie
automatique de bonne composition.

Cette étape demeure **hors de portée opérationnelle** jusqu'à couverture
et expertise du [TODO universitaire](todo-university-coverage.md), portes
**L01–L05**, et accord explicite de Léon.

### Deux modules, une connaissance commune

**Décision du 15 novembre 2026.** L’analyse et la création sont deux modules différents. La création dépend d’une analyse richement documentée et de la synthèse des savoirs transversaux. Ce n’est pas une inversion de l’analyse. Reconnaître un procédé ne dit pas quand le choisir, ni dans quel but. Les fiches de cours restent les sources de connaissance. La synthèse relie les preuves et leurs limites sans les remplacer.

| Responsabilité | Entrée | Sortie attendue |
|---|---|---|
| **Analyse** | Œuvre, passage, partition/MIDI/audio disponibles et question musicale | Observations localisées, hypothèses distinctes, raisonnement, explications concurrentes et inconnues. Une note notée, une identité de motif et une fonction tonale n’ont pas le même statut. |
| **Synthèse transversale** | Résultats d’analyse et enseignements documentés de plusieurs cours | Relations entre concepts, contextes d’application, contre-exemples et limites. Distinguer ce qui revient ensemble dans un exemple de ce qui peut varier indépendamment. Conserver les liens jusqu’au passage qui justifie chaque distinction. |
| **Création** | Intention explicite, forme/style/formation visés, contraintes du passage et connaissances pertinentes | Choix motivés et alternatives. Pour chaque choix, préciser ce qui doit rester reconnaissable, ce qui peut changer, ce qui pourrait contredire une autre contrainte et ce que l’écoute devra encore trancher. L’analyse peut vérifier le résultat, pas décider seule de sa valeur artistique. |

**Exemple de requête à la synthèse.** « Faire entendre une nouvelle région tonale sans perdre le motif et sans changer de porteur. » Consulter conjointement l’identité du dessin (contour, intervalles, rythme), le rôle et la conduite des voix, la confirmation tonale et l’échelle de la frontière. Si les sources ne soutiennent pas une relation dans le style visé, la laisser inconnue au lieu de généraliser. Le [relevé Buxtehude dans OLART-233](courses/berklee-online/OLART-233.md#le-dessin-passe-dans-une-autre-tonalité--buxtehude-buxwv-161) relie ces quatre axes et distingue le constat du scénario d’écriture. Sa transposition exacte et son adaptation modale sont deux options de composition, pas deux ordres à appliquer automatiquement. Le transfert du dessin à un autre porteur chez Bach sert de contraste, pas de consigne de réorchestration.

**Principe de sélection.** Partir du résultat musical voulu, pas d’un nom d’œuvre ou d’une liste de motifs voisins. Dans la requête ci-dessus, MTE-1221 aide à évaluer si la destination est installée, OLART-233 à choisir ce qui rend le dessin reconnaissable, et la comparaison BWV 78 à écarter un transfert de voix si le porteur doit rester fixe. Si la consigne exige les intervalles exacts, la variante modale devient inadmissible, même si le cas Buxtehude la documente. Si la consigne demande seulement une autre couleur sans quitter le centre, la réharmonisation ou la tonicisation redeviennent des options et la modulation n’est plus le résultat à chercher. L’accès transversal sert à **choisir quelles connaissances consulter, puis à expliquer quels gestes sont compatibles**, pas à cumuler les procédés.

**Préciser ce qui doit rester reconnaissable.** Comparer sur trois plans, sans remplacer un verdict par un autre. **Événements** : même voix, mêmes attaques, hauteurs et durées à la transformation autorisée près. **Dessin** : contour et intervalles analysés dans une voix continue, avec le rythme et les écarts explicités. **Charpente** : même rôle et mêmes destinations ou frontières pertinentes, même si les notes et leur placement changent. La [Variation 25 des Goldberg](courses/berklee-online/OLART-234.md#une-charpente-commune-sans-basse-identique--goldberg-variation-25) écarte l’identité des attaques sans écarter la parenté de structure. Réciproquement, une même descente chromatique peut servir d’autres fonctions dans deux œuvres. La création doit pouvoir demander un niveau précis et recevoir les preuves, les transformations admissibles et les incompatibilités à ce niveau, sans prétendre garantir une reconnaissance à l’écoute.

#### Choisir selon la contrainte musicale

Une relation d’analyse devient utile à la création quand elle aide à prendre une décision, y compris à rejeter une option. Pour chaque consigne, distinguer la partie de l’œuvre concernée, les contraintes fermes et ce qui relève encore d’un choix. Consulter ensuite les exemples et le contre-cas qui tranche l’ambiguïté. Quand les preuves ne permettent pas de prédire ce qui sera entendu, ne livrer que les propriétés vérifiables et formuler l’alternative à écouter.

| Intention formulée | Savoirs à consulter ensemble | Ce que la création ne doit pas déduire |
|---|---|---|
| Garder le rappel du début, mais changer la destination de la phrase | [Diabelli, Variations 1 et 15](courses/berklee-online/OLART-234.md#le-geste-survit-quand-la-cadence-change--beethoven-et-diabelli) pour identifier le rappel et dissocier la reprise de sa destination. [UdeM MTE-1221](courses/udem/MTE-1221.md#application-à-lanalyse-et-à-la-création--un-accord-deux-fonctions-de-préparation-13-novembre-2026) pour séparer la préparation de l’arrivée tonale. | Ne pas imposer l’ancienne cadence sous prétexte que le début est conservé. Une destination de cadence n’est pas à elle seule une région prolongée. |
| Garder un point d’appui au grave tout en faisant avancer les accords | [Brahms op. 24, Variation 22](courses/berklee-online/OLART-234.md#le-bourdon-ne-fixe-pas-lharmonie--brahms-sur-un-thème-de-haendel) pour le rôle de pédale. [McGill MUTH-150](courses/mcgill/MUTH-150.md#cas-comparatif--même-arrivée-de-basse-clôtures-différentes-13-novembre-2026) pour la clôture lue avec basse, dessus et contexte. | La note la plus grave ne donne ni toutes les fondamentales ni toutes les cadences. Si la basse doit jouer le contour d’origine, vérifier que l’option de pédale ne l’efface pas. |
| Transformer un motif par reflet, sans obligation de garder le mètre | [Rachmaninoff XVIII](courses/berklee-online/OCOMP-250.md#inverser-la-cellule-sans-inverser-la-phrase--rachmaninoff) pour une inversion intervallique locale. Le [canon des Goldberg XII](courses/berklee-online/OCOMP-250.md#cas-et-midi--imiter-en-mouvement-direct-ou-contraire-13-novembre-2026) comme contraste. | Préserver la relation des hauteurs n’oblige pas à garder les durées, le mètre ou l’harmonie. Si la consigne exige un canon, une relation entre sections ne remplace pas la réponse entre voix. |

L’[atelier à quatre versions](courses/berklee-online/OLART-234.md#un-motif-quatre-parcours--atelier-découte) fournit un premier exemple de cette discipline. Chacun des deux choix est comparé à la fois avec et sans l’autre. L’indépendance est vérifiée dans les événements du MIDI, pas postulée pour la perception. En particulier, rien ne garantit que les deux changements paraissent s’additionner à l’écoute.

C’est un **contrat documentaire** pour les échanges futurs, pas un schéma de données, une API ou une mise en production. Cette passe ne lève aucune porte L01–L05 et n’ajoute ni moteur ni générateur.

## 6. Source de vérité et prochaine construction

- [OBJECTIVES.md](OBJECTIVES.md) : pourquoi le système existe.
- [university-curriculum.md](university-curriculum.md) : quels savoirs
  universitaires doivent être examinés.
- [todo-university-coverage.md](todo-university-coverage.md) : quelles
  acquisitions, preuves et validations restent à réaliser.
- [course-material-collection.md](course-material-collection.md) : comment
  obtenir et attester la matière de chaque cours, **maintenant**.

**Prochaine tâche active :** obtenir un contenu pédagogique précis pour
**chaque cours**, en notant les chapitres, lectures, exercices, exemples et
lacunes avec leurs sources. Le futur registre versionné suivra ensuite la
chaîne `programme → cours → chapitre/objectif → concept académique unifié →
capacité MIDI analysable → preuve` ; il ne doit pas être rempli au hasard
à partir des seuls intitulés du catalogue.
