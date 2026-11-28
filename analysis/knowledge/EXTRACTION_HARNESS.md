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

## Contrat renforcé de lecture et de publication (v2)

Pour une publication nouvelle, le lecteur fournit la révision de matière,
le commit de lecture, l'empreinte du passage et, pour chaque assertion,
un extrait littéral unique du passage. Le pont conserve les bornes en
points de code Unicode et l'empreinte SHA-256 de cet extrait. Il exige
également les conditions d'application et une limite d'inférence explicite.
Les assertions v1 restent conservées sans réécriture de leur provenance.

La revue de passage classe séparément six dimensions : définitions,
méthodes, conditions, exceptions, contre-exemples et attribution.
Chaque dimension est examinée, absente ou ouverte. Une clôture refuse
les dimensions ouvertes et les questions d'extraction restantes.
Les assertions ne sont pas déduites automatiquement de la présence de
mots-clés. Un sujet non réconcilié peut être nommé explicitement sans
lui inventer de concept ni d'identité canonique.

```sh
python -m anamu_analysis.extraction queue --state not_examined_for_extraction --source-prefix docs/courses/ --limit 15 --packets
python -m anamu_analysis.extraction queue --state partial_extraction --limit 10 --packets
python -m anamu_analysis.extraction audit-anchors
```

Le pont GitHub propose aussi une lecture groupée sans publication avec
`batchSpec.mode = "packet"`, `paths` et éventuellement `material_ids`.
Le résultat est borné aux fragments demandés, accompagné de la révision et
du commit. Un changement de tête entre lecture et publication oblige à
relire la source. Les documents ne sont jamais exécutés. L'audit des
ancrages est un contrôle documentaire, pas un jugement musicologique.

## État courant de l'extraction

| Indicateur | Valeur |
| --- | ---: |
| Unités documentaires | 7 323 |
| Unités portant une assertion candidate | 74 |
| Assertions candidates | 154 |
| Assertions v2 avec ancrage d'extrait exact | 88 |
| Revues explicites de passages | 56 |
| Passages clos après extraction | 44 |
| Passages clos sans assertion analytique | 2 |
| Extractions explicitement partielles | 10 |
| Extractions historiques sans disposition de clôture | 20 |
| Mentions avec sujet explicitement non réconcilié (sans lien) | 26 |

Les 44 nouvelles clôtures concernent les mécanismes 1–44 des deux
synthèses thématiques AnaMu d'Open Music Theory. Les textes des fragments
ont été lus et leurs empreintes et ancrages ont été contrôlés sur GitHub
après publication : 28 assertions dans la première synthèse et 60 dans
la seconde, zéro divergence détectée. La clôture désigne une passe sur
la synthèse disponible, non une lecture exhaustive des traités externes,
qui n'ont pas été consultés à nouveau. Elle ne valide aucune interprétation
d'œuvre et ne clôt aucun cours. Les cinq lots sont dans mentions/omt-*.json.

Il reste 7 277 unités non closes. Le dénominateur des connaissances
à extraire demeure inconnu. La commande Python d'audit intégral et
la nouvelle CLI de paquets n'ont pas été exécutées sur un checkout
complet dans cette reprise. Les contrôles effectués ici ont utilisé
les octets et registres réellement récupérés via GitHub.
