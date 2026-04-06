"""Write tool - Write file contents"""
import os
from pathlib import Path
from typing import Optional

from claude_code.tools.base import BaseTool, ToolResult
from claude_code.api.types import TOOL_WRITE_SCHEMA


class WriteTool(BaseTool):
    """Write file contents"""

    name = "write"
    description = "Write contents to a file at the specified path."
    input_schema = TOOL_WRITE_SCHEMA

    async def execute(self, file_path: str, content: str, **kwargs) -> ToolResult:
        """
        Write content to a file

        Args:
            file_path: The path to the file to write
            content: The content to write

        Returns:
            ToolResult: Success or error
        """
        try:
            path = Path(file_path)

            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            path.write_text(content, encoding="utf-8")
            return ToolResult.ok(f"Written to {file_path}")

        except Exception as e:
            return ToolResult.error(f"Failed to write file: {str(e)}")

    def render_result(self, result: ToolResult) -> str:
        """Render write result"""
        return result.output if result.success else f"[Error] {result.error_msg}"