# PIAST Tense → IsoVAT tension : transfert entre corpus

**Exploratoire ; aucun ajustement des modèles sur IsoVAT.**

| Modèle | Paires correctement classées / 30 | Ordres exacts / 10 |
|---|---:|---:|
| baseline | 17 | 2 |
| distribution | 17 | 2 |
| temporal | 15 | 2 |
| Témoin : note_density | 20 | 3 |
| Témoin : cloud_diameter | 24 | 6 |

Contrôle de sélection parmi les trois modèles : p permutations par groupe = 0.4310 pour les paires, 0.7158 pour les ordres complets.

## Détail des classements humains

| Triplet | Ordre humain | Baseline | Distribution | Séquence |
|---|---|---|---|---|
| T-01 | HML | LMH | LMH | LMH |
| T-02 | HLM | HML | HML | HML |
| T-03 | HML | HLM | HLM | LHM |
| T-04 | HML | LHM | HLM | LHM |
| T-05 | HML | HLM | HML | HML |
| T-06 | LMH | MHL | MHL | MHL |
| T-07 | MHL | MHL | MHL | MHL |
| T-08 | MLH | LMH | LMH | LMH |
| T-09 | MHL | LMH | LHM | LHM |
| T-10 | HML | HML | HLM | HLM |

IsoVAT = 30 MIDI composés en groupes de trois de même genre et instrumentation ; les ordres de référence viennent des auditeurs, **pas** des noms H/M/L.
Les deux taxonomies émotionnelles et les domaines musicaux diffèrent : une réussite serait encourageante, pas une preuve d'une loi universelle.