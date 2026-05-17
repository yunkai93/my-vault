from __future__ import annotations

import json
import os
import pathlib
from datetime import datetime, timedelta, timezone


ROOT = pathlib.Path(__file__).resolve().parents[2]
BOT_ROOT = ROOT / "briefing-bot"
CONFIG_PATH = BOT_ROOT / "config" / "sources.json"
STATE_DIR = BOT_ROOT / "state"
LOG_DIR = BOT_ROOT / "logs"
NEWS_FILE = ROOT / "news" / "AI早报.md"
PROMPT_FILE = BOT_ROOT / "prompts" / "brief_prompt.md"
ENV_FILE = BOT_ROOT / ".env"


def now_cst() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


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


load_env_file()
