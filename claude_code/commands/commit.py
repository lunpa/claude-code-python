"""Commit command - Generate commit messages"""
import asyncio
from pathlib import Path

from claude_code.commands.base import BaseCommand, CommandResult, LocalCommand
from claude_code.api.client import ClaudeClient
from claude_code.api.types import Message


class CommitCommand(LocalCommand):
    """Generate git commit message"""

    name = "commit"
    description = "Generate a git commit message from staged changes"
    aliases = ["ci"]

    def __init__(self, api_client: ClaudeClient = None):
        super().__init__()
        self.api_client = api_client

    async def execute(self, args: str = "") -> CommandResult:
        """Execute the commit command"""
        try:
            # Get git diff
            process = await asyncio.create_subprocess_exec(
                "git", "diff", "--cached",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            diff = stdout.decode("utf-8", errors="replace")
            if not diff:
                return CommandResult(
                    success=False,
                    error="No staged changes. Use 'git add' to stage files.",
                )

            # Generate commit message
            if self.api_client:
                messages = [
                    Message(
                        role="user",
                        content=f"Generate a concise git commit message for these changes:\n\n{diff}",
                    )
                ]

                response = await self.api_client.send_message(
                    messages=messages,
                    system_prompt="You are a git commit message generator. Generate a short, conventional commit message. First line should be under 72 characters.",
                    model="claude-haiku-2025-01-24",
                )

                if response.content and response.content[0].text:
                    commit_message = response.content[0].text.strip()
                    return CommandResult(output=commit_message)

            return CommandResult(
                success=False,
                error="API client not available",
            )

        except Exception as e:
            return CommandResult(success=False, error=str(e))

    def get_usage(self) -> str:
        return "/commit - Generate commit message for staged changes"