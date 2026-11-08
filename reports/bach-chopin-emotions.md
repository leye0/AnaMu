# AnaMu — analyse de compositions connues

**Estimations algorithmiques uniquement.** Ces deux œuvres n'ont pas
d'annotations humaines temporelles associées dans VGMIDI ; ce rapport
ne mesure donc **pas** leur justesse émotionnelle. Le modèle est calibré
sur d'autres pièces annotées par des humains.

Modèle SHA-256 : `f5c536d9f1165e781b93d20ad7dd33bf180788dbcbf63bf07d004af24708d98f`.

| Composition | Mesures | Valence moyenne | Activation moyenne | Variables observées / apprises | jSymbolic original |
|---|---:|---:|---:|---:|---|
| Bach — BWV 66.6, chorale | 9 | +0.107 | -0.092 | 1193/1198 | ok |
| Chopin — Mazurka op. 6 no. 2 | 72 | +0.366 | +0.011 | 774/1198 | unavailable:no_original_java_output |

## Provenance et limites des moteurs

### Bach — BWV 66.6, chorale

- `partitura` : `ok`
- `music21` : `ok`
- `theory_probes` : `ok`
- `melody_features` : `ok`
- `melody_method` : `['strict_monophonic_track']`
- `jsymbolic` : `ok`
- `expectancy_baseline` : `ok`
- `temporal_memory_derivatives` : `104`
- **Limite** : estimated human-perceived valence/arousal, NOT measured human emotions
- **Limite** : VGMIDI piano calibration may not generalize to other eras, styles or instrumentation

### Chopin — Mazurka op. 6 no. 2

- `partitura` : `ok`
- `music21` : `ok`
- `theory_probes` : `ok`
- `melody_features` : `ok`
- `melody_method` : `['unverified_upper_pitch_skyline']`
- `jsymbolic` : `unavailable:no_original_java_output`
- `expectancy_baseline` : `ok`
- `temporal_memory_derivatives` : `14`
- **Limite** : original jSymbolic unavailable: model imputes its features
- **Limite** : estimated human-perceived valence/arousal, NOT measured human emotions
- **Limite** : VGMIDI piano calibration may not generalize to other eras, styles or instrumentation
- **Limite** : original_jsymbolic_unavailable:TimeoutExpired
- **Limite** : notated order only; malformed source repeats not performed/unrolled

## Lecture

Chaque point du graphique correspond à une mesure MIDI, et les valeurs
vont de −1 à +1. L'analyse peut refléter des régularités apprises sur
VGMIDI, mais ni le transfert au répertoire classique ni les émotions de
ses auditeurs n'ont été validés sur Bach ou Chopin.
