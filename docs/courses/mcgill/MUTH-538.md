# MUTH 538 — Mathematical Models for Musical Analysis

McGill, choix complémentaire du B.Mus. Composition, inventaire 2026. **Catalogue seulement ; plan de section non obtenu.** Consultation : 10 novembre 2026.

## Sources et état de recherche

- [Notice institutionnelle 2024–2025](https://www.mcgill.ca/study/2024-2025/courses/muth-538) — éventail de thèmes possibles : séries, ensembles de classes de hauteurs, contours, similarité, réseaux transformationnels, groupes et systèmes d’intervalles, théorie néo-riemannienne, conduite des voix géométrique, gammes, tempéraments et information. Préalable historique : MUTH 350 ou équivalent.
- [Exigences Composition consultées en 2026](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) — confirme le choix ; sa description ne précise pas quels thèmes sont sélectionnés dans une section donnée.

Les recherches ciblées par code avec syllabus/outline n’ont trouvé que des notices, des calendriers historiques et des listes de programme. Aucun sujet de devoir, séance ou lecture prescrite d’une section n’a été obtenu. Les listes anciennes ne doivent pas devenir un syllabus actuel par simple reprise.

## Prochaine acquisition

Chercher un plan autorisé, les références exactes, les œuvres analysées, les notations et les travaux. Identifier les thèmes réellement retenus et ceux absents. L’objet est ici la matière universitaire de modèles musicaux ; aucune programmation ou expérimentation de modèles n’est engagée.


## Application à l'analyse et à la création — évaluation des sources et formats (12 novembre 2026)

**Cours : MUTH 538. Contribution :** potentiellement directe, mais apprentissages effectivement retenus inconnus. **Source :** [notice institutionnelle historique de Mathematical Models for Musical Analysis : liste de thèmes possibles (ensembles, transformations, tempéraments, information, etc.) et choix de section non connu en 2026](https://www.mcgill.ca/study/2024-2025/courses/muth-538). **Pas de MIDI original** dans cette première évaluation; un exemple nécessiterait une partition, un graphe, une source audio ou la preuve d'un thème effectivement enseigné.

### Apprentissage ou domaine 1 — Modèles mathématiques possibles de la musique

**Statut de preuve :** thème du catalogue ou piste conditionnelle clairement distinguée. **Catégorie :** `UNKNOWN / MIDI_DIRECT / CONTEXT_REQUIRED`.

**Procédure pour analyser de la musique :** 1. Obtenir le plan et les objets d'étude réellement retenus en 2026. 2. Si les classes de hauteurs sont enseignées, définir les transformations modulo 12 et vérifier les ensembles sur des données MIDI. 3. Si la théorie de l'information est étudiée, documenter probabilités, corpus et mesure avant de calculer une entropie. 4. Si les tempéraments sont étudiés, exiger des fréquences/accordages plutôt que des seuls numéros MIDI égaux.

**Procédure pour créer une composition :** 1. Choisir **après preuve du syllabus** un modèle défini, préciser ses paramètres puis produire une courte composition testant ses prédictions. 2. Comparer au contexte musical et relever les cas où le modèle échoue.

**Démonstration requise, risques et limites :** La liste du catalogue représente un **menu de thèmes possibles**, pas des apprentissages confirmés d'une session précise. Un MIDI de théorie néo-riemannienne créé arbitrairement serait une attribution trompeuse à MUTH 538.

### Apprentissage ou domaine 2 — Comparer un modèle formel à une œuvre réelle

**Statut de preuve :** thème du catalogue ou piste conditionnelle clairement distinguée. **Catégorie :** `CONTEXT_REQUIRED / UNKNOWN`.

**Procédure pour analyser de la musique :** 1. Une fois l'outil choisi, obtenir corpus représentatif et annotations; séparer données d'entraînement et critères de validité si des statistiques sont utilisées. 2. Mesurer les écarts entre modèle et œuvre, consigner les ambiguïtés musicales.

**Procédure pour créer une composition :** 1. Écrire des variantes musicales qui satisfont ou violent une hypothèse explicite du modèle étudié, puis tester l'intérêt expressif; ne pas réduire le verdict esthétique à une seule métrique.

**Démonstration requise, risques et limites :** `non_algorithmique=null` ne signifie pas qu'un modèle mathématique n'est pas algorithmisable; il signifie que les contenus réellement enseignés ne sont pas établis.

### Verdict

- **Apport :** potentiellement directe, mais apprentissages effectivement retenus inconnus.
- **Domaines évalués :** 2, pas une liste exhaustive des apprentissages réels.
- **Drapeau :** `non_algorithmique=null` ; une valeur `null` désigne l'absence de preuve de section, pas une absence d'algorithmique.
- **Fichier MIDI :** aucun, pour les raisons expliquées; média mieux adapté indiqué ci-dessus.
- **Manques :** corpus de section, exercices exacts et critères.

## Deuxième passe qualitative — modèles de similarité, transformations et attentes (12 novembre 2026)

**Portée du catalogue, à ne pas surinterpréter.** Les [exigences McGill pour MUTH 538](https://www.mcgill.ca/music/programs/bmus/music-composition/requirements) énumèrent des **sujets parmi lesquels une section peut choisir** : mesures de similarité, réseaux transformationnels, groupes, géométrie de conduite des voix, théorie de l'information, entre autres. **Le cours est indiqué comme non offert actuellement**, et aucune sélection effective de thèmes ou travaux 2026 n'est connue. Les trois axes sont donc des **modèles AnaMu conditionnels correspondant à des familles citées**, **pas trois acquis officiellement évalués dans une session**. Le drapeau `non_algorithmique=null` et l'absence de MIDI sont conservés.

### Q1 — Similarité motivique : définir la mesure avant de déclarer un retour

**Analyser — protocole conditionnel.** Si des mesures de similarité sont réellement retenues dans un corpus, choisir une représentation déclarée (intervalles ordonnés, contours ou rapports de durées), la normalisation pertinente (transposition oui/non, rythme augmenté oui/non) et une distance (d) explicite. Comparer plusieurs occurrences candidates et des paires non apparentées, signaler le seuil retenu et les confusions, puis vérifier la pertinence formelle des correspondances par partition et écoute. Documenter le résultat comme « ressemblance selon (d) » et non « retour voulu par l'auteur ».

**Créer et contrôler.** Composer une cellule originale de cinq attaques, une variante transposée conservant les intervalles, une variante rythmique et une cellule de contour opposé; comparer leurs distances selon deux métriques distinctes et évaluer si la hiérarchie calculée concorde avec les relations entendues.

**Faux positifs / format.** Un motif court récurrent peut coïncider par hasard; le choix de distance et de seuil dépend de la tâche et du style. Une identité statistique ne certifie pas une intention, et le catalogue ne prouve **aucune** métrique particulière enseignée. `MIDI_DIRECT / CONTEXT_REQUIRED / UNKNOWN`.

### Q2 — Réseau transformationnel : une structure de relations n'est pas une histoire causale

**Analyser — protocole conditionnel.** Si les réseaux transformationnels sont au programme, représenter les occurrences par sommets et associer aux arêtes une **opération effectivement vérifiée** sur les classes de hauteurs, intervalles ou autres objets nommés. Par exemple, relier {0,1,4} à {2,3,6} par transposition T2, en distinguant collection et ordre des notes. Construire plusieurs chemins possibles, vérifier composition des opérations et constater si les liens reproduisent les sections de l'œuvre; laisser les arêtes non justifiées absentes.

**Créer et contrôler.** Choisir trois collections originales, définir deux transformations contrôlées, construire une forme A–B–A′ dont le graphe rend explicites les relations de hauteur, puis comparer à un ordre alternatif où le même réseau est conservé mais la trajectoire perçue change.

**Faux positifs / format.** Un graphe mathématiquement correct ne prouve ni une influence ni une intention compositionnelle; les chemins transformationnels ne remplacent pas rythme, texture et contexte. `MIDI_DIRECT / MIDI_PROXY / CONTEXT_REQUIRED / UNKNOWN`.

### Q3 — Information et attente : la surprise dépend d'un modèle de contexte

**Analyser — protocole conditionnel.** **Si** l'information musicale est réellement étudiée, définir ce qui constitue un événement (intervalle suivant, cadence, retour de motif), son contexte (style, position dans la phrase, histoire locale) et la source des probabilités. Un modèle probabiliste **déclaré** peut mesurer la surprise d'un événement (e) par (-\log_2 P(e\mid c)) bits, lorsque (P(e\mid c)>0). Comparer la prédiction à des événements observés, faire une validation sur des exemples distincts des données utilisées pour fixer le modèle et garder des hypothèses alternatives. Ne jamais confondre « surprise selon un corpus » et émotion ou attente psychologique d'un auditeur donné.

**Créer et contrôler.** Définir un motif et des règles de transition explicites dans **une étude originale**; placer d'abord un retour fortement attendu, puis un événement improbable selon ce modèle en conservant une fonction musicale compréhensible. Comparer les deux versions par écoute et journal de décisions, sans prétendre qu'une valeur de bits mesure le plaisir ou la tension vécue.

**Faux positifs / format.** Sans corpus, lissage des événements rares, modèle probabiliste et auditeur/contexte adéquats, le calcul ne démontre rien; le catalogue liste « information theory » parmi **plusieurs options**. `MIDI_PROXY / CONTEXT_REQUIRED / UNKNOWN`. Pas de MIDI artificiel ni de prétention à un modèle validé.

**Passerelles conditionnelles, sans équivalences de cours :** [MUTH-151](./MUTH-151.md) fournit des objets formels à segmenter; [MUTH-528](./MUTH-528.md) illustre des niveaux d'interprétation non réductibles à des distances numériques; [MUTH-350](./MUTH-350.md) relève des transformations post-tonales; [CM-373](../berklee/CM-373.md) fournit des questions sur le retour motivique et la grande forme. Ces liens sont des **questions transversales proposées**, pas le syllabus de MUTH 538.

**Bilan :** trois protocoles mathématiques conditionnels particulièrement pertinents pour les attentes et retours, sans promotion du statut du cours ni attribution d'une session inexistante; `non_algorithmique=null` conservé.
