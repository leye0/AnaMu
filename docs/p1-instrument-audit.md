# AnaMu — P1 : audit du détail instrumental dans XMIDI

**Date de mesure :** 7 novembre 2026  
**Exécution reproductible :** [GitHub Actions 42341726010](https://github.com/leye0/AnaMu/actions/runs/42341726010) — succès ; **30 tests réussis**.  
**Code :** `scripts/audit_xmidi_instruments.py`, `tests/test_audit_xmidi_instruments.py`, `.github/workflows/p1-instrument-audit.yml`.

## Question étudiée

XMIDI comprend-il surtout des versions réduites au piano ou des arrangements
instrumentaux détaillés, notamment avec **guitare, basse et batterie** ?
Cette mesure porte sur **les notes MIDI encodées** et leur famille
instrumentale *General MIDI*, pas sur la fidélité acoustique à un disque.

## Méthode

- Index distant d'un ZIP contenant 108 024 entrées, dont 108 016 MIDI
  admissibles aux limites : 200–180 000 octets non compressés, au plus
  100 000 octets compressés, compression ZIP `stored`/`deflate`.
- **100 fichiers aléatoires** de toute la population admissible (graine
  déterministe `20261107`) : échantillon utilisé pour estimer les proportions
  générales, sans surpondérer un genre.
- **100 autres fichiers, sans doublon**, tirés parmi les genres nommés `pop`,
  `rock` ou `grunge` : échantillon ciblé complémentaire. Un a échoué par
  erreur HTTP et 99 ont été lus/analysés. Les deux strates ne doivent jamais
  être fusionnées pour produire des pourcentages de corpus.
- Pour chaque fichier : lecture de l'en-tête ZIP et du membre compressé par
  HTTP Range, décompression en mémoire avec limite, contrôle CRC32, puis
  analyse par `mido` des événements `program_change` et `note_on` de vélocité
  positive, canal et position temporelle.
- Les pistes sans notes ne comptent pas comme parties actives. Les programmes
  24–31 correspondent à la famille `guitar`, 32–39 à `bass` et le canal
  10 General MIDI (index 9) à `drums`.
- Le marqueur **trio présent** exige au moins **16 notes** dans chacune des
  familles guitare, basse, batterie. Le marqueur **trio soutenu** exige en plus
  des notes dans au moins **4 des 16** portions temporelles du morceau pour
  chaque famille ; ce seuil est exploratoire et ne garantit pas trois parties
  continuellement présentes.

## Couverture des genres dans l'archive

| Genre déclaré par XMIDI | MIDI admissibles |
|---|---:|
| rock | 26 708 |
| pop | 25 582 |
| country | 23 548 |
| jazz | 15 862 |
| classical | 12 659 |
| traditional | 3 657 |
| **Total** | **108 016** |

Les catégories `rock` et `pop` réunissent **52 290** fichiers admissibles
(environ 48,4 % de la population). La catégorie `grunge` n'existe pas
séparément dans ces étiquettes ; un artiste grunge éventuel pourrait être
classé `rock` ou `pop`. **Le nom des artistes n'est pas dans les noms XMIDI**.

## Résultats sur les fichiers effectivement analysés

| Mesure | Aléatoire, n=100 | Pop/rock ciblé, n=99 |
|---|---:|---:|
| Deux pistes ou plus contenant des notes | 100/100 (100 %) | 99/99 (100 %) |
| Trois parties actives ou plus | 91/100 (91 %) | 89/99 (89,9 %) |
| Une famille guitare avec des notes | 72/100 (72 %) | 69/99 (69,7 %) |
| Une famille basse avec des notes | 88/100 (88 %) | 87/99 (87,9 %) |
| Un canal batterie avec des notes | 87/100 (87 %) | 93/99 (93,9 %) |
| **Guitare + basse + batterie (≥16 notes chaque)** | **64/100 (64 %)** | **59/99 (59,6 %)** |
| Trio soutenu (≥4/16 portions chaque) | 64/100 (64 %) | 59/99 (59,6 %) |
| Réduction piano seule | 0/100 | 0/99 |
| Batterie seule | 0/100 | 0/99 |
| Médiane du nombre de notes | 3 267 | 3 704 |
| Durée médiane estimée | 173,3 s | 186,6 s |

Les 100 MIDI de l'échantillon aléatoire ont été analysés. Dans le groupe
ciblé, 99/100 ont été analysés ; l'échec est un **HTTPError** au téléchargement,
pas une preuve de MIDI invalide. Les pourcentages de cette colonne utilisent
99 comme dénominateur. Aucune conclusion de représentativité ne doit être
tirée du sous-échantillon ciblé en dehors de son domaine pop/rock.

L'incertitude d'échantillonnage reste notable pour n≈100. Par exemple,
64 % de trios guitare/basse/batterie dans l'échantillon aléatoire est une
**estimation**, pas la proportion exacte des 108 016 fichiers.

## Réseau, exécution et conservation

| Mesure | Résultat |
|---|---:|
| Total sélectionné | 200 MIDI |
| MIDI analysés | 199 |
| Transfert HTTP réel pour le ZIP distant | 13 752 533 octets |
| Requêtes HTTP Range | 205 |
| Temps d'exécution principal | 198,8 s |
| Limite d'octets ZIP imposée | 32 000 000 |
| Limite de requêtes ZIP imposée | 250 |
| Limite de durée du script | 345 s |
| Limite du workflow | 7 min |

Les fichiers MIDI ont été décodés **en mémoire**, sans stockage persistant,
sans publication de noms de fichiers, hashes ou notes. Aucun audio, aucune
parole et aucun modèle d'apprentissage automatique n'ont été téléchargés.
La nouvelle lecture ZIP prend normalement une requête par membre, contre
trois requêtes par membre dans l'ancien pilote.

## Interprétation scientifique et limites

1. **Résultat positif :** XMIDI comporte clairement des arrangements à
   plusieurs pistes contenant des notes, très différents d'une simple
   collection de petites boucles isolées. Les statistiques globales de
   GigaMIDI, qui rassemble de nombreuses autres sources, ne décrivent pas
   XMIDI à elles seules.
2. **Attention à la fidélité :** `guitar`, `bass` et `drums` désignent des
   programmes ou canaux MIDI utilisés et actifs. Ils ne prouvent **ni la
   présence d'un instrument enregistré en studio**, ni une transcription
   exacte de ses notes, ses techniques ou son timbre.
3. La qualité mélodique, harmonique, rythmique et structurelle doit être
   comparée ultérieurement à des enregistrements identifiés. Les seuils
   de 16 notes et 4/16 portions temporelles sont des **heuristiques
   d'audit**, pas un label humain de « qualité ».
4. La provenance des étiquettes émotionnelles reste XMIDI. Aucun artiste
   (*The Cranberries*, Beatles, Rolling Stones, etc.) n'est encore confirmé
   **dans XMIDI** par ce seul audit, car les noms d'origine ne contiennent
   pas les titres/artistes.

## Suite recommandée

Utiliser cette richesse instrumentale pour **prioriser les MIDI multistes**
au moment des rapprochements XMIDI → GigaMIDI → MusicBrainz/Spotify :

- Rechercher des titres/artistes candidats, en particulier pop/rock.
- Conserver l'étiquette émotionnelle humaine, les identifiants et le profil
  instrumental comme des dimensions séparées avec leurs provenances.
- Sur un petit lot dont l'identité est vérifiée, comparer les parties MIDI
  à l'arrangement audio réel. Ne pas confondre identité d'œuvre, identité
  d'enregistrement et fidélité des parties instrumentales.
