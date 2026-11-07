# AnaMu — Audit P0 : accès aux corpus et réutilisation des analyses

**Dernière vérification :** 7 novembre 2026.  
**État :** en cours — les deux sources sont accessibles partiellement ; empreintes vérifiées côté GigaMIDI et trois MIDI XMIDI lus, mais **aucune jointure exacte encore démontrée**.  
**Priorité scientifique :** les **émotions humaines de XMIDI** restent la référence ; GigaMIDI est un candidat pour retrouver les identités et réutiliser les caractéristiques calculées.

## Preuves d'exécution

Trois workflows à exécution bornée ont été créés et terminés. Les sondes initiales ne transfèrent aucun contenu de corpus ; la dernière lit une unique ligne du viewer, sans enregistrer ni afficher le contenu musical :

1. [P0 - audit sources, exécution réussie](https://github.com/leye0/AnaMu/actions/runs/42332678641), tests réussis, artefact JSON `anamu-p0-source-audit` conservé sept jours. **Aucune archive téléchargée.**
2. [P0 - vérifier accès GigaMIDI, exécution réussie](https://github.com/leye0/AnaMu/actions/runs/42333456588), quatre tests réussis. Requête `HEAD` ciblée sur `v2.0.0/validation/00001.parquet`, redirections désactivées, **aucun contenu téléchargé** : réponse anonyme **HTTP 401**, aucun jeton configuré lors de cette première exécution.

3. [P0 - accès authentifié confirmé](https://github.com/leye0/AnaMu/actions/runs/42333965236) : le secret Actions `HUGGING_FACE_KEY` est présent ; le même `HEAD` reçoit **HTTP 302** (redirection autorisée), sans téléchargement du Parquet.
4. [P0 - lecture minimale du schéma, exécution réussie](https://github.com/leye0/AnaMu/actions/runs/42334121279) : cinq tests réussis. API `datasets-server.huggingface.co/rows`, `v2.0.0/validation`, **une seule ligne**, réponse HTTP 200 de **5 762 octets**, total annoncé de **213 621 lignes pour ce split** (et non pour tout le corpus). Réponse plafonnée à 400 Ko, aucun MIDI ni valeur de ligne loggés, aucune archive téléchargée.

Les scripts se trouvent dans `scripts/source_audit.py`, `scripts/probe_gigamidi_access.py` et `scripts/probe_gigamidi_schema.py`. Ils n'ont besoin d'aucun modèle ML. Les résultats sont des observations datées, non des garanties permanentes.

## Sources examinées

| Source | Faits observés ou officiellement documentés | Accès et téléchargement partiel | Utilité pour AnaMu |
|---|---|---|---|
| [XMIDI](https://github.com/xmusic-project/XMIDI_Dataset) | 108 023 fichiers MIDI, émotions annotées par des professionnels. Dépôt GitHub ne contenant que `README.md`. | Les auteurs proposent un **ZIP Google Drive unique**. Le `HEAD` a rendu une page HTML, sans taille exploitable. **Taille réelle et possibilité d'extraction partielle non établies.** | **Corpus maître des étiquettes émotionnelles humaines.** |
| [GigaMIDI v2](https://huggingface.co/datasets/Metacreation/GigaMIDI) | > 2,1 millions de MIDI ; schéma annoncé avec titre, artiste, scores de correspondance audio+texte, ID Spotify et MusicBrainz, signatures et caractéristiques structurelles. Les auteurs déclarent intégrer XMIDI. | Hub `gated=auto` ; conditions de recherche non commerciale. Fichiers Parquet répartis par sous-ensembles ; ZIP complet ~5,51 Go et CSV de métadonnées ~1,25 Go. Le dataset documente un mode **streaming** après autorisation. **Une requête viewer d'une ligne a été mesurée à 5 762 octets de corps de réponse** ; l'efficacité sur un lot important reste à mesurer. | **Référentiel d'identification et d'analyses préexistantes ; pas une source de vérité émotionnelle humaine.** |
| [MetaMIDI](https://zenodo.org/records/5142664) | 436 631 MIDI, 168 032 rapprochés d'ID MusicBrainz, relations audio Spotify. | Enregistrement public mais fichiers **restreints** sur Zenodo ; demande avec affiliation et description de recherche. API publique n'expose pas de fichiers accessibles. | Résultats de rapprochement utiles si accès accordé ; déjà partiellement inclus dans GigaMIDI. |
| [Discover MIDI](https://huggingface.co/datasets/projectlosangeles/Discover-MIDI-Dataset) | Déclare 6,74 millions de MIDI et des caractéristiques pré-calculées. L'API du Hub annonce seulement cinq fichiers racine dont une grosse archive. | Pas de portail `gated` ; **pas de Parquet** répertorié dans l'API racine, viewer standard indisponible. Les caractéristiques peuvent être archivées ; accès individuel à tester. Licence CC BY-NC-SA 4.0. | Solution secondaire pour la recherche d'identités et de similarités ; budget de transfert à vérifier. |
| [EMOPIA](https://github.com/annahung31/EMOPIA) | 1 087 extraits MIDI de piano pop, émotions humaines en quatre quadrants. Zenodo publie un ZIP de **5 510 182 octets** (v1.0). | Petit téléchargement possible, mais **non nécessaire pour la jonction XMIDI→GigaMIDI**. Licence CC BY-NC-SA 4.0. | Jeu de validation humaine complémentaire, non substitut à XMIDI. |
| [Lakh MIDI](https://colinraffel.com/projects/lmd/) | 176 581 MIDI, dont 45 129 reliés à Million Song Dataset ; métadonnées et scores de rapprochement déjà publiés. | Les métadonnées et scores sont téléchargeables séparément. Licence CC BY 4.0 du jeu diffusé. | Référence de contrôle des rapprochements, sans réexécuter l'analyse audio originale. |

Les licences des compilations n'effacent pas les droits éventuels sur les compositions, enregistrements et paroles.

## Découverte importante : XMIDI dans GigaMIDI

La fiche GigaMIDI v2 affirme incorporer XMIDI, mais **n'établit pas** dans son schéma documenté :

- la présence d'une colonne gardant le **nom original de fichier XMIDI** ;
- la conservation du **MD5 exact de la version XMIDI non normalisée** ;
- le transfert des **11 étiquettes émotionnelles humaines**, de leur provenance et de la méthodologie d'annotation ;
- la proportion d'éléments XMIDI qui disposent de titres, d'artistes ou d'ID MusicBrainz fiables.

Ces quatre inconnues forment maintenant le cœur de P1. Il serait incorrect de conclure que « GigaMIDI identifie XMIDI » simplement parce qu'il le contient. Après autorisation, inspecter le schéma réel et les lignes accessibles **avant** d'implémenter des signatures musicales coûteuses. Si l'ID d'origine est absent ou le MIDI normalisé, chercher la table de traçabilité publiée ; seulement ensuite envisager les correspondances par empreintes/structure.

## Accès authentifié vérifié ; limite de jointure encore ouverte

- Le propriétaire a accepté les conditions GigaMIDI, puis ajouté le secret GitHub Actions **`HUGGING_FACE_KEY`** ; il ne doit jamais figurer dans le dépôt ou les logs.
- Même fichier Parquet : **HTTP 401 en anonyme**, **HTTP 302 après authentification**.
- La lecture viewer de `v2.0.0/validation?offset=0&length=1` donne **HTTP 200**, une ligne et **5 762 octets de corps de réponse**. Cette taille n'inclut pas les en-têtes ni les éventuels coûts internes du service.
- Le schéma de 37 champs observés contient notamment `md5`, `title`, `artist`, `audio_text_matches_score`, `audio_text_matches_sid`, `audio_text_matches_mbid`, `tempo`, `music_styles_curated` et plusieurs caractéristiques de notes et d'instruments.
- **Aucun champ explicitement nommé XMIDI, source filename ou émotion humaine** n'y apparaît. `md5` est prometteur, mais il faut vérifier s'il correspond au fichier XMIDI original, à une version normalisée ou à une autre représentation.
- Le corps de la ligne a été reçu temporairement par le script pour examiner ses clés, **sans l'afficher ni le sauvegarder**. Aucune correspondance XMIDI/GigaMIDI n'a encore été mesurée.

## Étape suivante : établir la traçabilité XMIDI → GigaMIDI

1. Chercher dans la documentation officielle de GigaMIDI/XMIDI une table de correspondance source, des chemins d'origine ou une définition précise du `md5`.
2. Tester sur un très petit échantillon l'identité d'empreintes **si des originaux XMIDI sont accessibles sans transfert massif** ; ne pas supposer qu'un MD5 d'un fichier MIDI normalisé correspond au fichier initial.
3. Si aucune clé directe n'existe, définir un plan de jointure conservatrice par caractéristiques symboliques avec estimation de faux positifs, et expliciter le coût prévisionnel.
4. Mesurer ensuite, avant toute grande extraction, le trafic réel d'un lot borné via l'API viewer ; une réponse de 5,8 Ko pour une ligne ne préjuge pas du trafic pour des centaines de milliers de lignes.
5. Garder les annotations humaines XMIDI séparées et les relier uniquement à des entrées identifiées avec un niveau de confiance documenté.

## Nouvelles expériences — 7 novembre 2026

### GigaMIDI : validité des MD5

La [sonde d'empreintes](https://github.com/leye0/AnaMu/actions/runs/42335271305) a décodé temporairement trois petits MIDI exposés par l'API viewer et vérifié que leurs empreintes correspondent exactement à la colonne `md5` (**3 sur 3**). Cela prouve la signification de ce champ **pour les échantillons testés**, sans démontrer que les fichiers d'origine XMIDI ont les mêmes octets après normalisation.

### XMIDI : une archive ZIP exploitable sans téléchargement total

- [Sonde HTTP Range](https://github.com/leye0/AnaMu/actions/runs/42335377434) : l'URL de téléchargement public Google Drive répond **HTTP 206** pour les derniers 65 536 octets, avec une fin d'archive ZIP valide. Taille annoncée : **449 632 771 octets** (≈450 Mo décimaux).
- [Pilote de lecture ciblée](https://github.com/leye0/AnaMu/actions/runs/42335658732) : index ZIP de **108 024 entrées**, **108 016 MIDI éligibles** au plafond de taille sélectionné. Trois exemples extraits **en mémoire**, étiquettes provenant des noms de fichiers : `sad/rock` (45 691 octets), `romantic/pop` (41 144 octets), `happy/country` (35 811 octets).
- **Trafic réel mesuré** : **12 966 652 octets** reçus via **14 requêtes Range** (index central ZIP + fichiers ciblés). Aucun fichier musical conservé ; aucune archive complète téléchargée.
- La tentative de contrôle de correspondance par `/filter` a expiré. Les trois résultats de jointure sont **inconnus**, et non trois non-correspondances.

### GigaMIDI : limites du viewer, alternative Parquet

- [Vérification des endpoints de recherche](https://github.com/leye0/AnaMu/actions/runs/42335780264) : `/is-valid` annonce `filter` et `search` disponibles ; pourtant `/filter` a expiré sur un MD5 de contrôle et `/search` a renvoyé **HTTP 500**. Ne pas lancer des milliers de recherches une par une sans résoudre ce problème.
- [Projection Parquet `md5` uniquement](https://github.com/leye0/AnaMu/actions/runs/42336189129) : succès avec `pyarrow` et un accès `hf://` par plages HTTP. Le premier shard de validation contient **106 810 lignes**, réparties en **1 069 groupes** de 100 ; la colonne `md5` du premier groupe occupe **3 589 octets compressés**. **100 empreintes valides** lues, **5 473 205 octets de lectures logiques** au total (métadonnées Parquet incluses), sous un plafond de 24 Mo. Aucune colonne `music` demandée.
- Les octets de *lecture logique* ne sont pas un compteur réseau exact : le cache de lecture du système de fichiers peut ajouter des transferts. Lire tous les groupes de tous les shards exigera une estimation de débit, de requêtes, de trafic et de coût avant exécution.

### Nouvelle priorité de P1

1. Évaluer si une table de provenance publiée associe déjà le `md5` de GigaMIDI à l'original XMIDI ; c'est la voie prioritaire.
2. À défaut, **mesurer sur quelques groupes** le coût réel de collecte de la seule colonne `md5` (pas les MIDI) et estimer le coût à l'échelle des ≈2,1 millions de lignes.
3. Construire un petit index de MD5 GigaMIDI, comparer aux empreintes de quelques fichiers XMIDI extraits par plages, et publier **des exemples exacts** ou un échec documenté. Les annotations XMIDI restent des observations humaines séparées, associées seulement après preuve de jointure.

**Aucune extraction de plusieurs Go ni aucun traitement audio ne sont autorisés implicitement par cet audit.**
