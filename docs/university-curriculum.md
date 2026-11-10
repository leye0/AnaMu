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
| [McGill, Schulich, B. Mus. Composition](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) | 124 crédits annoncés ; groupes de cours et options à réconcilier | MUTH 150/151/251/350 théorie/analyse ; MUTH 202/204 contrepoint ; MUCO 241/242 écriture tonale ; MUCO 245/246 composition XXe/XXIe ; MUCO 261/360/460 orchestration ; MUCO 341/342/541 studio numérique ; MUSP formation musicale |
| [Berklee College of Music, B. Mus. Composition (catalogue automne 2024)](https://college.berklee.edu/composition/bachelor-of-music-in-composition) | 120 crédits ; tronc commun, majeure, options, portefeuille final | CM-221 écriture tonale ; CP-215 contrepoint ; MLAN-311/312 analyse ; CM-311/312 techniques contemporaines ; CM-231 instrumentation ; CM-441 orchestre complet ; ET-231/232 solfège ; MHIS-251/252 histoire ; projets et portfolio |

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
Le périmètre de validation comprend le **tronc commun de chacun des trois
programmes** et les **branches pertinentes** à l'écriture instrumentale,
orchestrale et contemporaine ; les autres branches sont documentées comme
écarts explicites, jamais cachées.

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
