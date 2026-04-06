# Claude Code Python

Python version of Claude Code CLI tool, built on Anthropic API. This project is a Python implementation of claude-code, providing the same functional experience as the original.

## Features

- Interactive TUI interface
- Full Claude API integration (supports official API and compatible APIs)
- File read, write, and edit tools
- Code search with grep
- Bash command execution
- Git command wrappers (commit, review)
- MCP protocol support
- Session management (supports `--continue` to continue session)

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Copy `.env.example` to `.env` and add your API key:

```bash
cp .env.example .env
```

Edit `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

### Run

```bash
# Using module (default: continue previous session)
python -m claude_code.run "your question"

# Interactive mode
python -m claude_code.run --tui

# Single run without saving session
python -m claude_code.run "your question" --once

# Explicitly continue previous session
python -m claude_code.run --continue
```

Or install as editable:

```bash
# Install as editable
pip install -e .

# Then run directly
claude-code "your question"
claude-code --tui
claude-code --continue
```

## Usage Examples

```bash
# Ask a question
python -m claude_code.run "write a quick sort for me"

# Interactive conversation
python -m claude_code.run --tui

# Continue previous session
python -m claude_code.run --continue

# Specify model
python -m claude_code.run "use haiku model" --model claude-haiku-2025-01-24

# Debug mode
python -m claude_code.run "your question" --debug
```

## Project Structure

```
claude_code_python/           # Project root
├── claude_code/              # Main package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                # CLI entry
│   ├── config.py             # Configuration
│   ├── query.py              # Query engine
│   ├── run.py                # Launcher script
│   ├── api/                  # API client
│   ├── commands/             # Commands
│   ├── mcp/                  # MCP support
│   ├── session/              # Session management
│   ├── tools/                # Tools
│   ├── tui/                  # Terminal UI
│   └── utils/                # Utilities
├── README.md
├── README_en.md
├── requirements.txt
└── pyproject.toml
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| ANTHROPIC_API_KEY | Anthropic API key | Required |
| ANTHROPIC_BASE_URL | API endpoint | https://api.anthropic.com |
| ANTHROPIC_MODEL | Default model | claude-sonnet-4-20250514 |
| API_TIMEOUT_MS | Request timeout (ms) | 600000 |
| CLAUDE_SESSION_DIR | Session directory | ~/.claude_py/sessions |
| CLAUDE_PLUGINS_DIR | Plugins directory | ~/.claude_py/plugins |

## Data Storage

- Session directory: `~/.claude_py/sessions`
- Plugins directory: `~/.claude_py/plugins`

Separated from official Claude's `.claude` directory to avoid conflicts.

## License

MIT License