# AnaMu S1 — contrôle externe IDyOM sur les attentes humaines

**9 novembre 2026 · expérience exploratoire, résultats reproductibles.**

## Question, provenance et cible

Nos proxies fondés sur le contour font-ils aussi bien qu'un prédicteur
statistique de mélodie **déjà calculé par un chercheur tiers** ?

La [thèse *Modelling Pitch Expectation in Melody*](https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation)
(commit `e9eb23384393c83de97e1a69d00133ae4673c425`) a elle-même comparé
IDyOM à un Music Transformer dans les expériences de Cuddy–Lunney (1995) et
Schellenberg (1996). Nous n'avons donc **pas découvert cette comparaison
scientifique pour la première fois** : nous l'intégrons comme *référence
indépendante à la bibliothèque de prédicteurs d'AnaMu* avec le même contrôle
des hauteurs, des unités et des partitions que nos autres essais.

- **Étiquette humaine** : note candidate jugée bonne ou mauvaise pour
  poursuivre une mélodie, moyenne de 20 auditeurs, huit fragments × 15
  notes, 120 valeurs dans `schell96.data`. Pas une émotion.
- **Entrée IDyOM** : probabilités précalculées et archivées par la thèse,
  notamment `schellenberg_idyom_selected_probe_probs.csv` ; **l'algorithme
  IDyOM original n'a pas été exécuté par AnaMu**. Son fichier de sortie `.dat`
  original, le corpus et les éventuels chevauchements d'apprentissage ne
  sont pas disponibles/vérifiés dans la révision inspectée.
- **Entrée proxy AnaMu** : mêmes 120 notes, modèles appris **uniquement sur
  les moyennes de Cuddy** ; leurs caractéristiques décrivent les deux
  dernières notes, alors qu'IDyOM peut utiliser le contexte de la mélodie.
  La quantité d'information accessible **n'est pas contrôlée** entre familles.
- **Contrôle d'alignement** : les 120 notes du classeur source XLSX concordent
  avec les 120 notes candidates reconstruites indépendamment à partir des
  fichiers MIDI et de la gamme ; les huit lignes et 15 colonnes de chaque
  tableau de probabilités sont contrôlées. Aucune note C6 artificielle de
  fin n'est prise pour une observation réelle du contexte.
- **Métrique** : Spearman calculé séparément par fragment (classement
  des 15 candidates), puis moyenne des huit. Une probabilité n'est *pas*
  une note humaine 1–7, donc ni R² direct ni « pourcentage de justesse ».

## Résultats en conditions **non équivalentes** (à ne pas traiter comme duel juste)

| Prédicteur | Spearman moyen 8 fragments | Statut |
|---|---:|---|
| Profil moyen de hauteurs de Cuddy | 0,560 | Référence source seulement |
| Proximité mélodique | 0,679 | Proxy entraîné sur Cuddy |
| **Contour mélodique** | **0,770** | Meilleur proxy transféré dans le test précédent |
| Profil + correction contextuelle | 0,650 | Proxy entraîné sur Cuddy |
| **IDyOM cpitch archivé** | **0,852** | Probabilités externes, réglages non reproduits |
| IDyOM « optimal viewpoint » | 0,894 | Variante secondaire, choix du point de vue non audité |
| IDyOM cpint/cpintfref | 0,739 | Variante secondaire, autre représentation |

Le cpitch fait **+0,081** de Spearman moyen face au contour, mais gagne
seulement **5 fragments sur 8**. Bootstrap apparié par *fragment*, 5 000
rééchantillonnages, intervalle exploratoire 95 % **[-0,004 ; +0,180]**.
Cet intervalle inclut zéro : aucune supériorité démontrée face au contour.

Face au profil moyen des hauteurs seul, cpitch gagne **8 sur 8**, différence
**+0,292**, intervalle **[+0,158 ; +0,443]**. Il s'agit d'un signal que la
mémoire statistique et/ou le contexte étendu sont importants, pas d'une
preuve causale du mécanisme qui produit le gain.

Sur les **huit contextes Cuddy** (8 × 25 sondes), les probabilités IDyOM
cpitch archivées ont une concordance moyenne **0,845** avec les moyennes
humaines. **Ne pas** mettre ce chiffre face à la validation leave-one-
context-out de nos proxies comme s'il s'agissait du même protocole : le
modèle IDyOM a été préparé ailleurs et la provenance de son corpus reste
inconnue.

## Conséquences pour la recherche AnaMu

1. Il existe de l'information réelle dans la **prédiction probabiliste des
   notes** qui ne se réduit pas au simple intervalle/contour, et AnaMu a
   maintenant une référence externe et des tests reproductibles.
2. Le changement de variante IDyOM affecte fortement les résultats
   (**0,739 à 0,894**) ; sélectionner après coup celle qui maximise les
   réponses humaines risquerait un biais. Garder cpitch comme référence
   préannoncée et les deux autres comme analyses secondaires descriptives.
3. La prochaine vraie intégration requiert soit **l'exécution autonome**
   d'IDyOM à version/corpus/paramètres gelés, soit un modèle probabiliste
   entraîné sur corpus explicite et évalué sur des mélodies non vues.
4. À terme, tester **l'émotion** demande une source indépendante annotée
   en émotion, et, pour « mystérieux », idéalement un véritable *audio*
   contenant les timbres/enveloppes. Aucune des corrélations ci-dessus ne
   mesure ce sentiment.

## Reproduire

```bash
git clone https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation.git ../melodic_expectancy_thesis
git -C ../melodic_expectancy_thesis checkout e9eb23384393c83de97e1a69d00133ae4673c425
python -m pip install numpy scipy scikit-learn mido
python -m unittest tests.test_research_contracts tests.test_idyom_archive tests.test_schellenberg_transfer
PYTHONPATH=. python -m scripts.idyom_archived_probe_comparison \
  --source ../melodic_expectancy_thesis \
  --output reports/idyom-archived-probe-comparison-2026-11-09.json
```

Le script et les tests utilisent Python standard pour lire les colonnes
numériques du XLSX. Les CSV de réponses humaines et de probabilités ne sont
pas incorporés ni redistribués par AnaMu. Le rapport stocke des **scores
agrégés** et les preuves de correspondance, pas les observations brutes.
