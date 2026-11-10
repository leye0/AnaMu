> **Étude de validation à cible précise.** Ses mesures sont utiles à la
> conception de la grammaire ; elles ne valident pas une couche G2–G6.

# Des annotations rares, un test de mécanisme : cadences du DCML DLC

**Étude du 8 novembre 2026 — exploratoire, non confirmatoire.**

La question évaluée est précise : **les relations tonales entre notes nous
aident-elles à identifier les cadences où des musicologues ont marqué une
arrivée/résolution musicale ?** Elle ne porte **pas** sur `Mysterious`, `Epic`,
la valence, le ressenti de tension, le timbre ni la qualité d'une génération.

## Provenance, capacités, limites

Source universitaire principale : Hentschel, Rammos, Neuwirth et Rohrmeier,
*A corpus and a modular infrastructure for the empirical study of (an)notated
music*, *Scientific Data* (2025), DOI
[10.1038/s41597-025-04976-z](https://doi.org/10.1038/s41597-025-04976-z).
Le **Distant Listening Corpus** rassemble 1 283 partitions notées et
expertisées, avec 240 000 annotations d'analyse environ (tonalités, accords,
phrases, cadences), validées par des musicologues. Les données et le workflow
sont publics sur [DCMLab/distant_listening_corpus](https://github.com/DCMLab/distant_listening_corpus).

Sous-corpus effectivement examinés, récupérés directement depuis les dépôts
des auteurs :

| Sous-corpus | Partitions/mouvements | Révision figée |
|---|---:|---|
| [Chopin — Mazurkas](https://github.com/DCMLab/chopin_mazurkas) | 55 | `5931135e614985023b96de2a291c74b7ef90b287` |
| [Mozart — Sonates pour piano](https://github.com/DCMLab/mozart_piano_sonatas) | 54 | `5337257a5318711e6302cfe85c3f1a6ade3c6271` |
| [Bach — Suites anglaises/françaises](https://github.com/DCMLab/bach_en_fr_suites) | 89 | `9cd6d362ed8246ed8edfc425944862ed88ddf1a5` |

**Total : 198 fichiers appariés**, 121 051 événements candidats, **1 992
cadences humaines**, toutes alignées exactement avec un début de note de
ces scores ; aucun fichier écarté. L'effectif aléatoire d'une cadence parmi
ces événements est **1,646 %**. Cette couverture n'est pas une validation
de la justesse subjective des annotations : les analystes travaillent
dans une tradition harmonique occidentale.

**Nature des entrées :** les tableaux `notes/*.notes.tsv` fournissent des
hauteurs MIDI (`midi`), des durées et des positions en quarts de temps de
**partitions symboliques**. Ces fichiers ne sont pas des enregistrements
audio ni des performances `.mid` ; les mesures sont toutefois entièrement
compatibles avec les événements MIDI. Les colonnes des `harmonies/*.harmonies.tsv`
ne servent **qu'à lire la présence et la position de `cadence`**. Le modèle
ne consulte jamais leurs tonalités locales, accords, chiffres romains,
fin de phrases ou classifications de cadence. Le test qui permute ces
colonnes d'expertise sans changer les caractéristiques le vérifie.

**Licence :** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Nous distribuons **le code et les résultats, pas le corpus original** ;
son usage commercial demande une vérification de licence séparée.

## Protocole reproductible

1. Extraire chaque début de note comme candidat, sans consulter les positions
   des analyses expertes pour la sélection. Estimer la tonalité globale
   (profils majeurs/mineurs appliqués aux hauteurs et durées des notes), puis
   calculer chroma actuel/passé, basse et indices de relation dominante–tonique.
   L'estimation de tonalité est **offline** et peut exploiter les notes futures,
   mais **jamais** les annotations humaines ; une vraie prédiction en ligne
   nécessitera un second protocole.
2. Comparer **rythme seul**, **harmonie seule**, **rythme + harmonie** et
   **rythme + harmonie permutée à l'intérieur du même mouvement**. Même
   `StandardScaler` et régression logistique équilibrée, graine 19 ; aucun
   apprenant académique original ni poids publiés n'est revendiqué.
3. Validation `StratifiedGroupKFold` sur cinq plis, **par œuvre parente** :
   les mouvements `K279-*` de Mozart et `BWV806_*` de Bach ne peuvent pas
   apparaître des deux côtés. Les mazurkas sont des œuvres distinctes.
   En tout **85 œuvres parentes** ; 80 ont des classes positive et négative
   permettant de calculer une AP par groupe.
4. Test de transfert indépendant du découpage précédent : entraîner sur
   **deux compositeurs et prédire le troisième**, trois fois, sans entraîner
   sur une pièce du compositeur test.
5. Mesure principale : `average_precision` (AP, utile pour une prévalence
   de 1,646 %). Rapport annexe : AP moyenne par œuvre parente et intervalle
   à 95 % de différence appariée, **rééchantillonnage des œuvres parentes**
   (2 000 tirages, graine 73), plutôt que des 121 051 événements corrélés.
6. Contrôle plus exigeant : ne noter, après entraînement, **que les débuts
   de mesures**. Parmi 16 108 candidats alignés sur les mesures, 1 341 sont
   des cadences (prévalence 8,325 %).

## Résultats observés

Voir [JSON reproductible](../../reports/dcml-cadence-exploratory-2026-11-08.json)
pour les métriques et révisions exactes.

| Modèle | AP, plis par œuvre | AP, compositeur inédit |
|---|---:|---:|
| Rythme seul | **0,0888** | **0,0548** |
| Harmonie seule | 0,0447 | 0,0379 |
| **Rythme + harmonie** | **0,1305** | **0,0743** |
| Rythme + harmonie permutée | 0,0894 | 0,0567 |

Gain du modèle combiné contre le rythme : **+47 % relatif** en validation
par œuvre parente, et **+36 %** sur un compositeur inédit. Le contrôle
permuté revient près du rythme seul, ce qui soutient l'hypothèse d'un
signal harmonique *localement aligné* avec les cadences.

À **positions métriques identiques** (seulement les débuts de mesures),
le score d'AP est **0,1038 → 0,1593** pour le modèle combiné ;
il reste **0,0769 → 0,1010** en transfert entre compositeurs. Ce n'est pas
une simple détection de début de mesure.

L'amélioration est **très inégale selon les compositeurs** : en test
sur compositeur entièrement inédit, AP Bach **0,237 → 0,245**, Chopin
**0,038 → 0,053**, Mozart **0,077 → 0,101**. Il reste beaucoup de
cadences non reconnues, notamment des fermetures non standard.

Le bootstrap apparié sur 80 œuvres parentes évaluables montre **62/80
œuvres améliorées**, gain moyen de l'AP par œuvre parente **+0,0447**
(IC 95 % rééchantillonné **[+0,0263 ; +0,0649]**). Lorsqu'on teste
des compositeurs entièrement exclus de l'entraînement : **60/80 œuvres
améliorées**, moyenne **+0,0346** (IC **[+0,0127 ; +0,0604]**).
Ces intervalles sont **conditionnés aux prédictions exploratoires figées**.
Ils quantifient une variation entre œuvres, **pas** une généralisation
confirmatoire à d'autres corpus, ni une preuve de causalité perceptive.

## Lancer sans réhéberger les partitions

Depuis la racine d'AnaMu, après avoir installé `numpy`, `scikit-learn` :

```bash
git clone --depth 1 https://github.com/DCMLab/chopin_mazurkas.git ../chopin_mazurkas
git clone --depth 1 https://github.com/DCMLab/mozart_piano_sonatas.git ../mozart_piano_sonatas
git clone --depth 1 https://github.com/DCMLab/bach_en_fr_suites.git ../bach_en_fr_suites
PYTHONPATH=. python scripts/dcml_cadence_benchmark.py \
  --corpus chopin=../chopin_mazurkas \
  --corpus mozart=../mozart_piano_sonatas \
  --corpus bach=../bach_en_fr_suites
```

Pour reproduire *exactement* les chiffres archivés, ramener ces trois clones
aux SHAs du tableau (les têtes des dépôts peuvent changer). Le code et les
tests : `anamu/cadence_events.py`, `scripts/dcml_cadence_benchmark.py`,
`tests/test_cadence_events.py`. Ce benchmark est inscrit au
`data/research-evidence.json` et s'arrête en cas de contrat incompatible.

## Deux autres sources discrètes découvertes, mais **pas** promues

| Source primaire | Annotations réellement décrites | Statut et réserve |
|---|---|---|
| [Panda et al., CMMR 2013](https://rppaiva.dei.uc.pt/publications/Conferences/CMMR2013_MultiModal.pdf), [téléchargement auteur](https://mir.dei.uc.pt/downloads.html) | 903 extraits audio ; **193 correspondances MIDI** ; cinq groupes d'humeurs MIREX reconstruits à partir de tags **AllMusic** | Pas 193 évaluations émotionnelles directes de plusieurs auditeurs ; pas de courbes temporelles ; ZIP officiel identifié mais données **non importées** dans AnaMu |
| [Ammirante & Russo, 2023](https://doi.org/10.1177/20592043231179410), [stimuli OSF](https://osf.io/y7zmt) | Expérience 2 : **48 stimuli** de fragments de mélodies, quatre conditions (sung/instrumental × registre), ~102 auditeurs donnant une **incertitude de continuation sur une échelle 1–9** | Très proche de la théorie d'attente musicale ; les stimuli sont disponibles, mais la disponibilité des **ratings individuels bruts** n'est pas encore vérifiée. Pas une annotation d'émotion. |

Ces deux sources ne sont volontairement **pas** injectées dans le modèle
`Mysterious` : ni les cinq clusters MIREX ni la certitude mélodique ne
sont des étiquettes d'atmosphère mystérieuse.

## Suite, critères de succès non négociables

1. **Rester dur sur les cadences :** distinguer *PAC/IAC/HC/PC*, les cadences
   interrompues ou évitées et les faux positifs à d'autres arrivées tonales.
   Comparer un algorithme de cadence publié lorsqu'un **moteur exécutable**
   et son domaine ont été vérifiés ; ne pas baptiser notre proxy « IDyOM ».
2. Tester sur **nouveaux compositeurs et familles stylistiques**, choisis
   avant de lire les labels, avec découpages par œuvre parente et vrais témoins.
3. Explorer les **annotations d'attente des auditeurs** (pas seulement
   l'analyse théorique d'un musicologue) si les réponses individuelles
   des études de continuation sont accessibles.
4. Seulement ensuite relier les mécanismes confirmés aux étiquettes
   humaines appropriées, notamment les humeurs difficiles de PIAST.
   **Aucun bénéfice sur `Mysterious` n'est encore démontré**.
