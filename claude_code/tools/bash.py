"""Bash tool - Execute shell commands"""
import asyncio
import os
import sys
import shutil
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path
from typing import Optional, Any, Tuple

from claude_code.tools.base import BaseTool, ToolResult
from claude_code.api.types import TOOL_BASH_SCHEMA

# Thread pool for running subprocesses
_executor = ThreadPoolExecutor(max_workers=4)

# Default timeout for commands (60 seconds)
DEFAULT_TIMEOUT = 60


class BashTool(BaseTool):
    """Execute shell commands"""

    name = "bash"
    description = "Execute a shell command in the terminal."
    input_schema = TOOL_BASH_SCHEMA

    def __init__(self, working_dir: Optional[str] = None):
        super().__init__(working_dir)
        # Detect shell - prefer bash on Windows if available
        if sys.platform == "win32":
            # Try to find bash (Git for Windows, WSL, etc.)
            bash_path = shutil.which("bash")
            if bash_path:
                self.shell = bash_path
            else:
                self.shell = "cmd.exe"
        else:
            self.shell = os.getenv("SHELL", "/bin/bash")

    def _run_subprocess(self, command: str, cwd: str, timeout: int) -> Tuple[int, str, str, str]:
        """Run subprocess in thread pool (synchronous) with timeout"""
        process = None
        try:
            # On Windows, use cmd.exe /c
            if sys.platform == "win32":
                cmd_parts = ["cmd.exe", "/c", command]
            else:
                cmd_parts = command

            # Use Popen to support timeout
            process = subprocess.Popen(
                cmd_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                env=os.environ.copy(),
                shell=False,
                encoding="utf-8",
                errors="replace",
                text=True,
            )

            # Wait for process with timeout
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return process.returncode, stdout, stderr, ""
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                return -1, "", "", f"Command timed out after {timeout} seconds (process killed)"

        except Exception as e:
            if process:
                try:
                    process.kill()
                except:
                    pass
            return 1, "", "", str(e)

    async def execute(self, command: str = None, description: str = "", workdir: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT, **kwargs: Any) -> ToolResult:
        """Execute a shell command

        Args:
            command: The shell command to execute
            description: A brief description of what this command does
            workdir: The working directory
            timeout: Maximum seconds to wait (default 60)

        Returns:
            ToolResult: Command output
        """
        if not command:
            return ToolResult.error("No command provided")

        cwd = workdir or self.working_dir or os.getcwd()

        try:
            # Run subprocess in thread pool with timeout
            loop = asyncio.get_event_loop()
            returncode, stdout, stderr, error_msg = await asyncio.wait_for(
                loop.run_in_executor(
                    _executor, self._run_subprocess, command, cwd, timeout
                ),
                timeout=timeout + 10  # Extra margin for executor overhead
            )

            output = ""
            if stdout:
                output += stdout
            if stderr:
                output += "\n[stderr]\n" + stderr

            # Check for timeout or other errors
            if error_msg:
                return ToolResult.error(error_msg)

            if returncode != 0:
                return ToolResult.error(output or f"Command exited with code {returncode}")

            return ToolResult.ok(output)

        except asyncio.TimeoutError:
            return ToolResult.error(f"Command timed out after {timeout} seconds")
        except Exception as e:
            return ToolResult.error(f"Failed to execute command: {str(e)}")

    def render_result(self, result: ToolResult) -> str:
        """Render bash result with minimal formatting"""
        if result.success:
            return result.output if result.output else "(no output)"
        return f"[Error] {result.error_msg}"