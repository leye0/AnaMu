# Corpus d’opéras AnaMu

Décision de Léon du **19 novembre 2026** : constituer en parallèle des cours un **gros corpus de MIDI d’opéras, avec mélodie vocale et paroles disponibles pour chaque fichier**. Ce corpus rassemble des œuvres existantes; il ne constitue pas un moteur d’analyse ni une génération de musique.

## Premier lot réellement acquis

**106 couples MIDI–paroles, 103 passages musicaux distincts, 10 opéras, 6 compositeurs, 19 éditions sources.** Ce sont des passages, pas 103 opéras ni 103 airs : le lot comprend notamment 46 récitatifs et deux chœurs. Les trois sections du no 4 de La Flûte enchantée comptent comme un seul passage; les deux éditions du no 15 également.

- [Catalogue des fichiers](CATALOGUE.md) : MIDI de partition, MIDI vocal isolé, paroles et provenance.
- [Manifeste exploitable](manifest.json) : identités, langues, indices de pistes, chemins et limites.
- [Sources, éditions, crédits et licences](sources.json).
- [Attributions humaines](ATTRIBUTION.md).

Chaque dossier `items/<id>/` contient `score.mid` (copie du MIDI source), `vocal.mid` (piste ou pistes vocales isolées) et `lyrics-source.ly` (paroles syllabiques conservées depuis le LilyPond). Les archives téléchargées et les partitions sont dans `sources/`. Les fichiers d’une même édition gardent sa licence; ce répertoire n’a pas de licence globale remplaçant les licences individuelles.

## Ce qui est acquis, et ce qui reste à établir

Les paroles sont **disponibles dans la partition source**, avec syllabes, prolongations et parfois plusieurs couplets ou traductions. Elles ne sont pas toutes intégrées au MIDI. **Aucun alignement note–syllabe n’est exporté ni validé dans ce lot.** Le texte conservé est du LilyPond, pas une transcription littéraire normalisée ni une version garantie complète du livret.

Les sélections vocales s’appuient sur les noms de pistes quand ils existent, les parties des partitions et, pour Giulio Cesare, le début des hauteurs. Une concordance initiale ne garantit pas toutes les notes. Les doublures instrumentales, portées créées tardivement, notes liées et ensembles ont nécessité des affectations explicites. Le manifeste documente la méthode par entrée; aucune audition humaine ni comparaison exhaustive note à note n’est revendiquée.

Deux lacunes précises : le récitatif `BBArecit` de Giulio Cesare n’a pas de bloc MIDI dans la source; le passage `CHBcesare` conserve le chœur dans `score.mid`, mais son `vocal.mid` isole seulement Cesare et l’affectation des autres voix reste à revoir. Certains récitatifs regroupent plusieurs personnages sur une même portée : on ne prétend pas avoir séparé ces personnages.

## Acquisition à grande échelle

L’objectif est une collection de **milliers de passages** à terme, en diversifiant les opéras, compositeurs, époques, langues et tessitures. Le présent lot est un amorçage, largement dominé par Giulio Cesare; il ne représente pas encore cet objectif.

Pour chaque prochain lot :

1. Repérer une édition téléchargeable avec provenance et droits explicites; conserver l’URL exacte, la date, le contributeur, la licence et l’empreinte des octets.
2. Acquérir MIDI et partition symbolique avec paroles ensemble lorsque possible. MusicXML, MEI et LilyPond restent des sources précieuses même si le livrable sonore est MIDI.
3. Identifier l’opéra, le passage, les personnages et les parties vocales; garder les ensembles à plusieurs voix et les récitatifs clairement étiquetés. Exclure les réductions instrumentales sans partie chantée identifiable du corpus apparié.
4. Conserver les variantes et transpositions sous un même identifiant musical; ne pas gonfler les comptes avec les parties instrumentales, les arrangements ou les copies identiques.
5. Isoler les voix avec les silences initiaux, tempos et mesures conservés. Fournir le texte original et son origine; distinguer texte disponible, syllabes rattachées à la partition et alignement MIDI effectivement vérifié.
6. Consigner les lacunes, relire les cas ambigus, puis diversifier les sources. Ne pas déclarer une piste correcte parce qu’elle utilise un son de chœur ou qu’elle est la plus aiguë.

Pistes suivantes : autres opéras de Mutopia, éditions symboliques ouvertes d’opéras complets, puis Aria Database pour la découverte d’airs. Les notices et liens d’autres sites ne sont pas encore des fichiers acquis et leurs droits de réutilisation doivent être établis avant redistribution. Les corpus de lieder ou de piano ne doivent pas être comptés comme des opéras.

Le suivi académique reste distinct; les tâches ouvertes sont dans le [TODO unique](../../docs/todo-university-coverage.md). Ce corpus n’atteste aucune compétence universitaire nouvelle et n’active ni moteur, ni tests, ni CI.
