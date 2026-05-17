from __future__ import annotations

import argparse

from common import set_env_values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--app-secret", required=True)
    parser.add_argument("--chat-id", default="")
    args = parser.parse_args()

    updates = {
        "FEISHU_APP_ID": args.app_id.strip(),
        "FEISHU_APP_SECRET": args.app_secret.strip(),
    }
    if args.chat_id.strip():
        updates["FEISHU_CHAT_ID"] = args.chat_id.strip()
    set_env_values(updates)
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
