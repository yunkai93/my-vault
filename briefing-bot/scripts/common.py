from __future__ import annotations

import json
import os
import pathlib
import uuid
from datetime import datetime, timedelta, timezone


ROOT = pathlib.Path(__file__).resolve().parents[2]
BOT_ROOT = ROOT / "briefing-bot"
CONFIG_PATH = BOT_ROOT / "config" / "sources.json"
STATE_DIR = BOT_ROOT / "state"
LOG_DIR = BOT_ROOT / "logs"
CHAT_STATE_DIR = STATE_DIR / "chat_sessions"
P2P_LOG_DIR = LOG_DIR / "p2p"
NEWS_FILE = ROOT / "news" / "AI早报.md"
PROMPT_FILE = BOT_ROOT / "prompts" / "brief_prompt.md"
ENV_FILE = BOT_ROOT / ".env"
VENV_DIR = BOT_ROOT / ".venv"


def now_cst() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    CHAT_STATE_DIR.mkdir(parents=True, exist_ok=True)
    P2P_LOG_DIR.mkdir(parents=True, exist_ok=True)


def load_env_file() -> None:
    if not ENV_FILE.exists():
        return
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            os.environ.setdefault(key, value)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def dump_json(path: pathlib.Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: pathlib.Path, default: object) -> object:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def require_env(name: str) -> str:
    value = env(name)
    if not value:
        raise SystemExit(f"missing required env: {name}")
    return value


def new_uuid() -> str:
    return str(uuid.uuid4())


def set_env_values(updates: dict[str, str]) -> None:
    existing: dict[str, str] = {}
    lines: list[str] = []
    if ENV_FILE.exists():
        for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                lines.append(raw_line)
                continue
            key, value = raw_line.split("=", 1)
            existing[key.strip()] = value.strip()
    existing.update({key: value for key, value in updates.items() if value is not None})
    rendered = [f"{key}={value}" for key, value in sorted(existing.items())]
    ENV_FILE.write_text("\n".join(rendered) + "\n", encoding="utf-8")
    try:
        ENV_FILE.chmod(0o600)
    except Exception:
        pass
    for key, value in updates.items():
        os.environ[key] = value


load_env_file()
