# AnaMu Grammar — corpus orchestraux polyphoniques (audit du 9 novembre 2026)

**But :** disposer d'arrangements complets, pas d'une réduction pour piano,
pour tester les relations `PARALLEL`, `SEQUENCE`, la conduite des voix, les
groupements, l'orchestration et les rôles instrumentaux. Un orchestre transcrit
ne fournit **pas**, à lui seul, une performance humaine (rubato réel, son,
enveloppes, dynamique acoustique). Les scores restent des scores.

## Priorités documentées

| Priorité | Source primaire | Contenu vérifié | Format source | Droits/risque | Usage AnaMu |
|---|---|---|---|---|---|
| **A — annotations complètes** | [S3, Symbolic Symphony Set (ISMIR 2024)](https://github.com/iis-mctl/mctl-symphony-dataset) ; [notice scientifique](https://ismir2024program.ismir.net/lbd_463.html) | **4 symphonies entières, 16 mouvements**, 285 387 notes, 532 phrases et 7 290 accords, avec notes par instrument, signatures, thèmes/phrases/sections, fonctions harmoniques et couches orchestrales `mel`, `rhythm`, `harm` | **MusicXML + CSV + PDF** ; MIDI non déclaré dans le README | Dépôt MIT ; statut juridique des transcriptions et annotations à vérifier avant **redistribution** | Validation de G1/G2/G3/G6 par œuvre, rôle des instruments et relations explicables ; source prioritaire malgré format non MIDI |
| **A — partitions et mélodie principale** | [OpenScore Orchestra / Hauptstimme](https://github.com/MarkGotham/Hauptstimme) ; [archive Zenodo](https://zenodo.org/records/15425749) | **Environ 100 mouvements**, dont les 9 symphonies de Beethoven, 4 de Brahms, Amy Beach ; annotations humaines indiquant la mélodie principale et ses passages entre pupitres, relations entre parties | **MuseScore + MusicXML** ; MIDI à produire par conversion ; des CSV d'annotations et de notes dérivées | **Scores CC0, annotations CC BY-SA, code MIT** selon les auteurs ; attribuer correctement les annotations | Évaluer les transferts de thème et voix principales, pour G2/G3 et `DEPEND` |
| **B — vrai MIDI avec orchestration appariée** | [LOP database, Crestel/Esling](https://qsdfo.github.io/LOP/database.html) ; [publication ISMIR 2017](https://www.mcgill.ca/mpcl/files/mpcl/crestel_2017_ismir.pdf) | **196 couples** partition piano / orchestration ; inventaire de flûte, hautbois, cor, violon, alto, violoncelle, contrebasse, timbales, etc. ; l'auteur signale une qualité inférieure pour le sous-dossier ISMLP | **MIDI** (archive zip) + outils d'alignement | Licence de redistribution du contenu musical **non établie** : utilisation limitée à étude locale tant que non vérifiée | Probes `PARALLEL`, doublures, activation d'instruments ; audits des paires mal alignées |
| **B — vraie banque de MIDI orchestraux** | [SOD, Symbolic Orchestral Database](https://qsdfo.github.io/LOP/database.html) ; [réutilisation académique MMT](https://github.com/salu133445/mmt) | Fichiers orchestraux **MIDI ou MusicXML** ; taille et provenance par fichier à auditer avant sélection | **MIDI et MusicXML** (`SOD.zip`) | Conditions de chaque fichier **non résolues** ; aucune redistribution automatique | Volume et diversité, après contrôle de l'instrumentation et de la provenance |
| **C — vaste MIDI multi-instruments, pas vérité experte** | [SymphonyNet](https://symphonynet.github.io/) ; [code](https://github.com/symphonynet/SymphonyNet) | Le site annonce **46 359 MIDI**, en moyenne **20 pistes**, et 3 284 h ; le même site affiche 46 187 dans un tableau secondaire (écart à clarifier) | **MIDI** via Google Drive | Licence MIT du *code* explicite, mais statut juridique des **MIDI individuels non confirmé** | Stress test de performance, diversité de textures ; ne pas en tirer une vérité de thèmes, rôles ou droits |

## Invariants d'importation, non négociables

1. **Deux catégories de corpus** : `(a)` partition orchestrale MusicXML/MuseScore
   et `(b)` fichier MIDI orchestral original. Une conversion MusicXML → MIDI
   est un nouvel artefact dérivé ; ne pas l'appeler « performance humaine ».
2. **Inventaire réel par pièce** : pistes, canaux, changements de programme,
   noms de pupitres, nombre de notes, notes simultanées, durée, contrôleurs,
   variations de tempo, signature temporelle ; conserver l'original.
3. **Labels distincts** : les indications humaines de rôle/orchestration et
   les accords annotés sont des *cibles d'évaluation*, jamais des attributs
   que l'analyse est autorisée à lire pour se prédire elle-même.
4. **Découpage par composition/symphonie** : ne pas compter les 16 mouvements
   de S3 comme 16 œuvres indépendantes ; éviter tout mélange d'une même
   composition entre entraînement, sélection et test.
5. **Droits documentés par fichier** : la licence du code d'une publication
   n'est pas automatiquement celle des fichiers musicaux. Ne rien recopier
   dans le dépôt sans provenance et licence explicite de la transcription.
6. **Contrôle de fidélité** : MusicXML → MIDI peut perdre l'orthographe des
   notes, les articulations, la structure des répétitions et les nuances ;
   G0 conserve des octets MIDI, pas ces informations de partition.

## Choix de première expérience

Prendre **S3** comme banque d'annotations expertes pour les structures de
phrases, les rôles instrumentaux et les couches orchestrales ; prendre
**OpenScore/Hauptstimme** comme contrôle indépendant du passage du thème
entre instruments. Utiliser **LOP/SOD** pour les véritables MIDI multipistes
en stress test, après audit de licences et de fichiers. Les métriques seront
**séparées par cible** : précision des couches orchestrales, frontières de
phrases, fonctions harmoniques et stabilité des relations temporelles, avec
baselines triviales. Ne pas confondre ces cibles avec un score émotionnel.

**État de la récupération :** liens et descriptions officielles vérifiés ;
archives binaires non téléchargées, partitions non converties, nombre de
fichiers réellement parsables et licences individuelles encore à confirmer.
