# Capacité du modèle sur les mêmes observations MIDI

Protocole fixé avant calcul des résultats de cette expérience, 8 novembre 2026.
La cohorte PIAST entière a déjà été explorée : aucune confirmation indépendante.

Hypothèse : les associations non linéaires entre indices musicaux disponibles
limitent le classement des émotions difficiles. Aucun nouveau descripteur,
aucun audio et aucune recherche d'hyperparamètres.

- Même extraction H1 + distribution tonale, mêmes 1 900 clips et cinq plis
  séparés par vidéo que l'expérience des votes fractionnaires.
- Référence : régression logistique existante sur votes fractionnaires.
- Référence supplémentaire : logistique sans rééquilibrage, meilleure dans
  la dernière run de calibration (Hard5 AP 0,393), lue avant cette expérience.
  Les gains du candidat seront comparés à cette référence plus forte.
- Témoin non linéaire additif : boosting de souches (profondeur 1).
- Candidat : même boosting, profondeur 3, interactions permises.
- Boosting fixé : erreur quadratique sur fractions de votes, 150 itérations,
  taux .05, au moins 30 observations par feuille, régularisation L2=5,
  aucun arrêt anticipé ni choix à partir des plis évalués.
- Cible d'évaluation inchangée : majorité de deux experts sur trois.
- Critère principal : moyenne AP des cinq émotions difficiles ; publier
  aussi les 14 noncalm, chaque émotion et les cinq plis. Mysterious reste
  dans le critère principal même si sa dépendance au timbre est plausible.
- Contrôle négatif : votes d'entraînement mélangés pour les cinq cibles,
  vérité du pli test inchangée. Incertitude par bootstrap des vidéos.
- Exporter les prédictions hors pli pour rendre les comparaisons auditables.

Une hausse mesure la capacité prédictive de ces observations sur ce corpus,
pas une preuve de mécanisme musical causal. Une absence de hausse ne prouve
pas que le timbre est la cause : il faudrait une comparaison MIDI/audio sur
les mêmes extraits pour l'établir. Aucune promotion automatique du candidat.

## Correction de provenance après exécution

Même stratégie de cinq plis, mais affectations différentes des rapports
historiques : voir le rapport de capacité. Le manifeste des identités de
cette run est désormais figé et rejoué ; aucun gain entre anciennes et
nouvelles partitions ne doit être attribué au modèle.
