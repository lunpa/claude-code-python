# Claude Code

一个基于 Anthropic API 的 AI CLI 工具，支持交互式对话和终端操作。

## 功能特性

- 交互式 TUI 界面
- 完整的 Claude API 集成
- 文件读写、编辑工具
- 代码搜索和 grep
- Bash 命令执行
- Git 命令封装（commit、review）
- MCP 协议支持
- 会话管理

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
# 交互模式
python -m claude_code

# 命令行模式
python -m claude_code "你的问题"

# 继续上次会话
python -m claude_code --continue
```

## 项目结构

```
claude_code/
├── api/          # API 客户端
├── cli.py        # CLI 入口
├── commands/     # 命令实现
├── config.py     # 配置管理
├── mcp/          # MCP 协议支持
├── query.py      # 查询引擎
├── session/      # 会话管理
├── tools/        # 工具集
└── tui/          # 终端 UI
```

## 许可证

MIT License