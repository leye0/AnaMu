> **Étude de validation à cible précise.** Ses mesures sont utiles à la
> conception de la grammaire ; elles ne valident pas une couche G2–G6.

# S1 — Transfert honnête vers la surprise humaine note par note (Manzara 1992)

**9 novembre 2026 — résultat exploratoire négatif.**

## Pourquoi ce test est différent

Les 24 auditeurs de Cuddy–Lunney (1995) et les 20 de Schellenberg
(1996) notaient à quel point **une note candidate continuerait bien** une
mélodie. Manzara, Witten et Conklin (1992) ont plutôt demandé à des personnes
de **deviner la prochaine note effectivement jouée et de parier** ; les
résultats indiquent combien de bits d'information humaine porte cette note
réalisée. Ce n'est **ni une note de 1 à 7, ni l'émotion perçue**.

- [Étude originale, Waikato (1992)](https://researchcommons.waikato.ac.nz/items/97793e93-66e4-4354-8159-9b1dbadda2f0).
- [Reconstruction / tables de l'étude, thèse 2025](https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation), révision
  `e9eb23384393c83de97e1a69d00133ae4673c425` :
  `manzetal92.data`, `manz_midi_stimuli/chorale151.mid`,
  `manz_midi_stimuli/chorale61.mid`.
- **29 + 57 observations de notes**, mais seulement **deux chorales**, donc
  deux œuvres parentes. Aucune réponse individuelle n'est exposée dans la
  source reconstruite ; on utilise la colonne `average`, distincte des
  autres agrégations `weighted` et `best`.

## Expérience contrôlée

1. Geler sur **Cuddy seulement** les modèles Ridge et la référence par
   hauteur relative du test précédent (aucun apprentissage Manzara).
2. Lire les 29/57 notes MIDI réalisées. Pour la note `i`, fournir
   strictement les notes `i−2` et `i−1` ; la note `i` sert uniquement
   d'événement final dont on estime la surprise.
3. Former les **25 candidats chromatiques** entre `i−1 ± 12` et transformer
   les 25 scores de plausibilité en pseudo-probabilités par **softmax à
   température fixée à 1 unité de score**. La surprise de la note jouée est
   `−log₂(probabilité)`. Ce choix est **arbitraire et non calibré sur les
   paris des humains** ; il ne reproduit pas IDyOM. Aucune des notes
   réalisées ne sort de cette fenêtre de 25 positions.
4. Exclure les deux premières notes de chaque chorale, car la méthode
   demande deux notes de contexte : **27 + 55 = 82** notes comparables.
5. Calculer les prédictions avant de lire la colonne de surprise humaine,
   puis la corrélation de rang au sein de **chaque** chorale. Comparer en
   contrôle descriptif aux mêmes scores cycliquement décalés dans chaque
   chorale, sans convertir les permutations en `p`-values.
6. Importer à titre **purement descriptif** les bits `idyom_ic` déjà produits
   par la thèse 2025, en vérifiant **86/86** correspondances de fichier,
   position et hauteur. **Le moteur IDyOM original n'est pas exécuté
   dans AnaMu ; ses conditions d'entraînement n'ont pas été auditées.**

## Résultat exact

| Prédiction | BWV 379, chorale 151 (27) | BWV 159, chorale 61 (55) | Moyenne de **2** ρ |
|---|---:|---:|---:|
| Profil de hauteur relative, Cuddy | +0,168 | −0,145 | +0,012 |
| Proximité, Cuddy | +0,044 | +0,117 | +0,080 |
| **Contour, Cuddy** (ancien gagnant externe) | **+0,013** | **−0,094** | **−0,040** |
| Contour + profil tonal, Cuddy | −0,025 | −0,233 | −0,129 |
| Correction résiduelle contextuelle, Cuddy | +0,032 | −0,115 | −0,041 |
| **IDyOM `cpitch`, pré-calculé par un tiers** | **+0,449** | **+0,481** | **+0,465** |

`ρ` est **Spearman** entre bits d'information humaine et bits prédits **de
la note effectivement jouée**, pas le score de bonne continuation des 15
ou 25 sondes. Moyenne de deux corrélations seulement : aucune barre d'erreur
inférentielle ou généralisation statistique. Les 82 lignes ne constituent
pas 82 morceaux, essais indépendants ou personnes distinctes.

**Conclusion : résultat négatif important.** Un proxy simple peut classer
les continuations possibles d'un fragment (ρ 0,770 sur Schellenberg) et
**échouer totalement** à suivre la surprise humaine de toutes les notes
successives d'un morceau. Nos modèles actuels utilisent seulement les deux
dernières notes ; ils n'apprennent pas les styles des chorales, la mémoire
de la mélodie ou les probabilités de transitions musicales à long terme.
La meilleure corrélation du fichier IDyOM tiers montre que la cible est
partiellement prévisible, **mais il ne s'agit pas d'une comparaison loyale
de modèles à entraînement vérifié** : IDyOM dispose potentiellement d'autres
contextes, corpus et conditions de préentraînement.

Il est **interdit** de promouvoir la méthode Cuddy comme détecteur de
surprise temporelle ou d'émotion sur cette base. La température de softmax
n'a pas été ajustée à ces 82 notes. La reconstruction musicale et les
annotations originales avaient déjà été inspectées : résultat exploratoire.

## Réexécution et tests

```bash
PYTHONPATH=. python -m scripts.manzara_cross_target \
  --source ../melodic_expectancy_thesis \
  --output reports/manzara-cross-target-2026-11-09.json
python -m unittest tests.test_manzara_cross_target tests.test_research_contracts -v
```

Le dépôt ne contient **aucun tableau de paris humains recopié** : uniquement
les analyseurs, des fixtures synthétiques et le JSON récapitulatif. Le
contrat `manzara_1992_cross_target` exige exactement la cible
`human_next_note_information_bits`, une validation groupée par **chorale**
et refuse sa conversion en émotion ou en jugement de continuation.

## Suite scientifiquement justifiée

1. **Préférer le vrai modèle de mémoire/statistique musicale** : exécuter
   IDyOM original ou un modèle probabiliste publié sur corpus d'entraînement
   explicitement disjoint, vérifier l'absence des deux chorales dans
   l'apprentissage et ne pas choisir les hyperparamètres sur ces deux œuvres.
2. Trouver plus de **chorales et de chansons indépendantes avec paris ou
   cotes humaines note par note** ; deux œuvres ne suffisent pas à conclure.
3. Conserver les deux tâches séparées : *plausibilité de continuation*
   (Cuddy/Schellenberg) et *surprise séquentielle réelle* (Manzara).
4. Étudier [MEX (2026)](mex-2026-source-audit.md) pour la comparaison
   MIDI/audio et les réponses neurales, sans les appeler des sentiments
   `Mysterious` ou `Epic`.
