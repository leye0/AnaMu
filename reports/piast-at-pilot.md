# PIAST-AT — premier banc MIDI → humeurs humaines

- Corpus : 2023 extraits annotés ; 240 MIDI locaux ; 240 analysés, 0 rejetés.
- Cibles : **humeurs/traits de perception**, pas émotions ressenties ; accord de **2 experts sur 3**.
- Entrée : uniquement MIDI. Classes genre/style exclues des cibles.
- Découpage : {'train': 180, 'validation': 29, 'test': 31} ; sans chanson/vidéo partagée.
- Observations : 97 résumés MIDI ; variante `basic`.

## Validation et test séparés

| Échantillon | Humeurs évaluables | AP moyenne du classement | Référence de fréquence |
|---|---:|---:|---:|
| validation / named_moods | 14 | 0.520 | 0.190 |
| validation / all_moods | 15 | 0.533 | 0.216 |
| test / named_moods | 12 | 0.393 | 0.167 |
| test / all_moods | 13 | 0.412 | 0.191 |

## Détail du test (majorité des experts)

| Terme | Exemples positifs test | AP modèle | AP hasard | F1 (seuil 0,5) |
|---|---:|---:|---:|---:|
| Bright | 6 | 0.520 | 0.194 | 0.286 |
| Cute | 3 | 0.087 | 0.097 | 0.000 |
| Dark | 5 | 0.152 | 0.161 | 0.000 |
| Dreamy | 4 | 0.377 | 0.129 | 0.500 |
| Emotional | 15 | 0.630 | 0.484 | 0.667 |
| Epic | 1 | — | — | — |
| Happy | 5 | 0.134 | 0.161 | 0.000 |
| Intense/Grand | 3 | 0.423 | 0.097 | 0.444 |
| Mysterious | 3 | 0.402 | 0.097 | 0.250 |
| Passionate | 4 | 0.715 | 0.129 | 0.600 |
| Playful | 6 | 0.251 | 0.194 | 0.375 |
| Powerful | 2 | — | — | — |
| Relaxing/Calm | 12 | 0.620 | 0.387 | 0.500 |
| Sad | 2 | — | — | — |
| Tense | 6 | 0.360 | 0.194 | 0.200 |
| Upbeat/Energetic | 5 | 0.679 | 0.161 | 0.429 |

## Popularité des humeurs dans les 2 023 annotations

| Terme | Cité par ≥1 expert | Accord ≥2 experts |
|---|---:|---:|
| Emotional | 1566 | 1225 |
| Relaxing/Calm | 1379 | 908 |
| Bright | 931 | 521 |
| Dreamy | 881 | 400 |
| Happy | 807 | 332 |
| Mysterious | 647 | 254 |
| Playful | 642 | 360 |
| Upbeat/Energetic | 599 | 353 |
| Passionate | 598 | 327 |
| Intense/Grand | 571 | 274 |

## Limites

- Échantillon prélevé par hachage ; certaines humeurs rares ont trop peu d'exemples dans le test.
- Associations musique/humeur, pas preuve d'émotion réellement ressentie ou causée.
- Domaine limité au piano solo ; aucun audio analysé, transfert à d'autres styles non démontré.
- Les MIDI de structure irrégulière peuvent être refusés ; refus et couverture sont déclarés.
- Le terme générique 'Emotional' est exclu de la moyenne des humeurs nommées.
- Validation et test restent séparés ; aucune sélection ni réglage sur les labels de test.

Extraction et mesures : 0.29 s.
