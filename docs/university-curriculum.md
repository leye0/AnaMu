# AnaMu — référentiel universitaire de composition et d'orchestration

**Statut : contrat de couverture à établir, pas certification d'exhaustivité.**
Le [TODO de couverture](todo-university-coverage.md) est la seule liste à cocher
des travaux nécessaires. Les [objectifs](OBJECTIVES.md) fixent la finalité et
les [règles de preuve](research-evidence-gates.md) fixent les validations.

## 1. La décision fondamentale

Nous faisons du **reverse engineering analytique de l'écriture musicale** :
pour chaque savoir effectivement enseigné en composition, harmonie,
contrepoint, orchestration, analyse et interprétation, retrouver dans les
œuvres des observations, des relations, des hypothèses alternatives et des
explications contrôlables. Le savoir musical prime sur les jolies statistiques.

**Aucune composition originale automatisée ne sera entreprise tant que la
couverture universitaire n'aura pas été auditée intégralement.** Les petites
reconstructions de notes masquées déjà présentes restent des **tests
diagnostiques** de règles analytiques, et non un chantier de création.

« Exhaustif » ne veut pas dire « nous avons nommé beaucoup de sujets » :
cela veut dire qu'un inventaire de cours **et de leur contenu réel** a été
réconcilié, qu'aucune compétence n'est oubliée, et que chaque capacité
pertinente reçoit une preuve d'analyse indépendante. Les compétences qui
ne sont pas automatisables (pratique d'instrument, audition intérieure,
direction et créativité humaine) demeurent **explicitement non couvertes**
tant qu'elles n'ont pas un protocole fidèle ; elles ne peuvent être
déclarées « faites » par assimilation à une mesure numérique.

## 2. Trois programmes témoins, sources primaires

| Programme et édition visible | Étendue publique vérifiable | Domaines et cours repères (exemples, pas liste complète) |
|---|---|---|
| [Université de Montréal, B. Mus. Composition, version 10 (A26)](https://admission.umontreal.ca/programmes/baccalaureat-en-musique-composition/structure-du-programme/) | 90 crédits, dont 63 obligatoires et 27 à option ; spécialisations et choix variables | MTE 1110/1111 contrepoint ; MTE 1220/1221 harmonie ; MTE 2114/2115 orchestration ; MTE 1205/1206 analyse XXe ; MTE 1403/1404 techniques contemporaines ; MUS 1300 acoustique ; MUS 1321 traitement du son ; MCT 1601/1602 et 3011/3012 composition |
| [McGill, Schulich, B. Mus. Composition (exigences consultées en 2026)](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) | 124 crédits : 32 de fondations, 61 de cours obligatoires, 13 complémentaires et 18 optionnels | MUTH 150/151/251/350 théorie/analyse ; MUTH 202/204 **choix** de contrepoint ; MUCO 241/242 écriture tonale ; MUCO 245/246 composition XXe/XXIe ; MUCO 261/360/460 orchestration **obligatoire** ; MUCO 341/342/541 studio numérique ; MUSP formation musicale |
| [Berklee College of Music, B. Mus. Composition (grille 2026F)](https://www.berklee.edu/sites/default/files/2026-05/2026f-composition-degree-grid.pdf?fv=gFJx2m0F) | 120 crédits : 32 de majeure, 22 de core spécifique, 35 de core musique, 24 d'arts libéraux, 7 d'options générales | CM-221 écriture tonale ; CP-215 contrepoint ; MLAN-311/312 analyse ; CM-311/312 techniques contemporaines ; CM-231 instrumentation ; CM-441 orchestre complet ; ET-231/232 solfège ; COND direction ; projets et portfolio |

**Première triangulation des catalogues :**

- [UdeM A26](udem-curriculum-a26-audit.md) : [190 entrées](data/udem-composition-a26.json), 22 cours obligatoires / 63 crédits.
- [McGill 2026](mcgill-curriculum-2026-audit.md) : [58 cours explicitement nommés](data/mcgill-composition-2026.json), dont 25 obligatoires / 61 crédits de cours imposés ; fondations, choix et crédits ouverts séparés.
- [Berklee 2026F](berklee-curriculum-2026f-audit.md) : [44 lignes d'exigences](data/berklee-composition-2026f.json), certaines étant des pools/alternatives/portfolio et non des cours individuels.

Leurs correspondances aux familles du TODO sont **préliminaires**.
Les **plans de cours détaillés** et toutes les branches réellement
suivables ne sont pas encore inventoriés avec la même précision.
Un [premier audit des enseignements recommandés et des majeures voisines](optional-knowledge-audit.md)
ajoute 30 pistes de connaissance issues de descriptions publiques McGill
et Berklee, sans assimiler ces cours à des crédits nécessairement admissibles
dans la majeure Composition.

### Premières divergences pédagogiques qu'AnaMu doit respecter

| Domaine | UdeM A26 | McGill | Berklee 2026F |
|---|---|---|---|
| Orchestration | 1–2 obligatoires ; 3–4 proposés à option | 1–3 dans les 61 crédits obligatoires | Instrumentation et orchestre complet dans la majeure |
| Contrepoint | Espèces à 2–3 voix obligatoires ; niveaux supérieurs à option | Modal **ou** tonal parmi les complémentaires ; théorie fugue ailleurs | CP-210 et CP-215 au parcours de référence |
| Studio et son | Acoustique, DSP et électroacoustique obligatoires ; maquettes MIDI en option | Studio numérique et avancé imposés | Technologie musicale dans le tronc ; autres studios selon options |
| Répétition et pratique | Direction/ensembles en options | Ensembles et leçons pratiques avec crédits | Ensembles, leçons privées, direction et portfolio |

Ce tableau ne donne **aucun ordre de qualité** entre les universités :
il prévient seulement l'erreur de déclarer qu'une règle de contrepoint
ou un module MIDI couvre identiquement trois formations différentes.

Ce tableau représente des **repères attestés dans les catalogues**,
non la totalité de leurs cours, lectures, exercices, critères d'évaluation,
branches optionnelles et savoirs tacites. Certains cours peuvent être
affichés mais non offerts à un trimestre. Les descriptions ne remplacent
pas les plans de cours : nous devons les collecter/licencier, les dater
et compléter les lacunes avec les établissements ou des ressources
publiques équivalentes, sans inventer leur contenu.

**Règle d'audit :** conserver, pour chaque ligne de programme, l'édition,
le statut obligatoire/option, le code, les crédits, les acquis attendus,
les chapitres/activités, l'évidence source et les limites d'accès.
Le périmètre de validation est **l'union des savoirs musicaux pertinents**
offerts par les trois programmes, et non le plus petit parcours permettant
d'obtenir chacun des diplômes. Une compétence intéressante enseignée dans
une **option, une recommandation ou une spécialisation alternative** compte
autant dans notre objectif de connaissance qu'une compétence obligatoire.

### Règle de maximisation des options

1. **Recenser toutes les possibilités** : cours obligatoires, choix de blocs,
   recommandations, options de majeure et options libres accessibles dans
   les catalogues musicaux. Une liste ouverte reste explicitement incomplète.
2. **Examiner chaque option**, même si aucun étudiant ne pourrait suivre
   simultanément toutes les branches. Le statut administratif d'un cours
   ne détermine pas sa valeur analytique.
3. **Inclure dans la matrice toute connaissance utile** à l'analyse, à
   l'arrangement, à l'orchestration, à la perception ou à l'évaluation de la
   musique : contrepoint avancé, fugue, jazz, écriture pour l'image et le jeu,
   instruments non standard, acoustique, production, interprétation,
   répertoires historiques et traditions autres qu'occidentales, notamment.
4. **Conserver une décision traçable par cours** : `à évaluer / inclus /
   hors périmètre motivé / contenu inaccessible`, avec la raison et la
   connaissance nouvelle attendue. Le verdict « doublon » exige de montrer
   que ses apprentissages sont couverts ailleurs, pas seulement que son nom
   ressemble à un autre cours.
5. **Ne pas confondre formation et recherche** : AnaMu peut étudier la
   matière de plusieurs parcours incompatibles entre eux sans prétendre
   qu'un diplômé a suivi l'ensemble, ni que le logiciel maîtrise déjà
   l'ensemble.

L'inventaire actuel d'UdeM conserve ses **168 entrées à option**,
McGill conserve ses **15 choix complémentaires et 8 recommandations**,
et Berklee ses **réserves ouvertes de 8 crédits de majeure et de 7 crédits
généraux**. Il reste à explorer les catalogues complets derrière les
réserves ouvertes : ces chiffres sont des **points de départ, pas des
plafonds de connaissances**.

## 3. Grille commune pour traduire un cours en analyse

Pour chaque compétence `C` et chacun des programmes pertinents :

1. **Savoir enseigné :** référence précise au cours, chapitre, exercice,
   répertoire et conventions stylistiques ; distinguer prescription
   pédagogique et propriété descriptive d'une œuvre.
2. **Question analytique :** que doit savoir expliquer un musicologue ou
   un orchestrateur dans une partition *inconnue* ?
3. **Observables requis :** notes écrites/sonnantes, voix, rythmes,
   indications, audio, annotations et leur provenance ; ce qui manque
   reste inconnu.
4. **Hypothèses :** unités et relations musicales interprétables,
   alternatives, dépendances contextuelles et désaccords expertisés.
5. **Diagnostic :** épreuve positive, faux-ami négatif, contre-exemple
   stylistique et ablation/contre-factuel **analytique**, pas morceau généré.
6. **Évaluation :** corpus tenu à l'écart, référence humaine indépendante,
   baselines, couverture, cas non résolus et erreurs par famille ; pour
   un phénomène timbral/acoustique, preuve audio, pas MIDI seul.
7. **Conformité :** statut `non abordé / candidat / testé / expertisé / validé`.
   Une case TODO n'est cochée que lorsque **toutes** les preuves de cette
   compétence sont localisées, reproductibles et approuvées.

Exemple : un module repérant trois notes conjointes n'a **pas** couvert
« les notes étrangères ». Il lui manque le contexte tonique, le statut
harmonique, les accents, les appoggiatures, les suspensions et leurs
résolutions, ainsi qu'une validation sur des annotations adaptées.

## 4. Ce que signifie *valider le parcours*

Une famille est couverte seulement lorsque :

- les objectifs de **tous les cours applicables** sont inventoriés et
  mappés à des capacités sans trous ni doublons non justifiés ;
- les sous-compétences disposent d'exemples positifs/négatifs annotés,
  de règles explicables, de tests indépendants et de résultats publiés ;
- les différences de style et les pratiques historiques sont respectées :
  une interdiction de contrepoint à espèces n'est pas une loi esthétique
  pour Mahler, Debussy ou une partition spectrale ;
- les contraintes d'instrument et d'audibilité sont observées dans la
  **bonne source** ; les exercices de studio, pratique instrumentale,
  répétition, direction et jugement artistique sont traités honnêtement ;
- un **audit contradictoire par des musiciens compétents** contrôle un
  échantillon aveugle de chaque domaine, y compris les contre-exemples ;
- les compétences non couvertes sont corrigées ou documentées comme
  **blocages** : on n'accorde pas la « certification » par moyenne pondérée.

**Porte de sortie :** le [TODO](todo-university-coverage.md) a toutes ses
cases nécessaires satisfaites, les matrices cours→compétences→preuves
sont consultables, et les contrôles d'évaluation sont repassés sur un jeu
indépendant. Ce n'est **pas le cas à ce jour**.

## 5. Frontière recherche / création

La capacité de prédire une note masquée ou d'évaluer un changement d'octave
permet d'éprouver une **hypothèse sur l'écriture existante**. Elle ne
permet pas de prétendre créer de la bonne musique. Un futur système de
composition nécessiterait en plus la direction formelle, des décisions
artistiques, un rendu sonore crédible, des contraintes d'exécutants et des
comparaisons d'écoute aveugles. Il demeure **hors programme opérationnel**
jusqu'à satisfaction du référentiel ci-dessus et décision explicite.
