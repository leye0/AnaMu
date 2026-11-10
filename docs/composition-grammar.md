# AnaMu — analyse des choix d'orchestration et diagnostics contrefactuels

**Contrat d'expériences existantes, 10 novembre 2026.** Ce document complète les
[objectifs normatifs](OBJECTIVES.md) et l'[état des prototypes](roadmap.md).
AnaMu doit pouvoir **expliquer des choix d'écriture** et, à terme,
**produire une variation audible et cohérente** sous les mêmes contraintes.
La simple détection de régularités mathématiques ou la compression des
notes ne répond pas à cette exigence.

**Attention : aucun générateur libre n'est au programme actuel.** Les
prédictions masquées et les modifications d'une note décrites ici sont
uniquement des **épreuves diagnostiques** sur des partitions existantes.
Toute création originale attend l'audit exhaustif des cursus et la porte
L01–L05 du [TODO universitaire](todo-university-coverage.md).

## 1. Le vrai problème : reconstruire les décisions d'un orchestrateur

La question de chaque mécanisme est : **« Si je retire ou modifie ce choix
d'arrangement, que devient la musique ? »** Une preuve structurelle n'est
pas encore une preuve d'impact esthétique.

| Axe d'écriture de niveau avancé | Questions musicales à apprendre à résoudre | Contre-épreuve constructive envisagée |
|---|---|---|
| Conception motivique | Où le motif est-il posé, varié, fragmenté, préparé puis repris ? | Continuer un développement sans répétition mécanique |
| Harmonie et conduite des voix | Quel accord est soutenu, à quelle inversion, avec quelles tensions, notes étrangères et résolutions ? | Réharmoniser un segment en préservant ses voix et sa direction |
| Distribution orchestrale | Quels pupitres portent la ligne, la doublent, la colorent ou lui répondent ? | Retirer, redistribuer et réintroduire un rôle avec registre jouable |
| Texture et contrepoint | Quelles strates sont actives et indépendantes : basse, contrechant, figuration, pédale, soutien harmonique ? | Modifier la densité tout en gardant les couches intelligibles |
| Registre et équilibre | Où se concentrent les hauteurs, les doublures, les espaces entre voix ? | Transposer/doubler sans écraser la ligne principale ou créer de trous involontaires |
| Forme et dramaturgie | Comment sont organisés attente, cadence, contraste, transition et point culminant ? | Générer une section qui va quelque part et conclut clairement |
| Écriture instrumentale | Tessiture, doigtés/archets, souffle, endurance, transposition, articulations, couleurs et mélanges | Réorchestrer sans exiger l'impossible à des exécutants |
| Expression interprétée | Comment nuances, crescendos, ralentissements, accents et phrasé travaillent-ils ensemble ? | Réaliser la phrase en MIDI/audio expressif, pas juste aligner les hauteurs |

**Rôle ≠ instrument.** Un violoncelle peut porter la basse, un thème,
un contrechant ou un ostinato selon le passage. Une « fonction orchestrale »
est une hypothèse **locale, relationnelle et révisable**, pas une étiquette
statique attachée à `cello`, à une piste MIDI ou à son programme GM.

## 2. Contrat analytique d'une règle réutilisable

Toute règle qui prétend représenter un savoir d'arrangement devra préciser :

1. **Contexte d'emploi** : tonalité, métrique, niveau formel, fonction de
   phrase, pupitres et registres, densité, niveau dynamique et style couvert.
2. **Indices de partition** : notes, voix, silences, articulations, textes,
   indications de tempo et d'instrumentation, avec identifiants de source.
3. **Opération constructive** : `DOUBLE_LINE`, `HANDOFF_MELODY`,
   `ADD_COUNTERLINE`, `DISTRIBUTE_HARMONY`, `THIN_TEXTURE`,
   `PREPARE_CADENCE`, etc. Ce sont des **opérations proposées**, non des
   capacités déjà implémentées.
4. **Invariants à préserver** : continuité mélodique, conduite des voix,
   rythme/métrique, placement de la basse, intention formelle, etc.
5. **Contraintes physiques et perceptives** : tessitures, durées
   respirables/jouables, timbres, balance, présence acoustique ; distinguer
   ce que la partition **encode** de ce que le son **prouve**.
6. **Contrefactuels** : même passage sans cette opération, avec un autre
   pupitre ou une autre octave, et avec une règle triviale concurrente.
7. **Tests** : reconstruction de mesures masquées, œuvres tenues à l'écart,
   comparaisons à des arrangements humains et **écoutes aveugles** si l'on
   affirme une amélioration esthétique.

Une règle n'est pas « bonne » parce qu'elle réduit le nombre de bits
nécessaires pour encoder un morceau. La description minimale peut être un
outil de sélection, **jamais le critère ultime de qualité musicale**.

## 3. Premier essai mesuré : les doublures instrumentales

La [MusicXML 4.0 (W3C)](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/note/)
définit les notes et les positions métriques ; sa
[transposition écrite → sonnante](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/transpose/)
évite de comparer deux instruments sur des hauteurs incompatibles. La
construction historique d'une texture par doublures, registres et
distribution harmonique est discutée par
[Rimsky-Korsakov, *Principles of Orchestration*](https://www.gutenberg.org/ebooks/33900).
**Ses préférences stylistiques ne sont pas des lois universelles.**

`anamu/score_texture.py` lit des partitions MusicXML `.mxl` auditées :

- noms et identifiants des parties ; position au sein de chaque mesure,
  divisions et voix multiples via `backup`/`forward`, accords via `chord` ;
- hauteurs écrites **et** hauteurs sonnantes avec `transpose` explicite ;
- durées de notation, fragments liés signalés, ornements et petites notes
  de renvoi exclus du modèle strict ; mesure imprimée distincte de son index ;
- preuve exacte d'au moins trois attaques **successives dans chaque partie**
  à l'unisson, à une octave ou deux octaves, avec durées identiques.

L'analyse renvoie des **candidats de doublure notée**, non « mélodie
renforcée avec succès ». Une ligne peut doubler la basse, une voix
intérieure ou simplement partager des notes avec une autre partie.

`anamu/orchestral_counterfactual.py` réalise une **micro-épreuve
générative falsifiable** : trois notes concordantes de deux pupitres
établissent une transposition fixe ; la suite du second pupitre est
masquée ; le programme génère trois notes à partir du premier pupitre,
puis seulement compare à la partition originale. Deux baselines : répéter
la dernière hauteur du second pupitre et copier le premier pupitre
**à l'unisson** sans apprendre d'intervalle.

| Corpus noté | Candidats de doublure | Notes prédites | Succès exacts | Hauteur constante | Copie à l'unisson |
|---|---:|---:|---:|---:|---:|
| Beethoven 5/I | 1 767 | 6 294 | 4 816 (76,5 %) | 1 885 (30,0 %) | 1 583 (25,2 %) |
| Beethoven 7/II | 441 | 6 303 | 5 625 (89,2 %) | 1 968 (31,2 %) | 1 573 (25,0 %) |

**Interprétation rigoureuse :** épreuves locales de reconstruction, **non**
échantillons indépendants. Les fenêtres d'un même couple de pupitres ne
se recouvrent pas, mais un même passage peut être représenté dans de
nombreux couples d'instruments. Les portions candidates ont été
sélectionnées par des préfixes concordants. Aucun compositeur, mouvement,
style ou public auditeur n'a été tenu à l'écart ; les notes exactes
reconstruites ne prouvent ni qualité d'orchestration ni musicalité nouvelle.

Reproduction sans téléchargement ni service payant :

```bash
python -m scripts.orchestral_doubling_probe --top 3
python -m unittest tests.test_score_texture tests.test_orchestral_counterfactual -v
```

## 3 bis. Conduite des voix : mouvement et alternatives composables

Dans [*Tone and Voice* (Huron, 2001)](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf),
les règles de conduite des voix sont étudiées comme moyens de répondre
à des objectifs **perceptifs**, notamment l'identité des flux auditifs,
et non comme des lois abstraites auxquelles toute œuvre doit obéir.
La [bibliothèque music21](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html)
propose également la représentation classique des mouvements contraires,
obliques, similaires et parallèles sur des quartets de notes.

`anamu/orchestral_voice_leading.py` examine quatre notes de deux **parties
notées** aux deux mêmes positions de partition : A0, A1, B0, B1. Les
attaques doivent être consécutives dans chaque partie, leur portée et
voix notées demeurer identiques, sans accords ni fragments liés ; on
ne relie pas artificiellement deux attaques séparées par plusieurs
mesures vides. On conserve les quatre IDs de source et mesure :

- mouvements **contraires, obliques, parallèles, similaires** ou **statiques** ;
- intervalles avant/après, croisements stricts de registre ;
- présence d'intervalles parallèles de quinte ou d'octave/unisson,
  comme **faits** et jamais comme infractions automatiques ;
- prise en compte des hauteurs sonnantes des instruments transpositeurs.

| Partition | Quartets exacts | Contraires | Parallèles | Croisements |
|---|---:|---:|---:|---:|
| Beethoven 5/I | 24 824 | 1 932 | 5 763 | 73 |
| Beethoven 7/II | 11 602 | 977 | 4 668 | 174 |

Ce sont des **comptages de quartets recouvrants**, non des scores de
contrepoint. En particulier, les octaves parallèles peuvent résulter
d'une doublure délibérée et souhaitable dans un orchestre.

Le module propose ensuite une **modification contrefactuelle unique** :
pour A0→A1 et B0 déjà observés, calculer un nouveau B1 qui produirait
un mouvement parallèle, contraire ou oblique. Il conserve le reste du
passage, refuse les hauteurs hors MIDI et renvoie les implications
structurales (nouvel intervalle, quinte/octave parallèle, croisement).
Ce n'est **pas** un conseil d'harmonisation ni de jouabilité ; la
compatibilité avec l'accord, le style, le rôle du pupitre et l'audition
reste à vérifier.

```bash
python -m scripts.orchestral_voice_leading_probe --top 2
python -m unittest tests.test_orchestral_voice_leading -v
```

## 3 ter. Une variante de voix modifie aussi la matière harmonique

**Premier pont structurel G3 :** `anamu/orchestral_harmony.py` rassemble
les notes **sonnantes** à un instant exact d'une partition, en incluant
les notes déjà attaquées et encore tenues dans la **même mesure**. Il
conserve les IDs de source, les hauteurs et la note la plus grave. Il
peut reconnaître une **forme verticale exacte** (classes de hauteur
d'une triade ou d'un accord de septième) ; les racines ambiguës des
accords symétriques sont toutes préservées.

Pour un changement hypothétique de **B1 seulement** proposé par la
conduite des voix, le module reconstruit les deux verticalités sur
**tous les pupitres simultanément** sans modifier la source MusicXML.
Il rapporte les classes de hauteur ajoutées/retirées, les formes
strictement compatibles et le changement éventuel de basse.

| Partition | Mouvements contraires modifiables | Forme exacte avant | Forme exacte perdue après | Classe de hauteur ajoutée | Note la plus grave changée |
|---|---:|---:|---:|---:|---:|
| Beethoven 5/I | 1 932 | 1 243 | 353 | 951 | 153 |
| Beethoven 7/II | 977 | 587 | 269 | 619 | 128 |

Ces observations sont **corrélées au sein des œuvres** et les colonnes
peuvent se recouper. Une forme d'accord qui disparaît peut correspondre
à une **suspension, une tension ou une note étrangère artistiquement
voulue** : ce n'est aucunement un score de qualité ou une interdiction.

La [syntaxe hiérarchique de l'harmonie tonale de Rohrmeier (2011)](https://doi.org/10.1080/17459737.2011.573676)
est beaucoup plus riche qu'un ensemble de notes. Les
[conventions analytiques DCML](https://dcmlab.github.io/standards/build/html/reference/reference.html)
distinguent tonalité, accords et cadences ; la
[documentation music21 des accords](https://music21.org/music21docs/moduleReference/moduleChord.html)
est un témoin pour les formes verticales, pas un substitut à l'analyse
experte. Notre prochaine expérience est d'aligner des fonctions
**annotées indépendamment**, puis de comparer des réalisations audibles.

```bash
python -m scripts.orchestral_harmonic_context_probe --top 3
python -m unittest tests.test_orchestral_harmony -v
```

**Limites :** aucune tonalité locale, note étrangère, résolution,
orthographe enharmonique ou fonction de dominante n'est inférée ;
aucune continuité automatique des tenues entre mesures ni reprise
dépliée ; il s'agit de **partition notée**, pas de son acoustique.

## 3 quater. Passages et broderies : l'harmonie n'est pas une liste de notes fixes

L'analyse contrapuntique distingue une **figure mélodique** d'une
**note étrangère à un accord** : une ligne peut traverser les sons de
l'harmonie, retarder une résolution ou former une dissonance intentionnelle.
Les API de [music21, `ThreeNoteLinearSegment` et `VerticalityTriplet`](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html)
séparent précisément la configuration linéaire de la justification
verticale ; le **nom et l'orthographe diatonique** des notes comptent.

`anamu/score_texture.py` garde maintenant le nom écrit (`C`, `D`, etc.),
l'altération et l'octave, en plus de la hauteur MIDI et de la
transposition sonnante. `anamu/orchestral_ornaments.py` repère des groupes
de **trois notes conjointes**, sur la même partie, voix et portée :

- `diatonic_passing_figure` : deux pas diatoniques successifs dans la même
  direction, chacun d'un ou deux demi-tons (ex. do–ré–mi) ;
- `diatonic_neighbor_figure` : un pas, puis retour **à la même note
  écrite**, sans équivalence enharmonique forcée (ex. do–ré–do).

Les trois attaques doivent être consécutives, leurs durées doivent
s'enchaîner et rester dans la même mesure ; les accords simultanés dans
la partie et les fragments liés sont exclus. Aucune analyse des
accentuations métriques ou des notes chromatiques de passage n'est
revendiquée.

En parallèle, l'algorithme regarde **les autres parties** aux trois
instants. Il marque un **candidat de soutien orchestral stable** seulement
si leurs classes de hauteur ne changent pas, si elles contiennent les
classes des deux notes extrêmes et si celle de la note centrale en est
absente. Cela *n'établit toujours pas une harmonie fonctionnelle*.

| Partition | Figures strictes | Passages | Broderies | Accompagnement inchangé | Soutien strict aux deux extrêmes |
|---|---:|---:|---:|---:|---:|
| Beethoven 5/I | 118 | 71 | 47 | 0 | 0 |
| Beethoven 7/II | 753 | 638 | 115 | 69 | 9 |

Exemple inspectable dans Beethoven 7/II : un pupitre écrit **si–la–sol**
en transposant, ce qui sonne **sol♯–fa♯–mi**, tandis que les autres
pupitres tiennent les classes **mi–sol♯–si**. L'algorithme observe une
figure de passage avec soutien stable ; seul un analyste disposant du
contexte peut affirmer si le fa♯ agit comme *note étrangère*.

Les [conventions de DCML](https://dcmlab.github.io/standards/build/html/reference/reference.html)
annotent notamment les retards et certaines additions, **mais pas
systématiquement les broderies et notes de passage ordinaires**. Elles
ne pourront donc **pas** servir de vérité positive exhaustive pour ce
détecteur : il faudra des annotations adaptées ou une vérification
experte indépendante. Les fenêtres de trois notes peuvent se recouvrir,
et leur nombre ne prouve pas la qualité d'un arrangement.

```bash
python -m scripts.orchestral_ornament_probe --top 3
python -m unittest tests.test_orchestral_ornaments -v
```

**Lien génératif recherché (pas encore réalisé) :** reconnaître un
geste *note d'appui → note de passage → arrivée*, puis construire ou
retirer une telle élaboration en conservant harmonie, accent, ligne,
articulation et intention de phrase. Comparer ensuite des versions
réellement interprétées, et non des taux de coïncidence de notes.

## 4. Ce qu'il faut encore prouver pour éviter le « AI slop »

1. **Vérité orchestrale** : comparer les rôles identifiés à des annotations
   humaines, et mesurer précisément les faux positifs (simples notes communes).
2. **Généralité** : prédire un pupitre d'une œuvre et d'un compositeur
   **entièrement tenus à l'écart**, contre baselines fortes (copie à
   l'unisson, règle de voix la plus proche, etc.).
3. **Règles de composition** : au-delà des doublures et mouvements exacts,
   les transitions de texture, les contrechants, les relais de mélodie,
   la conduite harmonique et la grande forme.
4. **Réalisation réaliste** : différencier MIDI noté, interprétation MIDI
   et audio ; ne pas inférer timbre, enveloppe, volume ou expressivité
   acoustique à partir du seul `program_change`.
5. **Audition** : synthétiser des versions contrôlées d'un même passage,
   auditer la jouabilité et mener une écoute comparative aveugle avec
   des musiciens (cohérence, tension, clarté, variété, intérêt, naturel).

**Interdiction méthodologique :** un bon score sur une transformation exacte
ne deviendra jamais à lui seul « 89 % de bonne musique ». La qualité d'une
composition est une **question musicale et perceptive**, dont l'analyse
symbolique ne fournit qu'une partie des conditions nécessaires.
