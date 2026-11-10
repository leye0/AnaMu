# AnaMu Grammar — règles de preuve et d'évaluation

**Contrat actuel (10 novembre 2026).** Ce document concerne les capacités
grammaticales G0–G6, **pas** des classes d'humeurs ou un score unique.
Le niveau « universitaire exhaustif » est un **deuxième verrou** : chacun des
cours et contenus applicables doit être cartographié au
[référentiel universitaire](university-curriculum.md), puis aux preuves et
cases du [TODO](todo-university-coverage.md). Réussir des tests unitaires
n'autorise pas à déclarer une compétence d'orchestration acquise.

## Chaque affirmation appartient à un niveau

1. **Donnée brute** : octet MIDI, événement, note MusicXML, échantillon audio.
2. **Observation construite** : note appariée de façon non ambiguë, intervalle
   temporel, énergie acoustique, partie déclarée.
3. **Hypothèse grammaticale** : voix, motif, phrase, accord, rôle, fonction,
   structure de section.
4. **Annotation indépendante** : décision d'un analyste ou d'un auditeur
   identifiée, avec sa tâche et sa licence.
5. **Conclusion évaluée** : résultat du mécanisme sur une source séparée,
   accompagné de baselines, erreurs et inconnus.

Une observation ne devient pas une annotation, et une hypothèse ne devient
pas une vérité par simple répétition. Le moteur doit garder provenance,
version, paramètres, qualité et ambiguïté.

## Sources et vérités admissibles

| Capacité évaluée | Vérité possible | Interdictions |
|---|---|---|
| G0 : lecture MIDI | Événements originaux et fixtures exactes | Inférer acoustique ou voix principale des pistes |
| G1 : ordre/chevauchement | Intervalles d'événements, 13 relations d'Allen | Appeler toute simultanéité « accord » ou « motif » |
| Instrumentation écrite | Noms et parties MusicXML | Traiter `instrument_name` MIDI comme la partition réelle |
| G2 : voix/motifs | Annotations de rôles Hauptstimme, transformations vérifiées | Lire l'annotation de test pendant l'analyse |
| G2/G4 : groupements et phrases | Frontières expertisées, corpus GTTM/SALAMI selon unité | Faire valider une phrase avec une étiquette de note |
| G3 : harmonie | Analyses DCML, partition et théorie explicite | Assimiler automatiquement sonorité et fonction |
| G5 : expression | Partition + performance alignées ; audio calibré | Confondre CC7, vélocité et décibels |

Les tâches d'**attentes mélodiques** de Cuddy–Lunney, Schellenberg et
Manzara sont des contrôles scientifiques distincts : continuation jugée,
surprise de vraie note et segmentation ne sont **pas interchangeables**.
Voir les [études utilisées](README.md).

## Avant d'annoncer un gain

- Décrire **exactement** l'unité indépendante (œuvre, mouvement, performance,
  segment) et les groupes partagés entre développement et test.
- Fixer les cibles et la métrique avant l'analyse du jeu d'évaluation ;
  ne pas ajuster une heuristique en regardant le test final.
- Comparer à une **baseline triviale** : répétition, contour, note précédente,
  densité, segmentation régulière, instrument constant selon la tâche.
- Ajouter un **témoin négatif** : labels mélangés, notes réordonnées ou
  association de la mauvaise partition, sans créer une tâche artificiellement
  impossible.
- Rapporter faux positifs, faux négatifs, cas d'ambiguïté, couverture
  des sources, temps de calcul et variations entre œuvres.
- Préférer une conclusion **négative** honnête à une amélioration obtenue
  après sélection répétée sur le même petit corpus.
- Vérifier la **licence de chaque artefact**, en distinguant code,
  partitions, MIDI, annotations et enregistrements.
- Garder les sources indépendantes : ne pas entraîner un détecteur de voix
  avec la partition de référence du morceau testé.

## Contrats déjà exécutés

- Les tests G0 préservent événements et incertitudes de pairage.
- Les tests G1 couvrent les 13 relations temporelles et transformations
  exactes, sans classifier de thèmes.
- Les deux MIDI Beethoven ont leurs empreintes et un audit de polyphonie.
- Les deux partitions MusicXML indépendantes ont leur inventaire de parties ;
  la divergence des noms d'instruments est documentée sans correction tacite.

## Ce qui reste à prouver

- L'identité et le regroupement **note par note** entre éditions.
- Une segmentation autonome et reproductible de voix, motifs et phrases,
  confrontée à des analystes humains indépendants.
- Les relations harmoniques et orchestrales au-delà de l'inventaire.
- Les correspondances partition–performance–audio avec incertitudes.

Les épreuves prioritaires sont dans le
[TODO de couverture](todo-university-coverage.md) ; [roadmap.md](roadmap.md)
conserve seulement les acquis vérifiés. Aucun score émotionnel ancien ne
constitue une preuve d'une capacité G2–G6.
