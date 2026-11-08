# Rubans de tension originaux sur les émotions MIDI difficiles

**Exploration post-hoc, pas une nouvelle découverte validée** : les 1 900 étiquettes PIAST ont déjà été vues.

MIDI traité : 1900/1900 ; rubans calculés : 1900/1900 ; manquants : 0 ; Partitura 1.9.0.

## Mesure réelle, au-delà de la distribution tonale

| Variante | Tense AP | Dark AP | Mysterious AP | Epic AP | Happy AP | Hard5 mAP | Noncalm14 mAP |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 historique | 0.392 | 0.340 | 0.295 | 0.387 | 0.328 | 0.348 | 0.467 |
| H1 + distribution tonale (comparateur fort) | 0.406 | 0.390 | 0.307 | 0.381 | 0.323 | 0.361 | 0.470 |
| + diamètre du nuage tonal | 0.410 | 0.385 | 0.308 | 0.382 | 0.323 | 0.362 | 0.468 |
| + trois rubans originaux | 0.410 | 0.385 | 0.308 | 0.377 | 0.321 | 0.360 | 0.466 |
| + rubans attribués à d'autres morceaux (placebo) | 0.402 | 0.394 | 0.304 | 0.381 | 0.317 | 0.359 | 0.463 |

## Incertitude par vidéo : gains contre la distribution tonale, pas H1

| Variante | Dark ΔAP et IC95% | Hard5 ΔmAP et IC95% | Noncalm14 ΔmAP et IC95% |
|---|---:|---:|---:|
| H1 historique | -0.049 [-0.081, -0.024] | -0.013 [-0.024, -0.003] | -0.003 [-0.009, 0.003] |
| + diamètre du nuage tonal | -0.004 [-0.014, 0.003] | +0.000 [-0.004, 0.004] | -0.001 [-0.003, 0.000] |
| + trois rubans originaux | -0.005 [-0.019, 0.008] | -0.001 [-0.007, 0.004] | -0.004 [-0.007, -0.001] |
| + rubans attribués à d'autres morceaux (placebo) | +0.004 [-0.012, 0.020] | -0.002 [-0.007, 0.004] | -0.006 [-0.009, -0.003] |

Contrôle négatif : étiquettes *Dark* mélangées à l'entraînement, AP hors pli 0.121.

**Interprétation** : le placebo vérifie que l'amélioration n'est pas due au seul nombre de variables. Les IC sont conditionnels aux prédictions hors pli ; un corpus humain indépendant reste indispensable avant de parler de progrès généralisable.

Source méthodologique : Herremans & Chew, *Tension Ribbons* (2016), et Partitura `estimate_tonaltension` (mêmes axes et fenêtres que notre test IsoVAT).
