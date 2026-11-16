# День 1 — закрытие окружения (16.11.2026)

Цель дня: `python 00_setup/check_env.py` печатает **«ДЕНЬ 1 ЗАКРЫТ»**.

Уже готово: Python 3.12 (в `.venv`), `uv`, папка `ai-lab`, скрипт `check_env.py`, `tiktoken`.

---

## 1. Git — 10 мин

```powershell
winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
```

**Закрой и заново открой PowerShell** (иначе `git` не появится в PATH), затем:

```powershell
git --version
git config --global user.name "Имя Фамилия"
git config --global user.email "твой@email"
```

Репозиторий и первый коммит:

```powershell
cd "C:\Users\ttopn\Documents\Проект по умолчанию\ai-lab"
git init
git add .
git commit -m "День 1: каркас ai-lab, проверка окружения"
```

GitHub: создай пустой репозиторий `ai-lab` (без README), затем:

```powershell
git branch -M main
git remote add origin https://github.com/<твой-логин>/ai-lab.git
git push -u origin main
```

При первом push откроется браузер — авторизуйся через Git Credential Manager.

Проверка: `git log --oneline` показывает коммит, на GitHub виден код.

---

## 2. Ollama — 25 мин

```powershell
winget install --id Ollama.Ollama -e
```

Снова **перезапусти PowerShell**, затем:

```powershell
ollama --version
ollama pull qwen3:4b
ollama run qwen3:4b "Скажи одной строкой, что такое токен"
```

Вывод из модели — через `/bye`.

Важно про железо: GTX 1050 Ti = 4 ГБ VRAM, RAM 11 ГБ. Модели больше 4B (7B, 14B) сюда не ставить — будет 1 токен в секунду. Ожидаемая скорость на `qwen3:4b`: 3–8 ток./с. Если совсем медленно — `ollama pull qwen2.5:3b`.

---

## 3. Ключ — 10 мин

1. https://openrouter.ai → регистрация → Keys → Create Key.
2. Пополнить на $5 (хватит на всю фазу 0–1).
3. Открой `ai-lab\.env` в блокноте и впиши строку:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

Остальные ключи (OpenAI, Anthropic, GigaChat, Yandex) пока пустые — они для контура 152-ФЗ, это неделя 41.

`.env` в `.gitignore` — проверять, что он не попал в коммит: `git status` не должен его показывать.

---

## 4. Зависимости и проверка — 5 мин

```powershell
cd "C:\Users\ttopn\Documents\Проект по умолчанию\ai-lab"
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
python 00_setup\check_env.py
```

Если PowerShell блокирует активацию:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Критерий дня** — последняя строка:

```
ДЕНЬ 1 ЗАКРЫТ: есть Python, минимум один ключ, локальная модель.
```

---

## 5. Скрипт руками — 20 мин

`01_basics\days_to_new_year.py`: спросить имя и дату рождения, посчитать дни до 31.12.2026.
Только `input`, `datetime`, `print`. Без агента. Сломалось — читаешь ошибку.

Запустить, закоммитить:

```powershell
git add .
git commit -m "День 1: скрипт без подсказок"
```

---

## 6. Заметка — 5 мин

`notes\2026-11-16.md`, пять строк: что не понял / что сломалось / что гуглил.
Это заготовка раздела «что не сработало» — главный маркер эксперта.

---

## 7. Опционально: VS Code — 10 мин

```powershell
winget install --id Microsoft.VisualStudioCode -e
```

Нужен, чтобы видеть структуру и диффы глазами, а не через агента.

---

## Чего сегодня не делать

- Docker (4 ГБ, нужен на неделе 21).
- Выбор 2 отраслей и первого процесса (день 7).
- Курсы и лекции вместо инфраструктуры.
- Второй LLM-фреймворк.

---

## Вероятные сбои

| Симптом | Причина | Лечение |
|---|---|---|
| `git` не найден после установки | старый процесс PowerShell | закрыть все окна терминала, открыть заново |
| `Activate.ps1` запрещён | ExecutionPolicy | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `python` открывает Microsoft Store | заглушка WindowsApps | использовать `.\.venv\Scripts\python.exe` |
| Ollama не отвечает в check_env | сервис не запущен | `ollama serve` в отдельном окне |
| `push` отклонён | репозиторий на GitHub создан с README | `git pull --rebase origin main`, затем push |
| ключ в `.env`, но «нет ключа» | пробелы вокруг `=` или BOM | строка ровно `OPENROUTER_API_KEY=sk-or-...` |
