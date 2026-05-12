# Codex

> [!abstract]
> 记录 Codex 的安装方式与最基础启动方法，后续可继续补充工作流和配置经验。

## 安装
```
npm i -g @openai/codex

# 服务器上
mkdir -p ~/.codex
chmod 700 ~/.codex
nano ~/.codex/config.toml
nano ~/.codex/auth.json
chmod 600 ~/.codex/config.toml ~/.codex/auth.json
```

## 基础
```
# 进入文件夹
codex ""
```

