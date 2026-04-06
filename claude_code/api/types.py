"""API type definitions"""
from typing import Optional, Literal, Any, List
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message"""
    role: Literal["user", "assistant", "system"]
    content: str


class ToolDefinition(BaseModel):
    """Tool definition for API"""
    name: str
    description: str
    input_schema: dict = Field(default_factory=dict)


class ToolUse(BaseModel):
    """Tool use from API response"""
    id: str
    name: str
    input: dict = Field(default_factory=dict)


class ToolResultMessage(BaseModel):
    """Tool result message"""
    type: Literal["tool_result"] = "tool_result"
    tool_use_id: str
    content: str
    is_error: bool = False


class ContentBlock(BaseModel):
    """Content block in API response"""
    type: Literal["text", "tool_use", "tool_result"]
    text: Optional[str] = None
    tool_use: Optional[dict] = None
    tool_result: Optional[dict] = None


class Usage(BaseModel):
    """Token usage"""
    input_tokens: int = 0
    output_tokens: int = 0


class ClaudeResponse(BaseModel):
    """Claude API response"""
    id: str
    type: str = "message"
    role: Literal["assistant"] = "assistant"
    content: List[ContentBlock] = Field(default_factory=list)
    model: str
    stop_reason: Optional[str] = None
    stop_sequence: Optional[str] = None
    usage: Usage = Field(default_factory=Usage)


# Tool input/output schemas
TOOL_BASH_SCHEMA = {
    "type": "object",
    "properties": {
        "command": {
            "type": "string",
            "description": "The shell command to execute"
        },
        "description": {
            "type": "string",
            "description": "A brief description of what this command does"
        },
        "workdir": {
            "type": "string",
            "description": "The working directory to execute the command in"
        }
    },
    "required": ["command"]
}

TOOL_READ_SCHEMA = {
    "type": "object",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "The path to the file to read"
        },
        "offset": {
            "type": "integer",
            "description": "The line number to start reading from"
        },
        "limit": {
            "type": "integer",
            "description": "The number of lines to read"
        }
    },
    "required": ["file_path"]
}

TOOL_WRITE_SCHEMA = {
    "type": "object",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "The path to the file to write"
        },
        "content": {
            "type": "string",
            "description": "The content to write to the file"
        }
    },
    "required": ["file_path", "content"]
}

TOOL_EDIT_SCHEMA = {
    "type": "object",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "The path to the file to edit"
        },
        "old_string": {
            "type": "string",
            "description": "The text to replace"
        },
        "new_string": {
            "type": "string",
            "description": "The replacement text"
        },
        "replace_all": {
            "type": "boolean",
            "description": "Replace all occurrences",
            "default": False
        }
    },
    "required": ["file_path", "old_string", "new_string"]
}

TOOL_GLOB_SCHEMA = {
    "type": "object",
    "properties": {
        "pattern": {
            "type": "string",
            "description": "The glob pattern to search for"
        },
        "path": {
            "type": "string",
            "description": "The directory to search in"
        }
    },
    "required": ["pattern"]
}

TOOL_GREP_SCHEMA = {
    "type": "object",
    "properties": {
        "pattern": {
            "type": "string",
            "description": "The regex pattern to search for"
        },
        "path": {
            "type": "string",
            "description": "The directory to search in"
        },
        "glob": {
            "type": "string",
            "description": "A glob pattern to filter files"
        },
        "-i": {
            "type": "boolean",
            "description": "Case insensitive search",
            "default": False
        }
    },
    "required": ["pattern"]
}