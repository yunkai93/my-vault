from __future__ import annotations

import subprocess
from pathlib import Path

from common import env

SANDBOX_DIR = Path(env("FEISHU_CHAT_SANDBOX_DIR", "/tmp/briefing-chat-agent"))
PROMPT = (
    "你现在是一个纯问答聊天机器人。"
    "禁止调用任何工具，禁止访问文件，禁止执行命令，禁止联网，禁止提供服务器控制能力。"
    "只根据用户问题进行正常问答。"
    "回答默认使用中文，简洁准确。"
)


def ask(question: str) -> str:
    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
    out_file = SANDBOX_DIR / "last_answer.txt"
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-rules",
        "--skip-git-repo-check",
        "-C",
        str(SANDBOX_DIR),
        "-s",
        "read-only",
        "-o",
        str(out_file),
        f"{PROMPT}\n\n用户问题：{question}",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout or "chat agent failed")
    text = out_file.read_text(encoding="utf-8").strip()
    if not text:
        return "这次没有生成可用回复，请稍后再试。"
    return text[:3500]


def ask_safe(question: str) -> str:
    try:
        return ask(question)
    except Exception:
        return "当前问答服务暂时不可用，请稍后再试。"
