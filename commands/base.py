"""Command type definitions"""
from typing import Literal, Optional, Callable, Awaitable, Any, List, Dict
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class CommandResult(BaseModel):
    """Command execution result"""
    success: bool = True
    output: str = ""
    error: Optional[str] = None


class BaseCommand(ABC):
    """Base class for commands"""

    name: str = ""
    description: str = ""
    aliases: List[str] = Field(default_factory=list)
    requires_args: bool = False

    @abstractmethod
    async def execute(self, args: str = "") -> CommandResult:
        """Execute the command"""
        pass

    def get_usage(self) -> str:
        """Get command usage string"""
        return f"/{self.name}"


# Type for command handler
CommandHandler = Callable[[str], Awaitable[CommandResult]]


class PromptCommand(BaseCommand):
    """Prompt-type command (AI-generated response)"""

    type: Literal["prompt"] = "prompt"
    prompt_template: str = ""


class LocalCommand(BaseCommand):
    """Local command (direct execution)"""

    type: Literal["local"] = "local"
    handler: Optional[CommandHandler] = None

    async def execute(self, args: str = "") -> CommandResult:
        if self.handler:
            return await self.handler(args)
        return CommandResult(error="Handler not implemented")


# Registry for commands
_command_registry: Dict[str, BaseCommand] = {}


def register_command(command: BaseCommand) -> None:
    """Register a command"""
    _command_registry[command.name] = command
    for alias in command.aliases:
        _command_registry[alias] = command


def get_command(name: str) -> Optional[BaseCommand]:
    """Get a command by name"""
    return _command_registry.get(name)


def get_all_commands() -> Dict[str, BaseCommand]:
    """Get all registered commands"""
    return _command_registry.copy()


def list_commands() -> List[str]:
    """List all command names"""
    return list(_command_registry.keys())