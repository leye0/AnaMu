# Est-ce qu'ignorer les votes minoritaires nous prive de signal ?

**Exploratoire seulement : même cohorte humaine de 1 900 extraits déjà examinée.**

Apprentissage sur 0, ⅓, ⅔, 1 vote; évaluation strictement sur la majorité humaine (2 ou 3 votes).

## Cohérence des annotations originales

| Émotion | 0 vote | 1 vote | 2 votes | 3 votes | Part majoritaire parmi les mentions |
|---|---:|---:|---:|---:|---:|
| Mysterious | 1285 | 379 | 147 | 89 | 38.4% |
| Epic | 1498 | 227 | 101 | 74 | 43.5% |
| Tense | 1417 | 253 | 135 | 95 | 47.6% |
| Dark | 1383 | 282 | 134 | 101 | 45.5% |
| Happy | 1138 | 447 | 203 | 112 | 41.3% |

## Prédiction hors vidéo d'entraînement (AP)

| Variante | Tense | Mysterious | Epic | Dark | Happy | Hard5 mAP | Noncalm14 mAP |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 : majorité binaire | 0.392 | 0.295 | 0.387 | 0.340 | 0.328 | 0.348 | 0.467 |
| H1 : votes fractionnaires | 0.416 | 0.297 | 0.431 | 0.371 | 0.342 | 0.372 | 0.487 |
| Distribution tonale : majorité binaire | 0.406 | 0.307 | 0.381 | 0.390 | 0.323 | 0.361 | 0.470 |
| Distribution tonale : votes fractionnaires | 0.433 | 0.308 | 0.424 | 0.431 | 0.336 | 0.386 | 0.492 |

## Incertitude : comparaison au meilleur modèle binaire actuel

| Variante | Tense ΔAP | Mysterious ΔAP | Epic ΔAP | Dark ΔAP | Happy ΔAP | Hard5 ΔmAP |
|---|---:|---:|---:|---:|---:|---:|
| H1 : majorité binaire | -0.014 [-0.033, 0.006] | -0.012 [-0.035, 0.009] | +0.006 [-0.012, 0.026] | -0.049 [-0.081, -0.024] | +0.005 [-0.004, 0.014] | -0.013 [-0.024, -0.003] |
| H1 : votes fractionnaires | +0.010 [-0.020, 0.037] | -0.010 [-0.040, 0.022] | +0.050 [0.014, 0.087] | -0.018 [-0.058, 0.017] | +0.019 [0.002, 0.036] | +0.010 [-0.005, 0.025] |
| Distribution tonale : votes fractionnaires | +0.027 [0.004, 0.048] | +0.001 [-0.027, 0.025] | +0.042 [0.011, 0.079] | +0.041 [0.012, 0.068] | +0.013 [-0.005, 0.031] | +0.025 [0.012, 0.037] |

Contrôle négatif : votes *Dark* mélangés uniquement à l'entraînement, AP hors pli 0.133.

Cette méthode suit une adaptation multi-étiquettes de l'idée de *Label Distribution Learning* (Xin Geng, TKDE 2016) : chaque vote informe une probabilité par émotion, et les étiquettes ne sont pas normalisées entre elles.

Les votes d'experts sont eux-mêmes inclus dans la majorité de référence : ces chiffres ne calculent pas un plafond de performance humaine. Les mêmes 1 900 clips avaient déjà servi à d'autres recherches.
