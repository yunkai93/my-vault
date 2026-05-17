from __future__ import annotations

import subprocess
import threading

import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

from briefing_view import help_text, normalize_command
from chat_agent import ask_safe
from common import BOT_ROOT, env, now_cst, set_env_values
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


def rerun_briefing() -> str:
    cmd = [str(BOT_ROOT / ".venv" / "bin" / "python"), str(BOT_ROOT / "scripts" / "run_briefing.py")]
    proc = subprocess.run(cmd, cwd=str(BOT_ROOT.parent), text=True, capture_output=True)
    if proc.returncode != 0:
        return "重跑失败，请稍后查看服务器日志。"
    return "早报已重跑，最新卡片已推送到群里。"


def handle_group_message(message_id: str, user_text: str) -> None:
    command = normalize_command(user_text)
    if any(key in command for key in ["帮助", "help", "指令", "命令"]):
        reply_text(message_id, help_text())
        return
    if "重跑" in command and "早报" in command:
        reply_text(message_id, rerun_briefing())
        return
    reply_text(message_id, help_text())


def handle_p2p_message(message_id: str, user_text: str) -> None:
    answer = ask_safe(user_text)
    reply_text(message_id, answer)


def dispatch_async(target, *args) -> None:
    thread = threading.Thread(target=target, args=args, daemon=True)
    thread.start()


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
    if data.event.message.chat_type == "p2p":
        dispatch_async(handle_p2p_message, data.event.message.message_id, user_text)
    else:
        dispatch_async(handle_group_message, data.event.message.message_id, user_text)
    log_line(f"{now_cst().isoformat()} accepted {data.event.message.message_id}: {user_text}")


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
