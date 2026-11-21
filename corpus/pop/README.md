# Corpus pop AnaMu — objectif 2 000 chansons

Décision de Léon, **21 novembre 2026** : acquisition gratuite de chansons de pop par des artistes ayant atteint le top 5/top 10 du Billboard durant les quinze dernières années, avec musique MIDI instrumentale, partie chantée identifiable et paroles. La cible est **2 000 chansons distinctes complètes**, pas 2 000 fichiers, arrangements ou transpositions.

## Premier lot réellement acquis

| Mesure | Nombre | Portée |
|---|---:|---|
| Identités de chansons regroupées, MIDI et paroles acquis | 1331 | Candidats, pas chansons complètes validées |
| Structure avec au moins trois canaux actifs, dont deux mélodiques | 1051 | Instruments programmés, pas pistes audio originales |
| Export des événements MIDI `lyrics` existants | 459 | Horodatages de source, pas alignements validés |
| Indication vocale/mélodique dans une piste source à canal unique | 71 | Affectations candidates à relire |
| Titre associé au top 5 dans le miroir Billboard | 292 | La preuve source et sa date sont conservées |
| Titre associé au top 10, top 5 compris | 440 | Ne pas additionner au top 5 |
| Autres titres des artistes admissibles | 891 | Rang du morceau non requis pour cette extension |
| Étiquette `pop` dans la source de paroles | 566 | Étiquette externe, pas expertise stylistique |
| Autre étiquette de genre / genre inconnu | 132 / 633 | Triage pop/rap/country/rock encore nécessaire |
| Titres répondant à tous les critères vérifiés | **0 / 2 000** | Ne pas remplacer cet objectif par le compteur d'acquisition |

**Le paquet privé `AnaMu-pop-lot-01.zip` contient les vrais `score.mid`, `lyrics.txt`, les exports `lyrics-timed.tsv` lorsqu'ils existent et un inventaire par chanson.** Dans ce dépôt public, le [manifeste](manifest.json), le [catalogue](CATALOGUE.md), les [sources](sources.json) et l'[index des membres d'archive](manifest.json) permettent de retrouver exactement ces fichiers et leurs empreintes. Les paroles intégrales et les MIDI tiers ne sont pas publiés ici. Le titre du morceau et l'artiste ne sont pas des paroles.

## Sélection et dédoublonnage

Le périmètre de travail est le **Billboard Hot 100**, du 1er janvier 2011 au 21 novembre 2026. Les titres ayant eux-mêmes atteint le top 5 puis le top 10 sont prioritaires. Les autres titres d'un artiste ayant atteint le top 10 pendant cette période peuvent compléter le corpus. Le miroir est une source secondaire, pas une vérification indépendante de toutes les pages officielles.

La concordance de titres et de crédits est normalisée pour la casse, les accents et la ponctuation, sans rapprochement flou de titres différents. Les crédits d'invités explicites sont dépliés pour identifier l'artiste admissible. Une première observation historique dans le classement avant 2011 exclut le candidat charté de cette passe; pour les autres morceaux, l'année déclarée par la source de paroles reste provisoire. **Première entrée au classement, date de réédition et date de sortie originale ne sont pas équivalentes.** La preuve de sortie originale reste ouverte.

Les copies, crédits et éditions *Taylor's Version* identifiés ont été regroupés par titre et artiste principal : **21 identités de variantes** ne sont pas comptées comme chansons supplémentaires. C'est un premier regroupement nominal, pas un dédoublonnage musicologique achevé. Les différentes versions non retenues restent décrites dans le manifeste. Les empreintes exactes des MIDI retenus sont distinctes.


Deux appariements source contradictoires (*Mean* et *Mine*, dont le MIDI est étiqueté *ME!*) ont été mis en quarantaine. Les versions acoustiques, live et longues repérées sont regroupées avec leur chanson.

## Ce qui a été contrôlé

Lecture stricte des MIDI avec `mido==1.3.3`; inventaire des canaux, pistes, noms, programmes et attaques; présence du texte acquis; CRC32 des membres ZIP lus par plages et SHA-256 des fichiers produits. **22 candidats de fichiers invalides ou vides** sont consignés dans `failures`, sans réparation silencieuse. Les sources originales ne sont ni transposées, ni quantifiées, ni réorchestrées.

Un MIDI de type 0 peut contenir plusieurs instruments sur différents canaux dans une seule piste. Le canal 10 ne suffit pas à garantir une batterie effective; les programmes GM sont des indications de rendu. L'étiquette d'une piste à plusieurs canaux ne désigne pas un canal vocal unique. Un timbre aigu ou un instrument GM de voix ne prouve pas la partie chantée. Les coïncidences entre ticks de paroles et attaques sont consignées uniquement comme observations, sans choix automatique d'une voix.

Les fichiers ont des **paroles associées par les corpus amont**; cette association n'est pas une validation de la version, de la langue ou des syllabes. Aucun audio studio ni stem original n'est inclus; les instruments sont des transcriptions/arrangements MIDI. Aucune audition humaine, partition indépendante ou analyse musicale complète n'a été effectuée. Aucun `vocal.mid` n'est inventé sur une sélection automatique.

## Réacquérir les fichiers

Depuis un clone du dépôt AnaMu, le petit utilitaire d'acquisition lit le manifeste et les sources figées. Il récupère seulement les membres nécessaires de la grande archive par requêtes HTTP Range, plus le sous-ensemble compact, puis confronte les fichiers aux empreintes publiées. Il n'exécute pas de pickle ou de code du corpus tiers.

```sh
python -m pip install mido==1.3.3
python corpus/pop/tools/materialize.py --destination /chemin/prive/anamu-pop --cache /chemin/cache/anamu-pop
```

La destination est explicitement hors du dépôt public. Le script refuse de remplacer un fichier local différent. Pour reprendre un téléchargement, réutiliser son cache. L'accès distant reste dépendant de la disponibilité de la source.

## Provenance et conditions

Alex Sigalov / Project Los Angeles déclare le corpus amont sous **CC BY-NC-SA 4.0**; l'archive attribue aussi les jeux de données de MIDI et de paroles d'origine. Cette déclaration est enregistrée comme celle du compilateur et n'est pas une attestation indépendante des droits sur chaque chanson, parole ou transcription. Le lot acquis est remis pour le travail privé; toute republication des contenus ou autre utilisation demande d'examiner les droits applicables. Aucun achat ni abonnement n'a été effectué : **0 $ de contenu**.

Les prochaines tâches sont dans le [TODO unique](../../docs/todo-university-coverage.md#corpus-pop-gratuit--21-novembre-2026). Priorité : isoler le sous-ensemble vraiment pop, vérifier les dates originales, établir les parties vocales, relire les appariements de paroles, puis acquérir d'autres chansons distinctes. Ne pas relancer les téléchargements déjà faits pour gonfler les chiffres. Ce chantier parallèle ne modifie pas les compteurs universitaires et n'active aucun moteur musical, test ou CI.
