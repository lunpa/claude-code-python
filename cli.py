"""CLI entry point"""
import asyncio
import logging
import sys
import platform
from typing import Optional

import click
from rich.console import Console

# Fix Windows asyncio proactor event loop issue
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from claude_code.config import get_config, get_api_key, ensure_directories
from claude_code.api.client import ClaudeClient
from claude_code.api.types import Message
from claude_code.tools.registry import get_all_tools
from claude_code.query import run_query, QueryEngine

console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--config", "config_path", help="Path to config file")
@click.pass_context
def cli(ctx, debug, config_path):
    """Claude Code - AI CLI Tool"""
    # Setup minimal logging to avoid interfering with output
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    else:
        # Disable most logging
        logging.getLogger("claude_code").setLevel(logging.WARNING)
        logging.getLogger("anthropic").setLevel(logging.WARNING)

    # Ensure directories exist
    ensure_directories()

    # Store config in context
    ctx.ensure_object(dict)
    ctx.obj["config"] = get_config()


@cli.command()
@click.argument("prompt", required=False)
@click.option("-p", "--print", "headless", is_flag=True, help="Print mode (non-interactive)")
@click.option("--continue", "continue_session", is_flag=True, help="Continue previous session")
@click.option("--model", help="Model to use")
@click.pass_context
def main(ctx, prompt, headless, continue_session, model):
    """Start Claude Code"""
    config = ctx.obj["config"]

    # Get API key
    try:
        api_key = get_api_key(config)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("\nPlease set ANTHROPIC_API_KEY in .env file or environment variable.")
        sys.exit(1)

    if headless:
        # Headless mode
        if not prompt:
            console.print("[red]Error:[/red] Prompt required in print mode")
            sys.exit(1)
        run_headless(prompt, config, api_key, model, continue_session)
    else:
        # TUI mode
        run_tui(config, api_key, model, continue_session)


async def async_main(
    prompt: str,
    config,
    api_key: str,
    model: Optional[str] = None,
    continue_session: bool = False,
):
    """Async main function"""
    # Initialize client
    client = ClaudeClient(
        api_key=api_key,
        base_url=config.anthropic_base_url,
        timeout=config.api_timeout_ms,
    )

    # Get tools
    tools = get_all_tools()

    # Build messages
    messages = [Message(role="user", content=prompt)]

    # Create engine and run query
    engine = QueryEngine(client=client, model=model or config.anthropic_model)
    engine.tools = tools

    # Run initial query
    await run_query(client, messages, tools, model or config.anthropic_model)

    # Sync messages from run_query to engine for continue_session
    if continue_session:
        engine.messages = messages.copy()

    # If continuing session, enter interactive loop
    if continue_session:
        while True:
            try:
                # Use asyncio to run input in thread
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("\n> ").strip()
                )
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit", "q"]:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                await engine.chat(user_input)
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]Goodbye![/yellow]")
                break


def run_headless(
    prompt: str,
    config,
    api_key: str,
    model: Optional[str] = None,
    continue_session: bool = False,
):
    """Run in headless mode"""
    try:
        asyncio.run(async_main(prompt, config, api_key, model, continue_session))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


def run_tui(config, api_key: str, model: Optional[str], continue_session: bool):
    """Run TUI mode"""
    try:
        from claude_code.tui.app import ClaudeApp

        app = ClaudeApp(
            api_key=api_key,
            base_url=config.anthropic_base_url,
            model=model or config.anthropic_model,
        )
        app.run()
    except ImportError as e:
        console.print(f"[red]Error:[/red] Failed to import TUI: {e}")
        console.print("Installing textual: pip install textual")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


def main_entry():
    """Entry point for the CLI"""
    cli(obj={})


if __name__ == "__main__":
    main_entry()