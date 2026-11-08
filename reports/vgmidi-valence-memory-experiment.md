# AnaMu — mémoire temporelle de la valence : expérience exploratoire

**Pas un nouveau modèle appris, ni une preuve indépendante.** Les mêmes analyses d'émotion, calculées antérieurement à partir des MIDI, sont comparées aux mêmes annotations humaines.

Hypothèse : la valence persiste d'une mesure à l'autre. Mémoire causale fixée à `alpha=0.2`. L'activation reste inchangée. Il s'agit d'une hypothèse temporelle inspirée des modèles de tension à mémoire (Farbood), **pas** de leur reproduction originale.

Le coefficient a été choisi en regardant le premier groupe de dix morceaux. Le deuxième groupe avait déjà été examiné lors d'une expérience antérieure : cette répétition confirme une tendance exploratoire, mais ne constitue **pas** un test indépendant vierge.

| Groupe de 10 morceaux | Valence : erreur initiale | Valence : avec mémoire | Corrélation temporelle initiale → mémoire | Activation (inchangée) |
|---|---:|---:|---:|---:|
| Premiers dix | 0.263 | 0.255 | +0.20 → +0.28 | 0.150 |
| Dix complémentaires | 0.177 | 0.169 | +0.16 → +0.21 | 0.193 |

**Attention : effet irrégulier entre les morceaux.** Les intervalles ci-dessous sont des intervalles bootstrap exploratoires (20 000 rééchantillonnages de morceaux) :

| Groupe | Morceaux améliorés | Gain moyen V | Intervalle bootstrap 95 % du gain |
|---|---:|---:|---:|
| Premiers dix | 7/10 | +0.008 | [-0.0005 ; +0.0204] |
| Dix complémentaires | 4/10 | +0.007 | [-0.0086 ; +0.0240] |

## Détail par morceau

| Groupe | Morceau | Mesures | Erreur V initiale | Erreur V mémoire | Gain (positif = mieux) |
|---|---|---:|---:|---:|---:|
| Premier | Chrono Trigger | 136 | 0.350 | 0.347 | +0.002 |
| Premier | Costa Del Sol | 32 | 0.400 | 0.408 | -0.008 |
| Premier | Tifa | 55 | 0.055 | 0.058 | -0.002 |
| Premier | Zeppelin | 35 | 0.172 | 0.166 | +0.005 |
| Premier | The Opened Way | 59 | 0.352 | 0.351 | +0.002 |
| Premier | Forest of Illusion | 16 | 0.183 | 0.178 | +0.005 |
| Premier | Cremia's Wagon Ride | 18 | 0.102 | 0.095 | +0.007 |
| Premier | Stone Temple Tower | 30 | 0.286 | 0.227 | +0.059 |
| Premier | Goron City | 32 | 0.217 | 0.220 | -0.003 |
| Premier | Hyrule Castle Courtyard | 24 | 0.508 | 0.497 | +0.011 |
| Complémentaire | Click Clock Wood | 39 | 0.382 | 0.388 | -0.006 |
| Complémentaire | Isle O Hags Cauldron Keep | 62 | 0.047 | 0.046 | +0.001 |
| Complémentaire | Terry | 38 | 0.249 | 0.250 | -0.002 |
| Complémentaire | Overworld | 57 | 0.135 | 0.140 | -0.005 |
| Complémentaire | Those Chosen By the Planet | 34 | 0.127 | 0.085 | +0.042 |
| Complémentaire | Trail of Blood | 36 | 0.119 | 0.087 | +0.033 |
| Complémentaire | Crossing | 55 | 0.212 | 0.215 | -0.004 |
| Complémentaire | Space Armada | 20 | 0.236 | 0.181 | +0.055 |
| Complémentaire | Stone Tower Temple | 30 | 0.134 | 0.172 | -0.038 |
| Complémentaire | Temple of Time | 40 | 0.126 | 0.127 | -0.001 |

## Conclusion

Cette mémoire diminue les erreurs moyennes sur les deux groupes, mais **les deux intervalles comprennent zéro**. Les gains peuvent être dus à quelques morceaux; ce n'est pas encore une amélioration statistiquement robuste ni une solution aux grandes erreurs de valence. Une vraie validation nécessitera de sélectionner l'hyperparamètre **uniquement sur les morceaux de validation**, puis de le tester une fois sur de nouveaux morceaux non inspectés.
