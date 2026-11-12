# AnaMu — objectifs et ordre impératif des phases

## DÉCISION ACTIVE — 11 novembre 2026 : arrêt de la boucle 1A et début du travail documentaire 1B

**Voir [STATUS.md](STATUS.md) pour le bilan actuel : 263 cartes utilisables, 115 cartes partielles, huit familles de choix; 93 recherches publiques terminées en meilleur effort, 22 bloquées faute de preuve externe, zéro recherche cyclique active.** Une vingtaine de passages sur les mêmes sources n'a pas livré les plans/œuvres spécifiques : il faut **conserver les inconnus, pas les rechercher sans fin**. La phase 1A de collecte **publique** est donc **arrêtée en meilleur effort** (NON couverte exhaustivement). **La phase 1B de documentation des sujets musicaux attestés est désormais ACTIVE**, même si certains cours restent partiels. Premier lot : [14 mécanismes musicaux décrits et sourcés](subject-research/2026-11-11-first-14-music-theory-mechanisms-primary-educational-sources.md). Le verrou de la phase 2, du MIDI, des tests et de la composition demeure entier. Les sections rédigées ci-dessous présentant 1A comme la seule phase active sont des **règles historiques antérieures remplacées par la présente décision**.

**Référence normative.** La finalité est une compréhension de la composition et de l'arrangement fondée sur **la réunion du contenu réel de plusieurs cursus universitaires entiers**. Cette connaissance doit permettre de reconnaître et d'expliquer les mécanismes de musique existante. Une composition musicale ultérieure devra reposer sur cette compréhension et sur des jugements d'écoute, mais **aucune génération n'est autorisée maintenant**.

**Périmètre obligatoire :** [matières musicales uniquement](music-only-scope.md). Les cours de culture générale et d'arts visuels sans musique ont été éliminés.

## Phase 1A — carte détaillée des sujets de TOUS les cours (SEULE PHASE ACTIVE)

Périmètre : **386 entrées musicales retenues** dans les programmes UdeM, McGill,
Berklee, incluant options, recommandations et connaissances de majeures voisines.
Objectif immédiat : **pour chaque cours**, écrire une **description suffisamment
détaillée des contenus** (principaux sujets, notions, techniques, styles,
applications et, si publiés, exemples et progression).

Sources privilégiées : **syllabus ou plan détaillé** propre au cours ; à défaut,
**description institutionnelle suffisamment riche pour cerner les sujets**,
avec honnêteté sur sa portée. Un simple titre ou une description vide ne suffit
pas. Cibler environ **4–12 axes thématiques** quand les documents le permettent,
sans fabriquer de structure hebdomadaire. Recueillir par lots de 10 à 30 cours.

**Ce qui N'EST PAS requis pour terminer la cartographie 1A :** les livres exacts
de chaque professeur, les chapitres prescrits, les consignes complètes de
tous les exercices, les corrigés, partitions, barèmes, accès aux cours fermés
ou une validation indépendante de chaque technique. Ils ne seront notés
qu'incidemment, s'ils se trouvent déjà dans une source accessible.

L'ancien indicateur de `syllabus_documented` / `catalog_only` indique la
**qualité de la provenance du cours**, pas son **avancement thématique**.
Le champ `topic_outline` dans le registre décrit désormais les deux
séparément. Une description riche au catalogue peut être utilisable en phase
1A, sans devenir artificiellement un syllabus.

**État actuel après filtrage du 10 novembre 2026 :** 386 entrées
musicales suivies, dont **203 cartes utilisables, 175 partielles et huit
familles de pratique musicale non dépliées**. Les 402 entrées de la
grille historique incluaient des cours extra-musicaux et ne sont plus
notre périmètre. [État détaillé](topic-outline-coverage-status.md).
Le balayage initial n'est pas la documentation approfondie de tous les sujets.

## Phase 1B — documentation académique par SUJET (DIFFÉRÉE)

Quand les contenus des 386 entrées musicales auront été cartographiés, rechercher dans
une passe distincte la littérature académique, les traités, exemples,
enregistrements, exercices et objections **sur chacun des sujets identifiés**,
pas cours après cours pour obtenir le matériel exact des enseignants.
Cette phase n'est pas activée actuellement.

## Phase 2 — réconcilier les connaissances (VERROUILLÉE)

Après couverture du contenu des cours et décision explicite de Léon, extraire les savoirs élémentaires enseignés et les réunir dans une **base de concepts musicaux partagés**, avec définitions, prérequis, relations, provenance précise, exemples, variantes et limites stylistiques. Voir [knowledge-base.md](knowledge-base.md).

## Phase 3 — choisir et développer les analyseurs MIDI (VERROUILLÉE)

**Seulement après la matière des cours :** établir pour chaque concept si l'on peut détecter son expression dans des **morceaux MIDI existants**.

1. Relier la capacité proposée au cours et au chapitre vérifiés.
2. Définir les observations MIDI pertinentes et les faux amis possibles.
3. Signaler les phénomènes **non déductibles du seul MIDI**, comme le timbre acoustique réel, une nuance effectivement entendue ou une intention d'orchestration.
4. Construire ensuite un outil explicable, montrant ses notes, relations, variantes et inconnues.
5. Vérifier les détections sur les exemples et contre-exemples académiques, puis sur des morceaux tenus à l'écart.

Les outils sont la **conséquence du savoir enseigné**, pas un programme libre de recherche algorithmique.

## Phase 4 — composition éventuelle (VERROUILLÉE)

Détecter correctement des composants musicaux n'implique pas encore savoir composer. Une éventuelle phase générative exigera la couverture universitaire, une analyse indépendante validée, des critères de cohérence musicale et d'écoute, puis l'autorisation explicite de Léon. Les portes L01–L05 du [TODO](todo-university-coverage.md) restent fermées.

## Statuts à distinguer

- **Cours recensé :** présent dans une édition officielle.
- **Carte thématique 1A :** utilisable / partielle / non encore traitée, avec source de cours et degré de précision indépendant du syllabus.
- **Matière obtenue :** documents détaillés localisés et accessibles.
- **Matière structurée :** objectifs, notions et exercices extraits avec citations.
- **Couverture vérifiée :** branches et lacunes évaluées indépendamment.
- **Concept modélisé, analyseur testé, compétence validée :** futurs statuts à ne jamais déduire d'une description de catalogue.

Le [TODO universitaire](todo-university-coverage.md) est la **seule liste active**. Les familles de capacités B–L y restent des exigences futures, pas une autorisation de développer maintenant.
