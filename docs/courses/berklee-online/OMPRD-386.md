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

## Quantification, groove, fills et interaction de la section rythmique — cinq MIDI originaux (17 novembre 2026)

**Ce que le syllabus officiel établit vraiment :** la [page OMPRD-386, auteur Erik Hawkins](https://online.berklee.edu/courses/programming-and-producing-drum-beats#syllabus) annonce **l'enregistrement MIDI et la quantification** (leçon 2), l'anatomie du drum kit (3), les percussions (5), les boucles (7), **groove quantize** (8), l'interaction de la section rythmique (10), les **fills et la structure de chanson** (11), puis le **mixage** (12). Aucune de ces leçons ne prescrit les fichiers ci-dessous : ce sont **cinq témoins originaux d'AnaMu**, créés sans reprise d'un hit commercial. **Le rendu audio ni la qualité stylistique ne sont vérifiés ici.**

### Témoin PR-1 — même nombre de notes, quatre variables différentes

[MIDI original de 16 mesures en quatre blocs de quatre](./OMPRD-386/quantization-groove-quatre-variables.mid). **192 notes sur canal GM1 10**, soit **48 par variante**, 120 BPM, PPQ 480, 4/4 constant; kick GM36 (1 et 3), snare GM38 (2 et 4), charleston GM42 (8 croches par mesure).

| Bloc | Changement réellement encodé | Invariants démontrés par les événements |
|---|---|---|
| A — grille stricte | Coups de charleston espacés de 240 ticks, sans décalage | Référence des dates et vélocités. |
| B — dynamique seulement | **Vélocités de la charleston** alternées sur temps/contretemps | Les **dates, nombres et identités** de notes restent égales à A. |
| C — microtiming de charleston | Seules les croches de charleston **en contretemps** sont retardées de **24 ticks** (25 ms à 120 BPM) | Kick et snare restent **au tick près** les mêmes qu'en A; les autres croches de charleston restent stables. |
| D — microtiming de caisse claire | Snare sur 2 et 4 retardée de **14 ticks** (environ 14,58 ms à 120 BPM) | Kick et charleston sont inchangés par rapport à A; pas de changement de vélocité ou de tempo. |

**L'[étude *Mapping timing and intensity strategies in drum-kit performance*, *Journal of New Music Research* (2022)](https://doi.org/10.1080/09298215.2022.2150649) est une référence académique externe**, sur des performances et l'évolution des coups selon le ressenti. Elle ne donne ni les **24/14 ticks** choisis ici ni un bon décalage universel. Dans un vrai enregistrement, la latence des échantillons, l'attaque du son et l'ensemble des autres instrumentistes peuvent changer l'impression. **Ne pas baptiser automatiquement C « swing » ni D « laid-back »** : ce sont des candidats de contrôle temporel, pas des jugements déjà obtenus à l'écoute.

**Procédure :** extraire les **grilles par instrument**, comparer dates et vélocités séparément, conserver des hypothèses de retard/avance plutôt que quantifier d'emblée. Une vraie groove quantize peut aussi déplacer des parties selon un **gabarit d'exécution enregistré**, qui n'est **pas présent** dans ces fichiers. La forme audio produite par DAW demeure inconnue.

### Témoin PR-2 — une arrivée fixe, trois préparations différentes

[MIDI original, 24 mesures](./OMPRD-386/fills-meme-arrivee-trois-versions.mid) : trois blocs de **huit mesures** à **104 BPM** avec mêmes grosse caisse, caisse et charleston en accompagnement. Les blocs contiennent **97 / 100 / 97 notes on** respectivement, soit **294 au total**. A ne place **aucun fill** en mesure 4. B réorchestre la **seconde moitié** de cette mesure avec des toms et une caisse à densité plus élevée. C écrit une succession de **12 frappes** jusqu'au tick local **7 080**, puis un **silence d'événements MIDI** avant l'attaque de la mesure 5 au tick local **7 680**. L'extinction de la dernière note du fill de C est encodée au tick local **7 124**, donnant un repos de **556 ticks sans note active** avant l'arrivée (un peu moins de **0,67 s** à 104 BPM).

**Contrôle capital :** **les mesures 5 à 8 sont exactement identiques dans les trois blocs** (49 notes après l'arrivée, mêmes dates relatives, hauteurs et vélocités). Elles commencent toutes par la **même crash GM49 et le même coup de grosse caisse GM36**. Seule la **préparation avant la frontière** change : ce n'est pas un « meilleur fill » garanti, ni une métrique nouvelle. Le cas C introduit **un vrai espace d'événements**; la réverbération d'un sample peut néanmoins continuer et le rendre **non silencieux acoustiquement**.

**Analyser / composer.** Relever **densité par segment**, moments d'arrivée, silence structurel avant la phrase, déplacements entre toms, et possibilités humaines réelles. Garder arrivée et harmonie constantes pour discuter la **fonction formelle** du fill, non son nombre de coups seul. La [leçon 11 du syllabus OMPRD-386](https://online.berklee.edu/courses/programming-and-producing-drum-beats#syllabus) prouve l'étude des fills dans la structure, mais **pas ces trois arrangements spécifiques**.

### Témoin PR-3 — linéarité versus superposition : même calendrier, nombre de coups différent

[MIDI original A/B, huit mesures](./OMPRD-386/lineaire-versus-superpose.mid), 120 BPM. Dans chacune des quatre mesures de A, huit coups de charleston se superposent à **deux grosses caisses** et **deux caisses claires**, soit **12 événements par mesure**, **48 par bloc**. B attribue **exactement une frappe** à chaque position de croche, huit par mesure (**32 par bloc**), en **remplaçant** les coups de charleston aux temps de kick et de snare. Les deux blocs ont **32 instants distincts** chacun en quatre mesures, et conservent la **même grille de dates d'attaque**.

**Ce qui est préservé :** les huit positions d'attaque possibles par mesure, la mesure, la période, la dynamique nominative des accents principaux. **Ce qui change :** nombre d'événements simultanés, densité de timbre en chaque instant et mise à contribution des membres. Il serait faux de conclure qu'A et B ont le **même nombre de coups**, et tout aussi faux de prétendre que B contient une **véritable superposition de deux parties** simplement parce que sa succession suggère plusieurs timbres. Le caractère **linéaire** de B est vérifié par l'absence de doubles attaques dans la même partie MIDI, non par la perception certaine d'un groupe.

### Témoin PR-4 — grosse caisse identique, basse syncopée : un décalage n'est pas une erreur de quantification

[MIDI original, douze mesures](./OMPRD-386/basse-kick-alignement-anticipation-retard.mid), 120 BPM. Trois blocs de **quatre mesures**, chacun **56 notes**, total **168 attaques**, dont **144 GM percussion canal 10** et **24 notes d'une basse mélodique** sur canal 1, **Program Change 33** (programme affiché GM1 **34 — Electric Bass (finger)**). Les événements de batterie **restent parfaitement identiques** dans les trois blocs, et le motif de hauteur de la basse reste identique. Le premier coup de basse de chaque mesure est toujours au temps 1; seule la seconde note se décale relativement au **kick du temps 3** :

| Bloc | Kick au temps 3 | Deuxième attaque de basse | Différence absolue à 120 BPM |
|---|---:|---:|---|
| A — attaque commune | tick local **960** | **960** | **0 ms** |
| B — anticipation | **960** | **840** | **–125 ms** |
| C — retard | **960** | **1020** | **+62,5 ms** |

**Interprétation disciplinée.** Les 125/62,5 ms sont des **valeurs de montage intentionnelles**, **pas** les écarts mesurés chez des musiciens ou un timing à imiter universellement. Un contexte de phrasé, les attaques des échantillons de basse, le style, et les notes longues peuvent rendre l'une des versions plus ou moins intelligible. L'activité de la **section rythmique** est inscrite au syllabus (leçon 10); la banque GM prouve uniquement que les deux parties **ont des programmes et canaux distincts**, pas qu'elles « verrouillent » ensemble le groove à l'écoute.

**Réinvestissement :** commencer par de vraies parties distinctes de basse et de batterie, comparer coïncidences, anticipation, retard et note tenue. Ne **jamais** traiter la note basse MIDI 36 comme une grosse caisse simplement parce qu'elle partage le nombre 36 avec GM Drum 36 : les **canaux et programmes diffèrent**.

### Témoin PR-5 — changer la percussion sans changer les attaques ni la dynamique numérique

[MIDI original, 16 mesures](./OMPRD-386/percussion-timbres-grille-invariante.mid) : **quatre variantes de quatre mesures**, **48 notes chacune**, soit **192** attaques sur canal 10 à 100 BPM. Grosse caisse GM36 et caisse GM38 **strictement identiques** sur les quatre variantes; huit attaques égales du plan de percussion par mesure, et **mêmes vélocités et instants** dans toutes les variantes. Seule **l'identité nominale du son** qui marque la subdivision est remplacée :

| Bloc | Son de subdivision (GM1) | Ce que cela modifie |
|---|---|---|
| A | **42 Closed Hi-Hat** | Surface de cymbale, attaque plutôt brève dans les banques typiques. |
| B | **70 Maracas** | Source normalement secouée, résonance et phrasé différents; en MIDI, une **substitution de sample**. |
| C | **75 Claves** | Timbre de bois à attaques sèches, identité différente sans nouveau motif. |
| D | **76 Hi Wood Block** | Autre timbre de bois, autre éventuel spectre. |

Ceci **ne représente pas** quatre grooves issus de traditions différentes. Un jeu de maracas de **huit déclenchements fixes par mesure** est un prototype de maquette, pas une preuve de **mouvement de secouement réaliste** ni d'authenticité stylistique. De même, remplacer une charleston par des claves peut demander une **nouvelle organisation des mains et des instruments** si l'on veut l'écrire pour des personnes. La norme GM définit le **nom** du déclencheur, mais pas son enveloppe ni son mixage. [Référence GM1](../../references/gm-percussion.md).

### Ce que les cinq fichiers prouvent et n'évaluent pas

**Relecture technique post-publication :** les cinq fichiers contiennent **192 / 294 / 80 / 168 / 192 notes**, respectivement, soit **926 attaques** en tout sur **deux ou trois pistes** selon l'exercice. Toutes les notes ont un note-off apparié; les changements de sections sont marqués dans la piste méta et toutes les études utilisent PPQ **480**. Les critères de comparaison ont été confrontés **sur les octets GitHub eux-mêmes**, notamment identités de kick/snare, rapports temporels, notes de basses et arrival de quatre mesures.

**Niveau de preuve :** la comparabilité des **dates** est MIDI_DIRECT; la fonction de groove et les timbres voulus sont **MIDI_PROXY**; la performance des coups et les styles sont **CONTEXT_REQUIRED**; l'acoustique, le mixage, l'impression de swing et le groove sont **AUDIO_REQUIRED**. Les cinq dossiers sont **du savoir de composition/production contextualisé**, non une banque de sons validée, une simulation humaine ni un moteur automatique.


## Dissonance de déplacement, timeline sur deux mesures et retour — 17 novembre 2026

**Sources et attribution.** Le [cours réel *Programming and Producing Drum Beats*, Erik Hawkins](https://online.berklee.edu/courses/programming-and-producing-drum-beats#syllabus) aborde la quantification, **le groove et groove quantize (leçon 8)**, **l'interaction dans la section rythmique (10)** et **la forme et les fills (11)**. Les deux créations AnaMu ci-dessous sont **des exercices de composition contrôlée**, jamais des transcriptions du manuel, des grooves culturels ou des évaluations de Berklee. Le contexte scientifique de [Nicole Biamonte, *Formal Functions of Metric Dissonance in Rock Music*, 2014](https://mtosmt.org/issues/mto.14.20.2/mto.14.20.2.biamonte.html) permet de distinguer **décalage d'un groupe** et **changement de groupe**, mais son analyse d'œuvres réelles n'est **pas** transférée mécaniquement à ce jeu MIDI.

### P-6 — retarder la caisse claire, puis revenir exactement au point de départ

[MIDI original, 16 mesures en quatre sections](./OMPRD-386/backbeat-deplacement-tension-retour.mid). 120 BPM, PPQ 480, 4/4 stable, **48 notes par section** et **192 en tout**. La grosse caisse GM36 (temps 1 et 3) et la charleston GM42 (croches) sont **strictement identiques** dans les quatre blocs, avec les mêmes vélocités. Seule la date des caisses GM38 est modifiée :

| Section | Positions de caisse locale à chaque mesure, ticks | Variante métrique voulue |
|---|---|---|
| A | **480, 1 440** | Backbeat sur 2 et 4 |
| B | **720, 1 680** | Caisse **+240 ticks**, sur les « et » suivant 2 et 4 |
| C | **600, 1 560** | Caisse **+120 ticks**, double-croche après 2 et 4 |
| D | **480, 1 440** | **Retour exact** à la section A |

Le retour **A = D a été vérifié sur les événements MIDI** (mêmes dates locales, pitches et vélocités), comme la stabilité du kick et de la charleston. Ces chiffres ne suffisent **pas** pour dire « B est tendu », « C groove mieux », ni « D est une résolution audible » : on a conçu une **hypothèse de tension et de retour**, pas mesuré son impact sur un auditeur. Par ailleurs **le mètre noté demeure 4/4**; une dissonance de placement n'est pas une modulation métrique.

**Analyse réutilisable.** Trouver d'abord une assise de subdivision autonome, puis les déplacements d'une couche qui porte habituellement un appui. Évaluer **l'amplitude et la répétition** du décalage, **la persistance des autres voix** et **le retour** à un ancien motif. Un drum fill peut résoudre ce décalage à une frontière de phrase, mais cette hypothèse demande une vraie étude de forme et d'écoute, pas un juge purement fondé sur les ticks.

### P-7 — cinq coups par deux mesures : 3+2 ou 2+3 ne nomme pas un genre

[MIDI original, 16 mesures en deux grandes variantes](./OMPRD-386/cinq-accents-3-2-vers-2-3-sans-style.mid). Une ligne GM42 déroule toujours **huit croches par mesure** pendant seize mesures, au tempo **116 BPM**, 4/4. Une seconde ligne GM76 (woodblock aigu) frappe **cinq fois sur chaque phrase de deux mesures**. Les huit premières mesures répètent une phrase **trois coups dans la première mesure, deux dans la deuxième**; les huit dernières inversent le rapport vers **deux puis trois**. Dans les deux blocs de huit mesures, **84 notes on**, soit **168 au total**; les 64 attaques de charleston par bloc sont **strictement identiques**.

| Variante, ticks relatifs à une phrase de deux mesures (3 840 ticks) | Première mesure | Deuxième mesure |
|---|---|---|
| A, trois puis deux | **0, 720, 1 440** | **480, 1 200** (ticks absolus de phrase **2 400, 3 120**) |
| B, deux puis trois | **0, 960** | **0, 720, 1 440** (ticks absolus de phrase **1 920, 2 640, 3 360**) |

**Ne pas appeler ces lignes « la clave traditionnelle 3-2 » ou « 2-3 ».** On ne possède ni la relation aux repères de la danse, ni la clave précise et les accentuations authentifiées, ni un corpus de performance. Le protocole illustre seulement **la direction d'une phrase à cinq événements** et les tensions possibles entre repères sur deux mesures. Le nom GM76 n'établit **ni technique, ni origine culturelle**. Une séquence cinq notes sur deux mesures peut aussi être un simple motif personnel. Pour l'orchestrateur, vérifier **l'emplacement du début de phrase**, sa répétition, le sens du passage vers la deuxième mesure et l'interaction avec la basse/les accords.

**Nuance théorique.** Le déplacement d'appuis sur un cycle régulier ne peut être correctement qualifié qu'en distinguant niveau de mètre, rythme de surface, groupements et **interprétation perceptive**. [Biamonte, 2014](https://mtosmt.org/issues/mto.14.20.2/mto.14.20.2.biamonte.html) justifie de garder distinctes les **dissonances de déplacement** et **de regroupement**. [Tabak, 2026](https://www.mtosmt.org/issues/mto.26.32.2/mto.26.32.2.tabak.php) rappelle en outre que les représentations métriques peuvent dépendre de l'enculturation, notamment pour les musiques du Pacifique colombien. Ces sources ne doivent **pas** servir à inventer un accompagnement de currulao depuis un simple GM76.

**Verdict de cette deuxième passe sur OMPRD-386 :** **deux fichiers, 360 notes on** (192 + 168), aucun nouveau code de production, aucun audio écouté ni performance instrumentale. La distinction tempo / grille / accent / phase / fonction formelle se lit dans la description; la preuve directe concerne **les octets MIDI**, et l'évaluation esthétique reste **AUDIO_REQUIRED**. [Inventaire complet](../../data/percussion-compound-meter-studies-2026-11-17.json).


## La batterie tout entière peut être en retard sans que ses membres soient désynchronisés — 17 novembre 2026

**Source du cours et comparaison expérimentale.** Le [syllabus de Programming and Producing Drum Beats, Erik Hawkins](https://online.berklee.edu/courses/programming-and-producing-drum-beats#syllabus) traite bien d'enregistrement MIDI en temps réel (leçon 2), de mécanique du kit et de programmation réaliste (3), de **Groove Quantize (8)**, d'amélioration de batterie captée (9), d'interaction en section rythmique (10) et de mix (12). Il ne publie **aucun preset de « humanization » à +16 ticks** ni l'expérience suivante : les chiffres appartiennent exclusivement à une **étude AnaMu originale**.

[**Fichier MIDI — quatre choix de référence temporelle**](./OMPRD-386/microtiming-snare-kick-tous-instruments.mid). **105 BPM, PPQ 480**, quatre blocs de quatre mesures, **48 notes par bloc, 192 en tout**. Le son nominal et la vélocité de chaque coup restent les mêmes entre les quatre blocs : GM42 charleston, GM38 caisse, GM36 grosse caisse. Voici les variations **relevées des événements directement depuis GitHub** :

| Bloc | Charleston | Caisse claire | Grosse caisse | Sens de la manipulation |
|---|---:|---:|---:|---|
| A | 0 tick | 0 tick | 0 tick | Référence sur la grille. |
| B | 0 | **+16** | 0 | Caisse claire **en retard relativement** aux autres couches. |
| C | 0 | 0 | **+16** | Grosse caisse **en retard relativement** aux autres couches. |
| D | **+16** | **+16** | **+16** | Toute la batterie **translatée ensemble** : les écarts entre coups restent les mêmes qu'en A. |

À **105 BPM**, 16 ticks correspondent à environ **19,05 millisecondes**. **En B et C**, ce sont les **rapports temporels entre instruments** qui changent. **En D**, la batterie complète est décalée d'autant **par rapport à la grille théorique**, mais ses relations internes sont conservées. Selon la présence d'une **basse, d'un métronome ou d'un autre groupe**, l'interprétation d'une translation globale sera différente de celle d'une caisse seule en retard.

**Les sources empiriques rendent le modèle plus exigeant.** [*Mapping timing and intensity strategies in drum-kit performance of a simple back-beat pattern*, *Journal of New Music Research* 51 (2022)](https://doi.org/10.1080/09298215.2022.2150649) compare les asynchronies inter-instruments et les stratégies de timing/intensité : **plusieurs batteurs peuvent choisir des combinaisons différentes**. [*Timing Is Everything…Or Is It?*, *Music Perception* 38(1), 2020](https://online.ucpress.edu/mp/article-abstract/38/1/1/111733/Timing-Is-Everything-Or-Is-It-Effects-of) a fait jouer **22 batteurs professionnels** sur différents patterns et références. Ces publications **n'établissent pas** que +16 ticks soit bon, mauvais, ou le timing de ces artistes.

**Encore plus important : son de l'attaque ≠ perception de la battue.** [Anne Danielsen, Justin London, Martin Torvik Langerød et Guilherme Schmidt Câmara, *All About That Bass Drum?*, *Annals of the New York Academy of Sciences*, 16 juin 2026](https://doi.org/10.1111/nyas.70306) étudient le **centre perceptif (P-center)** de sons musicaux combinés. La nature de l'attaque, notamment celle du kick, participe au moment où un événement est perçu. Un échantillon à attaque lente peut donner un **centre perçu** après son Note On MIDI; il ne suffit donc pas d'observer deux timestamps égaux pour affirmer que deux sons semblent jouer précisément ensemble.

**Procédure d'analyse musicale sérieuse :**

1. Connaître l'origine de **la grille de référence** : métronome, accompagnement, prise humaine, MIDI quantifié ou reconstruction hypothétique.
2. Comparer **les écarts inter-instruments** indépendamment des écarts **globaux à la grille** : la différence kick–snare–hat n'est pas la moyenne des retards de tout le groupe.
3. Comparer **les vélocités par instrument** et non la vélocité totale; si plusieurs pistes changent de dynamique ensemble, ne pas conclure à un décalage temporel.
4. En présence d'audio, mesurer séparément **l'attaque acoustique, l'enveloppe**, la résonance, les chevauchements et la possible position du P-center; il n'existe **pas** de conversion universelle d'un contrôleur GM en timing perçu.
5. Pour une composition, protéger **les relations qui portent le groove** avant d'appliquer une humanization; un décalage global peut être volontaire et **ne nécessite pas d'ajouter des erreurs aléatoires à chaque membre**.

**Limites de preuve.** MIDI_DIRECT : 192 notes, marqueurs, +16 ticks, égalité des vélocités, relation intra-batterie. MIDI_PROXY : tension, laid-back/pushed, équilibre. AUDIO_REQUIRED : P-center, fusion, groove et qualités du sample. CONTEXT_REQUIRED : référence de performance, configuration et style. L'étude est documentée dans le [manifeste de cette passe](../../data/percussion-performance-gesture-studies-2026-11-17.json). **Aucun échantillon n'a été rendu ou écouté, aucun moteur de groove ni logiciel de quantification n'a été développé.**

## Charleston : Note Off, état de pédale et ordre des événements

**Provenance.** Le [syllabus d'Erik Hawkins](https://online.berklee.edu/courses/programming-and-producing-drum-beats#syllabus) atteste la programmation MIDI, les échantillons de batterie et le traitement des grooves (leçons 2, 6 et 8). Les comparaisons ci-dessous sont des applications AnaMu. Les annexes MIDI et le manuel Roland sont des **sources techniques indépendantes**, pas des éléments attribués au syllabus de Berklee.

### HH-2 — Est-ce la fin de note ou la frappe suivante qui change la queue ?

[Six variantes avec contrôles isolés](OMPRD-386/charleston-gate-fermeture-et-controles-isoles.mid), **32 attaques**. Chacun des six blocs répète le même essai quatre fois, une fois par mesure. Le GM46, lorsqu'il existe, attaque au premier temps à vélocité 89. Les deux sons de fermeture nominale, lorsqu'ils existent, sont déclenchés à **+240 ticks**, à vélocité 70, avec un gate de 90 ticks.

| Bloc | GM46 ouvert | Son ajouté au tick +240 | Ce que le bloc contrôle |
|---|---|---|---|
| A | Gate de 720 ticks | Aucun | Référence GM46 isolée. |
| B | Gate de 240 ticks | Aucun | Effet éventuel d'un Note Off avancé sans nouvelle frappe. |
| C | Gate de 720 ticks | GM42 fermé | Effet éventuel d'une frappe fermée sans avance du Note Off. |
| D | Gate de 720 ticks | GM44 pédale | Effet éventuel du déclencheur de pédale sur la même ouverture. |
| E | Aucun | GM42 fermé | Frappe fermée seule. |
| F | Aucun | GM44 pédale | Frappe de pédale seule. |

La [spécification SoundFont, générateur 57](https://www.synthfont.com/sfspec24.pdf) prévoit que des zones d'un même preset peuvent partager une classe d'exclusion. Cela donne un mécanisme possible de coupure; ni les octets de C/D ni la présence de GM42/44 ne documentent la configuration d'un preset particulier. **Futur relevé sans imposer une écoute** : à banque et lecteur identifiés, comparer A/B pour la sensibilité au gate, C/D avec E/F pour ne pas prendre le transitoire ajouté pour la queue du GM46. Choisir une fenêtre où A contient encore un signal, fixer le gain, désactiver les effets si possible et relever la queue avant/après. Ne pas déduire un groupe d'exclusion d'une simple différence de mix. Comparer des sorties par voix, si disponibles, ou vérifier d'abord précisément la banque. **Aucun de ces rendus n'a été réalisé dans cette passe.**

### HH-3 — Un contrôle peut varier sans changer une seule note

[Trois séries de CC4 sur le même GM46](OMPRD-386/charleston-gm46-cc4-trois-trajectoires.mid). Chaque bloc a **8 Note On et 9 CC4**. Toute note (date, canal, pitch, vélocité et durée) est identique d'un bloc à l'autre. Un CC4 précède chaque Note On d'un tick. Les valeurs sont **0** en A, **127** en B et **0, 18, 36, 54, 72, 90, 108, 127** en C, puis le fichier réécrit 0 à la fin de chaque bloc. Ce retour explicite n'est pas une réinitialisation universelle de la banque ou de l'équipement.

La [MIDI Association](https://midi.org/midi-1-0-control-change-messages) définit le n°4 comme *Foot Controller*. Le [manuel d'implémentation du Roland TD-27, réception et émission CC4](https://static.roland.com/assets/media/pdf/TD-27_MIDI_Imple_eng04_W.pdf) précise un usage **configurable**, sur le canal de l'assignation de la surface du hi-hat, où 0→127 correspond à ouvert→fermé. Il couvre aussi d'autres assignations de contrôleur et de position de frappe. On ne peut donc pas rebaptiser *tout* CC4 « ouverture de charleston », ni transformer les valeurs en millimètres ou en niveaux acoustiques. **Décision AnaMu :** si le mapping n'est pas connu, décrire les messages bruts et noter *position physique inconnue*.

### HH-4 — Une égalité de ticks n'est pas une égalité d'ordre

[CC4 avant/après le Note On au même tick](OMPRD-386/charleston-cc4-ordre-meme-tick.mid). Dans chaque essai, CC4=0 est écrit au début, **CC4=127 et GM46 au tick 480**, retour CC4=0 au tick 960. **16 notes, 48 CC4**, en séquence A/B/B/A. Dans A, le CC4=127 précède le Note On dans l'unique piste SMF 0; dans B, il le suit. Le nombre d'événements, leurs valeurs et leurs ticks sont identiques **même si l'ordre des deux messages ne l'est pas**. Le Roland documente notamment un envoi de la position de pédale avant le Note On lorsque configuré ainsi. Notre contre-exemple B ne prétend pas émuler ce comportement à l'émission.

**Analyse :** garder l'ordre écrit des événements à delta zéro dans la piste avant toute fusion/normalisation. Pour une description conditionnelle sous un profil échantillonnant l'état à l'attaque, le dernier CC4 qui précède le Note On est 127 dans A, 0 dans B. Une réexportation ou un lecteur peut réordonner, échantillonner sur un autre cycle, suivre un changement après l'attaque, ou ignorer complètement CC4. **Réemploi :** si un profil cible garantit seulement « état avant frappe », exprimer l'antériorité avec un delta positif si le contexte l'autorise; vérifier l'ordre après réexportation. Un délai d'un tick n'est ni une recommandation de jeu ni une garantie de compatibilité.

[Manifeste et signatures des six études](../../data/percussion-hihat-state-studies-2026-11-17.json) · [Rôles de jeu et de groove](OPERC-160.md#charleston--destination-de-phrase-appuis-et-coordination-avec-la-caisse).

## Rendus audio des études de percussion

MP3 rendus à partir des MIDI des études, avec la banque GeneralUser GS. Les variantes d'un même fichier restent dans la même piste, sans correction de timing, de vélocité ou d'instrumentation.

- [Écouter — Grille, dynamique ou microtiming](OMPRD-386/quantization-groove-quatre-variables.mp3)
- [Écouter — Fills, même arrivée](OMPRD-386/fills-meme-arrivee-trois-versions.mp3)
- [Écouter — Linéaire ou superposé](OMPRD-386/lineaire-versus-superpose.mp3)
- [Écouter — Basse et grosse caisse](OMPRD-386/basse-kick-alignement-anticipation-retard.mp3)
- [Écouter — Même rythme, autres percussions](OMPRD-386/percussion-timbres-grille-invariante.mp3)
- [Écouter — Backbeat : déplacement et retour](OMPRD-386/backbeat-deplacement-tension-retour.mp3)
- [Écouter — Cinq accents : 3+2 puis 2+3](OMPRD-386/cinq-accents-3-2-vers-2-3-sans-style.mp3)
- [Écouter — Microtiming d’une voix ou de tout le kit](OMPRD-386/microtiming-snare-kick-tous-instruments.mp3)
- [Écouter — Charleston : fin de note ou coup de fermeture ?](OMPRD-386/charleston-gate-fermeture-et-controles-isoles.mp3)
- [Écouter — Les mêmes frappes avec trois séries de CC4](OMPRD-386/charleston-gm46-cc4-trois-trajectoires.mp3)
- [Écouter — CC4 et frappe au même tick](OMPRD-386/charleston-cc4-ordre-meme-tick.mp3)


**Contrôle en PCM avant encodage MP3.** Sur HH-2, avec FluidSynth 2.4.4 et GeneralUser GS, la fin de note avancée réduit la queue d'environ 0,9 dB RMS entre 320 et 650 ms après la première frappe ouverte. Par contraste, dans cette même fenêtre, le signal résiduel après retrait du témoin de fermeture seul descend d'environ 32 dB avec GM42 ou GM44. Ce résultat décrit le rendu de ce kit et de ce lecteur, sans conclure sur l'acoustique d'un vrai charleston.

**Témoins négatifs.** Les blocs de HH-3 et HH-4, rejoués séparément avec les mêmes ticks relatifs et dans une instance neuve, donnent exactement le même signal PCM à l'intérieur de chaque comparaison. Les MP3 livrés sont les rendus intégraux des fichiers MIDI d'origine. Ils ne cherchent pas à émuler le profil de pédale du TD-27. [Protocole et empreintes](../../data/percussion-audio-2026-11-17.json).
