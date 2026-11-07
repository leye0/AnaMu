# AnaMu — P1 : première correspondance XMIDI ↔ GigaMIDI par MD5

**Date :** 7 novembre 2026  
**Statut :** première correspondance exacte **confirmée** ; taux de couverture et identité discographique encore inconnus.  
**Preuve :** [GitHub Actions — exécution 42336949364](https://github.com/leye0/AnaMu/actions/runs/42336949364) (job réussi, 24 tests unitaires).

## Résultat vérifié

Un même contenu MIDI existe dans les deux corpus : son MD5 calculé depuis les
octets du fichier XMIDI est égal à la valeur `md5` d'une ligne GigaMIDI.
Cette égalité est une preuve de correspondance **binaire** pour cet élément ;
elle n'établit pas encore le nom de la composition, de l'interprète ou de
l'enregistrement audio précis.

| Mesure | Résultat |
|---|---:|
| Fichiers MIDI éligibles dans le ZIP XMIDI | 108 016 |
| Échantillon aléatoire déterministe (graine `20261107`) | 100 |
| En-têtes MIDI valides et MD5 distincts | 100 / 100 |
| Taille totale du ZIP distant | 449 632 771 octets |
| Octets HTTP reçus pour l'index ZIP et les 100 MIDI | 13 328 176 |
| Requêtes HTTP Range adressées au ZIP | 305 |
| Partition GigaMIDI interrogée | `v2.0.0/validation/00001.parquet` |
| Lignes / groupes dans cette partition | 106 810 / 1 069 |
| Groupes parcourus **avant arrêt au premier match** | 52 |
| MD5 GigaMIDI examinés | 5 200 |
| Lectures logiques Parquet | 5 657 337 octets |
| Correspondance exacte prouvée | 1 |

L'élément reconnu est l'échantillon XMIDI d'indice `32`, étiqueté
**émotion humaine `quiet`**, **genre `traditional`**. Il est localisé dans
le groupe de lignes Parquet `51`, à la position `25` au sein du groupe.
Les champs textuels éventuellement présents à cet emplacement n'ont fourni
aucun titre ou artiste exploitable (`text_metadata: {}`). Aucun identifiant
MusicBrainz de cette correspondance n'est donc confirmé.

**Ce que ce résultat ne démontre pas :**

- Ni que les 100 fichiers XMIDI échantillonnés sont tous présents dans GigaMIDI.
- Ni qu'un seul sur 100 serait retrouvé dans le corpus complet : le balayage
  s'est interrompu dès la première découverte et ne portait que sur **une**
  partition GigaMIDI.
- Ni que cette transcription MIDI correspond à un enregistrement commercial
  particulier. Une identité binaire MIDI et une identité d'enregistrement
  sont deux niveaux distincts.
- Ni que les étiquettes XMIDI ont été préservées dans le schéma GigaMIDI :
  elles ont été relues indépendamment à partir du nom d'origine XMIDI.

## Protocole et protections

1. Ouvrir le ZIP XMIDI distant par requêtes HTTP `Range`, lire uniquement son
   index central et les 100 fichiers sélectionnés (taille individuelle
   décompressée au plus 180 Ko, taille compressée au plus 100 Ko).
2. Vérifier l'en-tête `MThd`, calculer en mémoire l'empreinte MD5, conserver
   séparément les étiquettes humaines inscrites dans le nom d'origine.
3. Ouvrir la partition Parquet GigaMIDI avec le secret GitHub Actions
   `HUGGING_FACE_KEY`. Lire **exclusivement la colonne `md5`** de chaque
   groupe de lignes, à l'aide de PyArrow et de plages distantes.
4. Arrêter la lecture au premier MD5 identique, puis essayer de consulter
   seulement quelques colonnes textuelles optionnelles.
5. Afficher uniquement des statistiques et la position relative du résultat ;
   ne jamais publier de MD5 complet, nom de fichier, contenu MIDI, URL signée
   ou secret.

Limites codées : 30 Mo de transferts ZIP, 340 requêtes ZIP, 24 Mo de
**lectures logiques** Parquet, 350 secondes pour le script et 8 minutes pour
le workflow. Le trafic HTTP réel de Parquet peut dépasser les lectures
logiques à cause des blocs lus en avance : le chiffre Parquet ci-dessus
**n'est donc pas** une mesure exacte des octets réseau.

**Coût de calcul :** le traitement principal a duré environ **5 min 28 s**
(04:06:29 à 04:11:57 UTC) ; le délai des nombreux accès `Range` doit être
optimisé avant un lot plus grand. Le workflow GitHub Actions ne garantit pas
que ces minutes soient sans frais selon le forfait et les quotas du dépôt.

## Décisions et suite

- **Acquis :** une jointure exacte et réplicable existe au moins pour une
  partie des données XMIDI intégrées à GigaMIDI. La stratégie MD5 mérite
  d'être conservée avant toute reconnaissance approximative.
- **Non acquis :** la couverture de la jointure dans les genres pop, rock,
  grunge ou dans les chansons célèbres ; les données de titres, artistes et
  ID MusicBrainz de ces éléments ; le taux global de couverture.
- **Prochain pilote :** optimiser les lectures HTTP et constituer un petit
  index de MD5 issu de colonnes Parquet, sans télécharger la colonne MIDI.
  Étudier explicitement la disponibilité des métadonnées d'identification
  des morceaux correspondants avant de choisir une méthode par signature
  symbolique pour les cas restants.
- **Pas de démixage, d'audio ni de paroles à ce stade.** Les annotations
  émotionnelles humaines gardent leur provenance XMIDI et ne doivent pas
  être présentées comme produites par GigaMIDI.

## Code reproductible

- `scripts/pilot_exact_join.py`
- `scripts/pilot_xmidi_gigamidi.py` (lecteur ZIP distant)
- `scripts/probe_hf_parquet_columns.py` (lecture Parquet plafonnée)
- `tests/test_pilot_exact_join.py`
- `.github/workflows/p1-exact-join.yml`

La licence et les conditions d'accès de chaque source s'appliquent également
aux usages éducatifs. Les contenus musicaux et paroles ne sont pas redistribués
dans ce pilote.
