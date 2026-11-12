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

## Deuxième passe qualitative — preuve, méthode et réfutation (12 novembre 2026)

**Lien direct au cours :** [FILM-205 — Scoring Technology 1](https://college.berklee.edu/courses/film-205). **Portée de la preuve :** Notice FILM-205 Boston : séquençage MIDI/audio sur image, contrôle du tempo et de la métrique, instruments virtuels, automation et mixage. Les 12 leçons OCWPR-300 sont des comparateurs externes, non le contenu daté de cette section. L'analyse suivante complète la première passe; les exercices ci-dessous sont des protocoles de travail AnaMu, pas un syllabus ni une commande universitaire.

### Q1 — Calcul d'une carte de tempo avec marqueur de hit point

**Élément attesté par la notice.** Gestion de tempo, métrique et synchronisation à l'image attestée par la notice; l'exemple ci-dessous est un SMF original AnaMu, pas un exercice Berklee.

**Entrées et supports minimaux.** [MIDI original FILM-205](./FILM-205/exemple.mid), PPQ = 480, événements Set Tempo, marqueur texte HIT_POINT_ORIGINAL_2 au tick 2880; vidéo/timecode pour vérifier un cas réel.

**Détection / analyse ordonnée.** Lire la division du header et intégrer la durée en secondes par segment : tick 0→1920 à 120 BPM (4 noires, 2,0 s), puis tick 1920→2880 à 150 BPM (2 noires, 0,8 s). Le marqueur est donc à 2,8 secondes du début musical, et non à 3,0 secondes comme l'indiquerait un calcul erroné à 120 BPM constant. Puis appliquer le décalage absolu du cue dans le montage vidéo.

**Résultat falsifiable.** Événement illustratif t = 2,8 s pour 2880 ticks; décalage de −0,2 s par rapport au tempo constant. Ce calcul établit l'emplacement MIDI, **pas** le frame d'un film non joint.

**Application à une création originale.** Fixer une coupe de démonstration à 2,8 secondes d'une vidéo personnelle, créer une montée harmonique et une attaque synchronisée; ajuster la carte de tempo puis vérifier dans un export audio/vidéo que le hit survient réellement sur la coupe.

**Critère de réussite, contre-exemple et limite.** Rejeter une synchronisation si le projet n'a pas de timecode d'origine, si le marqueur est pris pour un vrai hit visuel sans scène, ou si le DAW applique une courbe de tempo différente.

**Applicabilité :** `MIDI_DIRECT` / `AUDIO_REQUIRED` / `CONTEXT_REQUIRED`.

### Q2 — Séparation des données MIDI, du rendu instrumental et de l'automation

**Élément attesté par la notice.** Séquençage, instruments virtuels et automation explicitement annoncés pour FILM-205.

**Entrées et supports minimaux.** Pistes MIDI, Program Change, contrôleurs CC et courbes d'automation dans la session, instruments virtuels utilisés, audio exporté et documentation du mapping des paramètres.

**Détection / analyse ordonnée.** Identifier les événements encodés dans le SMF et les comparer au projet de station audio : les automation lanes du DAW ne sont pas nécessairement exportées dans le MIDI. Tester séparément attaques, articulations, réverbération et enveloppe du rendu audio; documenter la latence des bibliothèques avant de conclure à une erreur de timing.

**Résultat falsifiable.** Table « événement musical → encodé dans MIDI ? → paramètre VST/DAW ? → résultat audible ? » avec cas explicites où seule la session ou l'audio fait preuve.

**Application à une création originale.** Créer deux rendus d'un même cue original, l'un avec notes/tempos identiques et articulation de bibliothèque différente, l'autre avec une automation de volume; préserver les paramètres et comparer les attaques auditives et la clarté.

**Critère de réussite, contre-exemple et limite.** Le numéro de programme GM ne certifie ni la banque sonore ni l'effet du contrôle. Ne pas faire passer un rendu ou une automation externe pour un événement présent dans le SMF.

**Applicabilité :** `MIDI_DIRECT` / `MIDI_PROXY` / `AUDIO_REQUIRED`.

### Q3 — Mixage musical sous dialogue et cohérence de livraison

**Élément attesté par la notice.** Mixage attesté dans la notice FILM-205; le découpage en stems par séance et les critères de livraison du syllabus Online ne sont **pas** prouvés pour Boston.

**Entrées et supports minimaux.** Audio de dialogue et de musique à même cadence, mix de référence, fichier de scène, session/source si accessibles.

**Détection / analyse ordonnée.** Repérer les intervalles parlés, comparer la densité musicale et les masquages spectrotemporels; écouter à volume réaliste, vérifier les coupures et les niveaux de mix. Si stems disponibles, aligner leurs débuts, unités, canaux et versions, puis comparer leur somme au mix musical avec réserve pour les traitements de bus.

**Résultat falsifiable.** Liste de corrections justifiées par écoute : réduction de densité, décalage de motif, automation et balance; état des exports et paramètres réellement contrôlés.

**Application à une création originale.** Produire deux versions audio d'une même esquisse : densité maximale puis dialogue prioritairisé, comparer l'intelligibilité et conserver les paramètres de rendu; valider les exports en les réimportant.

**Critère de réussite, contre-exemple et limite.** Une vitesse/velocité de note n'est pas un niveau acoustique; la sommation des stems peut différer du mix si des traitements non linéaires agissent sur un bus.

**Applicabilité :** `AUDIO_REQUIRED` / `CONTEXT_REQUIRED` / `MIDI_PROXY`.

**Portée après approfondissement.** Trois axes explicités par la deuxième passe; ces procédures n'ajoutent pas de nouvelles œuvres attribuées à la section et ne transforment pas un MIDI sans image en preuve de synchronisation réelle. Les statuts de syllabus, de recherche et de première évaluation du registre ne changent pas.
