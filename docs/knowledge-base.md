# AnaMu — architecture de la base de connaissances musicales académiques

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
