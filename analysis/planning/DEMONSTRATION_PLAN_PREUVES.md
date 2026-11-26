# Démonstration P4 — planifier des preuves, sans inventer une analyse

**25 novembre 2026.** Ce dossier documente le
[prototype de planificateur](../anamu_analysis/proof_planner.py), les deux
[contrats de cas 6/4](examples/verticale-64.case.json) et
[percussion](examples/percussion-physical.case.json), et leur rapport au
[contrat P0](../architecture/CONTRATS_PREUVES_ET_RAISONNEMENT.md).

## 1. Ce que le prototype fait réellement

À partir d'une question, de tâches et de **routes ET/OU** (chaque route
exige tous ses éléments), il déclare pour chaque route :

- « prête, entrées vérifiées » si toutes les exigences ont un statut vérifié ;
- « prête sous hypothèses déclarées » si les exigences sont toutes disponibles,
  mais qu'au moins l'une est simplement déclarée ;
- « bloquée » si une exigence manque ou n'est que candidate non vérifiée.

Il conserve, par tâche, les exigences satisfaites, les hypothèses, les
données manquantes, les conclusions **seulement envisageables** et ce qui
ne pourra pas être établi par cette voie. Un même terme déclaré dans deux
supports ne devient pas deux observations indépendantes.

**Le planificateur n'exécute aucune opération musicale.** Un état « prêt »
n'est ni un diagnostic, ni un résultat d'écoute, ni une validation de
source universitaire. Les « profils » de ces fichiers sont des
**entrées fictives déclarées**, construites à partir de fiches de cours ;
aucune œuvre enregistrée n'a été analysée dans cette démonstration.

## 2. Parcours constatés par exécution manuelle de la commande

Depuis le dossier analysis/ :

~~~sh
python -m anamu_analysis.proof_planner planning/examples/verticale-64.case.json --profile classes_only
python -m anamu_analysis.proof_planner planning/examples/verticale-64.case.json --profile tonal_annotated
python -m anamu_analysis.proof_planner planning/examples/percussion-physical.case.json --profile midi_only
python -m anamu_analysis.proof_planner planning/examples/percussion-physical.case.json --profile layout_annotated
~~~

| Profil illustratif | Tâches prêtes sous hypothèses | Tâches bloquées | Observation importante |
| --- | ---: | ---: | --- |
| Sixte-et-quarte, classes de hauteurs seules | 1 | 4 | Impossible de classer la fonction, la phrase ou la perception |
| Sixte-et-quarte, basse/voix/phrase annotées | 4 | 1 | La question perceptive reste bloquée faute d'écoute |
| Percussion, événements GM seuls | 1 | 2 | Ni le geste physique ni le déclin acoustique ne sont prouvés |
| Percussion, implantation/efforts déclarés | 2 | 1 | La résonance réelle reste bloquée sans audio |

Ces décomptes sont ceux des scénarios construits et du CLI, **pas des
performances de reconnaissance musicale**. Aucune suite de tests
unitaires, validateur ou workflow n'a été ajoutée ou lancée.

## 3. Pourquoi ces deux cas sont discriminants

**Figure 6/4** — La fiche
[CM-211](../../docs/courses/berklee/CM-211.md) juxtapose trois fonctions.
La même figure d'intervalles ne permet pas d'imposer une fonction. Il
faut au moins situer la basse, les mouvements de voix et la continuation.
Le cas montre qu'une connaissance peut être disponible tandis que les
données nécessaires pour l'appliquer à un passage sont absentes.

**Percussion** — La fiche
[CM-343](../../docs/courses/berklee/CM-343.md) distingue Note Off,
choke, implantation, interprète et fin acoustique de la résonance.
Le cas montre qu'un MIDI peut rendre pertinente une tâche
d'inventaire des événements tout en laissant la jouabilité et le son
réel explicitement **bloqués**. Un concept acoustique n'est donc pas
subordonné artificiellement à une analyse tonale.

## 4. Les décisions encore nécessaires

- Relier les termes des routes de preuve à des **types d'évidence
  versionnés**, pas à des chaînes libres rédigées pour un seul exemple.
- Vérifier automatiquement la provenance et les conditions de **portée**
  avant qu'une entrée soit acceptée comme « vérifiée ».
- Dépendances entre tâches, ordonnancement, détection des nouvelles preuves
  et reprises bornées ; la v0 ne fait que diagnostiquer des routes.
- Sorties réelles d'opérations, observations localisées et assertions
  concurrentes ; le prototype n'en produit aucune.
- Rejouer huit familles, dont histoire, electroacoustique, réduction,
  ethnomusicologie et musique de jeu, sans dépendance MIDI imposée.
- Faire évaluer les futures **conclusions musicales**, et non seulement
  les statuts informatiques des routes de preuve.

## 5. Frontière de confiance

Les fichiers de cours restent la vérité de leur contenu, avec les
attributions et limites propres à chaque section. Les huit familles de
calibration sont décrites par le contrat P0. Les 20 assertions candidates
du [premier lot P2b](../knowledge/mentions/calibration-2026-11.json)
sont à revoir. Aucune conclusion, ni même un « niveau de confiance »
sur une œuvre, ne découle automatiquement de ces propositions.
