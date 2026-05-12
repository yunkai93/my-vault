# Claude Code

> [!abstract]
> 记录 Claude Code 的安装方式与常用会话命令，适合作为快速操作备忘。

## 安装
### Windows
```
irm https://claude.ai/install.ps1 | iex
环境变量Path增加：C:\Users\你的用户名\.local\bin\
```
### Mac/Linux
```
curl -fsSL https://claude.ai/install.sh | bash
```

## 基础
```
# 进入文件夹
claude
/resume 当前目录历史会话
/context 查看上下文占用
/compact 手动压缩
```

