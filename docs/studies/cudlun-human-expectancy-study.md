> **Étude de validation à cible précise.** Ses mesures sont utiles à la
> conception de la grammaire ; elles ne valident pas une couche G2–G6.

# AnaMu S1 — attentes mélodiques mesurées par des auditeurs

**8 novembre 2026. Exploration ; ne constitue pas une validation indépendante.**

## Un nouveau phénomène : la plausibilité de la note suivante

Nous changeons de cible, plutôt que de reproduire le chantier des cadences.
L'expérience de [Cuddy et Lunney (1995)](https://doi.org/10.3758/BF03213071)
demande à **24 personnes** (12 musiciens, 12 non-musiciens) de noter de 1 à 7
la qualité d'une troisième note après un début mélodique de deux notes.
Huit intervalles initiaux (2, 3, 9 et 10 demi-tons, montants et descendants)
et 25 continuations par intervalle donnent **200 couples contexte–note** et
**400 moyennes publiées** (une moyenne par groupe d'auditeurs). Ce ne sont
pas 400 réponses individuelles disponibles.

Les quatre tableaux de l'Appendice de l'article original donnent les
moyennes **et leurs erreurs-types**. Le projet de mémoire universitaire
[yiannisem/MSc-Thesis---modelling-pitch-expectation](https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation)
en fournit une transcription `cudlun95.data` ainsi que des contextes MIDI
reconstitués (révision **`e9eb23384393c83de97e1a69d00133ae4673c425`**).
Les premières valeurs ont été recoupées avec les tableaux originaux :
major second ascendant 3,58 / 2,75, puis 2,08 / 2,25, etc.

**Limite cruciale de fidélité :** dans le protocole de 1995, les participants
entendaient des versions finissant sur **do4 ou fa♯4**. La reconstruction
MIDI du mémoire place tous les contextes sur **fa♯4**. Les annotations sont
regroupées par intervalle et hauteur *relative* ; AnaMu ne peut ni attribuer
une transposition exacte à chaque participant, ni prétendre reproduire le son
du synthétiseur « wood piano » utilisé dans l'expérience.

## Protocole reproductible

- Seules les **deux premières notes MIDI** composent le contexte. Le fichier
  contient une troisième note égale à la deuxième comme *placeholder* :
  elle n'est **jamais utilisée comme information prédictive**.
- On calcule 25 notes candidates, de −12 à +12 demi-tons relativement à la
  deuxième note ; leur hauteur candidate est une donnée d'entrée valide.
  Les scores humains ne servent pas à construire les caractéristiques.
- Réponse évaluée : moyenne des deux moyennes de groupe (poids égal des
  12 musiciens et 12 non-musiciens). Corrélations séparées pour chaque groupe.
- **Référence dure :** pour la position relative de chaque note, moyenne des
  scores obtenus dans **les contextes d'entraînement seulement** ; elle ne
  tient aucun compte de la première note.
- Proximités et contours simplifiés inspirés de Narmour/Schellenberg et
  profils de tonalité Krumhansl–Kessler, estimés par régression Ridge avec
  `alpha=10` fixé dans le code. **Ce ne sont pas les équations des auteurs.**
- Modèle combiné : apprendre uniquement la **correction résiduelle** de cette
  référence selon le contexte mélodique. La référence du pli est recalculée
  exclusivement avec ses données d'entraînement.
- Validation principale : huit plis, chacun excluant intégralement un des
  huit contextes. Deux contrôles complémentaires excluent successivement
  un intervalle de même taille *dans ses deux directions* (quatre plis),
  puis toutes les mélodies d'une même direction (deux plis).
- Incertitude : bootstrap apparié des **huit contextes-stimuli**, pas des
  200 lignes. **Les mêmes 24 personnes ont évalué plusieurs contextes** :
  l'intervalle décrit la variation entre stimuli, pas une incertitude
  interparticipants (votes individuels indisponibles).

## Mesures réellement obtenues

| Méthode | ρ de Spearman moyen sur les 8 contextes | R² prédictions hors contexte | Gain en ρ sur la référence |
|---|---:|---:|---:|
| Référence relative de note, sans première note | **0,724** | **0,577** | — |
| Simple proximité de hauteur | 0,522 | 0,208 | −0,202 |
| Contour / retour / intervalle (proxy) | 0,608 | 0,333 | −0,116 |
| Contour + hiérarchie tonale (proxy direct) | 0,733 | 0,473 | +0,009 |
| **Référence + correction contextuelle résiduelle** | **0,795** | **0,643** | **+0,071** |

La correction résiduelle améliore la corrélation sur **8/8 contextes** ;
bootstrap exploratoire **par contexte-stimulus**, sans correction pour
la dépendance entre réponses d'un même auditeur, du gain en ρ :
**[+0,041 ; +0,101]**. La
corrélation moyenne atteint **0,734** chez les musiciens et **0,799** chez
les non-musiciens, contre respectivement 0,660 et 0,736 pour la référence.

| Groupes totalement exclus | Référence ρ | Correction ρ | Référence R² | Correction R² |
|---|---:|---:|---:|---:|
| Un contexte à la fois (8 plis) | 0,724 | **0,795** | 0,577 | **0,643** |
| Taille d'intervalle et deux directions (4 plis) | 0,763 | **0,809** | 0,621 | **0,655** |
| Toutes les mélodies montantes ou descendantes (2 plis) | 0,711 | **0,762** | 0,461 | **0,533** |

La **leçon négative** est aussi importante : empiler des caractéristiques
de théorie musicale directement dans un modèle ne suffit pas, et peut être
moins bon qu'un patron statistique banal. Il semble plus utile de séparer
la *préférence générale de note* de la *correction liée au mouvement du début*.

**Ne pas qualifier ce résultat de confirmé** : le modèle résiduel a été
formulé *après* lecture des scores des modèles directs sur les **mêmes huit
contextes** ; les intervalles bootstrap ne corrigent pas ce choix post-hoc.
Les trois schémas de séparation ne constituent pas trois corpus indépendants.
La tâche est la plausibilité d'une continuation, pas l'émotion « mystérieuse »,
la surprise acoustique, ni l'attente pendant une véritable œuvre longue.

## Exécuter et auditer

Sans versionner le corpus d'autrui :

```bash
git clone https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation.git ../melodic_expectancy_thesis
git -C ../melodic_expectancy_thesis checkout e9eb23384393c83de97e1a69d00133ae4673c425
python -m pip install numpy scipy scikit-learn mido
python -m scripts.validate_research_contracts
python -m unittest tests.test_human_probe_expectancy tests.test_research_contracts
PYTHONPATH=. python scripts/cudlun_probe_benchmark.py \
  --source ../melodic_expectancy_thesis \
  --output reports/cudlun-human-expectancy-2026-11-08.json
```

Le script refuse une révision amont différente. Le JSON publié conserve le
hash d'origine, les huit contextes et les scores de chaque pli. Aucun fichier
MIDI, vote individuel, ni extrait d'un enregistrement n'est ajouté au dépôt.

## Où chercher une confirmation *nouvelle*

1. **Hansen et Pearce (2014)** : [Predictive uncertainty in auditory sequence
   processing](https://doi.org/10.3389/fpsyg.2014.01052) teste 24 mélodies
   avec neuf notes-sondes chacune (216 stimuli) et **des jugements d'attente
   humaine**. Trouver et vérifier les réponses accessibles, puis geler la
   méthode S1 ci-dessus **avant** d'examiner ces valeurs.
2. **Ammirante et Russo (2023)** : [Vocal constraints model](https://doi.org/10.1177/20592043231179410)
   compare l'attente après des mélodies jouées ou chantées. Stimuli signalés
   sur [OSF](https://osf.io/y7zmt/) ; la disponibilité des **votes** n'a pas
   été vérifiée. C'est un bon test de la différence voix/instrument qu'un
   MIDI ne saisit pas.
3. **Zhang et al. (2024)** : [Melodic contour supersedes short-term
   statistical learning in expressive accentuation](https://doi.org/10.1371/journal.pone.0312883),
   [données et stimuli](https://github.com/haiqin-zhang/gestaltIC_melodies).
   Les CSV contiennent des identifiants Prolific, IP et métadonnées de
   navigateur : **ne pas les copier dans AnaMu**. Cible = accentuation
   expressive, **pas** continuation ni émotion.
4. **Hansen et al. (2021)** : [Predictive Uncertainty Underlies Auditory
   Boundary Perception](https://doi.org/10.1177/0956797621997349),
   [OSF](https://osf.io/aqku2/). Cible = pause/complétude de phrase, pas
   « mysterious ». Accès OSF non encore confirmé.

**Critère d'avancement S1 :** reproduire un gain positif, fixé à l'avance,
sur un **nouveau corpus de réponses individuelles ou moyennes d'auditeurs**
sans rechoisir les caractéristiques après lecture des labels ; préserver
les baselines, les unités indépendantes et les limites de MIDI. Seulement
après étudier si cette attente améliore les émotions difficiles de PIAST.
