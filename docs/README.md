# Documentation AnaMu — point d'entrée

## Sources normatives (projet actuel)

**Si vous êtes un nouvel agent**, commencez par le
[contrat de reprise à la racine](../AGENTS.md). Le résultat voulu est une
**base de connaissances musicales académiques commune** qui alimente
une analyse experte ; composer ne viendra qu'ensuite.

1. **[OBJECTIVES.md](OBJECTIVES.md)** — objectif, périmètre, garanties,
   types de preuve et critères de sortie G0–G6.
2. **[knowledge-base.md](knowledge-base.md)** — **patrimoine académique
   unifié** et contrat de passage des cours aux concepts puis à l'analyse.
3. **[university-curriculum.md](university-curriculum.md)** — trois cursus
   officiels, méthode de revue cours par cours et verrou avant composition.
4. **[todo-university-coverage.md](todo-university-coverage.md)** — **unique
   liste de priorités à cocher**, sans compétences déclarées achevées.
5. **[roadmap.md](roadmap.md)** — acquis mesurés et limites, sans deuxième TODO.
6. **[music-grammar-research-program.md](music-grammar-research-program.md)**
   — ontologie académique, théories, opérateurs, choix de représentation.
7. **[orchestral-corpus-audit.md](orchestral-corpus-audit.md)** — corpus,
   provenance, licences, discordances MIDI ↔ MusicXML.
8. **[research-evidence-gates.md](research-evidence-gates.md)** — contrats
   scientifiques et impossibilités de certaines cibles de recherche.
9. **[composition-grammar.md](composition-grammar.md)** — contre-épreuves
   analytiques d'orchestration ; résultats mesurés et critères d'écoute.

**Audits de cursus en cours :**
[UdeM Composition A26](udem-curriculum-a26-audit.md),
avec [inventaire structuré](data/udem-composition-a26.json) ;
[McGill Composition 2026](mcgill-curriculum-2026-audit.md),
avec [relevé de ses exigences](data/mcgill-composition-2026.json) ;
[Berklee Composition 2026F](berklee-curriculum-2026f-audit.md),
avec [grille officielle structurée](data/berklee-composition-2026f.json).
Les relevés des codes/crédits ne sont pas des plans de cours complets et
ne ferment aucune case du TODO.

**Élargissement du périmètre de connaissance :**
[cours recommandés et majeures voisines](optional-knowledge-audit.md),
avec [registre des 30 pistes et sources](data/optional-knowledge-seeds-2026.json).
Les cours voisins ne sont pas présumés admissibles aux options du diplôme
Composition ; leur contenu reste à auditer avant toute validation.

**Ordre de priorité en cas de contradiction :** observations vérifiées et
tests pour le constat > `OBJECTIVES.md` pour le but > `knowledge-base.md`
pour le patrimoine attendu > référentiel universitaire pour le périmètre >
TODO pour les travaux à accomplir > `roadmap.md` pour
l'état des prototypes > spécifications pour les hypothèses. Aucun essai
historique ne modifie silencieusement le cap.

## Études empiriques utiles à la grammaire (`studies/`)

Elles servent de référence scientifique et de contre-épreuve ; ce **ne sont
pas** des validations de la grammaire intégrée :

- [Cadences expertisées DCML](studies/dcml-cadence-study.md)
- [Attentes humaines Cuddy–Lunney](studies/cudlun-human-expectancy-study.md)
- [Contre-épreuve Schellenberg](studies/schellenberg-external-transfer-study.md)
- [Surprise humaine Manzara](studies/manzara-cross-target-study.md)
- [IDyOM précalculé, comparaison](studies/idyom-archived-probe-comparison.md)
- [Audit MEX 2026](studies/mex-2026-source-audit.md)

Les protocoles de ces études restent utiles comme **contrôles indépendants**
des mécanismes de motifs, d'harmonie, d'attentes et de segmentation ; ils ne
deviennent pas automatiquement des fonctionnalités G2/G3.
