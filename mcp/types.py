"""MCP type definitions"""
from typing import Literal, Optional, Dict, Any, List
from pydantic import BaseModel, Field


class McpServerConfig(BaseModel):
    """MCP server configuration"""
    type: Literal["stdio", "sse", "ws", "http"]
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


class McpTool(BaseModel):
    """MCP tool definition"""
    name: str
    description: str
    input_schema: dict = Field(default_factory=dict)


class McpResource(BaseModel):
    """MCP resource definition"""
    uri: str
    name: str
    description: Optional[str] = None
    mime_type: Optional[str] = None


class McpPrompt(BaseModel):
    """MCP prompt definition"""
    name: str
    description: str
    arguments: Optional[Dict[str, str]] = None


class McpConnectionStatus(BaseModel):
    """MCP connection status"""
    server_name: str
    status: Literal["connected", "failed", "pending", "disabled"]
    error: Optional[str] = None