# AnaMu — connaissance universitaire pour analyser la musique

**Mission :** construire une immense base commune de connaissances musicales à partir de **toute la matière réellement enseignée** dans plusieurs programmes universitaires de composition, y compris les options, les recommandations et les spécialisations pertinentes. Ensuite, choisir les outils capables de **reconnaître et expliquer dans des morceaux MIDI existants** les composants enseignés. La composition musicale générative est une possibilité lointaine, interdite sans décision explicite de Léon.

## Phase active : obtenir les cours

**Aucun développement d'analyseur n'est autorisé actuellement.** L'ordre est strict :

1. Inventorier les programmes et **tous** les cours pertinents, y compris les choix ouverts.
2. Obtenir pour chaque cours le syllabus ou plan détaillé, les objectifs, chapitres, lectures, exercices, exemples et critères d'évaluation.
3. Conserver les sources, versions, droits et **lacunes explicites** sans jamais inventer de matière.
4. Après seulement, réconcilier les enseignements en concepts musicaux unifiés et sourcés.
5. Après la connaissance, décider quels éléments sont détectables dans le MIDI existant, construire les analyseurs et vérifier leur justesse.

Une description de catalogue n'est **pas** le contenu d'un cours. Une métrique sur un corpus n'est **pas** une compétence musicale acquise.

**Cycle autonome du prochain agent :** ouvrir
[le registre de progression cours par cours](docs/data/course-material-progress.json),
prendre le premier contenu non documenté, créer une fiche de matière sourcée
selon [le protocole](docs/course-material-collection.md), mettre à jour le
registre, puis poursuivre systématiquement. Les longues recherches et
rédactions sont le travail principal ; **aucun test algorithmique ni
développement MIDI pendant cette phase**.

## État honnête — 10 novembre 2026

- **Université de Montréal :** 190 entrées de catalogue recensées, dont 168 hors tronc obligatoire ; matière détaillée non collectée exhaustivement.
- **McGill :** 58 cours ou choix nommés recensés ; branches ouvertes et syllabi à approfondir.
- **Berklee :** 44 lignes de grille, dont des ensembles d'options encore à détailler.
- **Options voisines :** 30 pistes de savoir supplémentaires, non validées au niveau des contenus.
- **Suivi opérationnel :** [332 codes de cours candidats et 5 ensembles
  d'options encore à détailler](docs/data/course-material-progress.json),
  13 avec un syllabus public documenté (dont un nouveau plan historique UdeM MUS 4106), 178 avec des preuves partielles ou des supports parallèles, et 141 au statut catalogue, après la passe documentaire du 10/11 novembre. Les fiches datent chaque plan et distinguent les équivalents et les éditions historiques.
- [Options de majeure Berklee](docs/berklee-major-elective-candidates.md) — 83 codes candidats repérés dans cinq familles, dont 70 hors du registre initial.
- [Pistes de recherche et d’accès aux supports](docs/course-material-source-trail.md) pour UdeM, McGill et les options de Berklee.
- **Base unifiée :** non construite. **Analyseur MIDI académique :** non construit. **Composition :** verrouillée.

Ce sont des **inventaires administratifs**, pas des attestations de connaissance.

## Reprendre le projet de zéro

Tout nouvel agent commence par [AGENTS.md](AGENTS.md).

1. [Objectifs, phases et interdictions](docs/OBJECTIVES.md)
2. [Périmètre universitaire](docs/university-curriculum.md)
3. [Protocole de collecte du contenu des cours](docs/course-material-collection.md)
4. [Conception de la future base de connaissances](docs/knowledge-base.md)
5. [TODO unique avec cases à cocher](docs/todo-university-coverage.md)
6. [Index des inventaires académiques](docs/README.md)

## Vérification documentaire

Le dépôt contient les inventaires académiques, leurs sources structurées et des contrôles de cohérence. **Il ne contient pas de bancs d'essai autonomes ni de moteur d'analyse actif.**

Exécuter :

    python scripts/validate_project_docs.py

Ce contrôle facultatif vérifie la cohérence des inventaires, pas que la
matière des cours a été obtenue ou maîtrisée. La CI l'exécute automatiquement.
