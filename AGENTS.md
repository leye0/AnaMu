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

## Ordre de lecture obligatoire

1. [README.md](README.md) — mission, état réel, commandes.
2. [docs/OBJECTIVES.md](docs/OBJECTIVES.md) — finalité, limites, règle de progression.
3. [docs/knowledge-base.md](docs/knowledge-base.md) — **comment transformer les
   cursus en connaissances communes**, traçables et exploitables.
4. [docs/university-curriculum.md](docs/university-curriculum.md) — union des
   enseignements UdeM/McGill/Berklee, **y compris options et recommandations**.
5. [docs/todo-university-coverage.md](docs/todo-university-coverage.md) — **unique
   TODO** ; ne coche rien sans dossier de preuves complet.
6. [docs/roadmap.md](docs/roadmap.md) et
   [docs/research-evidence-gates.md](docs/research-evidence-gates.md) — code
   réellement disponible, tests indépendants et seuils d'affirmation.
7. [docs/README.md](docs/README.md) — index des audits et études spécialisés.

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
3. **L'analyse utilise cette connaissance.** Chaque capacité du moteur doit
   relier une observation de partition/MIDI/audio à des concepts traçables,
   produire des hypothèses musicales explicables et accepter `inconnu`.
   Les tests sur données synthétiques ne prouvent pas une maîtrise académique.
4. **Composition interdite pour l'instant.** Aucun projet de composition
   générative autonome tant que les portes **L01–L05** du TODO n'ont pas été
   expertisées et explicitement levées par Léon. Les reconstructions de notes
   masquées existantes sont des diagnostics d'analyse seulement.
5. **Pas de savoir inventé.** Une page de catalogue ne vaut pas syllabus ;
   un syllabus ne vaut pas apprentissage maîtrisé ; une implémentation ne vaut
   pas validation. Consigner les contenus indisponibles et les incertitudes.
6. **Documentation vivante.** Pas de dossier `archive` ni de documentation
   morte : mettre à jour la source canonique et supprimer prudemment les
   documents devenus inutiles. Préserver les données et preuves utilisées.

## Protocole concret de travail

1. Lire `main`, les derniers commits/CI, le TODO et les contrats concernés ;
   conserver les changements d'autrui.
2. Choisir une lacune **musicale et pédagogique** établie par un cours, pas
   un indicateur mathématique facile à améliorer.
3. Traiter la chaîne `programme → cours → objectif/chapitre → concept
   académique unifié → sous-compétence → mécanisme d'analyse → preuve`.
4. Ajouter sources, droits, variantes de contexte, exemples positifs,
   négatifs et preuves indépendantes avant toute revendication de réussite.
5. Mettre à jour la documentation canonique et les tests ; exécuter au moins
   `python scripts/validate_project_docs.py` et
   `python -m unittest discover -s tests -p 'test_*.py'`.
6. Rapporter séparément **inventorié / modélisé / implémenté / testé /
   validé par des experts**, les incertitudes et les travaux restants.

**En cas de conflit**, [docs/OBJECTIVES.md](docs/OBJECTIVES.md) définit le
but ; [docs/knowledge-base.md](docs/knowledge-base.md) définit le patrimoine
de connaissances ; [docs/university-curriculum.md](docs/university-curriculum.md)
définit le périmètre ; [docs/todo-university-coverage.md](docs/todo-university-coverage.md)
ordonne le travail ; les données, tests et revues expertisées déterminent ce
qui est réellement prouvé. Demander une décision explicite avant de changer
le but ou de franchir la porte de composition.
