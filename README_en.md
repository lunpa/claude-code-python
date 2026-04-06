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

### Run (Recommended: use run.py)

```bash
# Direct run (simplest way)
python run.py "your question"

# Interactive mode
python run.py --tui

# Continue previous session (main usage)
python run.py --continue
python run.py "continue previous task" --continue
```

Or use the standard Python module approach:

```bash
# Command line mode
python -m claude_code "your question"

# Interactive mode
python -m claude_code

# Continue previous session
python -m claude_code --continue
```

## Usage Examples

```bash
# Ask a question
python run.py "write a quick sort for me"

# Interactive conversation
python run.py --tui

# Continue previous session
python run.py --continue

# Specify model
python run.py "use haiku model" --model claude-haiku-2025-01-24

# Debug mode
python run.py "your question" --debug
```

## Project Structure

```
claude_code/
├── api/          # API client
├── cli.py        # CLI entry
├── commands/     # Command implementations
├── config.py     # Configuration management
├── mcp/          # MCP protocol support
├── query.py      # Query engine
├── run.py        # Convenience launcher script
├── session/      # Session management
├── tools/        # Tool collection
└── tui/          # Terminal UI
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| ANTHROPIC_API_KEY | Anthropic API key | Required |
| ANTHROPIC_BASE_URL | API endpoint | https://api.anthropic.com |
| ANTHROPIC_MODEL | Default model | claude-sonnet-4-20250514 |
| API_TIMEOUT_MS | Request timeout (ms) | 600000 |

## License

MIT License