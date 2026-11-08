# 0,5 signifie-t-il vraiment une probabilité émotionnelle de 50 % ?

**Non automatiquement : ce sont des scores multi-étiquettes rééquilibrés.**

Même cohorte de 1900 MIDI et même configuration que les tests précédents ; protocole exploratoire.
Les pertes Brier/logarithmiques évaluent une voix d'expert tirée au hasard, d'après les trois votes disponibles ; une valeur plus basse est meilleure.

| Modèle | Hard5 AP ↑ | Hard5 Brier ↓ | Hard5 Log-loss ↓ | Noncalm14 AP ↑ | Noncalm14 Brier ↓ |
|---|---:|---:|---:|---:|---:|
| Majorité binaire, classes équilibrées | 0.361 | 0.180 | 0.562 | 0.470 | 0.160 |
| Votes fractionnaires, classes équilibrées | 0.386 | 0.190 | 0.563 | 0.492 | 0.170 |
| Votes fractionnaires, correction des cotes | 0.386 | 0.116 | 0.378 | 0.492 | 0.111 |
| Votes fractionnaires, sans rééquilibrage | 0.393 | 0.115 | 0.374 | 0.497 | 0.110 |
| Taux moyen des votes à l'entraînement (null) | 0.117 | 0.131 | 0.429 | 0.135 | 0.137 |

## Les cinq émotions difficiles : erreur de probabilité par voix

| Émotion | Taux de vote humain | Balanced : préd. moy. | Balanced : Brier | Odds corrigés : Brier | Sans poids : Brier |
|---|---:|---:|---:|---:|---:|
| Mysterious | 0.165 | 0.437 | 0.218 | 0.131 | 0.131 |
| Epic | 0.114 | 0.341 | 0.159 | 0.085 | 0.083 |
| Tense | 0.142 | 0.375 | 0.177 | 0.104 | 0.103 |
| Dark | 0.150 | 0.377 | 0.180 | 0.110 | 0.108 |
| Happy | 0.209 | 0.438 | 0.214 | 0.152 | 0.151 |

## Brier : gains contre le modèle fractionnaire rééquilibré

| Modèle | Hard5 amélioration (IC95% par vidéo) | Noncalm14 amélioration (IC95% par vidéo) |
|---|---:|---:|
| Majorité binaire, classes équilibrées | +0.009 [0.007, 0.012] | +0.010 [0.009, 0.011] |
| Votes fractionnaires, correction des cotes | +0.073 [0.070, 0.077] | +0.059 [0.057, 0.062] |
| Votes fractionnaires, sans rééquilibrage | +0.074 [0.071, 0.078] | +0.060 [0.058, 0.063] |
| Taux moyen des votes à l'entraînement (null) | +0.059 [0.053, 0.065] | +0.033 [0.030, 0.037] |

Dans ce protocole, une sortie 0,5 pour *Epic* doit seulement être interprétée comme « une moitié des annotateurs de ce type diraient Epic » si la calibration est démontrée ; jamais 50 % de toute la masse d'émotions possibles.

La classe *Relaxing/Calm* est exclue des moyennes ciblées.

Source : [run 42520423568](https://github.com/leye0/AnaMu/actions/runs/42520423568), commit `77c810a72fd8e97f75199bf0f8824f34000aa12b`. Résultat antérieur archivé, pas une nouvelle expérience.
