# Acquisition exhaustive de la matière des cours

**Phase active unique d'AnaMu.** Ce contrat garantit qu'un catalogue ou une description sommaire ne soit jamais pris pour le **contenu musical réellement enseigné**.

## Unité : un cours dans une édition donnée

Partir des [inventaires officiels](university-curriculum.md), des JSON de
[l'index](README.md) et du
[registre de progression](data/course-material-progress.json). Chaque cours
nommé et chaque option encore ouverte doit avoir une fiche indiquant :

**Convention des fiches :** une fiche Markdown par cours dans
**docs/courses/udem/**, **docs/courses/mcgill/** ou **docs/courses/berklee/**,
nommée d'après le code du cours (espaces remplacés par des traits d'union).
Le registre fait autorité pour le statut et indique le chemin dans le champ
**material_file** dès que la première fiche sourcée existe. Il contient
actuellement **402 codes de cours candidats** et **5 pools de choix** à
déplier : ce sont des *points de départ*, pas une liste close.

| Champ | Information indispensable |
|---|---|
| institution / programme / édition / code / intitulé | Identité stable, sans confusion des versions |
| statut | Obligatoire, optionnel, recommandé, cours voisin pertinent ; admissibilité distincte de pertinence |
| sources | URL officielle ou ressource autorisée, date, section précise, droits d'accès |
| état du syllabus | Introuvable / description seule / plan partiel / syllabus obtenu / matière vérifiée |
| objectifs | Résultats d'apprentissage réellement annoncés |
| matière | Chaque thème, chapitre, technique, section et prérequis, avec source |
| lectures | Ouvrages et chapitres prescrits ; distinguer suggestion et obligation |
| exercices | Travaux, consignes, projets, barèmes et critères observables |
| exemples | Répertoire et passages proposés, style, instrument, exceptions |
| lacunes | Documents absents, versions divergentes, sections inaccessibles |
| apport de connaissance | Savoirs distinctifs potentiels, sans prétendre les avoir maîtrisés |

Une source inaccessible reste **inconnue**. Ne jamais inférer un syllabus du seul titre du cours ni confondre une liste de manuels avec les séances enseignées.

## Ingestion en lots plutôt que fiches longues pendant la recherche

**Nouvelle règle de cadence :** traiter 10 à 30 cours/sources par passe dans
une seule table docs/raw-batches. Les fiches individuelles sont la destination
finale après l'ingestion, pas un obstacle à l'exploration. Chaque ligne donne
le code, l'édition, le lien, la qualité de la source et la matière réellement
enseignée. Conserver les inconnues et les contradictions.

Priorité : d'abord les 402 cours suivis (notamment catalog_only), puis les
options à déplier, puis les autres cours académiques complémentaires. Un
plan-cadre externe ne promeut aucun cours au statut syllabus obtenu.
Les chiffres de PDF, de cours distincts et de vrais syllabus restent
séparés. Aucun test ni travail sur la CI.

## Procédure, cours par cours

1. **Fixer l'édition officielle** et explorer toutes les branches obligatoires, optionnelles, recommandées et complémentaires pertinentes.
2. **Chercher le plan détaillé** auprès de l'établissement : page du cours, syllabus public, calendrier pédagogique, objectifs, références ou exercices autorisés.
3. **Comparer les versions**, relever les lacunes, accès restreints et différences de contenu ; les compléments secondaires sont étiquetés comme tels.
4. **Découper chaque matière obtenue** en résultats d'apprentissage, chapitres, concepts, techniques, exercices et exemples, avec citations vérifiables.
5. **Vérifier chaque choix** et chaque section ; ne jamais exclure un cours parce que son intitulé ressemble à un autre.
6. **Enregistrer les preuves et les inconnues**, mettre à jour [le TODO](todo-university-coverage.md), puis passer au cours suivant.
7. **Ne développer aucun analyseur** pendant cette phase.

### Boucle de travail obligatoire pour tout agent reprenant le projet

1. Lire le registre et reprendre au **premier cours dont la matière est
   incomplète**. L'ordre conseillé privilégie les matières obligatoires,
   mais aucun cours optionnel pertinent ne sera abandonné.
2. Rechercher **systématiquement plusieurs sources** de contenu réel :
   syllabus institutionnel, page du cours, objectifs, calendrier, lectures,
   exercices, documents publics autorisés. Ne pas transformer le premier
   résultat de recherche en preuve d'exhaustivité.
3. Rédiger sa fiche dans un dossier de matières du programme, en citant les
   sections effectivement disponibles et les parties encore inconnues.
   Une fiche peut être partielle et doit le dire clairement.
4. Actualiser l'état du cours dans le registre. Ne marquer « syllabus obtenu »
   que si une vraie source de cours a été examinée et citée. Une fiche de
   catalogue reste « catalogue seulement ».
5. Passer au cours suivant ; **ne pas demander confirmation à chaque étape**.
   Si l'accès échoue, noter le blocage et changer de cours plutôt que
   prétendre que la couverture est terminée.

**Travail purement documentaire :** aucune implémentation d'algorithme,
aucun benchmark, aucune expérimentation de composition ni test logiciel
n'est une condition de progrès pendant cette phase. Le contrôle automatique
des liens et des statuts sert seulement à éviter des omissions de suivi.

### Contenu minimum d'une fiche rédigée

- **Cours et édition :** identifiant, année, statut et source du catalogue.
- **Sources pédagogiques obtenues :** liens autorisés, titre, auteur ou
  département, date, sections consultées et restriction de reproduction.
- **Plan réel :** résultats d'apprentissage, chapitres, lectures et
  exercices, chacun lié à la source correspondante.
- **Exemples et contexte :** œuvres et styles mentionnés, conventions
  spécifiques, différences éventuelles entre versions.
- **Ce qui manque :** séances, textes, exercices ou pages non accessibles,
  statut de vérification, pistes licites pour compléter le contenu.
- **Prochaine action :** source exacte à consulter ou autre cours à traiter.

Les **résumés sont rédigés de manière originale** : ne pas recopier
longuement des plans de cours sous droit d'auteur. Le statut du registre
reste **catalog_only** tant que la matière obtenue n'est pas sourcée.

Si un syllabus est non redistribuable ou soumis à accès restreint, consigner sa provenance et son état ; ne jamais contourner les restrictions ni importer des documents protégés sans autorisation.

## Porte avant la base de concepts

- Tous les cours et options pertinentes ont été recensés, y compris ceux cachés derrière des réserves de crédits.
- Chaque cours dispose d'une matière détaillée sourcée **ou d'une lacune explicite bloquant toute déclaration d'exhaustivité**.
- Les chapitres, lectures, exercices, exemples et variantes réellement disponibles sont structurés avec leur provenance.
- Les exclusions sont justifiées par comparaison de savoirs, pas par commodité.
- La couverture a été vérifiée et **Léon autorise explicitement** le passage à la réconciliation des concepts.

Une fiche « description seule » ne clôt pas un cours. Les exigences de détection MIDI et de composition restent verrouillées.
