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

## Rubato commun et décalage entre les voix

**Sources et fenêtre.** Le [descriptif de COND-217](https://college.berklee.edu/courses/cond-217) nomme le rubato et le travail avec solistes. Ce dossier AnaMu utilise les m. 1–6 de l’Aria initiale des *Variations Goldberg*, avec le début de m. 7 pour fermer la dernière mesure du relevé. Premier passage uniquement, [partition Werner Schweer, p. 2 du PDF](https://upload.wikimedia.org/wikipedia/commons/6/6d/Goldberg_Variations_complete_score.pdf#page=2). Deux prises sur piano : [Kimiko Ishizaka, Open Goldberg, piste 01](https://upload.wikimedia.org/wikipedia/commons/5/59/Kimiko_Ishizaka_-_J.S._Bach-_-Open-_Goldberg_Variations%2C_BWV_988_%28Piano%29_-_01_Aria.mp3) et [Tjako van Schie, MP3 publié par le Matheson Trust](https://themathesontrust.org/papers/audio/Goldberg-Aria-vanSchie.mp3), [attribution de la prise](https://www.themathesontrust.org/library/bach-architect-and-servant). Ce ne sont pas des prises du cours. Pour la distinction entre élasticité commune et décalage mélodie/accompagnement, voir [Werner Goebl, *Temporarily out of sync*, 2011, § 2](https://iwk.mdw.ac.at/goebl/papers/Goebl2011-ForumAcusticum-331.pdf), qui l'illustre sur d'autres œuvres.

### Deux mesures du temps à ne pas confondre

**Carte de pulsation de référence.** Le tableau suit les débuts de mesure repérés dans le grave. Les secondes sont comptées depuis le début de chaque MP3, silence compris. La dernière colonne donne 180 divisé par la durée entre ce repère et le suivant, soit une moyenne en noires/minute sur trois temps. Il ne s'agit ni d'un tempo imposé à l'intérieur de la mesure ni d'une pulsation déduite indépendamment de la basse.

| Début de mesure, note de basse | Ishizaka, s | Van Schie, s | Moyenne jusqu'au repère suivant, I / V |
|---|---:|---:|---:|
| 1, sol3 | 1,75 | 0,56 | 41 / 39 |
| 2, fa♯3 | 6,15 | 5,15 | 42 / 36 |
| 3, mi3 | 10,45 | ≈ 10,16 | 47 / 40 |
| 4, ré3 | 14,30 | 14,69 | 42 / 39 |
| 5, si2 | 18,61 | 19,35 | 39 / 39 |
| 6, do3 | 23,22 | 23,94 | 42 / 37 |
| 7, mi3 | 27,49 | 28,85 | — |

De m. 1 à m. 7, les 18 noires prennent **25,74 s** chez Ishizaka et **28,29 s** chez Van Schie, soit environ **42 et 38 noires/minute**. L'écart ne se répartit pas uniformément. À m. 5, les deux mesures ont presque la même durée (4,61 et 4,59 s) malgré l'écart déjà accumulé.

**Décalage local.** Pour un temps où la partition aligne deux attaques, soustraire l'instant du grave à celui du dessus, dans **la même prise**. Un résultat positif place le dessus après le grave. À m. 3, temps 1, le mi3 précède chez Ishizaka le premier sol4 identifiable du geste orné. Chez Van Schie, la séparation est trop petite par rapport à l'incertitude du grave pour assigner un ordre sûr. À m. 5, temps 3, le même contraste s'observe entre le sol3 de basse et le premier mi5 identifiable du geste orné. Ce relevé ne résout pas tous les battements de ces ornements.

| Repère écrit | Ishizaka, grave → dessus | Van Schie, grave et dessus | Interprétation permise |
|---|---|---|---|
| M. 3, temps 1 | 10,44–10,46 s → 10,53–10,56 s | Grave vers 10,14–10,20 s, dessus vers 10,15–10,17 s | Environ 0,10 s de retard du dessus chez Ishizaka. Ordre non tranché chez Van Schie. |
| M. 5, temps 3 | 21,52–21,55 s → 21,59–21,64 s | Grave vers 22,00–22,04 s, dessus vers 22,01–22,04 s | Le dessus entre après le grave chez Ishizaka, alors que les durées globales de m. 5 sont presque les mêmes entre les prises. |

**Reproduire et savoir s'arrêter.** Décoder les MP3 en mono à 22 050 Hz. Suivre l'énergie autour de la fondamentale et des deux premiers partiels supérieurs, avec une fenêtre de Hann d'environ 46 ms, pas d'environ 2 ms et des contrastes de niveau avant/après de 14 à 32 ms de part et d'autre du repère. Chercher les premières montées cohérentes dans plusieurs bandes, en contrôlant la note précédente et l'ornement suivant. Les intervalles sont des fourchettes de lecture du signal, pas des intervalles de confiance ni des horodatages de touches. Le deuxième harmonique du sol3 tombe sur sol4, donc la mesure 3, temps 2, ne donne pas ici deux attaques indépendantes à partir de ces seules bandes. Le tempo de référence n'efface pas un écart de voix, mais le mixage, la pente d'attaque ou le traitement d'une prise peuvent biaiser l'estimation. Deux points ne suffisent pas à généraliser une pratique ni à prouver une intention. Voir [CM-342](./CM-342.md#cas-comparatif--aligner-laria-des-goldberg-entre-partition-midi-et-enregistrement-13-novembre-2026) pour les reprises et [OCOMP-507](../berklee-online/OCOMP-507.md) pour l'écart possible entre commande MIDI et attaque rendue.

### Comparateur original à paramètres contrôlés

[Télécharger le MIDI A/B/C](https://raw.githubusercontent.com/leye0/AnaMu/main/docs/courses/berklee/COND-217/rubato-tempo-voix.mid). Trois blocs de trois mesures en 3/4, deux pistes au piano, motif original. À l'intérieur de chaque bloc, les hauteurs, vélocités et durées en ticks restent identiques.

| Bloc | Carte de tempos | Attaques du dessus par rapport au grave |
|---|---|---|
| A, m. 1–3 | 72 noires/minute | Ensemble. |
| B, m. 4–6 | 72 noires/minute | Dans la mesure du milieu, chaque note du dessus est décalée de 58 ticks, environ 101 ms. La basse est inchangée. |
| C, m. 7–9 | 72 → 56 → 72 noires/minute | Ensemble. Les deux voix suivent le ralentissement de la mesure centrale. |

**Réemploi.** Comparer B à A pour travailler le placement mélodique sans ralentir l'accompagnement. Comparer C à A pour travailler le tempo sans désunir les attaques. Si un écart apparaît seulement après rendu, mesurer l'attaque dans l'audio et vérifier la latence et l'enveloppe avant de retoucher l'écriture. `MIDI_DIRECT` pour les deux contrôles symboliques, `AUDIO_REQUIRED / CONTEXT_REQUIRED` pour les attaques dans les prises et leur interprétation. Le MIDI de direction préexistant reste inchangé.
