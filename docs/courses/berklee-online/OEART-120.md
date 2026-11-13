# OEART-120 — Ear Training 2

**Berklee Online, 3 crédits, cours de 12 semaines.** Auteur : **Gaye Tolan Hatfield**. Relevé du 10 novembre 2026. **Syllabus public réel structuré ; leçon complète et barème non obtenus.**

## Provenance et portée

- [Page officielle, sections « Syllabus » et « Requirements »](https://online.berklee.edu/courses/ear-training-2#syllabus) : progression par leçon et activités réellement affichées ; ne pas confondre avec le campus Boston ou l'UdeM/McGill.
- **Objectif du cours :** Suite de la formation auditive : mineur naturel, harmonique, mélodique et mélodique jazz ; swing, 6/8, métrique alla breve, syncopes, intervalles et accords de septième.

## Plan pédagogique public (résumé original)

| Leçon | Matière étudiée | Exercice ou exemple identifié |
|---|---|---|
| 1 | Révision du majeur et des rythmes | Diagnostic et vidéo de prestation |
| 2 | Mineur mélodique jazz, notes attractives, 6/8 | Chant et rythme |
| 3 | Renversements d'accords, subdivisions mixtes | Transcription et dictée |
| 4 | Mineur harmonique, swing et septièmes | Prestation et dictée |
| 5 | Mineur harmonique et valse jazz, accords de septième | Déchiffrage, étude rythmique et dictée |
| 6 | Révision mineur harmonique, swing et septièmes | Évaluations de mi-session : lecture puis dictée |
| 7 | Mineur naturel, six-huit dirigé, notes-guide | Chanter la gamme et le mètre |
| 8 | Tétracordes et mélodies mineures naturelles, dictée 6/8 | Prestation mélodique et dictée harmonique |
| 9 | Mineur mélodique traditionnel et alla breve | Chant et rythmes coupés |
| 10 | Mélange des mineurs, syncopes en doubles croches | Prestation mélodique et rythmique |
| 11 | Triolets de noires, mélodies en mineur et accords de septième | Lire et interpréter |
| 12 | Révision des mineurs, alla breve, triolets et harmonie | Examens finaux de lecture puis dictée |

## Lectures, activités et lacunes

- **Exigences et lectures :** Préalable : Ear Training 1 ou expérience équivalente. **Manuel imposé :** *Ear Training 2 Workbook* (deOgburn et coll.). Les enregistrements vidéo d'exercices et un logiciel de notation sont requis.
- **Nature exacte des preuves :** Des exercices sont nommés pour les douze semaines, avec **évaluations distinctes de lecture et de dictée** aux leçons 6 et 12. Les audio d'épreuves, réponses et barèmes ne sont pas accessibles.
- **Cours comparables :** Le cours [UdeM MUS 1012](../udem/MUS-1012.md) est une voie de solfège et dictée, sans équivalence de niveau ou de modalité démontrée.
- **Reste à obtenir :** cahier des consignes, supports d'écoute et partitions, corrigés, devoirs soumis, barèmes et édition spécifique d'une section. Les intitulés de tâches du site ne doivent pas être pris pour les énoncés intégraux.

**Réserve de phase :** cette fiche archive une **source pédagogique académique**, sans implémentation d'analyse musicale et sans création de tests logiciels.

## Application à l’analyse et à la création — regroupement métrique et notes variables du mineur (13 novembre 2026)

**Preuve du cours.** Le [plan public OEART-120](https://online.berklee.edu/courses/ear-training-2#syllabus) juxtapose mineur mélodique jazz et 6/8 (leçon 2), mineur harmonique et swing (4), mineur naturel et direction du 6/8 (7–8), puis mineur mélodique traditionnel et phrases comparées (9–10). Les études sont des adaptations AnaMu.

### Q1 — Six croches ne disent pas s’il y a deux ou trois appuis

**Analyse.** Dans l'[exemple MIDI original](./OEART-120/exemple.mid), comparer A, m. 1–2 en 6/8, et B, m. 3–4 en 3/4. Chaque mesure dure 1,5 s et les hauteurs, positions d’attaque relatives et durées se répètent à l’identique dans B. En A, les vélocités favorisent les croches 1 et 4, en B les croches 1, 3 et 5. Vérifier d'abord la grille de six attaques, puis les regroupements 3+3 et 2+2+2. Le fichier encode un regroupement via **deux indices** (signature et vélocité), pas une preuve qu’une vélocité particulière produit toujours un accent audible. L'appui imprimé par la hauteur reste un indice concurrent.

**Création.** Comparer les deux variantes en masquant l’indication de mesure à l’écoute. Une troisième version avec vélocités uniformes isolerait mieux le rôle des hauteurs, mais n'est pas incluse. **Preuve :** `MIDI_DIRECT` pour grille et vélocités, `AUDIO_REQUIRED` pour juger la pulsation réellement entendue.

### Q2 — Le sixième et le septième degrés variables se lisent en contexte

**Analyse.** En la mineur, distinguer fa → mi d'une montée fa♯–sol♯–la, puis relever la basse et la destination. Dans une phrase contenant les deux, un passage local peut avoir une inflexion mélodique ou un appui de dominante sans changement de tonalité. La collection cumulée des notes du passage ne décrit ni l'ordre ni la fonction. Un fragment incomplet sans sixte ou septième significative ne tranche pas entre les formes du mineur.

**Création.** Écrire trois fins de phrase avec même mètre, registre et arrivée sur la. Varier seulement les degrés 6 et 7 dans la mélodie et laisser le même support neutre sur la–mi. Ajouter ensuite une basse mi → la pour une écoute séparée. La comparaison des formes du mineur est **textuelle, non encodée dans le MIDI joint**, qui porte sur Q1. **Preuve :** `MIDI_PROXY` pour les inflexions et leur fonction.

## Cas sur partition — une hémiole peut franchir la barre de mesure (13 novembre 2026)

**Ancrage.** Le [syllabus OEART-120](https://online.berklee.edu/courses/ear-training-2#syllabus) atteste la battue, la subdivision et la dictée en mètre composé. Ce cas de regroupement binaire/ternaire est un comparateur, pas un extrait de dictée du cours ni un exemple noté en 6/8.

**Cas : Haendel, *Hornpipe*, *Water Music*, HWV 349, m. 1–10.** Dans la réduction de Hesselink, les huit premières mesures organisent trois blanches par mesure. Aux m. 9–10, la même durée de six blanches est organisée en trois groupes de deux : les groupes commencent à m. 9, temps 1 et 3, puis à m. 10, temps 2. Le groupe du milieu franchit donc la barre, alors que la notation conserve le 3/2. Le contexte cadentiel explique pourquoi ce regroupement est local plutôt qu’une nouvelle signature durable. [Nathan Hesselink, fig. 1, p. 3](https://journal.iftawm.org/wp-content/uploads/2022/06/Hesselink_AAWM_Vol_10_1.pdf).

**Analyse et réemploi.** Garder la blanche comme unité commune, noter la barre et les appuis sur deux lignes, puis chercher quelles attaques, tenues ou basses soutiennent la lecture par deux. Créer une fin de phrase en 3/2 et comparer une cadence qui maintient deux groupes de trois à la même arrivée préparée en trois groupes de deux. À l’écoute, battre les blanches dans les deux versions et marquer seulement les appuis candidats. Le [MIDI existant](./OEART-120/exemple.mid) compare plutôt deux signatures et deux jeux de vélocités : il n’encode pas cette hémiole de Haendel. **Preuve :** `MIDI_PROXY / AUDIO_REQUIRED`.
