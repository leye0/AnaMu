# Couverture thématique AnaMu — état initial du 10 novembre 2026

**L'inventaire a été balayé une fois : 402 entrées / 402 évaluées. Le travail n'est PAS achevé.** La distinction centrale est **carte initiale présente** vs **contenu suffisamment décrit**. Aucune chasse systématique aux livres, corrigés ou travaux exacts des professeurs n'est requise pendant cette passe.

| Établissement | Codes / entrées | Descriptions thématiques utilisables | Descriptions encore partielles | Catégories à déplier |
|---|---:|---:|---:|---:|
| UdeM | 190 | 79 | 111 | 0 |
| McGill | 58 | 34 | 24 | 0 |
| Berklee Boston | 154 | 96 | 41 | 17 |
| **TOTAL** | **402** | **209** | **176** | **17** |

## Attention : 402 entrées ne signifient pas 402 cours distincts

- **17 codes Berklee** sont des *familles de choix* (`LMSC-xxx`, `PIxx-111`, `ENxx`, etc.). Ils n'ont pas de syllabus unique ; les cours concrets choisis parmi eux restent à déplier. Il y a donc au plus **385 codes propres** dans les 402 entrées actuelles, sans préjuger du nombre de cours qui découleront des choix. Le registre contient également **5 pools de choix distincts** à examiner.
- **200 cartes utilisables** signifient une description initiale assez détaillée des **sujets** pour guider une recherche bibliographique future, et **non** la maîtrise de ces sujets, la récupération d'un vrai syllabus ou la preuve d'exhaustivité.
- **185 cartes partielles** manquent de précision. Beaucoup sont des leçons privées ou ensembles de pratiques à programme variable, des séminaires de section variable ou des notices à peine plus riches qu'un titre. L'enjeu n'est pas d'obtenir chaque devoir : il est d'obtenir suffisamment de **sujets réels** pour la cartographie.
- **Les anciens statuts** `catalog_only` / `partially_documented` / `syllabus_documented` restent indépendants de la couverture thématique 1A et n'ont pas été artificiellement modifiés.

## Lots créés pendant cette reprise

- [UdeM : 88 codes d'ensembles, instruments et pratiques variables](raw-batches/2026-11-10-udem-88-ensembles-instruments.md), toutes cartes encore partielles : un suivi de répertoire plus fin nécessite les informations par famille ou formation.
- [Berklee Boston : 68 cours de matière spécifique](raw-batches/2026-11-10-berklee-68-program-courses.md) : **36 utilisables, 32 partielles**.
- [Berklee : 59 dernières entrées et familles de choix](raw-batches/2026-11-10-berklee-59-final-topics-and-pools.md) : **29 utilisables, 13 partielles, 17 familles à déplier**.

## Suites prioritaires — même phase 1A

1. **Déplier les 17 codes génériques** et les 5 pools du cursus dans des **cours réellement identifiés**, à partir du parcours de crédits 2026F et des choix effectivement ouverts. Chaque nouveau code concret aura sa propre description thématique, s'il est pertinent.
2. **Enrichir les 199 fiches partielles** quand la notice précise trop peu les sujets. Pour les leçons privées et ensembles, chercher **les référentiels par instrument ou par formation**, pas les syllabus individuels de centaines d'étudiants.
3. Vérifier les **différences entre niveaux portant le même intitulé**. Une série 1/2/3 ne démontre pas automatiquement des progressions thématiques distinctes.
4. Une fois les sujets définis de manière suffisamment précise sur le périmètre réel, **phase 1B** : recherche académique par **sujet** (traités, manuels, articles, partitions, contre-exemples), pas reconstitution administrative des cours.

**Verrou actif :** pas de concepts réconciliés en base ni de développement de logiciels, analyseurs, composition, tests ou CI avant décision explicite.

## Exploration des réserves de crédits (10 novembre 2026)

[36 cours Berklee réels, codés et sourcés](raw-batches/2026-11-10-berklee-36-real-open-electives.md) ont été identifiés dans huit familles d'options. **Ils sont distincts des 402 entrées historiques** et n'en ferment aucune automatiquement. Parmi eux : acoustique, psychoacoustique, cognition musicale, économie sociale de la musique, traditions afro-diasporiques, cinéma et arts visuels. Leurs axes sont dans [un registre complémentaire JSON](data/berklee-open-elective-candidates-2026.json). Le travail restant sur les catégories de choix doit désormais partir de codes concrets, pas se limiter aux placeholders.

## Enrichissement spécifique des ensembles UdeM (10 novembre 2026)

[22 codes avec huit sources pédagogiques de formation](raw-batches/2026-11-10-udem-22-ensemble-specialized-topics.md) : interprétation collective, gamelan, cuivres, orchestre, chorale, chambre, percussions et ensemble à vents. Neuf cartes désormais utilisables au niveau du contenu **commun de l'ensemble** ; l'absence de progression distincte des sigles 1/2/3 reste explicitement signalée.
