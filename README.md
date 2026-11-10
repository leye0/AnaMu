# AnaMu — grammaire musicale explicable

AnaMu vise une **analyse musicale de niveau universitaire, vérifiable et
largement non fondée sur le machine learning**. Son objectif est de découvrir
et décrire les règles d'organisation d'une œuvre : notes, rythmes, harmonie,
voix, motifs, phrases, forme, instruments, orchestration et expression.

Ce projet **n'est plus centré sur la prédiction de l'émotion « mystérieuse »**.
Les anciens outils de classification émotionnelle ne définissent plus son
architecture ni ses objectifs.

## Lire le projet

1. **[Objectifs et critères de réussite](docs/OBJECTIVES.md)** — le contrat de
   recherche, les axes de musique étudiés et ce que nous refusons d'inférer.
2. **[Architecture académique de la grammaire](docs/music-grammar-research-program.md)**
   — ontologie, sources, opérateurs et fondements théoriques.
3. **[Feuille de route actuelle](docs/roadmap.md)** — acquis mesurés, travaux
   manquants, prochaine expérience G2.
4. **[Index documentaire](docs/README.md)** — documents actifs et études
   scientifiques pertinentes à la grammaire.
5. **[Grammaire de composition et orchestration](docs/composition-grammar.md)**
   — comment tester la valeur constructive des découvertes, jusqu'aux
   contre-épreuves d'écoute.

## Trois sources, trois types de vérité

| Source | Ce qui peut être observé | Ce qui ne peut pas être affirmé sans autre preuve |
|---|---|---|
| **Partition** (MusicXML/MEI) | Notation, parties, rythme, silences, indications expressives | Exécution et son acoustique réels |
| **MIDI** | Événements, hauteurs, durées de touches, pistes, contrôleurs, tempo encodé | Timbre réel, niveau sonore perçu, instrumentation correcte par simple nom de piste |
| **Audio** (étape ultérieure) | Forme d'onde, enveloppe, spectre et intensité mesurée | Voix/instruments/notes exacts sans analyse et incertitude |

Chaque résultat doit rester associé à sa **source**, son **statut**
(*observé, noté, annoté, inféré ou inconnu*) et ses **preuves**. Nous acceptons
plusieurs analyses possibles, sans inventer de certitude.

## État réellement implémenté (10 novembre 2026)

- **G0 MIDI** : conservation des octets, pistes, événements, notes
  non ambiguës, tempo, contrôleurs et diagnostics
  (`anamu/grammar_foundation.py`).
- **G1 partiel** : relations temporelles exactes d'Allen,
  `SEQUENCE`/`PARALLEL` et transformations déterministes avec correspondances
  fournies (`anamu/grammar_relations.py`).
- **G2 exploratoire** : repérage autonome de répétitions exactement
  transposées et/ou dilatées dans des fenêtres d'attaques MIDI, avec
  provenance et preuves `TRANSFORM` G1 (`anamu/grammar_motifs.py`). Les
  groupements sont **candidats**, pas des thèmes ou phrases reconnus.
- **Orchestration notée exploratoire** : lecture MusicXML des hauteurs
  écrites/sonnantes, doublures strictes entre pupitres, et prédiction
  contrefactuelle de notes masquées (`anamu/score_texture.py`,
  `anamu/orchestral_counterfactual.py`). Pas encore de jugement esthétique.
- **Conduite des voix** : mouvements exacts entre deux parties notées
  (contraire, similaire, parallèle, oblique, statique), croisements et
  variantes hypothétiques d'une note ; jamais de jugement automatique
  de qualité (`anamu/orchestral_voice_leading.py`).
- **G3 harmonique structurel** : sonorités notées locales, basses sonnantes,
  formes exactes de triades/septièmes et effet d'une variante de voix sur
  toute la texture (`anamu/orchestral_harmony.py`). Fonctions tonales
  et notes étrangères **non identifiées**.
- **G3 gestes mélodiques** : orthographe des hauteurs écrites conservée,
  figures conjointes candidates de passage et broderie, avec inspection
  des notes d'accompagnement à chaque attaque
  (`anamu/orchestral_ornaments.py`). Ce ne sont **pas** des étiquettes
  de dissonance ou des jugements de qualité.
- **Corpus orchestral** : deux mouvements de symphonies Beethoven, leurs MIDI,
  deux partitions MusicXML de référence, manifestes avec licences et SHA-256.
- **Contrôle des sources** : comparaison des familles instrumentales déclarées
  dans les deux éditions (`anamu/score_inventory.py`).
- **Non implémenté** : repérage autonome **validé** des voix, motifs, phrases,
  fonctions harmoniques, formes, timbres et expressions perceptives ; couches
  partition/performance/audio alignées.

Un résultat actuel illustre le besoin de prudence : les partitions de
Beethoven 5/I et 7/II contiennent **18 et 19 parties**, contre **12 pistes
MIDI actives** chacune. Les noms MIDI mentionnent des cors anglais là où
les partitions déclarent des cors et trompettes. Il s'agit d'un écart de
**déclarations**, pas encore d'une preuve de notes manquantes.

## Reproduire les validations de la grammaire

```bash
python -m pip install 'mido>=1.3,<2'
python -m unittest discover -s tests -p 'test_grammar_*.py'
python -m scripts.g2_motif_probe --top 3
python -m scripts.orchestral_doubling_probe --top 3
python -m scripts.orchestral_voice_leading_probe --top 2
python -m scripts.orchestral_harmonic_context_probe --top 3
python -m scripts.orchestral_ornament_probe --top 3
python -m unittest discover -s tests -p test_orchestral_grammar_probe.py
python -m unittest discover -s tests -p test_score_inventory.py
python scripts/orchestral_grammar_probe.py
python scripts/score_midi_orchestration_audit.py
```

Les composants musicologiques additionnels (analyse tonale, attente,
extraction de caractéristiques, expression, études indépendantes) sont
**exploratoires et réutilisables**, pas des couches G2–G6 déjà validées.
Le workflow de tests symboliques vérifie leurs invariants séparément des
contrôles G0/G1 et orchestraux.

## Principes de développement

- **Théorie académique identifiée → contrat vérifiable → algorithme générique
  → témoin négatif → évaluation indépendante.**
- Règles explicables d'abord, apprentissage statistique seulement lorsque
  sa nécessité et ses données d'évaluation sont établies.
- Aucun traitement spécial pour une œuvre, un compositeur ou un genre.
- Préserver les observations brutes et les découvertes négatives.
- Ne pas présenter des partitions MIDI comme des performances humaines.

Voir les [objectifs détaillés](docs/OBJECTIVES.md) pour les critères de
sortie de chaque couche.
