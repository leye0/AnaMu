# AnaMu — état de la recherche, sans liste concurrente

**La seule feuille de travaux à cocher est maintenant
[todo-university-coverage.md](todo-university-coverage.md).**
Elle dérive du [référentiel comparé des cursus de composition](university-curriculum.md)
et des [objectifs scientifiques](OBJECTIVES.md). Ce document consigne
uniquement **ce qui a été effectivement réalisé** et les limites des preuves.

## Incréments observés, non certifications universitaires

| Capacité | Résultat implémenté | Ce que cela ne démontre pas |
|---|---|---|
| MIDI G0 | Conservation des sources, événements, pistes, temps, contrôleurs, vélocités, appariements de notes sûrs | Timbre, interprétation, voix réelle |
| Relations G1 | Treize relations d'Allen, simultanéité, séquence, transposition et mise à l'échelle exactes sous correspondance fournie | Forme, motif entendu, intention |
| Motifs G2 exploratoires | Signatures candidates de fenêtres MIDI répétées par transposition/échelle temporelle uniforme | Thème, phrase, fonction, segmentation reconnue par un expert |
| Partition G0 exploratoire | Inventaire MusicXML, hauteurs écrites/sonnantes, voix et accords, orthographe ; fragments de notes liées signalés | Reprises et tenues transmesure reconstruites ; alignement note par note MIDI/audio |
| Orchestration exploratoire | Doublures exactes entre parties, reconstruction diagnostique de notes masquées | Identité perceptive, savoir d'orchestration complet, jouabilité ou qualité sonore |
| Conduite des voix G3 exploratoire | Quartets notés à attaques synchronisées, directions, croisements et variantes d'une note | Contrepoint à espèces/fugue, contraintes historiques et mouvements asynchrones |
| Harmonie G3 exploratoire | Verticalités, basses, compatibilité triades/septièmes, changement d'un contexte sous variante | Tonalité, fonction, cadence, notes étrangères déterminées |
| Mélodie G3 exploratoire | Figures conjointes candidates de passage et de broderie avec accompagnement observé | Statut harmonique, analyse des ornements complète ou expression |
| Corpus | Beethoven 5/I et 7/II : MIDI, MusicXML, licences, empreintes et audit des divergences | Couverture de styles, validation hors compositeur, édition identique |

Les rapports chiffrés des expériences de doublures, de conduite des voix,
d'harmonie et d'ornements, ainsi que leurs commandes reproductibles,
demeurent dans [composition-grammar.md](composition-grammar.md) ; les
expériences G0–G2 demeurent documentées dans
[music-grammar-research-program.md](music-grammar-research-program.md).
Les études empiriques accessibles via [l'index](README.md) restent des
**références**, pas des validations des couches intégrées.

## Prochaine vraie priorité

**A01–A12 : terminer l'inventaire vérifiable des trois programmes** avant de
choisir un nouvel algorithme. Il faudra ensuite construire la matrice
`cours → objectif pédagogique → compétence analysable → preuve`
et traiter les lacunes en suivant le [TODO](todo-university-coverage.md).
L'ordre des expériences dépendra des *manques du cursus*, des prérequis
musicaux et des jeux de référence, pas de la facilité à écrire un script.

Les découvertes anciennes se réexécutent avec les
[règles de preuve](research-evidence-gates.md). Les expériences de notes
masquées sont des **diagnostics internes**, pas le début d'un moteur de
composition. Aucun générateur de musique originale ne figure parmi les
travaux autorisés avant la porte L01–L05.

## Exécuter les vérifications actuelles

```bash
python -m pip install 'mido>=1.3,<2'
python -m unittest discover -s tests -p 'test_*.py'
python scripts/validate_project_docs.py
python -m scripts.g2_motif_probe --top 3
python -m scripts.orchestral_doubling_probe --top 3
python -m scripts.orchestral_voice_leading_probe --top 2
python -m scripts.orchestral_harmonic_context_probe --top 3
python -m scripts.orchestral_ornament_probe --top 3
```

Une suite verte prouve que ces mécanismes fonctionnent selon leurs tests,
**pas** que les compétences du TODO sont couvertes : toutes les cases
restent ouvertes jusqu'aux audits externes et tests adaptés.
