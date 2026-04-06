"""Edit tool - Edit file contents"""
import os
from pathlib import Path
from typing import Optional

from claude_code.tools.base import BaseTool, ToolResult
from claude_code.api.types import TOOL_EDIT_SCHEMA


class EditTool(BaseTool):
    """Edit file contents"""

    name = "edit"
    description = "Make edits to an existing file."
    input_schema = TOOL_EDIT_SCHEMA

    async def execute(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
        **kwargs,
    ) -> ToolResult:
        """
        Edit a file

        Args:
            file_path: The path to the file to edit
            old_string: The text to replace
            new_string: The replacement text
            replace_all: Replace all occurrences

        Returns:
            ToolResult: Success or error message
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return ToolResult.error(f"File not found: {file_path}")

            content = path.read_text(encoding="utf-8")

            if replace_all:
                if old_string not in content:
                    return ToolResult.error(f"String not found: {old_string}")
                new_content = content.replace(old_string, new_string)
            else:
                if old_string not in content:
                    return ToolResult.error(f"String not found: {old_string}")
                new_content = content.replace(old_string, new_string, 1)

            path.write_text(new_content, encoding="utf-8")
            return ToolResult.ok(f"Edited {file_path}")

        except Exception as e:
            return ToolResult.error(f"Failed to edit file: {str(e)}")

    def render_result(self, result: ToolResult) -> str:
        """Render edit result"""
        return result.output if result.success else f"[Error] {result.error_msg}"