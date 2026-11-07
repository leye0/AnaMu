# AnaMu — Analyse Musicale

AnaMu est un projet de recherche visant à comprendre **comment les
enchaînements de notes, d'accords, de rythmes et de motifs produisent des
attentes, des surprises, des tensions et des résolutions**, puis à étudier
leur relation avec les émotions **réellement annotées par des humains**.

**Direction scientifique (v1.0, 7 novembre 2026) :** développer d'abord les
algorithmes issus des théories musicales et psychologiques sur le **MIDI
symbolique brut**. Déterminer ensuite le corpus nécessaire à la validation
de chaque mécanisme. Les rapprochements MIDI↔audio et **Demucs sont reportés**.

- **[Feuille de route v1.1](docs/roadmap.md)** — priorités, jalons et état réel.
- **[Théorie → algorithmes](docs/theory-to-algorithms.md)** — références
  académiques, entrées/sorties, modèles, expériences et critères de preuve.
- **[Moteur émotionnel et couverture des algorithmes](docs/emotion-engine.md)** —
  23 mécanismes distincts étudiés, logiciels de recherche disponibles,
  intégration, expérience EMOPIA sans fuite et critères de validité.
- **[Audits historiques](docs/audit-p0.md)** ·
  [jointure exacte](docs/p1-exact-join.md) ·
  [audit instrumental XMIDI](docs/p1-instrument-audit.md) ·
  [protocole audio reporté](docs/p1-drum-audio-validation-plan.md).

## Objectifs

1. Analyser la composition de pièces connues (Bach, Chopin, puis pop)
   par des mécanismes musicaux explicables.
2. Étudier **les transformations musicales dans le temps**, et non seulement
   des associations simplistes « mineur / lent / triste ».
3. À terme, générer des compositions symboliques originales à partir de
   contraintes d'émotions, d'instrumentation, de forme et de traits stylistiques.

## Premier noyau expérimental

La base `anamu/` comporte :

- `midi_views.py` : lit directement des octets MIDI et extrait **uniquement
  les parties monophoniques non ambiguës comme candidates**, sans les déclarer
  automatiquement « mélodie principale ».
- `expectation.py` : baseline probabiliste à ordre variable calculant la
  probabilité conditionnelle d'un événement symbolique, sa surprise et
  l'entropie *avant* cet événement. **Ce n'est pas une implémentation d'IDyOM
  ni un détecteur d'émotions déjà validé.**
- `tests/test_symbolic_expectation.py` : fixtures contrôlées, invariants et
  rejets des parties MIDI ambiguës.
- `theory_features.py` : adaptateurs pour les **vrais outils** Partitura
  (tension tonale Herremans/Chew), music21 (tonalité Krumhansl-Schmuckler,
  sonorités et degrés romains hypothétiques), lecture d'export IDyOM **original**.
- `tempo_map.py` : conversion MIDI beats → secondes de performance, avec
  prise en compte des changements de tempo.
- `melody_toolbox.py` : **bibliothèque universitaire réelle**
  [`melody-features` 1.3.3](https://dmwhyatt.github.io/melody-features/),
  qui rassemble des centaines de descripteurs de mélodie issus de théories
  diverses. Sur neuf notes de test : **278 valeurs/structures, 12 familles** ;
  courbe temporelle des **cinq mesures Narmour** par triplet. Rejette les
  pistes polyphoniques sans séparation de voix fiable. Ce ne sont pas des
  étiquettes émotionnelles ni une exécution d'IDyOM original.
- `emopia.py` : inventaire du corpus EMOPIA directement à partir de ses noms
  de fichiers, hash, rejets, séparation reproductible de **chansons**.
- `emotion_evaluation.py` : baselines sur entraînement seulement et score sur
  test réservé, macro-F1 quatre classes, couverture, abstentions, confusion.
- `scripts/run_original_idyom.py` : configuration/lancement *optionnel* de
  l'outil IDyOM via py2lispIDyOM et SBCL. Le module
  `idyom_guardrails.py` vérifie les empreintes de toutes les pistes de
  préentraînement/test, refuse les doublons exacts et bloque EMOPIA dans le
  préentraînement. Aucun résultat IDyOM publié pour le moment.
- `idyom_dat.py` et `scripts/import_idyom_dat.py` : lecture du **format
  original `.dat` d'IDyOM** et conversion JSON sans recalculer ses modèles.
  Les surprises, entropies, probabilités de continuations, gains d'information,
  vues mélodiques/rythmiques et valeurs absentes sont conservés par note et
  par morceau. Lecture testée sur le schéma d'un exemple des auteurs, mais
  **aucun moteur Lisp original n'a encore tourné dans notre infrastructure**.
- `jsymbolic_ace.py` : parseur du **format ACE XML original 1.1** de
  jSymbolic, avec fonctions multi-valeurs et fenêtres temporelles natives.
  L'analyse Java 2.2 a un smoke test **facultatif dans le workflow habituel**,
  sur un MIDI polyphonique synthétique et avec archive officielle vérifiée
  par SHA-256 ; aucune extraction audio.
- `scripts/extract_tonal_tension.py`, `scripts/extract_harmony.py`,
  `scripts/emopia_benchmark.py` : exécutions locales et reproductibles.

Exécuter localement les tests légers :

```bash
python -m pip install 'mido>=1.3,<2'
python -m unittest tests.test_symbolic_expectation -v
```

Pour tester les **moteurs publiés** et préparer l'évaluation EMOPIA :

```bash
python -m pip install 'partitura>=1.8,<2' 'music21>=9,<12'
python -m unittest discover -s tests -p 'test_emotion_research.py' -v
python -m scripts.extract_tonal_tension /chemin/piano.mid
python -m scripts.extract_harmony /chemin/piano.mid
python -m scripts.emopia_benchmark /chemin/EMOPIA_2.2 --manifest-out emopia-split.jsonl
```

Pour extraire les mesures mélodiques académiques directement d'un MIDI :

```bash
python -m pip install 'melody-features==1.3.3'
python -m scripts.extract_melody_features /chemin/melodie.mid > melodia.json
python -m unittest discover -s tests -p 'test_melody_toolbox.py' -v
python -m scripts.import_idyom_dat /chemin/resultats-idyom.dat --json-out idyom-events.json
```

Le corpus de référence implicite de `melody-features` et la fidélité des
réimplémentations sont à auditer avant exploitation statistique. Le résultat
JSON garde ses valeurs inconnues et la provenance de chaque piste.

Le workflow GitHub Actions `symbolic-theory-tests.yml` exécute ces tests sur
des MIDI synthétiques, **sans télécharger de corpus ni traiter d'audio**.
La vérification Java originale peut être activée manuellement avec le
paramètre `jsymbolic_smoke` ; elle télécharge **seulement l'outil publié**,
dans une exécution séparée et plafonnée. Cette vérification plus coûteuse
n'est pas lancée à chaque modification de code.

## Corpus et qualité

- **Qualité avant quantité** : même 500 ou 2 000 MIDI corrects peuvent suffire
  à un protocole ; **10 000 n'est pas un minimum**.
- **Corpus à la demande** : chaque algorithme explicite d'abord ses besoins ;
  ne pas retraiter les MIDI s'il peut les consommer directement.
- **Annotation humaine séparée de l'inférence** : XMIDI (label global),
  EMOPIA (extraits piano), DEAM (émotions temporelles, surtout audio), PMEmo
  (annotations et physiologie). Ne pas inventer de vérités temporelles.
- **Précision plutôt que couverture** : conserver les refus, niveaux
  d'incertitude, provenances et contrôles négatifs.
- **Théories documentées** : Meyer, Huron, Narmour, Schellenberg, Pearce/IDyOM,
  Lerdahl/Krumhansl, Farbood, Herremans/Chew, Steinbeis, Egermann, Cheung.
- **Validation honnête** : séparer les œuvres entre entraînement et test,
  mesurer l'apport de l'ordre des événements, comparer aux baselines statiques,
  publier les échecs ; jamais de causalité déclarée sur simple corrélation.

## État préexistant (conservé)

- XMIDI : ZIP de **449 632 771 octets**, accès partiel par requêtes HTTP Range.
- Une correspondance MD5 XMIDI↔GigaMIDI confirmée sur le pilote ; aucune
  identité d'artiste, aucun taux de couverture global démontré.
- Audit de 200 XMIDI, **199 analysés**. Dans l'échantillon aléatoire de 100,
  **64** avaient au moins 16 notes dans chacune des parties guitare,
  basse et batterie. Cette richesse instrumentale **ne prouve pas** la
  fidélité de l'arrangement à un enregistrement.
- Ancien protocole Demucs/ADTOF/Omnizart écrit, **jamais exécuté** ; ses
  scripts et rapports restent consultables à titre historique.

**Important :** la tension musicale et les accords sont maintenant extraits
par des bibliothèques existantes sur des fichiers de test. **Aucun score de
prédiction émotionnelle sur les annotations humaines d'EMOPIA n'a encore été
mesuré.** L'entraînement émotionnel, la fusion temporelle des mécanismes, les
ablations et la validation humaine indépendante restent à construire.
