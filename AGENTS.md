# AnaMu — consignes de travail

## Mission et organisation

Construire une **base unifiée de connaissances musicales** à partir de plusieurs **programmes universitaires** de composition, cours obligatoires, **optionnels** et enseignements voisins pertinents compris. Ces connaissances doivent permettre d'**analyser** et d'expliquer des œuvres, puis éventuellement de **composer** après une décision dédiée.

Le projet contient trois ensembles de sources et un volet d’analyse indépendant :

- `docs/courses/<établissement>/<code>.md` : apprentissages sourcés, procédures d'analyse et de réinvestissement en composition. Les MIDI, audio et partitions sont dans le dossier `<code>/` du cours.
- `site/` et `scripts/build_course_site.py` : présentation web des fiches et de leurs exemples.
- `corpus/` : œuvres acquises pour l'étude, distinctes des exemples pédagogiques. [Opéra](corpus/opera/README.md) et [pop/Billboard](corpus/pop/README.md) sont intégrés. Pour la pop, le catalogue et la réacquisition sont dans le dépôt; les MIDI et paroles acquis ont été remis en paquet privé.

- `analysis/` : [mise en commun des connaissances et premier moteur d’analyse](analysis/README.md), autorisés explicitement par Léon le 21 novembre 2026. Les entrées des autres volets restent en lecture seule.

## Documents de référence

1. [README.md](README.md) : entrée du projet.
2. [État courant](docs/STATUS.md) : compteurs, capacités présentes et limites.
3. [Objectifs](docs/OBJECTIVES.md) et [référentiel universitaire](docs/university-curriculum.md) : finalité et périmètre musical.
4. [Méthode par cours](docs/course-material-collection.md) et [gabarit](docs/COURSE_ANALYSIS_TEMPLATE.md) : travail à effectuer dans les fiches existantes.
5. [Connaissances communes](docs/knowledge-base.md) : architecture et synthèses musicales sourcées.
6. [TODO unique](docs/todo-university-coverage.md) : tâches ouvertes et critères L01–L05.

Les dossiers `raw-batches/`, les audits et les pistes de sources servent de preuves datées. Leurs anciennes consignes de « prochaine recherche » ne définissent pas le travail courant. L'historique des décisions est conservé par Git, sans accumulation de bilans dans les documents de pilotage.

## Travail autorisé maintenant

Approfondir **chaque apprentissage attesté dans son cours** : expliquer comment le reconnaître dans une œuvre, comment l'employer en composition et donner des exemples ou contre-exemples localisés. Produire un véritable MIDI pédagogique original quand le phénomène est observable dans ce support; conserver les sources et les fichiers du cours. Les exemples pédagogiques ne sont pas un moteur de composition automatique.

Employer les catégories `MIDI_DIRECT`, `MIDI_PROXY`, `AUDIO_REQUIRED`, `CONTEXT_REQUIRED`, `NOT_MUSIC_ALGORITHM`, `UNKNOWN` du gabarit. Pour un phénomène acoustique, perceptif, instrumental ou contextuel, conserver la preuve manquante plutôt que fabriquer une démonstration MIDI.

L'acquisition de corpus peut se poursuivre en parallèle : MIDI originaux acquis, paroles, partie chantée identifiable, provenance, licence déclarée et limites. Distinguer fichiers, chansons, variantes, paroles disponibles, horodatages et alignements validés. Ne pas identifier la voix par le registre aigu, le timbre GM ou l'ordre supposé des pistes.

## Règles de preuve et de suivi

- Les matières musicales uniquement sont admissibles : [périmètre](docs/music-only-scope.md). Ne pas réintroduire les cours de culture générale sans objet musical.
- Une notice de catalogue n'est pas un syllabus; un exemple ne couvre pas un cours; un rendu synthétique n'est pas une audition ni une validation de jouabilité.
- Distinguer source du cours, source d'un mécanisme et cours voisin. Ne pas transférer un syllabus ou une section entre codes ou établissements.
- Conserver `UNKNOWN` ou `null` quand la matière manque. Ne pas promouvoir un statut parce qu'un exemple a été créé.
- Les 378 cours identifiables ont reçu une première évaluation. La suite est l'approfondissement des apprentissages, pas la répétition de cet audit initial.
- Les recherches publiques des 115 fiches partielles sont arrêtées en meilleur effort : 93 closes, 22 bloquées et **0 recherche cyclique active**. Réouvrir uniquement sur preuve nouvelle; les huit familles de choix restent à préciser.
- Réutiliser les études et rendus présents. Choisir les prochaines lacunes dans le TODO au lieu de régénérer les mêmes lots.
- Vérifier directement les sources, liens et fichiers modifiés. Préserver les changements d'autrui et les preuves encore utilisées.

## Limites de phase

**Le développement du volet d’analyse indépendant `analysis/` est explicitement autorisé.** Voir ses [consignes propres](analysis/AGENTS.md). En dehors de ce volet, une simple reprise documentaire n’autorise pas de moteur ni d’expérimentation logicielle. Les portes **L01–L05** restent fermées pour la composition générative de production.

**Ne pas créer, modifier ou exécuter de tests unitaires**, d'intégration ou de non-régression pendant ce travail. Ne pas modifier les validateurs, la CI ou les workflows pour faire passer une collecte au vert. Une exception exige une demande explicite visant ces travaux. Les contrôles documentaires existants ne prouvent aucune compétence musicale.

Pour décider de la prochaine tâche, lire l'état courant et le TODO, puis travailler dans les fiches ou le corpus concerné. Actualiser les compteurs seulement lorsque les registres ou les fichiers justifient le changement.
