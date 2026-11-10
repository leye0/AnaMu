# AnaMu — feuille de route active (10 novembre 2026)

**Référence des objectifs :** [OBJECTIVES.md](OBJECTIVES.md).
**Architecture académique :**
[music-grammar-research-program.md](music-grammar-research-program.md).

Cette page est la seule liste **active** des prochains développements.
Les études de référence encore utiles sont rangées dans
[`studies/`](studies/). Les anciennes feuilles de route des émotions ont
été retirées du projet.

## Ce qui est réellement acquis

| Domaine | Concrètement vérifié | Limite |
|---|---|---|
| **G0 MIDI** | Octets originaux, événements, pistes, temps exacts, vélocités, contrôleurs, notes non ambiguës et diagnostics | Pas de voix ni d'acoustique inférée |
| **G1 temporalité** | Les 13 relations d'Allen ; `SEQUENCE`/`PARALLEL` entre intervalles de touches | Relations entre notes, pas entre phrases ni instruments |
| **G1 transformations** | Transposition/augmentation exactes **si correspondance fournie**, avec vérification indexée pour lots de preuves | Pas de correspondance sémantique ou perceptive |
| **G2.2 exploratoire** | Recherche autonome de fenêtres d'attaques consécutives, répétées exactement sous transposition et changement uniforme d'échelle temporelle ; témoins `TRANSFORM` G1 | **Candidats structuraux**, pas thèmes, voix, phrases ou frontières validés ; ni SIA/SIATEC complet |
| **Partition MusicXML** | Inventaire des parties, notes notées, positions métriques exactes, hauteurs écrites/sonnantes selon transposition déclarée ; voix simultanées conservées | Pas de reconstruction des reprises, des durées liées, de rôles ou d'alignement aux notes MIDI |
| **Orchestration et contre-épreuve générative** | Détection de doublures strictes entre parties à l'unisson/octave ; reconstruction de trois notes masquées après trois notes d'apprentissage, comparée à un témoin | Structure et reconstruction **dans la même œuvre**, pas qualité d'orchestration, jouabilité ou écoute |
| **Conduite des voix notée** | Mouvements de quartets entre deux parties : contraire, parallèle, similaire, oblique, statique, croisements, quintes/octaves parallèles ; contre-proposition d'une note | Attaques strictement synchronisées et voix/portées notées constantes ; pas de fonction harmonique ni de qualité esthétique déduite |
| **Corpus orchestral** | Beethoven 5/I et 7/II : MIDI et scores complets, licences et SHA-256 distincts, rapports JSON | Éditions indépendantes, identité note par note non démontrée |
| **Contrôles scientifiques** | Contrats de sources, cadences et attentes humaines comme cibles indépendantes | N'évaluent pas encore un parseur G2/G3 |

## Prochaines expériences dans l'ordre

### G2.0 — confiance dans les sources et alignement (priorité immédiate)

1. Comparer les **hauteurs et temps de notes** de partitions vs MIDI avec
   tolérances explicites pour les reprises et transpositions instrumentales.
2. Identifier les pupitres fusionnés ou incorrectement étiquetés et conserver
   toute ambiguïté au lieu de corriger silencieusement les noms MIDI.
3. Tester la concordance sur les deux mouvements, puis une composition
   indépendante ; publier taux de couverture et cas impossibles.

**Critère de sortie :** table d'alignements traçables, taux de notes
couvertes, diagnostics d'écart et contrôles négatifs. La simple différence
18/19 parties vs 12 pistes ne suffit pas.

### G2.1 — annotations humaines de voix et de motif

1. Étudier les annotations `Hauptstimme` pour les phrases où la mélodie
   principale change de pupitre ; conserver **la licence CC BY-SA** des
   annotations sans les mêler au code/aux partitions CC0.
2. Produire des règles sans étiquettes humaines visibles lors de
   l'inférence ; évaluer leurs propositions sur les annotations retenues.
3. Mesurer des baselines : continuité du registre, de la durée et de
   l'instrument, répétition exacte, et hypothèse « aucune voix ».

**Critère de sortie :** précision/rappel de rôles par segment **et** échecs
qualitatifs ; tests entre œuvres plutôt que fragments apparentés.

### G2.2 — groupements, répétitions et transformations

**Prototype implémenté, non validé musicalement :**
`anamu/grammar_motifs.py` groupe les notes par piste/canal MIDI (et **non**
par voix supposée), puis recherche sur 3 à 5 attaques consécutives des
fenêtres exactement identiques après transposition et multiplication
uniforme de leurs durées/décalages. Les accords et notes superposées d'une
même piste/canal sont conservés ; les percussions, touches de durée nulle et
fenêtres trop denses sont comptées ou écartées explicitement. Des bornes
de calcul sont imposées. Chaque occurrence renvoie aux identifiants des
événements sources et chaque relation est prouvée par `TRANSFORM` G1.

Sur **Beethoven 5/I** : 1 578 signatures candidates pour 19 113 fenêtres
examinées (8 295 notes). Sur **Beethoven 7/II** : 2 022 signatures candidates
pour 15 648 fenêtres (6 041 notes). Ces comptes sont des **inventaires
algorithmiques**, pas des scores de précision/rappel ni des thèmes vérifiés.
Une signature commune avec répétition temporelle suffit à une hypothèse de
`GROUP` **plat** ; l'arbre hiérarchique et les motifs reconnus par un
analyste humain sont encore inconnus.

**À faire pour valider G2.2 :**

- Répétitions non adjacentes, transpositions, inversions, augmentations/
  diminutions et fragmentations ; ne pas confondre contour et identité
  thématique perceptive. Le prototype ne cherche actuellement que les
  transpositions avec facteur temporel uniforme.
- Frontières de groupes candidates et hiérarchies multiples, confrontées
  aux hypothèses GTTM/LBDM et à des annotations humaines explicites.
- Témoins permutés, segments aléatoires et baselines purement rythmiques.

**Critère de sortie :** gains reproductibles sur une source indépendante,
sans règle codée spécialement pour un compositeur.

### Orchestration notée — premier incrément et test de composition

Deux mécanismes ajoutés, distincts du motif MIDI :

1. `anamu/score_texture.py` lit les hauteurs écrites et les hauteurs
   **sonnantes** de parties MusicXML, la position en fractions de noire,
   les voix et accords sans les réduire à une piste monophonique. Il
   relève des lignes de plusieurs notes rigoureusement doublées entre
   pupitres, sans inférer leurs rôles artistiques.
2. `anamu/orchestral_counterfactual.py` **apprend localement** une relation
   de doublure sur trois notes, **génère** les trois suivantes du second
   pupitre en les cachant, puis mesure la reconstruction face aux
   baselines hauteur constante et copie à l'unisson. Beethoven 5/I :
   4 816/6 294 (76,5 %) ; Beethoven 7/II : 5 625/6 303 (89,2 %) ;
   témoins 30,0 %/25,2 % et 31,2 %/25,0 % respectivement.

Les nombreux couples instrumentaux d'une même pièce sont corrélés :
**ces pourcentages ne sont ni une validation hors œuvre, ni des notes de
qualité musicale.** Il manque la structure harmonique, les rôles
instrumentaux, les sources acoustiques et l'appréciation musicale humaine.
Consulter le [contrat composition/orchestration](composition-grammar.md)
avant d'étendre ces indicateurs.

**Prochaines tâches :**

- Poursuivre l'alignement **note à note** MusicXML↔MIDI : les sources
  indépendantes et les reprises empêchent toute équivalence supposée.
- Ajouter des annotations expertes de rôles de pupitres (mélodie,
  contrechant, basse, figuration, soutien) à l'échelle de passages,
  et un contrôle musical, pas seulement exact, des doublures.
- Tester un **compositeur tenu à l'écart**, des baselines plus fortes et
  des expériences d'ablation : ôter une doublure, changer l'octave,
  redistribuer le même matériau dans un autre registre.
- Pour toute prétention de « sonne bien », créer une réalisation audio
  et une **évaluation d'écoute aveugle** ; une bonne reconstruction de
  partition ne suffit jamais.

### Conduite des voix — un deuxième mécanisme d'écriture

`anamu/orchestral_voice_leading.py` mesure des *quartets* de notes
notées entre deux parties et génère un contrefactuel de mouvement
(`parallel`, `contrary`, `oblique`) en modifiant **une seule note**.
Le vocabulaire est celui de l'analyse contrapuntique traditionnelle,
mais on ne déclare pas les quintes ou octaves parallèles « interdites »
dans une orchestration. Chaque observation et contre-proposition garde
les IDs de notes sources et ne transforme jamais la partition d'origine.

- Beethoven 5/I : 24 824 quartets, dont 1 932 contraires et 73
  croisements stricts ; Beethoven 7/II : 11 602, dont 977 contraires
  et 174 croisements. Ce sont des **quartets corrélés**, pas autant de
  choix d'arrangement indépendants.
- Pour l'instant seuls les mouvements entre attaques synchronisées,
  dans la même voix/portée notée, sont probants. Les relais de mélodie,
  la conduite à travers des rythmes différents, les résolutions
  harmoniques et l'audition ne sont **pas implémentés**.
- Prochaine expérience : confronter la modification d'une note à un
  contexte harmonique *annoté*, puis écouter deux versions contrôlées
  avant de préférer l'une à l'autre.

### G3–G6 — à consolider après les premiers mécanismes

- **G3 :** approfondir la conduite des voix (premier mécanisme descriptif
  livré), puis harmonie, tonalité et fonctions d'orchestre.
- **G4 :** phrases, périodes, sections, développements, formes longues.
- **G5 :** articulations, ralentissements, nuances et timbres sur les vues
  partition/performance/audio correctement alignées.
- **G6 :** intégration des axes sans masquer les contradictions ou sources
  absentes ; plusieurs analyses concurrentes permises.

## Protocole obligatoire avant toute « découverte »

1. Source primaire et droit de redistribution vérifiés par **fichier**.
2. Définition opérationnelle de la cible (ce qui est réellement annoté).
3. Séparation des œuvres apparentées dans la sélection et le test.
4. Baseline triviale et témoin négatif.
5. Mesures détaillées (pas juste une moyenne) et examen des erreurs.
6. Reproductibilité des sorties, tests et budget explicite.
7. Décision : **implémenté**, **exploratoire**, **rejeté** ou **inconnu**.

Référence technique : [contrats scientifiques](research-evidence-gates.md).
Corpus : [audit orchestrations](orchestral-corpus-audit.md).

## Exécution légère actuelle

```bash
python -m pip install 'mido>=1.3,<2'
python -m unittest discover -s tests -p 'test_grammar_*.py'
python -m scripts.g2_motif_probe --top 3
python -m scripts.orchestral_doubling_probe --top 3
python -m scripts.orchestral_voice_leading_probe --top 2
python -m unittest discover -s tests -p test_orchestral_grammar_probe.py
python -m unittest discover -s tests -p test_score_inventory.py
python scripts/orchestral_grammar_probe.py
python scripts/score_midi_orchestration_audit.py
```

Seuls les mécanismes qui servent une couche grammaticale et leurs tests
justifiés doivent subsister dans le dépôt.
