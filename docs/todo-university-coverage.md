# AnaMu — TODO de couverture universitaire exhaustive

**Unique liste de priorités du projet.** Objectif : analyser les œuvres
avec la profondeur d'une formation universitaire complète en composition
et orchestration, **avant** d'engager la composition automatique.
Référentiel et sources : [university-curriculum.md](university-curriculum.md).
Principe expérimental : [research-evidence-gates.md](research-evidence-gates.md).

## Mode d'emploi et définition de « terminé »

**Aucune case ci-dessous n'est actuellement validée.** Des primitives
existent (MIDI, relations temporelles, doublures, quartets de voix,
verticalités, passages/broderies), mais ne satisfont pas une compétence
universitaire entière. Les cases ne sont **pas** une estimation d'avancement.

Une ligne ne peut être cochée que si elle possède simultanément :

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

Chaque case devra être liée à une fiche `cours → compétence → opérateur
→ corpus → référence experte → rapport → limites`, en précisant
`non abordé / exploratoire / implémenté non validé / validé`. Un sujet
présent seulement dans une table ou un script n'est **pas terminé**.
L'audit des plans de cours devra enrichir cette liste : **les descriptions
publiques ne sont pas une preuve de couverture exhaustive**.

## A. Inventaire des programmes et gouvernance de la couverture

**Avancement sans case cochée :** le [premier audit UdeM A26](udem-curriculum-a26-audit.md)
a répertorié les 190 cours visibles du catalogue, dont 22 obligatoires
totalisant 63 crédits, avec blocs et crédits. A01 reste **ouvert** : choix,
préalables, validation institutionnelle et plans détaillés sont encore
incomplets. Ce travail ne satisfait pas encore A04, A05 ni la porte L.

- [ ] A01 — Geler les éditions et sauvegarder l'inventaire **complet** de tous les cours du B. Mus. Composition UdeM : obligatoires, blocs, options, crédits, préalables et spécialisations.
- [ ] A02 — Faire de même pour le B. Mus. Composition McGill : exigences de majeure, tronc commun, groupes au choix, ensembles, perfectionnement instrumental et projet final.
- [ ] A03 — Faire de même pour le B. Mus. Composition Berklee : majeure, core, liberal arts, options, projects, ensemble, conducting et senior portfolio.
- [ ] A04 — Obtenir ou substituer par références publiques vérifiables les **plans détaillés** de chaque cours applicable, semaine par semaine / chapitre par chapitre ; consigner les contenus inconnus.
- [ ] A05 — Produire une matrice versionnée **programme → cours → résultat d'apprentissage → sous-compétence** sans lignes orphelines.
- [ ] A06 — Définir explicitement toutes les trajectoires d'options : tronc commun exhaustif pour **trois programmes**, branches composition instrumentale/orchestrale/contemporaine ; exceptions signalées.
- [ ] A07 — Réconcilier les divergences de vocabulaire et de tradition entre les trois programmes sans les aplatir en pseudo-règles universelles.
- [ ] A08 — Comparer l'inventaire aux manuels universitaires de référence pour relever des lacunes de syllabus, sans traiter les manuels comme une validation logicielle.
- [ ] A09 — Attacher à chaque sous-compétence une définition de réussite, des exemples de partition et le corpus de validation compatible.
- [ ] A10 — Établir une gouvernance de revue par au moins un orchestrateur/enseignant et un analyste indépendant ; conserver désaccords et cas impossibles.
- [ ] A11 — Documenter les droits d'accès, les licences et la provenance des syllabus, partitions, MIDI, annotations et enregistrements.
- [ ] A12 — Auditer périodiquement les nouvelles éditions des trois programmes et ne jamais convertir une couverture partielle en pourcentage trompeur.

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
- [ ] E12 — Étudier les fonctions dramaturgiques (anticipation, suspension, résolution, surprise) sans les confondre avec une étiquette d'émotion.

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

## K. Projet intégrateur : analyses complètes et revue indépendante

- [ ] K01 — Constituer un corpus orchestral représentatif, licencié, avec partitions complètes, au moins une autre réalisation quand la question le requiert, et compositeurs non vus au développement.
- [ ] K02 — Produire un protocole pour analyser intégralement un mouvement : notation → voix → motifs → harmonie → contrepoint → phrase → forme → orchestration → expression/son.
- [ ] K03 — Autoriser plusieurs interprétations cohérentes avec preuves et dépendances, plutôt qu'une analyse certaine mais erronée.
- [ ] K04 — Construire un rapport lisible par un étudiant avancé et un orchestrateur, avec extraits de mesures, fonctions musicales et limites.
- [ ] K05 — Évaluer cas mélodiques, homophoniques, polyphoniques, orchestraux complexes, contemporains, atypiques et volontairement piégeux.
- [ ] K06 — Mesurer précision/rappel lorsque pertinent, mais aussi fidélité d'explication, couverture, calibrage d'incertitude et erreurs graves.
- [ ] K07 — Réaliser une expertise aveugle sur les analyses entières par plusieurs musicologues/orchestrateurs, documenter leurs désaccords et corriger les lacunes.
- [ ] K08 — Démontrer que les opérations analytiques et contrefactuelles expliquent des choix **audibles et musicalement pertinents**, pas seulement des notes qui coïncident.
- [ ] K09 — Auditer chaque chemin programme→cours→compétence→preuve : **zéro cours pertinent oublié, zéro case validée par simple présence de code**.
- [ ] K10 — Auditer indépendamment les capacités pratiques/articulées par les cursus et inscrire les limites qui empêchent la revendication d'exhaustivité.
- [ ] K11 — Rejouer tests, corpus indépendants, rapports d'erreurs, licences et analyses sans dépendance à une manipulation manuelle cachée.
- [ ] K12 — Faire approuver le rapport de **couverture exhaustive** par des experts indépendants ; tant que l'avis est réservé, la porte reste fermée.

## L. Porte de passage à la composition (verrouillée)

- [ ] L01 — Toutes les matrices des trois programmes, y compris options pertinentes, sont complètes, datées et auditées.
- [ ] L02 — Toutes les compétences B–J pertinentes sont évaluées avec preuves et limites acceptées par les experts ; aucun « ça devrait marcher ».
- [ ] L03 — L'analyse intégrée K a réussi sur des œuvres **jamais utilisées** pour ajuster les règles, avec protocole d'écoute où nécessaire.
- [ ] L04 — Un rapport expose honnêtement les compétences humaines non représentables et explique si elles bloquent toujours l'exhaustivité demandée.
- [ ] L05 — Léon approuve explicitement la levée du verrou, après examen du rapport scientifique et musicologique.

**Tant qu'au moins une de ces conditions échoue : poursuite de l'analyse
et des validations seulement.** Aucune composition générative, entraînement
pour produire des morceaux, ou promesse d'arrangements agréables. Les
contre-épreuves internes de reconstruction restent autorisées si elles
mesurent exclusivement la compréhension des partitions existantes.
