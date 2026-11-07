# AnaMu — Analyse Musicale

**AnaMu** est un projet de recherche et d'ingénierie visant à découvrir des régularités musicales explicables en rapprochant des représentations MIDI, des enregistrements, des paroles, des annotations émotionnelles humaines et des informations contextuelles (genre, époque, popularité).

L'objectif n'est pas de commencer par entraîner un modèle génératif. Nous voulons d'abord bâtir un **corpus multimodal vérifiable**, puis des moteurs d'analyse indépendants capables de dégager des motifs, des structures, des attentes, des transformations et des relations statistiques avec la perception humaine.

## Cap initial

1. Vérifier les conditions d'accès aux sources XMIDI, MetaMIDI/GigaMIDI et aux référentiels d'identification.
2. Construire un catalogue où **œuvre**, **enregistrement**, **transcription MIDI** et **annotations** sont des entités distinctes.
3. Tester le rapprochement sur un échantillon maximal de **1 000 MIDI XMIDI**, avec preuves et scores de confiance.
4. Mesurer la couverture et les erreurs avant d'envisager le passage à grande échelle.
5. Enrichir ensuite les chansons identifiées avec leurs paroles, leurs données de popularité et, ultérieurement, des observations audio synchronisées.

**[Feuille de route détaillée →](docs/roadmap.md)** · **[Premier audit de sources →](docs/audit-p0.md)**

## Principes

- **Réutiliser les travaux existants** : ne pas refaire les extractions ou statistiques déjà disponibles.
- **Émotions humaines d'abord** : distinguer les annotations humaines des labels inférés par machine.
- **Provenance partout** : chaque observation conserve sa source, sa méthode, son horodatage éventuel et son degré de confiance.
- **Rapprochements prudents** : ne jamais présenter une ressemblance musicale comme une identité démontrée.
- **Modules indépendants** : enrichir le corpus sans le recalculer entièrement à chaque analyse.
- **Coûts mesurés** : petits lots et workflows GitHub Actions déclenchés explicitement avant toute opération volumineuse.
- **Droits respectés** : les analyses éducatives n'autorisent pas automatiquement la redistribution des enregistrements, paroles ou transcriptions.

## État du projet

- **Phase** : P0 en cours et pilote P1 démarré ; accès XMIDI par plages HTTP et lecture partielle de la colonne `md5` GigaMIDI démontrés sur [GitHub Actions](https://github.com/leye0/AnaMu/actions).
- **Corpus local** : aucune archive complète importée ; trois petits fichiers XMIDI lus temporairement en mémoire, sans conservation des MIDI ni téléchargement d'audio.
- **Rapprochements** : tentative de jointure exacte sur trois fichiers XMIDI ; résultat **indéterminé** parce que les endpoints `/filter` et `/search` du viewer GigaMIDI expirent ou échouent. Aucun match confirmé, aucun taux de couverture calculé.
- **Accès GigaMIDI** : sur trois lignes, `md5` correspond aux octets MIDI (3/3). Le CSV original a un champ `file_path`, mais 86 chemins inspectés sur 86 sont anonymisés sous leur MD5 ; aucune clé XMIDI explicite n'y a été observée. Secret Actions `HUGGING_FACE_KEY` vérifié ; accès anonyme HTTP 401, requête authentifiée autorisée (HTTP 302), et schéma consulté avec succès (HTTP 200, une ligne de réponse de 5 762 octets). Champs de rapprochement disponibles (`md5`, `title`, `artist`, `audio_text_matches_mbid`, `audio_text_matches_score`), mais **aucune colonne explicite d'identifiant XMIDI ou d'émotion humaine** dans le schéma observé.
- **Workflows** : 19 tests unitaires ; lecture XMIDI ciblée à **12 966 652 octets** de transfert HTTP pour inspecter l'index ZIP et trois MIDI ; essai de projection d'une colonne Parquet limité à 24 Mo de lecture logique, sans extraire la colonne `music`. Aucun traitement massif lancé. [Pilote XMIDI](https://github.com/leye0/AnaMu/actions/runs/42335658732) · [Projection Parquet](https://github.com/leye0/AnaMu/actions/runs/42336189129).

La feuille de route est un document vivant : les hypothèses doivent être confirmées par des expériences mesurables avant d'être considérées comme des acquis.
