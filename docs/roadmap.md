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
| **Partition MusicXML** | Inventaire des parties et des familles instrumentales déclarées | Pas de reconstruction des reprises, de rôles ou d'alignement aux notes MIDI |
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

### G3–G6 — à ouvrir après les contrats précédents

- **G3 :** harmonie, tonalité, conduite des voix et fonctions d'orchestre.
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
python -m unittest discover -s tests -p test_orchestral_grammar_probe.py
python -m unittest discover -s tests -p test_score_inventory.py
python scripts/orchestral_grammar_probe.py
python scripts/score_midi_orchestration_audit.py
```

Seuls les mécanismes qui servent une couche grammaticale et leurs tests
justifiés doivent subsister dans le dépôt.
