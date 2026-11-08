# AnaMu — écart partition/interprétation : hypothèse, contre-épreuves et transfert

**Date :** 8 novembre 2026. **Verdict :** nouveau mécanisme expérimental
implémenté et testé sur deux corpus réellement annotés ; **pas de grand gain
validé**, donc **aucune modification du moteur émotionnel de production**.

## 1. Hypothèse académique traduite en algorithme

Les travaux [PercePiano (2024)](https://www.nature.com/articles/s41598-024-73810-0)
et [Delta-VA / CP-WTC (2026)](https://arxiv.org/html/2607.28876v1)
étudient l'interprétation *relativement* à une partition ou à d'autres
interprétations de la même œuvre. Nous testons l'idée suivante : **ce que le
musicien change par rapport à ce qui est écrit** porte davantage d'information
sur les émotions difficiles que les propriétés brutes du morceau.

`anamu/score_aligned_expression.py` calcule **14 variables à partir des MIDI** :

- micro-déviations temporelles et rubato par rapport aux durées écrites ;
- ralentissement final, contour temporel et ralentissement aux frontières ;
- accentuation et synchronisation de la note haute contre les voix graves ;
- rapport durée jouée/durée notée et ses corrélations avec la dynamique ;
- interaction entre densité écrite et accentuation par vélocité MIDI.

L'appariement est un couplage un-à-un des notes de même hauteur, à position
normalisée proche (`scipy.optimize.linear_sum_assignment`). Au moins 70 % des
notes comparables doivent être alignées et chaque écart de position retenu
doit être ≤ 12 % de la durée totale. **Ce n'est pas une reproduction du
`pyScoreParser` des auteurs**. La métrique d'alignement n'entre jamais dans le
prédicteur ; les interprétations rejetées sont imputées par la moyenne des
interprétations fiables du même extrait, sans consulter leur émotion humaine.

Les caractéristiques sont centrées parmi les exécutions d'une même partition.
Pour une œuvre totalement nouvelle, cela suppose que l'on possède aussi
plusieurs interprétations **non étiquetées**. C'est une restriction d'usage
explicite, pas un système capable de prédire n'importe quel MIDI isolé.

## 2. PercePiano : quatre œuvres parentes intégralement tenues à l'écart

**Corpus :** 1 072 interprétations humaines, 99 extraits notés et quatre
œuvres parentes (variations incluses). Les 1 072 contreparties de partitions
MIDI officielles ont été consultées ; 1 070 alignements ont franchi le seuil,
couverture médiane **99,22 %** parmi les alignements fiables. Deux sont
neutralisés avec audit des identifiants :

- `Beethoven_WoO80_var25_8bars_19_14` : couverture 45,8 % ;
- `Schubert_D935_no.3_4bars_12_5` : couverture 67,7 %.

Validation **leave-one-entire-parent-work-out** : les interprétations d'une
œuvre parente absente de l'apprentissage sont évaluées par des comparaisons
où la moyenne humaine diffère d'**au moins un échelon de Likert entier**.
Même classificateur de classement par différences, mêmes paramètres.

| Axe humain difficile | 14 variables de référence | +14 variables partition | Contrôle partition mélangée |
|---|---:|---:|---:|
| **Dramatique / expressif** | **759/1 232 = 61,6 %** | **815/1 232 = 66,2 %** | 742/1 232 = 60,2 % |
| **Sombre** | **194/326 = 59,5 %** | **188/326 = 57,7 %** | 198/326 = 60,7 % |
| **Imaginatif** | **631/918 = 68,7 %** | **612/918 = 66,7 %** | 592/918 = 64,5 % |

Le gain brut de **+4,55 points** sur *Dramatique* est encourageant, mais
l'intervalle de bootstrap par **extrait noté** est de **−0,4 à +9,9 points**.
Il comprend zéro, et le regroupement par extrait sous-estime possiblement
la dépendance entre les variations de la même œuvre parente.
**51 des 56 paires nettes gagnées** sur Dramatic proviennent de la seule
œuvre `Schubert_D960_mv3` ; une œuvre recule. Donc aucune victoire générale.

### Sélection sans regarder les étiquettes des œuvres de test

Pour ne pas dégrader les deux autres axes, un sélecteur *imbriqué* choisit
`référence` ou `référence+partition` **par émotion**, en comparant les trois
œuvres d'entraînement laissées tour à tour à l'écart. Il exige **≥2 points**
de gain interne pour adopter la nouvelle branche ; la quatrième œuvre ne
participe jamais à la sélection.

| Axe | Sélection entraînement uniquement | Contrôle mélangé, même sélection |
|---|---:|---:|
| Dramatique | **764/1 232 = 62,0 %** | 759/1 232 = 61,6 % |
| Sombre | **188/326 = 57,7 %** | 193/326 = 59,2 % |
| Imaginatif | **631/918 = 68,7 %** | 631/918 = 68,7 % |

**Le gain brut +4,55 points ne survit donc pas à une sélection applicable
sans connaître l'œuvre test.** Les quatre œuvres parentes ne suffisent pas
pour apprendre des règles fiables de sélection par émotion.

Exécution reproductible, après acquisition du corpus officiel :

```bash
python -m scripts.percepiano_pulse_hypothesis /chemin/PercePiano \
  --feature-pack score --cache /tmp/anamu-percepiano-score-cache.json \
  --output /tmp/anamu-percepiano-score-result.json
```

## 3. Transfert indépendant CP-WTC : 48 œuvres de Bach × 6 pianistes

**Corpus :** 288 MIDI d'interprétation, 48 œuvres différentes ; partition
MusicXML fournie par les auteurs pour chaque pièce. Seules les **huit premières
mesures** sont comparées, correspondant à la fenêtre évaluée par les auditeurs.
Les notes du MusicXML sont converties en événements symboliques par `music21` ;
**aucun enregistrement sonore n'est lu** par ce code. Cependant, les auteurs
ont produit les MIDI d'interprétation par transcription audio : c'est une
limite de fiabilité de la vélocité et des attaques.

Les 48 œuvres sont séparées en **6 plis groupés par composition**. Les valeurs
humaines sont des déviations intra-composition en activation et valence. Les
paires faciles/ambiguës sont éliminées : activation Δ≥10, valence Δ≥1. Le
prédicteur Ridge, la régularisation et les plis restent identiques.

**Audit :** 282/288 alignements fiables, couverture médiane **89,73 %**.
Les **6 interprétations** de la pièce 05 ne passent pas le seuil (sur un
exemple, 67 notes écrites et 103 notes transcrites, couverture 47,8 %) et
sont neutralisées à l'intérieur de cette œuvre. Il faudra examiner un
éventuel décalage de transcription/mesure avant d'en tirer un signal négatif.

| Tâche exigeante | 14 variables originales | 14 partition seules | 28 variables combinées | Partition mélangée + originales |
|---|---:|---:|---:|---:|
| Activation, paires Δ≥10 | **269/339 = 79,4 %** | 239/330 = 72,4 % | **278/339 = 82,0 %** | 273/339 = 80,5 % |
| Valence, paires Δ≥1 | **137/193 = 71,0 %** | 127/193 = 65,8 % | **137/193 = 71,0 %** | 134/193 = 69,4 % |
| R² activation (déviations) | **0,366** | 0,130 | **0,365** | 0,314 |
| R² valence (déviations) | **0,119** | 0,074 | **0,087** | 0,067 |

Le supplément de partition donne **+2,65 points** d'activation difficile
contre les 14 variables originales, bootstrap par composition :
**[−0,31 ; +5,63 points]**. Il ne donne que **+1,47 point** contre le
**contrôle de partition mélangée**, bootstrap **[−2,87 ; +5,62 points]**.
Aucune différence n'est actuellement assez robuste pour une adoption.
La valence difficile **ne progresse pas** ; son R² baisse de 0,119 à 0,087.

Diagnostic par œuvre en activation : **11 améliorées**, **4 dégradées**,
**33 inchangées**, avec au plus trois paires nettes gagnées pour une œuvre.
Pour la valence : **11 améliorées**, **10 dégradées**, **27 inchangées**.
L'effet est donc faible et dispersé sur 48 œuvres, pas un effet démontré.

Exécution reproductible :

```bash
python -m scripts.cp_wtc_score_alignment_benchmark /chemin/The-CP-WTC-Dataset \
  --cache /tmp/anamu-cp-score-cache.json \
  --output /tmp/anamu-cp-score-result.json
```

## 4. Décision de recherche et vraie faiblesse à attaquer

1. **Conserver le moteur existant.** La branche expérimentale peut évoluer,
   mais on ne promeut pas une hausse rétrospective concentrée sur une œuvre.
2. **Ne pas optimiser Calm, High Energy ni tempo rapide.** Ces catégories
   peuvent avoir de forts scores sans démontrer une compréhension de *Dark*,
   *Mysterious*, *Epic* ou de la valence ambiguë.
3. **Ajuster l'alignement avant d'ajouter plus de variables.** La pièce 05 de
   CP-WTC, les notes ornementales non correspondantes, la pédale et les
   décalages temporels locaux doivent être audités en premier.
4. **Chercher plus d'œuvres *indépendantes* pour les trois axes difficiles.**
   Les 99 extraits de PercePiano ne constituent pas 99 unités indépendantes :
   ce sont seulement **4 œuvres parentes**. Une nouvelle expérience doit
   expliciter son unité d'indépendance.
5. **Accepter toute divergence algorithmique prouvée meilleure.** La fidélité
   à une théorie publiée n'est pas le critère de réussite ; le critère est
   une performance sur étiquettes humaines, pour les axes difficiles,
   *hors œuvre*, au-delà des modèles simples et d'un témoin mélangé, sans
   consommation d'audio.

**À éviter :** annoncer 66,2 % comme le score du « modèle AnaMu » alors que
la sélection réalisable hors test ne fournit que 62,0 %, ou mélanger les
catégories PercePiano/CP-WTC avec les 16 étiquettes PIAST sans calibration.

Le code, les résultats dérivés et les tests restent séparés des données
sous licence des auteurs. Les analyses ci-dessus sont exploratoires ; les
intervalles ne corrigent pas la sélection successive des hypothèses.
