---
title: "Модуль 06: Хуки и события"
description: "Модуль 06 траектории обучения: добавление хуков Claude Code, принятие решений на основе структурированного JSON, принцип Fail-Closed и тестирование без запуска интерактивной сессии. 1 час, средний уровень."
---

# Модуль 06: Хуки и события (Hooks & Events)

**Время:** 1 час | **Сложность:** ⭐⭐ Средний

**Предыдущий модуль:** [Модуль 05: Навыки (Skills) и автоматизация](05-skills.ru.md)

## Цель

Создать хук Claude Code, который анализирует структурированные входные данные перед выполнением инструментов, следует принципу **Fail-Closed** (блокирует при поврежденном вводе) и тестируется автономно без запуска сессии.

> **Обратите внимание:** Хуки Claude Code — это не Git-хуки. Git-хуки реагируют на действия репозитория (`pre-commit`, `post-merge`). Хуки Claude Code перехватывают события жизненного цикла ИИ: `PreToolUse`, `PostToolUse`, `SessionStart` и т.д.

---

## Что вы узнаете

- Где регистрируются хуки Claude Code (`.claude/settings.json`)
- Как работают матчеры (matchers) событий
- Какой JSON-пейлоад передается хуку на `stdin`
- Как хук `PreToolUse` разрешает или блокирует действие
- Коды возврата: почему код `2` блокирует действие, а код `1` — нет
- Автономное тестирование скрипта хука через тестовые фикстуры

---

## Архитектура перехвата (Hook Boundary)

Командный хук — это локальная программа, запускаемая Claude Code при возникновении события. На вход (`stdin`) она получает JSON-объект. Для события `PreToolUse` ключевыми полями являются `tool_name`, `tool_input` и `tool_use_id`.

```text
Claude предлагает вызвать Write или Edit
              │
              ▼
Матчер PreToolUse перехватывает событие
              │
              ▼
Скрипт хука читает JSON и возвращает решение
              │
              ▼
Claude Code применяет решение (deny или продолжение)
```

---

## Регистрация хука `PreToolUse`

Хуки проекта объявляются в файле `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-paths.py"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

---

## Скрипт валидации: `.claude/hooks/protect-paths.py`

Создайте скрипт защиты чувствительных файлов (например, `.env`, ключей `.pem` и служебной папки `.git`):

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import PurePosixPath


def decide(value: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": value,
            "permissionDecisionReason": reason,
        }
    }))


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    decide("deny", "Невалидный JSON на входе хука.")
    raise SystemExit(0)

if payload.get("tool_name") not in {"Write", "Edit"}:
    decide("deny", "Инструмент не поддерживается данным матчером.")
    raise SystemExit(0)

file_path = payload.get("tool_input", {}).get("file_path")
if not isinstance(file_path, str) or not file_path.strip():
    decide("deny", "Запрос Write/Edit не содержит file_path.")
    raise SystemExit(0)

path = PurePosixPath(file_path.replace("\\", "/"))
protected = (
    ".git" in path.parts
    or path.name == ".env"
    or path.name.startswith(".env.")
    or path.suffix in {".key", ".pem"}
)

if protected:
    decide("deny", f"Попытка модификации защищенного пути: {file_path}")
else:
    # Разрешаем стандартный поток проверки
    raise SystemExit(0)
```

---

## Коды возврата (Exit Codes) в Claude Code

- **Код `0`**: выполнение хука завершилось успешно; если выведен JSON со структурированным решением (`hookSpecificOutput`), Claude Code применяет его.
- **Код `2`**: жесткая блокировка действий для событий, поддерживающих отмену (включая `PreToolUse`). Ошибка из `stderr` передается модели.
- **Код `1`**: сигнализирует об ошибке самого скрипта, но **НЕ блокирует** вызов инструмента!

---

## Чек-лист готовности к следующему шагу

✓ Вы отличаете хуки Claude Code от хуков Git  
✓ Скрипт хука считывает JSON со стандартного потока ввода (`stdin`)  
✓ Некорректный или поврежденный вход блокируется (принцип Fail-Closed)  
✓ Вы знаете, что для блокировки используется код выхода `2` либо JSON `permissionDecision: "deny"`  
✓ Вы протестировали скрипт отдельно от Claude Code через `printf '...' | python3 ...`  

---

**Завершили Модуль 06?** → Переходите к **[Модулю 07: Продвинутые паттерны](07-advanced.ru.md)**.
