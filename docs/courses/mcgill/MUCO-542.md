# MUCO 542 — Advanced Digital Studio Composition 2

McGill, Schulich, Composition 2026. Sources publiques consultées le 10 novembre 2026.

## Sources et matière

[Exigences de Composition](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements). Option recommandée en studio avancé. Projet d’envergure mobilisant la composition assistée, l’analyse et la resynthèse ou les contrôleurs gestuels pour instruments numériques. L’[affichage Schulich H27, p. 2](https://www.mcgill.ca/music/files/music/winter_2027_-_musicresearch_-_detailed_job_posting.pdf#page=2) prévoit des démonstrations et exercices techniques parallèles. Les compétences demandées à l’auxiliaire de la section de Sean Ferguson comprennent Max/MSP et des outils IRCAM, dont AudioSculpt, OpenMusic et Spat.

## Lacunes

Les outils sont attestés dans l’environnement d’auxiliariat. Leur répartition par séance, les consignes des exercices et les critères du projet restent à confirmer.


## Application à l'analyse et à la création — évaluation sans MIDI trompeur (12 novembre 2026)

**Cours MUCO 542. Apport :** directe pour analyse, synthèse et composition sonore. **Preuve :** [option de studio numérique avancé ; affichage de l'auxiliariat H27 atteste des outils IRCAM/Max en environnement de section, mais pas leur affectation aux devoirs individuels](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements). **Pas de MIDI nouveau** : données de section, audio ou partition nécessaires pour démontrer les compétences sans inventer leur contenu.

### Apprentissage ou domaine 1 — Analyse et resynthèse d'un matériau enregistré

**Classification :** `AUDIO_REQUIRED / MIDI_PROXY`. La matière inconnue est identifiée comme telle, et les sources comparatives ne sont pas attribuées à ce cours.

**Procédure d'analyse :** Obtenir un fichier audio, mesurer spectre, enveloppes et transformations d'un dispositif de resynthèse; vérifier le résultat rendu et les paramètres au lieu d'inférer un procédé depuis les seules notes.

**Procédure de composition :** Définir un son source, reconstruire un spectre ou des enveloppes dans un outil adapté, composer une trajectoire de transformation et exporter audio et patch documenté.

**Exemple nécessaire et limites :** Le MIDI peut piloter des événements, mais ne montre ni spectre mesuré ni algorithme de resynthèse.

### Apprentissage ou domaine 2 — Contrôle gestuel d'un système de synthèse

**Classification :** `CONTEXT_REQUIRED / AUDIO_REQUIRED`. La matière inconnue est identifiée comme telle, et les sources comparatives ne sont pas attribuées à ce cours.

**Procédure d'analyse :** Lire logs de capteurs et mappings du vrai dispositif, aligner leurs valeurs sur le signal sonore et tester la latence. Ne pas supposer que chaque étudiant a utilisé un outil particulier.

**Procédure de composition :** Mapper des gestes documentés à un paramètre sonore, enregistrer plusieurs exécutions puis contrôler la répétabilité et l'intention musicale.

**Exemple nécessaire et limites :** Un exemple fidèle exige capture de gestes, patch et audio; le contenu exact de section reste à confirmer.

### Verdict

- **Apport :** directe pour analyse, synthèse et composition sonore ; `non_algorithmique=false` (indéterminé si la section est trop variable).
- **Évaluation :** 2 domaines, pas l'ensemble des apprentissages; aucun MIDI pertinent pour les preuves disponibles.
- **Suite :** obtenir la véritable partition, l'audio, le syllabus et les consignes du cours.

## Deuxième passe qualitative — resynthèse, geste et direction à grande échelle (12 novembre 2026)

**Preuve propre au cours.** Les [exigences McGill 2026–2027](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) présentent **MUCO 542, hiver 2027**, comme un approfondissement du studio numérique conduisant à une **œuvre de grande envergure**, avec composition assistée par ordinateur, analyse/resynthèse et nouveaux contrôleurs gestuels pour instruments numériques en performance live. L'affichage d'auxiliariat nomme des compétences Max/IRCAM : **aucun devoir n'est attribué à un logiciel particulier**. Les trois études ci-dessous sont des protocoles **AnaMu**, qui exigent audio, paramètres et/ou gestes; pas de MIDI de façade.

### Q1 — Analyse et resynthèse : trajectoire cible versus résultat audible

**Analyser.** Exiger fichier source, paramètres ou patch de resynthèse, rendu audio et conditions d'écoute. Calculer ou relever spectre et enveloppes avant/après, comparer partiels stables, composantes bruitées, transitoires et évolution temporelle. Mesurer l'écart entre une trajectoire cible et la sortie, puis décrire séparément ce que l'algorithme reproduit, transforme ou perd. Tester l'hypothèse « fidélité recherchée » contre « métamorphose esthétique volontaire » à l'aide des intentions documentées si disponibles.

**Composer.** Choisir un son original, construire trois états de resynthèse dont un reste reconnaissable et un s'éloigne volontairement; composer leur enchaînement vers un état de contraste puis un retour partiel. Exporter source, sorties et paramètres et vérifier à l'écoute le rôle de chaque transformation.

**Faux positifs / catégorie.** La similarité spectrale ne garantit ni même source ni même effet perceptuel; les événements de notes ne révèlent pas l'algorithme de resynthèse. `AUDIO_REQUIRED / MIDI_PROXY / CONTEXT_REQUIRED`.

### Q2 — Contrôle gestuel : relation entre mouvement, réponse et stabilité

**Analyser.** Réunir captation des gestes ou logs de capteurs, définition du mapping, timestamps, audio d'entrée/sortie et éventuelle partition. Vérifier la fonction réelle du geste (fréquence, spatialisation, déclenchement, grain, etc.), la latence et les zones où un geste plus ample ne produit plus de variation audible. Distinguer réponse continue, commutation par seuil et automation prédéfinie; comparer plusieurs prises pour évaluer la reproductibilité.

**Composer.** Définir deux gestes physiques mesurables et deux paramètres sonores audibles, puis écrire une courte progression où un geste rapproche une texture d'un seuil de rupture et le second provoque une réponse contrôlée. Enregistrer plusieurs interprétations, corriger la sensibilité et fournir une légende de gestes.

**Faux positifs / catégorie.** Un CC MIDI seul ne prouve ni mouvement corporel, ni mapping, ni effet effectif; une fluctuation capteur ne prouve pas l'intention expressive. `AUDIO_REQUIRED / CONTEXT_REQUIRED / MIDI_PROXY`.

### Q3 — Œuvre de grande envergure : tension de transformation, espace et retour

**Analyser.** Sur une œuvre complète connue, segmenter chronologie, familles de matériaux, rappels transformés, densité, silences et paramètres de spatialisation si l'audio multicanal est disponible. Comparer les transitions lentes, les bascules par seuil et les retours transformés, avec au moins deux interprétations possibles de la forme. Ne pas convertir directement volume, densité ou mouvement spatial en degré de tension esthétique.

**Composer.** Concevoir un plan long avec quelques matériaux suffisamment spécifiques pour revenir sous transformations de timbre, rythme et position spatiale; écrire d'abord trois transitions et une fin, puis développer les régions en fonction de l'arc global. Tester une version de conclusion qui rétablit un matériau initial et une autre qui le transforme définitivement, en recueillant des écoutes comparatives.

**Faux positifs / catégorie.** Le catalogue ne prescrit **aucune durée, forme, technologie ou contrôleur spécifique**, sauf les domaines généraux annoncés; un simple pan stéréo MIDI ne démontre pas une scénographie de diffusion ni une œuvre longue. `AUDIO_REQUIRED / CONTEXT_REQUIRED / MIDI_PROXY`.

**Passerelles conceptuelles, sans identité de projets :** [MUCO-342](./MUCO-342.md) fournit les premières pièces complètes en studio, [MUCO-541](./MUCO-541.md) distingue analyse esthétique et paramètres sonores, [CM-358](../berklee/CM-358.md) vérifie l'électronique live et les transformations audibles. Les outils mentionnés par un poste d'auxiliariat ne deviennent pas des critères d'évaluation.

**Bilan :** trois protocoles autour de l'analyse sonore, du geste musical et de la grande forme. Aucun MIDI nouveau, `non_algorithmique=false` et statuts de sources conservés.
