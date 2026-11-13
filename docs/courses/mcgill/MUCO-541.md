# MUCO 541 — Advanced Digital Studio Composition 1

Sources publiques consultées le 10 novembre 2026.

## Cours recensé

Obligatoire, Composition 2026. Esthétique, poétique et analyse de l’électroacoustique, synthèse et traitement du signal, pièce complète avec performance éventuelle. [Description institutionnelle](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements).

## Support parallèle consultable

MIT 21M.361, module 4. Quatre consignes de Max/MSP abordent synthèse, procédés et interaction, avec projet final. Ce cours d’introduction sert uniquement d’exemple de travaux pratiques. Il ne documente ni le niveau avancé ni les lectures esthétiques de McGill. [Support et contenu](https://ocw.mit.edu/courses/21m-361-composing-with-computers-i-electronic-music-composition-spring-2008/pages/assignments/).

## Lacunes

Ce support externe documente les sujets indiqués dans la fiche, avec sa propre progression. Les lectures prescrites, consignes, exemples et critères du cours recensé restent à obtenir auprès de l’établissement.


## Application à l'analyse et à la création — application conditionnée par l'audio ou les projets (12 novembre 2026)

**Code : MUCO 541. Contribution :** directe pour l'analyse/création sonore, surtout par audio et outils de synthèse. **[Preuve : description institutionnelle Advanced Digital Studio Composition 1 : esthétique, analyse électroacoustique, synthèse et traitement du signal, pièce complète; exercices MIT voisins mais non équivalents](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements)**. **Aucun MIDI original créé** pour cette passe : son contenu serait arbitraire ou le phénomène exige audio/partition/contexte, plutôt que seule liste de notes.

### Apprentissage ou domaine 1 — Synthèse sonore et traitement du signal

**Attestation :** domaine décrit dans la notice, sans attribution d'exercice spécifique. **Catégorie :** `AUDIO_REQUIRED / MIDI_PROXY`.

**Analyser de la musique — procédure :** 1. Charger audio source, signal synthétisé et métadonnées de paramètres si connues. 2. Mesurer contenu spectral, amplitude, transitoires et évolution avant/après traitement. 3. Pour tester une technique de synthèse, comparer une description de patch ou un ensemble de partiels avec le rendu effectif. 4. Ne pas prendre des notes MIDI ou un Program Change comme preuve de l'algorithme réellement utilisé.

**Composer en réutilisant le domaine — procédure :** 1. Définir une matière sonore originale par un oscillateur ou une capture. 2. Programmer des enveloppes/transformations, rendre plusieurs essais audio et contrôler le spectre et les artefacts. 3. Composer une forme qui réutilise ces états et consigner la méthode pour pouvoir la reproduire.

**Support d'exemple et limites :** Un fichier MIDI peut piloter une synthèse mais ne montre ni la forme d'onde ni les transformations. Un exemple honnête demanderait audio, réglages et patch ou script de synthèse.

### Apprentissage ou domaine 2 — Forme de la pièce électroacoustique et jugement esthétique

**Attestation :** domaine décrit dans la notice, sans attribution d'exercice spécifique. **Catégorie :** `AUDIO_REQUIRED / CONTEXT_REQUIRED`.

**Analyser de la musique — procédure :** 1. Segmenter l'enregistrement en événements, masses, transitions et silences; comparer densités spectrales/énergie et leur durée. 2. Confronter l'interprétation à une écoute critique et au contexte de l'œuvre. 3. Séparer les données objectives du jugement esthétique sans prétendre identifier l'intention de l'auteur.

**Composer en réutilisant le domaine — procédure :** 1. Définir introduction, transformation, rupture éventuelle et conclusion avec des sons choisis. 2. Produire un montage sonore, l'écouter puis ajuster le parcours perceptif. 3. Documenter les essais et la réponse des auditeurs quand pertinente.

**Support d'exemple et limites :** Les séances, œuvres de référence et critères de jugement de MUCO 541 ne sont pas publics. Aucun MIDI factice de « composition électroacoustique avancée ».

### Verdict

- **Apport :** directe pour l'analyse/création sonore, surtout par audio et outils de synthèse.
- **Domaines évalués :** 2, sans garantie de couvrir des objectifs individuels non publiés.
- **Drapeau :** `non_algorithmique=false` (valeur nulle = matière de section trop variable ou inconnue, et non absence d'algorithmique possible).
- **MIDI :** non produit, pour ne pas inventer d'apprentissage spécifique; supports mieux adaptés indiqués ci-dessus.
- **Lacunes :** projets de section, œuvres et critères réels, statuts académiques inchangés.

## Deuxième passe qualitative — forme électroacoustique, transformations et attentes audibles (12 novembre 2026)

**Provenance du code.** Les [exigences McGill 2026–2027](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) décrivent **MUCO 541 — Advanced Digital Studio Composition 1** : esthétique et poétique électroacoustiques, analyse de ce répertoire, synthèse et traitement numérique, **réalisation de pièces complètes** avec éventuelle composante de performance live. Les exercices MIT cités dans la fiche relèvent d'un **cours différent**, et les œuvres, outils exacts et travaux d'une section MUCO 541 ne sont pas publiés. Les protocoles ci-dessous sont des **applications AnaMu**, non des séances attestées. Les preuves attendues sont principalement **audio et paramètres de production**, et non MIDI.

### Q1 — Reconnaître un retour sonore malgré une transformation timbrale

**Analyser une œuvre existante.** Obtenir le fichier audio et, si possible, les sources/paramètres de production. Segmenter les événements en comparant attaques, enveloppes, durée, contour spectral, répétition de grains ou figures rythmiques; aligner les ressemblances dans le temps et tester si un matériau retourne sous filtrage, étirement temporel ou changement d'espace sonore. Préserver plusieurs lectures possibles (même source transformée, source différente mais similaire) tant qu'aucun projet de studio ne les départage.

**Créer et contrôler.** Fabriquer trois occurrences d'un matériau audio original : première présentation, version transformée mais reconnaissable et version fortement contrastée. Les disposer dans une forme simple à retour, écouter si les relations survivent et conserver audio de départ, traitements et rendu final comme preuves.

**Faux positifs / catégorie.** Une proximité de centroides spectraux ou d'enveloppes ne prouve pas une même source; un motif de notes MIDI identique peut produire des sons très différents. `AUDIO_REQUIRED / CONTEXT_REQUIRED / MIDI_PROXY`.

### Q2 — Transition, continuité et rupture : segmenter avec des indices indépendants

**Analyser.** Suivre sur l'audio l'énergie RMS, la densité d'attaques, l'évolution spectrale, les silences et la répartition spatiale lorsque des canaux multivoies existent. Comparer les frontières proposées par ces mesures à l'écoute des changements de geste et de texture. Vérifier si une transition est progressive (morphing, fondu, déplacement d'énergie) ou une rupture (coupure, silence, attaque contrastée) et si la perception dépend du niveau de diffusion.

**Créer et contrôler.** Écrire une courte pièce où A mène à B par transformation progressive, puis fabriquer une seconde version reliant les mêmes matériaux par coupure franche; conserver des niveaux de lecture comparables et comparer l'orientation perceptive de l'auditeur à chaque jonction.

**Faux positifs / catégorie.** Une hausse RMS ne prouve ni un climax ni une émotion; une variation du centre de gravité spectral dépend du matériau et du dispositif. Les logiciels et méthodes de segmentation sont **suggestions AnaMu**, pas des exercices confirmés. `AUDIO_REQUIRED / CONTEXT_REQUIRED`.

### Q3 — Attente dans une forme sonore complète : régularité locale puis écart motivé

**Analyser.** Sur plusieurs épisodes, relever un schéma reproductible (fréquence d'apparition d'une attaque, durée des silences, retour d'une texture ou d'un contraste de registres), puis formuler une prédiction **datée avant l'événement suivant**. Contrôler si le retour prévu survient, est retardé ou transformé; distinguer la surprise définie par ce schéma local de toute attente psychologique universelle. Lire les déclarations d'intention disponibles comme **contexte** et non comme mesure acoustique.

**Créer et contrôler.** Construire une séquence audio originale A–B–A–B établissant une récurrence; produire une version poursuivant le schéma et une autre qui réoriente progressivement la fin vers C. Faire écouter les deux versions et noter si les transitions sont perçues comme conséquence des matériaux, sans assigner de score esthétique automatique.

**Faux positifs / catégorie.** Une périodicité de segments n'est pas une intention formelle démontrée; l'attente est conditionnée par l'expérience d'écoute et la diffusion. Aucun fichier MIDI ne pourrait prouver les interactions spectrales demandées. `AUDIO_REQUIRED / CONTEXT_REQUIRED`.

**Passerelles analytiques, non programme partagé :** [MUTH-538](./MUTH-538.md) offre des modèles de similarité/attente seulement **conditionnels au thème d'une section**; [CM-357](../berklee/CM-357.md) décrit l'introduction à la morphologie électroacoustique; [CM-358](../berklee/CM-358.md) sépare gestes de contrôle et rendu spectral. Les enseignements et projets de ces cours ne sont pas transférés à MUCO 541.

**Bilan.** Trois protocoles fondés sur une musique réellement sonore, avec variantes et critères de falsification; aucun nouvel exemple MIDI, `non_algorithmique=false` et statuts de première évaluation inchangés.
