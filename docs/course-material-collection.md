# Méthode de travail par cours

L'activité courante est l'approfondissement des apprentissages dans les fiches existantes, selon [STATUS.md](STATUS.md), le [gabarit](COURSE_ANALYSIS_TEMPLATE.md) et le [TODO](todo-university-coverage.md). Les nouvelles sources enrichissent la matière sans relancer les recherches publiques closes ou bloquées.

## Unité documentaire

Une fiche correspond à un cours identifié, dans un établissement et une édition donnée : `docs/courses/<établissement>/<code>.md`. Les espaces du code deviennent des traits d'union dans les chemins. Le champ `material_file` du [registre de matière](data/course-material-progress.json) pointe vers cette fiche. Les MIDI, MP3, partitions et autres supports sont dans le dossier `<code>/` voisin.

| Information | Règle |
|---|---|
| Identité | Établissement, programme, code, intitulé, édition et section connue |
| Sources du cours | Notice, plan ou syllabus exact, date et qualité de preuve |
| Apprentissages | Thèmes, mécanismes, œuvres, exercices et prérequis réellement attestés |
| Sources complémentaires | Manuels, autres cours et références de pratique, explicitement distingués du syllabus cible |
| Procédure d'analyse | Observables dans une œuvre existante, contexte nécessaire et cas ambigus |
| Usage compositionnel | Paramètre musical travaillé, fonction recherchée et contraintes |
| Exemple | MIDI pédagogique original si pertinent, partition/audio/autre preuve sinon |
| Lacunes | Matière inconnue, sources inaccessibles, divergences ou validations manquantes |

Ne pas créer de seconde fiche pour raconter le même apprentissage. Les rapports bruts existants restent des sources; les procédures pédagogiques aboutissent dans les cours.

## Procédure d'approfondissement

1. Lire la fiche, ses sources et ses exemples avant de choisir une lacune précise du TODO.
2. Délimiter l'apprentissage effectivement enseigné. Une source du sujet peut l'expliquer sans prouver qu'un professeur particulier l'enseigne.
3. Expliquer comment le reconnaître dans une œuvre : notes, voix, rythme, forme, audio, partition ou contexte selon le cas.
4. Expliquer son emploi en composition et proposer un exemple ou contre-exemple original. Préserver les invariants d'une comparaison et nommer les paramètres modifiés.
5. Produire un vrai MIDI uniquement si ses événements rendent le phénomène démontrable. Pour perception, acoustique, geste ou jeu réel, préciser la preuve supplémentaire au lieu de simuler une validation.
6. Relire directement la source, les événements et les supports modifiés. Consigner audition et jouabilité comme inconnues sans données humaines.
7. Actualiser le registre approprié et le TODO si une preuve le justifie; passer à un autre apprentissage sans régénérer les lots déjà disponibles.

Les verdicts `MIDI_DIRECT`, `MIDI_PROXY`, `AUDIO_REQUIRED`, `CONTEXT_REQUIRED`, `NOT_MUSIC_ALGORITHM`, `UNKNOWN` sont définis dans le gabarit. Le drapeau `non_algorithmique` reste `null` lorsque la matière attestée ne permet pas de conclure.

## Statuts de matière et de recherche

- `topic_outline.state=usable_first_pass` : assez de thèmes précis pour une première carte, pas un syllabus complet garanti.
- `topic_outline.state=partial` : matière insuffisante, section variable ou détail inconnu.
- Le `status` historique du syllabus décrit le type de matière acquise; il n'est pas promu par un exemple pédagogique ou un manuel externe.
- `topic_outline.public_research.state=completed_best_effort` : recherche publique close sur les sources examinées.
- `blocked_external_evidence` : une pièce extérieure manque. Réouvrir seulement sur nouvelle preuve attribuable.

Le [suivi des 115 cartes partielles](remaining-115-course-evidence-queue-2026-11-11.md) est un inventaire de lacunes : 93 recherches closes, 22 bloquées, aucune recherche cyclique active. Une recherche terminée ne signifie pas une matière connue.

## Nouvelles sources, options et cours voisins

Vérifier le [périmètre musical](music-only-scope.md), puis l'établissement, le code, l'édition et la nature du support. Une notice officielle reste `official_catalogue` même si elle est détaillée. Les œuvres, séances et chapitres non nommés ne sont pas inventés.

Les huit familles `unresolved_pool` désignent des choix musicaux : quatre niveaux de leçons privées, labs, ensembles et options de musique/société. Étudier des codes réels sans transformer les alternatives en cours obligatoires ou reprendre les familles non musicales écartées.

Lors d'une acquisition de sources nouvelle et substantielle, une table de provenance sous `docs/raw-batches/` peut regrouper plusieurs cours. Séparer PDF obtenus, codes examinés, vrais syllabus et lacunes. Ne pas additionner leurs compteurs comme des compétences acquises.

## Limites du travail

Les fiches et les corpus alimentent une compréhension à construire; ils ne constituent pas un analyseur complet. Aucun développement de moteur, test, benchmark ni travail de CI n'est requis ou autorisé par cette méthode. La composition générative de production reste verrouillée; les exemples pédagogiques ponctuels sont autorisés.
