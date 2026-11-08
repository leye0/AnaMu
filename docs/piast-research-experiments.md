# PIAST-AT — hypothèses scientifiques à tester, pas « outils académiques »

**8 novembre 2026.** AnaMu cherche ici à comprendre quelles observations
symboliques sont réellement prédictives des **humeurs perçues**. Les
annotations PIAST-AT sont des jugements de trois experts sur 16 termes :
elles ne mesurent pas les émotions réellement *ressenties* par l'auditeur.
Genre et style sont exclus. L'accord de **deux experts sur trois** définit
les étiquettes positives. Aucun fichier audio n'est analysé.

## Une étude expérimentale précise → une hypothèse calculable

**Recherche principale.** [Micallef Grimaud & Eerola (2022), *Emotional
expression through musical cues: A comparison of production and perception
approaches*, PLOS ONE](https://doi.org/10.1371/journal.pone.0279605).
Les participants manipulaient notamment **mode majeur/mineur, tempo,
articulation staccato/legato, hauteur et dynamique** pour communiquer
différentes émotions. Les combinaisons et le contexte comptaient :
le résultat ne se réduit pas à « une note mineure implique la tristesse ».
L'étude portait sur des extraits instrumentaux manipulés ; elle **n'a pas
validé notre détecteur** sur PIAST-AT ni même les 16 mêmes étiquettes.

**Base perceptive du mode.** [Krumhansl & Kessler (1982), *Tracing the dynamic
changes in perceived tonal organization*](https://doi.org/10.1037/0033-295X.89.4.334).
L'algorithme expérimental utilise leurs profils de perception des 12 degrés
majeurs et mineurs, comparés à la distribution des notes réellement jouées.
Nous conservons deux degrés de confiance plutôt que d'imposer une tonalité
unique, possiblement fausse.

### Trois expériences identiques sauf pour les observations

| Essai | Ce que regarde le détecteur | Hypothèse testée |
|---|---|---|
| **H0 : référence** | 97 résumés de densité, registre, intervalles, durée, dynamique, harmonie et déroulement déjà disponibles | Les caractéristiques générales sont-elles déjà suffisantes ? |
| **H1 : indices issus de la recherche** | H0 + **mode probable**, tempo réellement joué, variations de tempo, durée des notes relativement à leurs suivantes, articulation staccato/legato estimée, évolution des nuances | Ces dimensions ajoutent-elles de l'information ? |
| **H2 : indices combinés** | H1 + mode × tempo, mode × articulation, tempo × articulation, mode × nuances, tempo × nuances, mode × variations de tempo | Les combinaisons sont-elles plus informatives que chaque indice isolé ? |

**Ce ne sont pas des coefficients empruntés à une publication.** Les équations
des six produits croisés ont été choisies ici comme hypothèses reproductibles,
*avant de comparer les variantes au test*. Les valeurs de tempo et les notes
sont extraites du MIDI seulement. L'articulation est approximée à partir du
rapport durée/inter-onset de la voix supérieure ; ce n'est pas une vérité
musicologique, et les pédales, accords et transcriptions peuvent la tromper.

Protocole : même classificateur linéaire, mêmes 16 catégories, mêmes morceaux,
mêmes groupes vidéo disjoints en entraînement (70 %), validation (15 %)
et test (15 %). La mesure choisie est la **précision moyenne du classement
(AP)**, confrontée à la fréquence de chaque émotion dans les données.
La moyenne principale exclut le terme générique `Emotional` ; toute catégorie
avec moins de trois exemples positifs dans le test est déclarée insuffisante.

Les 240 premiers extraits ont déjà été examinés lors du pilote. Le rapport
sur 850 pièces distingue donc un **test nouveau** qui exclut tous les groupes
vidéo de ces 240 morceaux, afin de ne pas masquer une régression par des
exemples déjà vus. Il ne s'agit pas d'une validation dans un autre corpus.

## Prochaines hypothèses indépendantes

1. **Attente et surprise :** [Egermann et al. (2013)](https://pubmed.ncbi.nlm.nih.gov/23605956/)
   ont relié des surprises mélodiques calculées probabilistiquement à des
   réponses psychophysiologiques et subjectives lors de concerts. Tester
   la surprise des continuations *avant chaque note*, ainsi que les
   accumulations et résolutions, contre un modèle dont l'ordre des notes est
   mélangé. Un lien éventuel avec les humeurs globales de PIAST ne reproduira
   pas leurs résultats temporels.
2. **Contexte appris et surprise :** [une étude de 2023 publiée dans
   *Philosophical Transactions B*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10725761/)
   trouve des contributions complémentaires d'attentes sensorielles et
   cognitives aux jugements de surprise/plaisir. Construire deux familles
   d'attentes symboliques et tester leur apport séparé. Il ne s'agit pas
   d'un modèle d'émotion prêt à l'emploi.
3. **Dynamique de la tension :** [Farbood (2012), *A Parametric, Temporal
   Model of Musical Tension*](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/f/11865/files/2020/08/Farbood_2012_Musical_Tension.pdf).
   Tester pentes, pics et relaxation des tensions sur une fenêtre glissante,
   plutôt qu'une moyenne de dissonance. Vérifier sur les labels humains
   si la temporalité apporte une information supplémentaire.

**Aucun de ces trois mécanismes supplémentaires n'est déclaré testé tant
qu'un vrai score d'ablation sur les données réservées ne le confirme.**

## Nouvelle expérience prédéfinie : surprise mélodique et incertitude

**Origine précise :** [Egermann, Pearce, Wiggins & McAdams (2013)](https://doi.org/10.3758/s13415-013-0161-y)
ont associé des violations des attentes mélodiques et des réponses
psychophysiologiques en concert ; [Cheung et al. (2019)](https://doi.org/10.1016/j.cub.2019.09.067)
étudient l'interaction surprise/incertitude dans le plaisir musical.
Ni l'un ni l'autre ne valide une prédiction de nos 15 adjectifs d'humeur
PIAST-AT. Le transfert à ce problème est **notre hypothèse à falsifier**.

Algorithme à tester : sur le MIDI polyphonique, prendre la note la plus
aiguë de chaque instant d'attaque comme *candidate* de mélodie, calculer les
intervalles successifs, puis apprendre des probabilités conditionnelles par
un petit modèle d'ordre variable jusqu'à trois intervalles précédents.
La **surprise** est `-log2 P(intervalle | contexte)` après l'arrivée de la
note. L'**incertitude** est l'entropie de cette distribution *avant* l'arrivée.
Leurs moyennes, fluctuations, extrêmes et évolutions temporelles forment
12 observations supplémentaires.

Trois contrôles étaient fixés **avant de regarder les nouveaux résultats** :

1. `research_cues` : H1 précédent, aucune surprise (référence).
2. `research_surprise` : H1 + surprise, entropie et variations d'ordre 3.
3. `research_surprise_unigram` : mêmes résumés mais probabilité d'ordre 0 ;
   mesure le bénéfice des fréquences, *sans* ordre des notes.
4. `research_surprise_shuffled` : probabilité d'ordre 3, mais ordre des
   intervalles mélangé de manière stable dans chaque morceau au moment du
   calcul ; la distribution des intervalles est préservée.

**Anti-fuite :** le prior musical est appris exclusivement sur le groupe
« entraînement », sans étiquettes d'humeur. Un exemple de cet entraînement
reçoit ses observations de surprise par *cross-fitting* en cinq plis :
aucune autre version du même groupe vidéo ne peut figurer dans son prior.
Validation et test reçoivent le prior appris sur la totalité de l'entraînement.
Tous les essais partagent la séparation groupes/labels et le classificateur
linéaire figé. La mesure principale reste l'AP moyenne des étiquettes
nommées, sur les morceaux précédemment inconnus.

**Résultat mesuré le 8 novembre 2026 :** les 1 400 MIDI sélectionnés ont
été téléchargés et contrôlés intégralement ; toutes les variantes ont
terminé avec 1 400 extraits analysés, distribués en 987 entraînement,
196 validation, 217 test. Dans le test, **94 extraits proviennent de groupes
vidéo absents des 850 pièces précédemment examinées**. Le lot et le
protocole sont identiques entre les quatre variantes.

| Modèle | Validation (196) | Test (217) | Nouveau test (94) |
|---|---:|---:|---:|
| H1 (sans surprise) | **0,512** | 0,484 | 0,474 |
| H1 + surprise conditionnelle d'ordre 3 | 0,502 | **0,504** | **0,502** |
| H1 + fréquences seules d'ordre 0 | 0,509 | 0,484 | 0,464 |
| H1 + surprise de notes mélangées | 0,501 | 0,494 | 0,483 |

Mesure : **AP moyenne de 15 humeurs nommées**, sans `Emotional`. Le modèle
conditionnel gagne **0,028 point d'AP** sur le nouveau test par rapport
à H1, **0,038** face au modèle sans ordre et **0,019** par rapport à
la version dont les notes sont mélangées. Sur les 15 humeurs, 10 montent
et 5 baissent. Les hausses les plus grandes sont `Epic` (+0,115 ; 8
positifs), `Powerful` (+0,082 ; 6), `Sad` (+0,078 ; 7), `Cute`
(+0,075 ; 5) et `Passionate` (+0,070 ; 12). Les baisses notables sont
`Tense` (−0,041 ; 8) et `Upbeat/Energetic` (−0,034 ; 15).

**Verdict prudent :** l'ordre des intervalles **semble** contenir un signal
utile sur les nouveaux morceaux, distinct de leur simple distribution.
Mais la validation se **dégrade** (0,512 → 0,502) ; sur seulement 94 tests
nouveaux, les termes rares sont instables. Il n'y a ni intervalle de
confiance ni preuve de significativité ou de causalité. L'algorithme
n'est **pas** déclaré validé au sens scientifique ; ce résultat oriente
la prochaine étude. Le compte rendu intégral et les scores par humeur
sont dans `reports/piast-at-1400-*`.

**Limites :** cette approximation n'est **pas** l'IDyOM original. La ligne
mélodique supérieure peut être fausse sur piano polyphonique ; la précision
des attaques dépend de la transcription. Le plaisir musical mesuré dans
une étude n'est pas synonyme des adjectifs d'humeur perçue par les experts.

## Expérience suivante : résoudre les échecs, sans se féliciter pour Calm

**Priorité exprimée par Léon le 8 novembre 2026 :** ne plus choisir nos
victoires en fonction de humeurs faciles, notamment `Relaxing/Calm`, déjà
à AP ≈ 0,91 sur le nouveau test précédent. Aucun nouveau score n'a été
regardé pour construire les critères qui suivent.

### Cibles fixées à l'avance, à partir de la validation précédente

Sur les 196 extraits de **validation** de l'expérience 1 400 (et non sur
les prochains extraits test), les cinq humeurs éligibles ayant la plus
faible AP étaient :

| Humeur-cible | Positifs dans l'ancienne validation | AP dans cette validation |
|---|---:|---:|
| `Mysterious` | 25 | 0,290 |
| `Epic` | 13 | 0,301 |
| `Tense` | 24 | 0,371 |
| `Dark` | 23 | 0,377 |
| `Happy` | 28 | 0,392 |

**Critère de succès prioritaire :** AP moyenne de ces **cinq** catégories
sur les groupes vidéo jamais vus, plus une seconde AP moyenne des **14
humeurs** spécifiques à l'exclusion de `Relaxing/Calm` et `Emotional`.
Pour chaque humeur, afficher aussi le nombre de positifs et son AP
individuelle. La moyenne des 15 humeurs incluant Calm n'est qu'un témoin
diagnostique : une amélioration portée uniquement par Calm ne compte pas.
Conserver en plus les cinq exemples notés les plus haut alors que le terme
n'a pas atteint deux votes, et les cinq exemples annotés positifs auxquels
le modèle donne les notes les plus basses. Ce sont des **désaccords de
classement**, pas des « faux positifs » cliniques ou des émotions prouvées.
La validation doit aussi aller dans le bon sens ; sinon le gain est
considéré instable. Trois positifs au minimum restent nécessaires pour
évaluer chaque humeur.

### Recherche, algorithme, ablations

**Étude primaire :** [Farbood (2012), *A Parametric, Temporal Model of
Musical Tension*](https://doi.org/10.1525/mp.2012.29.4.387).
Deux expériences avec jugements de tension continue montrent l'importance
de combiner des paramètres musicaux et surtout la **direction des tendances
dans une fenêtre d'attention**, avec une fenêtre de mémoire précédente.
L'étude précise que le signal d'attente mélodique n'avait pas de relation
directionnelle assez nette pour figurer dans le modèle final : cette piste
de tension est donc **distincte** de notre surprisal précédent.

Notre prototype prend cinq indices **déjà extraits du MIDI par mesure** :
dissonance verticale estimée, dynamique MIDI, fréquence des attaques,
proportion de syncopes estimées et étendue de registre. Nous les ramenons
sur des échelles physiques fixes, calculons les pentes de deux ou quatre
mesures et amplifions leur accumulation quand la fenêtre précédente évolue
dans le même sens. Nous résumons les montées persistantes, baisses,
inversions, excursions, chutes depuis le pic et relâchement final.

**Attention :** ce n'est PAS l'équation originale ni les poids appris
par Farbood ; ses fenêtres s'expriment en temps et non en mesures.
Ces substitutions sont explicites pour ne pas fabriquer un faux « outil
académique validé ».

**Variantes prévues avant tout test supplémentaire :**

1. H1 : indices physiques précédents sans surprise ni tension.
2. H1 + surprise mélodique : notre meilleur candidat précédent.
3. H1 + tendances de tension (mémoire et résolution).
4. H1 + tension des **mêmes mesures mélangées** (contrôle sans temporalité).
5. H1 + surprise mélodique + tendances de tension (complémentarité).

**Nouveau test protégé :** étendre l'échantillon déterministe de 1 400
à l'ensemble des **1 900 MIDI exactement appariés**. Le rapport distingue
les morceaux du test dont le groupe vidéo n'apparaissait dans **aucun
des 1 400 extraits précédemment examinés**. Les partitions restent
séparées par groupe ; les paramètres restent identiques. Une hausse sur
les 217 anciens tests n'est **pas** la preuve recherchée.

### Résultat réel — 8 novembre 2026, aucune victoire globale

Le workflow GitHub s'est terminé avec succès. Les **1 900 MIDI ont été
analysés sans aucun rejet** : 1 331 entraînement, 274 validation,
295 test. Dans ce dernier, **78 extraits de groupes vidéo n'appartenaient
à aucun des 1 400 précédemment examinés**. Les cinq étiquettes difficiles
avaient toutes au moins trois positifs dans ces 78 nouveaux extraits.

| Algorithme | Hard 5 validation | **Hard 5 nouveau test** | 14 noncalm nouveau test | Avec Calm (diagnostic) |
|---|---:|---:|---:|---:|
| H1 : indices physiques | **0,362** | **0,363** | **0,536** | **0,553** |
| H1 + surprise mélodique | 0,358 | 0,344 | 0,525 | 0,543 |
| H1 + tension temporelle | 0,360 | 0,334 | 0,511 | 0,532 |
| H1 + tension de mesures mélangées | 0,337 | 0,297 | 0,502 | 0,522 |
| H1 + surprise + tension | 0,356 | 0,353 | 0,520 | 0,539 |

Pour les cinq humeurs, la référence de fréquence seule est à **0,131**
d'AP moyenne. Une AP de 0,363 n'est pas un « 36,3 % de bonnes réponses ».

| Humeur | Positifs nouveaux | H1 AP | Tension AP | Surprise + tension AP |
|---|---:|---:|---:|---:|
| Mysterious | 13 | **0,403** | 0,334 | 0,361 |
| Epic | 6 | **0,313** | 0,221 | 0,306 |
| Tense | 11 | 0,330 | 0,349 | **0,379** |
| Dark | 9 | 0,255 | 0,258 | **0,304** |
| Happy | 12 | **0,514** | 0,507 | 0,416 |

**Verdict : hypothèse rejetée comme amélioration générale.** La tension
temporelle conserve davantage de signal que sa version mélangée, mais elle
ne dépasse pas le modèle simple. La combinaison surprise + tension donne
des pistes locales pour `Tense` et `Dark` (+0,049 d'AP chacun), aux dépens
des autres cibles. Cette observation est **postérieure au test** ; choisir
maintenant de n'activer ces indices que sur ces deux humeurs serait du
réglage sur le test et **ne prouverait rien** sans données indépendantes.
Le gain de surprise observé sur le précédent test nouveau (94 clips) ne
se généralise pas automatiquement à ce nouveau lot de 78 extraits.

Les JSON complets de `reports/piast-at-1900-*` conservent en outre, pour
chaque humeur, les cinq extraits positifs les plus mal classés et les cinq
extraits non annotés dans cette humeur les plus fortement classés. Cela
permet un audit qualitatif des erreurs, sans prétendre qu'une annotation
manquante signifie « émotion absente ».

**Direction suivante :** diagnostiquer les erreurs de catégories
particulières à partir de ces extraits et d'un nouveau jeu de données.
PIAST-AT a maintenant livré tous ses 1 900 MIDI appariés : **ne plus
revendiquer un nouveau test PIAST totalement inédit** après lecture de
ces résultats. Pour tester une spécialisation par humeur, obtenir une
évaluation réellement indépendante (autre corpus, nouvelle annotation,
ou protocole de validation croisée imbriquée explicitement exploratoire).

## Résultat observé — première hypothèse (8 novembre 2026)

Après avoir fixé les trois variantes ci-dessus, nous les avons exécutées
sur les **mêmes 850 MIDI** : 613 en entraînement, 115 en validation,
122 en test. Parmi les 122, **91 appartiennent à des groupes vidéo qui
n'avaient pas figuré dans le premier pilote de 240 pièces**.

Les 850 MIDI ont été lus sans refus. Les trois variantes partagent le
classificateur linéaire fixé à l'avance, les mêmes étiquettes humaines et le
même découpage. Moyenne d'AP des 15 humeurs spécifiques (hors `Emotional`) :

| Algorithme | Validation, 115 | Test complet, 122 | Nouveau test, 91 |
|---|---:|---:|---:|
| H0 : 97 observations générales | 0,490 | 0,452 | 0,528 |
| H1 : H0 + 10 indices perceptifs | **0,537** | **0,474** | **0,548** |
| H2 : H1 + 6 interactions | 0,538 | 0,468 | 0,539 |
| Référence par fréquence, sans musique | 0,166 | 0,169 | 0,178 |

**Bilan :** l'ajout des 10 indices H1 améliore le classement moyen de 0,020
point d'AP sur les 91 pièces nouvelles, mais ce n'est **pas** une preuve
statistique générale ni une validation de causalité. H2 est légèrement plus
faible que H1 sur les morceaux nouveaux malgré une validation supérieure :
**ne pas retenir une complexité supplémentaire uniquement parce qu'elle
améliore la validation.**

Sur le nouveau test H1 améliore `Bright` de +0,216 AP, `Dark` de +0,120,
`Cute` de +0,120 et `Tense` de +0,080 ; mais dégrade `Powerful` de −0,178,
`Intense/Grand` de −0,092, `Upbeat/Energetic` de −0,055. Le bilan ne
cache donc pas les régressions par émotion.

Rapports bruts et reproductibles :
[H0](../reports/piast-at-850-basic.md),
[H1](../reports/piast-at-850-research-cues.md),
[H2](../reports/piast-at-850-research-interactions.md),
et les mêmes noms en `.json`.

```bash
python -m scripts.fetch_piast_at /tmp/piast-at --limit 850
python -m scripts.piast_at_benchmark /tmp/piast-at --limit 850 --fresh-after 240 \
  --feature-set basic
python -m scripts.piast_at_benchmark /tmp/piast-at --limit 850 --fresh-after 240 \
  --feature-set research_cues
python -m scripts.piast_at_benchmark /tmp/piast-at --limit 850 --fresh-after 240 \
  --feature-set research_interactions
```

Le prochain test doit porter sur **les attentes et surprises mélodiques
apprises sans les labels** avec un véritable contrôle d'ordre temporel,
et non sur l'accumulation indiscriminée de variables.
