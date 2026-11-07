# AnaMu — Plan de validation batterie MIDI ↔ enregistrement réel

**Date :** 7 novembre 2026  
**Statut :** planifié, non exécuté  
**Rattachement :** audit instrumental P1 et premier pilote audio ciblé de P4  
**Question :** lorsqu'un MIDI XMIDI annonce une batterie, les frappes et la structure correspondent-elles réellement à celles de l'enregistrement associé ?

## 1. Pourquoi ce test

L'audit XMIDI de 200 fichiers (199 analysés) a établi la présence de plusieurs parties instrumentales : 64/100 MIDI aléatoires avaient guitare, basse et batterie actives. **Cette statistique ne mesure ni l'exactitude des notes ni la fidélité à une chanson.** Le test vise la batterie, car le temps et le type des frappes sont observables dans la forme d'onde et le MIDI.

Il faut distinguer trois objets : (a) le fichier MIDI / arrangement, (b) un **enregistrement audio précis** (studio, live, reprise, remaster), et (c) la transcription automatique tirée de cet audio. Aucun ne doit être confondu avec les deux autres.

Exemple pédagogique : « Zombie » — The Cranberries. **Ce titre n'a pas été retrouvé ni confirmé dans XMIDI.** Ne l'utiliser que si on dispose effectivement d'un MIDI de la chanson et de l'audio de la version correspondante, accessibles dans des conditions permises. Sinon, choisir un autre titre connu vérifiable.

## 2. Sources et outils éprouvés à évaluer

| Rôle | Première solution | Alternative / précaution |
|---|---|---|
| Séparer le mixage | [Demucs / htdemucs](https://github.com/facebookresearch/demucs) : extraction de drums.wav | Le stem est une **estimation**, avec fuites et artefacts possibles, pas le multitrack master |
| Transcrire les coups de batterie | [ADTOF](https://github.com/MZehren/ADTOF) : modèle publié et checkpoints, classes de percussion | [ADTOF-pytorch](https://github.com/xavriley/ADTOF-pytorch) pour faciliter l'inférence si compatible ; vérifier version et modèle |
| Deuxième détecteur indépendant | [Omnizart — drum transcription](https://github.com/Music-and-Culture-Technology-Lab/omnizart) | Tester la compatibilité avant adoption ; documentation officielle signale des contraintes ARM macOS et des problèmes d'entraînement |
| Complément si distinction de cymbales nécessaire | Séparation drum-kit spécialisée (p. ex. MDX23C DrumSep) | **Optionnel**, à n'ajouter que si elle apporte un gain mesuré ; vérifier licence/poids et fiabilité |
| Extraire les événements MIDI | Bibliothèque éprouvée **mido** ; parser tempos, canaux, notes | Réutiliser le lecteur déjà employé par l'audit P1 ; éviter une nouvelle logique MIDI parallèle |
| Aligner et évaluer | [librosa](https://librosa.org/doc/main/auto_tutorials/01-intro/05-onsets.html) pour le repérage temporel exploratoire ; [mir_eval](https://mir-eval.readthedocs.io/latest/api/onset.html) pour précision/rappel/F1 | Le pic d'énergie seul ne classe pas kick/snare/hi-hat ; l'outil ADT fournit cette distinction |

Les algorithmes et leurs checkpoints doivent être **épinglés par version/empreinte**, et les licences du code, des modèles et des fichiers audio vérifiées séparément. « Publié » ou « éprouvé » ne signifie pas « référence incontestable » ou compatible avec toute plateforme.

## 3. Préparation des paires musique–MIDI

1. **Cas pilote contrôlé** : 1 à 3 chansons connues avec audio légalement accessible et MIDI attribué, idéalement contenant de vraies pistes instrumentales et non une réduction approximative au piano.
2. Enregistrer pour chaque paire : titre, artiste, édition/version d'enregistrement, durée, source/identifiant de l'audio, source et empreinte du MIDI, provenance et méthode de correspondance, statut des droits.
3. **Ne pas déduire une paire de son seul titre.** Vérifier intro, arrangement, structure, durée et, au besoin, mélodie/harmonie. Un même morceau peut avoir plusieurs versions.
4. **Cas XMIDI** : dès qu'un fichier XMIDI est identifié avec preuve suffisante (jointure GigaMIDI/MetaMIDI/MusicBrainz ou inspection), lui appliquer le même protocole. Conserver séparément l'**étiquette émotionnelle humaine XMIDI** et le score de fidélité instrumental.
5. Inclure au moins un MIDI d'une **autre chanson**, un audio décalé et/ou une **autre version d'enregistrement** comme contrôles négatifs.

## 4. Deux voies d'analyse audio

- **Voie A, contrôle direct** : donner le mixage original au détecteur de batterie (ADTOF). Certains détecteurs sont entraînés sur de la musique mixée ; cette voie évite d'imputer automatiquement les artefacts à Demucs.
- **Voie B, séparation** : Demucs htdemucs → drums.wav → même détecteur ADTOF ; exécuter Omnizart sur l'une ou les deux voies si installation réalisable.
- Si des **vraies stems de référence** sont disponibles légalement pour un morceau de benchmark, comparer aussi leur sortie : cela distingue erreur de séparation et erreur de transcription.
- La transcription produite par ADTOF/Omnizart demeure une **estimation**, jamais une vérité terrain. Sur quelques fenêtres de 15–30 secondes (intro, couplet, refrain, fill), procéder à une inspection auditive et à une annotation humaine des frappes audibles, en notant les cas incertains.

Au premier essai, privilégier des extraits de 30–60 secondes pour limiter CPU, transferts et modèles. Pas d'entraînement de détecteur maison.

## 5. Comparateur MIDI ↔ batterie réelle

### 5.1 MIDI

- Reconstruire le temps des événements avec la piste de tempo complète et les changements de mesure utiles. Identifier les notes de percussion du canal General MIDI 10 (index 9).
- Normaliser les familles sans perdre les hauteurs d'origine : **kick** (GM 35–36), **snare** (38/40), **hi-hat** (42/44/46), **toms** (41/43/45/47/48/50), **cymbals/ride** (49/51/52/55/57/59). Prévoir les mappings non standard et les percussions particulières comme cas non interprétables ou « other ».
- Conserver les événements simultanés (kick+snare, etc.), la vélocité, l'instant, et la section musicale. Ne pas supprimer les coups faibles avant analyse.

### 5.2 Alignement

1. Mesurer décalage initial et rapport de tempo ; distinguer temps MIDI et temps audio.
2. Calculer un score avec **alignement global simple** (offset + tempo uniforme) avant les méthodes adaptatives.
3. Si nécessaire, évaluer un alignement local contraint (DTW ou méthode équivalente), **avec déformations plafonnées et pénalisées**. Sinon un algorithme trop flexible pourrait aligner n'importe quel rythme sur un autre.
4. Reporter **les deux scores** (global et adaptatif), les décalages, la carte temporelle et le pourcentage d'audio couvert. Les contrôles négatifs doivent rester mauvais après alignement.

### 5.3 Métriques

- Appariement **un-à-un** des événements par famille d'instrument avec fenêtres de tolérance **±50 ms et ±100 ms**, sans réutiliser un coup audio pour valider plusieurs coups MIDI.
- **Précision**, **rappel**, **F1**, nombre de frappes non appariées de chaque côté et erreur médiane/90e percentile des écarts temporels.
- Résultats par **kick**, **snare**, **hi-hat**, **toms**, **cymbales** et pour l'ensemble ; signaler explicitement les classes confondues par le détecteur.
- Scores **par section** (intro, couplet, refrain, pont, fills), notamment les transitions et les silences.
- Évaluer aussi la **densité rythmique**, l'alternance des instruments et la continuité de structure pour reconnaître une réduction qui ne conserve que le groove principal.
- **Ne pas** noter comme une erreur MIDI certaine un coup manqué par le détecteur : distinguer « désaccord MIDI vs transcription automatique » de « défaut MIDI confirmé à l'écoute ».

Prendre [mir_eval](https://mir-eval.readthedocs.io/latest/api/transcription.html) comme référence d'implémentation pour la logique d'appariement/évaluation temporelle. Les scores par instrument nécessitent un filtrage et une vérification de la taxonomie ; l'évaluation générique des onsets seule ne les distingue pas.

## 6. Qualité expérimentale et décision

- Préparer des **tests synthétiques** de notes simultanées, changements de tempo, décalages et frappes manquantes pour valider le comparateur indépendamment de l'IA.
- **Ne pas** fixer arbitrairement « 80 % = bon MIDI » : calibrer des seuils après examen humain de paires exactes, arrangements simplifiés et paires incorrectes.
- Vérifier les résultats de deux détecteurs, mais éviter d'interpréter leur accord comme une preuve indépendante si leurs biais/training data se recoupent.
- Séparer le jugement sur **fidélité des événements**, **identité de la chanson/version**, **richesse des instruments** et **qualité acoustique Demucs**.
- Après le pilote, étendre prudemment à **10–20 pièces identifiées**, avec échantillons rock/pop et quelques genres contrastés. Rapporter incertitude, échecs, biais et temps/coût.
- Conserver le F1 par classe, les désaccords illustratifs et un lien vers preuve d'identité ; ne déclarer la fiabilité généralisable qu'après validation sur d'autres œuvres/artistes.

## 7. Artefacts, coûts et droits

- Rapport compact (JSON/Markdown) : identifiants de paire, méthodes et versions, données de synchronisation, métriques par instrument/section, erreurs notables, avis humain, coût et statut « plausible / discordant / indéterminé ».
- Si une visualisation est produite : chronologie comparative MIDI/audio avec marqueurs de frappes ; elle ne doit pas redistribuer des extraits audio protégés.
- **Aucun audio, stem, transcription complète ni parole dans Git.** Traiter les fichiers autorisés dans un espace temporaire ; ne conserver que les résultats et références permis par les droits.
- Exécution volontaire et plafonnée. **Ne pas lancer Demucs sur des heures d'audio ou en CI par défaut.** Mesurer un seul extrait et une seule configuration avant de budgéter GitHub Actions ; stopper si dépendances/modèles trop volumineux.

## 8. Checklist et critères de sortie

- [ ] Choisir 1–3 paires identifiées, avec audio disponible et statut de droits explicite.
- [ ] Établir les versions et licences opérationnelles de Demucs, ADTOF et d'au moins un détecteur de comparaison.
- [ ] Tester la transcription de batterie sur le mix original, puis sur drums.wav.
- [ ] Normaliser les événements MIDI GM et tester le comparateur sur des fixtures contrôlées.
- [ ] Implémenter alignement global + (si justifié) alignement contraint, mesurer les faux positifs des contrôles négatifs.
- [ ] Vérifier manuellement trois types d'extraits (groove régulier, fill, changement de section) et indiquer les faux négatifs du modèle.
- [ ] Publier un rapport reproductible avec F1/erreurs par classe et les limites de l'expérience.
- [ ] Seulement après validation, répéter sur des MIDI **réellement retrouvés dans XMIDI** et documenter le lien avec l'émotion humaine.

**Terminé lorsque :** au moins une paire vraie et un contrôle négatif ont été comparés, qu'un humain a vérifié les événements problématiques, et que les chiffres distinguent erreurs de correspondance, erreurs du MIDI, erreurs de transcription et artefacts Demucs. **Aucune analyse audio n'a été exécutée au moment de la rédaction de ce plan.**
