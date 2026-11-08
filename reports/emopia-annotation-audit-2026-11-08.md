# EMOPIA 2.2 : audit d'une réplication indépendante des votes minoritaires

**Décision : ne pas réaliser de faux test de votes multi-annotateurs sur EMOPIA.**

Archive officielle : [EMOPIA 2.2, Zenodo 5257995](https://zenodo.org/records/5257995),
`EMOPIA_2.2.zip`, 32 117 182 octets, SHA-256
`ec6debc927679c844f9d6084755cc25771d0953836c6ed3cb05340371a94bcc7`.

Inspection par workflow opt-in, sans conserver ni redistribuer le MIDI/audio :

- 1 071 fichiers MIDI ; 389 fichiers de listes d'annotation (`tagging_lists/*.txt`).
- `label.csv` possède **1 078 lignes et 1 078 ID uniques**.
- **Zéro ID** n'a plusieurs lignes, maximum **une ligne par extrait**.
- Le champ `annotator` se répartit entre `A=34`, `B=136`, `C=546`, `D=362` ;
  ces identifiants décrivent les auteurs des annotations, et non quatre votes
  récupérables sur chaque extrait.
- Les classes 4Q sont `Q1=250`, `Q2=265`, `Q3=253`, `Q4=310`.
- Les fichiers de *tagging* contiennent des segments temporels et des scores ;
  leur présence n'établit pas de votes indépendants sur les mêmes extraits.

Le fait qu'un corpus ait été constitué par quatre personnes ne suffit pas à
inférer un consensus à quatre annotateurs. Un entraînement à fraction de votes
`0, 1/4, 2/4, 3/4, 1` serait **inventé** sur ces données.

**Utilisable ensuite :** quatre quadrants valence–activation, avec séparation
obligatoire par chanson originale. Cela pourrait tester le transfert général
des attributs MIDI, mais non le mécanisme d'information porté par les
annotations minoritaires PIAST.

Sources primaires :

- [Zenodo version 2.2 : notes de publication, fichiers et tailles](https://zenodo.org/records/5257995)
- [Hung et al., EMOPIA (ISMIR 2021)](https://arxiv.org/abs/2108.01374)

Résultat de cette étude : **limite de réplicabilité établie**, pas démonstration
de supériorité ou d'infériorité d'un modèle sur EMOPIA.
