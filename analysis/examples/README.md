# Parcours réels de la première version

Ces rapports sont produits par le code du volet, à partir de fichiers déjà présents dans les cours et le corpus. Ils démontrent une exécution reproductible, sans constituer une validation musicale indépendante.

| Rapport | Objet |
|---|---|
| [Harmonie](harmony.md) | Lectures augmentées et diminuées concurrentes, sans fonction tonale inventée |
| [Pédales](pedal.md) | Commandes CC64 et durées de touches, distinctes des durées sonores |
| [Rythme](rhythm.md) | Grille encodée et récurrences; aucune affirmation de groove perçu |
| [Profil inconnu](undeclared.md) | Lectures de hauteurs bloquées sans contrat MIDI explicite |
| [Opéra](opera.md) | Parcours d’une œuvre du corpus : 1 439 attaques lues, sans alignement vocal inféré |

Chaque `.json.gz` adjacent contient le rapport détaillé avec événements, provenance, alternatives, limites et audit de chaque document de cours. [runs.json](runs.json) conserve les entrées, profils et empreintes pour reproduire les commandes depuis `analysis/` :

```sh
.venv/bin/python -m anamu_analysis analyse ../<input> --midi-profile <midi_profile> --out .cache/reproduction
```

Remplacer les deux paramètres par ceux d’une ligne de `runs.json`. Le profil `gm1` est déclaré pour les exemples pédagogiques concernés; `unknown` reste le défaut. Les rapports qui l’utilisent ne prouvent pas à eux seuls la conformité complète du fichier à GM1.
