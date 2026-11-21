# AnaMu — cours de composition, exemples et corpus musicaux

AnaMu rassemble les connaissances de programmes universitaires de composition pour développer des compétences d'analyse musicale et comprendre comment employer ces connaissances en composition. Les programmes et cours servent de sources; leurs crédits ne sont pas un parcours étudiant à reproduire.

## Contenu du projet

| Ensemble | Contenu | Accès |
|---|---|---|
| Cours et compétences | Fiches sourcées par établissement et code; procédures d'analyse, usages compositionnels et limites | [Fiches](docs/courses/) · [Gabarit](docs/COURSE_ANALYSIS_TEMPLATE.md) |
| Exemples pédagogiques | MIDI originaux, rendus audio et partitions liés aux apprentissages dans les dossiers des cours | [Registre par cours](docs/data/course-algorithmic-assessments.json) |
| Site web | Bibliothèque des fiches, lecteurs d'exemples et partitions | [Site](https://www.streamlev.com/AnaMu/) · [Construction et publication](site/README.md) |
| Corpus d'opéras | MIDI acquis, extractions vocales, paroles et provenance | [Corpus](corpus/opera/README.md) |
| Corpus pop / Billboard | Acquisition gratuite de MIDI et paroles; catalogue, vérifications et cible de 2 000 chansons complètes | [Corpus pop](corpus/pop/README.md) |

L'[état courant](docs/STATUS.md) distingue les premières évaluations, la couverture des sources, les exemples et les validations encore absentes. Il est la référence des compteurs du projet.

## Volet indépendant d’analyse

Le [volet `analysis/`](analysis/README.md) met en commun tous les cours et sources et commence un moteur d’analyse de morceau. Il distingue les documents indexés, les concepts réellement rapprochés et les mécanismes implémentés. Les cours, leur site et les corpus restent ses entrées en lecture seule.

## Travail courant

Approfondir les apprentissages réellement documentés **cours par cours** : les reconnaître dans une musique existante, expliquer leur usage en composition et créer un exemple MIDI quand ce support peut les démontrer. Les [procédures](docs/course-material-collection.md) et le [TODO unique](docs/todo-university-coverage.md) guident ce travail. L'acquisition d'œuvres se poursuit en parallèle.

Une fiche, un exemple ou une première évaluation ne signifie pas que tout le syllabus du cours est couvert. Les lacunes des sources restent explicites. Les recherches publiques déjà clôturées ne sont pas relancées sans preuve nouvelle.

Le volet indépendant amorce la base de concepts communs et le moteur; l’intégration complète des connaissances reste à construire; la composition générative de production demeure verrouillée. Les MIDI pédagogiques originaux et les œuvres acquises ont des rôles et des provenances distincts.

## Repères

- [AGENTS.md](AGENTS.md) : consignes de reprise et limites de phase.
- [Objectifs](docs/OBJECTIVES.md) : finalité et organisation.
- [Index documentaire](docs/README.md) : registres, programmes et preuves conservées.
- [Connaissances communes](docs/knowledge-base.md) : architecture et synthèses musicales.

Le dépôt conserve le constructeur du site et des contrôles de cohérence documentaire. Leur réussite n'atteste ni la maîtrise des cours ni la justesse d'un analyseur. Les workflows existants et leur configuration sont décrits dans [la documentation du site](site/README.md).
