from __future__ import annotations

import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

from briefing_view import compact_digest, full_brief_text, help_text, latest_take, normalize_command, sources_text, status_text
from common import BOT_ROOT, NEWS_FILE, STATE_DIR, env, load_json, now_cst, set_env_values
from feishu_app import build_client, reply_text

LOG_FILE = BOT_ROOT / "logs" / "feishu-reply.log"


def log_line(text: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(text.rstrip() + "\n")


def extract_text(content: str) -> str:
    import json

    try:
        payload = json.loads(content)
    except Exception:
        return ""
    return (payload.get("text") or "").strip()


def build_reply(user_text: str) -> str:
    command = normalize_command(user_text)
    brief = load_json(STATE_DIR / "brief.json", {})
    if any(key in command for key in ["帮助", "help", "指令", "命令"]):
        return help_text()
    if any(key in command for key in ["简报", "digest", "摘要"]):
        return compact_digest(brief)
    if any(key in command for key in ["判断", "take", "观点"]):
        return latest_take(brief)
    if any(key in command for key in ["来源", "source"]):
        return sources_text(brief)
    if any(key in command for key in ["状态", "status"]):
        return status_text(brief, env("FEISHU_CHAT_ID"))
    if any(key in command for key in ["早报", "日报", "brief"]):
        return full_brief_text(brief)
    return help_text()


def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    if data.event is None or data.event.message is None:
        return
    if data.event.sender and data.event.sender.sender_type == "bot":
        return
    if data.event.message.chat_type == "group" and data.event.message.chat_id:
        if not env("FEISHU_CHAT_ID"):
            set_env_values({"FEISHU_CHAT_ID": data.event.message.chat_id})
    if data.event.message.message_type != "text":
        reply_text(data.event.message.message_id, "请发送文本消息。")
        return
    user_text = extract_text(data.event.message.content or "")
    if not user_text:
        reply_text(data.event.message.message_id, "消息解析失败，请发送文本消息。")
        return
    response = build_reply(user_text)
    reply_text(data.event.message.message_id, response)
    log_line(f"{now_cst().isoformat()} replied to {data.event.message.message_id}: {user_text}")


event_handler = (
    lark.EventDispatcherHandler.builder("", "")
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)
    .build()
)


def main() -> int:
    # Ensure credentials exist early.
    build_client()
    cli = lark.ws.Client(
        env("FEISHU_APP_ID"),
        env("FEISHU_APP_SECRET"),
        event_handler=event_handler,
        log_level=lark.LogLevel.INFO,
    )
    cli.start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
