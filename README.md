# AnaMu — Analyse Musicale

AnaMu est un projet de recherche visant à comprendre **comment les
enchaînements de notes, d'accords, de rythmes et de motifs produisent des
attentes, des surprises, des tensions et des résolutions**, puis à étudier
leur relation avec les émotions **réellement annotées par des humains**.

**Direction scientifique (v1.0, 7 novembre 2026) :** développer d'abord les
algorithmes issus des théories musicales et psychologiques sur le **MIDI
symbolique brut**. Déterminer ensuite le corpus nécessaire à la validation
de chaque mécanisme. Les rapprochements MIDI↔audio et **Demucs sont reportés**.

- **[Feuille de route v1.0](docs/roadmap.md)** — priorités, jalons et état réel.
- **[Théorie → algorithmes](docs/theory-to-algorithms.md)** — références
  académiques, entrées/sorties, modèles, expériences et critères de preuve.
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

Exécuter localement les tests légers :

```bash
python -m pip install 'mido>=1.3,<2'
python -m unittest tests.test_symbolic_expectation -v
```

Le workflow GitHub Actions `symbolic-theory-tests.yml` exécute les mêmes tests
sans télécharger de corpus ni traiter d'audio.

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

Le projet n'a pas encore démontré de capacité de prédiction d'émotions à
partir d'une séquence musicale. Les prochaines étapes visent précisément à
construire, comparer et valider ces mécanismes.
