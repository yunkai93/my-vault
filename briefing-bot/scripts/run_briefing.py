from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from common import BOT_ROOT, LOG_DIR, ROOT, ensure_dirs, now_cst


SCRIPTS = [
    "fetch_sources.py",
    "generate_brief.py",
    "update_vault.py",
]


def run_step(script: str) -> None:
    path = BOT_ROOT / "scripts" / script
    proc = subprocess.run(["python3", str(path)], cwd=str(ROOT), text=True, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"{script} failed:\n{proc.stderr or proc.stdout}")


def git_publish() -> None:
    subprocess.run(["git", "pull", "--rebase"], cwd=str(ROOT), check=False)
    tracked = [
        "news/AI早报.md",
        "briefing-bot/config/sources.json",
        "briefing-bot/prompts/brief_prompt.md",
        "briefing-bot/prompts/brief_schema.json",
        "briefing-bot/scripts/common.py",
        "briefing-bot/scripts/fetch_sources.py",
        "briefing-bot/scripts/generate_brief.py",
        "briefing-bot/scripts/push_feishu.py",
        "briefing-bot/scripts/run_briefing.py",
        "briefing-bot/scripts/update_vault.py",
        "briefing-bot/systemd/briefing-bot.service",
        "briefing-bot/systemd/briefing-bot.timer",
        "briefing-bot/.gitignore",
        "briefing-bot/AGENTS.md",
    ]
    subprocess.run(["git", "add", *tracked], cwd=str(ROOT), check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(ROOT))
    if diff.returncode == 0:
        return
    msg = f"chore: update AI briefing {now_cst().strftime('%Y-%m-%d')}"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(ROOT), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(ROOT), check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-git", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    for script in SCRIPTS:
        run_step(script)
    if not args.no_git:
        git_publish()
    run_step("push_feishu.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
