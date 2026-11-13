# MUSP 241 — Musicianship Training 4

Sources publiques consultées le 10 novembre 2026.

## Cours recensé

Mesures changeantes, collections atonales, modulations, instruments transpositeurs, accords chromatiques et passages à deux parties. [Source institutionnelle](https://www.mcgill.ca/music/programs/bmus/music-composition/study-plan).

## Ressource pédagogique ou contexte documenté

Le dossier de classement supérieur donne une partition à deux portées pour jouer la basse tout en chantant la mélodie à vue. Elle documente un format comparable de travail à deux parties. Les exemples de dictée et de transposition propres à MUSP 241 restent à obtenir. [Document consulté](https://www.mcgill.ca/music/files/music/music_theory_graduate_placement_exam_samples_musicianship_2016.pdf#page=2).

## Lacunes

Chercher le plan de section, les exercices, les lectures et les évaluations attribuables au cours cible.

## Application à l'analyse et à la création — première évaluation (12 novembre 2026)

**Provenance et couverture.** Cheminement McGill Composition : mesures changeantes, collections atonales, modulations, transposition instrumentale, accords chromatiques et deux voix. Aucun exercice précis de section identifié. **Apport :** directe. Évaluation limitée aux acquis attribuables à ce code : une source de classement, un programme de concert et le syllabus actuel ne sont pas interchangeables. Les procédures ci-dessous sont proposées pour AnaMu, pas annoncées comme devoirs universitaires.

### Apprentissage 1 — Reconnaître les changements de mesure en cours de phrase

**Procédure d'analyse de musique existante.** Entrée : événement MIDI Time Signature + attaques/durées. Reconstituer les bornes de mesure, recalculer les positions de temps et détecter la succession 4/4→3/4→5/8→4/4; si la signature est absente, inférer plusieurs segmentations avec incertitude.

**Procédure de création/réinvestissement.** Composer quatre mesures avec points d'appui adaptés à 4/4, 3/4, 5/8, 4/4; vérifier que la phrase reste lisible et que les accents n'exigent pas une fausse barre régulière.

**Support et démonstration.** Mesures 1–4 : événements 0xFF58 explicites dans le SMF avec 1920, 1440, 1200 et 1920 ticks respectifs. N'illustre pas les autres thèmes du cours.

### Verdict, classification et lacunes

| Critère | Décision |
|---|---|
| Apport analyse/composition | directe |
| Apprentissages couverts | 1 attesté(s), **non exhaustifs** |
| Applicabilité | `MIDI_DIRECT`, `MIDI_PROXY`, `AUDIO_REQUIRED` |
| `non_algorithmique` | false (activité musicale documentée) |
| MIDI / format adapté | [MIDI original AnaMu](./MUSP-241/exemple.mid) — démonstration pédagogique, non document du cours |
| Éléments manquants | Progression/syllabus et consignes propres à la section, œuvres ou matériels autorisés selon le cours |
| Statut de couverture académique | Inchangé : cette analyse n'établit pas un syllabus complet |

## Cas sur réduction annotée — distinguer barre écrite et battue proposée (13 novembre 2026)

**Ancrage.** La [notice MUSP 241](https://www.mcgill.ca/music/programs/bmus/music-composition/study-plan) atteste les mesures changeantes. La *Danse sacrale* du *Sacre du printemps* est un comparateur AnaMu. Les repères suivent l’édition analysée par Pieter van den Toorn, et non une renumérotation de la révision de 1943.

**Cas : Stravinsky, *Danse sacrale*, repères 142–145.** Dans l’exemple 36, Van den Toorn aligne quatre occurrences d’un matériau comprenant son motif b7. Les repères 142 et 143 donnent le placement de référence. Il lit à 144 + 4 un déplacement d’une croche sur la battue qu’il propose, puis à 145 + 4 une opposition entre placement sur le temps et hors temps. Les mesures irrégulières sont écrites. La grille régulière sous-jacente et la sensation de déplacement sont des lectures à comparer, pas des indications imprimées du même statut. [Van den Toorn, ex. 36 et commentaire, p. 94–96](https://publishing.cdlib.org/ucpressebooks/public/book/stravinsky-and-the-rite-of-spring.html).

**Analyse et réemploi.** Dresser une grille des doubles croches, inscrire les barres, puis aligner séparément les retours du motif par rythme et contour. Évaluer deux prédictions : la lecture littérale identifie les premiers temps écrits, et une battue maintenue prédit où l’occurrence suivante se déplace. Créer une phrase à mesures alternées, répéter une cellule sans changer ses intervalles ni ses durées internes, puis avancer son retour d’une subdivision. Battre un tactus constant pendant les deux versions et écouter si le décalage reste repérable sans métronome. Une carte MIDI de signatures établit les barres encodées, pas la battue perçue. **Preuve :** `MIDI_DIRECT / MIDI_PROXY / AUDIO_REQUIRED`.
