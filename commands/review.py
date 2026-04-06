"""Review command - Code review"""
import asyncio

from claude_code.commands.base import BaseCommand, CommandResult, LocalCommand


class ReviewCommand(LocalCommand):
    """Review code changes"""

    name = "review"
    description = "Review code changes using git diff"
    aliases = ["pr", "code-review"]

    async def execute(self, args: str = "") -> CommandResult:
        """Execute the review command"""
        try:
            # Get git diff
            process = await asyncio.create_subprocess_exec(
                "git", "diff",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            diff = stdout.decode("utf-8", errors="replace")
            if not diff:
                return CommandResult(
                    success=False,
                    error="No uncommitted changes to review.",
                )

            # For now, just show the diff
            # In full implementation, would send to Claude for review
            return CommandResult(
                output=f"[Code Review]\n\n{diff[:5000]}",  # Limit output
            )

        except Exception as e:
            return CommandResult(success=False, error=str(e))

    def get_usage(self) -> str:
        return "/review - Review uncommitted changes"