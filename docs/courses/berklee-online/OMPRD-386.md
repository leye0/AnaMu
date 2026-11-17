# OMPRD-386 — Programming and Producing Drum Beats

**Berklee Online, vrai cours de production et syllabus public de douze leçons**, [page et plan officiels](https://online.berklee.edu/courses/programming-and-producing-drum-beats#syllabus), auteur du cours **Erik Hawkins**, relevé le 17 novembre 2026. Les acquis annoncés vont de la mécanique d'une batterie à la programmation MIDI expressive, l'écriture des fills et la production/mix. **Dossier comparatif nouveau, hors du registre canonique de 378 cours** : ne pas transférer ses objectifs à CM-343, ni dire que son manuel ou ses exercices privés ont été lus.

## Matière attestée : douze leçons de l'instrument au morceau

| Leçon officielle | Champ documenté | Distinction utile pour AnaMu |
|---:|---|---|
| 1 | Éléments constitutifs du beat, station audio et instruments virtuels, mix élémentaire | Un kit virtuel n'est pas un **enregistrement acoustique**. |
| 2 | Enregistrement MIDI en direct, contrôleurs, quantization d'entrée et de post-traitement | **Performance enregistrée** et **grille mathématique** sont deux sources distinctes. |
| 3 | Anatomie du kit, techniques de jeu, baguettes/balais/mailloches, notation | La forme d'onde d'un sample ne renseigne pas toute la coordination. |
| 4 | Boîtes à rythmes analogiques/numériques et step sequencers | Machine rythmique et geste humain sont deux esthétiques plausibles, sans hiérarchie automatique. |
| 5 | Percussions de musique populaire, identification, modes de jeu, instruments d'orchestre | L'extension du vocabulaire percussif exige des **rôles** et la source du sample. |
| 6 | Samples MIDI de batterie et implantation dans le dispositif de production | Un sample peut porter son propre timbre et enveloppe, pas seulement le numéro GM. |
| 7 | Boucles, adaptation temporelle, time-stretch et beat matching | Une boucle d'audio **n'est pas** équivalente aux événements MIDI reconstruits. |
| 8 | **Groove et groove quantize** | Le temps d'attaque peut différer de la grille nominale d'une façon structurée. |
| 9 | Renforcement de batterie multitrack jouée et synchronisation | Une performance captée ne devient pas toute MIDI lorsqu'on y ajoute une couche. |
| 10 | **Interaction avec la section rythmique** | Basse, batterie et accompagnement articulent ensemble le groove; pas de performance de basse dans un canal GM de percussion. |
| 11 | **Structure de chanson et fills** | Les fills annoncent ou répondent à des **frontières formelles**, plutôt que « une mesure aléatoire de notes ». |
| 12 | Traitements de mix, compression, EQ et mastering | La vélocité MIDI ne certifie ni un compresseur ni un résultat sonore équilibré. |

Le livre *Producing Drum Beats: Writing and Mixing Killer Drum Grooves* (Erik Hawkins, Berklee Press, 2010) est indiqué dans la page officielle. **Le support sonore et les exercices intégraux restent non consultés**. Les douze leçons sont **attestées**, mais les expériences quantitatives AnaMu qui suivent sont **originales**, pas des devoirs assignés ou des transcriptions du manuel.

## Apprentissage A — quantification n'est pas microtiming : quatre traitements distincts

**Exercice contrôlé original.** Prendre une batterie de deux mesures, kick sur 1 et 3, snare sur 2 et 4, charleston sur les croches. La première version **préserve les dates rectilignes**. La deuxième conserve le kick et la caisse sur la grille mais **retarde seulement** les coups de charleston sur les contretemps, de **20 ticks MIDI à 480 PPQ**. À 120 BPM, l'écart représente **environ 20,83 ms**; ce n'est pas « le swing universel ». Dans la troisième, **déplacer la caisse** à un autre décalage (ex. 12 ticks) tout en laissant le chapeau droit : cela produit un autre rapport entre les lignes. Dans une quatrième, **changer seulement les vélocités** sans déplacer aucun coup. Il faut mesurer **timing** et **dynamique** indépendamment, sans confondre quantification/groove.

**Analyse.** Pour chaque partie, calculer les différences de dates observées à la grille **réellement déclarée**, et les **variations de vélocité par instrument**. Une quantification dite « swing 60 % » ne possède pas une seule interprétation si les outils découpent différemment la double-croche ou la croche; identifier le **gabarit de groove et ses bornes**. Une banque de sons peut introduire un échantillon à attaque plus lente, donc la comparaison auditive peut différer de l'horloge MIDI.

## Apprentissage B — le groove comme rôles complémentaires de la section rythmique

**Exemple construit, non extrait du cours.** Dans un motif de 4/4, le kick marque les temps 1 et 3, le snare souligne 2 et 4, et la charleston joue huit coups réguliers. Une note de basse mélodique peut **coïncider avec le kick**, intervenir avant lui, ou tenir sous sa résonance. Ces trois rapports changent la fonction du même coup de grosse caisse et peuvent avoir une conséquence perceptive, sans qu'une note GM36 contienne la basse réelle.

**Analyser.** Séparer canal percussion, programme de basse, piste de cymbales et métrique. Mesurer **coïncidences**, **décalages** et répétitions sur une phrase, puis vérifier au besoin sur audio si la basse et le kick se fusionnent, s'opposent ou masquent. **Ne pas** appeler un on/off 30 ms après le beat une erreur : il peut être volontaire, ou lié au monitoring/l'enregistrement.

## Apprentissage C — un fill doit avoir une position et une destination

**Étude originale.** Composer une séquence de huit mesures; les mesures 1–3 portent un ostinato, la mesure 4 peut se transformer en **fill de transition**, puis la mesure 5 commence la nouvelle phrase. Comparer trois versions du **même point d'arrivée** : A = pas de fill; B = fill sur les deux derniers temps de la mesure 4, en conservant la pulsation de grosse caisse; C = fill sur une mesure entière avec déplacement sur les toms et **un vrai silence juste avant l'attaque d'arrivée**. Ne pas modifier arbitrairement tempo, barres, harmonie et instrumentarium en même temps.

**Évaluer séparément :** exactitude de la grille, nombre d'attaques, montée/diminution de densité par mesure, préservation du premier temps de mesure 5, gestuelle réaliste du kit, espace d'autres instruments, et **lisibilité musicale** (qui demanderait un jugement humain). Une rafale de trente notes à la fin d'une phrase n'est pas nécessairement un meilleur fill. Une boucle de samples compressée n'est pas non plus une composition avec structure d'arrivée en soi.

**Vérifier le caractère GM.** Une banque General MIDI permet de représenter le kick (36), le snare (38), les charlestons (42/44/46), toms (41–50), cymbales et accessoires. Le [référentiel technique GM](../../references/gm-percussion.md) précise que ce ne sont pas 47 instrumentistes et qu'**un canal mélodique de basse** ne se lit pas dans la map de batterie. Les fichiers pédagogiques d'AnaMu sont **des preuves de commandes MIDI et de structure écrite**, pas de réalisme sonore ou de réussite de mix.

**Applicabilité :** MIDI_DIRECT pour date/velocité/canal/tempo/structure représentée; MIDI_PROXY pour groove entendu, coordination, fill et rôle; AUDIO_REQUIRED pour timbre/mix/sample attack/relation auditive basse-batterie; CONTEXT_REQUIRED pour style, DAW, instrumentistes, notation et rôle formel. [Cours de technique instrumentale OPERC-160](OPERC-160.md), [complexité rythmique CM-320](../berklee/CM-320.md) et [écriture CM-343](../berklee/CM-343.md). Aucun mixage, moteur ou modèle de groove prétendument calibré.
