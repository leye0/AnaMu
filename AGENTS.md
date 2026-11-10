# AnaMu — contrat de reprise pour tout agent

**Lis ce fichier avant de modifier le projet.** Il résume les décisions
fondamentales ; les liens ci-dessous désignent les documents normatifs.

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
syllabus vérifié, chercher les sources, documenter ses chapitres/exercices,
enregistrer les lacunes, puis passer au cours suivant. C'est un **travail
documentaire approfondi**, sans développement expérimental, benchmark
algorithmique ni test musical à cette étape.

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
   le TODO. **Aucun test algorithmique n'est demandé.** Le contrôle
   documentaire `python scripts/validate_project_docs.py` reste facultatif
   en local et est vérifié automatiquement par la CI.
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
