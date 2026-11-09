# AnaMu S1 — transfert externe des attentes mélodiques, 1995 → 1996

**8 novembre 2026 · contre-épreuve exploratoire indépendante de l'étude de départ.**

## La question, enfin testée sur d'autres auditeurs

Le [premier laboratoire Cuddy–Lunney](cudlun-human-expectancy-study.md) avait
trouvé que la combinaison d'un profil moyen de notes et d'une correction de
contour/tonalité dépassait les autres modèles sur huit débuts de **deux** notes
notés par 24 auditeurs. Mais son choix était *post-hoc* et les huit mélodies
étaient connues de l'expérimentateur.

L'étude primaire [Schellenberg (1996), *Expectancy in melody: tests of the
implication-realization model*](https://doi.org/10.1016/0010-0277(95)00665-6)
présente **huit fragments réels de chansons populaires britanniques** à
**20 autres auditeurs**, avec **15 notes diatoniques candidates** chacune.
Les **120 moyennes** de qualité de continuation (1–7) figurent en Appendice A
de l'article original. Elles ne sont ni des émotions ni des réponses
individuelles. Il s'agit d'une étude et d'un répertoire distincts, et les
stimuli sont maintenant **longs de 16 à 21 notes**.

Le dépôt universitaire
[yiannisem/MSc-Thesis---modelling-pitch-expectation](https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation),
commit `e9eb23384393c83de97e1a69d00133ae4673c425`, contient :

- `schell96.data` : les 8 blocs × 15 scores humains **ordonnés du grave à
  l'aigu après renversement** ; le renversement apparaît explicitement dans
  les scripts du mémoire car le fichier de base va de l'aigu au grave ;
- `schellenberg_midi_stimuli_with_probe/` : huit reconstructions du contexte
  **avec une dernière note artificielle C6 (MIDI 84)** qui ne constitue
  *pas* une vraie note du fragment et doit être retirée ;
- `schellenberg_midi_notes_predicted.xlsx` : les **120 notes candidates exactes**,
  vérifiées contre les 120 notes reconstruites indépendamment à partir des
  signatures tonales et du dernier son. **120/120 correspondent.**

Les fichiers MIDI sont reconstruits, pas les signaux acoustiques d'origine.
Les versions du mémoire préservent l'ordre des notes et les signatures
tonales de ces fragments, mais ne démontrent pas une reproduction fidèle du
timbre, du synthétiseur et des conditions d'écoute de 1996.

## Protocole gelé : aucun apprentissage sur la nouvelle étude

1. Charger **uniquement Cuddy** (8 × 25 × deux moyennes de groupe) pour
   obtenir les mêmes caractéristiques, les mêmes profils de hauteur et le
   même `StandardScaler` + `Ridge(alpha=10)` que dans le banc précédent.
2. Entraîner **les quatre variantes précédemment définies**, sur Cuddy
   seulement : proximité, contour, contour+tonalité, et correction résiduelle
   du profil moyen. Aucun paramètre n'est sélectionné sur Schellenberg.
3. Charger les **MIDI de Schellenberg sans les scores humains**. Supprimer
   la note artificielle finale, lire exclusivement les **deux dernières
   notes réelles** pour le modèle Cuddy, et construire les 15 continuations
   diatoniques publiées, dans leur ordre ascendant vérifié par le classeur.
4. Calculer et conserver toutes les prédictions **avant de lire** le fichier
   `schell96.data`. Puis ouvrir ses 120 moyennes et comparer le modèle à la
   baseline de hauteur seule. Une note candidate peut légitimement porter
   l'information de sa hauteur et de la gamme autorisée par le protocole ;
   aucune gamme annotée par l'humain n'est introduite comme caractéristique.
5. Évaluer la moyenne des **huit corrélations Spearman par fragment**, le
   R² global et la corrélation Pearson. Le bootstrap tire au sort des
   **fragments-stimuli**, pas les 120 notes ni les 20 personnes (les mêmes
   auditeurs ont évalué plusieurs fragments).

Ce test externe reste **exploratoire** : l'architecture résiduelle avait été
choisie après examen de Cuddy, et les tableaux de Schellenberg avaient été
partiellement consultés pendant la recherche de données. Nous n'avons pas
utilisé ces nouvelles valeurs pour ajuster l'algorithme, mais comparer cinq
variantes sur cet ensemble restreint ne transforme pas automatiquement la
meilleure variante en découverte confirmée.

## Résultats, 120 continuations jamais vues pendant l'apprentissage

| Modèle appris sur Cuddy seulement | Spearman moyen (8 fragments) | R² global | Gain de ρ par rapport aux hauteurs |
|---|---:|---:|---:|
| Hauteur relative moyenne de Cuddy, sans contexte | **0,560** | 0,170 | — |
| Proximité seule | 0,679 | 0,262 | +0,119 (6/8) |
| **Contour/retour/direction/intervalle — proxy** | **0,770** | **0,382** | **+0,210 (7/8)** |
| Contour + profils de tonalité, directement | 0,688 | 0,247 | +0,128 (6/8) |
| Hauteur + correction résiduelle contextuelle | 0,650 | 0,229 | +0,090 (5/8) |

L'intervalle bootstrap **par fragment** de la différence moyenne en ρ
contre la référence est **[+0,101 ; +0,324]** pour le contour seul et
**[+0,011 ; +0,176]** pour la correction résiduelle. Ces intervalles
décrivent les *huit stimuli* et ne mesurent pas la dispersion des réponses
individuelles (absentes de la source publique).

**Deux observations opposées** :

1. **La correction résiduelle ne s'effondre pas complètement** : elle améliore
   la baseline sur une étude indépendante, même avec des extraits beaucoup
   plus longs et des candidats diatoniques plutôt que chromatiques.
2. **Le gagnant sur Cuddy n'est pas le gagnant en transfert.** Le simple
   contour mélodique, qui ne prédisait pas aussi bien sur les huit contextes
   de Cuddy, **dépasse nettement** la correction contextuelle sur Schellenberg.
   L'ajout de profils tonals n'aide pas ici. Cela indique que la séparation
   « profil moyen + correction résiduelle » est trop spécialisée aux stimuli
   pauvres en contexte de la première étude, ou que les deux tâches diffèrent.
   Les données ne permettent pas d'affirmer quelle explication est causale.

**Le résultat scientifiquement le plus robuste est désormais la présence
d'information transférable dans le mouvement mélodique**, non la supériorité
universelle de la construction résiduelle. Ne pas intégrer de poids dans le
moteur émotionnel ni assimiler une continuation plausible à une humeur.

## Vérification et reproduction

```bash
git clone https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation.git ../melodic_expectancy_thesis
git -C ../melodic_expectancy_thesis checkout e9eb23384393c83de97e1a69d00133ae4673c425
python -m pip install numpy scipy scikit-learn mido
python -m scripts.validate_research_contracts
python -m unittest tests.test_schellenberg_transfer tests.test_research_contracts
PYTHONPATH=. python scripts/schellenberg_external_transfer.py \
  --source ../melodic_expectancy_thesis \
  --output reports/schellenberg-external-transfer-2026-11-08.json
```

Le script refuse toute autre révision du dépôt amont. La CI vérifie le
contrat, la construction des candidates, l'exclusion de la note finale et
l'entraînement isolé **sans télécharger ni versionner** les réponses
historiques de l'étude. Le rapport JSON conserve les 8 × 15 candidats,
les scores par fragment et les groupes effectivement évalués.

## Suite recommandée : nouvelle matière, nouveaux risques

- **Trouver une troisième étude** avec questions et réponses strictement
  identifiables ; la priorité est aux stimuli plus longs et aux réponses
  individuelles, si légalement accessibles. Hansen et Pearce (2014) semble
  pertinent (24 contextes, 9 notes-sondes), mais les réponses brutes n'ont
  pas été localisées avec certitude.
- **Reproduire les vrais modèles publiés** Schellenberg/Narmour ou IDyOM
  avant d'étiqueter notre proxy « moteur universitaire ». Le `melody-features`
  original extrait des descripteurs Narmour, mais les poids calculés ici sont
  les nôtres, appris exclusivement sur Cuddy.
- **Séparer contexte immédiat / mémoire à long terme** lorsque des vraies
  mélodies plus longues sont utilisées. La distance de généralisation
  entre Cuddy et Schellenberg est plus instructive que dix réglages
  additionnels sur la même tâche.
- **Ne pas répéter les cadences atypiques par défaut.** C'est une autre
  hypothèse, un autre phénomène et un autre jeu d'annotations.
