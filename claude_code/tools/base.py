"""工具基类定义"""
from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """工具执行结果"""
    success: bool = True
    output: str = ""
    error_msg: Optional[str] = None

    @classmethod
    def ok(cls, output: str) -> "ToolResult":
        return cls(success=True, output=output)

    @classmethod
    def error(cls, error_msg: str) -> "ToolResult":
        return cls(success=False, output="", error_msg=error_msg)


class BaseTool(ABC):
    """工具基类"""

    name: str = ""
    description: str = ""
    input_schema: dict = Field(default_factory=dict)

    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = working_dir

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具

        Args:
            **kwargs: 工具参数

        Returns:
            ToolResult: 执行结果
        """
        pass

    def validate_input(self, input_data: dict) -> bool:
        """验证输入参数"""
        required = self.input_schema.get("required", [])
        for field in required:
            if field not in input_data:
                return False
        return True

    def render_result(self, result: ToolResult) -> str:
        """渲染工具结果"""
        if result.success:
            return result.output
        return f"Error: {result.error_msg}"

    def get_definition(self) -> dict:
        """获取工具定义"""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


class ReadOnlyTool(BaseTool):
    """只读工具基类"""

    def is_read_only(self) -> bool:
        return True