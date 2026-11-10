# Université de Montréal — premier audit du B. Mus. Composition (A26)

**État : inventaire du catalogue public vérifié ; plans de cours, exercices,
préalables, lectures et appréciation experte non vérifiés.** Aucun item du
[TODO universitaire](todo-university-coverage.md) ne devient « terminé ».

Source primaire : [UdeM, B. Mus. Composition, structure du programme, version
10 (A26)](https://admission.umontreal.ca/programmes/baccalaureat-en-musique-composition/structure-du-programme/),
dernière modification affichée au **10 novembre 2026**.

## 1. Décompte du catalogue, pas du savoir maîtrisé

Le [relevé intégral des codes, intitulés, crédits et blocs](data/udem-composition-a26.json)
contient **190 entrées** publiées, dont **22 cours obligatoires totalisant
63 crédits**. Les **27 crédits à option** sont choisis dans plusieurs blocs :
les 168 autres entrées sont des *possibilités*, pas 168 cours à suivre.

| Bloc UdeM | Règle de choix affichée | Cours listés | Particularité |
|---|---|---:|---|
| 75A | 63 crédits obligatoires | 22 | Tronc commun intégral du programme |
| 75B | 6 à 9 crédits | 6 | Solfège et dictée, selon classement |
| 75C | 6 crédits | 6 | Un même parcours : instrumental, mixte **ou** image |
| 75D | Jusqu'à 6 crédits | 21 | Histoire, musicologie, arts et société |
| 75E | Jusqu'à 6 crédits | 16 | Harmonie, contrepoint, analyse, orchestration, jazz, psychoacoustique |
| 75F | Jusqu'à 6 crédits | 15 | Électroacoustique, studio, informatique, maquettes MIDI |
| 75G | Jusqu'à 3 crédits | 8 | Ateliers professionnels et projets/stages |
| 75H | Jusqu'à 4 crédits | 96 | Direction, ensembles et techniques instrumentales |

**Attention au piège du décompte :** la somme des plafonds de blocs
optionnels **ne représente pas** les 27 crédits optionnels réellement
suivis, et toutes les spécialisations ne sont pas suivies simultanément.
Le cours MTE 12041 est affiché à **0 crédit**, associé à une suite de
6 crédits ; le garder à zéro plutôt que « réparer » arbitrairement les
données. De même, certaines offres peuvent varier d'une session à l'autre.

## 2. Cartographie initiale des 22 cours obligatoires

Les correspondances ci-dessous relient les **sujets décrits publiquement**
aux familles du TODO ; elles ne prouvent **ni** que les contenus entiers
sont connus **ni** que nos mécanismes les comprennent. Les cours de
création, studio et pratique contiennent des apprentissages humains
irréductibles à un parseur de partitions.

| Cours obligatoire | Savoir public pertinent, paraphrasé | TODO concerné |
|---|---|---|
| MCT 1601, MCT 1602 | Travail de création instrumentale guidé | E, G, J, K |
| MCT 3011, MCT 3012 | Écriture de la tradition modale/tonale et ses transformations | C, D, E, J |
| MTE 1110, MTE 1111 | Contrepoint vocal en espèces à 2 puis 3 voix | D, C |
| MTE 1205, MTE 1206 | Analyse des courants de la première puis seconde moitié du XXe siècle | H, E, J |
| MTE 1220, MTE 1221 | Pratique et analyse de l'harmonie tonale | C, D |
| MTE 1403, MTE 1404 | Modes, séries, hétérophonie, polyrythmies et processus spectraux/algorithmiques | H, F, I |
| MTE 1503 | Création électroacoustique guidée | H, I, K |
| MTE 2114 | Ambitus, registres, timbres, dynamique, techniques et articulations instrumentales | G, I |
| MTE 2115 | Répartition verticale/horizontale, doublures, mélanges et pupitres | G, D, C |
| MUL 1117 | Langages et contexte esthétique des musiques récentes | J, H |
| MUS 1300 | Vibration, résonance, acoustique des salles et mesures du son | I |
| MUS 1321 | Analyse/synthèse et traitement numérique du signal | I |
| MUS 3101X | Démarches spectrales, assistées par ordinateur et interactives | H, I |
| MUS 3324X | Structuration musicale par programmation graphique et contrôle temps réel | H, I |
| MUS 3411, MUS 3412 | Forums, présentation critique et échange professionnel autour de la création | J, K |

La totalité du **tronc obligatoire** est présente dans le JSON. Il reste
à définir, pour chaque ligne, les résultats d'apprentissage précis et
leurs supports : une simple famille de TODO n'est pas une matrice achevée
`cours → résultat → compétence → preuve`.

## 3. Lacunes que révèle l'inventaire optionnel

Les descriptions publiques des cours optionnels ajoutent des sujets
qu'un programme « analyse symbolique MIDI » risquerait d'oublier :

- **MTE 2110/2111** : contrepoint à quatre voix, canon et fugue.
- **MTE 2210/2211** : déchiffrage analytique d'orchestre et formes tonales.
- **MTE 3114/3115/3115X** : instrumentation d'orchestre complet, réduction,
  matériel d'orchestre et orchestration stylistique selon l'époque.
- **MUS 3321** : perception psychoacoustique de l'intensité, de la hauteur,
  de la dissonance, du timbre et de l'espace.
- **MUS 3127X** : programmation expressive de maquettes MIDI orchestrales,
  échantillonnage, mixage, placement spatial. Le contrôle des articulations,
  des vélocités et des enveloppes d'un rendu ne se déduit pas de simples notes.
- **MCT 3511X/3512X** : composition pour l'image, dramaturgie, leitmotivs,
  textures, silences et relation musique/écran.
- **MTE 1315/1316 et MTE 2315/2316** : harmonie et arrangement jazz,
  substitutions, voicings, réharmonisation et écriture de sections.
- **MTE 3300, MUS 1217** : écoute et grammaires perceptives de l'objet
  sonore électroacoustique, distinctes du seul traitement de hauteur.
- **EMU 1310, EMU 2312** : direction d'ensemble et lecture/pratique ;
  compétences humaines à expliciter comme limites et évaluations dédiées.

Ces options sont **identifiées**, non validées ; notre objectif de
connaissance exige d'en examiner **toutes les 168**, même celles que le
parcours diplômant ne permet pas d'accumuler. Nous intégrerons à la matrice
chaque acquis utile (sans feindre que les étudiants suivent toutes ces
variantes) ; toute exclusion demandera une justification précise. Les
branches absentes d'AnaMu restent visibles au tableau de couverture.

## 4. Ce qui reste à faire pour fermer A01, A04 et A05

1. **A01 encore ouvert** : confronter les 190 lignes à une seconde source
   institutionnelle, réconcilier les préalables, les choix réels de crédits,
   les autres éditions éventuelles et les cours sans description.
2. **A04 encore ouvert** : rechercher les *plans de cours* et exercices
   réels, chapitre par chapitre ; déclarer les données non publiques
   comme manquantes plutôt que les reconstituer par imagination.
3. **A05 encore ouvert** : construire la matrice des acquis pédagogiques
   réels, puis des questions analytiques ; les grandes familles ci-dessus
   ne constituent qu'une orientation.
4. **A09–A10 encore ouverts** : exemples notés, contre-exemples, corpus
   indépendants et audit d'un enseignant/orchestrateur qualifié.
5. Répéter cet exercice sur **McGill et Berklee** et réconcilier les
   compétences communes et divergentes avant toute prétention de couverture.

**Conclusion :** le catalogue UdeM est désormais **inventorié** ; notre
connaissance de son contenu pédagogique **n'est pas exhaustive**. C'est
une avancée sur la traçabilité des exigences, **pas** une validation d'une
seule capacité musicale complète.
