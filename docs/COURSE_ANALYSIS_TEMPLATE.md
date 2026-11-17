# AnaMu — gabarit d'application d'un cours à l'analyse et à la composition musicale

**Convention obligatoire à partir du 11 novembre 2026.** Appliquer ce gabarit **dans la fiche existante du cours** `docs/courses/<établissement>/<CODE>.md`, sous le titre « Application à l'analyse et à la création ». Ne pas créer une seconde fiche de cours, un nouveau journal de recherche ou un fichier MIDI factice. Un exemple MIDI original se range dans `docs/courses/<établissement>/<CODE>/exemple.mid`, à côté de la fiche logique du cours. Les huit placeholders de choix Berklee ne sont pas huit cours individuels.

## 0. Périmètre et provenance

- **Code exact / intitulé / édition :** …
- **Source authentique du cours :** URL ou référence locale; préciser `notice officielle`, `examen de niveau`, `plan de section` ou `document connexe`.
- **Importance musicale :** `directe`, `indirecte`, `aucune démontrée`, `non déterminable`. Définir **pourquoi** cela peut améliorer une analyse, une création, un arrangement ou la compréhension de traditions musicales précises. Ne pas inventer la « gamme nationale » ou le « style national » d'un peuple.
- **Statut de l'évaluation :** `analysé_sur_contenu_attesté`, `partiel_faute_de_matière`, `non_algorithmique`, `non_evaluable_placeholder`.
- **Garde-fou :** le statut académique `topic_outline.state` et celui de la recherche publique ne changent pas quand on construit un exemple pédagogique original.

## 1. Pour **chaque apprentissage attesté** (répéter, sans gonfler artificiellement)

### Apprentissage [ID] : [technique, pratique ou fait culturel précis]

**Preuve du cours.** Nommer le contenu **explicitement attribué au code** dans sa notice, son épreuve ou son syllabus (avec type de preuve, année, URL). Un chapitre externe peut expliquer le mécanisme, mais ne prouve pas qu'il fait partie de ce cours.

**Analyse de musique existante — procédure textuelle.**
1. Entrées requises : MIDI (notes, hauteurs, attaques, durées, instruments, métrique, tempo, vélocités, contrôleurs), éventuellement audio, partition, paroles ou métadonnées externes. Décrire chaque source nécessaire.
2. Opérations dans l'ordre : normaliser la métrique et les temps, regrouper les voix et fenêtres, définir un ensemble de candidats, mesurer les conditions qui distinguent le motif du bruit.
3. Résultat attendu : nommer ce qui est détecté, son emplacement, sa fonction hypothétique et la preuve vérifiable; proposer des hypothèses concurrentes.
4. Faux positifs et limites : ce que le seul MIDI n'apprend PAS (timbre réel, spectre, nationalité d'une mélodie, intention d'auteur, effet clinique, apprentissage individuel).

**Créer une composition qui emploie ce savoir — procédure textuelle.**
1. Choisir une fonction musicale (préparer une cadence, prolonger une phrase, créer tension ou couleur, etc.) et ses contraintes.
2. Construire ou modifier les notes/voix/rythmes/contrôleurs progressivement en respectant le style déclaré.
3. Réécouter ou évaluer la progression; prévoir une variante et des critères de réussite **spécifiques à la fonction**, pas seulement au pattern.

**Exemples MIDI.** Lien vers un **vrai fichier Standard MIDI File**, au moins deux mesures quand pertinent. Distinguer `exemple de démonstration généré pour AnaMu` de `exercice historique du cours`. Indiquer exactement quelles mesures montrent l'apprentissage et quel événement l'illustre. Ne pas fournir un fichier MIDI lorsque le phénomène ne peut pas être représenté honnêtement dans ce format; expliquer le format requis.

**Contrôle musical d’un exemple original.** Le MIDI et le MP3 peuvent être corrects comme fichiers et néanmoins manquer le résultat musical souhaité. Pour un atelier **tonal** dont la variable à comparer est rythmique, conserver le parcours harmonique entre variantes, relever les accords qui sonnent réellement sous les nouvelles attaques, puis vérifier les notes et leur durée **contre l’accord actif**, pas seulement contre la gamme globale. Inspecter aussi les verticales formées par les autres voix et les résonances possibles du rendu. Si une note grave, un signal de percussion accordée ou une note commune se trouve sous un autre accord après déplacement, requalifier ou réécrire l’accompagnement avant de prétendre isoler le rythme. Les [observations sur une version antérieure de « Trois mesures ou quatre »](courses/berklee-online/OCOMP-485.md#trois-mesures-ou-quatre) en donnent un cas concret. Pour les procédés impliquant volontairement dissonance, bitonalité, polymodalité ou absence de centre, annoncer cette intention et les critères propres au style au lieu de forcer une triade.

**Contrôle de fonction harmonique, sans faux positif.** Pour une analyse d'accords, séparer cinq propriétés avant de conclure : **ensemble de classes de hauteurs**, **orthographe écrite**, **basse et renversement**, **conduite des voix jusqu'à la résolution**, puis **fonction de phrase et tonalité établie**. Les notes identiques peuvent recevoir plusieurs graphies ou fonctions (sixte allemande/V7, septième totalement diminuée, plusieurs emplois du 6/4); une substitution tritonique conserve parfois seulement les notes-guides, **pas l'accord entier**; une dominante à résolution déceptive n'est pas automatiquement non fonctionnelle. Si seule une liste de hauteurs MIDI est disponible, conserver des **hypothèses documentées** plutôt que fabriquer enharmonies, cadences ou modulations. [Tableau de distinctions et renvois aux cours](knowledge-base.md#une-même-sonorité-ne-décide-ni-de-sa-fonction-ni-de-sa-destination--17-novembre-2026). Ce contrôle n'est ni un moteur ni une levée de phase.


**Retards, appoggiatures et notes étrangères : vérifier l'histoire des attaques.** Dans les styles où la distinction est pertinente, une **suspension** retient une note consonante préparée avant qu'un autre événement ne la rende dissonante; une **appoggiature classique** est plutôt nouvellement attaquée, généralement **abordée par saut, accentuée**, puis résolue conjointement. Un accord éphémère de 6/4 n'est pas une preuve de l'une ou l'autre technique sans voix et contexte. Les cadences Renaissance peuvent exiger la **quatrième phase de perfection** au-delà de la résolution de la dissonance. Toujours préciser **tradition, voix, état initial, attaque, préparation, résolution et frontière de phrase**. [Synthèse et contre-cas des trois cours](knowledge-base.md#retard-appoggiature-et-perfection--la-dissonance-a-une-histoire--17-novembre-2026). Aucune de ces distinctions ne certifie l'effet audible d'un export MIDI sans prise identifiée.

**Ne pas confondre les types de validation.** Une lecture du MIDI établit les hauteurs et temps **notés**. L’inspection du MP3 établit les propriétés **mesurables** du rendu (durée, saturation, niveau, attaque, etc.). Aucune des deux ne remplace une écoute humaine pour juger la cohérence, la lisibilité d’une voix ou le plaisir musical. Si personne n’a écouté le résultat, le dire explicitement dans la fiche et demander un retour sur la fenêtre pertinente, sans annoncer que le morceau « sonne juste ».

**Accès au son.** Quand un atelier comporte un rendu audio, placer à côté de l’explication un lien vers le **fichier MP3 réel**, lisible dans un lecteur standard, et un lien distinct vers le MIDI. Le lien de documentation ou celui d’une page GitHub n’est pas un substitut au MP3. Donner les temps locaux de la comparaison et, pour plusieurs versions dans un même fichier, leur heure absolue. Cela permet de juger les différences au bon endroit, notamment sur téléphone.

**Applicabilité algorithmique (par apprentissage).**
- `MIDI_DIRECT` : paramètres explicitables depuis les événements MIDI (ex. pitch classes, onsets, mètres, canaux), avec incertitudes.
- `MIDI_PROXY` : MIDI fournit des **indices**, mais pas le phénomène complet (ex. instrumentation réelle, forme expressive).
- `AUDIO_REQUIRED` : spectre, enveloppe, écoute, mixage ou timbre ne sont pas observables depuis les seuls événements MIDI.
- `CONTEXT_REQUIRED` : origine/tradition, récit culturel, sens historique, perception d'un public ou intentions demandent d'autres documents et des humains.
- `NOT_MUSIC_ALGORITHM` : compétences professionnelles, cliniques, civiques, médiation sociale, par exemple, **non mesurables par un algorithme d'analyse de musique**. Ne signifie pas « aucun algorithme informatique possible ».
- `UNKNOWN` : objectifs spécifiques insuffisamment attestés pour conclure.
- **Un cours peut combiner plusieurs catégories.** Le drapeau `non_algorithmique` du cours vaut `true` seulement lorsqu'**aucune compétence attestée du cours ne se traduit de façon pertinente en algorithme d'analyse/création de musique**. Indiquer la raison et le degré de preuve.

## 2. Verdict du cours

| Champ | Valeur |
|---|---|
| Apport analyse/création | oui / indirect / non / indéterminé |
| Apprentissages traités | N / nombre exact connu, sinon N attestés, non exhaustif |
| Algorithmique | MIDI_DIRECT / MIDI_PROXY / AUDIO_REQUIRED / CONTEXT_REQUIRED / NOT_MUSIC_ALGORITHM / UNKNOWN |
| `non_algorithmique` | true / false / null (inconnu) |
| Couverture de cette analyse | détaillée sur sujets attestés / partielle, pas de syllabus / non applicable |
| Exemples créés | chemins des fichiers MIDI valides, ou motif d'absence |
| Lacunes bloquantes | matière exacte non publique, format audio, choix de section, expertise humaine |

**Interdits :** prétendre qu'un exemple MIDI original était une consigne universitaire, déduire une technique de son seul titre, identifier une culture depuis la seule gamme, déduire un effet thérapeutique du MIDI, ou annoncer une génération musicale « experte » à partir d'un motif de démonstration. Une évaluation limitée est préférable à un faux positif.

**Ordre d'exécution :** (1) audit des 386 entrées en distinguant les 8 placeholders; (2) rédaction détaillée d'après les fiches documentées; (3) génération MIDI uniquement pour les apprentissages réellement représentables; (4) drapeau pour les non-algorithmiques; (5) contrôle manuel des fichiers et de la provenance. Les tests logiciels et le développement du moteur ne font pas partie de ce travail documentaire.
