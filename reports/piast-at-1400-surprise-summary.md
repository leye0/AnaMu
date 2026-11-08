# PIAST-AT : est-ce que la surprise d'une note aide ?

- 1400 premières pièces MIDI disponibles, 850 déjà examinées auparavant.
- {'train': 987, 'validation': 196, 'test': 217}; test nouveau réellement exclu des groupes déjà vus : **94** extraits.
- Les mêmes humeurs humaines, mêmes partitions entraînement/test, même classificateur.
- Pour l'entraînement : calcul des surprises hors pli par groupe vidéo (aucune fuite).
- Pour le test : prior appris uniquement à partir des exemples d'entraînement.
- Les paramètres et les quatre variantes étaient fixés avant les scores du test.

| Variante | Validation AP | Test AP | Nouveau test AP |
|---|---:|---:|---:|
| H1 : indices perceptifs seuls | 0.512 | 0.484 | 0.474 |
| H1 + attente conditionnelle (ordre 3) | 0.502 | 0.504 | 0.502 |
| H1 + fréquence des notes, sans ordre (ordre 0) | 0.509 | 0.484 | 0.464 |
| H1 + attente sur notes mélangées (contrôle) | 0.501 | 0.494 | 0.483 |

**Interprétation :** seule une amélioration de la variante d'ordre 3
au-delà des deux contrôles (ordre 0 et notes mélangées) serait un signal
que la succession des notes fournit de l'information supplémentaire.
Une différence faible ou négative invaliderait l'intérêt pratique de
cette hypothèse *dans cette expérience*.

**Limites :** scores descriptifs; pas de test de significativité ni
d'émotions ressenties par les auditeurs. Le prior est un n-gramme
simplifié inspiré d'IDyOM, pas le vrai IDyOM.
