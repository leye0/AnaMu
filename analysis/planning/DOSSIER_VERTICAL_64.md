# P5 pilote — Dossier de raisonnement manuel sur trois figures 6/4

**25 novembre 2026 · Cas construit, non analyse automatique d'une œuvre.**

Sources de matière : [CM-211, section « Trois sixtes et quartes, trois
fonctions »](../../docs/courses/berklee/CM-211.md#trois-sixtes-et-quartes-trois-fonctions--17-novembre-2026)
et [section « Atelier sonore »](../../docs/courses/berklee/CM-211.md#atelier-sonore-et-partitions--fonctions-en-contexte-18-novembre-2026).
Matière : **material:0000013**, révision 1. Mentions et principes proposés :
[calibration P2b](../knowledge/mentions/calibration-2026-11.json),
notamment candidate-assertion:0001 et candidate-assertion:0002.
Les exemples sont des **constructions originales AnaMu** ; ils ne sont
pas des œuvres notées ou devoirs officiels attribués à Berklee.

## 1. Objet et question

Une figure de quarte et sixte décrit des intervalles **au-dessus d'une
basse**. Selon sa préparation, sa basse et la conduite des autres voix,
elle peut contribuer à des fonctions différentes. La question n'est
donc pas « quel nom d'accord pour cette collection ? », mais **quelle
lecture est soutenue dans la réalisation et la phrase ?**

Nous distinguons ici :
- un **fait du schéma fourni** (texte de la fiche) ;
- une **interprétation proposée selon le cadre tonal déclaré** ;
- une **preuve absente**, même si l'exemple est pédagogiquement plausible.

## 2. Trois variantes du même domaine, trois dossiers de preuve

| Cas de la fiche CM-211 | Données écrites dans le schéma AnaMu | Lecture conditionnelle | Ce qui empêche une règle automatique |
| --- | --- | --- | --- |
| A : cadentielle | Basse sol fixe ; sol–do–mi puis sol–si–ré, avec do→si et mi→ré | Figure 6/4 cadentielle embellissant une dominante, sous le cadre tonal décrit | Une verticale sol–do–mi **isolée** ne prouve pas cadence, résolution ou frontière de phrase |
| B : passage | Basse do→ré→mi ; I → V6/4 → I6 | Figure de passage, déployée sur une basse mobile | Le seul chiffrage 6/4 ne transforme pas ce mouvement en fonction cadentielle |
| C : pédale/voisine | Basse do maintenue ; I → IV6/4 → I, avec mi→fa→mi et sol→la→sol | Mouvement de voisinage décorant la tonique | Le fa transitoire ne prouve pas changement de centre tonal |

L'examen manuel applique successivement les mêmes **questions
générales** à A, B et C ; il n'encode pas les trois noms comme une
reconnaissance de suites de notes.

1. **Délimitation** : quel événement sert de basse réelle, dans quelle
   notation et quelle partie ? Une touche grave est une observation de
   registre, non une voix de basse certifiée.
2. **Simultanéités** : quelles notes sont tenues et quels intervalles
   figurent au-dessus de cette basse ? Conserver les graphies si
   présentes ; le MIDI ne garantit pas ces graphies.
3. **Trajectoires** : quelles voix restent, changent, se résolvent ou
   s'éloignent ? Les mouvements 4→3 et 6→5 sont des indices locaux dans
   le cas A, pas un théorème sur chaque figure 6/4.
4. **Contexte** : quels accords précèdent et suivent, quel centre est
   effectivement établi, et qu'arrive-t-il après l'arrivée ?
5. **Portée** : parle-t-on d'un nom de figure, d'une fonction locale,
   d'une cadence de phrase ou de sa perception sonore ? Ces
   conclusions requièrent des preuves différentes.

## 3. Chaîne des assertions et statuts

| Objet de raisonnement | Appui | État dans ce dossier |
| --- | --- | --- |
| Une figure 6/4 peut recevoir plusieurs fonctions | Définition comparative CM-211 ; candidate-assertion:0001 | **Savoir proposé**, non reconnaissance d'une occurrence |
| En A, 4→3 et 6→5 sur la dominante soutiennent une lecture cadentielle | Schéma de la fiche ; candidate-assertion:0002 | **Interprétation de l'exemple écrit**, cadre tonal déclaré |
| En B, la basse de passage soutient une autre lecture | Trajectoire do→ré→mi écrite dans le tableau | **Interprétation de l'exemple écrit** |
| En C, les voisines sous basse maintenue soutiennent la pédale | Mouvements de retour écrits dans le tableau | **Interprétation de l'exemple écrit** |
| Une œuvre inconnue contenant la même verticale réalise une cadence parfaite | Aucune œuvre, graphie, phrase ou audition fournie | **Non établi** |
| La cadence A est perceptivement plus forte que B ou C | Aucun jugement d'écoute recueilli dans ce dossier | **Non établi** |

Les assertions candidates ne sont pas des règles du moteur validées :
elles restent attachées à leur source, avec la réserve qu'une autre
tradition ou une suite différente peut conduire à un autre diagnostic.

## 4. Contre-examen : retirer une seule preuve

**Expérience conceptuelle** : supprimons la trajectoire de basse,
les voix et la phrase et conservons uniquement les hauteurs de la
première verticale.

Les trois fonctions ne peuvent plus être départagées. Une sortie
du type « fonction = cadentielle » serait alors un faux positif.
Le [planificateur P4](DEMONSTRATION_PLAN_PREUVES.md) doit faire
apparaître la recherche de basse, de conduite de voix et de contexte
comme **bloquée**, tandis que la consultation de la collection est
possible sous hypothèse déclarée.

À l'inverse, si une partition annotée révèle la suite et les voix,
les tâches deviennent **prêtes à examiner**, pas automatiquement
« vraies ». Une écoute supplémentaire pourra ensuite traiter la
force perceptive d'une clôture, sans modifier les observations de
notes déjà localisées.

## 5. Frontière source / œuvre / modèle

- **Faits de la fiche** : les trois schémas et les critères décrits.
- **Savoirs candidats** : rapports entre chiffrage, basse, voix et
  fonction ; ils demandent encore réconciliation et revue.
- **Preuve d'événements MIDI** : le fichier pédagogique CM-211
  six-quartes-trois-fonctions.mid a depuis été lu, avec les événements
  localisés dans le [rapport d'audit](../examples/cm211-six-four-midi-observations.json).
  Il permet de vérifier les attaques notées, **pas** une fonction harmonique
  ni une écoute.
- **Œuvre indépendante** : absente ; cette étude reste une démonstration
  AnaMu, pas une évaluation sur une œuvre extérieure aux exemples.
- **Capacité automatique** : les mécanismes MIDI initiaux d'AnaMu
  savent inventorier des notes et sonorités ; ils ne savent pas
  attribuer ce choix fonctionnel.
- **Évaluation indépendante** : non réalisée ; le dossier est un
  parcours de conception et une base pour préparer un véritable
  examen de passage musical.

## 6. Audit du véritable MIDI de l'étude AnaMu

**Un pas supplémentaire a été réalisé après la première rédaction de ce
dossier** : le fichier
[six-quartes-trois-fonctions.mid](../../docs/courses/berklee/CM-211/six-quartes-trois-fonctions.mid)
a été lu comme fichier MIDI format 1 via sa version Git
(empreinte blob SHA-1 commençant par 903eba91). Il contient cinq pistes,
dont quatre nommées Basse, Tenor, Alto et Soprano, à 480 ticks/noire,
4/4 et noire = 96. Les quatre pistes musicales comportent **27 attaques
de notes chacune**, soit **108 attaques**. Le nombre de Note Off observé
est aussi de 108 ; l'appariement strict de toutes les notes n'est pas
revendiqué par ce seul contrôle.

Les marqueurs de variantes commencent à 0:00, 0:22,5 et 0:45,0.
Voici les **numéros MIDI** des quatre pistes au début, au milieu et
à l'arrivée de leurs fenêtres décisives :

| Cas | Premier instant | Deuxième instant | Arrivée |
| --- | --- | --- | --- |
| A · m. 7→8 | [43, 55, 60, 64] | [43, 55, 59, 62] | [48, 55, 60, 64] |
| B · m. 16→17 | [48, 55, 60, 64] | [50, 55, 59, 67] | [52, 55, 60, 67] |
| C · m. 25→26 | [48, 55, 60, 64] | [48, 57, 60, 65] | [48, 55, 60, 64] |

L'ordre de chaque tableau est **Basse, Tenor, Alto, Soprano** tel que
nommé dans le MIDI. Les notes du deuxième instant sont attaquées
960 ticks après le début de la mesure, soit au troisième temps de 4/4 ;
l'arrivée est à la mesure suivante.

**Lecture comparée :** ces événements donnent les trajectoires
sol→sol→do, do→ré→mi et do→do→do dans la piste basse, comme le schéma
didactique. Mais nommer une piste « Basse » dans un MIDI ne suffit pas
à certifier son statut musical dans toute œuvre, et les trois fonctions
restent des **interprétations de la fiche**, sous son cadre tonal.

Ce que l'audit **n'a pas** fait : vérifier la partition MusicXML,
écouter l'audio, évaluer une cadence ou confronter une interprétation
à des annotations musicales indépendantes. Il confirme un **échantillon
réel d'événements** que le futur moteur pourra recevoir sans prétendre
que la classification fonctionnelle soit déjà implémentée.

## 7. Conditions d'une reprise réellement musicale

1. Choisir une pièce et une édition identifiables et fixer un passage.
2. Aligner partition/voix, événements MIDI éventuels et audio si la
   question l'exige, sans déclarer les supports équivalents.
3. Instancier ce dossier à partir d'observations **réellement obtenues**.
4. Enregistrer les lectures concurrentes avec leurs appuis/objections.
5. Demander une revue musicale indépendante, puis mesurer les
   divergences et revisiter les connaissances concernées.

**Premier gain :** on voit précisément ce que le moteur devra
savoir demander, comparer, bloquer et expliquer. **Ce dossier ne
constitue pas la preuve qu'il sait déjà le faire.**
