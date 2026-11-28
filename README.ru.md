# Полное руководство по Claude Code (Claude Code Ultimate Guide)

<table>
  <tr>
    <td width="64">
      <a href="https://www.florian.bruniaux.com/about/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide"><img src="https://cc.bruniaux.com/author.png" width="56" height="56" alt="Florian Bruniaux" /></a>
    </td>
    <td>
      <strong><a href="https://www.florian.bruniaux.com/about/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide">Florian BRUNIAUX</a></strong> &middot; Практикующий Fractional Chief AI Officer (CAIO)<br />
      Около 15 лет в разработке ПО, включая 8–10 лет технического лидерства &middot; <a href="https://www.florian.bruniaux.com/blog/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide">Блог &#8599;</a> &middot; <a href="https://www.florian.bruniaux.com/projects/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide">Проекты &#8599;</a>
      <br /><strong><a href="https://clauders.com/leaders/florian-bruniaux/">Официальный амбассадор сообщества Claude &middot; Париж &#8599;</a></strong>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://cc.bruniaux.com/"><img src="https://img.shields.io/badge/Интерактивный_гид-cc.bruniaux.com-ff6b35?style=for-the-badge" alt="Открыть интерактивное руководство" /></a>
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/Версия_руководства-v3.46.0-brightgreen?style=flat-square" alt="Версия руководства 3.46.0" /></a>
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/Обновлено-25_ноября_2026_·_v3.46.0-brightgreen?style=flat-square" alt="Обновлено 25 ноября 2026, версия руководства 3.46.0" /></a>
  <a href="https://creativecommons.org/licenses/by-sa/4.0/"><img src="https://img.shields.io/badge/Лицензия-CC_BY--SA_4.0-blue?style=flat-square" alt="Лицензия руководства: CC BY-SA 4.0" /></a>
  <a href="https://cc.bruniaux.com/mcp/"><img src="https://img.shields.io/badge/MCP-npx_ready-blueviolet?style=flat-square" alt="MCP-сервер доступен через npx" /></a>
  <a href="https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide"><img src="https://deepwiki.com/badge.svg" alt="Задать вопрос DeepWiki" /></a>
</p>

Освойте Claude Code, создавайте надежных агентов и безопасно масштабируйте их применение. Веб-сайт является основным интерфейсом для чтения и изучения. Этот репозиторий содержит канонические исходные тексты в Markdown, повторно используемые файлы, машиночитаемые индексы и историю изменений.

**Начните отсюда:** [выполните первую задачу онлайн](https://cc.bruniaux.com/guide/ultimate-guide/01-quick-start/) · [портал руководства](https://cc.bruniaux.com/guide/) · [полная карта сайта](https://cc.bruniaux.com/sitemap/) · [исходный текст в Markdown](./guide/ultimate-guide.md) · [шпаргалка на русском](./guide/cheatsheet.ru.md)

---

## Выберите следующий шаг

Таблица ниже сгенерирована из [`machine-readable/navigation.json`](./machine-readable/navigation.json). Тот же контракт формирует публичную карту сайта.

| Цель | Просмотр онлайн | Исходники в репозитории |
|---|---|---|
| **Старт** | [Портал руководства](https://cc.bruniaux.com/guide/) · [Быстрый старт](https://cc.bruniaux.com/guide/ultimate-guide/01-quick-start/) · [Траектории обучения](https://cc.bruniaux.com/learning/) · [Шпаргалка](https://cc.bruniaux.com/cheatsheet/) · [Роли в ИИ](https://cc.bruniaux.com/roles/) | [Шпаргалка (RU)](./guide/cheatsheet.ru.md) · [Траектория обучения](./guide/learning-path/README.md) · [AI Roles](./guide/roles/ai-roles.md) |
| **Создание** | [Agent Harness Engineering](https://cc.bruniaux.com/guide/agent-harness/) · [Loop & Graph Engineering](https://cc.bruniaux.com/guide/loop-graph-engineering/) · [Паттерны проектирования ИИ](https://cc.bruniaux.com/ai-design-patterns/) · [Контекстная инженерия](https://cc.bruniaux.com/context-engineering/) · [Системы памяти](https://cc.bruniaux.com/memory-systems/) · [Воркфлоу](https://cc.bruniaux.com/guide/workflows/) · [Методологии](https://cc.bruniaux.com/methodologies/) · [MCP или CLI?](https://cc.bruniaux.com/mcp-or-cli/) · [Примеры](https://cc.bruniaux.com/examples/) | [Архитектура](./guide/core/architecture.md) · [Инструменты](./guide/core/tools-reference.md) · [Примеры](./examples/) |
| **Масштаб** | [Безопасность](https://cc.bruniaux.com/security/) · [Корпоративное управление](https://cc.bruniaux.com/guide/enterprise-governance/) · [Наблюдаемость (Observability)](https://cc.bruniaux.com/guide/observability/) · [Метрики команды](https://cc.bruniaux.com/team-metrics/) · [Внедрение в команде](https://cc.bruniaux.com/guide/adoption-approaches/) · [AI FinOps](https://cc.bruniaux.com/finops/) · [Обзор рынка LLM](https://cc.bruniaux.com/guide/llm-market-snapshot/) · [Стратегия подписок](https://cc.bruniaux.com/guide/subscription-strategy/) · [Юнит-экономика ИИ](https://cc.bruniaux.com/guide/ai-unit-economics/) · [База знаний команды](https://cc.bruniaux.com/guide/team-knowledge-base/) · [API Gateway](https://cc.bruniaux.com/guide/api-gateway/) | [Security Hardening](./guide/security/security-hardening.md) · [Sandboxing](./guide/security/sandbox-isolation.md) |
| **Ресурсы** | [Центр ресурсов](https://cc.bruniaux.com/resources/) · [Загрузки](https://cc.bruniaux.com/downloads/) · [Шпаргалки](https://cc.bruniaux.com/cheatsheets/) · [Электронные книги](https://cc.bruniaux.com/whitepapers/) · [Диаграммы](https://cc.bruniaux.com/diagrams/) · [Экосистема](https://cc.bruniaux.com/ecosystem/) · [Сравнение](https://cc.bruniaux.com/compare/) · [Глоссарий](https://cc.bruniaux.com/guide/glossary/) · [FAQ](https://cc.bruniaux.com/faq/) · [MCP-сервер руководства](https://cc.bruniaux.com/mcp/) | [Глоссарий](./guide/core/glossary.md) · [Диаграммы](./guide/diagrams/) · [Шаблоны](./examples/) |
| **Обновления** | [Changelog руководства](https://cc.bruniaux.com/changelog/) · [Релизы Claude Code](https://cc.bruniaux.com/releases/) · [RSS-лента](https://cc.bruniaux.com/rss.xml) | [CHANGELOG.md](./CHANGELOG.md) · [Релизы](./guide/core/claude-code-releases.md) |

---

## Зачем создано это руководство

Официальная документация Claude Code объясняет возможности продукта. Это руководство связывает поведение продукта с инженерными решениями: что должно попадать в контекст, когда использовать агента вместо навыка (skill), как проверять сгенерированный результат и какие ограничения критически важны, когда инструмент используют не один разработчик, а целая команда.

| Потребность | С чего начать |
|---|---|
| Понять внутреннее устройство Claude Code | [Архитектура](./guide/core/architecture.md) и [Справочник инструментов](./guide/core/tools-reference.md) |
| Проектировать агентные системы | [Agent Harness Engineering](./guide/core/agent-harness.md), [Loop & Graph Engineering](./guide/core/loop-graph-engineering.md) и [AI Design Patterns](./guide/core/ai-design-patterns.md) |
| Структурировать разработку с помощью ИИ | [Методологии](./guide/core/methodologies.md) и [Практические руководства (Workflows)](./guide/workflows/) |
| Выстроить периметр безопасности | [Security Hardening](./guide/security/security-hardening.md) и [Изоляция песочницы (Sandbox)](./guide/security/sandbox-isolation.md) |
| Проверить свои знания | [Квиз на знание инструмента](https://cc.bruniaux.com/quiz/) и [Карточки-рекапы](https://cc.bruniaux.com/cheatsheets/) |

Руководство делает акцент на явных компромиссах и проверяемых процедурах. Там, где практические свидетельства пока неполны, соответствующая страница сохраняет это ограничение, а не выдает единственный воркфлоу за универсальный стандарт.

---

## Старт

### Установка Claude Code

Anthropic рекомендует использовать нативный установщик, который обновляется автоматически:

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

Альтернативные варианты без автообновления: `brew install --cask claude-code`, `winget install Anthropic.ClaudeCode` или `npm install -g @anthropic-ai/claude-code` (требуется Node.js 22+). См. [официальную страницу установки](https://code.claude.com/docs/en/setup).

Проверьте установку и авторизуйтесь:

```bash
claude --version
claude doctor
claude auth login
```

В главе [Быстрый старт (Quick Start)](./guide/ultimate-guide.md#1-quick-start-day-1) описаны альтернативные способы установки, аутентификация, обновления, режимы разрешений и типичные ошибки первого дня.

### Выполнение первой задачи

Откройте небольшой репозиторий с чистым состоянием Git, затем запустите Claude Code:

```bash
cd your-project
claude
```

Дайте Claude четко ограниченную задачу с указанием ожидаемого результата и способа проверки:

```text
Explain how this project runs its tests. Do not modify files.
Name the relevant commands and cite the files that define them.
```
*(Объясни, как в этом проекте запускаются тесты. Не изменяй файлы. Назови нужные команды и укажи файлы, где они определены).*

Перед тем как разрешать Claude редактировать код, добавьте файл инструкций `CLAUDE.md` на уровне проекта, зафиксировав команды и ограничения:

```markdown
# Project instructions

## Commands
- Test: `npm test`
- Lint: `npm run lint`

## Boundaries
- Do not edit generated files.
- Do not change dependencies without approval.
- Run the relevant tests before claiming completion.
```

Продолжайте с [первым рабочим процессом](./guide/ultimate-guide.md#12-first-workflow) или используйте [стартовые шаблоны CLAUDE.md](./examples/claude-md/).

### Выбор траектории обучения

| Ваша ситуация | Рекомендуемый маршрут |
|---|---|
| Новичок в Claude Code | [Траектория из 7 модулей](./guide/learning-path/README.md) |
| Уже используете CLI | [Ключевые концепции](./guide/ultimate-guide.md#2-core-concepts), затем [Контекстная инженерия](./guide/core/context-engineering.md) |
| Senior-разработчик / Tech Lead | [Методологии](./guide/core/methodologies.md), [Agent Harness Engineering](./guide/core/agent-harness.md), затем [Безопасность в продакшене](./guide/security/production-safety.md) |
| Engineering Manager / CTO | [Подходы к внедрению](./guide/roles/adoption-approaches.md), [Командные метрики](./guide/ops/team-metrics.md), затем [Стратегия подписок](./guide/ops/subscription-strategy.md) |
| Специалист по безопасности / Platform | [Security Hardening](./guide/security/security-hardening.md), [Enterprise Governance](./guide/security/enterprise-governance.md), затем [Observability](./guide/ops/observability.md) |
| Product Manager / Дизайнер | [Гид для продакт-менеджеров](./docs/for-product-managers.md) или [Воркфлоу Design-to-Code](./guide/workflows/design-to-code.md) |
| Нетехнический специалист | [Гид по Claude Cowork](https://github.com/FlorianBruniaux/claude-cowork-guide) |

Для персонализированного маршрута используйте онбординг-промпт репозитория:

```bash
claude "Fetch and follow the onboarding instructions from: https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/tools/onboarding-prompt.md"
```

---

## Создание (Build)

### Инженерия агентов (Agent Engineering)

Агент — это лишь один из компонентов более крупной системы. Окружающая обвязка (harness) управляет контекстом, инструментами, разрешениями, состоянием, условиями останова, восстановлением после ошибок и оценкой качества.

| Ресурс | Какое решение поддерживает |
|---|---|
| [Agent Harness Engineering](./guide/core/agent-harness.md) | Определение управляющих контуров вокруг цикла агента |
| [Loop & Graph Engineering](./guide/core/loop-graph-engineering.md) | Выбор между замкнутыми циклами с обратной связью и явными графами воркфлоу |
| [AI Design Patterns](./guide/core/ai-design-patterns.md) | Архитектура агентов через привычные разработчикам паттерны GoF, интеграции и устойчивости |
| [Карта агентных сред (Agent Harness Map)](./guide/ecosystem/agent-harness-landscape.md) | Разделение рантаймов, оркестраторов, фреймворков и панелей управления |
| [Agentic Tools](./guide/ecosystem/agentic-tools.md) | Сравнение ведущих агентов для кодинга и продуктов оркестрации |
| [Оценка агентов (Agent Evaluation)](./guide/roles/agent-evaluation.md) | Тестирование поведения, регрессий и результатов на уровне задач |
| [Глоссарий harness-систем](./guide/core/glossary.md) | Единая терминология при проектировании и код-ревью |
| [Границы понятий в ИИ](./guide/core/ai-concept-boundaries.md) | Разрешение 7 типичных путаниц с примерами из репозитория и тестами на понимание |

### Контекст и память

Качество контекста определяет каждый вызов инструмента и каждое принимаемое решение. Начинайте с инструкций проекта, добавляйте специализированный контекст только при возникновении регулярной задачи и тестируйте, влияет ли дополнительный материал на поведение.

| Ресурс | Фокус |
|---|---|
| [Контекстная инженерия](./guide/core/context-engineering.md) | Бюджет контекста, модульные инструкции, сборка и измерение |
| [Системы памяти](./guide/core/memory-systems.md) | Нативная память, межсессионные системы, совместное использование в команде и риски утечек |
| [Инструменты контекстной инженерии](./guide/ecosystem/context-engineering-tools.md) | Сжатие вывода, поиск (retrieval), шлюзы и инспекция контекста |
| [Аудит контекста](./tools/context-audit-prompt.md) | Оценка контекстной архитектуры проекта |
| [Инструкции ИИ для команды](./guide/workflows/team-ai-instructions.md) | Поддержание общих инструкций внутри команды разработчиков |

### Рабочие процессы (Workflows)

| Цель | Воркфлоу |
|---|---|
| Разработка через тестирование | [TDD с Claude](./guide/workflows/tdd-with-claude.md) |
| Определение поведения до реализации | [Spec-First Development](./guide/workflows/spec-first.md) |
| Разделение планирования и выполнения | [Plan-Driven Development](./guide/workflows/plan-driven.md) |
| Сравнение независимых вариантов | [Best-of-N](./guide/workflows/best-of-n.md) |
| Координация нескольких агентов | [Команды агентов (Agent Teams)](./guide/workflows/agent-teams.md) |
| Автономные фабрики кода | [Agentic Software Factories](./guide/workflows/agentic-software-factories.md) |
| Систематическое код-ревью | [Code Review](./guide/workflows/code-review.md) |
| Проверяемость изменений от агентов | [Reviewable Agent Changes](./guide/workflows/reviewable-agent-changes.md) |
| Подготовка PR в Open Source | [AI-Assisted Open Source Contributions](./guide/workflows/ai-assisted-open-source-contributions.md) |
| Исследование незнакомых репозиториев | [Exploration Workflow](./guide/workflows/exploration-workflow.md) |

[Изучите все воркфлоу](./guide/workflows/) для управления задачами, GitHub Actions, надежности в продакшене, событийных агентов, конвертации дизайна в код, генерации PDF, поиска и командных стандартов.

### Выбор минимального интерфейса

Claude Code умеет вызывать локальные команды, навыки (skills), агентов, хуки, плагины и MCP-серверы. Избыточная инфраструктура усложняет настройку, добавляет точки отказа и удорожает поддержку.

| Если задаче требуется | Предпочтительный вариант |
|---|---|
| Детерминированная локальная команда | CLI или bash-скрипт |
| Переиспользуемые инструкции и сопутствующие файлы | Skill (навык) |
| Отдельный контекст и изолированная роль | Agent (агент) |
| Реакция на событие жизненного цикла | Hook (хук) |
| Упакованный набор взаимосвязанных возможностей | Plugin (плагин) |
| Типизированный интерфейс к внешнему сервису | MCP-сервер |

Используйте [руководство по выбору MCP vs CLI](./guide/ecosystem/mcp-vs-cli.md) и [матрицу компромиссов](./guide/ultimate-guide.md#when-to-use-what) перед добавлением новой интеграции.

---

## Масштаб (Scale)

### Надежность и безопасность

| Направление | Основной ресурс | Практический инструмент |
|---|---|---|
| Разрешения и prompt injection | [Security Hardening](./guide/security/security-hardening.md) | [Аудит разрешений](./tools/permissions-audit-prompt.md) |
| Изоляция ненадежного кода | [Sandbox Isolation](./guide/security/sandbox-isolation.md) | [Нативная песочница](./guide/security/sandbox-native.md) |
| Изменения в проде и откат | [Безопасность в проде](./guide/security/production-safety.md) | [Production Reliability](./guide/workflows/production-reliability.md) |
| Конфиденциальные данные и хранение | [Приватность данных](./guide/security/data-privacy.md) | [Enterprise Governance](./guide/security/enterprise-governance.md) |
| Тестирование защищенности | [Agentic Pentesting](./guide/security/agentic-pentesting.md) | [Оценка DarkMoon и Strix](./docs/resource-evaluations/darkmoon-strix-agentic-pentesting.md) |
| Безопасность цепочки поставок MCP | [Экосистема MCP](./guide/ecosystem/mcp-servers-ecosystem.md) | [База угроз](./examples/commands/resources/threat-db.yaml) |
| Готовность к делегированию задач | [Аудит полноты спецификаций](./tools/spec-completeness-audit.md) | [Оценка агентов](./guide/roles/agent-evaluation.md) |

### Оценка и эксплуатация (Operations)

| Потребность | Ресурс |
|---|---|
| Трассировка поведения и сбоев агентов | [Observability](./guide/ops/observability.md) |
| Атрибуция изменений, созданных с ИИ | [AI Traceability](./guide/ops/ai-traceability.md) |
| Оценка результатов работы команды | [Метрики команды](./guide/ops/team-metrics.md) |
| Расчет стоимости на уровне задач | [AI Unit Economics](./guide/ops/ai-unit-economics.md) |
| Воркфлоу для инфраструктуры | [DevOps & SRE](./guide/ops/devops-sre.md) |
| Управляемая маршрутизация API-трафика | [API Gateways](./guide/ops/api-gateway.md) |

### Организация и экономика

| Вопрос | Ресурс |
|---|---|
| Развертывание Claude Code в команде | [Подходы к внедрению](./guide/roles/adoption-approaches.md) |
| Уровни доступа и согласования | [Enterprise Governance](./guide/security/enterprise-governance.md) |
| Сохранение базы знаний команды | [Team Knowledge Base](./guide/ecosystem/team-knowledge-base.md) |
| Сравнение подписок, API и шлюзов | [Стратегия подписок](./guide/ops/subscription-strategy.md) |
| Локальный инференс против облачного | [Local vs Cloud Inference](./guide/ecosystem/local-vs-cloud-inference.md) |
| Эволюция ролей в эпоху ИИ | [AI Roles](./guide/roles/ai-roles.md) |

---

## Форматы руководства

| Формат | Назначение | Читать онлайн | Исходник / Загрузка |
|---|---|---|---|
| Полное руководство | Глубокие объяснения всех концепций | [Ultimate Guide](https://cc.bruniaux.com/guide/ultimate-guide/) | [Markdown (EN)](./guide/ultimate-guide.md) · [Markdown (FR)](./guide/ultimate-guide.fr.md) |
| Ежедневная шпаргалка | Команды, шорткаты и проверки | [Quick Reference](https://cc.bruniaux.com/cheatsheet/) | [Markdown (RU)](./guide/cheatsheet.ru.md) · [Markdown (EN)](./guide/cheatsheet.md) |
| Обучающий курс | 7 модулей с практическими заданиями | [Learning Paths](https://cc.bruniaux.com/learning/) | [Модули курса](./guide/learning-path/) |
| Готовые шаблоны | Агенты, навыки, хуки и скрипты | [Examples](https://cc.bruniaux.com/examples/) | [Каталог примеров](./examples/) |
| Визуальные схемы | Архитектура, контекст, безопасность | [Diagrams](https://cc.bruniaux.com/diagrams/) | [Исходники схем](./guide/diagrams/) |
| Проверка знаний | Тесты со ссылками на документацию | [Quiz](https://cc.bruniaux.com/quiz/) | [Вопросы квиза](./quiz/) |
| Печатные карточки | Одна концепция на страницу | [Cheat Sheets](https://cc.bruniaux.com/cheatsheets/) | [Исходники карточек](./whitepapers/recap-cards/) |
| Электронные книги | PDF и EPUB для чтения офлайн | [Ebooks](https://cc.bruniaux.com/whitepapers/) | [Раздел загрузок](https://cc.bruniaux.com/downloads/) |
| Машиночитаемый индекс | Поиск и интеграция для LLM | [Guide MCP](https://cc.bruniaux.com/mcp/) | [llms.txt](./machine-readable/llms.txt) · [reference.yaml](./machine-readable/reference.yaml) |

---

## MCP-сервер: использование руководства в любом редакторе

Установите руководство как stdio MCP-сервер и делайте запросы напрямую из Claude Code, Codex, Cursor, VS Code или другого MCP-клиента.

```bash
claude mcp add --scope user claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.8
codex mcp add claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.8
```

Конфигурация Claude Code на уровне проекта задается в `.mcp.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.8"]
    }
  }
}
```

| Возможность | Количество | Названия |
| --- | ---: | --- |
| Инструменты (Tools) | 17 | `compare_versions`, `diff_official_docs`, `get_changelog`, `get_cheatsheet`, `get_digest`, `get_example`, `get_release`, `get_threat`, `init_official_docs`, `list_examples`, `list_threats`, `list_topics`, `read_section`, `refresh_official_docs`, `search_examples`, `search_guide`, `search_official_docs` |
| Ресурсы (Resources) | 7 | `claude-code-guide://agent-harnesses`, `claude-code-guide://ai-design-patterns`, `claude-code-guide://distribution-channels`, `claude-code-guide://llms`, `claude-code-guide://reference`, `claude-code-guide://releases`, `claude-code-guide://translations` |
| Промпты (Prompts) | 1 | `claude-code-expert` |
| Команды-компаньоны | 5 | `/ccguide:daily`, `/ccguide:diff-docs`, `/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:search-docs` |

---

## Языки и переводы

Английский язык является каноническим изданием. Французская версия поддерживается непосредственно в этом репозитории. Версии на русском, упрощенном китайском, украинском и латиноамериканском испанском языках созданы сообществом.

| Язык | Версия | Ссылка |
|---|---|---|
| English | Каноническое руководство | [guide/ultimate-guide.md](./guide/ultimate-guide.md) |
| Français | Официальный перевод в репозитории | [guide/ultimate-guide.fr.md](./guide/ultimate-guide.fr.md) |
| Русский | Версия сообщества (AnyKey1) | [GitHub repo](https://github.com/AnyKey1/claude-code-ultimate-guide-ru) · [README.ru.md](./README.ru.md) · [Шпаргалка](./guide/cheatsheet.ru.md) |
| 简体中文 | Сообщество (JAYcodr) | [GitHub repo](https://github.com/JAYcodr/claude-code-ultimate-guide-zh) |
| Українська | Сообщество (gerasimsergey) | [GitHub repo](https://github.com/gerasimsergey/claude-code-ultimate-guide-ua) |
| Español latinoamericano | Сообщество (Richardls) | [GitHub repo](https://github.com/Richardls/claude-code-ultimate-guide-es) |

Страница [статуса переводов](./guide/core/translations.md) содержит сведения о мейнтейнерах, коммитах источников, охвате и актуальности.

---

## Структура репозитория

```text
guide/
├── ultimate-guide.md       Полное каноническое руководство (EN)
├── ultimate-guide.fr.md    Полное руководство на французском (FR)
├── cheatsheet.md           Ежедневная шпаргалка (EN)
├── cheatsheet.ru.md        Ежедневная шпаргалка на русском (RU)
├── learning-path/          Пошаговый курс обучения
├── core/                   Архитектура, инструменты, контекст, методики
├── security/               Харденинг, изоляция, приватность, governance
├── ecosystem/              Агенты, MCP, инструменты, инференс, база знаний
├── roles/                  Внедрение, обучение, оценка, роли
├── ops/                    Observability, метрики, экономика, шлюзы
├── workflows/              Практические сценарии решения задач
└── diagrams/               Схемы Mermaid с текстовыми описаниями

examples/                   Шаблоны агентов, навыков, хуков и воркфлоу
machine-readable/           Машиночитаемые индексы и данные релизов
mcp-server/                 MCP-сервер руководства для редакторов
quiz/                       Тестирование знаний
docs/resource-evaluations/  Оценки внешних ресурсов
whitepapers/                Исходные материалы расширенных отчетов
```

---

## Участие в разработке (Contributing)

Исправления, отсутствующие примеры, битые ссылки, вопросы для квиза и улучшения документации приветствуются. Пожалуйста, прочтите [CONTRIBUTING.md](./CONTRIBUTING.md) перед созданием Pull Request.

---

## Автор и мейнтейнер

**Florian Bruniaux**

[GitHub](https://github.com/FlorianBruniaux) · [LinkedIn](https://www.linkedin.com/in/florian-bruniaux-43408b83/) · [Портфолио](https://www.florian.bruniaux.com/)

---

## Лицензия

Тексты руководства распространяются под лицензией [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Переиспользуемые шаблоны кода распространяются под [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (Public Domain).

---

*Версия 3.46.0 | Обновляется ежедневно*
