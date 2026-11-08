# D'où vient le gain des votes humains ?

**Audit mécanistique exploratoire sur les mêmes 1900 clips PIAST déjà étudiés.**

Même distribution tonale et mêmes cinq plis sans vidéo partagée dans toutes les variantes.

| Variante | Tense AP | Mysterious AP | Epic AP | Dark AP | Happy AP | Hard5 mAP | Noncalm14 mAP |
|---|---:|---:|---:|---:|---:|---:|---:|
| Majorité binaire | 0.406 | 0.307 | 0.381 | 0.390 | 0.323 | 0.361 | 0.470 |
| Votes minoritaires seulement | 0.436 | 0.311 | 0.426 | 0.425 | 0.339 | 0.387 | 0.493 |
| Incertitude des positifs seulement | 0.402 | 0.308 | 0.380 | 0.388 | 0.321 | 0.360 | 0.469 |
| Vrais votes 0/⅓/⅔/1 | 0.433 | 0.308 | 0.424 | 0.431 | 0.336 | 0.386 | 0.492 |
| Votes réattribués dans chaque classe (placebo) | 0.379 | 0.279 | 0.379 | 0.420 | 0.290 | 0.349 | 0.445 |

## Incertitude par groupe, Δ contre la majorité binaire

| Variante | Tense Δ et IC95% | Mysterious Δ et IC95% | Epic Δ et IC95% | Dark Δ et IC95% | Hard5 Δ et IC95% |
|---|---:|---:|---:|---:|---:|
| Votes minoritaires seulement | +0.029 [0.010, 0.048] | +0.004 [-0.018, 0.023] | +0.044 [0.014, 0.074] | +0.035 [0.009, 0.053] | +0.026 [0.015, 0.034] |
| Incertitude des positifs seulement | -0.004 [-0.011, 0.005] | +0.001 [-0.007, 0.009] | -0.002 [-0.009, 0.005] | -0.002 [-0.009, 0.005] | -0.002 [-0.005, 0.001] |
| Vrais votes 0/⅓/⅔/1 | +0.027 [0.004, 0.048] | +0.001 [-0.027, 0.025] | +0.042 [0.011, 0.079] | +0.041 [0.012, 0.068] | +0.025 [0.012, 0.037] |
| Votes réattribués dans chaque classe (placebo) | -0.027 [-0.053, -0.002] | -0.028 [-0.056, -0.000] | -0.002 [-0.036, 0.034] | +0.030 [-0.003, 0.054] | -0.012 [-0.025, -0.000] |

**Test central** : la différence entre les vrais votes et les votes réattribués dans la même classe élimine les effets de prévalence et de lissage de la seule majorité binaire ; seule l'association précise avec les morceaux diffère.

Ce contrôle n'annule pas la sélection post-hoc de notre hypothèse.
