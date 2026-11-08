# PIAST-AT — hypothèses scientifiques à tester, pas « outils académiques »

**8 novembre 2026.** AnaMu cherche ici à comprendre quelles observations
symboliques sont réellement prédictives des **humeurs perçues**. Les
annotations PIAST-AT sont des jugements de trois experts sur 16 termes :
elles ne mesurent pas les émotions réellement *ressenties* par l'auditeur.
Genre et style sont exclus. L'accord de **deux experts sur trois** définit
les étiquettes positives. Aucun fichier audio n'est analysé.

## Une étude expérimentale précise → une hypothèse calculable

**Recherche principale.** [Micallef Grimaud & Eerola (2022), *Emotional
expression through musical cues: A comparison of production and perception
approaches*, PLOS ONE](https://doi.org/10.1371/journal.pone.0279605).
Les participants manipulaient notamment **mode majeur/mineur, tempo,
articulation staccato/legato, hauteur et dynamique** pour communiquer
différentes émotions. Les combinaisons et le contexte comptaient :
le résultat ne se réduit pas à « une note mineure implique la tristesse ».
L'étude portait sur des extraits instrumentaux manipulés ; elle **n'a pas
validé notre détecteur** sur PIAST-AT ni même les 16 mêmes étiquettes.

**Base perceptive du mode.** [Krumhansl & Kessler (1982), *Tracing the dynamic
changes in perceived tonal organization*](https://doi.org/10.1037/0033-295X.89.4.334).
L'algorithme expérimental utilise leurs profils de perception des 12 degrés
majeurs et mineurs, comparés à la distribution des notes réellement jouées.
Nous conservons deux degrés de confiance plutôt que d'imposer une tonalité
unique, possiblement fausse.

### Trois expériences identiques sauf pour les observations

| Essai | Ce que regarde le détecteur | Hypothèse testée |
|---|---|---|
| **H0 : référence** | 97 résumés de densité, registre, intervalles, durée, dynamique, harmonie et déroulement déjà disponibles | Les caractéristiques générales sont-elles déjà suffisantes ? |
| **H1 : indices issus de la recherche** | H0 + **mode probable**, tempo réellement joué, variations de tempo, durée des notes relativement à leurs suivantes, articulation staccato/legato estimée, évolution des nuances | Ces dimensions ajoutent-elles de l'information ? |
| **H2 : indices combinés** | H1 + mode × tempo, mode × articulation, tempo × articulation, mode × nuances, tempo × nuances, mode × variations de tempo | Les combinaisons sont-elles plus informatives que chaque indice isolé ? |

**Ce ne sont pas des coefficients empruntés à une publication.** Les équations
des six produits croisés ont été choisies ici comme hypothèses reproductibles,
*avant de comparer les variantes au test*. Les valeurs de tempo et les notes
sont extraites du MIDI seulement. L'articulation est approximée à partir du
rapport durée/inter-onset de la voix supérieure ; ce n'est pas une vérité
musicologique, et les pédales, accords et transcriptions peuvent la tromper.

Protocole : même classificateur linéaire, mêmes 16 catégories, mêmes morceaux,
mêmes groupes vidéo disjoints en entraînement (70 %), validation (15 %)
et test (15 %). La mesure choisie est la **précision moyenne du classement
(AP)**, confrontée à la fréquence de chaque émotion dans les données.
La moyenne principale exclut le terme générique `Emotional` ; toute catégorie
avec moins de trois exemples positifs dans le test est déclarée insuffisante.

Les 240 premiers extraits ont déjà été examinés lors du pilote. Le rapport
sur 850 pièces distingue donc un **test nouveau** qui exclut tous les groupes
vidéo de ces 240 morceaux, afin de ne pas masquer une régression par des
exemples déjà vus. Il ne s'agit pas d'une validation dans un autre corpus.

## Prochaines hypothèses indépendantes

1. **Attente et surprise :** [Egermann et al. (2013)](https://pubmed.ncbi.nlm.nih.gov/23605956/)
   ont relié des surprises mélodiques calculées probabilistiquement à des
   réponses psychophysiologiques et subjectives lors de concerts. Tester
   la surprise des continuations *avant chaque note*, ainsi que les
   accumulations et résolutions, contre un modèle dont l'ordre des notes est
   mélangé. Un lien éventuel avec les humeurs globales de PIAST ne reproduira
   pas leurs résultats temporels.
2. **Contexte appris et surprise :** [une étude de 2023 publiée dans
   *Philosophical Transactions B*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10725761/)
   trouve des contributions complémentaires d'attentes sensorielles et
   cognitives aux jugements de surprise/plaisir. Construire deux familles
   d'attentes symboliques et tester leur apport séparé. Il ne s'agit pas
   d'un modèle d'émotion prêt à l'emploi.
3. **Dynamique de la tension :** [Farbood (2012), *A Parametric, Temporal
   Model of Musical Tension*](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/f/11865/files/2020/08/Farbood_2012_Musical_Tension.pdf).
   Tester pentes, pics et relaxation des tensions sur une fenêtre glissante,
   plutôt qu'une moyenne de dissonance. Vérifier sur les labels humains
   si la temporalité apporte une information supplémentaire.

**Aucun de ces trois mécanismes supplémentaires n'est déclaré testé tant
qu'un vrai score d'ablation sur les données réservées ne le confirme.**

## Résultat observé — première hypothèse (8 novembre 2026)

Après avoir fixé les trois variantes ci-dessus, nous les avons exécutées
sur les **mêmes 850 MIDI** : 613 en entraînement, 115 en validation,
122 en test. Parmi les 122, **91 appartiennent à des groupes vidéo qui
n'avaient pas figuré dans le premier pilote de 240 pièces**.

Les 850 MIDI ont été lus sans refus. Les trois variantes partagent le
classificateur linéaire fixé à l'avance, les mêmes étiquettes humaines et le
même découpage. Moyenne d'AP des 15 humeurs spécifiques (hors `Emotional`) :

| Algorithme | Validation, 115 | Test complet, 122 | Nouveau test, 91 |
|---|---:|---:|---:|
| H0 : 97 observations générales | 0,490 | 0,452 | 0,528 |
| H1 : H0 + 10 indices perceptifs | **0,537** | **0,474** | **0,548** |
| H2 : H1 + 6 interactions | 0,538 | 0,468 | 0,539 |
| Référence par fréquence, sans musique | 0,166 | 0,169 | 0,178 |

**Bilan :** l'ajout des 10 indices H1 améliore le classement moyen de 0,020
point d'AP sur les 91 pièces nouvelles, mais ce n'est **pas** une preuve
statistique générale ni une validation de causalité. H2 est légèrement plus
faible que H1 sur les morceaux nouveaux malgré une validation supérieure :
**ne pas retenir une complexité supplémentaire uniquement parce qu'elle
améliore la validation.**

Sur le nouveau test H1 améliore `Bright` de +0,216 AP, `Dark` de +0,120,
`Cute` de +0,120 et `Tense` de +0,080 ; mais dégrade `Powerful` de −0,178,
`Intense/Grand` de −0,092, `Upbeat/Energetic` de −0,055. Le bilan ne
cache donc pas les régressions par émotion.

Rapports bruts et reproductibles :
[H0](../reports/piast-at-850-basic.md),
[H1](../reports/piast-at-850-research-cues.md),
[H2](../reports/piast-at-850-research-interactions.md),
et les mêmes noms en `.json`.

```bash
python -m scripts.fetch_piast_at /tmp/piast-at --limit 850
python -m scripts.piast_at_benchmark /tmp/piast-at --limit 850 --fresh-after 240 \
  --feature-set basic
python -m scripts.piast_at_benchmark /tmp/piast-at --limit 850 --fresh-after 240 \
  --feature-set research_cues
python -m scripts.piast_at_benchmark /tmp/piast-at --limit 850 --fresh-after 240 \
  --feature-set research_interactions
```

Le prochain test doit porter sur **les attentes et surprises mélodiques
apprises sans les labels** avec un véritable contrôle d'ordre temporel,
et non sur l'accumulation indiscriminée de variables.
