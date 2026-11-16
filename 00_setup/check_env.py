"""
Проверка окружения. Только стандартная библиотека — работает до pip install.

Запуск:
    python 00_setup/check_env.py
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OK = "[ OK ]"
NO = "[ -- ]"
WARN = "[ !! ]"


def line(status: str, text: str) -> None:
    print(f"{status} {text}")


def check_python() -> bool:
    v = sys.version_info
    line(OK, f"Python {v.major}.{v.minor}.{v.micro} ({platform.machine()})")
    if v.major == 3 and v.minor >= 12:
        line(OK, "версия подходит")
        return True
    line(NO, "нужен Python 3.12+")
    return False


def check_tools() -> None:
    for name in ("git", "ollama", "code"):
        path = shutil.which(name)
        if path:
            line(OK, f"{name} найден: {path}")
        else:
            line(NO, f"{name} не установлен")


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    f = ROOT / ".env"
    if not f.exists():
        line(NO, ".env отсутствует — скопируй .env.example в .env")
        return env
    line(OK, ".env найден")
    for raw in f.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        k, v = raw.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def mask(value: str) -> str:
    if not value:
        return "пусто"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]} ({len(value)} симв.)"


def check_keys(env: dict[str, str]) -> int:
    groups = {
        "OpenRouter": ["OPENROUTER_API_KEY"],
        "OpenAI": ["OPENAI_API_KEY"],
        "Anthropic": ["ANTHROPIC_API_KEY"],
        "Google": ["GOOGLE_API_KEY"],
        "GigaChat": ["GIGACHAT_CLIENT_ID", "GIGACHAT_CLIENT_SECRET"],
        "Yandex": ["YANDEX_API_KEY", "YANDEX_FOLDER_ID"],
    }
    filled = 0
    for name, keys in groups.items():
        present = [k for k in keys if env.get(k)]
        if len(present) == len(keys):
            filled += 1
            line(OK, f"{name}: {', '.join(f'{k}={mask(env[k])}' for k in keys)}")
        elif present:
            line(WARN, f"{name}: заполнено частично")
        else:
            line(NO, f"{name}: нет ключа")
    return filled


def check_ollama(env: dict[str, str]) -> None:
    host = env.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=3) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        line(NO, f"Ollama не отвечает на {host} ({type(exc).__name__})")
        return

    models = [m.get("name", "?") for m in data.get("models", [])]
    if models:
        line(OK, f"Ollama работает, моделей: {len(models)}")
        for m in models:
            print(f"        - {m}")
    else:
        line(WARN, "Ollama работает, но моделей нет: ollama pull <model>")


def main() -> int:
    print("=" * 60)
    print("ПРОВЕРКА ОКРУЖЕНИЯ ai-lab")
    print("=" * 60)

    py_ok = check_python()
    print()
    check_tools()
    print()
    env = load_env()
    keys = check_keys(env)
    print()
    check_ollama(env)

    print("\n" + "=" * 60)
    if py_ok and (keys >= 1) and shutil.which("ollama"):
        print("ДЕНЬ 1 ЗАКРЫТ: есть Python, минимум один ключ, локальная модель.")
        return 0
    print("ДЕНЬ 1 НЕ ЗАКРЫТ. Доделай пункты с [ -- ] выше.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
