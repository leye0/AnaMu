# Routes d'analyse issues des assertions

Le registre `knowledge/assertion-routes.json` définit des tâches de
preuve explicites, liées à des assertions candidates extraites, et non à
des mots-clés. Une référence contient l'identité et l'empreinte de
l'assertion, l'identité et la révision de matière. La compilation relit le
chunk et les octets du passage source ; tout changement demande une
nouvelle décision éditoriale. Les routes ET/OU sont choisies par le lecteur
et utilisent le vocabulaire de faits, sans conversion automatique des
labels bruts d'exigence.

Depuis analysis/ :

```sh
python -m anamu_analysis.knowledge_routes list
python -m anamu_analysis.knowledge_routes plan operation:electroacoustic-continuity
python -m anamu_analysis.knowledge_routes plan operation:interactive-symbolic-audio-boundary --evidence <rapport-proof_inputs.json>
```

Une exécution sans paquet de preuves montre seulement les besoins d'un
parcours non associé à une œuvre. Une exécution avec paquet conserve sa
portée exacte; la pertinence de l'opération pour cette œuvre reste à
déterminer. Les provenances de connaissance sont dans le cas compilé,
les preuves d'œuvre dans le plan. Aucune route prête ne signifie que
l'opération a été exécutée.
