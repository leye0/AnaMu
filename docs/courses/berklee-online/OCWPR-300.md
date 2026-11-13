# OCWPR-300 — Scoring Technology

**Nature : syllabus public d'un cours Berklee Online distinct des cours de Boston.** Vérification : 10 novembre 2026. Auteur du cours : Andreas Bjørck. **Plan de 12 leçons documenté, contenus intégrals et évaluations non obtenus.**

## Provenance et portée

- [Page officielle, rubrique « Syllabus »](https://online.berklee.edu/courses/scoring-technology#syllabus) : objectifs, séquence de leçons, intitulés d'activités, exigences. Accès public au résumé ; ressources pédagogiques complètes non accessibles par cette page.
- Cours Berklee Online de 12 semaines, enseignement distinct du cours de Boston FILM-205. Plan de douze leçons avec un travail nommé pour chacune, y compris les deux étapes d'un projet final. Prérequis annoncé : Film Scoring 101 ou expérience équivalente.

## Résultats d'apprentissage déclarés ou directement exposés par le plan

- Préparer un environnement de composition audiovisuelle en DAW : routage, gabarit, instruments virtuels et séquences MIDI.
- Synchroniser une maquette à l'image au moyen du timecode, de repères et de cartes de tempo.
- Combiner textures électroniques, bibliothèques de sons et orchestre virtuel puis traiter et mixer le résultat en fonction du dialogue.
- Livrer les éléments techniques : parties, stems, fichiers de session, mixages et exports synchronisés.

## Progression attestée par le plan public

| Leçon | Matière annoncée (résumé original) | Activités/devoirs publics |
|---|---|---|
| 1 | Comprendre la chaîne de production et comparer à l'écoute une musique hybride | Analyse guidée d'un score hybride |
| 2 | Structurer le gabarit de projet, le routage et une séquence MIDI élémentaire | Créer un gabarit et une courte séquence |
| 3 | Choisir, régler et combiner des instruments virtuels et leurs échantillons | Créer une pièce à partir de sons d'instruments virtuels |
| 4 | Construire une maquette orchestrale expressive (réverbération, dynamique, programmation et timing) | Produire une maquette orchestrale |
| 5 | Placer une musique sur des points de synchronisation : SMPTE, vidéo, marqueurs, tempo et clic | Composer un passage calé sur des repères à l'image |
| 6 | Créer des timbres hybrides à partir de synthèse soustractive, échantillonnage et superposition | Concevoir un ensemble de sons hybrides |
| 7 | Employer boucles, rythmiques programmées et variations pour une scène d'action | Composer un cue d'action à motifs rythmiques |
| 8 | Construire profondeur et équilibre avec égalisation, compression et réverbération | Mixer une séquence avec ces outils |
| 9 | Modifier des sources avec distorsion, délai, montage et correction d'enregistrements | Transformer un cue avec traitements et éditions |
| 10 | Faire coexister musique, bruitages et dialogue ; automations et formats stéréo/multicanal | Mixer une séquence à l'image |
| 11 | Préparer les transferts MIDI/partition/séance, les parties et l'organisation de production ; mention de l'éthique de l'IA | Projet final, première étape |
| 12 | Produire stems, versions alternatives, formats conformes et niveaux adaptés à la livraison | Projet final, deuxième étape |

## Lectures, exemples et éléments non publics

- **Lectures :** Aucun manuel obligatoire identifié dans la section publique consultée ; matériel logiciel et bibliothèques sonores recommandés, non contenus de leçon redistribuables.
- **Limites :** Les sujets et intitulés de devoirs sont visibles ; durée précise, critères de notation, corrigés, fichiers MIDI, médias d'exercice, partitions et cours vidéo ne le sont pas. Ne pas attribuer ces douze devoirs à FILM-205 (Boston).
- **Cours de Boston potentiellement apparenté :** [FILM-205](../berklee/FILM-205.md), avec comparaison de thèmes seulement.

**Règle de preuve :** le syllabus **de ce cours en ligne** est publiquement décrit ; ces données ne modifient ni le statut ni l'admissibilité administrative d'aucun cours Boston du registre principal. Ne pas prendre un titre de devoir pour son cahier de consignes ; ni une maquette MIDI pour une orchestration instrumentale exécutée.

## Application à l'analyse et à la création — assembler les fonctions d'un cue (13 novembre 2026)

**Preuve du cours.** Le [plan public OCWPR-300](https://online.berklee.edu/courses/scoring-technology#syllabus) nomme les points de synchro et la carte de tempo (leçon 5), les boucles et variations d'action (7), le mixage musique/bruitages/dialogue et les automations (10), puis les stems et versions de livraison (12). Les exemples de procédure ci-dessous ne reproduisent pas les devoirs du cours.

### Q1 — Plusieurs points de synchro peuvent avoir des fonctions différentes dans une seule phrase

**Analyse.** Aligner image, marqueurs, tempo et audio sur la même origine et vérifier la cadence d'image. Pour trois repères successifs, distinguer celui qui déclenche la préparation, celui qui reçoit une ponctuation et celui après lequel le cue change de fonction. Noter l'attaque musicale audible et l'intervalle par rapport à chaque repère. Comparer avec l'hypothèse d'un alignement dû aux accents récurrents du groove, surtout si plusieurs marqueurs voisins sont possibles. Sans notes de spotting, l'alignement ne dit pas quel repère a guidé la composition.

**Création.** Fixer trois repères sur une vidéo originale. Choisir une arrivée musicale principale et aménager les deux autres sans accent obligatoire. Comparer à une version qui ponctue les trois, à tempo global et durée similaires. Évaluer le phrasé autant que l'erreur de synchro. **Preuve :** `CONTEXT_REQUIRED` pour l'image et la carte de repères, `AUDIO_REQUIRED` pour les attaques audibles.

### Q2 — La variation de boucle peut relier des groupes ou seulement décorer une répétition

**Analyse.** Aligner la boucle, les pistes de variation et les repères de scène. Séparer les variations récurrentes en fin de cycle de celles dont la suite change : retrait du grave, ajout persistant d'une couche, déplacement d'un appui ou interruption. Comparer si une variation prépare la section suivante parce qu'elle en introduit un élément distinctif, ou si elle ne se distingue pas des autres fins de cycle. Une coupure vidéo sans conséquence durable sur le cue peut rester une ponctuation locale.

**Création.** Écrire quatre cycles identiques puis deux versions de la dernière variation. Dans une seule, reprendre au cycle suivant un élément qu'elle introduit. Garder les marqueurs d'image et les niveaux comparables pour isoler la relation entre cycles. **Preuve :** `MIDI_PROXY` pour les motifs séquencés et `AUDIO_REQUIRED` lorsque les boucles ou traitements sont des fichiers audio.

### Q3 — Une section peut changer de rôle parce que le mix cède la place au dialogue

**Analyse.** Comparer la musique seule, les stems disponibles et le mix à l'image. Vérifier si le retrait audible suit une réécriture de la musique, un changement de balance, ou un masquage par le dialogue et les effets. Si la même phrase se poursuit dans le stem musique, annoter la continuité musicale et le changement de premier plan audiovisuel séparément. Sans session ni comparaison valable entre versions, ne pas attribuer le changement à une automation déterminée.

**Création.** Garder la composition intacte. Comparer un mix où la musique reste au premier plan avec un autre où elle libère de la place à une réplique et retrouve son rôle au repère suivant. Évaluer l'intelligibilité de la réplique et la continuité du cue. **Preuve :** `AUDIO_REQUIRED` et `CONTEXT_REQUIRED` pour le mix et la scène. Aucun MIDI ajouté : il manquerait les pistes et le montage qui déterminent la lecture.
