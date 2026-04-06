"""Tool registry - Manage available tools"""
from typing import Dict, List, Optional, Type
from claude_code.tools.base import BaseTool, ToolResult
from claude_code.tools.bash import BashTool
from claude_code.tools.read import ReadTool
from claude_code.tools.write import WriteTool
from claude_code.tools.edit import EditTool
from claude_code.tools.glob import GlobTool
from claude_code.tools.grep import GrepTool


class ToolRegistry:
    """Tool registry for managing available tools"""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._tool_classes: Dict[str, Type[BaseTool]] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register default built-in tools"""
        default_tools = [
            BashTool,
            ReadTool,
            WriteTool,
            EditTool,
            GlobTool,
            GrepTool,
        ]
        for tool_class in default_tools:
            self.register_tool_class(tool_class)

    def register_tool_class(self, tool_class: Type[BaseTool]) -> None:
        """Register a tool class"""
        instance = tool_class()
        self._tool_classes[instance.name] = tool_class

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool instance"""
        self._tools[tool.name] = tool

    def get_tool(self, name: str, working_dir: Optional[str] = None) -> Optional[BaseTool]:
        """Get a tool by name"""
        # Return existing instance if available
        if name in self._tools:
            return self._tools[name]

        # Create new instance from class
        if name in self._tool_classes:
            tool_class = self._tool_classes[name]
            return tool_class(working_dir=working_dir)

        return None

    def get_all_tools(self, working_dir: Optional[str] = None) -> List[BaseTool]:
        """Get all available tools"""
        tools = []
        for name in self._tool_classes:
            tool = self.get_tool(name, working_dir)
            if tool:
                tools.append(tool)
        return tools

    def get_tool_definitions(self) -> List[dict]:
        """Get tool definitions for API"""
        definitions = []
        for name in self._tool_classes:
            tool_class = self._tool_classes[name]
            instance = tool_class()
            definitions.append(instance.get_definition())
        return definitions


# Global registry instance
_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    """Get global tool registry"""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry


def get_all_tools(working_dir: Optional[str] = None) -> List[BaseTool]:
    """Get all available tools"""
    return get_registry().get_all_tools(working_dir)


def get_tool(name: str, working_dir: Optional[str] = None) -> Optional[BaseTool]:
    """Get a tool by name"""
    return get_registry().get_tool(name, working_dir)