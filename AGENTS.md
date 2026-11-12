# AnaMu — contrat de reprise pour tout agent

**ÉTAT CANONIQUE — 11 novembre 2026 :** [registre des 386 entrées](docs/data/course-algorithmic-assessments.json) : **63 cours avec au moins un apprentissage analysé et un MIDI original**, **18 cours évalués sans MIDI pertinent ou suffisamment sourcé**, **297 cours restant à évaluer**, **8 familles de choix**. **Dernier lot vérifié : 15 nouveaux exemples MIDI et 10 nouvelles analyses sans MIDI.** Deux cours seulement sont provisoirement flaggés `non_algorithmique=true`; un cours sans exemple MIDI n'est donc **pas** automatiquement non algorithmique. Le site Pages est généré depuis les fiches et ce registre; le gabarit reste [COURSE_ANALYSIS_TEMPLATE.md](docs/COURSE_ANALYSIS_TEMPLATE.md). **Continuer les cours par lots** en séparant objectifs attestés, méthodes de détection/création et limites; les 44 mécanismes généraux ne sont plus la priorité. Tous les comptes antérieurs plus bas sont historiques, pas des états actuels.

**PROGRESSION RECONCILIÉE DU GABARIT, 11 novembre 2026 :** [registre d'analyse des 386 entrées](docs/data/course-algorithmic-assessments.json) = **30 premières analyses de cours avec MIDI original réel**, **6 évaluations sans MIDI pertinent** (spectromorphologie, clinique, médiation, métier, philosophie/contextes, notation), **342 cours non encore analysés**, **8 placeholders de choix**. **2 cours flaggés `non_algorithmique=true`** sur les apprentissages connus; les limites de preuve restent inscrites. Les MIDI sont dans `docs/courses/<établissement>/<code>/exemple.mid`, et les procédures sont **directement dans la fiche existante du cours**. Cette directive de cours *prime* sur l'ancien objectif de 44 « mécanismes » généraux. [Gabarit](docs/COURSE_ANALYSIS_TEMPLATE.md). **Ne pas confondre un apprentissage démontré et un syllabus entièrement traité.**

## DIRECTIVE ACTIVE — analyse/création de CHAQUE cours (11 novembre 2026)

**L'utilisateur a explicitement demandé l'étape suivante** : pour chaque cours musicologique concret, 1) vérifier l'apport réel aux compétences d'analyse et de création musicales, 2) pour **chaque apprentissage prouvé**, écrire la procédure d'analyse (MIDI, audio ou contexte selon ce qui est observable), 3) écrire la procédure de réinvestissement en composition et **créer un véritable MIDI original** seulement lorsque cela représente effectivement l'apprentissage, 4) flagger `non_algorithmique` lorsqu'aucun algorithme musical pertinent ne ressort de la matière attestée. Les catégories `MIDI_DIRECT`, `MIDI_PROXY`, `AUDIO_REQUIRED`, `CONTEXT_REQUIRED`, `NOT_MUSIC_ALGORITHM`, `UNKNOWN` évitent les faux positifs. **Cette autorisation ciblée de produire des exemples MIDI et leur analyse remplace les anciennes interdictions générales de MIDI dans le travail documentaire**; elle n'autorise PAS des tests, de la CI, un moteur complet ni de la composition automatique de production. La documentation autonome des 44 « mécanismes » généraux de 1B **n'est pas le travail prioritaire demandé** et ne doit pas être poursuivie à la place des cours.

**Implémentation minimale :** [gabarit](docs/COURSE_ANALYSIS_TEMPLATE.md), [index de suivi exhaustif des 386 entrées](docs/data/course-algorithmic-assessments.json) et rédaction **dans la fiche de cours existante** `docs/courses/<établissement>/<code>.md`; ranger l'exemple MIDI original dans un dossier nommé par ce cours. **Bilan initial honnête :** 19 cours avec un apprentissage analysé + MIDI original, 5 évaluations à limites/non algorithmiques sans MIDI, 354 cours non encore évalués, huit placeholders Berklee. **Ne pas annoncer 386 cours analysés**. Continuer de traiter par lots de cours, sans créer des dossiers de rapports génériques supplémentaires. Les **115 cartes de matière partielle** le restent, les 22 recherches de syllabus bloquées ne sont pas relancées. [Bilan actuel](docs/STATUS.md).

**PROCHAINE ACTION 1B ET COMPTE ACTUEL :** [30 mécanismes réellement documentés dans le second lot](docs/subject-research/2026-11-11-batch-02-thirty-mechanisms-counterpoint-orchestration-jazz-rhythm.md) et [index source/par mécanisme](docs/data/subject-research-batch-02-30-mechanisms-2026-11-11.json). Avec les 14 premiers : **44 mécanismes documentés**, pas 44 cours universitaires complétés. Poursuivre par lots de 10–30 sujets diversifiés, en privilégiant de nouvelles sources indépendantes et les limites de style. **Ne pas rouvrir les 22 syllabus bloqués sans preuve concrète**, ne pas modifier les 115 `partial`, pas de tests/CI ni moteur.

## CONSIGNE OPÉRATIONNELLE PRIORITAIRE — 11 novembre 2026 : STOP aux recherches en boucle

**Nouveau bilan canonique :** [docs/STATUS.md](docs/STATUS.md), [22 blocages précis et 8 choix de programme](docs/phase1a-public-evidence-stop-2026-11-11.md). **263 cartes de cours utilisables, 115 partielles** (93 recherches publiques achevées en meilleur effort, 22 BLOQUÉES pour manque de preuve externe), **8 placeholders de choix; 0 recherche de syllabus ouverte**. Un agent ne doit plus recommencer les 22 recherches, ni les 93 premières, ni tenter de compléter une grille d'instruments au hasard. **Phase 1A : recherche publique arrêtée en meilleur effort, lacunes conservées. Phase 1B ACTIVE : documenter les sujets musicaux réellement repérés**, en lots substantiels de 10–30, avec sources académiques vérifiées, mécanismes précis, fonction musicale et limites. [14 mécanismes documentés](docs/subject-research/2026-11-11-first-14-music-theory-mechanisms-primary-educational-sources.md) dans le premier lot. **Ne jamais faire passer une source sur un sujet pour le syllabus d'un cours**. Les anciens comptes et consignes plus bas (1A seule active, 22 actifs, 93/22 à rechercher) sont historiques, pas applicables. **Phase 2, moteurs MIDI, tests/CI et composition toujours interdits.**

**ÉTAT ACTUALISÉ — seconde passe du 11 novembre 2026 :** [les 28 recherches actives ont été réexaminées](docs/raw-batches/2026-11-11-revisit-28-active-primary-evidence-and-six-closures.md); **six recherches publiques supplémentaires ont été clôturées en meilleur effort**. Nouveaux nombres opérationnels : **93 recherches terminées, 22 encore actives, huit familles non dépliées**. Les **115 descriptions pédagogiques restent partielles** et les **263 cartes utilisables sont inchangées**. [Quatre niveaux réels de leçons de basse Berklee PIBS](docs/raw-batches/2026-11-11-berklee-pibs-four-concrete-private-bass-levels.md) viennent d'être intégrés aux 4 familles PIxx, soit 32 codes candidats d'instruments (huit disciplines × quatre niveaux), sans fermer les familles. **Cette note remplace les anciens comptes opérationnels 87/28 dans les bilans historiques plus bas.** Aucune phase de test/code, aucun transfert de matière non attribuable.

## NOUVELLE RÈGLE — clôturer une recherche bloquée sans prétendre connaître la matière (11 novembre 2026)

**Distinguer deux axes.** `topic_outline.state` mesure les sujets réellement documentés (`usable_first_pass` ou `partial`). Un nouveau champ **`topic_outline.public_research.state`** mesure **uniquement la progression de recherche sur les sources publiques**. Quand le catalogue et les recherches ciblées n'offrent plus de plan/relevé de section attribuable au cours, surtout pour un instrument individuel, un ensemble à répertoire variable ou un tutorat/stage personnalisé, enregistrer **`completed_best_effort`** : la recherche en sources publiques est **terminée pour cette passe**. Conserver `topic_outline.state="partial"` et l'ancien `status` sans promotion. Préciser le motif et les sources, et réouvrir si une source plus précise apparaît.

**Audit daté du 11 novembre 2026 :** [87 recherches publiques clôturées (matière toujours partielle)](docs/raw-batches/2026-11-11-public-search-closure-87-partial-courses.md), [28 recherches actives sur les 115 cours partiels](docs/remaining-115-course-evidence-queue-2026-11-11.md), **8 familles encore ouvertes**. La collecte doit désormais privilégier les 28 actifs et le dépliage des familles au lieu de reconsulter indéfiniment les 87 notices pauvres. **Ne jamais lire « terminé » comme une certification de couverture, de syllabus ou de savoir acquis.**

**Lis ce fichier avant de modifier le projet.** Il résume les décisions
fondamentales ; les liens ci-dessous désignent les documents normatifs.

## FILTRE MUSICAL OBLIGATOIRE — DÉCISION DU 10 NOVEMBRE 2026

**NE PLUS collecter de cours sans objet musical explicite.** Art visuel,
culture générale, littérature, sociologie, psychologie ou santé générales
sont exclus de la recherche musicale même s'ils font partie du diplôme.
Seules les matières traitant de musique (y compris son acoustique,
cognition, histoire, pratiques, production, industrie du musicien) sont
admissibles. [Liste des 16 entrées et 11 candidats supprimés](docs/music-only-scope.md).
**Périmètre courant : 386 entrées**, dont 263 exploitables, 115 partielles,
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

### État actuel du registre musical filtré — 11 novembre 2026

**386 entrées**, dont **378 cours identifiables et huit familles musicales** à
déplier. **263 cartes initiales exploitables** et **115 descriptions
partielles** restent dans la phase 1A. Le précédent inventaire académique
de 402 entrées, dont les familles d'options générales, est un historique
et **ne doit pas être restauré**. Voir
[docs/topic-outline-coverage-status.md](docs/topic-outline-coverage-status.md).

**Prochaine action :** améliorer les 115 descriptions musicales partielles
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
