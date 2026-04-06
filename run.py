#!/usr/bin/env python
"""Simple runner for Claude Code"""
import sys


def main():
    # All arguments after run.py are passed to claude-code
    if len(sys.argv) == 1:
        print("Usage: claude_code.exe \"your prompt\" [--continue]")
        print("       claude_code.exe --tui")
        sys.exit(1)

    args = sys.argv[1:]

    # Import and call the CLI directly instead of subprocess
    from claude_code.cli import main_entry
    # Use -p (print/headless mode) when a prompt is provided
    sys.argv = ["claude-code", "main", "-p"] + args
    main_entry()


if __name__ == "__main__":
    main()