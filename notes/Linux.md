---
updated: 2026-05-14
---

# Linux

> [!note]
> 这是一篇偏实践的 Linux 运维速查笔记，重点覆盖系统概览、常用命令、目录和权限。

## 系统概览
- 系统：Ubuntu
- 端口：22-SSH，80-HTTP，443-HTTPS

## 指令
```
  # 先打补丁
  sudo apt update
  sudo apt upgrade -y
  
  # 创建用户
  adduser wuchao
  usermod -aG sudo wuchao # 登录wuchao需要管理员权限时sudo
  
  # 重启
  sudo reboot
  
  # 创建文件夹
  mkdir test
  # 创建多层目录 -p：如果上级目录不存在，就一起创建
  mkdir -p /home/wuchao/project/logs
  # 创建空文件
  touch a.txt
  # 一次创建多个
  touch a.txt b.txt c.txt
  # 创建后立刻编辑
  nano a.txt
  # 连隐藏文件一起看
  ls -la
  # 删除文件
  rm 文件名
  # 删除非空文件夹
  rm -r 文件夹名
  # 强制删除文件夹及其内容，不提示确认
  rm -rf 文件夹名

```

## 目录
```
/ 根目录，所有目录的起点
/home/wuchao 用户家目录：放项目代码、脚本、下载的文件、.ssh配置，简写 ~
/tmp 临时目录：放安装包、临时下载文件、解压中间产物，可能被清理
/etc 系统配置文件目录：重要配置 SSH配置、hosts配置、服务配置、软件配置文件
/usr 系统软件和程序文件大本营：/usr/bin-命令程序 /usr/local-手动安装的软件常放
/var 常变化的数据目录：日志/var/log、网站数据、缓存、数据库数据、运行时文件
/opt 额外安装软件：某些面板、商业软件、独立应用
/srv 服务数据目录
/dev 设备文件目录：系统底层设备相关
/proc 内核和进程信息的虚拟目录 /proc/cpuinfo 可以看cpu信息
```

## 权限
```
权限：谁可以read（r）看、write（w）改、execute（x）执行文件/目录
owner：拥有者
group：所属组
others：其他人
常用组合：rw-：可读可写；r--：只读；rwx：可读可写可执行
查看权限：ls -l
	-rw-r--r--:
		-:普通文件
		rw-：owner 可读可写
		r--：group 只读
		r--：others 只读
	drwxr-xr-x：
		d：目录
sudo：临时借root权限执行这条命令
644：文件常见权限
755：目录或可执行脚本常见权限
	r = 4，w = 2，x = 1
	7 = 4+2+1，6 = 4+2，5 = 4+1，4 = r--
改拥有者：
	# 把这个目录及里面的内容都归wuchao所有 -R是递归，表示目录下所有文件一起改
	sudo chown -R wuchao:wuchao /path/to/dir
	sudo chown -R wuchao:wuchao /home/wuchao/my-app
改权限：
	chomd 644 file.txt
	# 加执行权限
	chmod +x deploy.sh
通常系统级操作再用sudo：装软件、改服务、开端口、改配置

```

## nano
```
sudo nano /etc/ssh/sshd_config
- 方向键-移动光标
- 直接输入-修改内容
- Backspace-删除
- Ctrl+o-保存
- 回车-确认文件名
- Ctrl+x-退出
- Ctrl+w- 输入内容回车-跳转搜索位置
```

## Node
```
cd /tmp
curl -O https://nodejs.org/dist/v24.15.0/node-v24.15.0-linux-x64.tar.xz
sudo tar -xJf node-v24.15.0-linux-x64.tar.xz -C /usr/local --strip-components=1
npm config set registry https://registry.npmmirror.com
npm config get registry
```

## 服务器代理（mihomo）
```
# 服务状态
sudo systemctl status mihomo
sudo systemctl restart mihomo
sudo systemctl stop mihomo
sudo systemctl start mihomo

# 端口
# 127.0.0.1:7890  本机 mixed 代理端口
# 127.0.0.1:9090  Web 面板

# 查看当前面板地址和密钥
clashui
clashsecret

# 当前 shell 开启代理环境
clashon

# 当前 shell 关闭/开启代理环境变量，不停服务
clashproxy off
clashproxy on

# 停掉后台代理服务
clashoff

# 查看当前 shell 是否已经带代理
env | grep -i '_proxy='
```

当前这套的状态：
- `mihomo` 安装在 `/home/wuchao/apps/clashctl`
- 通过 `systemd` 管理，服务名 `mihomo`
- `wuchao` 的 `.bashrc` 已启用 `watch_proxy`，新 SSH 进入交互式 shell 会自动带上代理环境变量
- 不是全机透明代理，**是 shell / 命令行程序通过 `127.0.0.1:7890` 进入 mihomo，再由规则分流**

如果某个命令没有自动走环境变量，可以显式指定：
```
curl --proxy http://127.0.0.1:7890 https://github.com
git -c http.proxy=http://127.0.0.1:7890 clone https://github.com/xxx/yyy.git
```

浏览器打开：
```
http://127.0.0.1:9090/ui
```

订阅更新方式（当前不是服务器直连订阅，而是本地导出的 YAML 快照）：
```
# 导出的配置放在这里
/home/wuchao/apps/clashctl/resources/imported/clash-verge.yaml

# 覆盖文件后刷新订阅
bash -lc '. /home/wuchao/apps/clashctl/scripts/cmd/clashctl.sh && clashsub update 1'
```

## tmux 与 [[Codex]]
```
# 新建一个 tmux 会话
tmux new -s codex

# 新建但先不进入
tmux new -d -s codex

# 查看会话
tmux ls

# 接回会话
tmux attach -t codex
```

在 tmux 里临时离开：
- 先按 `Ctrl+b`
- 全松开
- 再按 `d`

区别：
- `tmux`：保留原来的终端和正在跑的程序
- `codex resume --last`：恢复 Codex 对话上下文，但不是接回原来的终端画面

典型工作流：
```
tmux new -s codex
codex
```

断开 SSH 之后，回到服务器再接回：
```
tmux attach -t codex
```

如果只是想继续最近一次 Codex 会话上下文：
```
codex resume --last
```
