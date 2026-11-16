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

## Un même geste avant ou après la coupe

**Ancrage.** La [notice FILM-205](https://college.berklee.edu/courses/film-205) nomme la synchronisation MIDI/audio à l'image. La [leçon 5 d'OCWPR-300](https://online.berklee.edu/courses/scoring-technology#syllabus) donne un appui parallèle pour les repères, le timecode et le tempo. L'extrait et le comparateur sont des exemples AnaMu, pas des travaux de ces cours.

**Cas réel et édition.** *Big Buck Bunny*, réalisation Sacha Goedegebure, musique et conception sonore Jan Morgenstern, Blender Foundation (2008). Utiliser [l'extrait OGV de 33,28 s sur Commons](https://commons.wikimedia.org/wiki/File:Big_Buck_Bunny_extract.ogv), 25 i/s, et compter depuis le début de **ce fichier**, pas du film entier. À **19,28 s** (image 482, index zéro), le plan du lapin et du papillon laisse place au plan rapproché au pied du tronc. L'image 481 est encore dans le plan précédent. Dans le mix, une composante tenue et tonale remonte vers **19,00–19,08 s** avant la coupe. Le relevé combine un spectrogramme du mono à 8 kHz et des fenêtres RMS de 40 ms espacées de 20 ms. Le changement est déjà présent avant la coupe, à environ **0,20–0,28 s d'avance** pour ce repère. La bande sonore complète [diffusée séparément sur Commons](https://commons.wikimedia.org/wiki/File:BigBuckBunny-stereo.ogg) aligne le même passage autour de **2:03**, par corrélation sur le signal du mix (décalage d'environ +104,0 s). Cette piste n'est pas un stem de la seule musique. On documente l'ordre temporel de la montée tonale et de la coupe, non une preuve que chaque son vient de la partition ni une intention du compositeur. La première apparition du personnage suivant est un autre repère possible et n'est pas le zéro retenu.

**Comparateur.** [Télécharger ou ouvrir la vidéo A/B (MP4, 10 s)](https://raw.githubusercontent.com/leye0/AnaMu/main/docs/courses/berklee/FILM-205/avant-apres-coupe.mp4). Le montage répète la même fenêtre de cinq secondes, de **17,28 à 22,28 s** dans l'extrait, avec la coupe à **2,00 s** dans chaque version. Le mix original est retiré. Le même geste tonal original AnaMu dure 460 ms et commence à **1,72 s** en A puis à **2,28 s** en B (dans la seconde moitié du fichier, **7,28 s**). Les écarts sont −280 et +280 ms, soit sept images à 25 i/s de chaque côté. La hauteur, l'enveloppe et le gain sont identiques. A montre qu'un geste peut amorcer le changement, B qu'il peut le ponctuer après coup. C'est une manipulation du placement, pas un résultat de perception ni une réédition officielle du film.

**Réemploi.** Poser d'abord le repère à l'image, puis choisir l'événement musical dont on veut mesurer l'écart. Distinguer la première attaque, le sommet d'une montée et la résolution. Exporter les deux versions avec la même vidéo et comparer ce qui semble amorcer ou ponctuer le plan. Une avance temporelle seule ne démontre pas que le spectateur anticipera la coupe. **Supports :** vidéo + son + montage identifié. Un MIDI peut donner la position prévue, pas vérifier l'image ou le résultat acoustique.

**Crédit de l'extrait modifié.** (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org. [Licence CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) et [crédits du projet Peach](https://peach.blender.org/about/). Modifications AnaMu : coupe, répétition A/B, repères à l'écran et remplacement du mix.

## Intensifier un cue sans déplacer son arrivée

**Ancrage.** Synchronisation, tempi et métrique sont attestés pour [FILM-205](https://college.berklee.edu/courses/film-205). Le [guide transversal Berklee Online *Music for Film, TV & Games*, p. 74–75](https://assets.online.berklee.edu/handbooks/berklee-online-music-for-film-TV-and-games-handbook.pdf#page=75) cite séparément le changement de tempo, de subdivision, de rythme harmonique et de registre. Il s’agit d’une ressource parallèle, pas d’une consigne du cours. Le [témoin MUSP-240](../mcgill/MUSP-240.md#accélérer-quoi--quatre-écoutes-avec-la-même-phrase) est un matériau original réutilisé ici comme exercice sur papier, sans film associé.

**Analyse.** Pour chaque version, lire le même repère musical d’arrivée sur mi à `17` noires du départ du bloc. À 66 noires/min (A et B) il tombe vers **15,45 s**, à 132 (C et D) vers **7,73 s**. Les départs du bloc sont remis à zéro : ne pas lire le temps global du MP3. B et C font entendre la même grille d’attaques de harpe au départ, mais le chant et la basse n’atteignent pas le même repère dans le même délai. Un décompte d’arpèges ou un estimateur de vitesse sur cette partie seulement ne valide donc pas la synchronisation du cue.

**Réemploi.** Pour une coupe fictive à 15,45 s, ou plus généralement un repère déjà calé à l’image, conserver d’abord les temps absolus des arrivées. A → B densifie la harpe sans déplacer celle sur mi. A → C la fait arriver trop tôt. Si la battue globale doit néanmoins changer, remettre des repères de temps autour de l’accélération et réécrire la carte de tempo ou le trajet avant l’arrivée. Mesurer de nouveau l’attaque choisie dans le rendu, en vérifiant aussi que la harpe ne détourne pas l’attention de l’événement à synchroniser. Une accélération qui respecte une coupe n’est pas assurée de respecter les coupes intermédiaires. `MIDI_DIRECT` pour l’arrivée calculée, `AUDIO_REQUIRED / CONTEXT_REQUIRED` pour le rendu et la synchronisation à une scène réelle.

## Fixer ce que l’image doit atteindre, pas toutes les entrées

À un **repère d’image imposé**, noter quel événement doit y tomber exactement, par exemple une résolution au grave ou l’attaque d’un nouvel ensemble. Une fois ce point fixé, décider séparément si le spectateur doit deviner le changement avant ou garder un écho de l’état précédent après. Dans le [témoin audio de MUS-2328](../udem/MUS-2328.md#faire-entrer-une-section-sans-couper-lancienne-dun-bloc), la basse et la résolution restent au seuil de 8 s alors qu’un motif de flûte peut apparaître 0,5 s plus tôt. Quatre attaques d’une autre partie peuvent rester après. Ce témoin ne contient pas d’image. Le [comparatif avec coupe réelle dans cette fiche](#un-même-geste-avant-ou-après-la-coupe) isole un autre choix, le signe du décalage entre un geste et la coupe.

**Mise en pratique.** Consigner séparément le premier signal, le hit point, le premier appui complet et la dernière attaque sortante. S’il faut cacher le changement jusqu’à la coupe, rejeter la levée caractéristique avant elle et porter la continuité dans la basse ou le débit. À l’inverse, si l’image doit révéler ce que l’oreille prépare, essayer la levée en gardant le geste appuyé sur l’image. Dans les deux versions, vérifier le rendu sur la même image avec les mêmes niveaux. `MIDI_DIRECT` pour positions de notes, `AUDIO_REQUIRED / CONTEXT_REQUIRED` pour le rendu et le sens de la coupe.

## Caler deux coupes sans confondre tempo et niveau

**Problème de travail.** La [notice FILM-205](https://college.berklee.edu/courses/film-205) distingue la synchronisation, l’automation et le mixage. Reprendre le second tour de [Grandir sans courir](../mcgill/MUCO-360.md#grandir-sans-courir), où le début de la mesure 5 (8 s) et de la mesure 7 (12 s) sont des repères musicaux. Supposer que deux coupes tombent sur ces temps d’une vidéo à **25 i/s**, aux images **200 et 300** à partir de zéro. Le MP3 contient la musique seule. Aucune scène ni réplique n’y est incorporée.

| Proposition | Image 200 : premier appui du second tour | Image 300 : entrée du cor | Ce que l’option met à l’épreuve |
|---|---|---|---|
| Garder ♩ = 120 et prendre C ou E | Appui écrit à 8,00 s | Entrée écrite à 12,00 s | Les deux repères sont inchangés. C et E ont les mêmes notes et des balances différentes. |
| Accélérer à ♩ = 150 dès le second tour, sans compensation | Appui écrit à 8,00 s | Entrée écrite à 11,20 s | Le deuxième repère arrive 20 images trop tôt. |
| Garder le premier repère, puis écrire 4 noires à 150 et 4 à 100 | Appui écrit à 8,00 s | Entrée écrite à 12,00 s | Les deux repères sont rétablis, mais la barre intermédiaire tombe à 9,60 au lieu de 10,00 s, soit 10 images plus tôt. |

**Ce que permet le calcul.** Les 8 noires entre les deux repères durent 3,20 s à 150. Avec compensation, les 4 premières prennent 1,60 s et les 4 suivantes 2,40 s. C’est une carte de tempo **par paliers** hypothétique, pas un accelerando joué ou un MIDI supplémentaire. Elle garde les deux bornes, pas leurs subdivisions. Rejeter cette solution si le montage comporte un troisième geste à 10,00 s que la musique doit accentuer. À tempo fixe, on peut avoir davantage de mouvement entre les repères sans déplacer ces appuis. La première attaque d’alto de C/E à **8,25 s**, soit 250 ms après la première coupe, est une conséquence de son contretemps. Ne pas la désigner comme le hit de l’image 200 simplement parce qu’elle apporte la première nouvelle couleur.

**Vérifier dans le mix de scène.** Si le cor doit ponctuer la seconde coupe, comparer l’attaque réellement audible à l’image, pas seulement le MIDI. Si l’on veut garder la clarinette lisible sans couvrir le dialogue, essayer un réglage de soutien avant de pousser tout le cue. [D et E](../udem/MUS-3322X.md#égaliser-le-total-sans-régler-la-place-du-thème) ont des RMS très voisins, mais des rapports différents entre la clarinette, le cor et l’accompagnement. Rien ne prouve leur interaction avec une réplique non fournie. Repérer l’attaque avec la piste du cor, puis écouter le mix dans le contexte final. **Supports :** `MIDI_DIRECT` pour les temps prévus, `AUDIO_REQUIRED` et `CONTEXT_REQUIRED` pour le résultat et l’intelligibilité.
