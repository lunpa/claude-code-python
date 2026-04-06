"""Session manager - Manage conversation sessions"""
import uuid
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from claude_code.api.types import Message
from claude_code.session.storage import SessionStorage


class SessionManager:
    """Session manager for handling conversation sessions"""

    def __init__(self, session_dir: Path):
        self.storage = SessionStorage(session_dir)
        self.current_session_id: Optional[str] = None
        self.current_messages: List[Message] = []

    def create_session(self) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())[:8]
        self.current_session_id = session_id
        self.current_messages = []
        return session_id

    def load_session(self, session_id: str) -> Optional[List[Message]]:
        """Load an existing session"""
        data = self.storage.load_session(session_id)
        if data is None:
            return None

        self.current_session_id = session_id
        self.current_messages = [
            Message(role=m["role"], content=m["content"])
            for m in data.get("messages", [])
        ]

        return self.current_messages

    def save_current_session(self, metadata: dict = None) -> None:
        """Save the current session"""
        if self.current_session_id is None:
            return

        self.storage.save_session(
            self.current_session_id,
            self.current_messages,
            metadata or {},
        )

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the current session"""
        self.current_messages.append(Message(role=role, content=content))

    def list_sessions(self) -> List[dict]:
        """List all sessions"""
        return self.storage.list_sessions()

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        return self.storage.delete_session(session_id)

    def get_current_session_id(self) -> Optional[str]:
        """Get the current session ID"""
        return self.current_session_id

    def get_messages(self) -> List[Message]:
        """Get messages for current session"""
        return self.current_messages