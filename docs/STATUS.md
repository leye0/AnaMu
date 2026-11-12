# AnaMu — état opérationnel de référence (11 novembre 2026)

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
