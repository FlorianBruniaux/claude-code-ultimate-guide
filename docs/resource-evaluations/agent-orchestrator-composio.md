# Évaluation de ressource : Agent Orchestrator (AO)

**Source** : [OrchestratorInc/agent-orchestrator](https://github.com/OrchestratorInc/agent-orchestrator), précédemment référencé sous ComposioHQ puis AgentWrapper.
**Évaluation initiale** : 8 juillet 2026. **Essai avec Codex** : 27 octobre 2026.
**Décision** : conserver la mention existante et le score éditorial **3/5**. Le suivi des PR et la notification CI sont vérifiés sur un scénario borné; la boucle autonome revue → correction → CI verte ne l'est pas.

Ce score mesure l'intérêt pour le guide, pas la fiabilité du produit. Cette réévaluation remplace les comparaisons de juillet fondées sur le nombre d'agents, les étoiles ou les issues, qui ne constituent pas une mesure de maturité ou de productivité.

## Fonctionnement et périmètre

AO supervise des agents de code existants. Son [architecture documentée](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.6/docs/architecture.md) associe un daemon Go, des clients desktop et CLI, des sessions et worktrees Git, puis des observateurs de l'activité de l'agent et de l'état des PR. Les faits collectés alimentent les statuts affichés et les messages transmis aux sessions. La séparation des worktrees ne confine pas les processus.

L'essai a utilisé l'archive officielle macOS arm64 [v0.14.6](https://github.com/OrchestratorInc/agent-orchestrator/releases/tag/v0.14.6), Codex CLI 0.159.2 et une seule session terminal, via la CLI et l'API locale d'AO. Le modèle était celui de la configuration Codex de l'évaluateur; aucun comparatif de modèles n'a été effectué. Le daemon embarqué affichait `dev` : l'identification de la release repose sur l'archive téléchargée et son empreinte vérifiée, pas sur cette chaîne de version.

Le dépôt synthétique et la PR utilisés sont privés. Les observations ci-dessous sont celles de l'évaluateur, appuyées par les messages conservés, les réponses AO/GitHub, les annotations de checks et les résultats de tests. Ces preuves ne sont pas publiquement consultables; les liens upstream expliquent le mécanisme et ne constituent pas une reproduction indépendante du pilote.

## Scénario et résultats observés

1. Créer une session Codex dans un worktree AO, sur deux branches dédiées à l'essai. Les deux tests initiaux d'une fonction Python de création de slug passent.
2. Ajouter un troisième test volontairement rouge sur les espaces multiples et tabulations, publier une PR et la rattacher explicitement à la session AO.
3. Observer la notification CI reçue par Codex, puis sa correction de l'implémentation. Les trois tests passent localement.
4. Publier un commentaire inline synthétique demandant de rejeter les titres vides ou composés uniquement de blancs avec `ValueError` et d'ajouter deux tests.
5. Après l'absence de livraison automatique du commentaire, relancer manuellement Codex sans recopier le contenu de la revue. L'agent lit le commentaire sur GitHub, démontre l'échec des deux nouveaux tests, corrige, puis pousse. Les cinq tests passent, vérifiés à nouveau par l'évaluateur.

| Capacité | Observation | Limite de preuve |
|---|---|---|
| Session et worktree Codex | Créés par AO | Une session seulement |
| Suivi PR, branche et commit | AO reflète la PR et le même SHA final que GitHub | Rattachement de la PR effectué explicitement |
| Notification CI vers Codex | Transmise automatiquement avec le job et son URL | Le contenu des logs n'a pas pu être récupéré |
| Correction du bug initial | Trois tests locaux passent après correction | Approbations nécessaires pour certaines opérations; aucun test distant exécuté |
| Détection de la revue | Commentaire ingéré avec fichier, ligne et fil non résolu | Commentaire de l'évaluateur, pas une revue indépendante |
| Livraison automatique de la revue | Non observée pendant plus de cinq minutes après ingestion | Commentaire arrivé pendant une approbation; pas de reprise constatée après retour au repos, ni après édition du commentaire |
| Correction demandée par la revue | Cinq tests locaux passent après relance manuelle | Ne valide pas le réveil automatique de l'agent |
| CI distante verte | **Bloquée** | GitHub indique un paiement en échec ou un plafond de dépenses à augmenter; le job ne démarre pas |

Le badge CI rouge n'était donc pas un résultat de test rouge. AO a envoyé un message invitant à corriger et pousser, accompagné d'une erreur `BlobNotFound` lors de la récupération des logs. L'évaluateur a dû lire les annotations GitHub pour identifier le blocage de compte et demander à Codex de ne pas multiplier les corrections pour cette cause. La correction du bug volontaire reste prouvée par les tests locaux, séparément.

La PR est restée ouverte, sans fusion; le fil de revue n'a pas été résolu. Le dernier commit poussé était correctement reflété par AO. Les agents et le daemon du pilote ont été arrêtés après collecte des preuves.

## Limites rencontrées et réglages d'adoption

- **Permissions Codex** : dans le [mapping de la release testée](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.6/backend/pkg/agentruntime/command.go#L198), le mode AO `default` passe `--dangerously-bypass-approvals-and-sandbox`. Le pilote a sélectionné `accept-edits` avant lancement et configuré séparément Codex en `workspace-write` avec approbations `on-request`. Ce choix a maintenu des interventions pour les lectures réseau, comptes rendus et push. Il ne faut pas interpréter `default` comme le maintien des protections habituelles de Codex.
- **Reprise de revue** : la [lifecycle](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.6/backend/internal/lifecycle/reactions.go#L146) diffère les notifications CI/revue pendant une attente de saisie. L'[observateur SCM](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.6/backend/internal/observe/scm/observer.go#L598) évite une nouvelle réaction lorsque les données observées n'ont pas changé. Ces chemins sont compatibles avec l'incident, mais sa cause exacte n'a pas été isolée. L'essai ne prouve pas que toutes les notifications de revue échouent.
- **Envoi manuel pendant une approbation** : une commande `ao send` a interrompu un compte rendu en attente et le début du message reçu était tronqué dans l'historique. Cet incident n'a pas fait l'objet d'une reproduction isolée permettant d'en attribuer entièrement la cause.
- **Installation macOS** : le premier contrôle de signature a échoué. Une nouvelle extraction avec `ditto` a passé les contrôles de signature et Gatekeeper a accepté l'application comme notarisée. La cause du premier échec n'a pas été isolée. Le [vérificateur upstream](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.6/frontend/scripts/verify-mac-artifact.sh) décrit la procédure de contrôle recommandée. Les vérifications réussies ont eu lieu après le lancement initial; aucune protection macOS n'a été désactivée.
- **Télémétrie** : la [documentation de la release](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.6/docs/telemetry.md) décrit des identifiants d'installation et de compte, dont le nom GitHub; elle ne qualifie pas les données de totalement anonymes. Les releases desktop activent la télémétrie distante, avec désactivation dans les réglages de confidentialité. Le pilote a désactivé les contrôles de télémétrie du daemon; aucune capture réseau exhaustive n'a vérifié l'absence d'émission.

Les hashes des fichiers globaux Codex de configuration, d'instructions et de hooks contrôlés sont restés identiques. Cette vérification limitée ne constitue pas un audit complet des effets sur le poste. L'interface graphique, les autres agents, plusieurs PR simultanées, les conflits Git, la reprise après redémarrage, les commentaires de bots, la fusion et la résolution des fils n'ont pas été testés.

## Apport et décision

**Apport vérifié** : réunir la PR, son commit, la CI et les fils de revue autour de la session, et transmettre un échec CI à Codex sans recopier manuellement cet événement. Aucune mesure de temps, de coût ou de productivité ne démontre un avantage sur Codex Desktop ou un autre outil.

L'[essai Escouade](./agent-workspace-cockpits.md#escouade) portait sur les dépendances entre tâches, la reprise et les tests avant livraison locale. AO a ici exercé le suivi GitHub. Les scénarios diffèrent : ils ne permettent pas de classer les produits. [Orca](./agent-workspace-cockpits.md#orca) reste une évaluation documentaire, sans essai runtime dans cette comparaison.

**Score maintenu : 3/5.** Conserver AO comme candidat pour le suivi de plusieurs PR, sans recommander un remplacement du fonctionnement existant. Avant adoption, refaire le scénario avec un runner disponible et exiger : un vrai échec de test distant, sa correction suivie d'une CI verte au bon SHA, puis un commentaire arrivé pendant une approbation et livré après déblocage sans relance manuelle.

La formule historique « deux retries CI puis escalade humaine » reste non établie par cet essai. Les limites de notifications de revue présentes dans le code ne prouvent pas cette politique de correction CI.

## Revue de l'évaluation

Un agent de revue technique distinct a confronté le texte aux preuves conservées et aux sources de la release. Il maintient le score de 3/5 et confirme les limites sur la CI, la relance manuelle et la confidentialité. Il a demandé de retirer l'attribution certaine du premier échec de signature à l'extraction : cette cause n'a pas été isolée. La correction est intégrée ci-dessus. Cette revue documentaire n'est pas une reproduction indépendante de l'essai.
