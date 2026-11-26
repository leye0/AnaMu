# Registre maintenable des matières (première implémentation)

Le [manifeste P1](source-manifest.json) a figé les 530 documents connus
(424 fiches, 76 références, 30 JSON), et ce registre réalise **une calibration
de P2a** du [plan de mapping](../planning/MAPPING_MATIERE.md). Une première
[extraction candidate P2b](mentions/calibration-2026-11.json) et des contributions
P3 ont été amorcées. Ce travail n'achève ni l'extraction exhaustive ni la
réconciliation ni l'évaluation musicologique indépendante.

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

Un **catalogue pilote est publié**, avec **36 fiches représentées**,
**457 unités documentaires candidates**, **23 descriptions** vérifiées sur des
passages précis par l'assistant, et **44 contributions analytiques proposées**
(dont **5 cibles non résolues**). Vingt-huit fiches ont été entièrement
partitionnées en sections documentaires ; les huit fiches de calibration
supplémentaires possèdent encore **une seule section délimitée chacune**.
Les passages restants de ces huit fiches et les autres sources doivent être
générés pendant la reprise complète.

Les 23 descriptions restent des **brouillons éditoriaux**, et aucun lien
n'est confirmé musicologiquement.
Les cinq cibles sans concept canonique sont suivies dans
[les sens candidats P3](candidate-senses.json) : contexte historique,
dramaturgie, spectromorphologie, enquête ethnomusicologique et
interprétations du tango. Ces **propositions** conservent leur portée et
leurs exigences de preuve; aucune n'est automatiquement fusionnée aux
25 concepts existants. Dix mentions sélectionnées ont fourni
20 assertions candidates dans un fichier séparé : elles ne constituent pas
la lecture détaillée de tous les passages des 36 fiches.

La commande **refresh** permet de poursuivre sur toutes les sources et de
conserver les unités, descriptions et liens existants. Son exécution complète
sur le checkout n'a pas encore été effectuée. Ne pas confondre les inventaires
documentaires de **compile_knowledge** et le registre éditorial, encore pilote.

## Commandes

Depuis **analysis/** avec Python 3.11+ et les dépendances déjà indiquées
dans [le README d'analyse](../README.md) :

~~~sh
# Préparer la génération complète sans écrire sur disque
python -m anamu_analysis.materials refresh --dry-run

# Appliquer seulement après examen des nouveaux IDs et des liens périmés
python -m anamu_analysis.materials refresh
python -m anamu_analysis.materials search "sixtes et quartes"
python -m anamu_analysis.materials search --course berklee:CM-211
python -m anamu_analysis.materials search --concept harmony.function
python -m anamu_analysis.materials search --candidate-sense candidate-sense:00003
python -m anamu_analysis.materials search --review assistant_source_checked_draft
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

### Audit et parcours de raisonnement

Le snapshot des sources peut être inspecté puis synchronisé sans modifier
les cours :

~~~sh
python -m anamu_analysis.source_manifest audit
python -m anamu_analysis.source_manifest sync
~~~

Le [contrat P0](../architecture/CONTRATS_PREUVES_ET_RAISONNEMENT.md)
et la [démonstration de routes de preuve](../planning/DEMONSTRATION_PLAN_PREUVES.md)
distinguent une opération **prête** d'une conclusion effectivement
établie. Le module de planification ne crée ni analyse d'œuvre ni règle
musicologique automatiquement.

Le mode **--dry-run** parcourt les documents et les entrées JSON, calcule
le nombre d'IDs nouveaux/réutilisés, les cibles orphelines refusées et
les liens à revoir, **sans écrire de nouveaux fichiers**. Il constitue
la première inspection avant de produire un catalogue volumineux sur un
checkout complet. Le contenu pilote reste sous contrôle Git.

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
