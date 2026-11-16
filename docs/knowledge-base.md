# AnaMu — architecture de la base de connaissances musicales académiques

**DÉCISION DE PHASE (11 novembre 2026) :** [État courant](STATUS.md). La collecte publique de plans par cours (1A) est arrêtée en meilleur effort : **115 cours restent partiels, dont 22 bloqués en attente de source extérieure, mais aucun n'est une recherche active sans nouvelle preuve**. La **documentation académique des sujets identifiés (1B) est maintenant ACTIVE**; [14 mécanismes sourcés](subject-research/2026-11-11-first-14-music-theory-mechanisms-primary-educational-sources.md) sont acquis comme documentation *des sujets*, pas comme syllabus. Les développements de la base de concepts unifiés / phase 2 restent verrouillés. Les assertions plus bas disant « seule collecte par cours active » sont des instantanés historiques.

**Document de conception normatif, pas une implémentation achevée.**
L'ambition est de posséder un patrimoine **massif, structuré, traçable et
interrogeable de connaissances musicales** obtenu par la mise en commun de
plusieurs programmes universitaires avancés. Ce patrimoine doit alimenter
plus tard des **analyseurs de morceaux MIDI existants** et, **une fois les
portes académiques levées**, un éventuel système de composition musicale.
**La priorité actuelle est exclusivement la collecte de la matière des
cours**, selon [le protocole](course-material-collection.md). La conception
du patrimoine ci-dessous décrit la phase suivante, encore verrouillée.

## 1. L'actif central n'est pas un catalogue de cours

Les [catalogues UdeM, McGill, Berklee](university-curriculum.md) décrivent
**où chercher les connaissances**, pas les connaissances elles-mêmes.
Les [recommandations et spécialités voisines](optional-knowledge-audit.md)
enrichissent le périmètre ; leur statut optionnel ne réduit pas leur valeur.

Un même concept peut être enseigné dans trois cours différents sous des
noms divers. L'objectif est de **réconcilier les savoirs** dans une base
commune, en conservant les formulations, divergences, prérequis, exercices,
exemples et exceptions propres à chaque source. On ne confond jamais
« connaître le nom du concept » avec « être capable de l'identifier et de
l'expliquer correctement dans une œuvre ».

### Quatre couches à ne jamais confondre

| Couche | Produit attendu | Ce qu'elle ne prouve pas |
|---|---|---|
| **1. Sources universitaires** | Programmes, éditions, cours, syllabus, chapitres, exercices, lectures, crédits et provenance | Que le moteur comprend la matière |
| **2. Base académique unifiée** | Concepts, règles conditionnelles, exemples, relations, contre-exemples, styles et divergences | Que chaque concept est implémenté |
| **3. Moteur d'analyse MIDI** | Hypothèses sourcées sur des morceaux MIDI existants, références aux concepts utilisés, limites des observations | Que les analyses sont justes sans épreuve indépendante ou que MIDI contient le son acoustique |
| **4. Évaluation / composition future** | Compétences expertisées et, plus tard, décisions génératives cohérentes évaluées à l'écoute | Qu'une métrique isolée garantit une musique agréable |

**État actuel :** nous avons des inventaires de catalogues (couche 1
**partielle**). La matière détaillée des cours n'a pas été collectée
exhaustivement. **La grande base de concepts réconciliés (couche 2) reste
à construire.** Il n'existe plus de prototype analytique dans le dépôt
actif : les futures capacités seront décidées à partir des enseignements
réellement obtenus. La composition reste fermée.

## 2. Unité de connaissance à construire

La représentation définitive devra évoluer avec la recherche, mais toute
unité académique devra pouvoir exprimer au minimum :

| Champ conceptuel | Raison d'être |
|---|---|
| `concept_id`, `version`, intitulés et synonymes | Identité stable sans doublons dus à la terminologie |
| Définition et **fonction musicale** | Expliquer ce que le compositeur, l'orchestrateur ou l'analyste cherche à faire |
| Domaine de validité | Style, époque, formation, instrument, convention, restrictions et exceptions |
| Relations entre concepts | Prérequis, spécialisation, variante, contraste, contradiction justifiée |
| `sources[]` | Programme, cours, section de syllabus, édition, lecture et droits d'accès |
| Exemples et contre-exemples | Mesures/partitions licites, annotations d'expert, résultats attendus et cas ambigus |
| Conditions observables | Notes, voix, rythme, harmonie, notation, interprétation, timbre ou audio requis |
| Capacités d'analyse liées | Hypothèses, mécanismes, points du TODO, tests négatifs et preuves |
| Statut et incertitude | `repéré / décrit / réconcilié / implémenté / testé / validé` et limites |

Ces champs sont un **contrat de conception**, pas la description d'un
schéma de base de données déjà présent dans le dépôt. Aucun script actuel
ne doit être présenté comme un moteur complet de cette base.

## 3. Transformer plusieurs programmes en une connaissance commune

1. **Inventorier** toutes les branches pertinentes des cours obligatoires,
   optionnels, recommandés et voisins, avec statut d'admissibilité séparé.
2. **Lire la matière réelle** : objectifs, chapitres, conventions,
   exercices, œuvres et barèmes d'évaluation ; signaler ce qui est inconnu.
3. **Extraire des savoirs élémentaires** : par exemple, une doublure
   d'octave est un geste d'orchestration seulement si sa fonction, son
   registre, ses instruments et son effet perceptif sont contextualisés.
4. **Réconcilier** : associer des enseignements équivalents à un concept
   stable, conserver leurs nuances, et séparer les variantes incompatibles
   plutôt que d'inventer une règle universelle.
5. **Relier** concepts, prérequis, opérations, styles, partitions annotées
   et sous-compétences. Rendre possible la navigation dans les deux sens :
   `cours → concepts` et `concept → cours, preuves et mécanismes`.
6. **Après autorisation de passage à la phase MIDI**, exercer l'analyse
   sur l'inconnu : vérifier que le moteur peut reconnaître dans un MIDI
   des composants effectivement enseignés, expliquer leur fonction,
   garder des hypothèses concurrentes et détecter ses propres limites.
7. **Évaluer ensuite** les résultats avec des œuvres hors développement, des
   musiciens indépendants et de l'audio lorsque l'affirmation porte sur
   une qualité sonore. Le statut `validé` requiert le dossier probant.

Un cours « optionnel » peut apporter le seul enseignement disponible d'un
geste orchestral essentiel : il doit être étudié. Un cours répétitif peut
renforcer la preuve ou préciser un contexte, même si sa matière recoupe un
autre. L'exclusion doit être justifiée **par acquisition de connaissance**,
jamais par la facilité de terminer un programme de crédits.

## 4. Ce qui fait une vraie explication musicale

Exemple d'une question future : « Pourquoi le compositeur confie-t-il le
contrechant aux altos pendant que les bois doublent le thème ? »

Une analyse crédible doit pouvoir articuler : rôles et indépendance des
voix, tessitures, directions mélodiques, harmonie et dissonances, texture,
équilibre des pupitres, articulation, contexte formel, couleur audible et
alternatives d'orchestration. Chaque affirmation renvoie aux notes, aux
sources pédagogiques et à une connaissance pertinente. Elle peut conclure
qu'une partie du résultat reste **inconnue sans enregistrement**.

Une simple corrélation de pistes MIDI, un score de similarité ou une
prédiction de note correcte ne résout pas cette question. **Les
mathématiques sont des instruments de vérification du savoir musical,
pas la finalité du projet.**

## 5. Relation avec l'éventuelle composition

Le système pourrait un jour utiliser cette connaissance pour choisir un
développement de motif, une conduite des voix, une répartition orchestrale
et un geste expressif **en comprenant leurs conséquences musicales**.
Cela exigerait en plus des choix artistiques, un rendu crédible et des
évaluations auditives humaines. Une bonne analyse n'est pas une garantie
automatique de bonne composition.

Cette étape demeure **hors de portée opérationnelle** jusqu'à couverture
et expertise du [TODO universitaire](todo-university-coverage.md), portes
**L01–L05**, et accord explicite de Léon.

### Deux modules, une connaissance commune

**Décision du 15 novembre 2026.** L’analyse et la création sont deux modules différents. La création dépend d’une analyse richement documentée et de la synthèse des savoirs transversaux. Ce n’est pas une inversion de l’analyse. Reconnaître un procédé ne dit pas quand le choisir, ni dans quel but. Les fiches de cours restent les sources de connaissance. La synthèse relie les preuves et leurs limites sans les remplacer.

| Responsabilité | Entrée | Sortie attendue |
|---|---|---|
| **Analyse** | Œuvre, passage, partition/MIDI/audio disponibles et question musicale | Observations localisées, hypothèses distinctes, raisonnement, explications concurrentes et inconnues. Une note notée, une identité de motif et une fonction tonale n’ont pas le même statut. |
| **Synthèse transversale** | Résultats d’analyse et enseignements documentés de plusieurs cours | Relations entre concepts, contextes d’application, contre-exemples et limites. Distinguer ce qui revient ensemble dans un exemple de ce qui peut varier indépendamment. Conserver les liens jusqu’au passage qui justifie chaque distinction. |
| **Création** | Intention explicite, forme/style/formation visés, contraintes du passage et connaissances pertinentes | Choix motivés et alternatives. Pour chaque choix, préciser ce qui doit rester reconnaissable, ce qui peut changer, ce qui pourrait contredire une autre contrainte et ce que l’écoute devra encore trancher. L’analyse peut vérifier le résultat, pas décider seule de sa valeur artistique. |

**Exemple de requête à la synthèse.** « Faire entendre une nouvelle région tonale sans perdre le motif et sans changer de porteur. » Consulter conjointement l’identité du dessin (contour, intervalles, rythme), le rôle et la conduite des voix, la confirmation tonale et l’échelle de la frontière. Si les sources ne soutiennent pas une relation dans le style visé, la laisser inconnue au lieu de généraliser. Le [relevé Buxtehude dans OLART-233](courses/berklee-online/OLART-233.md#le-dessin-passe-dans-une-autre-tonalité--buxtehude-buxwv-161) relie ces quatre axes et distingue le constat du scénario d’écriture. Sa transposition exacte et son adaptation modale sont deux options de composition, pas deux ordres à appliquer automatiquement. Le transfert du dessin à un autre porteur chez Bach sert de contraste, pas de consigne de réorchestration.

**Principe de sélection.** Partir du résultat musical voulu, pas d’un nom d’œuvre ou d’une liste de motifs voisins. Dans la requête ci-dessus, MTE-1221 aide à évaluer si la destination est installée, OLART-233 à choisir ce qui rend le dessin reconnaissable, et la comparaison BWV 78 à écarter un transfert de voix si le porteur doit rester fixe. Si la consigne exige les intervalles exacts, la variante modale devient inadmissible, même si le cas Buxtehude la documente. Si la consigne demande seulement une autre couleur sans quitter le centre, la réharmonisation ou la tonicisation redeviennent des options et la modulation n’est plus le résultat à chercher. L’accès transversal sert à **choisir quelles connaissances consulter, puis à expliquer quels gestes sont compatibles**, pas à cumuler les procédés.

**Préciser ce qui doit rester reconnaissable.** Comparer sur trois plans, sans remplacer un verdict par un autre. **Événements** : même voix, mêmes attaques, hauteurs et durées à la transformation autorisée près. **Dessin** : contour et intervalles analysés dans une voix continue, avec le rythme et les écarts explicités. **Charpente** : même rôle et mêmes destinations ou frontières pertinentes, même si les notes et leur placement changent. La [Variation 25 des Goldberg](courses/berklee-online/OLART-234.md#une-charpente-commune-sans-basse-identique--goldberg-variation-25) écarte l’identité des attaques sans écarter la parenté de structure. Réciproquement, une même descente chromatique peut servir d’autres fonctions dans deux œuvres. La création doit pouvoir demander un niveau précis et recevoir les preuves, les transformations admissibles et les incompatibilités à ce niveau, sans prétendre garantir une reconnaissance à l’écoute.

#### Choisir selon la contrainte musicale

Une relation d’analyse devient utile à la création quand elle aide à prendre une décision, y compris à rejeter une option. Pour chaque consigne, distinguer la partie de l’œuvre concernée, les contraintes fermes et ce qui relève encore d’un choix. Consulter ensuite les exemples et le contre-cas qui tranche l’ambiguïté. Quand les preuves ne permettent pas de prédire ce qui sera entendu, ne livrer que les propriétés vérifiables et formuler l’alternative à écouter.

| Intention formulée | Savoirs à consulter ensemble | Ce que la création ne doit pas déduire |
|---|---|---|
| Garder le rappel du début, mais changer la destination de la phrase | [Diabelli, Variations 1 et 15](courses/berklee-online/OLART-234.md#le-geste-survit-quand-la-cadence-change--beethoven-et-diabelli) pour identifier le rappel et dissocier la reprise de sa destination. [UdeM MTE-1221](courses/udem/MTE-1221.md#application-à-lanalyse-et-à-la-création--un-accord-deux-fonctions-de-préparation-13-novembre-2026) pour séparer la préparation de l’arrivée tonale. | Ne pas imposer l’ancienne cadence sous prétexte que le début est conservé. Une destination de cadence n’est pas à elle seule une région prolongée. |
| Garder un point d’appui au grave tout en faisant avancer les accords | [Brahms op. 24, Variation 22](courses/berklee-online/OLART-234.md#le-bourdon-ne-fixe-pas-lharmonie--brahms-sur-un-thème-de-haendel) pour le rôle de pédale. [McGill MUTH-150](courses/mcgill/MUTH-150.md#cas-comparatif--même-arrivée-de-basse-clôtures-différentes-13-novembre-2026) pour la clôture lue avec basse, dessus et contexte. | La note la plus grave ne donne ni toutes les fondamentales ni toutes les cadences. Si la basse doit jouer le contour d’origine, vérifier que l’option de pédale ne l’efface pas. |
| Faire avancer ou recolorer l’accompagnement sous un motif dont les hauteurs restent fixes | [Debussy](courses/berklee-online/OCOMP-367.md#le-même-pas-ne-ramène-pas-au-même-endroit) pour collection, centre et date de retour par couche, [Chopin](courses/mcgill/MUTH-251.md#chopin--les-voix-ne-descendent-pas-en-même-temps) pour le trajet des voix, [MTE-2316](courses/udem/MTE-2316.md#sous-les-mêmes-notes-un-autre-sol) pour isoler basse et note de couleur, et [CM-221](courses/berklee/CM-221.md#trois-voix-une-descente) pour décaler les voix sans changer leur destination. | Distinguer la note ajoutée, la collection, le point d’appui et la cadence. Ne pas appeler « transposition » l’opération qui garde les hauteurs du motif. Ne pas appeler « résultat identique » deux trajets qui ne partagent que leurs bornes. |
| Transformer un motif par reflet, sans obligation de garder le mètre | [Rachmaninoff XVIII](courses/berklee-online/OCOMP-250.md#inverser-la-cellule-sans-inverser-la-phrase--rachmaninoff) pour une inversion intervallique locale. Le [canon des Goldberg XII](courses/berklee-online/OCOMP-250.md#cas-et-midi--imiter-en-mouvement-direct-ou-contraire-13-novembre-2026) comme contraste. | Préserver la relation des hauteurs n’oblige pas à garder les durées, le mètre ou l’harmonie. Si la consigne exige un canon, une relation entre sections ne remplace pas la réponse entre voix. |
| Accroître le mouvement sans avancer une arrivée déjà calée | [MUSP-240](courses/mcgill/MUSP-240.md#accélérer-quoi--quatre-écoutes-avec-la-même-phrase) pour séparer vitesse locale et tempo global, [Arietta](courses/berklee-online/OLART-234.md#accélérer-la-cellule-sans-accélérer-toute-la-musique--beethoven-arietta) et [Chopin](courses/berklee-online/OLART-234.md#même-balancement-sous-deux-densités--chopin-berceuse) pour les appuis et les porteurs, [FILM-205](courses/berklee/FILM-205.md#intensifier-un-cue-sans-déplacer-son-arrivée) pour le contrôle en secondes. | Deux arpèges de même vitesse ne garantissent ni la même battue ni la même durée de phrase. Rejeter une accélération globale non compensée si l’arrivée est fixe. Si le nombre d’attaques doit rester prévisible, distinguer une subdivision écrite d’un [trille non mesuré](courses/berklee/CM-320.md#densité-écrite-et-densité-entendue--beethoven-op-109). |
| Changer la poussée rythmique en gardant le tempo et l’arrivée | [Stravinsky](courses/berklee-online/OCWPR-366.md#des-cors-qui-accentuent-sans-créer-de-nouvelles-croches) distingue attaque et renfort. [CM-320](courses/berklee/CM-320.md#six-croches-deux-reliefs) dissocie appuis de surface et réattaques du grave. [Beethoven IX](courses/berklee-online/OCOMP-485.md#trois-mesures-ou-quatre) sépare période et phase de groupement entre mesures. | Une nouvelle accentuation n’implique ni changement de BPM ni nouvelles barres. Un accent local ne garantit pas que le cycle entier se soit réorienté. |
| Faire cohabiter plusieurs lectures d’un cycle sans décaler le point de rencontre | [*Pantoum* de Ravel](courses/berklee/CM-312.md#vingt-quatre-noires-un-rendez-vous) présente des mètres de partie distincts sur la même grille. [CM-361](courses/berklee/CM-361.md#les-coups-de-cloche-ne-commencent-pas-tous-un-groupe) sépare battue, coups et coïncidences, étayés par la transcription et des pistes isolées. | Une superposition d’accents n’est pas à elle seule une preuve de polymétrie écrite. Un point commun en ticks ne suffit pas à énoncer le sens d’un repère ou à baptiser une tradition. |
| Faire réapparaître un son sans que le thème redémarre | [Ravel](courses/berklee-online/OCOMP-485.md#la-cloche-réapparaît-sans-avoir-disparu) pour la cloche qui n’a jamais quitté la partition, [Chopin op. 28 no 15](courses/berklee-online/OLART-234.md#la-même-touche-change-de-rôle--chopin-op-28-no-15) pour la même classe de hauteurs confiée à une autre main, [MUS-3322X](courses/udem/MUS-3322X.md#la-cloche-na-pas-repris) pour la comparaison à attaques préservées ou supprimées. | Ne pas confondre réapparition au premier plan, changement de porteur et reprise après silence. Une hauteur commune dans le spectre ne choisit pas entre les trois. |
| Faire sentir que le mouvement continue alors que le fichier boucle | [MUS-2327](courses/udem/MUS-2327.md#un-retour-de-thème-nest-pas-forcément-un-tour-de-boucle) pour distinguer début, rappel interne et tour, [OCOMP-490](courses/berklee-online/OCOMP-490.md#interrompre-le-moteur-puis-le-relancer--schubert-gretchen) pour l’arrêt intentionnel du moteur, [MUS-2328](courses/udem/MUS-2328.md#le-raccord-rythmique-et-la-coupure-audio-sont-deux-problèmes) et [MUS-3322X](courses/udem/MUS-3322X.md#deux-échantillons-proches-ne-suffisent-pas-à-un-raccord) pour distinguer l’attaque d’entrée et la coupure de la queue. | Une phrase peut revenir sans qu’on soit revenu au début du cycle. À l’inverse, un raccord propre au niveau des échantillons ne suffit pas si le geste d’entrée se rejoue. Ne pas appliquer un fondu comme correction de forme. |
| Ouvrir une nouvelle section sans perdre l’élan au point de passage | [Mozart K. 457](courses/berklee-online/OLART-234.md#une-attaque-peut-finir-une-phrase-et-en-lancer-une-autre) pour la fonction double d’une attaque, [CM-231](courses/berklee/CM-231.md#préparer-le-finale-sans-retarder-le-changement-de-mouvement) pour la préparation étagée et [MUS-2328](courses/udem/MUS-2328.md#faire-entrer-une-section-sans-couper-lancienne-dun-bloc) pour distinguer anticipation et prolongation. [FILM-205](courses/berklee/FILM-205.md#fixer-ce-que-limage-doit-atteindre-pas-toutes-les-entrées) ajoute l’obligation de garder le repère absolu. | Ni deux sons simultanés ni une frontière sans silence ne font à eux seuls une élision. Ne pas déplacer le point harmonique ou le repère d’image simplement pour avancer la première couleur. |
| Évoquer une couleur de bossa sans perdre le thème ni le point d’arrivée | [OPIAN-300](courses/berklee-online/OPIAN-300.md#entendre-deux-couches-dans-une-même-guitare) pour séparer le pouce, les tirés et les réattaques. [OCOMP-493](courses/berklee-online/OCOMP-493.md#une-couleur-ne-se-déduit-pas-dun-accord--jobim) pour l’harmonie et la forme. [MUS-2328](courses/udem/MUS-2328.md#couleur-sous-la-loupe--trois-façons-de-changer-le-même-arpège) pour entendre séparément placement, son et notes dans un arrangement fixé. | Une guitare nylon, des accords enrichis ou des contretemps ne suffisent pas à attribuer un style. Ne pas déduire l’effet à l’écoute de la seule invariance du MIDI. |
| Rendre une reprise plus intense à battue fixe, sans reléguer le thème | [Ravel](courses/berklee-online/OCWPR-366.md#ravel--le-thème-change-de-porteur-avant-de-grossir) pour le relais au-dessus d’un fond stable. [Grieg](courses/berklee/CM-231.md#grieg--le-crescendo-et-laccélération-sont-deux-consignes) pour la montée à plusieurs paramètres et son contre-cas de subdivision. [MUCO-360](courses/mcgill/MUCO-360.md#grandir-sans-courir) et [MUS-3322X](courses/udem/MUS-3322X.md#égaliser-le-total-sans-régler-la-place-du-thème) pour distinguer gain, ajout de rôle et niveau du thème. | Plus de parties ne veut pas dire plus de lignes indépendantes. Faire monter tout le mix ne remet pas le thème devant son accompagnement. Un même niveau moyen n’implique ni le même premier plan ni une intensité perçue égale. |

L’[atelier à quatre versions](courses/berklee-online/OLART-234.md#un-motif-quatre-parcours--atelier-découte) fournit un premier exemple de cette discipline. Chacun des deux choix est comparé à la fois avec et sans l’autre. L’indépendance est vérifiée dans les événements du MIDI, pas postulée pour la perception. En particulier, rien ne garantit que les deux changements paraissent s’additionner à l’écoute.

**Requête transversale — rendre le retour reconnaissable, mais lui donner une autre assise.** Noter ce qui reste fixe et à quelle échelle. Une voix peut garder ses hauteurs, son rythme ou son contour sans garder sa position ou son rôle. Dans [*So What*](courses/berklee/CM-385.md#le-même-mode-sur-un-autre-centre--miles-davis), le pont transpose le dessin et conserve le type de mode. Chez Debussy aux m. 4–5, le pas garde ses hauteurs tandis que ses soutiens et la collection changent. Chez Chopin, la chronologie des mouvements internes suffit à changer les accords intermédiaires. Si l’arrivée doit **fermer** et pas seulement marquer un appui, [comparer les trois pauses du prélude](courses/udem/MTE-1221.md#chopin--larrêt-ne-dit-pas-sur-quel-accord-on-sarrête). Pour une boucle, [identifier quelles attaques peuvent encore changer à la phase courante](courses/udem/MUS-2328.md#changer-la-couleur-dune-boucle-sous-un-thème-verrouillé). [Le témoin tardif](courses/udem/MUS-2328.md#une-seconde-pour-changer-dassise) montre pourquoi une couleur disponible immédiatement peut arriver sur l’ancienne basse, ou en même temps que la note qu’elle devait remplacer. Si la demande ne fixe que la mélodie, proposer plusieurs solutions et préciser ce qui reste à écouter.

**Requête transversale — intensifier le milieu en gardant le chant et le point d’arrivée.** Demander d’abord si « garder » concerne les hauteurs, les attaques du chant en secondes, sa saillance ou les trois. Pour des attaques verrouillées, chercher le mouvement supplémentaire dans une autre voix. L’op. 109 donne une raison de réécouter le résultat : la voix la plus aiguë peut devenir le plan figuré sans être le chant. Si la battue doit rester lisible, une cellule identifiable et un grave constant peuvent aider, mais ne la garantissent pas. Si l’effet visé est seulement de maintenir la continuité, le balancement de Chopin offre une autre voie que la diminution de l’Arietta. Rapporter ce que les notes et les temps établissent, puis l’écoute encore nécessaire pour choisir.

Pour un **changement d’état sans heure fixe**, [MUS-2328](courses/udem/MUS-2328.md#monter-lintensité-dune-boucle-sans-casser-son-cycle) ajoute la phase de boucle au choix : une couche plus active peut garder le cycle, un autre trajet exige de choisir un raccord. Deux boucles au même BPM et dans la même tonalité ne sont pas forcément superposables au même point du cycle.

**Requête transversale — la boucle semble repartir de zéro.** Identifier ce qui révèle le départ avant de choisir. **Forme** : le signal initial est-il réservé à l’entrée ou écrit dans chaque cycle ? **Mouvement** : quelle couche porte la pulsation sous le raccord, indépendamment du rappel de thème ? **Signal audio** : faut-il conserver une queue en traversant la frontière ? Comparer les solutions dans cet ordre. Par exemple, garder le débit du grave et le retour harmonique mais retirer le signal d’entrée à chaque tour. Un [accord qui prépare ou anticipe l’arrivée](courses/berklee/AR-228.md#le-prochain-tour-commence-à-se-préparer-avant-sa-barre) peut aussi faire avancer la phrase sans fortifier le premier temps. Ensuite seulement comparer les rendus avec queue préservée ou coupée. Si l’objectif est justement de marquer un choc dans la scène, un arrêt puis une reprise fragmentaire comme chez Schubert devient une option, pas un défaut à gommer.

**Requête transversale — faire arriver une section à l’heure sans en faire un nouveau départ.** Identifier séparément le **premier indice**, **l’appui exigé au seuil** et **le dernier événement actif de la section sortante**. Si l’intention interdit d’annoncer la suite, garder le premier indice au seuil et transporter l’élan dans une voix commune ou un écho sortant. Si la section suivante doit être annoncée, choisir quel élément préparer avant, et vérifier que ses hauteurs conviennent aussi à l’harmonie précédente. Si la cadence doit rester parfaitement lisible, ne proposer un point partagé que si la même attaque satisfait réellement la résolution et lance le nouvel incipit. À durée fixe, préférer d’abord des solutions qui désynchronisent les rôles sans déplacer l’appui. Donner les positions et leurs preuves, puis laisser à l’écoute la décision sur le caractère.

**Requête transversale — garder mon thème, mais rapprocher l’arrangement d’une couleur de bossa.** Séparer une impression (« mon oreille entend du latino »), une référence nommée (une prise, un passage) et une contrainte écrite (par exemple même mélodie et même cycle). Le témoin ne doit pas imposer du nylon si la référence repose sur un dialogue entre graves et accords. Le [quintette sans guitare chez Silver](courses/berklee/AR-111.md#faire-voyager-le-rôle-pas-linstrument--horace-silver) permet de chercher la fonction dans un autre porteur, sans prendre le morceau métissé pour une définition du genre. Relever le cycle des appuis et la place des attaques supérieures, puis leurs fins. La [comparaison des deux prises d’*Outra vez*](courses/berklee-online/OPIAN-300.md#même-chanson-et-même-guitariste-nouveau-plan-daccompagnement--outra-vez) donne un choix supplémentaire. Préserver la signature au retour et déplacer la variation à une position reconnaissable à l’intérieur du A. S’il manque des parties séparées, apporter une transcription sûre ou laisser l’attribution incertaine. Pour une autre couleur harmonique, contrôler les notes de tension contre le chant et l’accord au moment où elles sonnent, pas seulement la liste des degrés de la gamme. Pour une modification de rendu, écouter à deux placements différents, puis vérifier le niveau de la partie isolée. Un niveau de mix inchangé peut cacher un arpège moins en avant. L’écoute à niveau de piste comparable ne supprime pas toute différence de saillance. Décrire la variante disponible, la propriété qu’elle conserve, le contre-cas et quelque chose de concret à écouter. Une hypothèse perceptive n’est pas un champ d’analyse déjà validé.

**Exemple de réponse à cette requête.** Pour *Nouvelle section, même élan*, le passage examiné est l’ouverture des quatre premières mesures de A, et non la transition à la flûte. L’arpège est discret et décalé. Ce qu’on peut promettre dans une variante se formule au niveau des parties, pas au niveau du genre.

| Si la demande signifie… | Choix compatible | Contrôle qui peut faire rejeter ce choix |
|---|---|---|
| « Garde cette poussée quand la palette change » | Garder les attaques et les hauteurs de l’arpège dans un premier essai, puis vérifier sa place dans le nouveau mix. | Si le changement de niveau masque le dessin, compenser la partie avant d’écarter le timbre. Si l’effet dépend des coïncidences exactes, un motif de basse réécrit n’est pas un remplacement équivalent. |
| « Rends le balancement plus ou moins marqué, sans toucher à l’arrivée » | Comparer les attaques hautes au grave commun, puis choisir lesquelles se joueraient à contretemps. Au seuil, tester séparément l’attaque d’un nouvel accord et sa tenue. | Si les notes de l’accord suivant ne sont pas acceptables avant la basse de destination, garder l’harmonie en place et ne préparer que le geste. Si une queue couvre l’appui de reprise, son extinction reste à vérifier à l’écoute. |
| « Rapproche le morceau d’une prise précise » | Nommer la prise et le passage, relever les rôles du grave, des accords, du chant et des percussions, puis distinguer une cellule ordinaire d’une variante à la frontière. | Un exemple qui ne montre qu’un arpège, sans attaques d’accords et sans chant, ne peut pas servir de preuve de fidélité à la batida ou au phrasé de Gilberto. Si une partie manque, rendre compte de cette lacune avant de proposer une imitation. |

La base peut donc répondre avec une **hypothèse locale**, les **contraintes préservées**, les **contre-cas** et les **écoutes à faire**, avant que quiconque compose un morceau. C’est le même geste que pour un raccord en jeu. Une observation sur le rendu n’est pas automatiquement une règle d’écriture.

**Requête transversale — la deuxième reprise doit prendre de l’ampleur, sans courir ni perdre le thème.** Exprimer séparément ce qui est verrouillé (pulsation, attaques de la phrase, phase de boucle, repère en secondes) et le contraste voulu (plus fort, plus large, plus mobile, nouveau premier plan). À l’analyse, relever quatre pistes d’indices avant de diagnostiquer la montée.

| Indice à localiser | Ce qu’il permet de distinguer | Si la contrainte de création l’interdit |
|---|---|---|
| Entrées par rôle, hauteur réelle, rythme relatif | Un nouveau porteur se substitue au précédent. Une doublure le renforce. Un contrechant a une trajectoire propre. Un registre élargi ne tranche pas à lui seul. Le relais du [moteur de Holst](courses/berklee/CM-320.md#holst--garder-le-moteur-en-changeant-qui-le-joue) change les parties sans faire disparaître le cycle. | Garder le porteur et changer d’abord le soutien. Si les attaques du thème sont fixes, chercher le mouvement dans une autre partie. |
| Subdivisions dans les parties, puis temps de battue en secondes | Le débit d’une voix peut augmenter à tempo stable, ou ses subdivisions s’alléger malgré un tempo plus vif comme aux violons de Grieg à B. Une même partition peut produire des profils de battue différents, comme dans les [deux transferts de Ravel](courses/berklee-online/OCWPR-366.md#pulsation-stable-dans-une-prise-resserrée-dans-une-autre). | Garder la battue, la carte de tempo et le point d’arrivée. Si la battue est libre mais que deux repères sont fixes, les recaler ne suffit pas à conserver ceux qui se trouvent entre les deux. [FILM-205](courses/berklee/FILM-205.md#caler-deux-coupes-sans-confondre-tempo-et-niveau). |
| Trajectoire de niveau du mix et du thème seul, attaques autour des nouvelles entrées | Un gain commun change le total sans redistribuer les rôles. À total égal, l’équilibre peut changer. Sans pistes séparées, l’attribution d’un changement de niveau à un pupitre peut rester indécidable. | Si une réplique ou un bruitage impose un plafond, maintenir le thème et essayer de libérer de l’espace dans le soutien. Vérifier le son entier sur la scène. |
| Position musicale des entrées et délai depuis la demande | Une réaction de gain et une attaque de motif n’ont pas les mêmes conditions de délai. Un moteur peut dévoiler une couche à la phase courante, mais pas rejouer une attaque passée sans changer le geste. | Si le délai est trop court, choisir un autre premier signal ou une entrée compatible plutôt que relancer le cycle. [Application jeu](courses/udem/MUS-2328.md#intensifier-sans-remettre-la-boucle-à-zéro). |

**Exemple de choix justifié.** Dans [l’atelier MUCO-360](courses/mcgill/MUCO-360.md#grandir-sans-courir), écarter l’accélération préserve les appuis et le repère. Si la demande est une urgence plus audible, proposer C contre B pour savoir si les parties supplémentaires apportent quelque chose au-delà du gain. Si les niveaux doivent rester proches du témoin, comparer D à A. Si la question devient « le nouveau fond couvre-t-il mon thème ? », comparer E à D et vérifier la phrase en contexte. La conservation du signal de clarinette dans E est une preuve de rendu, pas celle de sa saillance chez un auditeur. Une réponse d’analyse cite ces événements et ce qu’elle ne sait pas. Une réponse de création propose une option et un critère d’écoute sans transformer Ravel ou Grieg en recettes.

**Cas de décision — la demande de jeu manque la première note.** Dans [La note est déjà partie](courses/udem/MUS-2328.md#la-note-est-déjà-partie), l’alerte tardive survient 50 ms après le départ écrit de l’alto. Si la réponse doit commencer sans attente et que le début du motif est dispensable, essayer de dévoiler la piste en phase. Si une attaque entière compte plus que la première note exacte, choisir une autre attaque compatible dans le même tour. Si l’incipit doit absolument être intact, attendre une reprise équivalente et vérifier le délai maximum accepté. Avec les horaires de l’atelier, un plafond de 500 ms accepte C et rejette D. Une contrainte interdisant aussi de retirer la première note et de la révéler en cours ne laisse aucune de ces options. La synthèse doit signaler le conflit ou proposer un signal distinct, sans faire croire qu’un fondu rend toutes les contraintes simultanément satisfaisables.

**Cas de décision — même mélodie, autre assise sans attendre la fin de la boucle.** La création reçoit la mélodie et sa phase comme contraintes, un « nouveau fond » comme intention encore ouverte, et éventuellement un délai. La synthèse rend les alternatives ci-dessous, avec leur raison d’être et ce qui manque. Elle ne rend pas une étiquette unique de style ou de tonalité.

| Si la demande précise… | Choix que la synthèse peut proposer | Veto ou contrôle à l’écoute |
|---|---|---|
| « Même hauteur absolue au chant, même point d’appui » | Conserver le mi grave et comparer do/do♯ dans [Sous les mêmes notes](courses/udem/MTE-2316.md#sous-les-mêmes-notes-un-autre-sol). | Écarter la transposition du pont de [*So What*](courses/berklee/CM-385.md#le-même-mode-sur-un-autre-centre--miles-davis), qui déplacerait les hauteurs. Réécouter si la note colorante attire le centre ailleurs. |
| « Même départ et même arrivée, mais que ça avance entre les deux » | Comparer les ordres de déplacement des deux voix intérieures dans [Trois voix, une descente](courses/berklee/CM-221.md#trois-voix-une-descente). | Les bornes ne garantissent pas les mêmes verticales ni le même moment perçu de résolution. Écarter une voix anticipée si elle révèle trop tôt l’arrivée. |
| « Une autre assise, dans l’ordre basse puis couleur » | Dans [Une seconde pour changer d’assise](courses/udem/MUS-2328.md#une-seconde-pour-changer-dassise), conserver le passage de la basse puis du piano ou attendre la prochaine paire d’attaques. | Écarter le do♯ sur l’ancienne basse si l’ordre est impératif. Écarter aussi son recouvrement avec do si une seule couleur est autorisée. À délai incompatible, proposer un signal dans une autre couche. |
| « Ramène ce son au premier plan, ne rejoue pas la phrase » | Garder la piste et dégager son registre, comme le contraste A/B de [La cloche n’a pas repris](courses/udem/MUS-3322X.md#la-cloche-na-pas-repris). | Ne pas choisir le cas C/D si la continuité est exigée. Si la piste est toujours présente, sa présence écrite ne garantit pas qu’on l’entende sous le nouveau fond. |

**Cas de décision — décaler les appuis sans déplacer le temps.** Le mot « rythme » ne désigne pas une seule variable. Relever l’unité qui reste stable, la couche qui porte chaque appui, la période, la phase et la fonction de l’arrivée. [Biamonte, § 2.1](https://www.mtosmt.org/issues/mto.14.20.2/mto.14.20.2.biamonte.html) appelle déplacement un conflit de phase entre groupements de même longueur, et conflit de groupement un conflit entre longueurs différentes. Les [deux cas de rock](courses/berklee/MHIS-322.md#la-guitare-ne-donne-pas-toujours-la-barre) séparent aussi une lecture révisée après coup d’un conflit qui reste audible sur plusieurs cycles. Pour une captation, préciser la prise et distinguer l’accent de niveau de l’accent de durée, comme dans [Mozart K. 550 chez Britten et Marriner](courses/berklee/COND-217.md#la-mesure-forte-ne-change-pas-au-même-moment). Une mesure très accentuée peut être le moment où l’on réinterprète le groupe, pas celui où la phrase a atteint sa destination. [Le témoin agogique](courses/berklee/COND-217.md#avant-ou-après-la-même-attaque) sépare l’intervalle avant l’attaque, celui après, la tenue de la note et la vélocité. Pour un seul point verrouillé, chacune de ces solutions préserve l’heure du repère. Pour une grille voisine verrouillée, seules certaines restent compatibles.

| Ce que la demande verrouille | Comparaison que la synthèse peut proposer | Contrôle ou motif de rejet |
|---|---|---|
| « Même trame et mêmes attaques, mais un autre balancement » | Dans [Six croches](courses/berklee/CM-320.md#six-croches-deux-reliefs), A/B ou C/D ne changent que les accents du marimba. Si ce n’est pas assez, B/C autorise ensuite une modification du nombre et de la place des attaques du grave. | L’[exemple en 6/8 et 3/4 rendu à l’identique](courses/berklee-online/OEART-120.md#changer-le-six-huit-sur-le-papier-sans-changer-le-son) interdit d’utiliser la seule étiquette pour prétendre avoir changé l’écoute. B/C ne respecte plus une contrainte d’attaques identiques du grave. |
| « Mêmes mesures, mais des phrases qui poussent par trois plutôt que par quatre » | Garder la grille et la phrase. Faire entendre un départ de groupe plus ou moins tôt dans [Trois mesures ou quatre](courses/berklee-online/OCOMP-485.md#trois-mesures-ou-quatre). Le passage de B à C conserve la période de trois et déplace sa phase d’une mesure. | Comparer les variantes au même point d’arrivée. Une récurrence de timbale qui disparaît ou glisse ne fixe pas seule la vraie frontière d’une séquence. Si plusieurs repères d’image doivent rester audibles, vérifier leur série entière et l’attaque dans le mix, comme dans [FILM-205](courses/berklee/FILM-205.md#une-image-une-phase-plusieurs-appuis). |
| « Les deux plans doivent finir au même repère » | À unité commune et départ aligné, la première nouvelle rencontre des cycles par 3 et 8 a lieu après 24 unités. Si la phase change, recalculer les rencontres à partir des deux dates de référence. | Un régime régulier n’assure pas une rencontre arbitraire. Pour deux cycles de périodes 4 et 6 et phases 0 et 1, la parité des repères empêche toute rencontre exacte. Réécrire une fin de groupe, déplacer une phase ou renoncer à l’une des deux coïncidences. Ne pas transformer un calcul de rencontre en preuve d’une cadence. |
| « Réponds tout de suite, mais marque encore l’arrivée prévue » | Dans [L’accent arrive trop tôt](courses/udem/MUS-2328.md#laccent-arrive-trop-tôt), une note tenue à travers le repère et un signal bref suivi d’une réattaque livrent deux résultats distincts. | Si la réaction rapide et une nouvelle attaque à la barre sont toutes deux obligatoires, écarter le maintien seul. Si la basse doit aussi rester liée, mettre le signal immédiat dans une autre couche. Un emplacement autorisé par la grille n’autorise pas n’importe quelle note. |

L’analyse fournit ici les positions, les parties et les alternatives plausibles. La création choisit une réalisation, écarte les variantes incompatibles et fait écouter le reste. Ne pas déduire un appui entendu d’une vélocité ni une intention de direction d’un pic d’amplitude isolé.

C’est un **contrat documentaire** pour les échanges futurs, pas un schéma de données, une API ou une mise en production. Cette passe ne lève aucune porte L01–L05 et n’ajoute ni moteur ni générateur.

## 6. Source de vérité et prochaine construction

- [OBJECTIVES.md](OBJECTIVES.md) : pourquoi le système existe.
- [university-curriculum.md](university-curriculum.md) : quels savoirs
  universitaires doivent être examinés.
- [todo-university-coverage.md](todo-university-coverage.md) : quelles
  acquisitions, preuves et validations restent à réaliser.
- [course-material-collection.md](course-material-collection.md) : comment
  obtenir et attester la matière de chaque cours, **maintenant**.

**Prochaine tâche active :** obtenir un contenu pédagogique précis pour
**chaque cours**, en notant les chapitres, lectures, exercices, exemples et
lacunes avec leurs sources. Le futur registre versionné suivra ensuite la
chaîne `programme → cours → chapitre/objectif → concept académique unifié →
capacité MIDI analysable → preuve` ; il ne doit pas être rempli au hasard
à partir des seuls intitulés du catalogue.
