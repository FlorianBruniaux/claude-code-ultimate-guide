# GenAI Days Nantes: Emmanuel Sciara's conference account

Reviewed November 19, 2026. Score: **3/5**, useful attributed examples for existing pages, with no benchmark claim. The integration was requested by the author of this guide. Technical review is recorded separately from human publication approval.

## Source boundary

Emmanuel Sciara, *Retour sur la conférence GenAI Days Nantes 2026*, dated November 19, 2026. The account reports talks by Tristan Fransen (Pennylane), Charli Idrac (Brevo), Nicolas Martignole (Back Market), and Jean-Yves Simon (Mirakl), among others. The original article URL has not been verified. The [conference programme](https://genai-days-nantes.com/) identifies speakers and subjects, not the implementations or performance figures. No talk recording, slide deck, implementation, or evaluation dataset was checked for these additions.

Treat the article as a secondhand practitioner account. It motivates patterns worth testing. It does not establish causality, comparative accuracy, production reliability, or productivity gains. The integration omits the throughput and productivity figures whose measurement conditions are unavailable. The reported 40-team champion programme is retained as organisational context, attributed to Martignole through Sciara.

## Decisions

| Case | Placement | Contribution and boundary |
| --- | --- | --- |
| Pennylane | [Agent evaluation](../../guide/roles/agent-evaluation.md#criterion-specific-judges-and-human-calibration) | Small judges per criterion, disagreement inspection and actionable aggregation. No demonstrated superiority over a larger judge, no inference that a vote removes shared bias. |
| Back Market | [Adoption approaches](../../guide/roles/adoption-approaches.md#back-market-champions-and-role-specific-support) | Champions and role-specific training as a situated voluntary-adoption example, without a mandatory-rollout comparison. |
| Brevo | [Support workflow](../../guide/workflows/support-csm-agent.md#brevo-explicit-procedures-before-open-ended-routing) | Explicit support procedures and fixed data retrieval, distinct from the separate staff-built tooling project. No claim that MCP intrinsically adds randomness. |

Mirakl's product-investment example is integrated in the portfolio's existing bilingual organisational draft. It does not require another Guide page.

## French translation of the Pennylane addition

### Évaluateurs spécialisés par critère et calibration humaine

Un juge plus gros est une option. Dans « Retour sur la conférence GenAI Days Nantes 2026 », publié le 19 novembre 2026, Emmanuel Sciara rapporte le dispositif décrit par Tristan Fransen chez Pennylane : de petits évaluateurs prennent chacun un critère, comme le respect des consignes ou les signes d’insatisfaction. Le récit décrit aussi, lorsque les données manquent, un vote d’évaluateurs paramétrés différemment sur un même critère, puis une agrégation nocturne qui produit une liste de corrections. C’est un récit de praticien rapporté par un tiers, sans comparaison établissant que ces petits juges dépassent un juge plus gros.

Pour tester cette variante, conserver séparément le résultat de l’agent, sa trace d’actions, les signaux d’expérience utilisateur et le verdict du juge. Comparer un juge unique et des juges spécialisés sur les mêmes cas annotés indépendamment. Relever les fausses acceptations, les faux rejets, le coût et la latence par critère. Examiner les désaccords avec les annotations humaines avant de modifier un juge ou sa grille, puis évaluer la modification sur des cas réservés.

Une réponse copiée peut indiquer un usage et des reformulations répétées une friction. Aucun de ces signaux n’établit la justesse. Les pouces peuvent révéler des désaccords, mais leur sélection et les cas sans retour limitent la calibration. L’agrégation ne démontre ni l’indépendance des erreurs ni la disparition d’un biais partagé. Un vote sur un critère reste distinct de l’autorité d’accepter un changement ou de le publier.

This translates the added section only. It is not a French translation of the complete Agent evaluation chapter. The full-guide translation registry is unchanged because its tracked English source was not modified.

## Technical review

A separate technical-writer agent confirmed the 3/5 score for selective integration. Its review narrowed the Back Market contribution-file passage to an invitation, without claiming adoption, and restored the French workflow article’s explicit distinction between architectural trade-offs and capability levels. The changes were applied. This was a documentary review, not an experiment or human publication approval.
