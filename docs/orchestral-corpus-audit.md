# AnaMu Grammar — corpus orchestraux polyphoniques (audit du 9 novembre 2026)

**But :** disposer d'arrangements complets, pas d'une réduction pour piano,
pour tester les relations `PARALLEL`, `SEQUENCE`, la conduite des voix, les
groupements, l'orchestration et les rôles instrumentaux. Un orchestre transcrit
ne fournit **pas**, à lui seul, une performance humaine (rubato réel, son,
enveloppes, dynamique acoustique). Les scores restent des scores.

## Priorités documentées

### Premier corpus réel importé — deux mouvements symphoniques (G0/G1)

Les deux fichiers sources ci-dessous sont désormais **présents en binaire**
dans `data/orchestral/`, avec provenance, URL de publication et empreinte
SHA-256 par pièce dans `data/orchestral/SOURCES.json`. La bibliothèque Mutopia
déclare **Public Domain** pour ces éditions :

1. [Beethoven, Symphonie nº 5, mouvement I](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=941) :
   13 pistes, 8 295 appuis de touches non ambigus, polyphonie instantanée
   observée jusqu'à 22 touches simultanément maintenues ; **une** consigne
   explicite de tempo et aucun message de contrôle MIDI.
2. [Beethoven, Symphonie nº 7, mouvement II](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=595) :
   13 pistes, 6 041 appuis non ambigus, polyphonie jusqu'à 20 ; 12 messages
   de tempo à une valeur identique et **1 464 contrôleurs CC7** (volume MIDI).

Ces MIDI ont été récupérés depuis le [miroir de fichiers de `fate-pv`](https://github.com/jtydhr88/fate-pv/blob/main/score/SOURCES.md),
dont la déclaration de provenance pointe vers Mutopia. **Nous n'avons pas
encore comparé octet par octet le miroir aux téléchargements originaux, ni
validé la conformité des pistes à une partition critique.** Les noms de piste
inclus dans les fichiers, comme `english horn`, sont des **déclarations dans
le MIDI**, pas une identification musicologique : ils ne suffisent pas à
confirmer les instruments employés par Beethoven.

Reproduction :

```bash
python -m pip install 'mido>=1.3,<2'
python scripts/orchestral_grammar_probe.py
python -m unittest discover -s tests -p test_orchestral_grammar_probe.py -v
```

Le rapport déterministe est dans
`reports/orchestral-grammar-probe-2026-11-09.json`. Il inclut inventaire des
événements et programmes, contrôleurs, signatures tempo, pistes, notes par
piste, simultanéités exactes et un échantillon borné de 5 000 relations G1
entre notes adjacentes dans l'ordre des attaques. **Cet échantillon est
biaisé vers les accords simultanés et ne doit pas être présenté comme une
fréquence de toutes les relations possibles.** Aucune émotion, fonction
harmonique, intention de ralentir ou volume acoustique n'est déduite.

Prochain audit utile : confrontation des programmes MIDI à une partition
MusicXML critique, identification des pupitres manquants, puis annotation
humaine des motifs/phrases pour valider les futures couches G2/G3.

### Confrontation à deux partitions indépendantes (G0 ↔ MusicXML)

Nous avons ajouté deux **partitions orchestrales complètes compressées `.mxl`**
du corpus [Hauptstimme](https://github.com/MarkGotham/Hauptstimme). Ses auteurs
déclarent les **partitions CC0 1.0**, les **annotations CC BY-SA** et le code
MIT. Ici, seules les partitions CC0 sont copiées ; aucune annotation humaine
CC BY-SA n'est distribuée. Chaque fichier a son SHA-256 et une provenance
distincte des MIDI Mutopia dans `data/orchestral/SOURCES.json`.

Le nouveau `score_midi_orchestration_audit.py` lit les listes de parties
MusicXML et les compare aux noms d'instruments **écrits dans les MIDI** :

| Mouvement | Parties de la partition Hauptstimme | Pistes MIDI actives | Familles dans la partition mais absentes des noms MIDI | Familles dans le MIDI mais absentes des parties de la partition |
|---|---:|---:|---|---|
| Beethoven 5/I | **18** | **12** | Cor, trompette | Cor anglais |
| Beethoven 7/II | **19** | **12** | Cor, trompette | Cor anglais |

Ce résultat **n'établit pas** que les notes des cors/trompettes sont absentes
du MIDI : elles pourraient être regroupées ou mal étiquetées. Il établit que
les déclarations de pupitres ne correspondent pas à celles d'une autre
édition orchestrale, donc **pas de vérité instrumentale implicite** dans le
MIDI. Les partitions MusicXML et les MIDI n'ont pas encore été alignés note
par note, et le comptage des notes écrites ne déroule ni reprises, ni tenues
liées, ni transpositions. Les timbres et intensités acoustiques restent hors
du domaine de cette comparaison.

Reproduire :

```bash
python scripts/score_midi_orchestration_audit.py
python -m unittest discover -s tests -p test_score_inventory.py -v
```

Résultat : `reports/orchestral-score-inventory-2026-11-09.json`.

**À faire pour G2 :** exploiter les annotations humaines Hauptstimme comme
vérité indépendante (avec leurs conditions CC BY-SA), vérifier la cohérence
des hauteurs et positions temporelles entre éditions, et construire une
segmentation de voix/motifs mesurée avec une métrique explicite.

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

## Prochains corpus candidats (non importés)

Les **deux mouvements Beethoven** importés sont le premier corpus réel.
Pour le compléter, évaluer **S3** comme banque d'annotations expertes des
structures de phrases et des couches orchestrales, puis les annotations
**Hauptstimme** pour les passages de mélodie entre instruments. Les droits
des annotations doivent être respectés avant toute copie. **LOP/SOD**
restent des candidats aux stress tests multipistes après audit des fichiers
et des licences. Les métriques doivent rester séparées par cible :
frontières de phrases, rôles instrumentaux, fonctions harmoniques et
relations temporelles, avec baselines simples.

**État du corpus (10 novembre 2026) :** deux MIDI Beethoven et leurs deux
partitions MusicXML de référence sont effectivement importés, parsés,
empreintés et testés dans GitHub Actions. Les archives **S3, LOP/SOD et
SymphonyNet** proposées dans le tableau ci-dessus ne sont **pas** importées ;
leurs formats, fichiers précis et droits de redistribution restent à auditer
avant usage. Les annotations humaines Hauptstimme ne sont pas redistribuées.
