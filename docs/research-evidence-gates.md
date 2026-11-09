# AnaMu — contrats de preuve avant chaque expérience

**État : 8 novembre 2026.** Aucune victoire algorithmique n'est annoncée par
ce changement. La question est d'arrêter les expériences mal alignées sur la
source et les faux gains issus de données déjà examinées.

Le registre faisant foi est [`data/research-evidence.json`](../data/research-evidence.json).
Il sépare :

1. **Sources** : ce que les humains ont effectivement annoté, unité, granularité,
   accessibilité des votes, origine du MIDI, groupe à tenir hors entraînement ;
2. **Méthodes** : moteur universitaire original effectivement exécuté *ou*
   approximation AnaMu inspirée d'une théorie, sorties réellement calculables ;
3. **Expériences** : source × cible exacte × protocole × provenance de méthode
   × statut exploratoire/confirmatoire.

Le validateur refuse les affirmations scientifiquement incompatibles. Il ne
remplace pas la revue du papier, du code ni le calcul statistique : une
expérience compatible peut échouer, et un score élevé ne démontre pas une
cause psychologique.

## Les neuf sources, sans convertir une cible en une autre

| Source | Étiquette humaine réellement utilisée | Unité indépendante | Ce que cela **ne prouve pas** |
|---|---|---|---|
| PIAST-AT | Trois choix d'experts, humeurs globales sur 30 s | Vidéo source | Dynamique locale d'une humeur ; les auteurs excluaient les changements subtils |
| VGMIDI | Valence **et** activation continues ; ~30 auditeurs | Pièce | Présence de *Mysterious*, *Epic* ou d'une émotion discrète |
| IsoVAT | Comparaison relative tension/valence/activation entre clips de quatre mesures | Triplet | Courbe temporelle de tension à l'intérieur du clip |
| PercePiano | 19 attributs de performance notés par des pianistes experts | Œuvre parente | Identité avec les tags *Dark/Epic/Mysterious* de PIAST |
| CP-WTC | Valence/activation des huit premières mesures de six interprètes, 48 compositions | Composition | Courbe de valence par mesure ; effet causal du seul interprète si groupes d'annotateurs confondus |
| EMOPIA | Un quadrant par extrait | Chanson source | Quatre votes indépendants par extrait ; les quatre annotateurs ont réparti les chansons |
| XMIDI | Catégorie émotionnelle/genre sur morceau entier | Pièce (doublons à auditer) | Émotion humaine datée ou votes individuels accessibles |
| DCML Distant Listening Corpus | Cadences et phrases annotées par des musicologues sur partitions symboliques | Œuvre parente (sonate/suite entière) | Émotions, ressenti de tension ou véritable timbre MIDI/audio ; pas de votes individuels par cadence |
| Cuddy & Lunney (1995) | **Qualité perçue d'une note suivante**, 200 notes-sondes × deux moyennes de groupe | Contexte mélodique à deux notes | Émotion, anticipation en temps réel, votes individuels ; le MIDI de 2025 est reconstruit et transposé |

Sources primaires : [PIAST](https://aclanthology.org/2024.nlp4musa-1.2/),
[VGMIDI](https://github.com/lucasnfe/vgmidi),
[IsoVAT](https://doi.org/10.5334/tismir.120),
[PercePiano](https://doi.org/10.1038/s41598-024-73810-0),
[CP-WTC](https://zenodo.org/records/21693024),
[EMOPIA](https://annahung31.github.io/EMOPIA/),
[XMIDI](https://github.com/xmusic-project/XMIDI_Dataset),
[DCML DLC](https://doi.org/10.1038/s41597-025-04976-z),
[Cuddy & Lunney](https://doi.org/10.3758/BF03213071).

**Important sur l'instrumentation :** les commandes MIDI contiennent notes,
temps, vélocité, programmes et parfois pédale, **pas** le timbre original,
les résonances acoustiques ou l'enveloppe sonore entendus par les auditeurs.
Le fait que *Mysterious* reste faible n'établit pas que le timbre en est la
cause. Audio/Demucs restent reportés ; aucun nouvel appel audio.

## Les méthodes sont des observations, pas des émotions

| Moteur / théorie | Statut réel dans AnaMu | Observation utilisable | Limite |
|---|---|---|---|
| Partitura / Herremans-Chew | Moteur exécuté | Diamètre, momentum, strain tonal | Ni tension humaine directement ni timbre |
| music21 | Moteur exécuté | Accords et tonalités **hypothétiques** | Pas vérité d'analyse harmonique |
| melody-features / Narmour | Moteur exécuté | Descripteurs mélodiques | Pas continuation humaine prédite et validée |
| jSymbolic original | Java exécuté sur des lots VGMIDI | Texture, rythme, articulation symboliques | Pas enveloppe spectrale ni émission émotionnelle |
| IDyOM original | Adaptateur/import, Lisp **non exécuté** | Aucune sortie originale confirmée | Les n-grammes maison ne sont pas IDyOM |
| Farbood | Proxy temporel maison | Pentes, cumuls, relâchements | Pas les équations/poids perceptifs originaux |
| Modulation tonale inspirée de MoFi | Proxy maison | Distribution et ordre des tonalités locales | Le contrôle réordonné annule l'argument temporel |
| Modèle relatif inspiré de Delta-VA | Proxy maison | Différences d'interprétation MIDI | Pas reproduction du réseau original |
| Proxy de cadences par notes MIDI-compatibles | Proxy maison exécuté | Indices rythmiques + chroma relatif à la tonalité estimée + basse et transitions | Pas l'algorithme publié DCML, pas l'analyse experte ni l'émotion humaine |
| Proxy de continuation Cuddy/Narmour | Proxy maison exécuté | Proximité, direction/retour mélodique, profils tonals, correction résiduelle | Pas la formulation originale des auteurs ; évalué seulement sur huit contextes déjà examinés |

La présence de 1 203 colonnes ou de 23 mécanismes dans l'inventaire n'est
**pas** une validation indépendante de 23 phénomènes perceptifs.

## Deux laboratoires, deux exigences

### Laboratoire musical : M0–M4

- Contrôler les événements natifs, les voix, tonalités, cadences, motifs et
  attentes sur fixtures et **vérités musicales appropriées**, avec ambiguïté.
- Pour un mécanisme temporel, comparer l'ordre réel au même contenu mélangé
  sans ordre et au témoin statique ; mesurer gain sur changement **interne**.
- Un bon score d'intervalle ou de tension ne signifie jamais que le modèle
  sait prédire *Mystérieux* ou *Épique*.

### Laboratoire émotionnel : M5

- PIAST : classement **global** et votes minoritaires ; mesures Hard5
  (`Mysterious`, `Epic`, `Tense`, `Dark`, `Happy`) et 14 noncalm. La catégorie
  Calm ne peut pas masquer les échecs difficiles.
- VGMIDI : trajectoire valence/activation, avec corrélations **intra-pièce**
  séparées des moyennes globales. Ne pas baptiser les deux axes « émotions ».
- IsoVAT : ordres humains de tension entre les clips, pas courbes continues.
- PercePiano / CP-WTC : effets relatifs entre interprétations d'une même
  partition ; séparation par œuvre entière, pas juste par extrait.

Un lien entre les laboratoires est une **hypothèse de transfert** à tester,
pas une équivalence d'étiquettes.

## Règles de passage aux conclusions

1. Déclarer le phénomène, la cible humaine exacte, la source et ce qu'elle
   **ne mesure pas** avant toute extraction.
2. Fixer la cohorte, les groupes, le prétraitement, le modèle et la métrique ;
   archiver les affectations exactes aux plis, pas seulement `GroupKFold`.
3. Garder le meilleur modèle simple, les labels mélangés, les fenêtres
   mélangées et les contrôles de variables manquantes comme références.
4. Choisir les paramètres uniquement sur l'entraînement/validation interne.
   Une évaluation répétée du même test reste **exploratoire**.
5. Publier chaque humeur difficile, effectifs et intervalles, ainsi que les
   régressions. Aucune promotion sans gain stable sur œuvre/source inédite.
6. Séparer les affirmations : extraction exacte, prédiction musicale,
   concordance humaine, prédiction affective, causalité. La causalité requiert
   un protocole d'intervention et ne résulte pas d'une simple association.

## Contrôle exécutable, sans dépendances lourdes

```bash
python -m scripts.validate_research_contracts
python -m unittest tests.test_research_contracts -v
```

Pour une expérience proposée, fournir un objet JSON contenant les champs
de l'une des entrées `experiments` du registre, puis lancer :

```bash
python -m scripts.validate_research_contracts --proposal /tmp/experience.json
```

Les scripts `piast_tonal_motion_experiment`, `isovat_tension_benchmark` et
`vgmidi_temporal_benchmark` vérifient leur contrat enregistré **avant leur
traitement coûteux**. Le workflow `research-evidence-contracts.yml` réalise
les contrôles hors corpus, sur chaque modification pertinente. Un nouveau
banc doit être enregistré et brancher le même contrôle ; **cela ne constitue
pas encore un garde automatique sur tous les anciens scripts**.

La PR de reproductibilité [PIAST #1](https://github.com/leye0/AnaMu/pull/1)
reste distincte : elle fige les 1 900 affectations et leurs prédictions.
Ne comparer les scores entre PR que lorsque les plis sont identiques.

## Prochaine expérience qui mérite d'être financée

Le [premier test de plausibilité de continuation mélodique jugée par des
auditeurs](cudlun-human-expectancy-study.md) déplace la question hors du
chantier des cadences et observe un **gain exploratoire** lorsque les profils
de hauteur généraux sont complétés par une correction contextuelle. La
comparaison directe de nombreuses caractéristiques harmoniques fait moins
bien que cette simple référence ; voir le rapport et les réserves de
validation post-hoc sur huit contextes.

**Priorité :** chercher une deuxième source indépendante de **continuations
jugées par des humains**, avec réponses réellement accessibles, fixer le
modèle et les métriques sans regarder les nouveaux jugements, puis exécuter
une vraie contre-épreuve. Ne pas réutiliser un benchmark de cadences ou une
annotation valence/activation comme vérité pour cette cible. À terme,
mesurer si ce mécanisme ajoute un signal sur les émotions difficiles de
PIAST sans prétendre que les tâches humaines sont identiques.
