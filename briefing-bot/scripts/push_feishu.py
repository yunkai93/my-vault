from __future__ import annotations

from briefing_view import compact_digest
from common import env
from feishu_app import enabled, send_text_to_chat


def main() -> int:
    if not enabled():
        return 0
    chat_id = env("FEISHU_CHAT_ID")
    if not chat_id:
        return 0

    send_text_to_chat(chat_id, compact_digest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
