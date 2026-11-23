# AnaMu — volet indépendant de mise en commun et d'analyse

Ce volet commence la réunion de **tous les cours et connaissances disponibles** pour analyser un morceau. Il lit les sources existantes sans modifier les fiches, leur site, leurs exemples ou les corpus. Son code, ses contrats et ses rapports sont séparés sous `analysis/`.

## Orientation du chantier

Le [plan directeur de cartographie et de raisonnement musical](planning/PLAN_RAISONNEMENT_MUSICAL.md), établi le 22 novembre 2026, organise la suite : extraction de tous les concepts, relations syntagmatiques et paradigmatiques, contextes historiques et culturels, hiérarchies et ordre conditionnel d’application. Il distingue la connaissance à représenter des mécanismes déjà disponibles ci-dessous.

Le [référentiel de matière et ses deux mappings](planning/MAPPING_MATIERE.md) précise la couche préalable : décrire et maintenir les contenus, puis les relier au raisonnement. Un exemple JSON accompagne cette proposition.

Le [registre maintenable des unités de matière](knowledge/MATERIAL_REGISTRY.md) fournit désormais une première implémentation distincte : découverte documentaire, identités persistantes, descriptions révisables et index de navigation. Son contenu de production doit encore être généré et revu ; il ne constitue pas un nouveau rapprochement analytique validé.

## Ce qui existe dans cette première version

| Niveau | Contenu | Portée |
|---|---|---|
| Sources universitaires | 424 documents pour 419 cours : 378 du registre, 41 complémentaires et cinq fiches supplémentaires de cours déjà présents; huit familles de choix explicites | Une fiche indexée n'est pas un cours maîtrisé |
| Connaissances documentaires | Sections des fiches, lots bruts et références transversales; données JSON des registres et manifestes | Texte et métadonnées préservés, sans conversion automatique en règles |
| Concepts communs | 25 premiers concepts avec définition, prérequis, sources localisées, modalités, distinctions et limites | 21 fiches reliées partiellement; la réconciliation complète reste à faire |
| Premier moteur | Six mécanismes génériques sur les événements MIDI | Observations et candidats structurels, pas analyse universitaire complète |
| Rapport | Observations localisées, sources, état de chaque concept et audit de chaque cours | Les connaissances non intégrées ou non implémentées restent visibles |

Le [relevé de couverture](knowledge/coverage.json) et le [tableau de tous les cours](knowledge/course-coverage.csv) sont des instantanés reproductibles. Les cours inconnus, partiels, non algorithmiques et complémentaires restent distingués. Les données structurées conservent notamment les cartes thématiques qui ne figurent pas intégralement dans les fiches.

**Exhaustivité de lecture ≠ exhaustivité d'analyse.** Le moteur ne prétend pas appliquer toutes les connaissances parce qu'il a lu tous les fichiers. Aucun cours n'est encore entièrement intégré sémantiquement. Une connaissance sans mécanisme approprié apparaît comme à intégrer ou à implémenter, sans résultat inventé.

## Architecture

1. **Inventaire sans perte** : partition des documents en fragments, arborescence des sections, lignes et empreintes de sources. Leur concaténation restitue tout le texte. Les métadonnées JSON sont conservées séparément comme sources.
2. **Rapprochement curaté** : les concepts réunissent explicitement plusieurs preuves de cours; leurs prérequis et distinctions forment un graphe vérifié. Une ressemblance de titre ou un mot-clé ne produit pas une équivalence.
3. **Lecture du morceau** : événements MIDI, identifiants de notes, ticks, canaux, commandes et avertissements; aucune voix musicale assignée automatiquement.
4. **Plan d'analyse complet sur les concepts rapprochés** : chacun reçoit un état, y compris les cas bloqués par les entrées, non implémentés ou sans observation correspondante. Les autres fragments documentaires restent une dette d'intégration distincte.
5. **Observations et interprétations** : les propriétés encodées sont séparées des candidats et des fonctions musicales non établies. Les sources et événements permettant de revoir chaque observation sont conservés dans le JSON.

Les instructions opérationnelles de cinq documents de pilotage sont exclues des preuves musicales; leurs chemins et cette exclusion sont déclarés dans l'inventaire. Les fiches, 58 lots bruts, audits, pistes de sources, synthèses et 30 fichiers JSON de `docs/data/` sont pris en entrée. Le corpus d'œuvres n'est pas assimilé aux connaissances : un morceau choisi dans ce corpus est une entrée à analyser.

## Premier contrat d'observation

- Inventaire des attaques, relâchements, canaux et contrôleurs, avec événements sources.
- Ensembles de touches actives et lectures de triades/septièmes candidates. Les symétries augmentées ou diminuées conservent toutes les fondamentales compatibles.
- Récurrences de trois groupes d'attaques par piste/canal, exactes ou sous transposition constante avec le même rythme noté. Ce ne sont pas automatiquement des motifs ou des voix.
- Mètres et tempos explicitement encodés, avec conflits simultanés et absences signalés.
- Distributions de vélocités, distinctes du volume acoustique et de l'accent perçu.
- Contrôleurs de pédale, distincts du geste, de l'amortissement et de la résonance réelle.

Le profil MIDI est **inconnu par défaut**. `--midi-profile gm1` est une hypothèse déclarée par l'appelant; seul ce contrat permet ici d'exclure le canal 10 humain des sonorités de hauteurs. Il ne transforme pas les noms GM en instruments réels. Les durées sont celles des touches : sustain, résonance et commandes All Notes Off ne sont pas simulés. Les événements restent disponibles et les limites sont déclarées.

Le MIDI de type 2 et la division SMPTE sont arrêtés explicitement : une chronologie commune ou une résolution PPQ ne leur est pas inventée. Les notes non appariées, les empilements d'une même touche, les canaux partagés entre pistes et les SysEx sont signalés. Un résultat vide signifie absence d'observation sous le mécanisme limité, pas absence du phénomène musical.

## Exécuter

Depuis le dossier `analysis/`, avec Python 3.11 ou plus récent :

```sh
python -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m anamu_analysis inventory --out .cache/inventory
.venv/bin/python -m anamu_analysis inspect berklee:CM-211
.venv/bin/python -m anamu_analysis analyse ../docs/courses/mcgill/MUTH-251/exemple.mid --midi-profile gm1 --out .cache/harmonie
```

`inventory` produit `knowledge.json.gz`, `coverage.json` et `courses.csv`. `analyse` produit `report.json` et `report.md`; le JSON comporte l'audit des 424 documents de cours et la provenance complète, le Markdown facilite la lecture des résultats.

Les sorties peuvent être écrites sous `analysis/` ou dans un dossier extérieur, pas dans les sources du reste du dépôt. Elles restent ignorées sous `.cache/`. La dépendance de lecture est `mido==1.3.3`; aucun appel à un modèle externe ni service payant n'est effectué.

Les options `--audio`, `--score`, `--lyrics`, `--context` enregistrent la présence et l'empreinte d'autres fichiers. **Leurs adaptateurs ne sont pas implémentés** : fournir ces fichiers ne rend pas leurs connaissances automatiquement analysables.

## Étendre la connaissance et les mécanismes

1. Prendre un apprentissage documenté dans un cours encore peu ou pas relié du tableau de couverture.
2. Délimiter une unité de connaissance : définition, question analytique, entrées nécessaires, faits observables, interprétations concurrentes et conditions d'échec.
3. Vérifier les sources précises et leurs différences de contexte. Réutiliser ou rapprocher un concept existant seulement sur une justification musicale; conserver les variantes stylistiques et les contradictions.
4. Mettre à jour `knowledge/concepts.json`. Une source absente, une section ambiguë, un identifiant dupliqué ou un cycle de prérequis arrête la compilation.
5. Ajouter un mécanisme générique avec un contrat étroit. Relier ses observations aux événements et aux concepts concernés; ne pas attribuer une fonction par un simple nom d'accord.
6. Rejouer un parcours réel, confronter le cas et ses limites aux sources puis actualiser l'inventaire. La validation musicale indépendante reste distincte de l'exécution du logiciel.

Les prochains développements concernent le rapprochement de davantage d'apprentissages, les dépendances entre voix, harmonie et phrase, puis les adaptateurs de partition, d'audio, de paroles et de contexte. La génération de compositions de production reste hors de ce volet.

Les [rapports de démonstration](examples/) montrent la portée réelle de cette première version. Ils ne constituent pas une expertise humaine ou une évaluation indépendante du moteur.
