# FILM-205 — Scoring Technology 1

Berklee College of Music, Boston. Inventaire 2026 des spécialités voisines. Admissibilité au baccalauréat Composition à confirmer. Sources publiques consultées le 10 novembre 2026.

## Cours de Boston

Piste voisine. Séquençage MIDI et audio synchronisé à l’image, contrôle des tempi et mesures, instruments virtuels, automation et mixage. [Description institutionnelle](https://college.berklee.edu/courses/film-205).

## Support pédagogique parallèle

Travaux sur les gabarits de session, les bibliothèques orchestrales, les maquettes, la synchronisation à des points précis, les sons hybrides et le mixage. [Plan public de Berklee Online](https://online.berklee.edu/courses/scoring-technology#syllabus).

## Lacunes

Le programme en ligne a son propre syllabus. Les séances, lectures, consignes et barèmes du cours de Boston restent à obtenir.

## Renvoi précis vers le syllabus en ligne (édition consultée le 10 novembre 2026)

La [fiche OCWPR-300](../berklee-online/OCWPR-300.md) détaille **12 leçons avec tâches repérables**, dont gabarit MIDI (2), maquette orchestrale (4), timecode et points de synchronisation (5), sonorités hybrides (6), cue d'action programmé (7), mixage compatible avec le dialogue (10) et livraison en stems (12). Les familles de matière sont voisines de la notice officielle FILM-205 ; **aucune de ces semaines ni consignes n'est attribuée au cours Boston**. Le syllabus Boston de FILM-205 reste à chercher auprès de sa section.

## Autre syllabus de comparaison : réalisme de la maquette

La [fiche de deuxième cycle OCOMP-507](../berklee-online/OCOMP-507.md) recense **11 travaux publics** sur dynamiques, articulation des vents/cuivres/cordes, latence des échantillons, réverbération, routage et stems ; elle renforce le répertoire de méthodes audio à examiner, sans constituer des travaux de FILM-205. La recherche du vrai syllabus de FILM-205 reste nécessaire.


## Application à l'analyse et à la création — étude du contenu attesté (11 novembre 2026)

**Apport : direct aux compétences d'analyse et de création.** [Notice institutionnelle du cours](https://college.berklee.edu/courses/film-205) ; [exemple MIDI original pour AnaMu](./FILM-205/exemple.mid) — **pas un exercice, ni une œuvre du professeur**.

### Apprentissage : Synchronisation de cue par tempo, mesures et hit point

**Procédure d'analyse MIDI :** 1. Convertir la timebase PPQ et les événements de tempo en secondes cumulées. 2. Lire le marqueur MIDI HIT_POINT_ORIGINAL_2 et calculer son instant. 3. Comparer cet instant à une liste d'images/timecodes fournie séparément pour mesurer l'écart du cue. 4. Ne pas inférer un film ou une synchronisation effective de la seule séquence MIDI.

**Procédure de composition :** 1. Définir un hit point à six noires et une énergie recherchée. 2. Écrire une montée de texture et modifier le tempo à quatre noires. 3. Placer une attaque forte au marqueur, puis calculer sa position réelle en secondes. 4. Rendre un mixage et comparer à la vidéo source.

**Illustration, limites et faux positifs :** Le fichier donne un exemple original de changement de tempo et de marqueur, pas de piste vidéo ni de vrai timecode externe; les outils de mixage et le rendu audio ne sont pas dans MIDI.

**Classification :** `MIDI_DIRECT, CONTEXT_REQUIRED, AUDIO_REQUIRED`. **Verdict :** `non_algorithmique=false` sur cet apprentissage musical; les autres sujets du cours ne sont pas déclarés couverts par cette unique démonstration.
