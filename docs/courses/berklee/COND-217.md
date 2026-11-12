# COND-217 — Conducting 2 with Live Keyboard Ensemble

Sources publiques consultées le 10 novembre 2026.

## Cours recensé

Travail avec solistes, mesures changeantes, collaboration et rubato, avec un volet de direction sur une séquence de film. Répertoire indicatif, dont des œuvres de Stravinsky. [Source institutionnelle](https://college.berklee.edu/courses/cond-217).

## Support pédagogique comparable

Le plan M-SK 0992, Boston Conservatory, H24, donne des exemples de préparation de conducteur, d’accompagnement vocal et d’organisation des répétitions. Les consignes de synchronisation à l’image propres à COND-217 restent à obtenir. [Support consultable](https://apolyakov.com/wp-content/uploads/2025/01/Spring-2024-M-SK-0992-5-Conducting-2-1.pdf).

## Lacunes

Le support comparable a sa propre provenance. Le plan de section, le répertoire, les consignes détaillées et les barèmes du cours recensé restent à obtenir.


## Application à l'analyse et à la création — première évaluation par apprentissage (12 novembre 2026)

**Cours :** COND 217. **Apport : direct à l'analyse et à la création pour au moins une technique identifiable**. **Preuve :** [Notice officielle : direction avec ensemble de claviers, solistes, rubato, changements de mesure et séquence de film; l'image et les consignes exactes ne sont pas publiées.](https://college.berklee.edu/courses/cond-217). [**MIDI original AnaMu**](./COND-217/exemple.mid) ; ce fichier n'est ni une œuvre du répertoire universitaire, ni une captation de répétition, ni un exercice assigné.

### Apprentissage 1 — Rubato et carte de tempos sur une séquence

**Preuve et applicabilité :** domaine du cours attesté, opération détaillée proposée comme exercice AnaMu, non comme consigne de section. **Catégorie :** `MIDI_DIRECT / CONTEXT_REQUIRED`.

**Détection dans une musique — procédure textuelle :** 1. Lire les événements méta `FF 51` du fichier, qui définissent les tempos à chaque frontière : 96, 112, 84, 118 et 100 noires/minute. 2. Recalculer la durée en secondes des phrases avec la carte de tempos, plutôt qu'un seul BPM global. 3. Lire aussi les signatures 4/4, 5/8, 3/4 et 4/4, puis associer les changements de tempo à leurs positions temporelles.

**Intégration dans une composition — procédure textuelle :** 1. Concevoir un court motif accompagné et noter cinq régions de tempo contrastées. 2. Programmer la carte de tempos et vérifier le déplacement des attaques en secondes; ajouter de vrais gradients intermédiaires si l'on souhaite ensuite représenter un rubato plus continu.

**Exemple MIDI, vérification et limites :** Le MIDI montre **des changements de tempo discrets**, pas un rubato continu ou une écoute réactive d'un ensemble en concert.

### Apprentissage 2 — Coordonner une image et l'orchestre (média manquant)

**Preuve et applicabilité :** domaine du cours attesté, opération détaillée proposée comme exercice AnaMu, non comme consigne de section. **Catégorie :** `CONTEXT_REQUIRED / MIDI_PROXY / AUDIO_REQUIRED`.

**Détection dans une musique — procédure textuelle :** 1. Obtenir vidéo et marqueurs image/temps, convertir timecodes en secondes. 2. Aligner des événements musicaux aux repères et mesurer les décalages; distinguer synchronisation voulue et simple coïncidence. 3. Un MIDI sans vidéo n'indique pas les événements visibles ni le contexte de la scène.

**Intégration dans une composition — procédure textuelle :** 1. Choisir trois repères visuels, écrire des entrées musicales ou changements de tempo à ces points et les vérifier contre un montage vidéo. 2. Revoir les transitions de tempo et les durées pour maintenir la fluidité musicale.

**Exemple MIDI, vérification et limites :** L'exemple n'est **pas synchronisé à un film** : aucune image n'est fournie, donc le volet cinéma reste une procédure à exécuter avec un média réel.

### Verdict et suite

- **Apport :** oui, au moins une technique utile à l'analyse et à la composition est démontrable avec des notes ou événements MIDI.
- **Apprentissages abordés :** 2 domaines du cours, sans prétendre épuiser le syllabus ni les évaluations.
- **Classification :** `MIDI_DIRECT`, `CONTEXT_REQUIRED`, `MIDI_PROXY`, `AUDIO_REQUIRED`.
- **Drapeau :** `non_algorithmique=false` sur le contenu attesté; les compétences d'écoute/d'interprétation restent signalées.
- **MIDI :** [exemple original](./COND-217/exemple.mid), non associé à une œuvre enseignée.
- **Manques :** activités et enregistrements précis de section; aucune promotion de la couverture académique.
