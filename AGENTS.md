# AnaMu — contrat de reprise pour tout agent

**Lis ce fichier avant de modifier le projet.** Il résume les décisions
fondamentales ; les liens ci-dessous désignent les documents normatifs.

## FILTRE MUSICAL OBLIGATOIRE — DÉCISION DU 10 NOVEMBRE 2026

**NE PLUS collecter de cours sans objet musical explicite.** Art visuel,
culture générale, littérature, sociologie, psychologie ou santé générales
sont exclus de la recherche musicale même s'ils font partie du diplôme.
Seules les matières traitant de musique (y compris son acoustique,
cognition, histoire, pratiques, production, industrie du musicien) sont
admissibles. [Liste des 16 entrées et 11 candidats supprimés](docs/music-only-scope.md).
**Périmètre courant : 386 entrées**, dont 219 exploitables, 159 partielles,
8 familles musicales. Le chiffre historique 402 n'est PLUS le scope.
Les grilles officielles originales restent des sources, pas des listes
de travail imposant tous les cours non musicaux.

## La mission, en une phrase

Construire une **très vaste base unifiée de connaissances académiques sur la
musique**, en extrayant et réconciliant la matière réelle de **plusieurs
programmes universitaires complets de composition**, afin qu'AnaMu puisse
**analyser et expliquer** des œuvres inconnues avec la profondeur d'un
compositeur/orchestrateur avancé, puis **éventuellement composer** de la
musique cohérente et agréable à écouter à partir de cette compréhension.

Le projet ne cherche **ni** à faire des mathématiques pour les mathématiques,
**ni** à accumuler des noms de cours, **ni** à fabriquer immédiatement un
générateur de notes MIDI. Le test ultime de chaque concept est sa valeur
musicale explicable et démontrable, pas la seule réussite d'un algorithme.

**Hiérarchie de travail impérative :**

> **Programmes → cours → matière réelle → concepts unifiés → (plus tard)
> capacités d'analyse MIDI → (bien plus tard) composition.**

**Phase courante : programmes → cours → matière réelle, exclusivement.**
Un nouvel agent doit **commencer immédiatement** cette acquisition systématique,
sans attendre de consigne supplémentaire : choisir le prochain cours sans
carte thématique exploitable, chercher plans et descriptions détaillées,
noter ses thèmes et limites, puis passer au cours suivant. C'est un **travail
documentaire approfondi**, sans développement expérimental, benchmark
algorithmique ni test musical à cette étape.

## DÉCISION PRIORITAIRE — objectif réel de la première passe (10 novembre 2026)

**Le livrable attendu pour CHACUN des 386 entrées musicales est une DESCRIPTION
DÉTAILLÉE DES SUJETS ENSEIGNÉS**, et non la collection exhaustive de tout
le matériel exact utilisé par le professeur.

**Phase 1A — ACTIVE : cartographie des contenus**, par lots massifs :
- Pour chaque cours, récupérer en priorité un **syllabus, plan détaillé,
  plan-cadre, description institutionnelle suffisamment précise**.
- En extraire un **aperçu thématique exploitable**, idéalement 4–12 axes :
  notions, mécanismes musicaux, techniques, pratiques, exemples de styles
  ou œuvres **explicitement cités**, variantes, niveau et progression si elle
  existe. Une page avec des unités ou des objectifs détaillés suffit pour
  cette cartographie ; les simples intitulés restent insuffisants.
- **Ne PAS chercher systématiquement** la lecture exacte, le manuel prescrit,
  la partition de chaque exercice, son corrigé, le barème de l'évaluation,
  les feuilles distribuées ni le matériel sous accès privé. Les prendre
  uniquement lorsqu'ils sont fournis immédiatement, sans enquête longue.
- Une notice officielle assez riche peut alimenter la **carte thématique**
  même si **le statut historique syllabus reste `catalog_only`** : noter
  honnêtement `source_kind=official_catalogue`, jamais « syllabus ».
- Si la source est trop vague, produire quelques axes sûrs et marquer
  `partial` ; ne pas inventer de séances ni forcer de l'exhaustivité.
- Conserver une trace séparée de la **couverture thématique 1A**
  (`topic_outline` dans le registre), indépendante de l'ancien indicateur
  d'obtention d'un syllabus. Les `raw-batches` peuvent être la source
  canonique de dizaines de descriptions à la fois, sans fiches séparées.

**Phase 1B — DIFFÉRÉE :** lorsque la carte de tous les cours sera en place,
rechercher **la documentation académique sur chaque sujet recensé**, puis
construire plus tard les concepts partagés. Ce n'est **pas** la tâche actuelle.

Ce contrat **prime** sur toute ancienne instruction imposant la récupération
de chapitres, lectures, devoirs et barèmes exacts avant de considérer la
**cartographie 1A** utile. Il ne supprime pas les règles d'exactitude et de
provenance, n'autorise ni code ni tests, et ne prétend pas qu'un catalogue
détaillé soit un syllabus officiel.

### État actuel du registre musical filtré — 10 novembre 2026

**386 entrées**, dont **378 cours identifiables et huit familles musicales** à
déplier. **219 cartes initiales exploitables** et **159 descriptions
partielles** restent dans la phase 1A. Le précédent inventaire académique
de 402 entrées, dont les familles d'options générales, est un historique
et **ne doit pas être restauré**. Voir
[docs/topic-outline-coverage-status.md](docs/topic-outline-coverage-status.md).

**Prochaine action :** améliorer les 159 descriptions musicales partielles
et identifier de vrais cours de pratique musicale derrière les huit familles
non dépliées. Les sources des cours non musicaux, arts visuels, littérature,
sciences sociales et santé générales ne font plus partie du registre.
Aucune recherche de devoirs exacts, aucun test ni CI.

## INTERDICTION EXPLICITE — tests et maintenance logicielle pendant la collecte

**Consigne prioritaire et non négociable pour tous les agents : NE PAS FAIRE DE
TESTS UNITAIRES pendant cette phase documentaire.** Il s'agit de recueillir
les connaissances enseignées, **pas d'écrire ou d'entretenir de la logique
logicielle**.

- **Ne pas créer, écrire, modifier, exécuter ou réparer de tests unitaires**,
  d'intégration, de non-régression ou de suites automatisées.
- **Ne pas modifier** les fichiers sous `tests/`, les scripts de validation,
  la configuration de CI ou les workflows GitHub Actions pour satisfaire des
  tests ou faire passer un pipeline au vert.
- **Ne pas lancer de tests ni entreprendre de débogage de CI**, même lorsqu'un
  contrôle existant échoue à cause du registre documentaire qui s'agrandit.
  Une CI rouge n'est **pas** un motif pour interrompre l'acquisition des cours.
- Le travail attendu est uniquement : **chercher des sources universitaires,
  recueillir une carte détaillée des sujets par cours, puis actualiser les
  lots bruts et le registre**. Les exercices/lectures précis ne sont
  récupérés que si immédiatement disponibles. Vérifier manuellement les
  informations et les références utilisées, sans transformer cette
  vérification documentaire en développement de tests.
- Une exception exige une **demande explicite de Léon** visant spécifiquement
  des tests ou de la maintenance logicielle. Un simple « continue » ou
  « vérifie » **n'autorise pas** les tests.

## Cadence obligatoire de collecte brute par lots (demande du 10 novembre 2026)

Léon privilégie la **vitesse et la matière brute** aux fiches longues et polies.
**Traiter 10 à 30 cours ou sources par passe**, avec la priorité absolue
aux codes musicaux déjà inventoriés, particulièrement les 181 au stade catalogue.

- Consigner dans docs/raw-batches un tableau court : code exact, édition,
  URL institutionnelle, type de preuve, matière/lecture/exercice identifié,
  et limite de la source. Un document brut par lot suffit.
- Ne pas réécrire des pages de présentation, faire de la mise en forme
  sophistiquée, ni créer une fiche longue pour chaque résultat immédiatement.
  Conserver les documents originaux via leurs liens; noter sans spéculation.
- Quand aucune matière réelle propre au cours n'est accessible, noter
  « catalogue seulement », passer au cours suivant et ne pas combler le
  vide par le syllabus d'une université voisine.
- Réserver la répartition ultérieure dans des fiches individuelles à une
  passe groupée d'intégration. Les raw-batches sont des travaux actifs,
  pas des archives. Modifier le registre uniquement si la source concerne
  vraiment le cours visé.
- **Chiffrer séparément PDF, codes abordés, vrais syllabus et statuts
  promus.** Ne pas confondre variantes linguistiques et cours distincts.
- Ne pas exécuter ni modifier de tests, CI ou logique logicielle.

Cette cadence supplante l'obligation de rédaction immédiate d'une fiche
par cours pendant la chasse aux sources; la traçabilité et l'exactitude
restent non négociables.

## Ordre de lecture obligatoire

1. [README.md](README.md) — mission, état réel, commandes.
2. [docs/OBJECTIVES.md](docs/OBJECTIVES.md) — finalité, limites, règle de progression.
3. [docs/university-curriculum.md](docs/university-curriculum.md) — union des
   enseignements UdeM/McGill/Berklee, **y compris options et recommandations**.
4. [docs/course-material-collection.md](docs/course-material-collection.md) —
   **procédure prioritaire pour obtenir la matière réelle de chaque cours**.
   Utiliser aussi [le suivi cours par cours](docs/data/course-material-progress.json)
   pour choisir l'élément suivant sans reprendre le travail accompli.
5. [docs/knowledge-base.md](docs/knowledge-base.md) — comment, **ensuite**,
   réconcilier les enseignements en connaissances communes et exploitables.
6. [docs/todo-university-coverage.md](docs/todo-university-coverage.md) —
   **unique TODO** ; les phases analytiques restent verrouillées.
7. [docs/README.md](docs/README.md) — index des inventaires de cursus.

## Principes intangibles

1. **Mise en commun maximale.** Les programmes sont des *sources de savoir*,
   pas des parcours de crédits à reproduire. Rassembler les apprentissages
   distincts des cours obligatoires, optionnels, recommandés et pertinents
   des majeures voisines ; consigner la provenance et les différences de
   traditions. Ne jamais présumer qu'un cours d'une autre majeure est
   administrativement admissible comme option.
2. **La connaissance est l'actif central.** Construire des concepts musicaux
   versionnés, reliés par prérequis et relations, avec définition, mécanisme,
   exemples, contre-exemples, exceptions stylistiques et références de cours.
   Ne pas multiplier artificiellement les concepts identiques ; ne pas
   écraser des désaccords ou des règles valables dans des contextes différents.
3. **Priorité absolue à la matière des cours.** Pour l'instant, recueillir
   systématiquement les syllabus, objectifs détaillés, chapitres, lectures,
   travaux et exemples de **tous** les cours pertinents, options incluses.
   Une description de catalogue ne vaut pas un contenu de cours obtenu.
   **Ne pas développer de nouvel analyseur ni lancer d'étude expérimentale**
   avant la fin vérifiée de cette phase et une décision explicite de Léon.
   Ensuite seulement, déterminer les capacités nécessaires pour détecter
   dans des **MIDI existants** les composants enseignés, avec provenance,
   hypothèses explicables et possibilité de conclure `inconnu`.
4. **Composition interdite pour l'instant.** Aucun projet de composition
   générative autonome tant que les portes **L01–L05** du TODO n'ont pas été
   expertisées et explicitement levées par Léon. Aucun prototype de
   composition ou d'analyse ne doit être commencé pendant la collecte.
5. **Pas de savoir inventé.** Une page de catalogue ne vaut pas syllabus ;
   un syllabus ne vaut pas apprentissage maîtrisé ; une implémentation ne vaut
   pas validation. Consigner les contenus indisponibles et les incertitudes.
6. **Documentation vivante.** Pas de dossier `archive` ni de documentation
   morte : remplacer la source canonique quand elle évolue et supprimer les
   anciens essais qui ne servent pas la collecte académique. Ne pas confondre
   une expérimentation passée et une connaissance enseignée.

## Protocole concret de travail

1. Lire `main`, les derniers commits, le TODO et la procédure de collecte ;
   conserver les changements d'autrui.
2. Choisir le **prochain cours non documenté** dans
   [le registre](docs/data/course-material-progress.json), en privilégiant
   les obligatoires puis en couvrant **toutes** les options et les choix
   non encore dépliés ; ne pas sauter les cours difficiles.
3. Traiter la chaîne active `établissement → programme → cours → syllabus →
   objectifs/chapitres/exercices/lectures → source et statut d'accès`.
4. Répertorier la matière **sans inventer de syllabus** et sans prétendre
   que la présence d'un intitulé de cours constitue une connaissance acquise.
5. Créer/mettre à jour la fiche de matière, son état dans le registre et
   le TODO. **Ne pas écrire, modifier ou exécuter de tests et ne pas intervenir
   sur la CI** : voir l'interdiction explicite ci-dessus. La vérification
   des sources et la cohérence des fiches se font directement par lecture.
6. Rapporter séparément **cours recensés / contenus obtenus / contenus
   vérifiés / contenus indisponibles** et les prochains cours à traiter.
7. **Poursuivre de cours en cours tant que des sources accessibles restent
   à examiner** ; ne pas stopper après un seul cours pour demander quoi faire.
   Si un cours est bloqué, conserver son état puis traiter le suivant.

**En cas de conflit**, [docs/OBJECTIVES.md](docs/OBJECTIVES.md) définit le
but ; [docs/university-curriculum.md](docs/university-curriculum.md) définit
le périmètre ; [docs/course-material-collection.md](docs/course-material-collection.md)
définit la tâche actuelle ; [docs/todo-university-coverage.md](docs/todo-university-coverage.md)
ordonne le travail ; [docs/knowledge-base.md](docs/knowledge-base.md)
décrit la phase suivante. Demander une décision explicite avant de commencer
les analyseurs ou de franchir la porte de composition.
