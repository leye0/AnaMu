# AnaMu — audit de la tentative Java sur les œuvres classiques longues

Exécution originale : [GitHub Actions 42445411162](https://github.com/leye0/AnaMu/actions/runs/42445411162), terminée avec succès au niveau CI. Une **run réussie ne signifie pas une couverture académique complète**.

| Œuvre | Extraits MIDI tentés avec jSymbolic original | Extraits réussis | Conclusion |
|---|---:|---:|---|
| Bach BWV 66.6 | œuvre complète | complète | jSymbolic original exploitable |
| Chopin, Mazurka op. 6 nº 2 | 5 | **1/5**, mesures 65–72 uniquement | **partiel, insuffisant** |
| Bach BWV 140.7 | œuvre complète | complète | jSymbolic original exploitable |
| Mozart, Sonate K. 545 (exposition) | œuvre complète | complète | jSymbolic original exploitable |
| Beethoven, Quatuor op. 18 nº 1, mouvement 3 | 10 | **1/10**, mesure 145 uniquement | **partiel, insuffisant** |

Les autres 13 extraits de Chopin et Beethoven ont dépassé la limite d'exécution Java par extrait. Le MIDI écrit de Beethoven contient également 28 événements `note_off` sans contrepartie et 28 `note_on` non clos, exclus et comptabilisés par l'outil de découpage.

**Correctif de transparence :** désormais, AnaMu retourne `partial:1/5_original_java_segments` et `partial:1/10_original_java_segments`, plutôt que de déclarer `ok` lorsqu'un seul extrait a produit des résultats. Il compte aussi les mesures réellement couvertes et la moyenne des caractéristiques effectivement observées par mesure ; le simple nombre de colonnes présentes quelque part dans l'œuvre surestimait la couverture.

Les trajectoires émotionnelles de cette tentative ne remplacent **pas** le rapport publié antérieurement sur les cinq œuvres. Celui-ci garde les résultats et leurs limites vérifiés, sans déguiser les trous temporels en véritables analyses.

**Décision :** suspendre les longues tentatives Java sur ces deux œuvres. Revenir à l'objectif prioritaire : améliorer les analyses d'émotions sur un corpus annoté par des humains, en distinguant les vrais moteurs académiques des approximations et des lacunes.
