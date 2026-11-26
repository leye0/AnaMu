# Démonstration P4 — planifier des preuves, sans inventer une analyse

**25 novembre 2026.** Ce dossier documente le
[prototype de planificateur](../anamu_analysis/proof_planner.py), les deux
[contrats de cas 6/4](examples/verticale-64.case.json) et
[percussion](examples/percussion-physical.case.json), le
[parcours électroacoustique](examples/electroacoustic.case.json) sans MIDI,
et leur rapport au
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
python -m anamu_analysis.proof_planner planning/examples/verticale-64.case.json --profile real_midi_events_only
python -m anamu_analysis.proof_planner planning/examples/percussion-physical.case.json --profile midi_only
python -m anamu_analysis.proof_planner planning/examples/percussion-physical.case.json --profile layout_annotated
python -m anamu_analysis.proof_planner planning/examples/electroacoustic.case.json --profile audio_only
python -m anamu_analysis.proof_planner planning/examples/electroacoustic.case.json --profile audio_and_listening_annotated
python -m anamu_analysis.proof_planner planning/examples/electroacoustic.case.json --profile documents_only

# Comparer ce qu'une nouvelle preuve rend seulement examinable
python -m anamu_analysis.proof_planner planning/examples/verticale-64.case.json --profile classes_only --compare tonal_annotated
python -m anamu_analysis.proof_planner planning/examples/percussion-physical.case.json --profile midi_only --compare layout_annotated
~~~

| Profil illustratif | Tâches prêtes sous hypothèses | Tâches bloquées | Observation importante |
| --- | ---: | ---: | --- |
| Sixte-et-quarte, classes de hauteurs seules | 1 | 4 | Impossible de classer la fonction, la phrase ou la perception |
| Sixte-et-quarte, basse/voix/phrase annotées | 4 | 1 | La question perceptive reste bloquée faute d'écoute |
| Sixte-et-quarte, événements du vrai MIDI CM-211 vérifiés | 0 sous hypothèses, **1 sur données vérifiées** | 4 | Les notes sont disponibles, mais la fonction, la voix et l'audio ne sont pas inférés |
| Percussion, événements GM seuls | 1 | 2 | Ni le geste physique ni le déclin acoustique ne sont prouvés |
| Percussion, implantation/efforts déclarés | 2 | 1 | La résonance réelle reste bloquée sans audio |
| Électroacoustique, audio seulement déclaré | 1 | 3 | Relevé d'audio envisageable; segmentation et contexte restent à étayer |
| Électroacoustique, observations et écoute annotées | 3 | 1 | Segmentation et confrontation possibles sous hypothèses; archives de production manquantes |
| Électroacoustique, archives seulement | 1 | 3 | La branche documentaire avance sans dépendre d'un MIDI ou d'un fichier audio |

Les profils illustratifs restent des scénarios déclarés. La nouvelle
ligne de **MIDI réel** emploie les attaques relevées dans le
[rapport d'observations CM-211](../examples/cm211-six-four-midi-observations.json),
sans ajouter de voix ou de fonction automatiquement.

Ces décomptes sont ceux des profils du CLI, **pas des performances de
reconnaissance musicale**. Aucune suite de tests
unitaires, validateur ou workflow n'a été ajoutée ou lancée.

En comparaison des profils, le CLI constate **trois tâches devenues
examinables sous hypothèses** pour la sixte-et-quarte (basse, fonction,
phrase) et **une** pour la percussion (gestes/implantation). Les
changements de faits sont explicités; la perception acoustique reste
bloquée dans les deux cas. Il s'agit d'une réévaluation du **plan**,
pas d'une révision automatique de conclusions musicales.

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

**Électroacoustique (nouveau cas)** — La source
[MTE-3300](../../docs/courses/udem/MTE-3300.md) décrit une analyse
spectromorphologique fondée sur l'audio et l'écoute. Les profils
illustratifs distinguent l'accès à un fichier audio, des observations
et segmentations annotées, et des documents de production. Une tâche
documentaire peut être prête quand la segmentation audio ne l'est pas ;
**aucune route MIDI n'existe dans ce cas**. Le vocabulaire de preuves
partagé a été étendu à 23 types. Les décomptes du tableau représentent
la disponibilité selon les profils, pas des résultats d'écoute.

## 4. Généralisation des preuves et ordre d'exécution

Les deux cas partagent désormais le
[registre de 23 catégories de faits](../knowledge/evidence-facts.json) :
événements MIDI, continuité des voix, partitions, écoute, contexte,
implantation d'instruments, gestes d'amortissement et autres besoins.
L'orthographe d'une exigence inconnue provoque un arrêt, au lieu de
créer silencieusement une catégorie de preuve.

Le planificateur conserve également un **ordre technique des tâches
candidates**. Une dépendance « observer les événements avant de
départager une fonction » organise les opérations sans devenir une loi
sur le déroulement temporel de l'œuvre. Des opérations indépendantes,
comme l'écoute d'un extrait, n'ont pas besoin d'attendre une mesure
d'accord préalable. Une boucle entre prérequis d'exécution est refusée ;
un aller-retour entre interprétations musicales, lui, demeure possible
dans l'architecture de connaissance.

La sortie distingue maintenant trois concepts :
- disponibilité d'une route selon son profil ;
- ordre de préparation de tâches dépendantes ;
- **exécution réelle absente** des opérations, explicitement signalée.

Le statut « verified » d'un fait est **déclaré par le profil de preuves**.
La CLI exige une provenance écrite et refuse des faits dupliqués, mais
**ne vérifie pas elle-même les sources, les fichiers et leur authenticité**.
Le rapport de lecture MIDI associé à CM-211 a été établi séparément ;
sa référence ne valide pas automatiquement toute interprétation.

## 5. Les décisions encore nécessaires

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
