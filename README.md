# AnaMu — Analyse Musicale

**AnaMu** est un projet de recherche et d'ingénierie visant à découvrir des régularités musicales explicables en rapprochant des représentations MIDI, des enregistrements, des paroles, des annotations émotionnelles humaines et des informations contextuelles (genre, époque, popularité).

L'objectif n'est pas de commencer par entraîner un modèle génératif. Nous voulons d'abord bâtir un **corpus multimodal vérifiable**, puis des moteurs d'analyse indépendants capables de dégager des motifs, des structures, des attentes, des transformations et des relations statistiques avec la perception humaine.

## Cap initial

1. Vérifier les conditions d'accès aux sources XMIDI, MetaMIDI/GigaMIDI et aux référentiels d'identification.
2. Construire un catalogue où **œuvre**, **enregistrement**, **transcription MIDI** et **annotations** sont des entités distinctes.
3. Tester le rapprochement sur un échantillon maximal de **1 000 MIDI XMIDI**, avec preuves et scores de confiance.
4. Mesurer la couverture et les erreurs avant d'envisager le passage à grande échelle.
5. Enrichir ensuite les chansons identifiées avec leurs paroles, leurs données de popularité et, ultérieurement, des observations audio synchronisées.

**[Feuille de route détaillée →](docs/roadmap.md)** · **[Premier audit de sources →](docs/audit-p0.md)** · **[Première jointure exacte XMIDI ↔ GigaMIDI →](docs/p1-exact-join.md)**

## Principes

- **Réutiliser les travaux existants** : ne pas refaire les extractions ou statistiques déjà disponibles.
- **Émotions humaines d'abord** : distinguer les annotations humaines des labels inférés par machine.
- **Provenance partout** : chaque observation conserve sa source, sa méthode, son horodatage éventuel et son degré de confiance.
- **Rapprochements prudents** : ne jamais présenter une ressemblance musicale comme une identité démontrée.
- **Modules indépendants** : enrichir le corpus sans le recalculer entièrement à chaque analyse.
- **Coûts mesurés** : petits lots et workflows GitHub Actions déclenchés explicitement avant toute opération volumineuse.
- **Droits respectés** : les analyses éducatives n'autorisent pas automatiquement la redistribution des enregistrements, paroles ou transcriptions.

## État du projet

- **Phase :** P0 a démontré l'accès partiel aux deux corpus ; P1 a confirmé **une première jointure binaire exacte XMIDI ↔ GigaMIDI** par MD5. [Exécution vérifiée du 7 novembre 2026](https://github.com/leye0/AnaMu/actions/runs/42336949364).
- **Émotions humaines :** l'exemple joint est étiqueté `quiet` / `traditional` dans XMIDI ; l'étiquette ne provient **pas** d'une détection émotionnelle automatique de GigaMIDI.
- **Mesures :** 100 XMIDI valides et distincts prélevés en mémoire ; 5 200 MD5 GigaMIDI examinés dans **un seul shard** jusqu'au premier match. 13 328 176 octets HTTP pour XMIDI ; 5 657 337 octets de lectures *logiques* Parquet (pas un compteur réseau exact). **24 tests réussis**.
- **Limites :** le balayage s'est arrêté au premier match, donc **aucun taux de couverture global** n'est calculable. Aucun titre, artiste ni MusicBrainz n'a été confirmé pour cet exemple ; aucune chanson audio ni parole n'a été récupérée. Le job a duré environ 5 min 28 s : optimiser les requêtes avant de généraliser.
- **Conservation :** aucun gros corpus ni audio téléchargé ou archivé, aucun contenu MIDI conservé. Les limites de temps et de volume sont imposées dans les scripts et workflows.

La feuille de route est un document vivant : les hypothèses doivent être confirmées par des expériences mesurables avant d'être considérées comme des acquis.
