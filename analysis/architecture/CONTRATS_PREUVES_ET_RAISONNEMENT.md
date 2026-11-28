# P0 — Contrat d'identité, d'assertions et de raisonnement conditionnel

**Édition de conception 1 · 25 novembre 2026.** Ce contrat précise le
[plan directeur](../planning/PLAN_RAISONNEMENT_MUSICAL.md) et s'applique
au registre pilote de la [PR de matière](../knowledge/MATERIAL_REGISTRY.md).
Il ne certifie aucune compétence musicale et ne remplace aucune source de cours.

## 1. Séparer les objets plutôt que gonfler un « concept »

| Objet | Responsabilité | Confusion interdite |
| --- | --- | --- |
| SourceDocument / SourceSpan | Version d'un document et passage consulté | Document disponible ≠ document lu/validé sémantiquement |
| MaterialUnit | Matière identifiable, éditable et attribuable à des sources | Rubrique Markdown ≠ concept ni savoir maîtrisé |
| Mention | Formulation réellement présente, langue, attribution, portée, emplacement | Terme voisin ≠ sens identique |
| ConceptSense | Sens défini et frontières d'emploi | Nom du concept ≠ détecteur MIDI |
| KnowledgeAssertion | Proposition conditionnelle, négation, exception et validité | Assertion générale ≠ conclusion sur une œuvre |
| Relation | Liaison typée et justifiée entre objets | Chronologie musicale ≠ prérequis de calcul |
| AnalysisOperation | Question, voies de preuve alternatives, hypothèses produites | Opération disponible ≠ preuve d'une interprétation |
| EvidenceItem | Événement ou fait d'œuvre localisé, versionné et attesté | Note MIDI ≠ voix, instrument réel ou geste |
| AnalysisClaim | Conclusion candidate, appuis, objections, alternatives, cadre, révision | Appui d'une hypothèse ≠ vérité exclusive |
| AnalysisTask | Exécution envisagée, prête, bloquée, différée ou à revoir | Planifier une tâche ≠ l'avoir exécutée |

Conserver les IDs opaques et pérennes, distincts de la position dans les cours,
de la catégorie musicale et du nom de fichier. Les scissions, fusions et
relocalisations sont des décisions éditoriales traçables, pas un effet caché
de l'indexation.

## 2. Portée, provenance et statut indépendants

Chaque énoncé conserve au minimum :

- source_refs : document versionné, emplacement, attribution et rôle de la source
  (notice officielle, synthèse AnaMu, comparateur externe, etc.).
- scope : théorie, tradition, pratique, œuvre, version, réalisation,
  passage, voix, période et horloge pertinentes ; champs inconnus admis.
- epistemic_kind : encoded_observation, derived_observation,
  documented_fact, convention, hypothesis, interpretation,
  perceptual_judgment ou open_question.
- review_state : extracted_unreviewed, assistant_source_checked,
  human_reviewed, contested, deprecated et marqueur séparé
  requires_revisit ; aucun score de confiance implicite.
- conditions / exceptions : les conditions et le cadre appartiennent
  à l'assertion, pas à un concept global supposé universel.
- supports, challenges, derived_from : chaînes vérifiables et
  dépendances de version, pas des citations décoratives.

**Une source peut annoncer un domaine sans enseigner une règle détaillée.**
**Une interprétation possible ne devient jamais une observation encodée.**
Une preuve utilisée par deux chemins garde la même identité et ne compte pas
comme deux confirmations indépendantes.

## 3. Contrat de voie de preuve ET/OU

Une opération décrit plusieurs **routes alternatives** (any_of). Chaque
route décrit une **conjonction d'exigences** (all_of), la conclusion maximale
que cette route peut soutenir et ses limites.

Exemple de contrat de planification — pas un détecteur déjà implémenté :

~~~json
{
  "id": "operation:suspension-voice-history",
  "question": "La note est-elle retenue entre préparation et dissonance ?",
  "scope": "passage_et_voix_candidates",
  "any_of": [
    {
      "id": "score_route",
      "all_of": ["score_with_notated_ties", "verified_voice_identity", "stylistic_framework"],
      "max_produces": ["suspension_interpretation_candidate"]
    },
    {
      "id": "midi_annotated_route",
      "all_of": ["midi_note_events_verified", "verified_voice_identity", "stylistic_framework"],
      "max_produces": ["timing_and_voice_suspension_candidate"]
    }
  ],
  "cannot_establish": ["perceived_continuity_without_audio",
                       "renaissance_fourth_phase_without_context"],
  "revisit_when": ["voice_identity_changed", "new_score_reading",
                   "stylistic_framework_changed"]
}
~~~

Une voie peut être **prête** alors qu'une autre est bloquée. Une route moins
riche ne produit pas silencieusement la même assertion qu'une partition
avec voix identifiées. Les données manquantes constituent une sortie du plan,
pas une preuve d'absence du phénomène.

Le statut d'une tâche n'est jamais une affirmation que l'opération a été
exécutée ni que la connaissance a été appliquée correctement.

## 4. Relations et différents ordres

Relations musicales : precedes, overlaps, part_of, elaborates,
transforms_into, contrasts_with, alternative_to. Elles parlent de
réalisations ou de sens avec une portée explicite.

Relations de connaissances : is_a, applies_under,
historically_attested_in, supports, challenges. La taxonomie
n'impose pas l'ordre d'exécution.

Relations opérationnelles : requires_evidence (strict),
benefits_from (facultatif), revisits_on (révision).

Relation pédagogique : pedagogically_requires. Elle ne devient
jamais une dépendance automatique d'analyse d'œuvre.

Quatre ordres sont distincts : **temps de la musique**, **hiérarchie
interprétative**, **progression pédagogique**, **plan d'examen**.
Une préparation précède sa résolution dans l'œuvre, mais sa détection
peut dépendre d'une lecture des voix obtenue plus tard.

Des concepts comme cadence et phrase peuvent se rééclairer ; le graphe
de savoir n'est pas nécessairement acyclique. Une conclusion retenue
doit toutefois avoir un appui **extérieur** à une boucle de justification.
Les reprises sont bornées, versionnées et explicables.

## 5. Calibration contrastée avant extraction massive

| Cas | Fiches sources consultées | Problème discriminant et preuve manquante |
| --- | --- | --- |
| Verticale ambiguë | CM-211, CM-212, MUTH-251, MTE-1221 | Même figure, fonctions diverses ; besoin de basse, graphie, suite et style |
| Retard contextualisé | MUTH-202 | La perfection Renaissance peut suivre la résolution ; la verticale seule ignore l'histoire des voix |
| Identité dramatique | OCOMP-491 | Retour musical ≠ identité documentée de personnage ; besoin de scène et texte |
| Électroacoustique | MTE-3300 | Analyse d'objet sonore sans imposer note–accord–cadence ; besoin d'audio et écoute |
| Hiérarchie de réduction | MUTH-528 | Note longue ≠ structurelle ; graphes et arguments concurrents nécessaires |
| Pratique culturelle | MUL-3314, MUL-6262-H27 | Ressemblance rythmique ≠ provenance ; documents de pratiques et comparaisons |
| Percussion | CM-343 | Événement GM ≠ effectif, baguette, amortissement ni résonance réelle |
| Musique de jeu | MUS-2327 | Retour de thème ≠ boucle intégrale ni déclenchement ; chronologie de jeu nécessaire |

Ce sont des **familles de calibration**, non huit capacités déjà livrées.
Leur rôle est de faire apparaître les failles d'un schéma centré uniquement
sur l'harmonie tonale.

## 6. Couverture : cinq dimensions séparées

1. indexed : la source figure dans l'édition et son empreinte est connue.
2. material_delimited : les unités sont identifiées, les omissions visibles.
3. semantic_extracted : mentions, propositions, contre-cas et qualifications relevés.
4. reconciled_placed : sens, conditions, relations et rôle analytique revus.
5. operationally_supported : des opérations produisent effectivement
   des observations et, séparément, des conclusions évaluées.

Une matière peut être complète aux niveaux 1–3 et ne posséder aucun algorithme.
Un savoir historique conserve un rôle, même si sa voie opérationnelle
est documentaire et humaine. Ne pas calculer un pourcentage unique de
« compréhension » en mélangeant ces états.

## 7. Critères d'entrée en P4/P5

Premier parcours « fonction d'une verticale » :
- deux lectures rivales, non fusionnées ;
- exigences de preuve ET/OU avec portées explicites ;
- provenance de la théorie et de l'exemple ;
- tâches prêtes et bloquées, chacune avec explication ;
- interdiction de conclure fonction ou cadence depuis les seules classes ;
- révision si une graphie fiable ou une autre continuation apparaît.

Premier parcours non harmonique : percussion ou musique interactive,
avec résultat **partiellement bloqué** plutôt qu'un faux diagnostic.
Le même ordonnanceur doit respecter leurs routes, sans exiger de MIDI
quand ce média n'est pas pertinent.

La mise en production d'un véritable planificateur et la validation
musicologique des conclusions sont ultérieures à ce contrat.
