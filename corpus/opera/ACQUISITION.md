# Acquisition et reprise — 19 novembre 2026

## Bilan des deux passes

| Mesure | Premier lot | Après extension |
|---|---:|---:|
| MIDI de partition appariés aux paroles | 106 | 439 |
| Opéras représentés | 10 | 30 |
| Compositeurs représentés | 6 | 11 |
| Éditions sources | 19 | 46 |
| MIDI avec horodatages de paroles exportés | 0 | 437 |
| Événements syllabiques exportés | 0 | 99 233 |
| Alignements indépendamment validés | 0 | 0 |

Le zéro initial désigne l’absence d’export, pas l’absence de paroles MIDI : la seconde passe a constaté que 105 des 106 premiers fichiers contenaient déjà des événements de paroles.

Les six éditions françaises apportent 312 entrées; les 21 autres proviennent d’airs et d’arrangements. Les sections instrumentales sans paroles ne sont pas ajoutées comme entrées chantées. Deux groupes de copies instrumentales strictement identiques de Phaéton sont notés dans le registre; ces sections sont déjà exclues pour absence de paroles. Les archives originales ne sont pas modifiées.

## Données obtenues

Les horodatages sont lus dans les messages MIDI `lyrics`, en préférant le décodage UTF-8 des éditions LilyPond, puis Latin-1 pour les fichiers anciens qui le nécessitent. Les ticks absolus et la résolution d’origine sont conservés. La présence d’une attaque au même tick dans la piste retenue est consignée; elle ne valide pas à elle seule l’affectation musicale. Les extraits français emploient des pistes de paroles suivant leurs voix dans ces fichiers précis; les anciennes éditions peuvent stocker toutes les paroles à la fin ou avant les notes. **Ne pas généraliser l’adjacence à tous les MIDI.**

Six erreurs de sélection du premier lot sont corrigées et tracées dans [le registre](acquisition-2026-11-19-expansion.json), avec anciens et nouveaux indices. L’examen des parties vocales et des attaques de syllabes permet d’écarter les anciennes basses ou doublures instrumentales. Les nouveaux MIDI vocaux de la seconde passe incluent leurs pistes de paroles sources.

## Limites conservées

Aucune écoute humaine ni comparaison exhaustive des notes avec une gravure indépendante n’a été réalisée. Les syllabes et les incipits du catalogue restent ceux des fichiers, avec les éventuelles coquilles, arrangements ou reprises de leurs éditions. Une partie de chœur est encore à isoler dans CHBcesare. L’absence de MIDI pour BBArecit n’est pas comblée artificiellement. Le dédoublonnage SHA-256 élimine les copies de fichiers, mais n’établit pas l’unicité musicale entre arrangements et transpositions.

## Prochaine piste documentée

Le dépôt PDMX et sa notice Zenodo v9 ont été examinés comme piste d’élargissement romantique. Le catalogue signale des opéras de Verdi, Puccini, Donizetti, Rossini, Bizet, Gounod et Wagner. L’examen de MIDI candidats montre que les paroles présentes dans les métadonnées de la partition ne sont pas nécessairement exportées dans le MIDI : ces candidats ne sont pas comptés ici sans les paroles réellement acquises. Pour une future collecte, employer les fichiers sans conflit de licence signalé et récupérer les partitions ou les données de paroles correspondantes. Sources : https://github.com/pnlong/PDMX et https://zenodo.org/records/15571083 .
