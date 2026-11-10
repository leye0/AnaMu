# AnaMu — TODO de couverture universitaire exhaustive

**Unique liste de priorités du projet.** Objectif : analyser les œuvres
avec la profondeur d'une formation universitaire complète en composition
et orchestration, **avant** d'engager la composition automatique. Notre cible
est **l'union des contenus instructifs**, même optionnels, recommandés ou
issus de spécialisations alternatives ; elle ne se limite pas aux cours
qu'un étudiant doit suivre pour obtenir son diplôme.
Cette union devra devenir, **après la collecte**, une base de connaissances
académiques unifiée suivant [knowledge-base.md](knowledge-base.md), et pas
une simple liste de matières. Référentiel et sources :
[university-curriculum.md](university-curriculum.md). Protocole actif :
[course-material-collection.md](course-material-collection.md).
Le [registre de progression](data/course-material-progress.json) suit
**332 codes de cours candidats** et les **5 ensembles d'options à déplier**.

La collecte du 10 novembre 2026 ajoute **16 fiches partielles** pour des cours de Berklee Boston, reliées à **12 plans pédagogiques publics distincts** de Berklee Online. Ces plans parallèles complètent les preuves déjà recensées. Les [pistes examinées et les lacunes](course-material-source-trail.md) indiquent où reprendre la collecte UdeM et McGill et détaillent les huit options de majeure explicitement nommées par Berklee.

**VERROU DE PHASE : seuls les travaux de collecte A01–A15, A18 et de revue
de leur couverture sont actifs.** La réconciliation de concepts A16–A17,
les capacités analytiques B–K et la composition L ne commencent qu'avec
l'accord explicite de Léon, après acquisition et vérification du contenu
des cours. **Ne créer aucun nouvel analyseur MIDI à ce stade.**

## Mode d'emploi et définition de « terminé »

**Aucune case ci-dessous n'est actuellement validée.** Des catalogues
ont été inventoriés, mais leur présence ne constitue pas une collecte
des syllabus. Les cases ne sont **pas** une estimation d'avancement.
La progression quotidienne se fait **cours par cours dans le registre** ;
les cases A ne sont cochées qu'après revue exhaustive de leur périmètre.

**Pour A01–A15 et A18 (acquisition)**, une ligne ne peut être cochée que
si chaque cours applicable a une source vérifiable, la matière annoncée
effectivement obtenue ou ses limites explicitement documentées, ses
options examinées et une revue de couverture réalisée. Un catalogue seul
ne clôt jamais un cours.

**Pour A16–A17 et B–L (phases futures)**, les exigences ultérieures sont :

1. une référence **précise** au cours ou au chapitre du référentiel,
   y compris la variété stylistique et les exceptions ;
2. un **contrat de représentation** (observables, hypothèses, inconnus,
   sources et traçabilité jusqu'aux notes et mesures) ;
3. un **mécanisme analytique** explicable et des fixtures positives,
   négatives, ambiguës, limites et contre-exemples ;
4. une **évaluation indépendante** sans fuite, distincte des morceaux
   et compositeurs employés pour le développement, avec baselines, erreurs,
   couverture et reproductibilité ;
5. une **revue musicologique contradictoire** documentée. Tout savoir
   non automatisable exige son épreuve spécifique ou reste non couvert.

Chaque case future devra être liée à une fiche `cours → chapitre → concept
→ mécanisme MIDI → preuve indépendante → limites`, en précisant le statut.
**Pour le moment, la seule fiche à produire est celle de la matière des
cours**, suivant le protocole de collecte. Les descriptions publiques ne
sont pas une preuve de couverture exhaustive.

## A. Inventaire des programmes et gouvernance de la couverture

**Avancement sans case cochée :** les trois inventaires publics sont maintenant
consultables : [UdeM A26](udem-curriculum-a26-audit.md) (190 cours),
[McGill](mcgill-curriculum-2026-audit.md) (58 cours nommés dans les exigences)
et [Berklee 2026F](berklee-curriculum-2026f-audit.md) (44 lignes de grille,
dont des choix et pools). A01–A03 restent **ouverts** : préalables, options
effectivement admissibles, validation institutionnelle et plans détaillés
sont incomplets. Le travail n'a pas encore satisfait A04, A05 ni la porte L.

Un [premier registre vérifiable de 30 candidats de connaissance](data/optional-knowledge-seeds-2026.json)
vient de cours **recommandés à McGill** et de cours de composition, jazz ou
musique à l'image **décrits officiellement par Berklee**. Consulter
[l'audit de ces possibilités](optional-knowledge-audit.md) : il ne démontre
pas l'admissibilité de chaque cours dans la majeure Composition, ni l'examen
de son syllabus ; A13–A15 demeurent ouverts.

- [ ] A01 — Geler les éditions et sauvegarder l'inventaire **complet** de tous les cours du B. Mus. Composition UdeM : obligatoires, blocs, options, crédits, préalables et spécialisations.
- [ ] A02 — Faire de même pour le B. Mus. Composition McGill : exigences de majeure, tronc commun, groupes au choix, ensembles, perfectionnement instrumental et projet final.
- [ ] A03 — Faire de même pour le B. Mus. Composition Berklee : majeure, core, liberal arts, options, projects, ensemble, conducting et senior portfolio.
- [ ] A04 — Obtenir ou substituer par références publiques vérifiables les **plans détaillés** de chaque cours applicable, semaine par semaine / chapitre par chapitre ; consigner les contenus inconnus.
- [ ] A05 — Produire une matrice versionnée **programme → cours → résultat d'apprentissage → sous-compétence** sans lignes orphelines.
- [ ] A06 — Définir explicitement toutes les trajectoires d'options : tronc commun exhaustif pour **trois programmes**, branches composition instrumentale/orchestrale/contemporaine ; exceptions signalées.
- [ ] A07 — Réconcilier les divergences de vocabulaire et de tradition entre les trois programmes sans les aplatir en pseudo-règles universelles.
- [ ] A08 — Comparer l'inventaire aux manuels universitaires de référence pour relever des lacunes de syllabus, sans traiter les manuels comme une validation logicielle.
- [ ] A09 — Recueillir les objectifs, exercices, exemples et critères d'évaluation **enseignés** pour chaque sous-compétence, sans inventer de protocole algorithmique avant la phase MIDI.
- [ ] A10 — Établir une gouvernance de revue par au moins un orchestrateur/enseignant et un analyste indépendant ; conserver désaccords et cas impossibles.
- [ ] A11 — Documenter les droits d'accès, les licences et la provenance des syllabus, partitions, MIDI, annotations et enregistrements.
- [ ] A12 — Auditer périodiquement les nouvelles éditions des trois programmes et ne jamais convertir une couverture partielle en pourcentage trompeur.
- [ ] A13 — Explorer **tous les cours à option, complémentaires, recommandés et hors majeure accessibles** dans les catalogues musicaux des trois établissements, y compris les réserves de crédits ouvertes ; conserver les candidats non encore consultés.
- [ ] A14 — Tenir un registre **cours optionnel → apprentissages distinctifs → décision d'inclusion motivée → compétences TODO**, y compris les cours de jazz, composition à l'image, acoustique/perception, électronique, direction, étude instrumentale et traditions variées ; démontrer les vrais doublons avant de les écarter.
- [ ] A15 — Vérifier avec des spécialistes que l'union des cours inclus ne perd **aucune matière pertinente** du fait de contraintes de choix ou de spécialisation, et étendre B–J dès qu'un nouvel enseignement manque au référentiel.
- [ ] A16 — Concevoir et matérialiser un **registre versionné de connaissances musicales unifiées** (concepts, définitions, mécanismes, prérequis, contextes, exemples, exceptions, sources et provenance multi-cursus), distinct des catalogues administratifs.
- [ ] A17 — Réconcilier les équivalences, nuances et contradictions des contenus universitaires **au niveau des concepts**, avec identifiants stables et navigation bidirectionnelle `cours ↔ concept ↔ preuve`, sans réduire plusieurs traditions à une règle universelle.
- [ ] A18 — Auditer **cours par cours** la complétude des syllabus et contenus réellement disponibles ; tout manque doit être explicite, attribué à sa source et traité avant de déclarer la phase de collecte achevée.

### Collecte des liens — 10 novembre 2026

- **Orchestration et ensembles à McGill** — [MUCO 360](courses/mcgill/MUCO-360.md) dispose d’un sujet d’orchestration et de traces d’une section 2020. Huit options d’ensemble disposent de programmes de concert ou de consignes d’audition. Les pistes vers MUCO 261 et MUCO 460 et les exemples de classement supérieur en théorie restent au statut catalogue.
- **Sciences et sciences sociales à Berklee** — les fiches [LMSC-xxx](courses/berklee/LMSC-xxx.md) et [LSOC-xxx](courses/berklee/LSOC-xxx.md) pointent vers des plans en douze leçons, avec les conditions d’équivalence du registraire. Elles suivent des familles qui restent ouvertes.

- **UdeM** — quatre cours obligatoires avec exercices d’exemption spécifiques en harmonie et contrepoint. Deux cours optionnels d’analyse ont une piste de classement générale, encore au statut catalogue.
- **McGill** — sept cours préparatoires avec des objectifs d’exemption historiques. Chercher les sources des sections actuelles et poursuivre par les cours obligatoires de composition.
- **Berklee** — cinq plans publics d’équivalents en ligne reliés par le registraire aux codes du campus. Seize fiches de Boston rattachées au registre signalent aussi des supports parallèles en composition, arrangement, solfège et musique à l’image. Chercher les plans des sections du campus.
- **Couverture** — 332 entrées suivies, dont 11 syllabus documentés, 153 au statut partiel et 168 au statut catalogue. Cinq ensembles d’options restent à déplier. Le [relevé des options de majeure Berklee](berklee-major-elective-candidates.md) donne 83 codes, dont 70 à vérifier avant intégration au registre.
- **Cours ciblés dans cette passe** — études dirigées et projet final à Berklee avec programme du concert de 2022 et accès au portfolio réservé aux membres de Berklee. Clavier, solfège et analyse classique avec plans parallèles. Acoustique et traitement du son à l’UdeM, puis orchestration, contrepoint et studio à McGill avec supports externes dont la provenance est explicitée dans chaque fiche.

- **Plans UdeM** — treize fiches ajoutées. Quatre syllabus portent les sigles cibles, dont deux plans A26 et deux plans historiques. Neuf fiches conservent des plans-cadres, des documents abrégés ou des preuves ciblées dont les limites sont précisées. La [piste institutionnelle](course-material-source-trail.md#udem--plans-de-séminaires-et-éditions) donne les éditions et la prochaine source à examiner.

- **Harmonie, écoute et composition** — les preuves nouvelles concernent 21 entrées auparavant au statut catalogue. Le [plan conjoint UdeM MUS 3329X / 6329X](courses/udem/MUS-3329X.md) détaille le projet et ses évaluations. Les plans d’harmonie de Berklee Online ont été distingués des sections Boston, et les descriptions McGill de travaux, lectures ou exercices ont été rattachées à leurs sigles quand l’affichage de section le permettait.

- **Direction, orchestration et tutorats** — dix-sept fiches partielles ajoutées. Les plans du Boston Conservatory restent des supports parallèles. Le concert de MUCO 342 atteste des productions de la section H24. Les exemples du concert de composition de mars 2025 sont attribués à la classe, avec niveaux individuels à vérifier.

- **Histoire, formation auditive et écriture tonale** — dix-huit nouvelles fiches partielles. Le plan de section A24 fait passer [MUL 3333X](courses/udem/MUL-3333X.md) au statut syllabus documenté, avec l’édition H27 conservée séparément dans la fiche. Les exemples de formation auditive McGill sont signalés comme exercices de classement.

- **Pratique d’ensemble** — vingt fiches partielles ajoutées, dont dix-huit au bloc 75H de l’UdeM et deux à McGill. Les fiches différencient objectifs d’ensemble, répertoires annoncés, productions historiques et matériel d’audition. L’attribution aux sections et les évaluations restent à vérifier.

- **Écriture, jazz et analyse** — 22 dossiers traités (19 créations, 3 compléments) et 17 passages au statut partiel, avec descriptions des supports parallèles. Cinq dossiers restent au catalogue. Les syllabus des cours cibles restent à obtenir ; [le relevé des sources](course-material-source-trail.md) conserve la discordance de datation du syllabus UNT parallèle à MUTH 528. Reprendre les ateliers MCT 1601/1602 dès qu’une source spécifique devient accessible, puis MCT 1603/1604, 1701/1702, 1801/1802 et les options encore sans matière.

## Phases suivantes — exigences pédagogiques à documenter après la collecte

Les sections B–J ci-dessous sont un **cadre provisoire de compétences à
vérifier contre la matière réelle des cours**. Elles ne remplacent pas
les chapitres des syllabus ; elles devront être augmentées, corrigées ou
réorganisées à partir de ces sources. **Aucun script ni benchmark ne doit
être développé pour cocher ces cases tant que la phase 1 reste ouverte.**

## B. Lecture de partition, théorie élémentaire et fidélité de source

*Repères : UdeM MUS 1011–1016 (choix), MTE 1220/1221 ; McGill MUSP/MUTH ; Berklee ET-231/232 et tronc commun.*

- [ ] B01 — Lire clefs, portées multiples, transpositions, octaves, armures, altérations de précaution, enharmonies, hauteurs écrites/sonnantes.
- [ ] B02 — Conserver voix indépendantes, accords, repos, reprises, sauts, anacrouses, mesures irrégulières, césures, pauses et fermates.
- [ ] B03 — Reconstruire et vérifier les durées **liées entre mesures**, les ligatures, tuplets, grâces et événements d'ornementation sans notes fantômes.
- [ ] B04 — Dérouler les reprises, premières/deuxièmes fins, da capo, coda, ossia et chemins alternatifs en préservant la partition non déroulée.
- [ ] B05 — Distinguer notes réelles, notation de percussion, techniques de jeu, indications verbales et symboles non normalisés.
- [ ] B06 — Représenter intervalles diatoniques/chromatiques, enharmonie, classes de hauteur, registres, échelles, modes et degrés sans réduire le tout au numéro MIDI.
- [ ] B07 — Préserver les accents métriques et l'orthographe rythmique (valeur écrite ≠ durée effectivement jouée).
- [ ] B08 — Aligner MusicXML/MEI ↔ MIDI à l'échelle de la note avec confiance, répétitions et exceptions, sans fusionner les éditions par intuition.
- [ ] B09 — Aligner partition ↔ performance ↔ audio avec des preuves instrumentales et temporelles indépendantes et des marges d'erreur.
- [ ] B10 — Valider le lecteur sur partitions avec polyphonie dense, transpositions, édition divergente et cas non déchiffrables ; publier ce qui reste inconnu.

## C. Harmonie tonale, langage modal et conduite harmonique

*Repères : UdeM MTE 1220/1221, MCT 3011/3012 ; McGill MUTH 150/151/251, MUCO 241/242 ; Berklee CM-221, MLAN-311.*

- [ ] C01 — Reconnaître tonalités/modes et changements de centre sans prendre la collection globale pour une tonalité certaine.
- [ ] C02 — Identifier triades/septièmes, renversements, chiffrage, fondamentales, doublures et réalisations partielles.
- [ ] C03 — Inférer fonctions locales (tonique, pré-dominante, dominante) et prolongations par conduite des voix et contexte phrastique.
- [ ] C04 — Expliquer cadences authentiques, imparfaites, plagales, rompues, demi-cadences, évitements et ambiguïtés stylistiques.
- [ ] C05 — Distinguer note d'accord, passage, broderie, échappée, anticipation, appoggiature, suspension/retard et leurs résolutions.
- [ ] C06 — Différencier pédales, accords incomplets, agrégats de notes étrangères, suspensions et enrichissements harmoniques.
- [ ] C07 — Analyser dominantes et sensibles secondaires, tonicisations et séquences harmoniques.
- [ ] C08 — Analyser modulations diatoniques/chromatiques/enharmoniques et leurs degrés de certitude.
- [ ] C09 — Analyser mélange modal, emprunts, accords napolitains, sixte augmentée, médiantes chromatiques et cadences modulantes.
- [ ] C10 — Représenter réinterprétations enharmoniques, accords symétriques, tonalité élargie et frontières du fonctionnalisme.
- [ ] C11 — Analyser mouvements de basse, basse chiffrée, progressions, diminution harmonique, rythme harmonique et niveaux de prolongation.
- [ ] C12 — Séparer harmonie de surface et réduction structurelle ; permettre plusieurs analyses romanisées justifiables.
- [ ] C13 — Tester harmonie sans utiliser une étiquette DCML incompatible comme vérité des notes étrangères ou de toute la texture.
- [ ] C14 — Confronter harmonies standard, tonalité ambiguë, polytonalité, modalité et cas où l'analyse fonctionnelle n'a pas de sens.
- [ ] C15 — Analyser l'harmonie d'arrangement jazz : voicings par gammes d'accords, upper structures, clusters, positions à cinq/six voix, voicings linéaires et logique de section ; distinguer ces pratiques de l'harmonisation classique.

## D. Contrepoint, polyphonie et indépendance des voix

*Repères : UdeM MTE 1110/1111 ; McGill MUTH 202/204 ; Berklee CP-215.*

- [ ] D01 — Analyser première à cinquième espèces, puis deux, trois et plusieurs voix selon les conventions historiques de l'exercice.
- [ ] D02 — Évaluer consonances/dissonances en relation avec temps fort/faible, préparation, liaison, résolution et style.
- [ ] D03 — Suivre mouvements contraires, parallèles, directs, obliques, croisement/chevauchement, registres, profils conjoints et grands sauts.
- [ ] D04 — Distinguer doublure orchestrale voulue et voix contrapuntique indépendante ; ne pas interdire universellement les quintes parallèles.
- [ ] D05 — Repérer contrepoint imitatif, entrées, réponses, imitation stricte/libre, augmentation, diminution et inversion.
- [ ] D06 — Analyser canon, fugue (sujet, réponse, contresujet, exposition, épisode, strette, pédale) et variations formelles.
- [ ] D07 — Traiter conduites de voix à attaques **non synchronisées**, durées tenues, échanges de voix et relais entre instruments.
- [ ] D08 — Repérer mélodie composée, contrechant, ostinato, imitation par couches et contours masqués par une texture.
- [ ] D09 — Comparer les règles propres au contrepoint modal, tonal, moderne et libre avec exceptions documentées.
- [ ] D10 — Évaluer sur analyses de polyphonie annotées par des experts, pas seulement sur quartets exacts de notes synchronisées.

## E. Mélodie, motifs, phrasé et grandes formes

*Repères : UdeM MCT 1601/1602, MCT 3011/3012 ; McGill MUCO 241/242 et MUTH 251 ; Berklee MLAN-311, CM-398/497.*

- [ ] E01 — Décrire contour, ambitus, direction, respiration, tension locale, appuis, climax, silences et asymétries d'une ligne.
- [ ] E02 — Distinguer motif rythmique, intervallique, mélodique et gestuel et leurs identités perceptives concurrentes.
- [ ] E03 — Détecter séquence, transposition, permutation, inversion, rétrograde, augmentation, diminution, contraction et expansion.
- [ ] E04 — Détecter fragmentation, liquidation, variation, répétition transformée, transition et développement non littéral.
- [ ] E05 — Segmenter cellules, incises, propositions, antécédent/conséquent, périodes, phrases et groupes en hiérarchies alternatives.
- [ ] E06 — Repérer structure de sentence, période, parallèle/contrastante, prolongation, extension et élision de phrases.
- [ ] E07 — Distinguer frontières rythmiques, harmoniques, motiviques, timbrales et de respiration, y compris les frontières contradictoires.
- [ ] E08 — Analyser formes binaires, ternaires, thème-variations, rondo, forme-sonate, scherzo/trio, fugue et formes libres.
- [ ] E09 — Analyser exposition, contrastes, reprise, récapitulation, transition, pont, climax, développement et conclusion sur la durée entière.
- [ ] E10 — Conserver la macro-forme lorsque répétitions et codas déplacent la réalisation temporelle sans changer l'écriture imprimée.
- [ ] E11 — Valider thèmes/phrases/formes sur éditions et répertoires tenus à l'écart avec annotations humaines et désaccords explicites.
- [ ] E12 — Étudier les fonctions dramaturgiques (anticipation, suspension, résolution, surprise) sans les réduire à un simple adjectif subjectif.
- [ ] E13 — Analyser la narration par musique à l'image : relations scène/forme, fonctions des thèmes et leitmotivs, reprises entre séquences, choix de silence et évolution de l'arc dramatique avec preuves audiovisuelles adaptées.

## F. Rythme, métrique, durée et expression temporelle

*Repères : UdeM formation auditive et MTE 1403/1404 ; McGill MUSP/MUTH/MUCO ; Berklee solfège et techniques contemporaines.*

- [ ] F01 — Représenter divisions, subdivisions, accentuation, anacrouse, hypermesure et changement de mètre.
- [ ] F02 — Détecter syncopes, contretemps, anticipations, retards rythmiques, silences articulants et déplacements d'accent.
- [ ] F03 — Distinguer mètre noté, pulsation perçue, groupement rythmique et tempo interprété.
- [ ] F04 — Traiter mètres composés, asymétriques, alternés, polymétrie, polyrythmie, changements et superpositions.
- [ ] F05 — Analyser rubato, agogique, ralentissements, accélérations, ritardando, accelerando, a tempo et changements brusques.
- [ ] F06 — Distinguer indication expressive, valeur MIDI `set_tempo`, microtemporisation humaine et artefact d'alignement.
- [ ] F07 — Reconstruire les courbes de tempo avec incertitude, différentes granularités et fermates sans confondre performance et partition.
- [ ] F08 — Relier gestuelle rythmique, phrase, cadence, orchestration et attentes de l'auditeur ; validation musicale indépendante.
- [ ] F09 — Étudier la synchronisation image/partition/performance : changements de tempo et de mesure, points d'ancrage, montage, musique adaptative et temporalité non linéaire, sans inférer l'alignement du seul MIDI.

## G. Instrumentation, techniques et orchestration complète

*Repères : UdeM MTE 2114/2115 ; McGill MUCO 261, MUCO 360, MUCO 460 ; Berklee CM-231, CM-441.*

- [ ] G01 — Construire un catalogue vérifiable des familles cordes, bois, cuivres, percussions, claviers, harpe, voix et instruments usuels d'ensemble.
- [ ] G02 — Vérifier les tessitures pratiques, registres caractéristiques, transpositions, clefs et difficultés par niveau de jeu.
- [ ] G03 — Modéliser modes de jeu ordinaires/étendus, souffle, cordes, sourdines, doigtés, archet, résonance, percussion et technique.
- [ ] G04 — Analyser articulation écrite et réalisable : legato, détaché, staccato, accent, marcato, pizzicato, tremolo, trilles et effets.
- [ ] G05 — Représenter nuances réelles/notées, crescendos, decrescendos, profils enveloppe et dynamique relative entre pupitres.
- [ ] G06 — Identifier les rôles **locaux** mélodie, basse, harmonie, contrechant, pédale, ostinato, figuration, ponctuation et silence fonctionnel.
- [ ] G07 — Analyser unisson, octave, redoublement et mélanges hétérogènes avec registre, phase d'attaque, densité et objectif auditif.
- [ ] G08 — Décrire répartition de l'harmonie (position serrée/large, doublures, espacements, renversements, relais, équilibre).
- [ ] G09 — Analyser écriture horizontale et verticale des cordes seules : divisions, doublures, contrepoint, textures, articulations spécifiques.
- [ ] G10 — Faire de même pour bois, cuivres, percussions et formations mixtes, en respectant forces/faiblesses instrumentales.
- [ ] G11 — Distinguer orchestration de chambre, petits ensembles, grand orchestre et orchestre contemporain/étendu.
- [ ] G12 — Analyser mélodie accompagnée, homophonie, hétérophonie, polyphonie, masses, nappes, tutti et alternance de texture.
- [ ] G13 — Reconstruire entrée, sortie, densification, raréfaction, changement de couleur et relais de ligne à travers plusieurs mesures.
- [ ] G14 — Analyser équilibre perceptif, masquage fréquentiel, projection, doublure colorante et continuité de timbre **avec audio approprié**.
- [ ] G15 — Lire partition d'orchestre complète, faire réduction piano/ensemble et comparer redistribution orchestrale avec conservation des rôles.
- [ ] G16 — Distinguer intention d'orchestration, étiquette MIDI, échantillon virtuel et performance acoustique ; garder les contradictions.
- [ ] G17 — Vérifier jouabilité/endurance/respiration/articulation avec références instrumentales et, au besoin, musiciens réels.
- [ ] G18 — Valider les analyses d'orchestrations sur **plusieurs compositeurs et styles**, avec jugement expert d'arrangements et contrôle d'écoute aveugle lorsqu'une propriété sonore est invoquée.
- [ ] G19 — Analyser orchestrations et arrangements jazz (big band, petites sections, section rythmique, place de l'improvisation, écriture flexible) avec voicings, équilibre, parties et niveaux de jeu.
- [ ] G20 — Analyser les écritures spécifiques de guitare et clavier : ergonomie, positions, doigtés, figurations, résonances, limites de main et techniques étendues, avec musiciens experts.

## H. Langages contemporains, post-tonalité et notation

*Repères : UdeM MTE 1205/1206, MTE 1403/1404 ; McGill MUTH 350, MUCO 245/246/460/575 ; Berklee CM-311/312, MLAN-312.*

- [ ] H01 — Analyser modalité ancienne/moderne, collections symétriques, pentatoniques, octatoniques, modes à transpositions limitées et systèmes personnels.
- [ ] H02 — Analyser ensembles de classes de hauteur, intervalles, vecteurs, complémentarité, transposition/inversion et limites d'interprétation.
- [ ] H03 — Analyser sérialisme dodécaphonique, rangées, transformations et constructions non tonales quand le répertoire les exige.
- [ ] H04 — Analyser polytonalité, atonalité, clusters, densités d'intervalles, accords quartaux/quintaux et techniques de masse.
- [ ] H05 — Analyser textures de micropolyphonie, hétérophonie, canons complexes et processus graduels.
- [ ] H06 — Analyser micropulsation, métriques mixtes, modes rythmiques, superpositions et organisation du temps hors grille régulière.
- [ ] H07 — Analyser écriture spectrale, hauteur-timbre, partiels, accords dérivés de spectres et évolutions de couleur à partir de preuves sonores ou de partition.
- [ ] H08 — Traiter microtonalité, tempéraments, glissandi, hauteur continue, bruit et paramètres non notables par 12 demi-tons.
- [ ] H09 — Lire notation proportionnelle, graphique, ouverte, aléatoire et instructions textuelles sans inventer de notes déterminées.
- [ ] H10 — Analyser musique concrète instrumentale, techniques étendues, jeu improvisé et interactions exécutant-partition.
- [ ] H11 — Examiner algorithmes/processus compositionnels historiques comme objets **à expliquer**, sans basculer vers un générateur du projet.
- [ ] H12 — Évaluer chaque langage selon ses propres conventions ; ne pas appliquer les critères de cadence tonale à une œuvre sérielle.

## I. Acoustique, perception, électroacoustique et production

*Repères : UdeM MUS 1300/1321, MTE 1503, MUS 3101X/3324X ; McGill MUCO 341/342/541 ; Berklee objectifs de réalisation et enregistrement.*

- [ ] I01 — Représenter fréquence, intensité, spectre, partiels, enveloppe d'attaque/relâchement, résonance et propagation acoustique.
- [ ] I02 — Mesurer timbre/brillance/rugosité/bandes spectrales avec limites de micro, salle, mixage, compression et source instrumentale.
- [ ] I03 — Mesurer volume acoustique et courbes dynamiques sans identifier faussement vélocité MIDI, CC7 et décibels.
- [ ] I04 — Analyser masquage, fusion/ségrégation des flux, identité des voix perçues, saillance mélodique et registres.
- [ ] I05 — Distinguer production du son, timbre instrumental, technique expressive, traitement et effets d'enregistrement.
- [ ] I06 — Examiner FFT/STFT, échantillonnage, fenêtre temporelle, résolution, filtres et autres modèles avec calibration et contrôles.
- [ ] I07 — Identifier réverbération, spatialisation, panorama, égalisation, compression, modulation, synthèse et traitements utilisés dans le contexte.
- [ ] I08 — Étudier électronique fixe, électroacoustique, musique mixte, interaction en temps réel et relations entre partition et technologie.
- [ ] I09 — Aligner notes/gestes/nuances à des signaux réels avec incertitude ; disposer d'enregistrements variés licites et annotés.
- [ ] I10 — Construire des protocoles d'écoute indépendants et reproduisibles pour les questions qu'aucune partition ni MIDI ne peuvent trancher.
- [ ] I11 — Analyser la fabrication et les limites d'une **maquette orchestrale virtuelle** : échantillons, keyswitches/contrôleurs, articulations, transitions, automation, mixage et comparaison en aveugle avec instruments réels.

## J. Histoire, style, interprétation, écriture vocale et savoirs pratiques

*Repères : UdeM MUL 1117 et options d'histoire ; McGill histoire, musicianship, ensemble/performance ; Berklee MHIS-251/252, ET-231/232, direction, portfolio.*

- [ ] J01 — Cartographier les langages et conventions Moyen Âge/Renaissance, Baroque, Classicisme, Romantisme, XXe et XXIe siècles.
- [ ] J02 — Situer formes, instrumentation et écriture dans leur contexte esthétique et social sans essentialiser un siècle ou une culture.
- [ ] J03 — Étudier les pratiques de notation et interprétation historiques : ornementation, tempérament, articulation, basse continue, rubato.
- [ ] J04 — Représenter spécificités de musique vocale : tessitures, respiration, prosodie, syllabation, accent textuel, imitation et chœur.
- [ ] J05 — Étudier adéquation entre texte, phrase musicale et organisation de voix sans déduire le sens des paroles du seul MIDI.
- [ ] J06 — Intégrer les savoirs de solfège, dictée, lecture à vue, mémoire auditive et reconnaissance de flux comme **évaluations propres**, pas équivalents de parseur.
- [ ] J07 — Intégrer connaissances de pratique instrumentale, ensembles, répétition, direction et communication de la partition comme limites/épreuves explicites.
- [ ] J08 — Étudier la construction d'une édition critique et les variantes de partitions avant d'inférer une décision du compositeur.
- [ ] J09 — Évaluer la transférabilité à d'autres traditions/style de composition et décrire les limites du corpus occidental choisi.
- [ ] J10 — Confronter analyses de spécialistes des périodes, des instruments et des musiques actuelles, avec dissensus conservé.
- [ ] J11 — Inventorier et comparer les structures musicales de traditions diverses (rythmes, modes, instruments, pratiques collectives) par leurs propres références expertes, en évitant l'appropriation simplificatrice pour un contexte filmique ou ludique.

## K. Projet intégrateur : analyses complètes et revue indépendante

- [ ] K01 — Constituer un corpus orchestral représentatif, licencié, avec partitions complètes, au moins une autre réalisation quand la question le requiert, et compositeurs non vus au développement.
- [ ] K02 — Produire un protocole pour analyser intégralement un mouvement : notation → voix → motifs → harmonie → contrepoint → phrase → forme → orchestration → expression/son.
- [ ] K03 — Autoriser plusieurs interprétations cohérentes avec preuves et dépendances, plutôt qu'une analyse certaine mais erronée.
- [ ] K04 — Construire un rapport lisible par un étudiant avancé et un orchestrateur, avec extraits de mesures, fonctions musicales et limites.
- [ ] K05 — Évaluer cas mélodiques, homophoniques, polyphoniques, orchestraux complexes, contemporains, atypiques et volontairement piégeux.
- [ ] K06 — Mesurer précision/rappel lorsque pertinent, mais aussi fidélité d'explication, couverture, calibrage d'incertitude et erreurs graves.
- [ ] K07 — Réaliser une expertise aveugle sur les analyses entières par plusieurs musicologues/orchestrateurs, documenter leurs désaccords et corriger les lacunes.
- [ ] K08 — Démontrer que les opérations analytiques et contrefactuelles expliquent des choix **audibles et musicalement pertinents**, pas seulement des notes qui coïncident.
- [ ] K09 — Auditer chaque chemin programme→cours→compétence→preuve, **obligatoire ou optionnel** : zéro cours pertinent oublié, zéro case validée par simple présence de code.
- [ ] K10 — Auditer indépendamment les capacités pratiques/articulées par les cursus et inscrire les limites qui empêchent la revendication d'exhaustivité.
- [ ] K11 — Rejouer tests, corpus indépendants, rapports d'erreurs, licences et analyses sans dépendance à une manipulation manuelle cachée.
- [ ] K12 — Faire approuver le rapport de **couverture exhaustive** par des experts indépendants ; tant que l'avis est réservé, la porte reste fermée.
- [ ] K13 — Auditer l'intégration **base de connaissances → mécanismes d'analyse → explications musicales** sur des œuvres indépendantes, y compris l'apport unique des cours optionnels et les contradictions stylistiques.

## L. Porte de passage à la composition (verrouillée)

- [ ] L01 — Toutes les matrices des trois programmes, y compris **tous les choix et cours optionnels apportant un savoir pertinent**, même hors parcours diplômant unique, sont complètes, datées et auditées ; les exclusions sont justifiées cours par cours.
- [ ] L02 — La base de connaissances unifiée est effectivement constituée et exploitée par l'analyse ; toutes les compétences B–J pertinentes sont évaluées avec preuves et limites acceptées par les experts ; aucun « ça devrait marcher ».
- [ ] L03 — L'analyse intégrée K a réussi sur des œuvres **jamais utilisées** pour ajuster les règles, avec protocole d'écoute où nécessaire.
- [ ] L04 — Un rapport expose honnêtement les compétences humaines non représentables et explique si elles bloquent toujours l'exhaustivité demandée.
- [ ] L05 — Léon approuve explicitement la levée du verrou, après examen du rapport scientifique et musicologique.

**Tant que la phase de collecte n'est pas clôturée et approuvée : acquisition
des cours uniquement.** Ensuite viendront la base de connaissances et les
analyseurs MIDI. Aucune composition générative ni promesse d'arrangements
agréables tant que les portes L01–L05 ne sont pas levées.
