"""Read tool - Read file contents"""
import os
from pathlib import Path
from typing import Optional

from claude_code.tools.base import BaseTool, ToolResult
from claude_code.api.types import TOOL_READ_SCHEMA


class ReadTool(BaseTool):
    """Read file contents"""

    name = "read"
    description = "Read the contents of a file from the file system."
    input_schema = TOOL_READ_SCHEMA

    async def execute(
        self,
        file_path: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> ToolResult:
        """
        Read a file

        Args:
            file_path: The path to the file to read
            offset: The line number to start reading from
            limit: The number of lines to read

        Returns:
            ToolResult: File contents
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return ToolResult.error(f"File not found: {file_path}")

            if path.is_dir():
                return ToolResult.error(f"Path is a directory: {file_path}")

            content = path.read_text(encoding="utf-8")
            lines = content.splitlines()

            # Apply offset and limit
            if offset is not None:
                lines = lines[offset - 1:]  # Convert to 0-indexed
            if limit is not None:
                lines = lines[:limit]

            output = "\n".join(lines)
            return ToolResult.ok(output)

        except Exception as e:
            return ToolResult.error(f"Failed to read file: {str(e)}")

    def render_result(self, result: ToolResult) -> str:
        """Render file contents"""
        return result.output