# La tonalité suit-elle vraiment les émotions difficiles ?

**Exploratoire : 1900 MIDI déjà examinés. Aucun nouveau test externe.**

Cinq plis sans aucune œuvre/vidéo partagée ; les 10 statistiques de distribution sont séparées des 8 signatures de transition.

| Variante | Dark (AP hors pli) | Hard 5 (mAP hors pli) | Noncalm 14 (mAP hors pli) |
|---|---:|---:|---:|
| H1 | 0.340 | 0.348 | 0.467 |
| H1 + distribution tonale | 0.390 | 0.361 | 0.470 |
| H1 + distribution + ordre réel | 0.389 | 0.361 | 0.467 |
| H1 + distribution + ordre mélangé | 0.390 | 0.358 | 0.463 |

## Émotions réellement difficiles

| Émotion | Positifs / 1900 | H1 | Distribution | Ordre réel | Ordre mélangé |
|---|---:|---:|---:|---:|---:|
| Mysterious | 236 | 0.295 | 0.307 | 0.306 | 0.307 |
| Epic | 175 | 0.387 | 0.381 | 0.369 | 0.370 |
| Tense | 230 | 0.392 | 0.406 | 0.416 | 0.409 |
| Dark | 235 | 0.340 | 0.390 | 0.389 | 0.390 |
| Happy | 315 | 0.328 | 0.323 | 0.324 | 0.316 |

## Incertitude (rééchantillonnage des vidéos ; Δ AP vs H1)

| Variante | Dark Δ et IC 95 % | Hard 5 Δ et IC 95 % | Noncalm 14 Δ et IC 95 % |
|---|---:|---:|---:|
| H1 + distribution tonale | +0.049 [0.023, 0.080] | +0.013 [0.003, 0.024] | +0.003 [-0.003, 0.008] |
| H1 + distribution + ordre réel | +0.049 [0.016, 0.085] | +0.012 [-0.001, 0.026] | +0.000 [-0.007, 0.007] |
| H1 + distribution + ordre mélangé | +0.050 [0.022, 0.083] | +0.010 [-0.003, 0.023] | -0.003 [-0.011, 0.004] |

Contrôle étiquettes Dark mélangées **sur l'entraînement seulement** : AP hors pli 0.118.

Attention : les intervalles conditionnent sur les prédictions déjà entraînées ; ce ne sont **pas** des preuves de nouvelle découverte.
La sélection d'une variante à partir de ces résultats exigera un autre corpus d'annotations humaines indépendant.