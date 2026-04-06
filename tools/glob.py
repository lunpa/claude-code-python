"""Glob tool - File pattern matching"""
import os
from pathlib import Path
from typing import Optional
import fnmatch

from claude_code.tools.base import BaseTool, ToolResult
from claude_code.api.types import TOOL_GLOB_SCHEMA


class GlobTool(BaseTool):
    """Glob file pattern matching"""

    name = "glob"
    description = "List files in a directory matching a pattern."
    input_schema = TOOL_GLOB_SCHEMA

    async def execute(self, pattern: str, path: Optional[str] = None, **kwargs) -> ToolResult:
        """
        Search for files matching a glob pattern

        Args:
            pattern: The glob pattern to search for
            path: The directory to search in

        Returns:
            ToolResult: List of matching files
        """
        try:
            search_path = Path(path) if path else Path(self.working_dir or os.getcwd())

            if not search_path.exists():
                return ToolResult.error(f"Directory not found: {path or '.'}")

            matches = []
            for item in search_path.rglob(pattern):
                if item.is_file():
                    matches.append(str(item.relative_to(search_path)))

            if not matches:
                return ToolResult.ok(f"No files matching '{pattern}'")

            output = "\n".join(sorted(matches))
            return ToolResult.ok(output)

        except Exception as e:
            return ToolResult.error(f"Failed to glob: {str(e)}")

    def render_result(self, result: ToolResult) -> str:
        """Render glob result"""
        return result.output