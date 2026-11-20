# Corpus d’opéras AnaMu

Décision de Léon du **19 novembre 2026** : constituer en parallèle des cours un gros corpus de MIDI d’opéras avec partie vocale identifiable et paroles disponibles pour chaque fichier.

## État acquis

**439 couples MIDI–paroles, 30 opéras, 11 compositeurs, 46 éditions sources.** Les 439 MIDI de partition ont des empreintes SHA-256 différentes. Ce nombre compte des fichiers, pas 439 opéras ni 439 airs distincts : récitatifs, scènes, chœurs, ensembles, arrangements et variantes sont présents. Le dédoublonnage musicologique entre éditions reste partiel.

La seconde passe ajoute **333 entrées**, dont 312 passages chantés issus de six grandes éditions françaises : David et Jonathas (40), Phaéton (54), Psyché (56), Armide (66), Hippolyte et Aricie (69) et Les Fêtes de Ramire (27). Elle ajoute aussi 21 airs ou arrangements de Purcell, Vinci, Lully et Haendel. Les sections sans paroles sont écartées; les deux groupes de copies identiques repérés dans l’archive Phaéton concernent ces sections instrumentales.

- [Catalogue de tous les fichiers](CATALOGUE.md).
- [Manifeste exploitable](manifest.json) : identités, langues, pistes vocales, événements de paroles, provenance et limites.
- [Sources et licences](sources.json) · [Attributions](ATTRIBUTION.md).
- [Bilan de l’acquisition](ACQUISITION.md) · [Registre de la seconde passe](acquisition-2026-11-19-expansion.json).

## Contenu d’une entrée

Chaque dossier `items/<id>/` propose `score.mid` (copie du MIDI acquis), `vocal.mid` (piste ou pistes vocales extraites) et les paroles sous une des formes suivantes :

- `lyrics-source.ly` conserve les paroles et leur contexte LilyPond du premier lot ou d’une source sans texte MIDI;
- `lyrics-syllables.txt` reproduit les syllabes intégrées dans le MIDI, séparément pour chaque piste de paroles;
- `lyrics-timed.tsv` conserve l’indice de piste, le tick MIDI, la position en noires, la syllabe, la piste de notes associée lorsqu’elle est établie et les hauteurs attaquées à ce tick.

**437 entrées disposent maintenant d’un export d’horodatages de paroles : 99 233 événements de syllabes.** Les deux autres ont leurs paroles dans le LilyPond. Les fichiers sources acquis sont conservés avec leurs notices; pour une archive MIDI, le manifeste indique aussi le nom exact du membre copié.

L’export temporel copie les événements de la source. La correspondance des ticks avec les attaques des pistes retenues constitue un contrôle structurel, **pas une validation indépendante note–syllabe**, une garantie de prononciation ni une audition. Les mélismes, reprises, plusieurs couplets, traductions et personnages partageant une portée doivent encore être relus musicalement. Un texte syllabique n’est pas une transcription normalisée du livret complet.

## Corrections de la première passe

Six anciennes extractions vocales ont été corrigées : Sesto « La giustizia ha già sull’arco », Cara sposa, Solo dal brando, Sulla ruota di fortuna, Io già t’amai et Se del fiume. Elles avaient isolé une partie instrumentale, dont parfois une doublure du chant. Le registre de la seconde passe conserve les anciens et nouveaux indices, et la concordance des attaques de syllabes a été revue avec les parties notées. Ne pas réutiliser les anciennes copies de ces six `vocal.mid`.

Deux lacunes précises demeurent : `BBArecit` de Giulio Cesare n’a pas de bloc MIDI associé dans la source; `CHBcesare` conserve le chœur dans `score.mid`, mais `vocal.mid` isole seulement Cesare. Les personnages partageant une même portée de récitatif ne sont pas artificiellement séparés.

## Poursuite de l’acquisition

L’objectif reste une collection de milliers de passages, avec davantage d’époques, de langues et de compositeurs. La collection actuelle est encore très baroque. Pour les prochains lots :

1. Acquérir ensemble MIDI, paroles et partition symbolique quand elle est disponible, en enregistrant édition, contributeur, URL, licence et empreinte.
2. Identifier la voix par la partie notée et ses paroles; ne jamais conclure à partir du registre aigu, du timbre MIDI ou de l’ordre supposé des pistes.
3. Conserver les silences, tempos et mesures des sources dans les extractions. Distinguer paroles disponibles, événements horodatés et alignement indépendamment validé.
4. Regrouper les éditions, transpositions et arrangements sous une identité musicale revue; ne pas compter les fichiers instrumentaux comme passages chantés.
5. Élargir au répertoire classique et romantique, puis relire les cas ambigus avec les partitions et à l’écoute.

L’exporteur [tools/export_embedded_lyrics.py](tools/export_embedded_lyrics.py) conserve les paroles MIDI existantes; il ne les invente pas et ne constitue pas un analyseur musical. Dépendance : `mido==1.3.3`. Son mode CLI exporte les horodatages sans présumer une correspondance avec une voix : `python corpus/opera/tools/export_embedded_lyrics.py score.mid repertoire_de_sortie`.

Les tâches restent dans le [TODO unique](../../docs/todo-university-coverage.md). Ce corpus n’atteste aucune compétence universitaire nouvelle et n’active ni moteur d’analyse ou de composition, ni tests ou CI. Chaque fichier conserve la licence de son édition; aucune licence globale ne remplace ces licences individuelles.
