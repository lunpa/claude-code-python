# Claude Code Python

Python 版本的 Claude Code CLI 工具，基于 Anthropic API 实现。本项目是 claude-code 的 Python 实现版本，提供与原版相同的功能体验。

## 功能特性

- 交互式 TUI 界面
- 完整的 Claude API 集成（支持官方 API 及兼容 API）
- 文件读写、编辑工具
- 代码搜索和 grep
- Bash 命令执行
- Git 命令封装（commit、review）
- MCP 协议支持
- 会话管理（支持 `--continue` 继续会话）

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境

复制 `.env.example` 为 `.env` 并填入你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

### 运行

```bash
# 使用模块方式运行（默认继续上次会话）
python -m claude_code.run "你的问题"

# 交互模式
python -m claude_code.run --tui

# 单次运行，不保存会话
python -m claude_code.run "你的问题" --once

# 显式继续上次会话
python -m claude_code.run --continue
```

或者直接运行：

```bash
# 安装为可编辑模式
pip install -e .

# 然后可以直接运行
claude-code "你的问题"
claude-code --tui
claude-code --continue
```

## 使用示例

```bash
# 问一个问题
python -m claude_code.run "帮我写一个快速排序"

# 交互式对话
python -m claude_code.run --tui

# 继续之前的会话
python -m claude_code.run --continue

# 指定模型
python -m claude_code.run "用 haiku 模型" --model claude-haiku-2025-01-24

# 调试模式
python -m claude_code.run "你的问题" --debug
```

## 项目结构

```
claude_code_python/           # 项目根目录
├── claude_code/              # 主代码包
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                # CLI 入口
│   ├── config.py             # 配置管理
│   ├── query.py              # 查询引擎
│   ├── run.py                # 启动脚本
│   ├── api/                  # API 客户端
│   ├── commands/             # 命令实现
│   ├── mcp/                  # MCP 协议支持
│   ├── session/              # 会话管理
│   ├── tools/                # 工具集
│   ├── tui/                  # 终端 UI
│   └── utils/                # 工具函数
├── README.md
├── README_en.md
├── requirements.txt
└── pyproject.toml
```

## 配置说明

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| ANTHROPIC_API_KEY | Anthropic API 密钥 | 必填 |
| ANTHROPIC_BASE_URL | API 地址 | https://api.anthropic.com |
| ANTHROPIC_MODEL | 默认模型 | claude-sonnet-4-20250514 |
| API_TIMEOUT_MS | 请求超时(毫秒) | 600000 |
| CLAUDE_SESSION_DIR | Session 目录 | ~/.claude_py/sessions |
| CLAUDE_PLUGINS_DIR | Plugins 目录 | ~/.claude_py/plugins |

## 数据存储

- Session 目录：`~/.claude_py/sessions`
- Plugins 目录：`~/.claude_py/plugins`

与官方 Claude 的 `.claude` 目录区分开，避免冲突。

## 许可证

MIT License