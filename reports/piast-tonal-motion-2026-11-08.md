# PIAST-AT : tonalité locale et humeurs difficiles — expérience exploratoire

**8 novembre 2026. Verdict : un signal positif « Dark » assez fort, mais
pas de gain général sélectionnable sans examen du test. Aucune promotion.**

## Hypothèse et statut scientifique

[Xia et al., AAAI 2026, *Let the Model Learn to Feel*](https://ojs.aaai.org/index.php/AAAI/article/view/37201)
montrent qu'une injection explicite de **mode** peut aider un encodeur
symbolique MIDIBERT sur EMOPIA et VGMIDI. Nous ne reproduisons **ni leur
réseau ni MoFi** : nous testons une autre hypothèse, plus locale.

**Hypothèse :** des passages dont la tonalité évolue vers le mineur,
devient ambiguë ou change de centre tonal peuvent mieux expliquer des
étiquettes humaines comme `Dark` et `Mysterious` que le seul mode moyen.

`anamu/tonal_motion.py` découpe les attaques de notes en huit fenêtres
temporelles. Pour chaque fenêtre, il compare son chroma pondéré aux
24 profils majeur/mineur de Krumhansl-Kessler (1982). Il résume **18
variables** : évidence mineure, confiance et ambiguïté des profils,
changements de tonique, changements majeur/mineur et chromatismes. L'entropie
est une approximation des corrélations, **pas une probabilité psychologique
validée de l'incertitude de l'auditeur**. Aucun fichier audio n'est analysé.

Deux variantes sont comparées au même classificateur linéaire fixé :

1. **H1** : 97 observations MIDI + 10 indices de mode, tempo, articulation ;
2. **H1 + trajectoire réelle** : H1 et les 18 variables tonales ;
3. **H1 + fenêtres mélangées** : H1 et les mêmes 18 variables après permutation
   des huit fenêtres d'un morceau ; les distributions de notes et la
   moyenne des caractéristiques par fenêtre sont conservées.

Le témoin permet de savoir si un gain provient de **l'ordre temporel** ou
simplement de davantage de résumé tonal.

**Cohorte :** les 1 900 MIDI exactement appariés de PIAST-AT, zéro rejet,
1 331 entraînement, 274 validation, 295 test, groupes vidéo disjoints.
Les 78 exemples de l'ancien sous-test « nouveau par rapport à 1 400 » ont
**déjà été examinés** dans notre étude précédente. Il n'existe plus de test
PIAST totalement neuf dans ce lot. Toutes les conclusions ci-dessous sont
donc **exploratoires**, malgré la séparation mécanique train/validation/test.

## Mesure principale : précision moyenne AP, pas taux de bonnes réponses

| Variante | 5 difficiles en validation | 5 difficiles ancien test (295) | 5 difficiles ancien sous-test (78) | 14 humeurs hors Calm ancien test |
|---|---:|---:|---:|---:|
| H1 (référence) | 0,362 | **0,352** | 0,363 | **0,498** |
| H1 + tonalité évolutive | **0,400** | **0,363** | 0,378 | 0,489 |
| H1 + fenêtres mélangées | **0,402** | 0,350 | **0,390** | 0,482 |

Le gain macro de +0,011 d'AP sur l'ancien test ne suffit pas à justifier
la nouvelle représentation : les 14 humeurs noncalm régressent.

### Où se trouve le signal ?

| Humeur (positifs / 295) | H1 AP | Trajectoire réelle AP | Mélangée AP |
|---|---:|---:|---:|
| **Dark (39)** | 0,344 | **0,455** | 0,386 |
| Mysterious (44) | **0,442** | 0,436 | **0,446** |
| Epic (25) | **0,378** | 0,367 | 0,351 |
| Tense (37) | 0,279 | **0,289** | 0,273 |
| Happy (45) | **0,319** | 0,268 | 0,296 |

Pour `Dark`, le gain brut est **+0,111 d'AP** contre H1, dont **+0,069
contre le contrôle temporel mélangé**. La validation suit le même ordre
en comparant à H1 (0,408 → 0,542), mais **l'ablation mélangée fait encore
mieux en validation (0,555)**. Sur le sous-test ancien de 78 exemples,
qui contient seulement **9 Dark positifs**, la trajectoire passe seulement
de 0,255 à 0,288 : l'effet est nettement moins convaincant.

**Il serait incorrect de conclure que le mouvement tonal est validé.**
Les caractéristiques de tonalité locale peuvent améliorer des cas `Dark`,
mais ni la robustesse, ni le choix du meilleur algorithme n'est acquis.

## Contrôle crucial : choisir sans regarder le test

Une règle simple prend pour chaque humeur **la variante ayant l'AP maximale
en validation**, sans utiliser les labels de test pour choisir.

| Humeur | Choix par validation | AP de l'ancien test |
|---|---|---:|
| Mysterious | Tonalité réelle | 0,436 |
| Epic | Fenêtres mélangées | 0,351 |
| Tense | Tonalité réelle | 0,289 |
| **Dark** | **Fenêtres mélangées** | **0,386** |
| Happy | Tonalité réelle | 0,268 |

**Moyenne de cinq AP : H1 = 0,352 → sélection par validation = 0,346.**
Donc la décision réaliste **régresse**, même si une des branches avait
atteint 0,455 sur `Dark` en regardant a posteriori les résultats du test.
Cette règle de choix est exécutable sans labels de test ; cependant le
chercheur a déjà inspecté les performances des trois modèles sur ces
295 exemples. Elle n'est **pas** une évaluation externe indépendante.

## Prochain protocole pour viser un vrai gain

1. **Ne pas optimiser seulement les cinq scores a posteriori.** Nous
   aurions besoin d'un nouveau lot d'annotations humaines, ou d'une
   validation par groupes répliquée strictement signalée exploratoire.
2. **Séparer structure tonale et mouvement** : la permutation garde
   beaucoup de performance en validation. Il faut isoler les informations
   qui viennent des profils locaux, de leur ambiguïté et de l'ordre de
   succession — avec un témoin distinct pour chacune.
3. **Mettre l'accent sur l'AP de `Dark` et ses 39 positifs, puis transférer
   à d'autres œuvres et styles**. Ne pas annoncer une victoire
   `Mysterious` ou `Epic` si ces étiquettes stagnent.
4. **Nouvelle source à examiner, pas un nouveau gold standard :**
   [TASTE (Yao et al., octobre 2026)](https://arxiv.org/abs/2610.15960)
   publie des labels et du MIDI symbolique à grande échelle (≈432 000
   morceaux, dont ≈9 949 dits « high-quality »), mais nombre de labels
   sont produits par des procédures automatiques ou du texte, et les
   émotions proposées ne recoupent pas `Dark` et `Mysterious`. Éventuel
   **pré-entraînement faible**, jamais validation humaine indépendante.

Exécution sur le corpus officiel (licence et provenance à respecter) :

```bash
python -m scripts.piast_tonal_motion_experiment /chemin/piast-1900 \
  --out /tmp/anamu-piast-tonal
```

La [CI GitHub de cette expérience](https://github.com/leye0/AnaMu/actions/runs/42508716152)
a terminé avec succès ; l'artifact conserve les scores JSON et la table
d'ablation, sans reproduire les MIDI des auteurs. Le
[résultat agrégé JSON](piast-tonal-motion-results-2026-11-08.json)
est également archivé dans le dépôt, sans identifiants individuels.
