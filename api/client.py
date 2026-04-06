"""Anthropic API 客户端"""
import anthropic
from typing import List, Optional, AsyncGenerator
import logging

from claude_code.api.types import (
    Message,
    ToolDefinition,
    ClaudeResponse,
    ContentBlock,
    Usage,
)

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Anthropic Claude API 客户端"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.anthropic.com",
        timeout: int = 600000,
    ):
        self.client = anthropic.AsyncAnthropic(
            api_key=api_key,
            base_url=base_url,
            timeout=anthropic.Timeout(timeout / 1000),
        )
        self.default_model = "claude-sonnet-4-20250514"

    async def send_message(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[ToolDefinition]] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
    ) -> ClaudeResponse:
        """发送消息到 Claude API"""
        api_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        tool_definitions = None
        if tools:
            tool_definitions = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                }
                for tool in tools
            ]

        try:
            response = await self.client.messages.create(
                model=model or self.default_model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=api_messages,
                tools=tool_definitions,
            )

            content_blocks = []
            for block in response.content:
                if hasattr(block, "text"):
                    content_blocks.append(
                        ContentBlock(type="text", text=block.text)
                    )
                elif hasattr(block, "name"):
                    content_blocks.append(
                        ContentBlock(
                            type="tool_use",
                            tool_use={
                                "id": block.id,
                                "name": block.name,
                                "input": block.input,
                            },
                        )
                    )

            return ClaudeResponse(
                id=response.id,
                content=content_blocks,
                model=response.model,
                stop_reason=response.stop_reason,
                usage=Usage(
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                ),
            )

        except anthropic.APIConnectionError as e:
            logger.error(f"API 连接错误: {e}")
            raise
        except anthropic.RateLimitError as e:
            logger.error(f"速率限制: {e}")
            raise
        except anthropic.APIStatusError as e:
            logger.error(f"API 状态错误: {e}")
            raise

    async def send_message_stream(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[ToolDefinition]] = None,
        model: Optional[str] = None,
    ) -> AsyncGenerator[ContentBlock, None]:
        """流式发送消息到 Claude API"""
        api_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        tool_definitions = None
        if tools:
            tool_definitions = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                }
                for tool in tools
            ]

        async with self.client.messages.stream(
            model=model or self.default_model,
            max_tokens=4096,
            system=system_prompt,
            messages=api_messages,
            tools=tool_definitions,
        ) as stream:
            async for chunk in stream:
                if chunk.type == "content_block_start":
                    pass
                elif chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, "text"):
                        yield ContentBlock(type="text", text=chunk.delta.text)
                    elif hasattr(chunk.delta, "name"):
                        yield ContentBlock(
                            type="tool_use",
                            tool_use={
                                "id": chunk.delta.id,
                                "name": chunk.delta.name,
                                "input": chunk.delta.input,
                            },
                        )
                elif chunk.type == "content_block_stop":
                    pass