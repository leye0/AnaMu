# OCOMP-507 — Orchestral Mockups in Film Scoring

**Établissement et édition :** Berklee Online, cours de niveau maîtrise, 3 crédits (Berklee Online), cours écrit par **Andreas Bjørck**. Relevé public du 10 novembre 2026. **Un vrai plan détaillé de douze leçons a été consulté, mais non les cours intégraux et barèmes.** Le présent code est distinct des cours du campus Berklee Boston (CM, FILM) et n'entre pas automatiquement dans leurs crédits de majeure Composition.

## Preuve pédagogique

- [Source primaire : page officielle OCOMP-507, rubrique « Syllabus », « Requirements » et « Instructors »](https://online.berklee.edu/courses/orchestral-mockups-in-film-scoring#syllabus).
- **Objectif et matière :** Fabriquer une maquette orchestrale vraisemblable avec des échantillons, du MIDI expressif, une gestion exacte des articulations et des traitements spatiaux. Cours de réalisation audio, pas de théorie de l'orchestration acoustique à lui seul.

## Séquence réelle du syllabus, résumée sans reproduction des leçons

| Leçon | Matière ou tâche explicitement annoncée |
|---|---|
| 1 | Échantillonnage orchestral, rappels MIDI, finalité d'une maquette ; devoir 1 : contrôle des nuances. |
| 2 | Gabarit de session et réverbération auxiliaire ; devoir 2 : petite configuration d'orchestre virtuel. |
| 3 | Échantillons et articulation des bois ; égalisation et réverbération ; devoir 3 : séquence de bois. |
| 4 | Cuivres et voix orchestrales, phénomène de son d'orgue des masses de cuivres et de bois ; devoir 4 : cuivres doux. |
| 5 | Percussions, harpe et piano, effets de pièce et d'égalisation ; devoir 5 : séquence avec ces instruments. |
| 6 | Cordes courtes, articulations et délais négatifs pour compenser la latence des échantillons ; devoir 6 : phrases courtes de cordes. |
| 7 | Cordes longues, legato, divisi et traits rapides ; délai de prédéclenchement des samples ; devoir 7 : cordes longues. |
| 8 | Réverbération de plateau vs de salle ; micros multiples et mélange de bibliothèques ; devoir 8 : configuration de la salle. |
| 9 | Architecture du gabarit et gestion des articulations ; devoir 9 : gabarit du projet final. |
| 10 | Panoramique stéréo, routage, bus et stems ; devoir 10 : travail de panorama. |
| 11 | Mixage, gain staging, traitement du bus master et livraison des stems ; devoir 11 : projet final. |
| 12 | Contrôleurs tactiles et configurations de serveurs hôtes ; intégration de Vienna Ensemble Pro ; aucun devoir autonome nommé. |

## Prérequis, matériel, lectures, travaux et limites

- **Prérequis et supports exigés :** Prérequis : diplôme de premier cycle pour l'inscription à ce cours de maîtrise, connaissances de Film Scoring 101 ou équivalent, lecture de partitions transposées, MIDI (velocité et contrôleurs), routage DAW et fonctionnement des instruments orchestraux. Lectures **recommandées**, pas requises : Paul Gilreath, *The Guide to MIDI Orchestration* (4e, 2010) ; Andrea Pejrolo, *Acoustic and MIDI Orchestration for the Contemporary Composer* (2e, 2016).
- **Exercices et évaluation :** **Onze devoirs titrés sont directement publiés**, associés aux leçons 1–11 ; le plan ne nomme aucun devoir pour la leçon 12. Les sessions audio, consignes complètes, maquettes et barèmes ne sont pas publics.
- **Relation aux autres cours :** Le rapprochement utile avec [FILM-205 Boston](../berklee/FILM-205.md) tient au séquençage et aux instruments virtuels. Ne pas confondre niveau, crédits et objectifs : OCOMP-507 est un cours en ligne **de deuxième cycle**.
- **Matériel absent :** fichiers d'enregistrement, partitions d'étude intégrales, contenu vidéo, consignes détaillées, corrections, critères de notes, copies d'étudiants et confirmation de chaque session. Le programme rendu public en ligne n'atteste pas la même progression pour un cours homonyme du campus Boston.

**Nature de la preuve :** syllabus public consulté et structuré pour **OCOMP-507** uniquement. Aucune analyse MIDI, écriture de logique ou test logiciel n'a été réalisé.

## Application à l'analyse et à la création — du geste écrit à l'articulation entendue (13 novembre 2026)

**Preuve du cours.** Le [plan public OCOMP-507](https://online.berklee.edu/courses/orchestral-mockups-in-film-scoring#syllabus) documente la latence des cordes courtes et le prédélai de legato (leçons 6–7), les réverbérations de plateau et de salle et le mélange des bibliothèques (8), puis la gestion d'articulations, le routage et les stems (9–11). Les comparaisons proposées sont des études AnaMu pour maquette virtuelle, sans extrapolation à un orchestre réel.

### Q1 — Une attaque avancée dans la session peut produire un unisson à l'écoute

**Analyse.** Sur partition, événements de session et pistes audio, aligner le temps cible, le déclenchement effectif et l'attaque audible des articulations. Définir une convention d'écoute ou de mesure adaptée aux attaques progressives et conserver une marge. Répéter sur plusieurs occurrences d'une figure. Un déclenchement de cordes avancé dans la session, malgré une attaque simultanée sur la partition, peut compenser le délai d'un échantillon. Si l'avance reste audible sur la piste isolée et dans le mix, garder l'hypothèse d'une anticipation musicale. Un décalage fixe d'export ou de piste doit être écarté avant d'interpréter la phrase.

**Création.** Rendre deux phrases de mêmes notes et nuances avec et sans compensation propre aux articulations. Vérifier si la jonction demeure groupée et si l'appui prévu ressort. **Preuve :** `AUDIO_REQUIRED` et session, un fichier MIDI seul n'établit pas le début audible.

### Q2 — Une queue de salle peut relier deux sons sans prolonger le geste instrumental

**Analyse.** Comparer pistes isolées, retours de réverbération et mix. À la jonction de deux groupes, relever les relâchements notés, la décroissance des sources et la persistance du signal réverbéré. Si le lien disparaît en écoutant sans le retour de salle, retenir une continuité spatiale plutôt qu'une note tenue. Les micros ambiants déjà inclus dans les échantillons et la résonance de l'instrument sont des explications concurrentes : mettre un seul auxiliaire en sourdine ne suffit pas à les exclure.

**Création.** Conserver articulation et silence écrit, puis varier uniquement la queue ajoutée dans une maquette. Comparer la cohérence spatiale et la netteté de la nouvelle attaque sans confondre plus de réverbération avec plus de continuité formelle. **Preuve :** `AUDIO_REQUIRED`, idéalement avec retours et pistes séparés.

### Q3 — Un changement d'articulation peut ponctuer ou redéfinir le passage

**Analyse.** Cartographier articulations effectivement jouées, transitions legato et contrastes de timbre, puis vérifier comment ils se combinent avec les accents et les frontières de phrase. Une seule note courte peut ponctuer une ligne tenue. Une alternance qui se stabilise ensuite peut faire entendre une nouvelle organisation. Contrôler la correspondance entre les commandes MIDI et la bibliothèque avant d'attribuer à la composition un changement de son qui provient d'un aiguillage erroné.

**Création.** Rendre un passage avec un contraste ponctuel, puis un passage où le nouveau mode d'attaque s'installe sur la phrase suivante. Vérifier d'abord la conformité du rendu à la partition, puis comparer la frontière entendue. **Preuve :** `AUDIO_REQUIRED` et `CONTEXT_REQUIRED` pour la correspondance commandes/articulations. Aucun MIDI ajouté : les trois distinctions nécessitent une réalisation sonore et des réglages de maquette.
