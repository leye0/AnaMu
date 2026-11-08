# Classement directement optimisé sur les émotions fortes : CP-WTC

**8 novembre 2026 — expérience exploratoire. Pas de gain majeur validé.**

## Origine et hypothèse

Le cadre de comparaison relative des interprétations est étudié par
[Ching et Widmer (ISMIR 2026)](https://ismir2026program.ismir.net/poster_413.html)
et son [code officiel](https://github.com/joann8512/performance-rlt).
Notre ancienne régression Ridge ajustait directement les valeurs numériques
de valence/activation, alors que notre mesure prioritaire cherche le **bon
ordre entre deux interprétations de la même partition**.

Hypothèse testée : optimiser les différences de classement pendant
l'entraînement est plus approprié pour les grands désaccords humains.

Implémentation propre (`scripts/cp_wtc_pairwise_rank_benchmark.py`) :

- les 288 MIDI des six pianistes sont regroupés par **48 œuvres entières** ;
- six plis extérieurs `GroupKFold` ne voient **aucune composition testée** ;
- les différences de variables sont apprises avec une régression logistique
  de classement à intercept nul, et paires symétrisées ;
- seuls les écarts humains clairement distincts servent à entraîner le
  classeur (activation ≥10, valence ≥1) ;
- la régularisation `C ∈ {0,01 ; 0,1 ; 1 ; 10}` est choisie par une
  **validation imbriquée** sur quatre plis d'œuvres d'entraînement ;
- témoin : mélanger les labels humains entre interprètes de la **même**
  œuvre dans l'entraînement seulement, jamais dans le test.

L'article original utilise une architecture et des caractéristiques
différentes ; ce script **n'en revendique pas la réimplémentation**.

## Mesures hors œuvre

| Humeur humaine relative | Ridge (14 variables MIDI) | Rang optimisé sur paires | Labels d'entraînement mélangés |
|---|---:|---:|---:|
| Activation, Δ≥10 | **269/339 = 79,4 %** | **272/339 = 80,2 %** | 164/339 = 48,4 % |
| Valence, Δ≥1 | **137/193 = 71,0 %** | **133/193 = 68,9 %** | 103/193 = 53,4 % |

Gain de classement contre Ridge : **+0,9 point** en activation, intervalle
exploratoire de bootstrap par composition **[−1,1 ; +3,1 points]** ;
**−2,1 points** en valence, **[−6,9 ; +2,7 points]**.

Le témoin revient près du hasard, signe que l'entraînement réel exploite
des relations entre observations et labels. Cela ne démontre ni un modèle
causal de l'émotion ni une fiabilité indépendante des six identités
d'interprète et des groupes d'annotateurs.

**Conclusion : changer la fonction de perte ne résout pas le problème.**
La représentation des phénomènes musicaux est un goulot d'étranglement plus
plausible. Ne pas déployer le classeur de remplacement.

## Reproduction

```bash
python -m scripts.cp_wtc_pairwise_rank_benchmark /chemin/The-CP-WTC-Dataset \
  --output /tmp/anamu-cp-wtc-pairwise-result.json
```

Seules les annotations humaines et les MIDI du dépôt officiel sont lus ;
aucun audio n'est analysé. Le jeu CP-WTC est sous licence CC BY-NC-SA 4.0.
Les 48 œuvres ont déjà été inspectées par notre recherche : ce nouveau test
reste **exploratoire**, même si sa validation interne est sans fuite.
