# OEART-119 — Ear Training 1

**Berklee Online, 3 crédits, cours de 12 semaines.** Auteur : **Allan Chase et Roberta Radley**. Relevé du 10 novembre 2026. **Syllabus public réel structuré ; leçon complète et barème non obtenus.**

## Provenance et portée

- [Page officielle, sections « Syllabus » et « Requirements »](https://online.berklee.edu/courses/ear-training-1#syllabus) : progression par leçon et activités réellement affichées ; ne pas confondre avec le campus Boston ou l'UdeM/McGill.
- **Objectif du cours :** Solfège mobile, direction rythmique, reconnaissance d'intervalles et dictées en tonalités majeures. Le parcours relie notes entendues, partition, chant et harmonie fonctionnelle.

## Plan pédagogique public (résumé original)

| Leçon | Matière étudiée | Exercice ou exemple identifié |
|---|---|---|
| 1 | Do mobile, gamme majeure, seconde mineure et direction de la mesure | Chant et reconnaissance du mètre |
| 2 | Subdivisions en 4/4, clé de fa et seconde majeure | Lire rythmes ; composer, transposer et chanter une mélodie |
| 3 | Sauts de l'accord I, tierce majeure et notation 4/4 | Dictée rythmique et chant |
| 4 | Notes attractives, tierce mineure et fonctions I, IV, V | Prestation en 3/4 et duo |
| 5 | Doubles croches, intervalles et V7 | Lecture rythmique et transcription mélodique |
| 6 | Révision des notions 1–5 | Évaluation médiane : performance, dictée et reconnaissance |
| 7 | Syncopes en croches, si bémol majeur et accords mineurs | Lecture chantée, dictée et reconnaissance |
| 8 | Syncopes et dynamiques, triton, accords II mineur et V sus4 | Exercices intégrés chant/transcription |
| 9 | Sixièmes, doubles croches, ré majeur et septième diminuée | Prestation et dictée |
| 10 | Signes de reprise et coda, septièmes et cycle des quintes | Analyse et dictée des fonctions |
| 11 | Révision des tonalités C, F, G, Bb, D et lien mélodie/harmonie | Lecture, chant et dictée |
| 12 | Synthèse générale des paramètres auditifs et écrits | Évaluation finale de performance puis dictée/reconnaissance |

## Lectures, activités et lacunes

- **Exigences et lectures :** Préalable : connaissances de base en théorie/notation, ou Music for Beginners, Music Theory 101, Music Theory and Composition 1. **Livres imposés :** *Ear Training 1 Workbook* (deOgburn et coll.) ; Roberta Radley, *Reading, Writing and Rhythmetic* (2016). Travaux avec enregistrements vidéo et logiciels de notation ou DAW.
- **Nature exacte des preuves :** Le plan donne **deux évaluations médianes** (prestation puis dictée/reconnaissance) et **deux examens finaux** de même type. Les critères de correction et fichiers de dictée ne sont pas publiés.
- **Cours comparables :** Les cours [UdeM MUS 1011–1012](../udem/MUS-1011.md) portent sur l'écoute tonale mais leurs contenus de niveau ne peuvent être déduits de ce syllabus en ligne.
- **Reste à obtenir :** cahier des consignes, supports d'écoute et partitions, corrigés, devoirs soumis, barèmes et édition spécifique d'une section. Les intitulés de tâches du site ne doivent pas être pris pour les énoncés intégraux.

**Réserve de phase :** cette fiche archive une **source pédagogique académique**, sans implémentation d'analyse musicale et sans création de tests logiciels.

## Application à l’analyse et à la création — résolution indirecte et accent de phrase (13 novembre 2026)

**Preuve du cours.** Le [plan public OEART-119](https://online.berklee.edu/courses/ear-training-1#syllabus) traite les degrés attractifs du majeur (leçon 4), puis syncope en croches et résolutions indirectes (7–8). Le plan cite ces matières séparément. Leur combinaison à l'échelle d'une phrase est une proposition AnaMu.

### Q1 — Intercaler une note sans déplacer l’arrivée harmonique

**Analyse.** Dans l'[exemple MIDI original](./OEART-119/exemple.mid), comparer m. 1–4 et m. 5–8. À m. 2 et m. 6, la voix aiguë attaque si au troisième temps sur un support sol–ré–sol. Dans A, si se maintient jusqu'au do sur le premier temps de m. 3. Dans B, ré s’intercale au quatrième temps avant le même do, m. 7. L’appui sol → do arrive au même moment. A montre une succession si → do contiguë, B un geste si–ré–do. Décrire B comme une résolution **indirecte candidate** à l'échelle de la ligne, pas comme un déplacement de la cadence ni une obligation de réduire tout passage si–ré–do à si → do.

**Création.** Modifier seulement la ligne aiguë en gardant début du si, instant d’arrivée et accompagnement. Si l'on change aussi l'arrivée de la basse, on ne peut plus distinguer détour mélodique et report harmonique. **Preuve :** `MIDI_DIRECT` pour la différence d'événements, `AUDIO_REQUIRED` pour la force d’attraction perçue.

### Q2 — Une attaque anticipée ne déplace pas forcément le temps fort

**Analyse.** Noter les attaques faibles qui se prolongent au-dessus d'un temps fort. Les comparer aux appuis de basse et à la subdivision stable sur les deux mesures voisines. Si le temps fort reste repérable et la note accentuée a commencé avant lui, lire une syncope relative à ce cadre. Si les parties se décalent ensemble ou si le cadre lui-même change durablement, considérer un autre placement métrique. Une attaque isolée hors grille ne suffit pas à établir une syncope.

**Création.** Réutiliser A sur papier et avancer seulement le do mélodique d'une croche, en le tenant au travers du premier temps de m. 3. La basse entre toujours sur ce temps. Comparer cette version à celle où basse et mélodie anticipent ensemble. Cette variante métrique **n'est pas encodée dans le MIDI joint**. **Preuve :** `MIDI_PROXY` pour la syncope si le mètre est établi, audio pour le placement ressenti.
