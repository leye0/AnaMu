# AnaMu — référentiel universitaire de composition et d'orchestration

**Statut : contrat de couverture à établir, pas certification d'exhaustivité.**
Le [TODO de couverture](todo-university-coverage.md) est la seule liste à cocher
des travaux nécessaires. Les [objectifs](OBJECTIVES.md) fixent la finalité et
le [protocole de collecte](course-material-collection.md) fixe les preuves
nécessaires pour affirmer qu'un cours est réellement documenté.
Le [registre cours par cours](data/course-material-progress.json) indique
la prochaine matière à rechercher et les pools d'options encore ouverts.
La [base de connaissances académiques](knowledge-base.md) définit **le produit
à constituer à partir des cursus** : cours et syllabus sont des sources, les
concepts musicaux réconciliés sont le patrimoine exploitable par AnaMu.

## 1. La décision fondamentale

**Maintenant, nous reconstruisons d'abord la matière des cours.** Pour
chaque savoir effectivement enseigné en composition, harmonie,
contrepoint, orchestration, analyse et interprétation, recueillir les
objectifs, chapitres, exercices et références. **Ensuite seulement**, nous
chercherons comment reconnaître ces composants dans des œuvres MIDI
existantes. Le savoir musical prime sur les jolies statistiques.

**Le résultat central attendu n'est pas trois diplômes copiés ni trois
collections séparées de règles : c'est une immense connaissance unifiée**,
enrichie par les particularités de chacun des cursus. Le moteur d'analyse
doit pouvoir invoquer cette connaissance commune pour justifier ses
interprétations. Une variation de tradition ou de style reste une relation
documentée, jamais écrasée au nom de l'uniformisation.

**Aucun développement d'analyseur ni composition originale automatisée
ne sera entrepris pendant la collecte intégrale du contenu des cours.**
Le passage à une phase technique exige une décision explicite de Léon.

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

## 3. Travail immédiat : connaître vraiment chaque cours

Pour chaque ligne de ces catalogues, appliquer
[le protocole d'acquisition](course-material-collection.md) et établir :

1. **Le contenu réellement enseigné** : syllabus, chapitres, objectifs,
   lectures, exercices, œuvres citées et critères d'évaluation.
2. **La source exacte** : établissement, édition, lien ou ouvrage, section
   et droits d'utilisation. Une description publique ne remplace pas un plan.
3. **La couverture des options** : vérifier les cours derrière les blocs
   de choix, les recommandations, les spécialités voisines et les contenus
   qui n'apparaissent que dans une branche du programme.
4. **Les inconnues** : documents introuvables, contenu partiel, variantes
   de cours et comparabilité incertaine entre éditions.
5. **L'apport pédagogique distinctif** : ne pas fusionner deux matières
   parce que leurs titres semblent équivalents ; relever d'abord les
   apprentissages et exceptions de chacune.

**Un cours n'est couvert que si sa matière détaillée est effectivement
documentée et vérifiée.** Les lacunes qui empêchent cette affirmation
restent visibles et bloquent le passage. Les étapes ultérieures — base de
concepts commune, conception des détecteurs MIDI, validations musicales et
composition éventuelle — sont définies dans
[OBJECTIVES.md](OBJECTIVES.md), mais ne sont pas ouvertes actuellement.
