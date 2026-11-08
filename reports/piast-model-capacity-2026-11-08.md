# Capacité non linéaire sur les mêmes indices MIDI

Exploratoire : les 1 900 clips avaient déjà été examinés. Aucun modèle promu.

| Modèle | Mysterious | Epic | Tense | Dark | Happy | Hard5 mAP | Noncalm14 mAP |
|---|---:|---:|---:|---:|---:|---:|---:|
| linear_votes | 0.310 | 0.438 | 0.438 | 0.453 | 0.349 | 0.398 | 0.495 |
| linear_unbalanced | 0.309 | 0.446 | 0.438 | 0.462 | 0.350 | 0.401 | 0.501 |
| additive_votes | 0.284 | 0.368 | 0.392 | 0.398 | 0.365 | 0.361 | 0.469 |
| interaction_votes | 0.291 | 0.404 | 0.403 | 0.417 | 0.372 | 0.377 | 0.499 |

Les prédictions hors pli, contrôles négatifs, résultats par pli et intervalles
par bootstrap de vidéos sont enregistrés dans les JSON associés.

## Verdict

**Ne pas retenir les arbres comme remplacement du modèle linéaire.**
Le modèle à interactions perd 0,024 d'AP moyenne sur les cinq humeurs contre
la logistique sans rééquilibrage ; IC95% par vidéos [-0,042 ; -0,002].
Il est moins bon dans quatre des cinq plis. Les interactions améliorent les
arbres additifs (+0,016), mais cela ne suffit pas à battre la référence.
Les contrôles aux votes mélangés donnent AP 0,123 / 0,106 / 0,148 / 0,120 /
0,157 pour Mysterious / Epic / Tense / Dark / Happy, proches des prévalences.
Ces intervalles restent conditionnels aux modèles ajustés et ne corrigent
pas la recherche répétée d'hypothèses sur ce corpus.

## Écart avec les rapports précédents : pas un nouveau gain

La référence équilibrée atteint ici 0,398, contre 0,386 dans le rapport
historique. Les partitions diffèrent : dans le premier pli, Happy compte
75 positifs contre 61 dans l'ancien découpage, et Dark 49 contre 57.
La méthode GroupKFold, le nombre de clips et la séparation par vidéo sont
les mêmes, mais pas l'affectation exacte aux plis. L'environnement a aussi
changé (Python 3.12 et scikit-learn 1.8.0 explicitement fixés ici).
La cause complète de la différence entre scores historiques n'est pas isolée.
**Ne pas présenter 0,393 → 0,401 comme une amélioration algorithmique.**
Les quatre bras de cette expérience partagent leurs observations et leurs
partitions ; leur comparaison interne reste interprétable.

Le manifeste `data/piast-capacity-folds-v1.json` enregistre désormais les
1 900 identités et leurs groupes/plis. Le script le rejoue indépendamment du
tri des égalités des bibliothèques. Un test compare exactement les plis aux
prédictions archivées, même après inversion de l'ordre des entrées, et
refuse cohortes incomplètes ou vidéo partagée entre entraînement et test.
Ce manifeste fixe cette expérience, pas rétroactivement les anciennes.

## Exécution et audit

- [Run complète réussie](https://github.com/leye0/AnaMu/actions/runs/42521960975),
  commit `63604fc78e278b0ae1a519efdcf246059441844f` : 1 900/1 900 extraits,
  aucun rejet, 1 896 vidéos, 117 observations, cinq plis, 500 bootstrap.
- `piast-model-capacity-2026-11-08.json` : scores, plis et intervalles complets.
- `piast-model-capacity-oof-2026-11-08.json.gz` : prédictions hors pli et
  contrôles négatifs, sans MIDI brut.
- Le rejeu par manifeste a été ajouté après cette run et vérifié contre les
  affectations réellement utilisées, sans refaire l'apprentissage.

Mysterious reste faible (0,309 contre 0,291 avec interactions). Cela ne
permet pas de choisir entre manque de timbre, erreur de transcription,
ambiguïté des annotations ou descripteurs inadéquats.
