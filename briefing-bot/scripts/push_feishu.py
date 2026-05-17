from __future__ import annotations

import json
import os
import urllib.request

from common import NEWS_FILE, STATE_DIR, load_json


def extract_today_block(date: str) -> str:
    if not NEWS_FILE.exists():
        return ""
    text = NEWS_FILE.read_text(encoding="utf-8")
    marker = f"## {date}\n"
    start = text.find(marker)
    if start == -1:
        return ""
    next_pos = text.find("\n## ", start + len(marker))
    block = text[start: next_pos if next_pos != -1 else len(text)].strip()
    return block


def markdown_to_text(block: str) -> str:
    lines: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            lines.append("")
            continue
        if line.startswith("## "):
            lines.append(line.replace("## ", ""))
            continue
        if line.startswith("### "):
            lines.append(line.replace("### ", ""))
            continue
        if line.startswith("_") and line.endswith("_"):
            lines.append(line.strip("_"))
            continue
        line = line.replace("](", " | ").replace("[", "").replace(")", "")
        lines.append(line)
    return "\n".join(lines).strip()


def main() -> int:
    webhook = os.environ.get("FEISHU_WEBHOOK", "").strip()
    if not webhook:
        return 0

    brief = load_json(STATE_DIR / "brief.json", {})
    date = brief.get("date", "")
    if not date:
        return 0

    content = markdown_to_text(extract_today_block(date))
    if not content:
        content = f"{date} AI早报已生成，但未找到对应正文块。"

    payload = {
        "msg_type": "text",
        "content": {
            "text": content,
        },
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8", errors="ignore")
        if resp.status >= 300:
            raise SystemExit(body or f"feishu push failed with status {resp.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
