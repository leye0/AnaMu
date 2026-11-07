# AnaMu — Feuille de route de recherche et de développement

**Version :** 0.3 — accès et schéma GigaMIDI vérifiés sur GitHub Actions  
**Objectif :** constituer un corpus musical multimodal, identifiable et traçable, sur lequel plusieurs moteurs pourront étudier le langage musical et ses relations avec les émotions humaines.

Ce document guide le projet. Une tâche n'est « terminée » que lorsque son résultat et ses limites sont documentés et vérifiés.

## 1. Vision

AnaMu vise à étudier conjointement :

1. **La composition symbolique** : notes, intervalles, accords, séquences, rythmes, motifs, répétitions, transformations, structure et attentes.
2. **La sémantique des paroles** : thèmes, émotions exprimées, figures, tensions narratives et changements de sens.
3. **L'interprétation et le son** : voix, instruments, timbres, intensité, articulation, effets et production.
4. **La perception humaine** : annotations émotionnelles réellement produites par des personnes, avec leurs méthodes et éventuels désaccords.
5. **Le contexte** : artiste, genre, époque, version de l'enregistrement, popularité et diffusion.

L'ambition à long terme est une **grammaire musicale explicable** : découvrir des régularités génériques, calculer des attentes conditionnelles, caractériser les surprises et relier les structures observées à des phénomènes humains. Une corrélation n'est pas automatiquement une explication causale.

### Hors périmètre initial

- Entraîner un grand modèle de génération musicale.
- Télécharger et conserver toutes les chansons de toutes les bases.
- Démixer immédiatement des dizaines de milliers d'enregistrements.
- Affirmer qu'une annotation émotionnelle générée automatiquement est une vérité humaine.
- Reproduire des analyses ou extractions disponibles et réutilisables sans nécessité démontrée.

## 2. Stratégie générale

**Construire d'abord un catalogue d'identités, puis l'enrichir avec des observations indépendantes.**

Les identités ne doivent pas être confondues :

- **Œuvre** : composition musicale, éventuellement avec texte original.
- **Enregistrement** : réalisation sonore précise (studio, concert, reprise, remaster, etc.).
- **Transcription MIDI / arrangement** : représentation symbolique pouvant différer de l'enregistrement.
- **Version des paroles** : langue, modifications et éventuelle synchronisation.
- **Annotation émotionnelle** : jugement humain ou sortie de machine, à conserver séparément.
- **Observation analytique** : résultat d'un moteur, associé à une version et une configuration reproductibles.

Une même œuvre peut avoir plusieurs enregistrements, et un MIDI peut correspondre à plusieurs candidats. Ces relations sont **plusieurs-à-plusieurs** lorsque nécessaire.

## 3. Sources candidates et limites connues

| Source | Intérêt | Limites / vérifications préalables |
|---|---|---|
| [XMIDI / XMusic](https://github.com/xmusic-project/XMIDI_Dataset) | 108 023 MIDI, 11 classes d'émotions annotées par des professionnels, catégories de genre | Noms publiés selon le modèle XMIDI_Emotion_Genre_ID ; pas de titre/artiste dans ces noms. Téléchargement présenté sous forme d'une archive Google Drive : vérifier taille, droits et accès partiel. Émotions principalement au niveau du morceau. |
| [MetaMIDI](https://github.com/Metacreation-Lab/MetaMIDI-Dataset) | 436 631 MIDI ; nombreux titres/artistes et rapprochements Spotify/MusicBrainz déjà calculés | L'accès aux fichiers est soumis à une demande ; ne pas supposer les données disponibles avant autorisation. |
| [GigaMIDI](https://github.com/Metacreation-Lab/GigaMIDI-Dataset) et [Discover MIDI](https://huggingface.co/datasets/projectlosangeles/Discover-MIDI-Dataset) | Grands corpus et caractéristiques pré-calculées ; solutions ou compléments selon les données réellement accessibles | Vérifier les sous-ensembles, les champs, les licences, les coûts de transfert et les mécanismes d'accès. |
| [MusicBrainz](https://musicbrainz.org/doc/Work) | Référentiel des œuvres, enregistrements, artistes, relations et identifiants stables | Ne fournit pas l'audio complet ni nécessairement les paroles ; un identifiant d'œuvre n'identifie pas une version studio précise. |
| [LRCLIB](https://lrclib.net/docs) | Paroles en texte, parfois synchronisées par ligne ou mot | Couverture variable, correspondance à vérifier avec l'enregistrement ; examiner les droits d'usage. |
| [Musixmatch](https://github.com/musixmatch/musixmatch-sdk) | Recherche de paroles et catalogue sous licence | Conditions d'accès, de stockage et de réutilisation à vérifier. |
| [DEAM](https://cvml.unige.ch/databases/DEAM/) | 1 802 extraits/chansons avec évaluations humaines temporelles de valence et d'activation | Principalement audio ; ne pas inventer un lien MIDI. |
| [EMOPIA](https://annahung31.github.io/EMOPIA/) | 1 087 extraits de piano avec MIDI et émotions évaluées par des humains | Plus petit et centré sur le piano pop. |

**Politique émotionnelle :** les annotations humaines forment le corpus de référence. Les étiquettes automatiques peuvent servir d'hypothèses secondaires, jamais de vérité de validation non signalée.

## 4. Popularité et représentativité

La popularité est utile à deux titres :

1. **Priorisation** : favoriser initialement les œuvres connues susceptibles de posséder paroles, enregistrements et métadonnées riches.
2. **Variable de recherche** : étudier si des structures musicales sont statistiquement associées à la diffusion, à la mémorisation ou aux succès commerciaux.

Mais la popularité **n'est pas** une mesure directe de qualité, d'émotion ou de préférence universelle. La stocker comme une suite de **mesures datées**, chacune avec source et définition (par exemple un rang de palmarès ou des écoutes), et non comme un score permanent universel.

Conserver également un échantillon diversifié de morceaux peu connus. Sinon, la grammaire risquerait de modéliser surtout les biais commerciaux ou les particularités d'une époque.

## 5. Modèle de données initial

Schéma conceptuel — les champs définitifs seront précisés lors du premier prototype :

| Entité / table | Champs essentiels |
|---|---|
| works | work_id, musicbrainz_work_id, title, composers, lyricists, language |
| recordings | recording_id, work_id, musicbrainz_recording_id, isrc, artist_id, duration, year, version_type |
| midi_assets | midi_id, source, source_file_id, checksum, emotion_label_source, genre_source, storage_reference |
| midi_recording_matches | midi_id, recording_id, method, score, decision, reviewed_at, evidence |
| lyrics_versions | lyrics_id, work_id, recording_id (facultatif), language, provider, rights, sync_level |
| lyric_segments | lyrics_id, start_ms, end_ms, text_or_reference, confidence, alignment_method |
| emotion_annotations | subject_type, subject_id, time_range, label_or_dimensions, annotator_type, source, confidence |
| popularity_observations | recording_id ou work_id, source, metric, value, observed_at |
| analysis_runs | run_id, engine, version, parameters, source_checksums, execution_date |
| analysis_events | run_id, target_id, start_ms, end_ms, feature_type, value, confidence |

**Règle fondamentale :** ne pas perdre les données originales ni leur provenance lorsque des résultats normalisés ou agrégés sont ajoutés.

Pour les textes protégés, pouvoir stocker seulement les identifiants, références ou caractéristiques permises par les droits de la source.

## 6. Identité musicale : stratégie de rapprochement

On ne peut **pas** joindre directement XMIDI à MusicBrainz par le nom de fichier : les noms XMIDI ne comprennent pas le titre ni l'artiste.

Approche progressive :

1. Chercher les correspondances exactes éventuellement établissables par empreinte de fichier ou identifiant d'origine partagé.
2. Constituer un index de candidats à partir des données symboliques et des métadonnées identifiées accessibles.
3. Rechercher les candidats par des signatures de mélodie, intervalles, rythme et structure robustes aux changements de tempo et de tonalité.
4. Comparer plus finement les candidats (alignement de séquences et mesures de similitude musicale).
5. Ne confirmer automatiquement que les rapprochements dépassant des seuils **calibrés expérimentalement**.
6. Conserver les candidats ambigus, les contre-exemples et l'explication des scores pour réévaluation.

**Ne pas utiliser une simple progression d'accords comme preuve d'identité :** de nombreuses chansons partagent les mêmes progressions.

Les outils existants de rapprochement MIDI/audio (notamment les résultats MetaMIDI) doivent être réutilisés lorsque les données et droits le permettent.

### Mesures de qualité

- Couverture : MIDI identifiés / MIDI évalués.
- Précision estimée des correspondances acceptées, sur un échantillon revu manuellement.
- Ambiguïtés : plusieurs candidats plausibles / MIDI évalués.
- Cas de refus et faux positifs, notamment entre reprises et versions studio.
- Répartition des résultats selon genre, année, popularité et émotion.

**Ne pas annoncer une couverture ou une précision avant mesure.**

## 7. Étapes et critères de sortie

### P0 — Audit de faisabilité et d'accès

**Livrables :** tableau des sources accessibles, formats, volumes, restrictions, identifiants, caractéristiques déjà calculées et possibilités de téléchargement partiel.

- Inspecter l'archive XMIDI et déterminer si un sous-ensemble est accessible sans transfert massif.
- Vérifier le processus d'autorisation MetaMIDI et les données déjà publiques.
- Évaluer les alternatives exploitables immédiatement (GigaMIDI, Discover MIDI, Lakh, etc.).
- Inventorier précisément les jeux de correspondances identifiées, leurs scores et licences.

**Terminé lorsque :** les méthodes d'accès, coûts estimés et obstacles sont documentés ; aucun téléchargement de plusieurs Go ne doit être lancé implicitement.

### P1 — Expérience de rapprochement sur un échantillon

**Cible :** jusqu'à **1 000 MIDI XMIDI**, sous réserve d'un accès raisonnable. Si l'archive ne permet aucun échantillonnage, documenter le problème et convenir d'une alternative avant un téléchargement massif.

- Construire le plus petit pipeline reproductible de lecture des MIDI et de signatures.
- Chercher les correspondances exactes puis approchées dans un référentiel identifié.
- Vérifier manuellement un échantillon des résultats, y compris les cas difficiles et les refus.
- Publier les taux de couverture, de précision estimée et les erreurs représentatives.

**Terminé lorsque :** nous savons si l'identification est suffisamment fiable pour justifier une montée en charge. Une couverture élevée avec de nombreux faux positifs est un échec, pas un succès.

### P2 — Catalogue et enrichissement léger

- Normaliser les entités œuvre / enregistrement / MIDI.
- Récupérer les informations MusicBrainz avec leurs identifiants.
- Intégrer des indicateurs de popularité datés, de sources vérifiables.
- Rechercher les versions disponibles des paroles et leur niveau de synchronisation.
- Mesurer le pourcentage de chansons couvertes pour chaque type d'information.

**Terminé lorsque :** on peut interroger et exporter un catalogue dédupliqué, traçable et représentatif.

### P3 — Première grammaire symbolique

- Réutiliser les caractéristiques musicales pré-calculées pertinentes.
- Normaliser les tonalités, intervalles, rythmes et positions structurelles.
- Mesurer motifs, répétitions, suites d'accords, transitions et probabilités conditionnelles.
- Étudier les attentes, la surprise et les structures multi-échelles.
- Tester la généralisation sur des œuvres et artistes retenus hors du corpus d'exploration.
- Relier les résultats aux émotions **humaines** sans en inférer une causalité prématurée.

**Terminé lorsque :** des règles explicables sont évaluées sur des morceaux inconnus, avec échecs documentés.

### P4 — Prototype audio et paroles synchronisées

**Périmètre initial :** petit lot de chansons identifiées, accessibles pour une analyse conforme aux droits.

- Préférer des paroles déjà synchronisées au mot ; sinon à la ligne.
- Avec des paroles connues, tenter d'abord un **alignement forcé** sur la voix isolée.
- Utiliser la transcription Whisper comme recours si le texte manque, en mesurant ses erreurs sur le chant.
- Démixer temporairement avec Demucs ; la séparation piano/guitare et les effets vocaux peuvent être imparfaits.
- Extraire hauteurs vocales, contour mélodique, vibrato, intensité, articulation, timbres et indices de production.
- Aligner les événements audio avec la chronologie MIDI ; mesurer les écarts entre l'arrangement et l'enregistrement réel.

**Terminé lorsque :** qualité de synchronisation, temps de traitement, coûts et taux d'erreur sont mesurés sur un lot représentatif.

### P5 — Analyses multimodales et grammaires croisées

Étudier les relations entre :

- Grammaire de composition.
- Sémantique et narration des paroles.
- Grammaire de l'interprétation vocale et de la production sonore.
- Perception émotionnelle humaine.
- Contexte historique, genre et popularité.

Exemples de questions : tensions/résolutions, continuité entre phrases, contradictions entre texte et harmonie, effets de l'interprétation sur une même mélodie, différences historiques dans les structures récurrentes.

**Terminé lorsque :** chaque hypothèse précise ses variables, son jeu de validation, ses résultats et les explications alternatives possibles.

## 8. Qualité scientifique

- **Fuites de données** : séparer les jeux d'entraînement/exploration/test par œuvre, et si nécessaire par artiste, pas uniquement par fichier MIDI.
- **Doublons** : identifier reprises, arrangements et transpositions avant de calculer des fréquences.
- **Annotations** : distinguer « émotion exprimée/perçue » de « émotion ressentie par un auditeur ».
- **Désaccords** : conserver les jugements individuels lorsqu'ils sont disponibles, pas seulement la moyenne.
- **Biais** : documenter les genres, époques, cultures, langues et niveaux de popularité sous-représentés.
- **Généricité** : interdire les règles particulières à des titres, artistes ou fichiers individuels sans justification de portée générale.
- **Reproductibilité** : versionner les configurations, scripts, définitions de caractéristiques et rapports de validation.

## 9. Exécution, stockage et budget

- GitHub Actions pour les inventaires, téléchargements de métadonnées, signatures et statistiques de taille raisonnable.
- Déclenchement manuel des traitements volumineux, petites limites de lots, durée maximale et rapports de consommation.
- Enregistrer de préférence les **résultats compacts**, manifestes et index ; ne pas mettre les grosses archives dans Git.
- Pour l'audio, traiter temporairement les fichiers et ne garder les stems que si leur conservation est indispensable et autorisée.
- Évaluer séparément les coûts du démixage et de l'alignement de nombreux enregistrements ; ne pas supposer que des runners CPU gratuits suffiront.
- Les restrictions d'accès et les droits de reproduction/stockage/redistribution ne disparaissent pas parce que l'usage est éducatif.

## 10. Prochaine action concrète

**Démarrer P0, puis P1 uniquement si l'accès aux sources le permet.**

Liste de contrôle immédiate :

- [x] Vérifier la forme de distribution de XMIDI (ZIP Google Drive unique) et le contenu du dépôt public.
- [ ] Mesurer la taille du ZIP XMIDI et établir si un sous-ensemble est accessible sans l'archive complète.
- [x] Vérifier les restrictions MetaMIDI (Zenodo) et GigaMIDI (Hugging Face) et mesurer le rejet anonyme (HTTP 401).
- [x] Configurer le secret GitHub Actions `HUGGING_FACE_KEY`, vérifier l'accès authentifié et lire un schéma minimal GigaMIDI (HTTP 302 puis 200, 5 762 octets de réponse).
- [ ] Vérifier si le champ GigaMIDI `md5` ou une table de provenance permet de retrouver sans ambiguïté les MIDI et annotations humaines XMIDI.
- [ ] Choisir un référentiel identifié utilisable sans droit d'accès supplémentaire.
- [ ] Définir un format de manifeste minimal et une convention de scores de rapprochement.
- [ ] Créer un test reproductible sur un petit nombre de MIDI avant de viser 1 000.
- [ ] Exécuter le pilote, inspecter les faux positifs et publier les premiers chiffres.
- [ ] Décider, à partir des résultats, s'il faut étendre l'identification ou changer de stratégie.

## 11. Suivi de progression

Ce document décrit les **jalons** ; les progrès doivent être enregistrés avec des états précis :

- **À faire** : aucune preuve d'exécution.
- **En cours** : code ou expérience partiellement exécutée, avec résultat intermédiaire.
- **Bloqué** : obstacle et action requise documentés.
- **Terminé** : livrable et validation vérifiables, avec lien vers commit/rapport.

### État initial

| Phase | Statut | Preuve / observation |
|---|---|---|
| P0 — Audit | **En cours** | [Rapport de vérification](audit-p0.md) et [workflow d'audit réussi](https://github.com/leye0/AnaMu/actions/runs/42332678641) ; [sonde initiale](https://github.com/leye0/AnaMu/actions/runs/42333456588) : HTTP 401 anonyme ; [sonde authentifiée](https://github.com/leye0/AnaMu/actions/runs/42333965236) : HTTP 302 ; [schéma lu](https://github.com/leye0/AnaMu/actions/runs/42334121279) : HTTP 200, 1 ligne, champs `md5`/titre/artiste/MusicBrainz, aucune clé XMIDI explicite. Taille et extraction partielle XMIDI non établies |
| P1 — Identification | À faire | Aucun rapprochement exécuté |
| P2 — Catalogue | À faire | Aucun catalogue produit |
| P3 — Grammaire | À faire | Aucun résultat expérimental |
| P4 — Audio et paroles | À faire | Aucun pipeline exécuté |
| P5 — Multimodal | À faire | Aucun résultat expérimental |

Lorsqu'une phase progresse, mettre à jour sa **mesure de couverture**, ses **critères de sortie** et son **état**.

**Mesures du 7 novembre 2026 :** 4 exécutions P0 réussies (audit, accès anonyme, accès authentifié, schéma), 5 tests automatiques réussis, 5 sources initialement interrogées par API, un contrôle d'accès GigaMIDI anonyme puis authentifié, et une lecture viewer d'une ligne (corps de réponse de 5 762 octets). 0 archive téléchargée, 0 correspondance XMIDI/GigaMIDI exécutée. P0 reste *En cours* : absence de preuve de clé commune XMIDI/GigaMIDI et conditions d'échantillonnage XMIDI encore inconnues. Ne pas laisser éternellement le même nombre de « grands chantiers ouverts » sans indiquer leurs sous-étapes effectivement terminées.
