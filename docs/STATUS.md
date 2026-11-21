# AnaMu — état opérationnel de référence

État documentaire au **21 novembre 2026**. Ce document présente les capacités et les manques actuels; l'historique des étapes est dans Git et les preuves sont dans les fiches, registres et manifestes.

## Structure et travail courant

- **Cours** : fiches par établissement et code, méthodes d'analyse et d'usage compositionnel, exemples MIDI et supports adaptés.
- **Site** : bibliothèque construite depuis les fiches et les registres, avec lecteurs, comparaisons et partitions. Voir [la publication](../site/README.md).
- **Corpus** : œuvres acquises avec provenance et paroles; [opéra](../corpus/opera/README.md) et [catalogue pop/Billboard](../corpus/pop/README.md) dans `main`.

Poursuivre les apprentissages attestés dans les fiches et les lacunes du [TODO](todo-university-coverage.md). La présence d'un exemple ne clôt pas le cours. Ne pas régénérer les lots existants ni reprendre un audit initial déjà effectué.

## Périmètre académique et connaissances (NE PAS GONFLER)

| Mesure | Total | Portée |
|---|---:|---|
| Entrées du registre musical | 386 | 378 codes de cours et huit familles de choix |
| Premières évaluations de cours identifiables | 378 | Tous les codes ont été examinés une première fois |
| Cours avec un exemple MIDI pédagogique initial | 122 | Apprentissages identifiables, pas totalité des syllabus |
| Évaluations limitées sans MIDI approprié | 256 | Audio, contexte, matière manquante ou autre support requis |
| Cartes thématiques utilisables en première passe | 263 | Descriptions musicales délimitées, pas syllabus complets garantis |
| Cartes thématiques partielles | 115 | Détail authentique insuffisant ou enseignement variable |
| Familles de choix non résolues | 8 | Familles, pas huit cours fixes |

Les [évaluations par cours](data/course-algorithmic-assessments.json) et le [registre de matière](data/course-material-progress.json) suivent des axes distincts. Leurs 9 drapeaux `non_algorithmique=true` concernent les apprentissages attestés; les inconnus restent `null`. Les cours complémentaires hors registre ne gonflent pas les 386 entrées.

## Effort de recherche des 115 fiches partielles (INDÉPENDANT de la couverture)

| État de recherche publique | Nombre | Consigne |
|---|---:|---|
| `completed_best_effort` | 93 | Ne pas reprendre les mêmes sources sans preuve nouvelle |
| `blocked_external_evidence` | 22 | Matière manquante documentée; réouverture sur pièce nouvelle |
| Recherche cyclique active | 0 | Aucun ratissage automatique à recommencer |

La [liste des lacunes](remaining-115-course-evidence-queue-2026-11-11.md) et l'[audit des blocages](phase1a-public-evidence-stop-2026-11-11.md) restent utiles. La collecte publique est arrêtée en meilleur effort, pas déclarée exhaustive en matière pédagogique.

## Harmonie : fonctions et continuations — 18 novembre 2026

Six cours approfondis : CM-211, CM-212, MTE-1221, MUTH-251, HR-211 et HR-212. **Huit études originales**, huit MIDI/MP3 et huit partitions SVG/HTML/MusicXML représentent 724 attaques à quatre voix. Cinq comparaisons personnelles supplémentaires portent le total à **douze comparaisons** et **onze partitions**, percussion comprise.

Les [sources, événements, invariants et limites](data/harmony-context-studies-2026-11-18.json) sont documentés. Les notes et gravures ont été relues; aucune réponse d'auditeur ni maîtrise de tous les apprentissages des cours n'est acquise.

## Partitions de travail et résonance — 18 novembre 2026

**62 rendus de percussion** sont disponibles dans les cours. Ils comprennent les 41 rendus initiaux, 15 réalisations en contexte et six rendus de résonance supplémentaires. Les sources GMD sont attribuées; les banques, gains et mesures PCM sont distingués des preuves perceptives.

Trois partitions modifiables de travail représentent deux batteries de 32 mesures et un conducteur de 16 mesures à trois exécutants. Les articulations et affectations sont des propositions; leur gravure ne certifie pas la jouabilité.

- [Rendus initiaux et parcours d'écoute](data/percussion-audio-2026-11-17.json).
- [Contexte, arrangements et prises humaines](data/percussion-context-2026-11-17.json).
- [Résonance dans deux banques](data/percussion-resonance-2026-11-18.json).
- [Provenance des partitions](data/percussion-scores-2026-11-18.json).

## Reprise percussion — 17 novembre 2026, comparaisons dans chaque cours

Les études sont intégrées à leurs fiches avec questions, repères, exercices, MIDI et limites. Les comparaisons masquent les noms avant la réponse, comprennent des témoins A/A et ne collectent aucune réponse. Une prise humaine de jeu n'est pas un jugement d'auditeur.

Restent les retours datés d'interprètes et d'auditeurs : jouabilité, déplacements, affectations, articulations et perception des contrastes. Les tâches sont dans le TODO; les synthèses musicales se trouvent dans les cours et [knowledge-base.md](knowledge-base.md).

## Corpus parallèle d'opéras

**439 couples MIDI–paroles, 30 opéras, 11 compositeurs, 46 éditions sources.** Les 439 MIDI ont des empreintes distinctes; les variantes et arrangements ne sont pas nécessairement des passages musicaux distincts. **437 exports horodatés** contiennent **99 233 événements syllabiques** issus des sources. Six sélections vocales ont été corrigées.

Le [corpus](../corpus/opera/README.md) conserve les originaux, extractions, paroles, crédits et licences. Restent l'affectation complète du chœur de `CHBcesare`, les comparaisons indépendantes notes–syllabes, les auditions, le regroupement des éditions et l'élargissement du répertoire. `BBArecit` n'est pas artificiellement compté sans MIDI source.

## Corpus pop / Billboard

Le [corpus pop/Billboard](../corpus/pop/README.md) contient le catalogue et la réacquisition du premier lot gratuit; les fichiers acquis ont été remis en paquet privé. **1 331 identités candidates**, dont 1 051 structures à plusieurs canaux, 459 exports de paroles MIDI et 440 titres associés au top 10 dans un miroir du Hot 100, dont 292 au top 5.

La cible de **2 000 chansons distinctes complètes** n'est pas atteinte. Il reste à vérifier le genre pop, les dates originales, les parties chantées et les appariements de paroles. Le catalogue et la réacquisition sont intégrés à `main`; les fichiers pop tiers restent dans le paquet privé. Ce chantier ne modifie pas les compteurs universitaires.

## Prochaine activité autorisée — par cours, analyse et création

Utiliser le [gabarit](COURSE_ANALYSIS_TEMPLATE.md) dans la fiche existante du cours. Pour chaque apprentissage sourcé : procédure d'analyse, usage compositionnel, exemple ou contre-exemple et limites `MIDI_DIRECT`, `MIDI_PROXY`, `AUDIO_REQUIRED`, `CONTEXT_REQUIRED`, `NOT_MUSIC_ALGORITHM` ou `UNKNOWN`. D'autres apprentissages de contrepoint, forme ou orchestration peuvent être approfondis sans refaire les percussions.

Les 44 mécanismes généraux documentés en [deux lots](subject-research/) sont des références complémentaires, pas une nouvelle file à substituer aux cours.

## Verrous toujours en vigueur

Aucun moteur d'analyse ou de composition automatique n'est opérationnel ou autorisé par ces travaux. La réconciliation définitive des concepts et la composition de production restent soumises à décision et aux portes L01–L05 du TODO. Aucun test ni travail sur la CI n'est ouvert par une collecte ou une rédaction pédagogique.
