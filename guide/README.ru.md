---
title: "Документация руководства (Guide Documentation)"
description: "Индекс всех основных файлов руководства по освоению Claude Code"
tags: [guide, reference, russian]
---

# Документация руководства по Claude Code

Основная документация для глубокого освоения Claude Code, структурированная по темам.

---

## Начало работы (Getting started)

| Файл | Описание | Время |
|------|----------|-------|
| [**learning-path/**](./learning-path/README.ru.md) | **Структурированная траектория из 7 модулей** для новичков: Установка, Базовый цикл, Память, Агенты, Навыки (Skills), Хуки, Продвинутые паттерны | 8–11 часов |
| [core/ai-concept-boundaries.md](./core/ai-concept-boundaries.md) | Семь практических концептуальных различий, примеры из репозитория и сценарии на понимание | В своем темпе |
| [learning-path/01-installation.ru.md](./learning-path/01-installation.ru.md) | Модуль 01: Установка Claude Code и проверка работоспособности | 15 мин |
| [learning-path/02-core-loop.ru.md](./learning-path/02-core-loop.ru.md) | Модуль 02: Понимание цикла взаимодействия и контекста | 45 мин |
| [learning-path/03-memory.ru.md](./learning-path/03-memory.ru.md) | Модуль 03: Создание CLAUDE.md и настройка памяти | 1 час |
| [learning-path/04-agents.ru.md](./learning-path/04-agents.ru.md) | Модуль 04: Создание специализированных агентов | 1.5 часа |
| [learning-path/05-skills.ru.md](./learning-path/05-skills.ru.md) | Модуль 05: Создание переиспользуемых навыков | 1.5 часа |
| [learning-path/06-hooks.ru.md](./learning-path/06-hooks.ru.md) | Модуль 06: Создание автоматизирующих хуков | 1 час |
| [learning-path/07-advanced.ru.md](./learning-path/07-advanced.ru.md) | Модуль 07: Мульти-агентная оркестрация | 2–3 часа |

---

## Базовый справочник (Core reference)

| Файл | Описание | Время |
|------|----------|-------|
| [ultimate-guide.md](./ultimate-guide.md) | Полный канонический справочник по всем возможностям Claude Code (EN) | ~3 часа |
| [ultimate-guide.fr.md](./ultimate-guide.fr.md) | Полный справочник на французском языке (FR) | ~3 часа |
| [cheatsheet.ru.md](./cheatsheet.ru.md) | **Шпаргалка на русском языке**: ежедневный компактный справочник | 5 мин |
| [cheatsheet.md](./cheatsheet.md) | Ежедневная шпаргалка на английском языке | 5 мин |
| [core/glossary.ru.md](./core/glossary.ru.md) | **Глоссарий (RU)**: терминология Claude Code и агентных систем (со ссылками на главы) | 5 мин |
| [core/tools-reference.ru.md](./core/tools-reference.ru.md) | **Справочник инструментов (RU)**: все 40 встроенных инструментов, синтаксис правил разрешений | 20 мин |
| [core/computer-use.ru.md](./core/computer-use.ru.md) | **Computer Use (RU)**: границы разрешений, безопасные процедуры и проверка | 12 мин |
| [core/translations.md](./core/translations.md) | **Управление переводами и языками**: статус, коммиты источников, официальные и комьюнити-версии | 5 мин |
| [cowork.md](./cowork.md) | Claude Cowork: десктопный агентный инструмент для нетехнических специалистов | 10 мин |
| [core/architecture.md](./core/architecture.md) | Как Claude Code устроен изнутри: мастер-цикл, инструменты, контекст | 25 мин |
| [core/computer-use.md](./core/computer-use.md) | **Computer Use**: границы разрешений, порядок отката, безопасные процедуры и проверка | 12 мин |
| [core/agent-harness.md](./core/agent-harness.md) | **Agent Harness Engineering**: компоненты рантайма, горизонты циклов, безопасность, оптимизация обвязки | 35 мин |
| [core/loop-graph-engineering.md](./core/loop-graph-engineering.md) | **Loop & Graph Engineering**: замкнутые циклы обратной связи, исполняемые графы воркфлоу, персистентное состояние | 25 мин |
| [core/ai-design-patterns.md](./core/ai-design-patterns.md) | **AI Design Patterns**: паттерны GoF, интеграции и отказоустойчивости в преломлении к механизмам Claude Code | 20 мин |
| [core/tools-reference.md](./core/tools-reference.md) | **Полный справочник инструментов**: все 40 встроенных инструментов, синтаксис правил разрешений, поведение Bash/Edit/Glob/WebFetch | 20 мин |
| [core/hooks-events-reference.md](./core/hooks-events-reference.md) | **Полный справочник хуков**: все 33 события жизненного цикла, схемы входных данных, форматы решений и таймауты | 15 мин |
| [core/settings-reference.md](./core/settings-reference.md) | **Полный справочник settings.json**: все подтвержденные параметры и переменные окружения | 15 мин |
| [core/methodologies.md](./core/methodologies.md) | Справочник по 15 методологиям разработки (TDD, SDD, BDD и др.) | 20 мин |
| [core/visual-reference.md](./core/visual-reference.md) | Визуальная шпаргалка: ASCII-диаграммы ключевых концепций | 5 мин |
| [core/claude-code-releases.md](./core/claude-code-releases.md) | Официальная история релизов Claude Code в сжатом виде | 10 мин |
| [core/known-issues.md](./core/known-issues.md) | **Трекер критических багов**: проблемы безопасности, расход токенов, подтвержденные баги | 15 мин |
| [core/context-engineering.md](./core/context-engineering.md) | **Контекстная инженерия**: бюджет токенов, модульная архитектура, пайплайн ACE, метрики качества | 25 мин |
| [core/memory-systems.md](./core/memory-systems.md) | **Системы памяти**: нативный стек (CLAUDE.md, Auto Memory), межсессионные инструменты (claude-mem), риски и блок-схема выбора | 30 мин |
| [core/glossary.md](./core/glossary.md) | **Глоссарий**: терминология Claude Code и агентных систем (41 термин со ссылками на главы) | 5 мин |
| [core/community-patterns.md](./core/community-patterns.md) | **Паттерны сообщества**: около 130 понятий и терминов ИИ-инженерии, введенных комьюнити | 10 мин |
| [core/skill-design-patterns.md](./core/skill-design-patterns.md) | **Паттерны проектирования навыков (Skills)**: архитектура надежных и экономных по токенам навыков | 20 мин |
| [diagrams/](./diagrams/) | **Серия визуальных диаграмм**: 53 интерактивные диаграммы Mermaid с ASCII-версиями | 15 мин |

---

## Визуальные схемы и диаграммы (Visual diagrams)

**53 интерактивные диаграммы Mermaid** в 12 тематических файлах с нативным рендерингом на GitHub и текстовыми ASCII-версиями. См. [diagrams/README.md](./diagrams/README.md).

| Файл | Диаграмм | Темы |
|------|:--------:|------|
| [diagrams/01-foundations.md](./diagrams/01-foundations.md) | 4 | 4-уровневая модель, конвейер воркфлоу, дерево решений, режимы разрешений |
| [diagrams/02-context-and-sessions.md](./diagrams/02-context-and-sessions.md) | 4 | Зоны контекста, иерархия памяти, телепортация сессий, свежий контекст |
| [diagrams/03-configuration-system.md](./diagrams/03-configuration-system.md) | 4 | Приоритет конфигураций, skills vs commands vs agents, жизненный цикл агента, хуки |
| [diagrams/04-architecture-internals.md](./diagrams/04-architecture-internals.md) | 5 | Мастер-цикл, категории инструментов, сборка системного промпта, изоляция подагентов |
| [diagrams/05-mcp-ecosystem.md](./diagrams/05-mcp-ecosystem.md) | 4 | Карта экосистемы MCP, архитектура MCP, атака rug pull, иерархия настроек |
| [diagrams/06-development-workflows.md](./diagrams/06-development-workflows.md) | 6 | Цикл TDD, конвейер spec-first, plan-driven, итеративное улучшение |
| [diagrams/07-multi-agent-patterns.md](./diagrams/07-multi-agent-patterns.md) | 6 | Топологии агентов, worktree, dual-instance, горизонтальное масштабирование |
| [diagrams/08-security-and-production.md](./diagrams/08-security-and-production.md) | 4 | 3-уровневая защита, выбор песочницы, парадокс верификации, пайплайн CI/CD |
| [diagrams/09-cost-and-optimization.md](./diagrams/09-cost-and-optimization.md) | 4 | Выбор моделей, оптимизация расходов, уровни подписок, сокращение токенов |
| [diagrams/10-adoption-and-learning.md](./diagrams/10-adoption-and-learning.md) | 4 | Пути онбординга, протокол UVAL, калибровка доверия |
| [diagrams/11-context-engineering.md](./diagrams/11-context-engineering.md) | 4 | 3-уровневая система контекста, деградация следования инструкциям, модульность |
| [diagrams/12-enterprise-governance.md](./diagrams/12-enterprise-governance.md) | 4 | Уровни рисков управления, процесс согласования MCP, классификация данных |

---

## Безопасность (Security)

| Файл | Описание | Время |
|------|----------|-------|
| [security/security-hardening.md](./security/security-hardening.md) | Угрозы безопасности, аудит MCP, защита от prompt injection | 25 мин |
| [security/sandbox-isolation.md](./security/sandbox-isolation.md) | Песочницы Docker, облачные среды, сценарии безопасной автономии | 10 мин |
| [security/sandbox-native.md](./security/sandbox-native.md) | Нативная песочница Claude Code: конфигурация и модель безопасности | 10 мин |
| [security/production-safety.md](./security/production-safety.md) | Безопасность в продакшене: защитные барьеры, гейты ревью, откат | 15 мин |
| [security/data-privacy.md](./security/data-privacy.md) | Хранение данных и руководство по конфиденциальности | 10 мин |
| [security/agentic-pentesting.md](./security/agentic-pentesting.md) | Пентэстинг с ИИ: DarkMoon и Strix, границы выполнения, протокол оценки | Справочно |
| [security/enterprise-governance.md](./security/enterprise-governance.md) | **Корпоративное управление**: регламенты использования, согласование MCP, уровни рисков | 25 мин |

---

## Экосистема (Ecosystem)

| Файл | Описание | Время |
|------|----------|-------|
| [ecosystem/ai-ecosystem.md](./ecosystem/ai-ecosystem.md) | Вспомогательные ИИ-инструменты (Perplexity, Gemini, Kimi, NotebookLM, TTS) | 30 мин |
| [ecosystem/plugin-distribution.md](./ecosystem/plugin-distribution.md) | **Дистрибуция плагинов**: границы пакетов, доверие к маркетплейсам | 15 мин |
| [ecosystem/agentic-tools.md](./ecosystem/agentic-tools.md) | **Сравнение агентных инструментов**: Hermes Agent, Codex CLI, Aider, Devin, SWE-agent, CrewAI, LangGraph | 20 мин |
| [ecosystem/mcp-vs-cli.md](./ecosystem/mcp-vs-cli.md) | **Выбор между MCP и CLI**: когда использовать MCP-серверы, а когда консольные утилиты | 15 мин |
| [ecosystem/claude-code-guide-mcp.md](./ecosystem/claude-code-guide-mcp.md) | **Технический справочник MCP-сервера руководства**: установка, возможности, архитектура | 12 мин |
| [ecosystem/agent-harness-landscape.md](./ecosystem/agent-harness-landscape.md) | **Карта агентных систем**: строгие рантаймы, оркестраторы, исследовательские системы | 10 мин |
| [ecosystem/mcp-servers-ecosystem.md](./ecosystem/mcp-servers-ecosystem.md) | **MCP-серверы сообщества**: проверенные серверы (Playwright, Semgrep, K8s и др.) | 25 мин |
| [ecosystem/third-party-tools.md](./ecosystem/third-party-tools.md) | **Инструменты сообщества**: графические интерфейсы, TUI, менеджеры настроек, трекеры токенов | 15 мин |
| [ecosystem/context-engineering-tools.md](./ecosystem/context-engineering-tools.md) | **Оптимизация токенов и контекста**: сжатие вывода (RTK, Headroom), сжатие промптов, шлюзы | 20 мин |
| [ecosystem/team-knowledge-base.md](./ecosystem/team-knowledge-base.md) | **Инфраструктура базы знаний команды**: 3-уровневый фреймворк, MCP-коннекторы, RAG | 18 мин |
| [ecosystem/local-vs-cloud-inference.md](./ecosystem/local-vs-cloud-inference.md) | **Экономика локального и облачного инференса**: расчет конфигураций оборудования, GPU-аренда, TCO | 20 мин |

---

## Роли и внедрение (Roles & Adoption)

| Файл | Описание | Время |
|------|----------|-------|
| [roles/ai-roles.md](./roles/ai-roles.md) | Карта специализаций и ролей в эпоху ИИ, конвергенция малых команд, траектории карьеры | 25 мин |
| [roles/adoption-approaches.md](./roles/adoption-approaches.md) | Стратегии внедрения инструментов разработки с ИИ в инженерных командах | 15 мин |
| [roles/learning-with-ai.md](./roles/learning-with-ai.md) | Руководство для начинающих разработчиков: как использовать ИИ без деградации собственных навыков | 15 мин |
| [roles/agent-evaluation.md](./roles/agent-evaluation.md) | **Метрики качества агентов**: измерение эффективности кастомных агентов с хуками и тестами | 20 мин |

---

## Эксплуатация (Operations)

| Файл | Описание | Время |
|------|----------|-------|
| [ops/devops-sre.md](./ops/devops-sre.md) | Фреймворк FIRE для диагностики инфраструктуры и реагирования на инциденты | 30 мин |
| [ops/observability.md](./ops/observability.md) | Мониторинг сессий и отслеживание затрат | 15 мин |
| [ops/api-gateway.md](./ops/api-gateway.md) | **API-шлюзы**: разделение поведения шлюза Claude apps и сторонних прокси (LiteLLM, Portkey) | 15 мин |
| [ops/ai-traceability.md](./ops/ai-traceability.md) | Атрибуция ИИ-изменений, политики раскрытия, git-ai, соответствие нормативам | 20 мин |
| [ops/team-metrics.md](./ops/team-metrics.md) | **Метрики команды при разработке с ИИ**: DORA, SPACE, DX Core 4 | 20 мин |
| [ops/ai-unit-economics.md](./ops/ai-unit-economics.md) | **Юнит-экономика ИИ**: декомпозиция затрат на задачу, рычаги экономии | 15 мин |
| [ops/subscription-strategy.md](./ops/subscription-strategy.md) | **Стратегия подписок в масштабе команды**: портфели Claude, Codex, Copilot, Cursor | 20 мин |
| [ops/ai-finops.md](./ops/ai-finops.md) | **AI FinOps**: три режима затрат (квота, токены, мощности), цикл Inform-Optimize-Operate | 12 мин |
| [ops/llm-market-snapshot.md](./ops/llm-market-snapshot.md) | **Обзор рынка LLM**: актуальные цены, лимиты, бенчмарки | 20 мин |

---

## Практические сценарии (Workflows)

| Файл | Описание |
|------|----------|
| [workflows/tdd-with-claude.md](./workflows/tdd-with-claude.md) | Разработка через тестирование (TDD) с Claude Code |
| [workflows/spec-first.md](./workflows/spec-first.md) | Разработка на основе спецификаций (Spec-First / SDD) |
| [workflows/plan-driven.md](./workflows/plan-driven.md) | Эффективная работа в режиме планирования (/plan) |
| [workflows/iterative-refinement.md](./workflows/iterative-refinement.md) | Итеративные циклы доработки и улучшения |
| [workflows/best-of-n.md](./workflows/best-of-n.md) | Генерация независимых вариантов решения с оценкой по единой рубрике |
| [workflows/task-management.md](./workflows/task-management.md) | Межсессионное управление задачами, миграция с TodoWrite на Tasks API |
| [workflows/agent-teams.md](./workflows/agent-teams.md) | Оркестрация мульти-агентных команд для решения масштабных задач |
| [workflows/agent-teams-quick-start.md](./workflows/agent-teams-quick-start.md) | Быстрый старт по организации команд агентов |
| [workflows/dynamic-workflows.md](./workflows/dynamic-workflows.md) | Пайплайны на JavaScript: детерминированный поток управления, параллелизация |
| [workflows/dual-instance-planning.md](./workflows/dual-instance-planning.md) | Планирование на двух инстансах: Opus строит план, Sonnet реализует |
| [workflows/event-driven-agents.md](./workflows/event-driven-agents.md) | Паттерны координации агентов на основе событий |
| [workflows/github-actions.md](./workflows/github-actions.md) | Пошаговая интеграция claude-code-action в GitHub Actions |
| [workflows/reviewable-agent-changes.md](./workflows/reviewable-agent-changes.md) | Как делать код от ИИ-агентов удобным для ревью коллегами |
| [workflows/code-review.md](./workflows/code-review.md) | Автоматизированное мульти-агентное ревью пулл-реквестов |
| [workflows/production-reliability.md](./workflows/production-reliability.md) | Паттерны надежности: circuit breakers, эскалация, graceful degradation |
| [workflows/design-to-code.md](./workflows/design-to-code.md) | Превращение макетов Figma и вайрфреймов в рабочий код |
| [workflows/exploration-workflow.md](./workflows/exploration-workflow.md) | Систематическое исследование незнакомых кодовых баз |
| [workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md) | Мастерство поиска по коду: связка rg, grepai, Serena и ast-grep |
| [workflows/team-ai-instructions.md](./workflows/team-ai-instructions.md) | Масштабирование правил CLAUDE.md на команду разработчиков |

---

## Рекомендуемый порядок чтения

1. **Новичкам**: начните с раздела Quick Start в `ultimate-guide.md` или модуля [learning-path/](./learning-path/README.md)
2. **Для ежедневной работы**: держите под рукой [шпаргалку cheatsheet.ru.md](./cheatsheet.ru.md)
3. **Тимлидам**: прочтите `roles/adoption-approaches.md` для стратегии внедрения
4. **Инженерам по безопасности**: изучите `security/security-hardening.md` и `security/sandbox-isolation.md`
5. **Глубокая архитектура**: разберите `core/architecture.md` и визуальные схемы в `diagrams/`

---

*Возврат к [основному README](../README.ru.md)*
