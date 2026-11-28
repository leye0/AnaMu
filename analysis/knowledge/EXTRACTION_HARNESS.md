# Harnais d'extraction P2b

Ce module distingue l'inventaire (7 323 unités à l'édition initiale),
la lecture de passages, les assertions candidates et la clôture explicite
d'une passe d'extraction. Il ne calcule pas un pourcentage de connaissance
musicale comprise : le dénominateur des assertions reste inconnu.

Depuis analysis/ :

```sh
python -m anamu_analysis.extraction status
python -m anamu_analysis.extraction queue --kind course_markdown --limit 20
python -m anamu_analysis.extraction queue --source docs/courses/mcgill/MUTH-538.md
python -m anamu_analysis.extraction packet material:0002131
```

Le statut est dérivé du catalogue et des lots, sans compteur maintenu à la
main. Le packet relit les octets du document et le passage et refuse les
empreintes divergentes. Les anciens lots sans source_span sont conservés,
mais ne clôturent aucune passe. Les nouvelles extractions conservent le
source_span complet et un passage_reviews par unité consultée :

- partial_extraction : assertions extraites, questions restantes explicites ;
- no_analytic_assertion_in_passage : examen effectué, raison explicite ;
- extraction_complete_for_passage : passe déclarée complète sur cette version.

Une clôture ne vaut ni validation musicologique, ni implémentation. Un
changement de source ou de révision invalide le statut courant. Des
dispositions simultanées incompatibles demandent une réconciliation.
La file est répartie entre documents; elle est filtrable sans présumer
la valeur musicale à partir du titre.

Le vocabulaire des exigences de preuve est distingué du catalogue
d'assertions. Les labels qui n'ont pas de définition dans evidence-facts.json
sont listés comme dette, sans assimilation automatique à un fait existant.

## Publication par connecteur

Le script tools/connector_extraction_batch.js reçoit tools, text, branch,
batchSpec. Il ne lit pas des assertions à partir d'un titre : le lecteur
fournit explicitement l'unité, le SHA-256 du passage consulté, la portée,
l'attribution, le sens proposé, les assertions, leurs conditions et leurs
preuves manquantes. Il relit la source et le chunk à un seul commit, refuse
les divergences et publie le lot et ses index en un seul commit atomique.
Un ID de lot déjà publié est refusé. Les nouveaux IDs de mention et
d'assertion sont namespacés par lot, les identités historiques sont conservées.

Ce pont est réservé à l'environnement du connecteur. La commande Python est
l'interface maintenable sur un checkout complet. Le code des sources n'est
jamais exécuté.
