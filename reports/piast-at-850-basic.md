# PIAST-AT — premier banc MIDI → humeurs humaines

- Corpus : 2023 extraits annotés ; 850 MIDI locaux ; 850 analysés, 0 rejetés.
- Cibles : **humeurs/traits de perception**, pas émotions ressenties ; accord de **2 experts sur 3**.
- Entrée : uniquement MIDI. Classes genre/style exclues des cibles.
- Découpage : {'train': 613, 'validation': 115, 'test': 122} ; sans chanson/vidéo partagée.
- Observations : 97 résumés MIDI ; variante `basic`.

## Validation et test séparés

| Échantillon | Humeurs évaluables | AP moyenne du classement | Référence de fréquence |
|---|---:|---:|---:|
| validation / named_moods | 15 | 0.490 | 0.166 |
| validation / all_moods | 16 | 0.512 | 0.194 |
| test / named_moods | 15 | 0.452 | 0.169 |
| test / all_moods | 16 | 0.473 | 0.194 |
| fresh_test / named_moods | 15 | 0.528 | 0.178 |
| fresh_test / all_moods | 16 | 0.545 | 0.203 |

## Détail du test (majorité des experts)

| Terme | Exemples positifs test | AP modèle | AP hasard | F1 (seuil 0,5) |
|---|---:|---:|---:|---:|
| Bright | 34 | 0.473 | 0.279 | 0.557 |
| Cute | 10 | 0.235 | 0.082 | 0.258 |
| Dark | 16 | 0.234 | 0.131 | 0.245 |
| Dreamy | 21 | 0.337 | 0.172 | 0.412 |
| Emotional | 68 | 0.793 | 0.557 | 0.792 |
| Epic | 11 | 0.296 | 0.090 | 0.387 |
| Happy | 23 | 0.193 | 0.189 | 0.242 |
| Intense/Grand | 16 | 0.670 | 0.131 | 0.615 |
| Mysterious | 18 | 0.366 | 0.148 | 0.400 |
| Passionate | 19 | 0.804 | 0.156 | 0.653 |
| Playful | 21 | 0.581 | 0.172 | 0.561 |
| Powerful | 11 | 0.612 | 0.090 | 0.606 |
| Relaxing/Calm | 59 | 0.809 | 0.484 | 0.780 |
| Sad | 11 | 0.257 | 0.090 | 0.304 |
| Tense | 18 | 0.245 | 0.148 | 0.240 |
| Upbeat/Energetic | 22 | 0.668 | 0.180 | 0.618 |

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

Extraction et mesures : 22.22 s.
