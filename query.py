"""Query engine - Main conversation loop with tool execution"""
import asyncio
import logging
import sys
from typing import List, Optional, Dict, Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule

# Console with proper output handling
console = Console(force_terminal=True)

from claude_code.api.client import ClaudeClient
from claude_code.api.types import (
    Message,
    ContentBlock,
    ToolDefinition,
)
from claude_code.tools.base import BaseTool, ToolResult
from claude_code.tools.registry import get_all_tools

logger = logging.getLogger(__name__)


class QueryEngine:
    """Query engine for handling conversation and tool execution"""

    def __init__(
        self,
        client: ClaudeClient,
        model: str,
        system_prompt: Optional[str] = None,
    ):
        self.client = client
        self.model = model
        self.system_prompt = system_prompt or get_default_system_prompt()
        self.tools = get_all_tools()
        self.messages: List[Message] = []

    async def chat(self, user_input: str) -> None:
        """Process a user message and handle the response"""
        # Show user input
        print(f"\n>>> {user_input}\n")

        # Add user message
        self.messages.append(Message(role="user", content=user_input))

        # Send to API
        await self._send_message()

    async def _send_message(self, depth: int = 0) -> None:
        """Send message to API and handle response"""
        # Prevent infinite recursion
        if depth > 20:
            print("Error: Maximum conversation depth reached")
            return

        # Convert tools to definitions
        api_tools = [
            ToolDefinition(
                name=tool.name,
                description=tool.description,
                input_schema=tool.input_schema,
            )
            for tool in self.tools
        ]

        # Show thinking indicator
        with console.status("[bold yellow]Thinking...", spinner="dots"):
            response = await self.client.send_message(
                messages=self.messages,
                system_prompt=self.system_prompt,
                tools=api_tools,
                model=self.model,
            )

        # Check if we should stop
        print(f"DEBUG: stop_reason={response.stop_reason}, blocks={len(response.content)}")
        if response.stop_reason == "end_turn":
            # Just print final text if any, then return
            for block in response.content:
                if block.type == "text" and block.text:
                    print("\n" + block.text + "\n")
                    self.messages.append(Message(role="assistant", content=block.text))
            print("\n[对话结束]\n")
            return

        # Process response content
        has_tool_use = False
        for block in response.content:
            if block.type == "text" and block.text:
                # Print assistant's text response
                print("\n" + block.text + "\n")

                # Add to message history
                self.messages.append(
                    Message(role="assistant", content=block.text)
                )

            elif block.type == "tool_use" and block.tool_use:
                has_tool_use = True
                tool_name = block.tool_use.get("name")
                # Handle tool call
                await self._handle_tool_use(block.tool_use, depth + 1)

        # If no tool use, we're done for this turn
        if not has_tool_use:
            print("---")

    async def _handle_tool_use(self, tool_use: Dict[str, Any], depth: int = 0) -> None:
        """Handle a tool use request from the API"""
        tool_name = tool_use.get("name")
        tool_input = tool_use.get("input", {})
        tool_id = tool_use.get("id")

        # Show tool call header
        print(f"\n--- Calling tool: {tool_name} ---")

        # Find the tool
        tool = self._find_tool(tool_name)
        if not tool:
            error_msg = f"Tool not found: {tool_name}"
            print(f"Error: {error_msg}")
            self._add_tool_result(tool_id, error_msg, is_error=True)
            return

        # Execute the tool
        try:
            result = await tool.execute(**tool_input)

            # Show result
            if result.success:
                output = result.output if result.output else "(no output)"
                print(f"\nResult:\n{output}\n")
            else:
                print(f"\nError: {result.error_msg}\n")

            # Add result to messages
            self._add_tool_result(
                tool_id,
                result.output if result.success else result.error_msg or "Error",
                is_error=not result.success,
            )

        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            print(f"Error: {error_msg}")
            self._add_tool_result(tool_id, error_msg, is_error=True)

        # Continue conversation with tool results
        await self._send_message(depth + 1)

    def _add_tool_result(self, tool_id: str, content: str, is_error: bool = False) -> None:
        """Add a tool result message"""
        self.messages.append(
            Message(
                role="user",
                content=f"[Tool Result for {tool_id}]: {content}"
            )
        )

    def _find_tool(self, name: str) -> Optional[BaseTool]:
        """Find a tool by name"""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None


async def run_query(
    client: ClaudeClient,
    messages: List[Message],
    tools: List[BaseTool],
    model: str,
) -> None:
    """Run a simple query"""
    engine = QueryEngine(
        client=client,
        model=model,
    )
    engine.tools = tools

    if messages:
        for msg in messages:
            if msg.role == "user":
                await engine.chat(msg.content)


def get_default_system_prompt() -> str:
    """Get the default system prompt"""
    return """You are Claude Code, an AI programming assistant.

You have access to a set of tools that you can use to interact with the user's file system and execute commands.

Available tools:
- bash: Execute shell commands
- read: Read file contents
- write: Write content to files
- edit: Edit existing files
- glob: Find files matching a pattern
- grep: Search for text in files

When you need to perform actions, use the appropriate tools. Always be helpful and accurate."""