from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from common import BOT_ROOT, LOG_DIR, ROOT, ensure_dirs, now_cst


SCRIPTS = [
    "fetch_sources.py",
    "generate_brief.py",
    "update_vault.py",
]


def run_cmd(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(cwd), text=True, capture_output=True, check=check)


def run_step(script: str) -> None:
    path = BOT_ROOT / "scripts" / script
    proc = run_cmd(["python3", str(path)], cwd=ROOT, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"{script} failed:\n{proc.stderr or proc.stdout}")


def git_publish() -> None:
    origin = run_cmd(["git", "config", "--get", "remote.origin.url"], cwd=ROOT).stdout.strip()
    if not origin:
        raise SystemExit("git publish failed: remote.origin.url not found")

    tmp_root = BOT_ROOT / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="briefing-publish-", dir=str(tmp_root)) as tmpdir:
        repo_dir = Path(tmpdir) / "repo"
        run_cmd(["git", "clone", "--depth", "1", "--branch", "main", origin, str(repo_dir)], cwd=ROOT)

        target_news = repo_dir / "news" / "AI早报.md"
        target_news.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "news" / "AI早报.md", target_news)

        run_cmd(["git", "add", "news/AI早报.md"], cwd=repo_dir)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(repo_dir))
        if diff.returncode == 0:
            return
        msg = f"chore: update AI briefing {now_cst().strftime('%Y-%m-%d')}"
        run_cmd(["git", "commit", "-m", msg], cwd=repo_dir)
        run_cmd(["git", "push", "origin", "main"], cwd=repo_dir)


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
