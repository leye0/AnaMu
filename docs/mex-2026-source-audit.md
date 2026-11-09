# Audit des cibles — MEX, Musical Expectation Benchmark Suite (novembre 2026)

**Nouvelle publication scientifique primaire :** Bjare et al.,
*MEX: The Musical Expectation Benchmark Suite*,
[arXiv:2611.01843 v1 (1er novembre 2026)](https://arxiv.org/abs/2611.01843),
[code officiel MIT](https://github.com/MusicPerceptModeling/mex),
[catalogue des jeux de données](https://huggingface.co/datasets/MusicPerceptModeling/mex).

Ce projet est une **suite d'évaluation**, pas un corpus unique où des humains
ont noté des émotions. Son interface reçoit des **séries temporelles de
surprise (`IC`) ou d'incertitude (entropie) estimées par un modèle audio**,
et les confronte à quatre tâches distinctes. Les algorithmes audio
GIVT/DIF et le package MEX n'ont **pas encore été exécutés dans AnaMu**.

| Tâche | Données | Vérité externe exacte | Ce qu'il serait faux de conclure |
|---|---|---|---|
| **RE** — répétition | SALAMI, enregistrements multipistes/genres | Segments de forme musicale **annotés** qui se répètent | Des votes humains quantifiant directement la surprise de chaque note ou `Mystérieux` |
| **SB** — limites structurelles | SALAMI, ~1 310 enregistrements | Frontières de segments à trois niveaux (local, global, fonction) | Émotions, tension ressentie, ou une segmentation causée exclusivement par l'harmonie |
| **SY** — correspondance symbolique/audio | SYN, mélodies synthétisées avec **cinq timbres** (piano, guitare, pad, voix synthétique, trompette) | **Valeurs calculées par IDyOM**, pas des annotations humaines d'émotion | Une preuve que l'audio détecte la composante `Mysterious` ou que les timbres ont été notés par des auditeurs |
| **NE** — prédiction neurale | VOC, **18 mélodies chantées**, EEG auditeur | Réponses électrophysiologiques humaines et contrôle de l'enveloppe sonore | Une note subjective des émotions ou une mesure directe de mystère |

### Pourquoi cela nous intéresse

MEX répond enfin à un besoin concret d'AnaMu : **tester le transfert MIDI
symbolique → musique audible avec plusieurs timbres** sur les **mêmes
mélodies**. On peut mesurer si l'information d'attente perdue par un modèle
MIDI se retrouve dans l'audio, puis vérifier si ses prédictions expliquent
un signal neural au-delà de l'enveloppe acoustique. En revanche, la tâche
**SY mesure l'accord avec IDyOM**, qui n'est pas une vérité humaine directe.
L'étude rapporte des associations de rang audio–IDyOM approximativement
entre **0,4 et 0,6** et constate une variation selon le timbre : **ne pas
convertir cette association en qualité de prédiction d'une humeur**.

### Obstacles d'usage vérifiés

- La structure MEX accepte `Dataset` avec `id` + série temporelle de modèle,
  et des métadonnées cohérentes avec cette clé (API `Task`). On pourrait
  ajouter un adaptateur AnaMu seulement si l'on produit une série de surprise
  *audio* temporellement alignée ; nos scores Cuddy sur sondes MIDI de fin
  de fragment ne correspondent pas à cette entrée.
- SALAMI ne fournit **pas** tous ses enregistrements audio en accès libre
  depuis le Hub. L'article le signale comme limite d'accès ; ne pas lancer
  un benchmark complet sans résolution des droits et de la disponibilité.
- Les baselines audio sont des modèles à dépendances potentiellement lourdes
  (`pip install ".[baselines]"`, PyTorch) et des calculs de vraisemblance
  coûteux ; aucun coût GPU ou résultat local n'est revendiqué.
- Les tests EEG exigent de préserver les groupes **participants / essais**,
  pas de compter chaque fenêtre EEG comme un auditeur différent.

**Priorité recommandée :** petit pilote SY à timbres multiples, mais
**uniquement après** avoir établi un vrai modèle probabiliste de surprise
et un protocole apparié de notes. L'évaluation directe de l'émotion
`Mysterious` reste un chantier séparé nécessitant ses propres annotations.
