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

## Relevé d'exécution et de contrôle

Les cinq opérations, onze tâches, quinze assertions distinctes et vingt
références assertion–tâche ont été contrôlées sur les métadonnées et les
empreintes des assertions. Les preuves demandées sont toutes inscrites
au registre de faits. Les sources de MUTH 538, MHIS 201, MUS 2328 et
MTE 1503 sont ancrées par leurs passages et révisions.

Le [relevé local](../examples/knowledge-routes-electroacoustic-2026-11-28.json)
provient d'une exécution Python réelle de la compilation de
`operation:electroacoustic-continuity` sur les octets identiques du cours
MTE 1503, les quatre assertions entières, deux unités et les projections
nécessaires du registre. Les empreintes des modules Python ont été
comparées aux blobs Git. Quatre assertions ont été vérifiées; deux tâches
sont bloquées, faute de preuves audio et de production. Ce n'est pas une
exécution de l'analyse du signal ni une validation musicologique.
