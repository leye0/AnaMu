# PIAST-AT — premier banc MIDI → humeurs humaines

- Corpus : 2023 extraits annotés ; 850 MIDI locaux ; 850 analysés, 0 rejetés.
- Cibles : **humeurs/traits de perception**, pas émotions ressenties ; accord de **2 experts sur 3**.
- Entrée : uniquement MIDI. Classes genre/style exclues des cibles.
- Découpage : {'train': 613, 'validation': 115, 'test': 122} ; sans chanson/vidéo partagée.
- Observations : 107 résumés MIDI ; variante `research_cues`.

## Validation et test séparés

| Échantillon | Humeurs évaluables | AP moyenne du classement | Référence de fréquence |
|---|---:|---:|---:|
| validation / named_moods | 15 | 0.537 | 0.166 |
| validation / all_moods | 16 | 0.556 | 0.194 |
| test / named_moods | 15 | 0.474 | 0.169 |
| test / all_moods | 16 | 0.494 | 0.194 |
| fresh_test / named_moods | 15 | 0.548 | 0.178 |
| fresh_test / all_moods | 16 | 0.564 | 0.203 |

## Détail du test (majorité des experts)

| Terme | Exemples positifs test | AP modèle | AP hasard | F1 (seuil 0,5) |
|---|---:|---:|---:|---:|
| Bright | 34 | 0.600 | 0.279 | 0.622 |
| Cute | 10 | 0.333 | 0.082 | 0.261 |
| Dark | 16 | 0.365 | 0.131 | 0.410 |
| Dreamy | 21 | 0.335 | 0.172 | 0.358 |
| Emotional | 68 | 0.801 | 0.557 | 0.794 |
| Epic | 11 | 0.264 | 0.090 | 0.387 |
| Happy | 23 | 0.242 | 0.189 | 0.328 |
| Intense/Grand | 16 | 0.545 | 0.131 | 0.585 |
| Mysterious | 18 | 0.438 | 0.148 | 0.409 |
| Passionate | 19 | 0.702 | 0.156 | 0.604 |
| Playful | 21 | 0.624 | 0.172 | 0.566 |
| Powerful | 11 | 0.556 | 0.090 | 0.643 |
| Relaxing/Calm | 59 | 0.839 | 0.484 | 0.769 |
| Sad | 11 | 0.306 | 0.090 | 0.350 |
| Tense | 18 | 0.346 | 0.148 | 0.383 |
| Upbeat/Energetic | 22 | 0.611 | 0.180 | 0.655 |

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

Extraction et mesures : 56.43 s.
