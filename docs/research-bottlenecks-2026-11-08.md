# Pourquoi l'activité ne devient pas toujours du progrès

## Ce que les derniers résultats établissent

Les trajectoires tonales, rubans de tension et indices de surprise n'ont pas
produit de gain général stable sur les cinq humeurs difficiles. L'ordre des
fenêtres tonales ne dépasse pas leur permutation. Le transfert de Tense
PIAST à la tension comparative IsoVAT échoue. Ce sont des échecs de ces
opérationnalisations et protocoles, pas une réfutation générale des théories.

La piste positive actuelle concerne les annotations : préserver les votes
minoritaires améliore le classement par rapport à la majorité binaire.
La dernière calibration (run 42520423568, commit 77c810a) montre également
que retirer le rééquilibrage améliore Hard5 AP de 0,386 à 0,393 et Brier
de 0,190 à 0,115. Ce Brier vise le vote d'un expert, pas la présence objective
d'une émotion. Le témoin moyen atteint 0,131 ; une amélioration face au
score équilibré mal calibré ne doit pas être présentée comme une révolution.

## Le banc PIAST ne mesure pas notre ambition temporelle

Source primaire : Bang et al., *PIAST: A Multimodal Piano Dataset with
Audio, Symbolic and Text*, NLP4MusA 2024, §2.3.1, p. 3 du PDF :
https://aclanthology.org/2024.nlp4musa-1.2.pdf

Les experts annotaient des extraits audio de 30 secondes. Le protocole
leur demandait d'exclure les extraits non strictement piano solo ou comportant
de subtils changements d'humeur. Les MIDI sont des transcriptions automatiques.

Conséquence méthodologique : PIAST peut tester des associations entre structure
MIDI et étiquettes globales. Il ne fournit pas de vérité émotionnelle datée,
et sa sélection réduit précisément les changements que les modules temporels
d'AnaMu cherchent à expliquer. Un résultat négatif PIAST ne suffit pas à
abandonner un mécanisme temporel ; un positif n'en démontre pas la temporalité.

## Hypothèse du timbre soulevée par Léon

Le MIDI décrit des événements et commandes, sans conserver le son original.
Programme, vélocité et pédale éventuels ne reconstruisent pas automatiquement
la banque sonore, les résonances, l'enveloppe et la prise de son entendues par
les experts. Mysterious peut dépendre de cette information manquante.
Mais il n'est pas établi que le timbre explique son faible score : ambiguïté
du vocabulaire, désaccord des experts, transcription et modèle sont également
possibles. Ne pas retirer Mysterious des cinq cibles pour augmenter la moyenne.

## Ordre concret des prochaines décisions

1. Comparaison de capacité terminée : arbres à interactions 0,377 contre
   logistique 0,401 Hard5 AP sur les mêmes plis ; ne pas promouvoir les arbres.
   Les plis historiques diffèrent, donc ne pas comparer 0,401 à 0,393 comme
   un gain. Manifeste de partitions enregistré pour les prochaines reprises.
   Protocole dans
   [piast-nonlinear-protocol.md](piast-nonlinear-protocol.md). Même information
   musicale, meilleur témoin linéaire et contrôle de mélange des votes.
2. Pour la dynamique émotionnelle, revenir aux annotations temporelles
   VGMIDI et aux trajectoires de tension IsoVAT. Mesurer les changements
   à l'intérieur des œuvres, pas uniquement l'erreur sur leur niveau moyen.
   Les jeux déjà inspectés restent exploratoires.
3. Une comparaison future audio/MIDI doit garder exactement les mêmes extraits,
   votes et plis. Elle pourrait tester l'information supplémentaire du son,
   mais ne séparerait pas à elle seule timbre et erreurs de transcription.
   Aucun pipeline audio/Demucs lancé ici.
4. Toute sélection supplémentaire de modèle doit se faire dans les plis
   d'entraînement. Les 1 900 PIAST ne peuvent plus servir de test inédit.

La priorité est de faire correspondre la question, l'observation disponible
et la métrique, avant d'ajouter une nouvelle famille de descripteurs.
