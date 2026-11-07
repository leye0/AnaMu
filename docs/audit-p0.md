# AnaMu — Audit P0 : accès aux corpus et réutilisation des analyses

**Dernière vérification :** 7 novembre 2026.  
**État :** en cours — premier inventaire exécuté, accès aux données GigaMIDI non encore authentifié.  
**Priorité scientifique :** les **émotions humaines de XMIDI** restent la référence ; GigaMIDI est un candidat pour retrouver les identités et réutiliser les caractéristiques calculées.

## Preuves d'exécution

Deux workflows avec des plafonds respectifs de cinq et trois minutes ont été créés. Leur durée réelle était de quelques secondes :

1. [P0 - audit sources, exécution réussie](https://github.com/leye0/AnaMu/actions/runs/42332678641), tests réussis, artefact JSON `anamu-p0-source-audit` conservé sept jours. **Aucune archive téléchargée.**
2. [P0 - vérifier accès GigaMIDI, exécution réussie](https://github.com/leye0/AnaMu/actions/runs/42333456588), quatre tests réussis. Requête `HEAD` ciblée sur `v2.0.0/validation/00001.parquet`, redirections désactivées, **aucun contenu téléchargé** : réponse anonyme **HTTP 401**, `HF_TOKEN` absent des secrets Actions, essai authentifié non exécuté.

Les scripts se trouvent dans `scripts/source_audit.py` et `scripts/probe_gigamidi_access.py`. Ils n'ont besoin d'aucun modèle ML. Les résultats sont des observations datées, non des garanties permanentes.

## Sources examinées

| Source | Faits observés ou officiellement documentés | Accès et téléchargement partiel | Utilité pour AnaMu |
|---|---|---|---|
| [XMIDI](https://github.com/xmusic-project/XMIDI_Dataset) | 108 023 fichiers MIDI, émotions annotées par des professionnels. Dépôt GitHub ne contenant que `README.md`. | Les auteurs proposent un **ZIP Google Drive unique**. Le `HEAD` a rendu une page HTML, sans taille exploitable. **Taille réelle et possibilité d'extraction partielle non établies.** | **Corpus maître des étiquettes émotionnelles humaines.** |
| [GigaMIDI v2](https://huggingface.co/datasets/Metacreation/GigaMIDI) | > 2,1 millions de MIDI ; schéma annoncé avec titre, artiste, scores de correspondance audio+texte, ID Spotify et MusicBrainz, signatures et caractéristiques structurelles. Les auteurs déclarent intégrer XMIDI. | Hub `gated=auto` ; conditions de recherche non commerciale. Fichiers Parquet répartis par sous-ensembles ; ZIP complet ~5,51 Go et CSV de métadonnées ~1,25 Go. Le dataset documente un mode **streaming** après autorisation. **L'efficacité réelle en octets à transférer reste à mesurer.** | **Référentiel d'identification et d'analyses préexistantes ; pas une source de vérité émotionnelle humaine.** |
| [MetaMIDI](https://zenodo.org/records/5142664) | 436 631 MIDI, 168 032 rapprochés d'ID MusicBrainz, relations audio Spotify. | Enregistrement public mais fichiers **restreints** sur Zenodo ; demande avec affiliation et description de recherche. API publique n'expose pas de fichiers accessibles. | Résultats de rapprochement utiles si accès accordé ; déjà partiellement inclus dans GigaMIDI. |
| [Discover MIDI](https://huggingface.co/datasets/projectlosangeles/Discover-MIDI-Dataset) | Déclare 6,74 millions de MIDI et des caractéristiques pré-calculées. L'API du Hub annonce seulement cinq fichiers racine dont une grosse archive. | Pas de portail `gated` ; **pas de Parquet** répertorié dans l'API racine, viewer standard indisponible. Les caractéristiques peuvent être archivées ; accès individuel à tester. Licence CC BY-NC-SA 4.0. | Solution secondaire pour la recherche d'identités et de similarités ; budget de transfert à vérifier. |
| [EMOPIA](https://github.com/annahung31/EMOPIA) | 1 087 extraits MIDI de piano pop, émotions humaines en quatre quadrants. Zenodo publie un ZIP de **5 510 182 octets** (v1.0). | Petit téléchargement possible, mais **non nécessaire pour la jonction XMIDI→GigaMIDI**. Licence CC BY-NC-SA 4.0. | Jeu de validation humaine complémentaire, non substitut à XMIDI. |
| [Lakh MIDI](https://colinraffel.com/projects/lmd/) | 176 581 MIDI, dont 45 129 reliés à Million Song Dataset ; métadonnées et scores de rapprochement déjà publiés. | Les métadonnées et scores sont téléchargeables séparément. Licence CC BY 4.0 du jeu diffusé. | Référence de contrôle des rapprochements, sans réexécuter l'analyse audio originale. |

Les licences des compilations n'effacent pas les droits éventuels sur les compositions, enregistrements et paroles.

## Découverte importante : XMIDI dans GigaMIDI

La fiche GigaMIDI v2 affirme incorporer XMIDI, mais **n'établit pas** dans son schéma documenté :

- la présence d'une colonne gardant le **nom original de fichier XMIDI** ;
- la conservation du **MD5 exact de la version XMIDI non normalisée** ;
- le transfert des **11 étiquettes émotionnelles humaines**, de leur provenance et de la méthodologie d'annotation ;
- la proportion d'éléments XMIDI qui disposent de titres, d'artistes ou d'ID MusicBrainz fiables.

Ces quatre inconnues forment maintenant le cœur de P1. Il serait incorrect de conclure que « GigaMIDI identifie XMIDI » simplement parce qu'il le contient. Après autorisation, inspecter le schéma réel et les lignes accessibles **avant** d'implémenter des signatures musicales coûteuses. Si l'ID d'origine est absent ou le MIDI normalisé, chercher la table de traçabilité publiée ; seulement ensuite envisager les correspondances par empreintes/structure.

## Blocage d'accès mesuré

- Le propriétaire du projet a indiqué avoir accepté les conditions GigaMIDI sur son compte Hugging Face.
- Le runner GitHub **n'a pas de `HF_TOKEN`** à ce jour (exécution du 7 novembre 2026).
- L'accès public direct à un fichier Parquet a renvoyé **HTTP 401**.
- Donc **aucun MIDI de GigaMIDI n'a été lu** et aucune correspondance XMIDI/GigaMIDI n'a été mesurée.

**Action à effectuer par le propriétaire :** créer un jeton Hugging Face avec permission de lecture limitée au dépôt GigaMIDI et l'ajouter aux secrets *Actions* du dépôt AnaMu sous le nom `HF_TOKEN`. Ne jamais publier le jeton dans un commit, un problème GitHub ou une conversation. Une fois ce secret présent, relancer le workflow **P0 - vérifier accès GigaMIDI** ; une redirection autorisée à la requête `HEAD` sera un premier signal, à confirmer par une lecture bornée.

## Étape suivante, après authentification

1. Vérifier l'accès au Parquet de validation ; examiner le schéma/les premiers enregistrements **avec un plafond strict d'octets et de lignes**.
2. Mesurer le trafic effectif du mode streaming Hugging Face : une interface qui expose une ligne à la fois ne garantit pas zéro téléchargement de blocs Parquet.
3. Tester les champs de provenance et les liens explicites avec XMIDI, avant toute analyse de similarité.
4. Choisir une méthode de jointure conservatrice et réserver les comparaisons MIDI lourdes aux cas non identifiés.
5. Publier le nombre de lignes lues, la volumétrie transférée, la part identifiable et les limites, sans conclure avant mesure.

**Aucune extraction de plusieurs Go ni aucun traitement audio ne sont autorisés implicitement par cet audit.**
