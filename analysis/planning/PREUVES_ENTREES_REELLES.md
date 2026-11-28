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
