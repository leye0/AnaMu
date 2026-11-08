# Tension : la performance sur les humeurs DIFFICILES, pas Calm

- 1900 MIDI analysés, dont 78 tests encore jamais vus (groupes des premiers 1400 exclus).
- {'train': 1331, 'validation': 274, 'test': 295} ; aucun rejet : True.
- **Cible primaire fixée d'avance** : Mysterious, Epic, Tense, Dark, Happy,
  cinq dernières AP de validation sur l'expérience précédente (1400 MIDI).
- Seconde mesure : les 14 étiquettes sans Emotional ni Relaxing/Calm.
- Une troisième moyenne incluant Calm n'est présentée que pour détecter les illusions de progrès.
- Tous les modèles gardent le même découpage et le même classificateur ;
  toutes les variantes étaient définies avant de mesurer le nouveau test.

| Variante | Hard 5 validation | Hard 5 test nouveau | Noncalm 14 test nouveau | Avec Calm test nouveau (diagnostic) |
|---|---:|---:|---:|---:|
| H1 : indices physiques, aucune attente | 0.362 | 0.363 | 0.536 | 0.553 |
| H1 + surprise melodique seule | 0.358 | 0.344 | 0.525 | 0.543 |
| H1 + tendances de tension | 0.360 | 0.334 | 0.511 | 0.532 |
| H1 + tension sur mesures melangees | 0.337 | 0.297 | 0.502 | 0.522 |
| H1 + surprise + tendances de tension | 0.356 | 0.353 | 0.520 | 0.539 |

## Cinq humeurs-cibles, sur le nouveau test

| Humeur | Nombre de positifs | H1 AP | Tension AP | Surprise + tension AP |
|---|---:|---:|---:|---:|
| Mysterious | 13 | 0.403 | 0.334 | 0.361 |
| Epic | 6 | 0.313 | 0.221 | 0.306 |
| Tense | 11 | 0.330 | 0.349 | 0.379 |
| Dark | 9 | 0.255 | 0.258 | 0.304 |
| Happy | 12 | 0.514 | 0.507 | 0.416 |

**Garde-fous :** ne pas confondre AP et taux de bonnes réponses ;
vérifier le contrôle temporel mélangé ; ne pas annoncer de victoire
si un gain vient seulement de Calm, si la validation se dégrade,
ou si les cinq humeurs sont trop rares pour être évaluées.
Ces résultats ne prouvent ni causalité ni émotion ressentie.
