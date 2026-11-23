# Registre maintenable des matières (première implémentation)

Ce registre réalise **P1 et un premier passage documentaire de P2a** du
[plan de mapping](../planning/MAPPING_MATIERE.md). Il ne réalise ni l'extraction
exhaustive des assertions de P2b, ni la réconciliation de P3, ni l'analyse
musicologique indépendante.

## Entrées et frontières de vérité

- La source pédagogique est le Markdown original dans **docs/**, en lecture seule.
- Le socle **compile_knowledge** fournit les 424 fiches de cours, les 76
  documents transversaux et les 30 sources structurées JSON de l'instantané
  connu. Ces compteurs concernent **les documents**, pas les matières comprises.
- Chaque fragment Markdown reçoit une unité **candidate**. Les JSON sont
  subdivisés en enregistrements localisables par pointeur JSON, sans prétendre
  qu'un enregistrement est une leçon. Une rubrique vide reste à décrire.
- L'absence d'un syllabus public, les divergences d'attribution et les limites
  de preuve ne sont pas corrigées par la génération.
- Aucun détecteur, moteur de composition, cours, site ou corpus n'est modifié.

Un titre ou un premier extrait peut proposer une description documentaire,
mais **jamais une description éditoriale approuvée**. Les catégories
source_proposal_unreviewed, draft et human_reviewed restent explicites.
Les deux unités dans
[la maquette](../planning/examples/mapping-matiere.example.json) demeurent des
**exemples de conception**, non des fiches déclarées revues dans ce registre.

## Fichiers de sortie

Depuis **analysis/** :

| Fichier | Rôle |
| --- | --- |
| knowledge/materials/catalog.json | Manifeste des fragments de registre, pas copie du cours |
| knowledge/materials/sources/*.json | Un fichier par document source : IDs, descriptions, révisions, références |
| knowledge/course-material-maps/links.json | Rattachements explicitement attribués à leurs cours, distincts du concept |
| knowledge/material-knowledge-maps/links.json | Contributions analytiques éditoriales ; vide au démarrage et non inféré automatiquement |
| knowledge/material-index.json | Vue dérivée : couverture, navigation inverse cours/source/concept, liens périmés |

Le catalogue contient des pointeurs vers les sections et les enregistrements,
des empreintes du document et de l'unité et un résumé de travail. **Il ne
recopie pas le texte intégral** des 424 fiches. Les unités de source peuvent
être retravaillées et subdivisées plus finement lors de la revue P2a ; une
section automatiquement détectée n'est pas une définition universelle du
niveau de granularité.

Ces fichiers de production sont générés à la **première exécution locale**.
Ils ne sont pas préremplis par la présente livraison de code : ne pas annoncer
leur publication ou leur validation avant d'avoir exécuté cette commande sur
les sources complètes et vérifié le résultat.

## Commandes

Depuis **analysis/** avec Python 3.11+ et les dépendances déjà indiquées
dans [le README d'analyse](../README.md) :

~~~sh
python -m anamu_analysis.materials refresh
python -m anamu_analysis.materials search "sixtes et quartes"
python -m anamu_analysis.materials show material:0000001 --source
python -m anamu_analysis.materials describe material:0000001 \
  "Description précise basée sur la section consultée"
python -m anamu_analysis.materials describe material:0000001 \
  "Description effectivement relue et approuvée" --reviewed
python -m anamu_analysis.materials refresh
~~~

L'identifiant ci-dessus n'est qu'un exemple de syntaxe : chercher d'abord
l'ID réellement attribué. **show --source** relit le passage Markdown ou
l'enregistrement JSON dans sa source, pour vérifier ce que la description
affirme. La modification éditoriale n'affecte pas le corps original.

### Actualiser sans détruire le travail humain

1. Les ancrages de source encore présents gardent leur identité, même si des
   lignes précédentes ont bougé. Un changement de contenu incrémente la
   révision et demande une nouvelle revue.
2. Si l'ancrage a changé, un passage identique et **unique** peut recevoir une
   proposition de relocalisation. Une identité encore ancrée ailleurs n'est
   pas réattribuée par cette heuristique. La relocalisation exige une revue.
3. Une ambiguïté ou une disparition n'entraîne **aucune fusion silencieuse** :
   un ID nouveau est créé si nécessaire ; l'ancien reste en
   source_missing_not_deleted.
4. Les descriptions humaines, leur statut et les rattachements éditoriaux sont
   conservés. Les nouvelles propositions de description ne les écrasent pas.
5. Les liens analytiques maintiennent la révision de matière revue ;
   l'index dérivé indique les liens dont cette révision n'est plus actuelle.

Un changement de sens sous le même ancrage est **détecté comme changement
textuel**, mais pas interprété automatiquement. Inversement, une réécriture
à sens égal réclame elle aussi une revue. Cette prudence est intentionnelle.

### À faire après la première exécution

- Contrôler les compteurs de documents et le nombre réel d'unités candidates.
- Inspecter la qualité du découpage sur des fiches de nature contrastée
  (harmonie, contexte historique, timbre, percussion, etc.), puis subdiviser ou
  fusionner **éditorialement**, avec conservation des identités.
- Rédiger et relire progressivement les descriptions selon les sources ;
  distinguer la notice officielle de l'étude comparatrice AnaMu.
- Renseigner les contributions matière–concept/assertion de façon motivée,
  avec état de revue, aspects couverts, contexte et preuve. Le mapping vide
  n'est **pas** une couverture analytique complète.
- Ne commencer le placement syntagmatique, paradigmatique et hiérarchique
  qu'après ces rapprochements traçables.

Aucun test automatisé, workflow ou validation musicologique n'est ajouté
par cette première implémentation. Un parcours réel de génération et une
revue de son résultat sur le dépôt complet restent nécessaires.
