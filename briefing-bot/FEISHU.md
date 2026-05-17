# 飞书应用机器人接入说明

当前仓库已按「飞书自建应用机器人」接入，分为两部分：

1. `push_feishu.py`
   - 用应用机器人向固定群发送每日早报
2. `feishu_reply.py`
   - 用飞书长连接接收 `@机器人` 消息并回复

## 你需要提供

写入 `briefing-bot/.env`：

```env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CHAT_ID=oc_xxx
```

## 飞书开放平台内需要确认

1. 已开启机器人能力
2. 已发布最新版本
3. 已给应用添加以下权限之一或组合：
   - `im:message`
   - `im:message:send_as_bot`
   - `im:message.group_at_msg:readonly`
   - `im:message.p2p_msg:readonly`
4. 已订阅事件：
   - `im.message.receive_v1`
5. 事件订阅方式选择：
   - `长连接`

## 群里回复逻辑

当前先实现最小可用版：

- `@机器人 早报`：回复当天最新早报
- `@机器人 简报`：回复群聊短版摘要
- `@机器人 判断`：只回复当天一句话判断
- `@机器人 来源`：回复本次采用的媒体源
- `@机器人 状态`：回复当前本地摘要状态
- `@机器人 帮助`：回复可用指令
- 其他文本：回复简短帮助

## 本地命令

检查配置：

```bash
briefing-bot/.venv/bin/python briefing-bot/scripts/check_feishu_config.py
```

手动发群消息：

```bash
briefing-bot/.venv/bin/python briefing-bot/scripts/push_feishu.py
```

手动启动回复服务：

```bash
briefing-bot/.venv/bin/python briefing-bot/scripts/feishu_reply.py
```
