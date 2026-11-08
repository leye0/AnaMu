# AnaMu — nouveaux tests humains MIDI : les cas difficiles d'abord

Date : 8 novembre 2026. **Statut : recherche exploratoire vérifiable ; aucun
gain déployé dans le modèle PIAST.** Le but est de tester des mécanismes
académiques sur des émotions **annotées par des humains**, avec MIDI uniquement.
Ni décodage audio ni reconnaissance d'émotion sur enregistrements sonores.

## 1. Ce qui est réellement nouveau

| Corpus | Véritable cible humaine | MIDI analysable | Pertinence et limites |
|---|---|---|---|
| **IsoVAT (Plut et al., 2022)** | Ordres de tension, valence et activation évalués par des auditeurs | **90** extraits de 4 mesures, 30 triplets | 10 triplets *Tension* seulement ; 11/30 ordres humains ne reproduisent pas exactement l'intention du compositeur |
| **CP-WTC (Ching & Widmer, 2026)** | **7 652** évaluations perçues de valence/activation | **288** interprétations transcrites, 48 œuvres × 6 pianistes | Comparer des interprétations d'une même composition, donc aucune victoire possible par sa seule tonalité ; MIDI issu de transcription automatique, source audio évaluée par les humains |
| **PercePiano (Park et al., 2024)** | 19 axes évalués par des **pianistes experts** | **1 189** entrées annotées ; **1 072** interprétations humaines exploitables après exclusion de 116 exécutions « Score » et d'un MIDI manquant | Axes **sombre**, **dramatique/expressif**, **imaginatif** : directement utiles aux faiblesses ; ne sont *pas* les mêmes étiquettes que PIAST Dark/Epic/Mysterious |

Les corpus restent chez leurs auteurs, hors de ce dépôt. Les scripts ne
téléchargent rien ni ne reproduisent les fichiers tiers. Les annotations
humaines concernent **l'écoute de musique**, et non une émotion prouvée
« ressentie » par chaque auditeur au moment de jouer un MIDI.

### Sources primaires et provenance

- IsoVAT : [publication originale, Plut et al.](https://transactions.ismir.net/articles/10.5334/tismir.120), [MIDI](https://github.com/CalePlut/IsoVAT_Dataset). **Vérité terrain :** colonne *Aggregate G-T Order* du Tableau 8, pas les niveaux H/M/L voulus par les compositeurs.
- Herremans & Chew (2016) : [*Tension Ribbons* (manuscrit institutionnel)](https://qmro.qmul.ac.uk/xmlui/bitstream/handle/123456789/11798/Herremans%20Tension%20ribbons%20Quantifying%202016%20Accepted.pdf?isAllowed=y&sequence=1) ; les mesures de *cloud diameter*, *cloud momentum* et *tensile strain* proviennent de la bibliothèque universitaire `partitura`, pas d'une réimplémentation renommée.
- CP-WTC : [données et instructions](https://github.com/CPJKU/The-CP-WTC-Dataset), [version Zenodo](https://zenodo.org/records/21693024), [*Learning to Predict Performance-induced Emotion Differences in Classical Piano Music*, Ching & Widmer (2026)](https://arxiv.org/html/2607.28876v1). Ce corpus annonce une licence **CC BY-NC-SA 4.0** ; vérifier les droits avant tout usage commercial.
- PercePiano : [*Piano performance evaluation dataset with multilevel perceptual features*, Park et al. (2024)](https://www.nature.com/articles/s41598-024-73810-0), [données officielles et indices des 19 axes](https://github.com/JonghoKimSNU/PercePiano).

## 2. IsoVAT — tension réellement perçue, et non tempo facile

Le script `scripts/isovat_tension_benchmark.py` teste **11 indices sans
paramètres ajustés sur IsoVAT** sur les dix triplets de tension. Les ordres
humains peuvent être inhabituels ; le triplet n°6 est **L → M → H**.

| Indice isolé | Ordres exacts / 10 | Paires correctes / 30 |
|---|---:|---:|
| Nombre d'attaques par seconde | 3 | 20 |
| Vélocité MIDI moyenne | 2 | 16 |
| Collision harmonique moyenne approximative | 2 | 18 |
| Tension Ribbon : diamètre tonal moyen | **6** | **24** |
| Tension Ribbon : diamètre tonal final | 5 | 22 |
| Tension Ribbon : strain moyen | 1 | 16 |

Le hasard uniforme donne en moyenne 1,67 ordre exact sur 10 et 15 paires sur
30. Un contrôle par **20 000 permutations des ordres humains**, tenant compte
de la **sélection du meilleur parmi les 11 indices**, donne p ≈ **0,0237**
pour le meilleur nombre d'ordres exacts et p ≈ **0,0186** pour les meilleures
paires. **Ce n'est pas une validation aveugle** : le tableau humain était
connu au moment de définir l'expérience et il n'y a que 10 triplets.
L'indice de collision est une heuristique d'intervalles MIDI, **pas** une
simulation physique de rugosité spectrale.

**Hypothèse qui mérite réplication :** la dispersion harmonique peut expliquer
la tension au-delà de l'attaque ou de la vitesse. On ne peut pas déduire de ce
résultat que l'étiquette PIAST *Tense* est résolue.

## 3. CP-WTC — même composition, différences de jeu

Le script `scripts/cp_wtc_relative_benchmark.py` s'inspire du **Delta-VA**
de Ching & Widmer (2026) : déviation de l'affect d'une interprétation par
rapport aux autres interprétations du même score. L'approximation de notre
propre modèle utilise 14 indices MIDI de dynamique, densité d'attaques,
variabilité du temps, durées et étalement d'accords. **Elle n'utilise pas
le codec aligné au score original**, ni le timbre ou l'audio.

Les **48 compositions** sont divisées en six groupes : aucune composition
testée ne figure dans l'entraînement. Le centrage des indices des six
interprétations d'une nouvelle composition est autorisé, mais **les étiquettes
de test ne sont jamais fournies à l'entraînement**.

| Tâche difficile | Tempo seul | Dynamique seule | 14 indices expressifs |
|---|---:|---:|---:|
| Activation, paires Δ≥10 points | 262/339 = 77,3 % | 256/339 = 75,5 % | **269/339 = 79,4 %** |
| Valence, paires Δ≥1 point | 128/193 = 66,3 % | 72/193 = 37,3 % | **137/193 = 71,0 %** |
| R² des déviations d'activation | 0,223 | 0,241 | **0,366** |
| R² des déviations de valence | 0,027 | -0,034 | **0,119** |

Le gain de **R² par rapport au tempo seul**, avec bootstrap groupé par œuvre,
est +0,143 en activation (intervalle exploratoire 95 % : **+0,040 à +0,244**)
et +0,092 en valence (**+0,001 à +0,173**). L'amélioration de précision
des paires seules est trop petite pour être déclarée certaine : intervalles
de **-3,8 à +7,8 points** (activation) et **-3,6 à +13,9 points** (valence).

**Limites importantes :** le MIDI est transcrit de versions commerciales
audio et peut introduire des erreurs de vélocité / durée ; les participants
ont évalué les œuvres d'un pianiste donné, si bien que des différences entre
groupes d'annotateurs peuvent être confondues avec des différences de jeu ;
48 œuvres restent un échantillon petit et stylistiquement homogène.

## 4. PercePiano — Dark, Dramatic, Imaginative évalués par des experts

Le script `scripts/percepiano_hard_benchmark.py` apparie les différentes
interprétations du **même extrait noté** (99 groupes, 1 072 MIDI joués par
des humains). Les 116 *Score* mécaniques sont volontairement exclus pour
ne pas gagner sur une différence triviale humain-versus-synthétique.
Une annotation sans MIDI correspondant est également exclue, explicitement.

On garde les paires où la moyenne humaine diffère d'au moins **un échelon
entier** sur l'échelle originale de 1 à 7 ; les intervalles incertains ne
peuvent pas gonfler la métrique principale. Validation croisée en 6 plis,
**groupée par extrait noté**. Les œuvres et variations parentes restent
toutefois apparentées, même d'un pli à l'autre : **ne pas appeler cela une
validation sur de nouveaux compositeurs**.

| Axe cible | Tempo | Dynamique | Régression 14 indices | Classement par paires difficiles |
|---|---:|---:|---:|---:|
| **Sombre** | 134/326 **41,1 %** | 186/326 **57,1 %** | 211/326 **64,7 %** | **222/326 = 68,1 %** |
| **Imaginatif** | 520/918 **56,6 %** | 599/918 **65,3 %** | 648/918 **70,6 %** | **652/918 = 71,0 %** |
| **Dramatique/expressif** | 647/1 232 **52,5 %** | 773/1 232 **62,7 %** | **812/1 232 = 65,9 %** | 802/1 232 **65,1 %** |
| Haut niveau d'énergie (*contrôle facile*) | 64,7 % | 77,2 % | 80,0 % | 80,0 % |

**Algorithme nouveau :** classificateur logistique *pairwise* (apprentissage
par différences `x_a - x_b`), entraîné seulement sur les paires d'un échelon
humain ou plus. Sa prédiction est un ordre, **pas** une intensité calibrée ;
il n'a donc pas de R² à présenter. Inspiré des travaux de classement relatif
en émotions musicales, mais **ce n'est pas** le réseau à perte RnC exact
de Ching & Widmer.

Gain du classement par paires **versus dynamique seule** :

- **Sombre +11,0 points**, bootstrap par extrait noté 95 % ≈ **+0,8 à +20,8**.
- **Imaginatif +5,8 points**, 95 % ≈ **+0,6 à +10,8**.
- **Dramatique +2,4 points**, 95 % ≈ **-1,0 à +5,6**.

Cependant, par rapport au **meilleur concurrent déjà disponible, la
régression à 14 indices**, le gain « sombre » n'est que **+3,4 points**
(intervalle **-3,6 à +10,3**) et « imaginatif » **+0,4 point** (intervalle
**-2,2 à +3,4**). Les deux contiennent zéro. La régression sombre a même
un **R² négatif (-0,012)** sur les notes moyennes centrées : l'ordre semble
moins difficile à récupérer que la magnitude. **Ne pas déclarer victoire.**

L'expérimentation et les intervalles sont exploratoires : nous avons
essayé le classement après avoir vu les premiers résultats ; ils ne
corrigent pas toute la recherche d'hyperparamètres, ni les dépendances
entre différentes variations d'une même œuvre.

## 5. Corpus et théories évalués mais non intégrés

- **EMOPIA / EMOPIA+ :** EMOPIA possède de vraies annotations humaines de
  valence/activation pour MIDI pop-piano, déjà connu d'AnaMu. EMOPIA+ étend
  les représentations et corrections de tonalité, **pas le nombre de labels
  émotionnels indépendants** : [EMOPIA](https://annahung31.github.io/EMOPIA/),
  [EMOPIA+](https://zenodo.org/records/13122742).
- **XMIDI :** 108 023 MIDI, annotations déclarées vérifiées par des
  experts ; **déjà répertorié** dans la feuille de route. Pas une découverte
  de cette session : [papier XMIDI](https://arxiv.org/abs/2501.08809).
- **Simin Yang et al., annotations temporelles :** 51 enregistrements piano,
  133 477 points humains, correspondance envisagée avec MAESTRO MIDI, **mais
  accès aux CSV restreint sur Zenodo**. On ne les a ni lus ni testés :
  [Zenodo](https://zenodo.org/records/8375588).
- **TenseMusic (2024) :** modèle académique intégrant des tendances de tension,
  fenêtres attentionnelles et mémoire, mais fondé sur des **indices audio**.
  Approche MIDI possible à tester, pas une implémentation fidèle sans son :
  [article original](https://pmc.ncbi.nlm.nih.gov/articles/PMC10798497/).
- **Zentner et al. (2008), GEMS :** 9 dimensions d'émotions musicales dont
  *tension*, *wonder*, *power* et *transcendence*, plus riche que valence
  binaire ; c'est une **taxonomie psychologique** et non une conversion
  automatique fiable des labels PIAST :
  [publication](https://pubmed.ncbi.nlm.nih.gov/18729581/).
- **Cheung et al. / cognition et sensorialité (2023) :** les attentes
  *cognitives* expliquent davantage de variance de surprise que les attentes
  sensorielles seules. Hypothèse MIDI : comparer incertitude de long contexte
  harmonique/rythmique et simple densité ; aucun gain expérimental encore
  établi dans ce rapport :
  [publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC10725761/).

## 6. Reproduction, interprétation et travaux restants

Installer les dépendances facultatives de recherche :

```bash
python -m pip install 'mido>=1.3,<2' 'partitura>=1.8,<2' \
  'scikit-learn>=1.5,<2' numpy

python -m scripts.isovat_tension_benchmark /chemin/IsoVAT_Dataset/MIDI/Tension \
  --output /tmp/isovat-result.json
python -m scripts.cp_wtc_relative_benchmark /chemin/The-CP-WTC-Dataset \
  --output /tmp/cp-wtc-result.json
python -m scripts.percepiano_hard_benchmark /chemin/PercePiano \
  --output /tmp/percepiano-result.json

python -m unittest discover -s tests -p 'test_relative_emotion_benchmarks.py' -v
```

Les scripts enregistrent métadonnées, protocoles, résultats et comparaisons,
mais **aucun MIDI tiers**. Un test complet local : **126 tests réussis,
1 ignoré, 16 sous-tests réussis**. Les tests unitaires nouvellement ajoutés
valident le traitement des MIDI et le blocage des scores entre plis, sans
faux fichiers d'émotions « humaines ».

### Priorités scientifiques suivantes

1. Réplication **aveugle** de la tension harmonique sur une autre collection
   de jugements humains de tension (notamment des items non utilisés lors du
   choix des 11 indices) ; ne plus ajuster sur les 10 triplets IsoVAT.
2. Sur PercePiano, tester un vrai **modèle ordinal/magnitude calibré** et
   une séparation **par œuvre entière** ; le 68 % actuel compare des scores
   et n'est pas transférable automatiquement au label PIAST *Dark*.
3. Étudier les confusions **Dark ↔ Imaginative ↔ Dramatic** et les trajectoires
   d'**incertitude → surprise → résolution**, suivant GEMS/ITPRA ; tester
   contre des labels difficiles exclusivement, jamais une moyenne sauvée par
   « calme ».
4. Pour PIAST, exiger un **nouveau lot de morceaux jamais consultés** avant
   d'annoncer un gain de précision par classe. L'ancien lot de 1 900 est
   maintenant exposé à de nombreux essais et n'est plus un test vierge.

**Conclusion :** trois nouveaux benchmarks humains MIDI fonctionnent.
La dispersion tonale et l'expressivité sont de bonnes pistes, le classement
sur différences fortes semble utile. L'efficacité sur **les cinq étiquettes
PIAST les plus faibles** demeure **non démontrée**.
