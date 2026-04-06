"""MCP client - Connect to MCP servers"""
import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
from enum import Enum

from claude_code.mcp.types import McpServerConfig, McpTool, McpConnectionStatus

logger = logging.getLogger(__name__)


class TransportType(str, Enum):
    """MCP transport types"""
    STDIO = "stdio"
    SSE = "sse"
    WS = "ws"
    HTTP = "http"


class McpClient:
    """MCP client for connecting to MCP servers"""

    def __init__(self, config: McpServerConfig):
        self.config = config
        self._process: Optional[asyncio.subprocess.Process] = None
        self._connected = False
        self._tools: List[McpTool] = []

    async def connect(self) -> bool:
        """Connect to the MCP server"""
        try:
            if self.config.type == "stdio":
                return await self._connect_stdio()
            elif self.config.type in ("sse", "ws", "http"):
                # TODO: Implement HTTP/WebSocket transports
                logger.warning(f"Transport {self.config.type} not yet implemented")
                return False
            return False
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            return False

    async def _connect_stdio(self) -> bool:
        """Connect via stdio"""
        if not self.config.command:
            return False

        try:
            self._process = await asyncio.create_subprocess_exec(
                self.config.command,
                *(self.config.args or []),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self.config.env,
            )
            self._connected = True

            # Initialize the server
            await self._send_initialize()
            return True

        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            return False

    async def _send_initialize(self) -> None:
        """Send initialize request"""
        request = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "claude-code",
                    "version": "0.1.0",
                },
            },
        }

        if self._process and self._process.stdin:
            self._process.stdin.write(json.dumps(request).encode() + b"\n")
            await self._process.stdin.drain()

        # TODO: Read response and parse tools

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server"""
        if not self._connected:
            return {"error": "Not connected"}

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments,
            },
        }

        if self._process and self._process.stdin:
            self._process.stdin.write(json.dumps(request).encode() + b"\n")
            await self._process.stdin.drain()

            # TODO: Read response
            return {"result": "Tool called"}

        return {"error": "Process not available"}

    async def disconnect(self) -> None:
        """Disconnect from the MCP server"""
        if self._process:
            self._process.terminate()
            await self._process.wait()
            self._connected = False

    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connected

    def get_tools(self) -> List[McpTool]:
        """Get available tools"""
        return self._tools


class McpClientManager:
    """Manage multiple MCP clients"""

    def __init__(self):
        self._clients: Dict[str, McpClient] = {}

    async def add_server(self, name: str, config: McpServerConfig) -> bool:
        """Add and connect to an MCP server"""
        client = McpClient(config)
        success = await client.connect()

        if success:
            self._clients[name] = client

        return success

    async def remove_server(self, name: str) -> bool:
        """Remove an MCP server"""
        if name in self._clients:
            await self._clients[name].disconnect()
            del self._clients[name]
            return True
        return False

    def get_client(self, name: str) -> Optional[McpClient]:
        """Get an MCP client by name"""
        return self._clients.get(name)

    def get_all_tools(self) -> List[McpTool]:
        """Get all tools from all connected servers"""
        tools = []
        for client in self._clients.values():
            tools.extend(client.get_tools())
        return tools

    def get_status(self) -> List[McpConnectionStatus]:
        """Get connection status for all servers"""
        statuses = []
        for name, client in self._clients.items():
            statuses.append(McpConnectionStatus(
                server_name=name,
                status="connected" if client.is_connected() else "failed",
            ))
        return statuses