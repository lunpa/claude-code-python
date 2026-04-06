"""Configuration management"""
import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class ClaudeConfig(BaseSettings):
    """Claude Code configuration"""

    # API Configuration
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_auth_token: Optional[str] = Field(default=None, alias="ANTHROPIC_AUTH_TOKEN")
    anthropic_base_url: str = Field(default="https://api.anthropic.com", alias="ANTHROPIC_BASE_URL")
    anthropic_model: str = Field(default="claude-sonnet-4-20250514", alias="ANTHROPIC_MODEL")
    api_timeout_ms: int = Field(default=600000, alias="API_TIMEOUT_MS")

    # Model mappings
    default_sonnet_model: str = Field(default="claude-sonnet-4-20250514", alias="ANTHROPIC_DEFAULT_SONNET_MODEL")
    default_haiku_model: str = Field(default="claude-haiku-2025-01-24", alias="ANTHROPIC_DEFAULT_HAIKU_MODEL")
    default_opus_model: str = Field(default="claude-opus-4-6-20250514", alias="ANTHROPIC_DEFAULT_OPUS_MODEL")

    # Behavior
    disable_telemetry: bool = Field(default=False, alias="DISABLE_TELEMETRY")
    disable_nonessential_traffic: bool = Field(default=False, alias="CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC")

    # Session
    session_dir: Path = Field(
        default=Path.home() / ".claude_py" / "sessions",
        alias="CLAUDE_SESSION_DIR"
    )

    # Plugins
    plugins_dir: Path = Field(
        default=Path.home() / ".claude_py" / "plugins",
        alias="CLAUDE_PLUGINS_DIR"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


def get_config() -> ClaudeConfig:
    """Get global configuration instance"""
    return ClaudeConfig()


def get_api_key(config: Optional[ClaudeConfig] = None) -> str:
    """Get API key from config"""
    cfg = config or get_config()
    if cfg.anthropic_api_key:
        return cfg.anthropic_api_key
    if cfg.anthropic_auth_token:
        return cfg.anthropic_auth_token
    raise ValueError("ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN must be set")


def get_api_base_url(config: Optional[ClaudeConfig] = None) -> str:
    """Get API base URL from config"""
    cfg = config or get_config()
    return cfg.anthropic_base_url


def ensure_directories(config: Optional[ClaudeConfig] = None) -> None:
    """Ensure required directories exist"""
    cfg = config or get_config()
    cfg.session_dir.mkdir(parents=True, exist_ok=True)
    cfg.plugins_dir.mkdir(parents=True, exist_ok=True)