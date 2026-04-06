#!/usr/bin/env python
"""Simple runner for Claude Code

Usage:
    python run.py "your prompt"           # 默认继续上次会话
    python run.py "your prompt" --once    # 单次运行，不保存会话
    python run.py --tui                   # 交互模式
    python run.py --continue              # 继续上次会话
"""
import sys


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: claude_code.exe \"your prompt\" [--once]")
        print("       claude_code.exe --tui")
        print("       claude_code.exe --continue")
        print()
        print("默认行为：继续上次会话 (--continue)")
        print("单次运行：使用 --once 参数")
        sys.exit(1)

    # Check for special flags
    if "--tui" in args:
        from claude_code.cli import main_entry
        sys.argv = ["claude-code", "main"] + args
        main_entry()
        return

    # Default: use --continue (session mode)
    # Use --once for single-run mode
    run_once = "--once" in args
    if run_once:
        args.remove("--once")

    from claude_code.cli import main_entry

    if args:
        # Has prompt - headless mode
        sys.argv = ["claude-code", "main", "-p"]
        if not run_once:
            sys.argv.append("--continue")
        sys.argv.extend(args)
    else:
        # No prompt
        if not run_once:
            sys.argv = ["claude-code", "main", "--continue"]
        else:
            sys.argv = ["claude-code", "main"]

    main_entry()


if __name__ == "__main__":
    main()