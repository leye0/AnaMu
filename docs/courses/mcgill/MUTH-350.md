# MUTH 350 — Theory and Analysis 5

B. Mus. Composition McGill, édition 2026. Cours obligatoire. Sources publiques consultées le 10 novembre 2026.

## Sources et matière accessible

- Description du classement supérieur en analyse post-tonale. Analyse des classes de hauteurs, des séries et des relations motiviques avec prise en compte du rythme, du registre, de la texture et du timbre. Chapitres 1, 3, 7 et 10 de Roig-Francolí proposés pour la préparation [Consulter la source](https://www.mcgill.ca/music/files/music/composition_placement_descriptions1617.pdf).
- Exigences institutionnelles, entrée MUTH 350 ou options recommandées [Consulter la source](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements).

## Activités de la section H27

L’[affichage Schulich, p. 12](https://www.mcgill.ca/music/files/music/winter_2027_-_musicresearch_-_detailed_job_posting.pdf#page=12) annonce pour la section de Christoph Neidhöfer des cours magistraux, des sections dirigées, des devoirs, des projets finaux et des examens. Les [exigences de Composition](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) indiquent que l’écriture et l’analyse portent sur l’organisation des hauteurs, du rythme et du timbre dans les répertoires des XXe et XXIe siècles.

## Lacunes et reprise

Identifier le thème de la section et vérifier le plan. L’examen supérieur n’attribue pas son exercice au cours.


## Application à l'analyse et à la création — étude sourcée (11 novembre 2026)

**Cours :** MUTH 350. **Pertinence musicale :** directe. **Preuve :** [exigences McGill sur hauteurs, rythme et timbre des musiques XXe et XXIe siècles; diagnostics de cycles supérieurs cités séparément](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements). Les supports comparatifs et examens d'autres niveaux ne sont pas présentés comme cours exact. [**MIDI original à écouter**](./MUTH-350/exemple.mid), non tiré de l'établissement.

### Apprentissage 1 — Cellules post-tonales de classes de hauteurs et transposition

**Preuve :** famille thématique attestée par les sources propres au cours; détails de section inconnus. **Catégorie :** `MIDI_DIRECT`.

**Analyser une pièce existante :** 1. Extraire les triples attaques des mesures 1–3. 2. Normaliser les classes de hauteurs modulo 12 par soustraction de la première. 3. Obtenir chaque fois {0,1,4}, depuis do–do♯–mi, ré–mi♭–fa♯, mi–fa–sol♯. 4. Démontrer les transformations T0, T2 et T4 sans imposer une tonalité fonctionnelle.

**Écrire une composition :** 1. Choisir une cellule [0,1,4] et une durée propre. 2. Transposer chaque répétition de +2 demi-tons. 3. Changer les registres ou les durées en conservant les intervalles. 4. Évaluer la reconnaissance de la parenté motivique.

**Exemple et limites :** Mesures 1–3 : mêmes classes d'intervalles sous transposition, étude originale; ce n'est pas une analyse de The Cage de Charles Ives.

### Apprentissage 2 — Rythme, registre et texture comme paramètres analytiques

**Preuve :** famille thématique attestée par les sources propres au cours; détails de section inconnus. **Catégorie :** `MIDI_DIRECT / MIDI_PROXY / AUDIO_REQUIRED`.

**Analyser une pièce existante :** 1. Mesurer les intervalles interattaques (0, 1,5 et 3 noires relatives) de chaque cellule. 2. Suivre les déplacements de registre de la mélodie. 3. Relever le soutien de basse, son nombre de notes actives et les changements de densité. 4. Pour le timbre réel, analyser l'audio et la partition plutôt que le simple programme General MIDI.

**Écrire une composition :** 1. Garder le motif de hauteurs et modifier rythme, registre ou registre d'instrument entre sections. 2. Introduire un soutien tenu ou fragmenté. 3. Contrôler la cohérence et la différence perceptuelle à l'écoute.

**Exemple et limites :** Le fichier décrit des notes, événements et programmes instrumentaux MIDI; **il ne contient pas la couleur spectrale de l'œuvre**.

### Apprentissage 3 — Inversion : ne pas attribuer un procédé non prouvé

**Preuve :** famille thématique attestée par les sources propres au cours; détails de section inconnus. **Catégorie :** `MIDI_DIRECT / CONTEXT_REQUIRED`.

**Analyser une pièce existante :** 1. Formaliser I_n(x)=n−x (mod 12), puis chercher les cellules réellement inversées. 2. Ne pas confondre un simple contour descendant avec l'inversion exacte des intervalles.

**Écrire une composition :** 1. Produire une inversion contrôlée comme seconde section puis mesurer la relation formelle avec le motif initial.

**Exemple et limites :** La quatrième mesure est une variante de contour, **pas une inversion démontrée**. La source du cours n'attribue pas une technique précise d'inversion à une évaluation de section.

### Verdict du cours

- **Apport :** analyse et composition musicales directes.
- **Familles étudiées :** 3 dans cette passe; pas un syllabus exhaustif.
- **Drapeau :** `non_algorithmique=false`.
- **Exemple MIDI :** [étude originale](./MUTH-350/exemple.mid) ; seules les observations explicitement décrites ci-dessus sont revendiquées.
- **Reste à documenter :** corpus, méthodes et évaluations véritables de la section; aucune promotion de `topic_outline.state`.

## Deuxième passe qualitative — analyse post-tonale multi-paramètres (12 novembre 2026)

**Source propre au code :** [McGill MUTH 350, Theory and Analysis 5](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) : organisations des **hauteurs, rythmes et timbres** des XXe et XXIe siècles, analyse et interprétation de techniques/esthétiques du répertoire. Le diagnostic de cycles supérieurs mentionné ci-dessus et les références préparatoires à Roig-Francolí ne sont **pas le syllabus de la section**; aucun système sériel particulier ne doit être attribué au professeur. Les trois outils sont des protocoles **AnaMu**. L'[exemple MIDI original](./MUTH-350/exemple.mid) démontre quelques transpositions de classes de hauteurs et rythmes, pas la couleur acoustique d'une œuvre.

### Q1 — Classes de hauteurs : relation mathématique versus fonction musicale

**Analyser.** Extraire les classes modulo douze des motifs notés ou MIDI et comparer les occurrences suffisamment longues. Pour la collection {0,1,4}, vérifier sa transposition `T2={2,3,6}`; pour une inversion candidate, calculer `I0(x)=−x mod 12`, donc `I0({0,1,4})={0,11,8}`, puis contrôler si la suite *ordonnée*, les durées et le registre de la pièce soutiennent cette lecture. Distinguer équivalence de collections et reconnaissance perceptive du même matériau.

**Créer et contrôler.** Composer une cellule originale [0,1,4], la transposer puis l'inverser avec un rythme reconnaissable; présenter les trois versions dans des registres contrastés et annoter explicitement les transformations. Écouter lesquelles demeurent identifiables.

**Faux positifs / catégorie.** Une similarité de pitch-class set ne prouve ni une série dodécaphonique ni l'intention de l'auteur; la mesure 4 du MIDI joint n'est **pas une inversion attestée**. `MIDI_DIRECT / CONTEXT_REQUIRED / AUDIO_REQUIRED`.

### Q2 — Rythme et registre : préserver les invariants tout en changeant la forme perçue

**Analyser.** Séparer événements de hauteurs, intervalles entre attaques, durées, silences et étendues de registre. Chercher, sur deux régions, un motif intervallique conservé mais déplacé en tempo interne ou densité; comparer cette hypothèse à celle d'un nouveau matériau. Examiner comment les sauts de registre et l'agencement des voix transforment la segmentation formelle sans imposer une grammaire tonale.

**Créer et contrôler.** Garder la même cellule de classes mais l'exposer d'abord par attaques espacées, ensuite par figures serrées et registre élargi; préserver un point de repère perceptible. Vérifier mathématiquement les hauteurs et rythmes, puis écouter le changement de caractère.

**Faux positifs / catégorie.** Plus de notes par seconde ne prouvent pas une transformation motivique, et les données de registre ne décrivent pas la fusion acoustique. `MIDI_DIRECT / MIDI_PROXY / AUDIO_REQUIRED`.

### Q3 — Timbre, texture et esthétique : ne pas déduire le son des programmes MIDI

**Analyser.** Aligner partition, audio et descriptions de dispositif. Mesurer attaques, enveloppes, régions spectrales, densité de couches et relais entre instruments; identifier ce qui varie indépendamment de la hauteur. Proposer une lecture de la forme par changements de timbre et de texture, puis l'opposer à une lecture par cellules de hauteurs. Justifier toute attribution esthétique par sources du répertoire, pas par une simple sonorité de synthèse.

**Créer et contrôler.** Composer deux versions du même matériau de notes : l'une redistribuée entre sources contrastées, l'autre enrichie de couches acoustiques et de silences structurants. Comparer les trajectoires timbrales à l'écoute avec des enregistrements réels ou rendus dont les paramètres sont documentés.

**Faux positifs / catégorie.** Un changement de programme General MIDI n'est ni une preuve de spectralisme ni de texture historique; la fidélité demande des sources sonores et le contexte d'œuvre. `AUDIO_REQUIRED / MIDI_PROXY / CONTEXT_REQUIRED`.

**Passerelles conceptuelles, sans fusion d'enseignements :** [MUTH-251](./MUTH-251.md) distingue chromatisme tonal et symétrie, [CP-350](../berklee/CP-350.md) compare les organisations contrapuntiques modernes, [CM-312](../berklee/CM-312.md) traite des objets sonores exigeant audio, et [CM-441](../berklee/CM-441.md) permet de comparer répartition orchestrale et rôle de la texture. Ces liens ne documentent **aucun cours commun**.

**Bilan :** trois protocoles qui séparent la preuve mathématique, les paramètres de partition et l'écoute/contextualisation. Pas de nouveau MIDI, pas de modification du drapeau `non_algorithmique=false`.
