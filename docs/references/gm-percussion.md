# General MIDI — percussions : carte vérifiable, GM1 et GM2

**Référence technique pour les dossiers de cours AnaMu, pas un nouveau syllabus ni un moteur.** Mise au point : 17 novembre 2026. [MIDI Association, GM1](https://midi.org/general-midi-level-1), [GM2](https://midi.org/general-midi-2), [table de touches GM1 archivée à Carnegie Mellon](https://www.cs.cmu.edu/~music/cmp/archives/cmsip/readings/GMSpecs_PercMap.htm), [table des programmes](https://www.cs.cmu.edu/~music/cmp/archives/cmsip/readings/GMSpecs_Patches.htm) et [MIDI Field Guide](https://midi.community/docs/general-midi/). La [représentation structurée parallèle](../data/gm-percussion-reference.json) contient les mêmes numéros et est réservée à la **lecture/documentation**, sans aucun changement de code exécuté par le projet.

## Le mécanisme : note ≠ programme ≠ banque ≠ son réel

En **General MIDI niveau 1**, les messages de **note sur canal 10** (**9 sur le fil**, si la numérotation commence à zéro) sélectionnent les **47 emplacements de percussion 35 à 81**. Chaque numéro est une *identité nominale* de son, pas une hauteur qu'on pourrait transposer pour changer de pitch. **La note 38 est Acoustic Snare; la note 60 est Hi Bongo; la note 81 est Open Triangle.** Une DAW affichant « C4 » ou « C3 » pour la note 60 peut varier dans ses **noms d'octaves**, mais **jamais dans le numéro 60**. Sous GM1, un Program Change sur le canal 10 ne donne **pas** accès à neuf kits standardisés; cette extension appartient à GM2 ou à des conventions GS/XG.

Un événement de batterie est un **numéro de note sur un canal de percussions**, associé à un instrument nominal du kit. Une **percussion chromatique** (vibraphone, marimba, timbales d'orchestre) se règle autrement, par **Program Change sur un canal mélodique**, et ses notes deviennent des **hauteurs jouées**. La distinction est essentielle pour analyser mélodie, harmonie, tessiture, transposition, durée, pédale et traits de jeu.

## GM1 : les 47 sons de percussion, noms et numéros exacts

### Batterie et claviers de batterie

| Note (décimale) | Nom GM1 normalisé | Famille documentaire |
|---:|---|---|
| 35 | Acoustic Bass Drum | grosse caisse |
| 36 | Bass Drum 1 | grosse caisse |
| 37 | Side Stick | caisse claire |
| 38 | Acoustic Snare | caisse claire |
| 39 | Hand Clap | clap |
| 40 | Electric Snare | caisse claire |
| 41 | Low Floor Tom | toms |
| 42 | Closed Hi-Hat | charleston |
| 43 | High Floor Tom | toms |
| 44 | Pedal Hi-Hat | charleston |
| 45 | Low Tom | toms |
| 46 | Open Hi-Hat | charleston |
| 47 | Low-Mid Tom | toms |
| 48 | Hi-Mid Tom | toms |
| 49 | Crash Cymbal 1 | cymbales |
| 50 | High Tom | toms |
| 51 | Ride Cymbal 1 | cymbales |
| 52 | Chinese Cymbal | cymbales |
| 53 | Ride Bell | cymbales |
| 54 | Tambourine | idiophones |
| 55 | Splash Cymbal | cymbales |
| 56 | Cowbell | idiophones |
| 57 | Crash Cymbal 2 | cymbales |
| 58 | Vibraslap | idiophones |
| 59 | Ride Cymbal 2 | cymbales |

### Percussions complémentaires et accessoires

| Note (décimale) | Nom GM1 normalisé | Famille documentaire |
|---:|---|---|
| 60 | Hi Bongo | peaux |
| 61 | Low Bongo | peaux |
| 62 | Mute Hi Conga | peaux |
| 63 | Open Hi Conga | peaux |
| 64 | Low Conga | peaux |
| 65 | High Timbale | peaux |
| 66 | Low Timbale | peaux |
| 67 | High Agogo | idiophones |
| 68 | Low Agogo | idiophones |
| 69 | Cabasa | idiophones |
| 70 | Maracas | idiophones |
| 71 | Short Whistle | effets |
| 72 | Long Whistle | effets |
| 73 | Short Guiro | idiophones |
| 74 | Long Guiro | idiophones |
| 75 | Claves | idiophones |
| 76 | Hi Wood Block | idiophones |
| 77 | Low Wood Block | idiophones |
| 78 | Mute Cuica | peaux |
| 79 | Open Cuica | peaux |
| 80 | Mute Triangle | idiophones |
| 81 | Open Triangle | idiophones |

**Quelques couples à ne pas fusionner :** 42/44/46 (**closed/pedal/open hi-hat**); 62/63 (**mute/open hi conga**); 71/72 (**short/long whistle**); 73/74 (**short/long güiro**); 78/79 (**mute/open cuíca**); 80/81 (**mute/open triangle**). Leur coexistence dans un fichier **ne prouve pas une alternance physiquement exécutée** sur un instrument réel. De même, 35 et 36 sont deux **désignations nominales de grosse caisse**; le standard ne définit pas leurs formes d'onde.

## GM2 : quinze ans de raccourcis à éviter

**GM2 propose neuf kits de percussions** par messages de **sélection de banque puis programme**. Les Program Changes sont affichés ci-dessous dans les deux numérotations : le programme « 25 » sur documentation 1–128 s'écrit « 24 » dans l'octet 0–127, **pas la note MIDI 25**.

| Kit GM2 | Programme affiché (1–128) | Valeur à transmettre (0–127) |
|---|---:|---:|
| Standard | 1 | 0 |
| Room | 9 | 8 |
| Power | 17 | 16 |
| Electronic | 25 | 24 |
| Analog | 26 | 25 |
| Jazz | 33 | 32 |
| Brush | 41 | 40 |
| Orchestra | 49 | 48 |
| SFX | 57 | 56 |

**Sélection GM2 sur canal 10 :** Bank Select **CC0 = 120** (soit **0x78**), **CC32 = 0**, puis **Program Change** correspondant au kit (ex. **24** pour Electronic). Les changements de banque n'entrent en vigueur qu'au Program Change. L'initialisation [GM2 On](https://midi.community/docs/general-midi/) (SysEx universel non temps réel **F0 7E 7F 09 03 F7**) peut être nécessaire sur un module compatible; **un fichier contenant le bon message n'assure pas qu'un lecteur non GM2 le respecte**. Le canal 10 GM2 est courant, mais **GM2 peut aussi convertir un autre canal en canal rythmique via la banque 120**; le critère « percussion = canal 10 » est donc **suffisant dans le cadre strict GM1**, mais non universel dans tous les MIDI. [Échange technique de la MIDI Association sur les canaux GM2](https://midi.org/community/midi-specifications/general-midi-level-2-ch-11-percussion).

La carte de touches GM2 étend la couverture autour du noyau GM1 par **14 désignations**, pour un intervalle **27–87** au total (**61 positions** dans la carte étendue). Les notes supplémentaires **27–34** : 27 High Q; 28 Slap; 29 Scratch Push; 30 Scratch Pull; 31 Sticks; 32 Square Click; 33 Metronome Click; 34 Metronome Bell. Les notes **82–87** : 82 Shaker; 83 Jingle Bell; 84 Belltree; 85 Castanets; 86 Mute Surdo; 87 Open Surdo. Les kits ne proposent **pas nécessairement les mêmes samples ou le même rôle par touche**, et « 9 kits × 61 positions = 549 instruments » serait un **faux compte**. La [référence comparative GM2](https://soundprogramming.net/file-formats/general-midi-level-2/) donne les variantes; la [MIDI Association](https://midi.org/general-midi-2) confirme la nature étendue du standard.

## Autre gisement GM1 : les sons percussifs sur canaux mélodiques

Sur des **canaux mélodiques** et avec les notes définissant alors **des hauteurs**, GM1 possède notamment ces programmes. Leurs noms ne font pas de ces programmes un kit de 47 batteries. Ils exigent leurs **propres gestes d'écriture** (accords, tenue, pédale ou nuances), qu'une simple comparaison de note on ne peut certifier.

| Programme affiché | Octet PC | Instrument GM1 |
|---:|---:|---|
| 9 | 8 | Celesta |
| 10 | 9 | Glockenspiel |
| 11 | 10 | Music Box |
| 12 | 11 | Vibraphone |
| 13 | 12 | Marimba |
| 14 | 13 | Xylophone |
| 15 | 14 | Tubular Bells |
| 16 | 15 | Dulcimer |
| 48 | 47 | Timpani |
| 113 | 112 | Tinkle Bell |
| 114 | 113 | Agogo |
| 115 | 114 | Steel Drums |
| 116 | 115 | Woodblock |
| 117 | 116 | Taiko Drum |
| 118 | 117 | Melodic Tom |
| 119 | 118 | Synth Drum |
| 120 | 119 | Reverse Cymbal |

**Deux confusions courantes :** « note 48 » sur canal 10 = **Hi-Mid Tom**, tandis que « programme 48 » sur canal mélodique = **Timpani** (octet PC = 47). De même « note 12 » sur canal 10 n'est pas un vibraphone GM1; c'est le **programme affiché 12** (octet PC 11) qui demande un vibraphone sur un canal mélodique. Les percussions à hauteur définie peuvent jouer **une ligne ou des accords**; la banque les rend accessibles, mais **ne remplace pas les contraintes de technique de jeu**.

## Ce que le General MIDI ne donne pas

1. **Fidélité acoustique garantie.** Le standard relie des **numéros à des noms de sons**, sans imposer une qualité précise de samples, microphones, accordages, résonances ou bibliothèque. Voir l'[énoncé de la MIDI Association](https://midi.org/general-midi-level-1) sur les caractéristiques acoustiques non définies.
2. **Un roulement joué par un percussionniste.** Un **buzz** ou un *double-stroke roll* suppose un geste, des rebonds et souvent une densité qui ne se déduit pas d'une **note on de longue durée**. [CM-343](../courses/berklee/CM-343.md#audit-de-gestes-de-roulements-et-de-résonances--17-novembre-2026).
3. **Un étouffement réel.** « Open/Closed » dans une table GM est un **nom de sample**; un instrument en concert peut nécessiter un geste ou une pédale, et les **exclusive groups** / auto-chokes dépendent du moteur. Ne pas inférer « l.v. » ou « choke » depuis un simple note off.
4. **Une configuration d'effectif.** Plusieurs notes GM simultanées = plusieurs **événements**; pas nécessairement plusieurs percussionnistes ni un instrument physiquement jouable en solo.
5. **Une origine stylistique ou culturelle.** Bongos, congas ou timbales portent des **noms d'instruments**, pas une preuve de tradition, de technique authentique ou de groove culturel. Pour une analyse de tradition, demander **partition, sources historiques et performance réelle**.

## Vérifier un fichier AnaMu en pratique

* **Avant toute interprétation**, trouver le standard annoncé (GM1/GM2/GS/XG ou inconnu), SysEx, **canal**, Bank Select, Program Change, numéro de note et piste; ne pas attribuer une table GM à un sample custom non documenté.
* Pour **GM1 canal 10**, joindre les numéros à la table ci-dessus; compter séparément **attaques de notes**, **instants distincts**, **timbres nominaux** et **nombre de voix/instruments réellement confirmés**.
* Pour **GM2**, rechercher **CC0=120 / CC32=0 + PC**. Sans banque, sans reset ou sans synthétiseur compatible, laisser le kit **indéterminé** si l'information manque.
* Pour les instruments **chromatiques**, traduire le **programme**, puis les **notes comme hauteurs** sur leurs canaux mélodiques; ne pas traiter la note 60 d'un vibraphone comme Hi Bongo.
* Quand le but musical est **accent**, **densité**, **contre-rythme** ou **résonance-pont**, tester les fonctions séparément. Une suite de coups correctement nommés ne démontre **ni beau groove**, ni percussionniste réel, ni qualité de mixage.
* **Vérifier les exemples existants :** [CM-343, exemple GM1](../courses/berklee/CM-343.md#audit-indépendant-du-vrai-exemple-gm--quatre-mesures-de-batterie-pas-un-solo-de-multi-percussion-17-novembre-2026) emploie 36, 38, 42, 49, donc **quatre des 47 entrées nominales**; son reste de vocabulaire ne prouve aucune composition réalisée. C'est précisément la place de ce référentiel, pas une preuve de maîtrise.

**Frontière du projet :** ces tables et observations sont **des données documentaires externes** utilisables pour approfondir les cours, **pas un moteur d'analyse**, ni un nouveau cours dans le registre académique. L'application à l'écriture reste dans [CM-343](../courses/berklee/CM-343.md), [CM-320](../courses/berklee/CM-320.md), [MTE-2114](../courses/udem/MTE-2114.md) et [OCMUS-105](../courses/berklee-online/OCMUS-105.md).


## Quatre témoins Standard MIDI File originaux — couverture contrôlée, sans écoute

Les **quatre fichiers ci-dessous** sont des créations AnaMu du 17 novembre 2026; les deux premiers sont **GM1**, les deux derniers **GM2**. Ils ne sont **ni des exercices officiels de CM-343 ni des rendus audio**, et leur audit ne prouve pas la qualité de la banque sonore, l'authenticité de technique ni le plaisir musical.

| Usage | MIDI réel (lien vers les octets GitHub) | Structure et couverture vérifiées |
|---|---|---|
| **Atlas GM1** | [GM1 — 47 touches isolées](../courses/berklee/CM-343/gm1-atlas-47.mid) | Type 1, 480 ticks/noire, 120 BPM, 47 notes **35–81**, 47 marqueurs nommés; **47 événements**, canal 10 humain exclusivement. |
| **Étude GM1 composée** | [GM1 — ensemble 16 mesures](../courses/berklee/CM-343/gm1-ensemble-16-mesures.mid) | 8 × 4/4 puis 8 × 7/8 au tempo 120, **261 frappes GM1** (31 numéros différents) et **48 notes de vibraphone** (PC 11, affiché 12) = **309 attaques**, fin au tick 28 800. |
| **Atlas des ajouts GM2** | [GM2 — 14 touches étendues](../courses/berklee/CM-343/gm2-atlas-14-nouvelles-notes.mid) | Type 1, **GM2 On SysEx**, banque percussions CC0=120 et CC32=0, PC0, 14 événements sur les notes **27–34 et 82–87**, 14 marqueurs de noms, aucune note pendante. |
| **Neuf kits GM2** | [GM2 — un même rythme dans neuf kits](../courses/berklee/CM-343/gm2-neuf-kits-comparaison.mid) | Type 1, 9 séquences de **deux mesures de 4/4** à 120 BPM; même motif de **30 frappes par kit**, soit **270 attaques**; **9 Program Change** sur canal 10, aux valeurs transmises 0/8/16/24/25/32/40/48/56, chacune précédée de CC0=120, CC32=0. |

### Ce que ces fichiers permettent de constater (et ce qu'ils ne peuvent pas garantir)

* **GM1** : les numéros 35–81 sont bien parcourus dans l'atlas; les marqueurs textuels indiquent le nom correspondant à la convention. Des lecteurs MIDI **non GM1** peuvent ignorer le reset ou déclencher des sons non conformes, sans que le fichier soit corrompu.
* **GM2** : le message SysEx **GM2 On** est bien présent sous forme d'événement Standard MIDI File (F0, longueur, données **7E 7F 09 03 F7**). Chaque kit est choisi par **Bank Select** et **Program Change**, donc le fichier donne les informations nécessaires à un synthétiseur **GM2 compatible**. Le kit **SFX** et les variantes **Orchestra/Brush** ne sont pas de simples changements de volume du kit Standard; ils peuvent modifier l'identité ou l'existence d'un son à une touche donnée.
* **Contrôle de qualité non perceptif** : chaque événement note on a un note off, toutes les pistes ont une fin valide, les valeurs de canal, de programme et de signature ont été **relues après publication sur GitHub**. Cela n'implique **aucune écoute de cette version**, aucune analyse spectrale de ses samples, aucun succès de changement de kit dans un lecteur arbitraire.
* **Comparaison inter-kits et contamination par les queues de son** : deux mesures d'attaques identiques passent immédiatement au kit suivant; un sample à **longue résonance** peut chevaucher la frontière. Le test prouve la **séquence de commandes MIDI**, pas une isolation acoustique entre variantes. Pour un futur A/B audio, insérer des fenêtres de silence et fixer une banque GM2 précise avant de juger la différence.
* **La réalité orchestrale demeure séparée** : le programme mélodique 12 (vibraphone) exige sa propre ligne de notes; les programmes GM1 113–120 incluent des **effets et instruments percussifs** dont le comportement de transposition dépend de la synthèse, sans être nécessairement des instruments **chromatiques académiques**. La convention MIDI n'établit ni type de pédale ni quatre mailloches, ni fidélité de marimba, timbales ou objets trouvés.

**Application à des cours attestés :** [CM-343 — étude des percussions](../courses/berklee/CM-343.md), [CM-320 — temps et groupement](../courses/berklee/CM-320.md), [MTE-2114 — instrumentation](../courses/udem/MTE-2114.md), [OCMUS-105 — rythme intériorisé](../courses/berklee-online/OCMUS-105.md). Ne pas promouvoir le registre de cursus sur la base d'une convention de soundbank.
