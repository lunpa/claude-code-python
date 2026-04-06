"""Grep tool - Search file contents"""
import os
import re
from pathlib import Path
from typing import Optional, List

from claude_code.tools.base import BaseTool, ToolResult
from claude_code.api.types import TOOL_GREP_SCHEMA


class GrepTool(BaseTool):
    """Search file contents using regex"""

    name = "grep"
    description = "Search for text in files using regular expressions."
    input_schema = TOOL_GREP_SCHEMA

    async def execute(
        self,
        pattern: str,
        path: Optional[str] = None,
        glob: Optional[str] = None,
        case_insensitive: bool = False,
        **kwargs,
    ) -> ToolResult:
        """
        Search for pattern in files

        Args:
            pattern: The regex pattern to search for
            path: The directory to search in
            glob: A glob pattern to filter files
            case_insensitive: Case insensitive search

        Returns:
            ToolResult: Search results
        """
        try:
            search_path = Path(path) if path else Path(self.working_dir or os.getcwd())

            if not search_path.exists():
                return ToolResult.error(f"Directory not found: {path or '.'}")

            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)

            matches: List[str] = []

            for file_path in search_path.rglob(glob or "*"):
                if not file_path.is_file():
                    continue

                # Skip binary files
                try:
                    content = file_path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, PermissionError):
                    continue

                for line_num, line in enumerate(content.splitlines(), 1):
                    if regex.search(line):
                        relative_path = file_path.relative_to(search_path)
                        matches.append(f"{relative_path}:{line_num}: {line.rstrip()}")

            if not matches:
                return ToolResult.ok(f"No matches found for '{pattern}'")

            output = "\n".join(matches)
            return ToolResult.ok(output)

        except re.error as e:
            return ToolResult.error(f"Invalid regex: {e}")
        except Exception as e:
            return ToolResult.error(f"Failed to grep: {str(e)}")

    def render_result(self, result: ToolResult) -> str:
        """Render grep result"""
        return result.output