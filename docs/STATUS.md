# AnaMu — état opérationnel de référence (11 novembre 2026)

**BILAN CANONIQUE — 12 novembre 2026 :** [registre des 386 entrées](data/course-algorithmic-assessments.json) : **101 cours avec MIDI pédagogique**, **77 évalués sans MIDI approprié**, **200 à traiter**, **8 familles de choix**. Lot en cours : 11 nouvelles fiches, 2 MIDI nouveaux (maquette orchestrale expressive et voix chorales), 9 analyses sans MIDI. **6 flags `non_algorithmique=true`** sur la matière prouvée, distincts des cours sans MIDI. Aucune couverture complète de syllabus présumée. Les comptes historiques plus bas ne reflètent pas ce lot.

**Mise à jour de l'étape cours → analyse/composition :** [index canonique](data/course-algorithmic-assessments.json) : **30 cours à premier apprentissage analysé et illustré par 30 fichiers MIDI originaux, 6 cours évalués sans MIDI parce qu'inadéquat, 342 cours encore à traiter, 8 codes de choix**. Deux cours sont provisoirement marqués `non_algorithmique=true` au sens musical (médiation de concert MUS4101, métier de musicien MUPD235). L'exemple de gravure CM342 requiert MusicXML/PDF; la spectromorphologie requiert audio. **Le gabarit en vigueur** est [COURSE_ANALYSIS_TEMPLATE.md](COURSE_ANALYSIS_TEMPLATE.md); le dossier de chaque cours contient les fichiers MIDI originaux et sa fiche existante reçoit les procédures. **Pas de claims de 386 cours entièrement analysés** : les 30 restent une première passe sur apprentissage(s) précis, avec des objectifs supplémentaires à analyser. Les 263/115/8 et les 93/22 blocages de syllabus demeurent séparés et inchangés.

## Prochaine activité autorisée — par cours, analyse et création (11 novembre 2026)

**Demande utilisateur explicite :** [gabarit d'évaluation de chaque cours](COURSE_ANALYSIS_TEMPLATE.md), à écrire dans les fiches `courses/` existantes, **sans nouveau tas de rapports de recherche**. Chaque apprentissage scolaire prouvé doit expliquer comment le détecter dans une musique existante (MIDI, audio et/ou contexte, avec limites), comment l'exploiter dans une composition, et inclure un **MIDI original réel lorsqu'il est démontrable**. Flaguer `non_algorithmique` uniquement pour les cours dont les compétences attestées ne se traduisent pas en analyse/création musicale algorithmique; laisser `null` si l'information manque. Pour audio spectral, clinique, perception d'un public, ne pas fabriquer un MIDI qui prétend simuler la preuve. Les travaux de chapitre général sur 44 mécanismes sont **des références secondaires, non la priorité actuelle**. Aucun développement d'analyseur, CI ou test n'est autorisé; des MIDI pédagogiques ponctuels sont autorisés.

**[Index des 386 entrées](data/course-algorithmic-assessments.json)** : **19 analyses de premiers apprentissages avec 19 MIDI originaux**, **5 évaluations de limites/absence d'exemple MIDI**, **354 cours à traiter**, **8 placeholders non évaluables comme cours fixes**. Les 19 fiches ne signifient pas la couverture intégrale de tous leurs apprentissages. **2 cours possèdent provisoirement `non_algorithmique=true`** sur la matière attestée (MUS 4101, MUPD 235); les autres verdicts doivent respecter le niveau de source. Le périmètre universitaire reste 263 utilisables / 115 partiels / 8 familles. Priorité : travailler les **354 cours restants par lot**, puis approfondir les premiers cas avec plusieurs apprentissages; ne pas rouvrir les 22 syllabus bloqués sans source nouvelle.

**Progrès 1B, second lot du 11 novembre 2026 :** [30 nouveaux mécanismes avec source, fonction, exemple et limites](subject-research/2026-11-11-batch-02-thirty-mechanisms-counterpoint-orchestration-jazz-rhythm.md), [index exploitable de 30 objets](data/subject-research-batch-02-30-mechanisms-2026-11-11.json). **44 sujets/mécanismes documentés au total** (14 premier lot + 30 deuxième), provenant de **15 chapitres externes distincts dans le lot 2**. Domaines : 8 contrepoint, 5 orchestration, 9 jazz, 6 rythme, 2 harmonie chromatique. Ce bilan de 1B est INDEPENDANT des 386 entrées universitaires; aucune matière universitaire spécifique n'a été inventée ni promue. **22 blocages, 93 recherches closes et zéro syllabus en recherche active demeurent inchangés.**

**Ce document est la source de vérité COURANTE pour décider de la prochaine action. Les anciens TODO et comptes datés conservés dans les notes sont historiques, non des instructions de recherche actives.** En cas de chiffres contradictoires, relire [le registre par cours](data/course-material-progress.json), puis ce bilan. Ne pas recopier des états périmés comme 87/28 ou 93/22 actifs dans de nouvelles consignes.

## Périmètre académique et connaissances (NE PAS GONFLER)

| Mesure | Total actuel | Signification |
|---|---:|---|
| Entrées du registre musical | 386 | 378 codes de cours + 8 placeholders de choix |
| Cartes thématiques utilisables en première passe | **263** | Des sujets musicaux au moins raisonnablement délimités par des sources; pas de syllabus complet garanti |
| Cartes thématiques partielles | **115** | Manque de détail authentique par code, conservé sans promotion |
| Choix de programme non identifiés individuellement | **8** | Familles de codes, pas 8 cours dont le syllabus manquerait |

## Effort de recherche des 115 fiches partielles (INDÉPENDANT de la couverture)

| Type de suivi | Nombre | Action |
|---|---:|---|
| `public_research.state=completed_best_effort` | **93** | Ne pas réexaminer les mêmes sources; rouvrir sur preuve nouvelle |
| `public_research.state=blocked_external_evidence` | **22** | Bloqué hors des sources publiques; savoir manquant consigné par code |
| Recherche de syllabus restant active sans nouvelle preuve | **0** | **STOP aux recherches cycliques** |
| `unresolved_pool`, `public_research.state=program_choice_dependent` | **8** | Famille d'options; étudier les vrais codes candidats, ne pas inventer l'affectation des crédits |

[Blocages précis des 22, familles et condition de réouverture](phase1a-public-evidence-stop-2026-11-11.md). L'inconnu reste inconnu : **la phase 1A est arrêtée en meilleur effort pour la collecte publique, PAS déclarée complète en matière pédagogique**. Une preuve de section authentique peut rouvrir un dossier.

## Phase de travail courante — documentation par sujet (phase 1B)

**L'activité productive immédiate est de documenter en masse les sujets musicaux attestés**, à partir des 263 cartes exploitables et de la part déjà prouvée des 115 cartes partielles; approfondir avec des traités, chapitres et ouvrages musicaux à provenance claire. Conserver une distinction stricte :

- Source **du cours** : atteste qu'un sujet est réellement enseigné dans ce cours.
- Source **du sujet** : explique un mécanisme musical, mais ne prouve pas que tel professeur l'enseigne.
- Source **de formation/section voisine** : comparateur seulement, sans transfert de syllabus.

**Premier résultat 1B déjà commité :** [14 mécanismes explicites depuis 10 chapitres/pages d'Open Music Theory](subject-research/2026-11-11-first-14-music-theory-mechanisms-primary-educational-sources.md) : deux contrepoints, fonction harmonique, modulation, sentence, période, modes, pentatonique, tons entiers, octatonique, classes d'ensembles, dodécaphonisme, syncope et groupement 3+3+2. **Les cours ne sont pas promus** par des sources externes.

**Prochain travail autonome :** recueillir 10 à 30 mécanismes/sujets par lot, vérifier les pages réelles, expliquer la fonction musicale et les limites, donner les sources, suivre le raccordement au corpus de cours **comme contexte, non comme preuve d'enseignement**. Ne pas rebalayer les 22 syllabus sans pièce nouvelle. Les véritables contenus de cours futurs peuvent enrichir la carte sans rebloquer 1B.

## Verrous toujours en vigueur

La réconciliation définitive des concepts (phase 2), tout moteur d'analyse MIDI, les expérimentations et la génération/composition restent **verrouillés** jusqu'à autorisation/critères dédiés. Aucun test ni CI, aucun développement algorithmique dans la collecte documentaire et la phase 1B.
