# Preuves d'œuvre : premier adaptateur de lecture réelle

`proof_inputs` relie le lecteur MIDI existant au planificateur ET/OU. Il
sépare les événements d'attaque encodés, la portée de preuve (empreinte
SHA-256, fenêtre de ticks demi-ouverte, profil déclaré), et les hypothèses
de lecture. Chaque fait fourni conserve les identités d'événements et
les références aux observations. Une route restitue les IDs des preuves
qui la rendent disponible.

Depuis analysis/ :

```sh
python -m anamu_analysis.proof_inputs ../docs/courses/berklee/CM-211/six-quartes-trois-fonctions.mid --case-template planning/examples/verticale-64.case.json
python -m anamu_analysis.proof_inputs ../docs/courses/berklee/CM-343/triangle-gm80-81-memes-frappes.mid --midi-profile gm1 --case-template planning/examples/percussion-physical.case.json
```

Les profils hypothétiques des cas fournis ne sont jamais importés :
seules les questions, routes et références de connaissance sont reprises
sur une portée neuve. Leur pertinence reste à juger. Les faits GM sont
conditionnés au profil explicitement choisi; une lecture de notes ne
confirme aucune jouabilité, résonance, voix, cadence ou fonction.
Les fenêtres d'attaque ne représentent pas l'état sonore continu.

Les adaptateurs audio, partition et contexte restent à développer. Une
route prête signifie que ses entrées sont fournies selon ce contrat,
pas que l'opération a été exécutée ni qu'une interprétation est vraie.

## Exécution réelle du 28 novembre 2026

Le [relevé d'exécution](../examples/proof-inputs-2026-11-28.json) conserve les
empreintes des trois modules Python et des deux MIDI. Le lecteur, l'adaptateur
et le planificateur ont été reconstitués localement avec des blobs Git identiques ;
le helper SHA-256, les champs de tâches des cas et les identifiants du registre
ont été repris pour cette exécution partielle, sans checkout complet.

| Source | Attaques | Route disponible | Questions bloquées |
| --- | ---: | --- | ---: |
| CM-211, trois figures 6/4 | 108 | Inventaire MIDI, entrées vérifiées par le lecteur | 4 |
| CM-343, triangle GM | 32 | Attaques GM sous hypothèse déclarée | 2 |

Le message SysEx de CM-343 n'est pas interprété. Les hypothèses GM restent
explicites. Aucune fonction harmonique, résonance, jouabilité ou appréciation
perceptive n'a été validée. Ce sont deux parcours réels d'exécution, pas une
suite de tests ni un audit intégral du dépôt.
