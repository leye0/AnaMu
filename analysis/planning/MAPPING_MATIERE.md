# Référentiel de matière et mapping analytique

**Précision du plan directeur · 22 novembre 2026.**

Léon propose de structurer d'abord la matière que nous possédons, pour l'identifier, la décrire et la maintenir facilement, puis de construire un autre mapping entre cette matière et l'organisation analytique. Cette couche devient un préalable explicite à l'extraction à grande échelle.

## 1. Deux mappings distincts, reliés par une identité stable

| Ensemble | Question à laquelle il répond | Responsabilité |
|---|---|---|
| Référentiel des unités de matière | De quoi parle exactement ce contenu ? | Identifier, décrire, délimiter, sourcer et versionner chaque unité |
| Mapping cours–matière | Où cette unité figure-t-elle et sous quelle attribution ? | Organisation pédagogique, ordre de présentation, sources et exemples locaux |
| Mapping matière–connaissance analytique | À quels concepts et relations cette matière contribue-t-elle ? | Liens explicites vers le graphe, rôle, couverture partielle, contexte et justification |

Les deux mappings sont le **mapping de ce que nous avons** et le **mapping de ce que ce contenu apporte à l'analyse**. Le référentiel d'identités et de descriptions est leur point de jonction.

Le chemin de navigation est : **cours et documents → unités de matière → concepts et assertions → relations, opérations et parcours d'analyse**. On doit pouvoir le parcourir en sens inverse pour savoir quels cours et contenus maintenir lorsqu'une définition ou un mécanisme analytique change.

Une unité de matière ne doit pas être forcée à correspondre à un concept unique. Une leçon sur les sixtes-et-quartes peut contribuer à la sonorité, à la basse, à la conduite des voix et à la fonction harmonique. Un concept commun peut être documenté par plusieurs unités de plusieurs cours, avec des limites différentes.

## 2. Ce qu'est une unité de matière

C'est un **contenu pédagogique ou documentaire cohérent, décrit et délimité**, sur lequel on peut travailler sans réidentifier tout le cours. Elle peut correspondre à une section, plusieurs paragraphes complémentaires, une étude comparative ou une partie délimitée d'une leçon. Les lignes et les titres aident à la retrouver mais ne constituent pas son identité.

Une unité doit pouvoir dire :

- quel sujet précis est traité et quelle question il permet d'aborder ;
- ce qui est expliqué, comparé, exercé ou seulement nommé ;
- les aspects effectivement couverts et ceux qui ne le sont pas ;
- son contexte et son niveau de détail, lorsqu'ils sont connus ;
- les sources de l'enseignement et celles de l'explication complémentaire ;
- les exemples et contre-exemples associés ;
- les contenus qui la composent, s'il existe des sous-unités utiles ;
- les informations manquantes et les modifications à revoir.

**Exemple de titre précis :** « Sixtes-et-quartes : distinguer fonction cadentielle, passage et pédale ». La description donne les critères et les limites du contenu. Le titre « Harmonie 1 » reste un regroupement pédagogique trop large pour ce niveau de maintenance.

La granularité n'est pas « une notion par ligne » : on conserve l'unité de l'explication et l'on crée des sous-unités si un aspect possède sa propre description, ses preuves ou ses besoins de mise à jour. Un bloc nommé mais non documenté est enregistré comme matière à préciser, sans lui inventer une définition.

### Unité locale, réutilisation et matière commune

Deux sections proches restent d'abord deux unités avec leurs attributions. On ne les fusionne pas parce qu'elles emploient le même mot. Lorsqu'un même bloc est réellement réutilisé, une unité peut avoir plusieurs rattachements de cours. Des adaptations stylistiques ou des formulations indépendantes peuvent rester des unités distinctes reliées au même concept.

Une synthèse transversale possède son propre ID ; elle référence ses unités d'appui sans devenir rétroactivement leur texte officiel. Les exemples MIDI et les rendus ont des liens vers la matière, mais leur présence ne certifie pas sa couverture complète.

## 3. Champs et répartition des responsabilités

| Objet | Champs de travail proposés | Règle de maintenance |
|---|---|---|
| `MaterialUnit` | `id`, `revision`, `title`, `description`, `covers`, `does_not_cover`, `content_state`, `editorial_review`, `source_bindings`, `examples`, `child_ids` | Décrire le contenu, sans y encoder son rang dans le futur moteur |
| `CourseMaterialBinding` | ID, `course_id`, `material_id`, groupe, ordre local, attribution, contexte pédagogique, statut | Un changement d'ordre du cours ne modifie pas l'identité de la matière |
| `MaterialKnowledgeBinding` | ID, matière et révision, cible et version, nature du lien, aspects couverts, contexte, justification, état de revue | Un lien peut être partiel, proposé, confirmé, à revoir ou déprécié |
| `KnowledgePlacement` | Concept/assertion, types de relations, échelles, conditions, prérequis et rôle analytique | L'organisation du raisonnement reste dans le graphe analytique |

Les champs de description sont maintenus pour les humains et pour l'extraction ultérieure. Les champs calculés — empreintes, résolution des emplacements, index inverses, détection des changements — restent distingués des descriptions et décisions revues.

**Ne pas copier toutes les hiérarchies dans chaque unité.** Le mapping matière–connaissance pointe vers les concepts et assertions ; leurs placements analytiques sont ensuite consultés dans le graphe. Si l'on change une relation entre cadence et phrase, on ne doit pas corriger cette relation à la main dans vingt fiches de matière.

Les relations `teaches_definition`, `illustrates`, `contrasts`, `documents_context`, `provides_method` sont des propositions de vocabulaire pour les liens de contribution. Elles ne signifient ni équivalence conceptuelle ni compétence acquise. Chaque lien conserve les aspects couverts et ceux qu'il ne démontre pas.

L'ordre pédagogique local est distinct de l'ordre d'analyse : `presentation_order: 3` veut dire « troisième dans ce regroupement », pas « appliquer ce savoir en troisième dans toute œuvre ».

## 4. JSON lisible et organisation maintenable

Les formats sont une proposition, pas une migration déjà exécutée :

```text
analysis/knowledge/materials/                 unités de matière maintenues
analysis/knowledge/course-material-maps/      rattachements et organisation par cours
analysis/knowledge/material-knowledge-maps/   contributions au graphe analytique
analysis/knowledge/material-index.json       index dérivé et points d'entrée
```

Ce bloc liste des chemins proposés ; il n'impose pas une arborescence musicale exclusive. Des fichiers par cours ou par groupe éditorial sont préférables à un énorme JSON monolithique. Les liens se font par ID, indépendamment du fichier qui contient l'objet. Une vue par établissement, cours, sujet ou concept peut être générée depuis les mêmes données.

L'[exemple JSON adjacent](examples/mapping-matiere.example.json) rend ce contrat concret : deux unités de matière, deux rattachements de cours et des contributions candidates. Il documente la différence entre une étude harmonique AnaMu fondée sur des comparateurs et un domaine historique annoncé au catalogue. **C'est un exemple de conception limité, non un inventaire exhaustif ni un mapping chargé par le moteur.**

### Identité et version

- Un ID est opaque et persistant, par exemple `material:000001`. Le titre, le nom de fichier, le code de cours et la ligne ne le déterminent pas. Les IDs d'exemple ne constituent pas une réservation d'IDs de production.
- Un renommage, un déplacement ou une correction de forme conserve l'ID. La révision de contenu et celle des descriptions restent traçables.
- Une scission crée de nouveaux IDs avec `split_from` ; une fusion garde les redirections `replaced_by`. Les anciens liens restent explicables.
- Une suppression produit un état déprécié avec motif, sans recycler l'ID.
- Une révision matérielle n'invalide pas tout par défaut : on distingue déplacement, mise en forme, exemple ajouté et changement de sens. Un changement sémantique demande une revue des contributions concernées.

### Emplacements et changements de source

Chaque rattachement source conserve le document, son empreinte, la section ou le pointeur JSON, les limites du passage et son empreinte propre. Ces empreintes contrôlent une version ; elles ne remplacent pas les IDs.

Si des lignes sont insérées avant un passage dont le contenu est inchangé, le système peut proposer son nouvel emplacement. Si le passage est modifié, ambigu ou absent, son lien est marqué à résoudre. On ne choisit pas silencieusement une autre section au titre proche. Un changement ailleurs dans le document peut rendre son empreinte globale différente sans changer la matière considérée ; le suivi distingue ces cas.

Le rattachement analytique conserve `reviewed_material_revision`. La mise à jour d'une matière permet ainsi de lister ses concepts et assertions liés, les opérations concernées puis les analyses qui en dépendent. Les anciens rapports restent rattachés à leur ancienne édition de connaissance ; ils ne sont pas réécrits comme s'ils avaient utilisé la nouvelle matière.

## 5. Une seule source de vérité pour le contenu

**Dans la phase actuelle, les fiches Markdown restent l'autorité du texte de cours.** Les JSON sont l'autorité des identités, descriptions revues et rattachements de ce nouveau référentiel. Ils ne doivent pas contenir une seconde copie éditable du corps complet des fiches.

Pour modifier une explication, on modifie sa source ; pour améliorer son identification, son résumé ou son rattachement, on modifie le référentiel. Les descriptions sont des résumés éditoriaux reliés aux sources et doivent être revues si leur matière change. Une régénération doit préserver les IDs et les décisions humaines, et présenter un changement au lieu de les écraser.

À terme, on pourra choisir des contenus modulaires structurés comme source canonique et générer les fiches ainsi que le site. Cela exige une migration dédiée avec conservation du contenu et des attributions. Le présent mapping prépare cette possibilité sans instaurer deux versions concurrentes du cours.

**Parcours de modification proposé :**

1. Retrouver la matière par ID, cours, titre ou concept lié.
2. Consulter description, périmètre, texte source et dépendants.
3. Modifier la bonne source ou les métadonnées éditoriales.
4. Actualiser le rattachement et qualifier le changement ; conserver l'historique.
5. Revoir seulement les contributions et dépendants concernés ; afficher les autres comme inchangés.
6. Publier une nouvelle édition du référentiel, avec ce qui a été revu et ce qui reste en attente.

Les vérifications futures porteront sur les identités uniques, références résolues, cycles de regroupement éditorial, attributions, révisions et absences de liens orphelins. Elles ne constituent pas des preuves de justesse musicale. Aucun validateur ou test n'est ajouté par cette précision de conception.

## 6. Place dans le plan et prochain travail

Le mapping documentaire est une **première couche de structuration**, avant la réconciliation globale des concepts. On peut le renseigner progressivement sur tout le corpus et en tirer un tableau des matières navigable, même avant que chaque contribution analytique soit établie.

- **P0** : préciser le contrat de matière et les deux mappings avec les autres objets du plan.
- **P1** : figer les sources et les identités des documents.
- **P2a** : identifier, décrire et délimiter toutes les unités de matière ; créer leurs rattachements aux cours et aux documents transversaux.
- **P2b** : extraire les mentions et assertions depuis ces unités, tout en qualifiant les contenus qui n'ont pas encore de matière résolue.
- **P3** : établir les contributions matière–concepts/assertions puis leur place dans le raisonnement, avec revue et limites explicites.

Le suivi doit montrer, séparément, couverture des sources, matières identifiées, descriptions revues, extraction détaillée et contributions analytiques. Un cours peut avoir une table de matières bien structurée sans que ses concepts soient tous réconciliés ; cette distinction reste visible.

Le critère attendu est simple : **pouvoir retrouver et modifier chaque contenu sans casser son identité, puis expliquer à quels éléments de notre organisation analytique il contribue et pourquoi.**
