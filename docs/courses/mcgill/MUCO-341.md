# MUCO 341 — Digital Studio Composition 1

Sources publiques consultées le 10 novembre 2026.

## Cours recensé

Obligatoire, Composition 2026. Études électroacoustiques courtes avec MIDI, enregistrement et traitement du signal. Écoute critique d’œuvres électroniques. [Description institutionnelle](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements).

## Support parallèle consultable

MIT 21M.361, printemps 2008, module 1. Les travaux portent sur la prise de son, la technique de studio et la progression d’un schéma de composition vers une pièce. Le module 4 propose des travaux gradués de synthèse et d’interaction dans Max/MSP. [Support et contenu](https://ocw.mit.edu/courses/21m-361-composing-with-computers-i-electronic-music-composition-spring-2008/pages/assignments/).

## Lacunes

Ce support externe documente les sujets indiqués dans la fiche, avec sa propre progression. Les lectures prescrites, consignes, exemples et critères du cours recensé restent à obtenir auprès de l’établissement.


## Application à l'analyse et à la création — apprentissages sourcés (11 novembre 2026)

**Cours : MUCO 341. Apport :** direct à l'analyse et à la création. **Preuve :** [exigences institutionnelles du programme McGill](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements), qui annoncent les compétences sans publier leurs travaux détaillés de section. [**Vrai MIDI original dans le dossier**](./MUCO-341/exemple.mid), distinct d'un exercice scolaire réel.

### Apprentissage 1 — Séquençage MIDI et paramètres de contrôle

**Attestation :** thème nommé dans la description institutionnelle du cours. **Classification :** `MIDI_DIRECT / MIDI_PROXY`.

**Procédure pour détecter dans une musique :** 1. Analyser les Note On/Off et les changements de programme sur deux canaux. 2. Lire les événements Control Change 74 de la partie synthétique, avec leur date et valeur de 0 à 127. 3. Mesurer la relation entre rampes de contrôle et attaques des notes. 4. Ne pas attribuer un timbre ou un effet précis à un CC si le synthétiseur n'a pas de mapping connu.

**Procédure de composition :** 1. Séquencer un bourdon synthétique sur plusieurs mesures et une courte mélodie. 2. Programmer une courbe CC74 à plusieurs points. 3. Dans un moteur sonore connu, mapper le contrôleur à un paramètre, puis écouter sa courbe. 4. Exporter MIDI + audio de référence si la reproductibilité du timbre compte.

**Exemple MIDI, mesure et limites :** Le MIDI original contient notes et CC74, pas de patch ni de preuve de variation de filtre audible. Les contrôleurs ne se transforment pas automatiquement en spectre.

### Apprentissage 2 — Enregistrement et traitement du signal

**Attestation :** thème nommé dans la description institutionnelle du cours. **Classification :** `AUDIO_REQUIRED / MIDI_PROXY`.

**Procédure pour détecter dans une musique :** 1. Pour un enregistrement réel, mesurer niveau, spectre, durée, artefacts et traitement appliqué. 2. Inspecter la chaîne d'effets, paramètres et comparaison avant/après si disponibles. 3. Ne pas confondre les notes d'un séquenceur et un signal enregistré.

**Procédure de composition :** 1. Capturer du son brut, l'éditer et le traiter. 2. Réinjecter éventuellement des repères MIDI synchronisés au montage. 3. Écouter la pièce finale et archiver les paramètres de traitement.

**Exemple MIDI, mesure et limites :** **Le fichier MIDI ne démontre pas l'enregistrement ni les traitements**; une vraie étude de ce volet exige au moins deux fichiers audio comparables.

### Apprentissage 3 — Écoute critique d'œuvres électroniques

**Attestation :** thème nommé dans la description institutionnelle du cours. **Classification :** `AUDIO_REQUIRED / CONTEXT_REQUIRED`.

**Procédure pour détecter dans une musique :** 1. Analyser l'organisation des sons dans un enregistrement (textures, entrées, transitions). 2. Consigner les hypothèses esthétiques et les confronter aux œuvres effectivement indiquées par la section. 3. Éviter de prétendre extraire des intentions d'un MIDI.

**Procédure de composition :** 1. Comparer sa courte pièce électronique à des références étudiées, avec citations de styles ou techniques correctement attribuées. 2. Réviser équilibre, développement et continuité.

**Exemple MIDI, mesure et limites :** L'exemple synthétique de notes ne remplace pas un corpus d'écoute critique; les œuvres de la section restent inconnues.

### Verdict du cours

- **Pertinence :** oui, directe.
- **Familles de matière traitées :** 3; premier passage sans promesse de couvrir chaque devoir, œuvre et sous-technique.
- **Drapeau :** `non_algorithmique=false` (au moins une compétence traduisible en méthode de détection/composition).
- **Exemple :** [MIDI original](./MUCO-341/exemple.mid), non attribué à McGill.
- **Données manquantes :** plan de section, partitions et évaluations réelles, sans changement du statut académique du cours.
