"""Session storage - Save and load sessions"""
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from claude_code.api.types import Message


class SessionStorage:
    """Session storage handler"""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def save_session(self, session_id: str, messages: List[Message], metadata: Dict[str, Any]) -> None:
        """Save a session"""
        session_file = self.session_dir / f"{session_id}.json"

        data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ],
            "metadata": metadata,
        }

        session_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session"""
        session_file = self.session_dir / f"{session_id}.json"

        if not session_file.exists():
            return None

        try:
            data = json.loads(session_file.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, IOError):
            return None

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions"""
        sessions = []

        for session_file in self.session_dir.glob("*.json"):
            try:
                data = json.loads(session_file.read_text(encoding="utf-8"))
                sessions.append({
                    "session_id": data.get("session_id", session_file.stem),
                    "created_at": data.get("created_at", ""),
                    "updated_at": data.get("updated_at", ""),
                })
            except (json.JSONDecodeError, IOError):
                continue

        return sorted(sessions, key=lambda x: x.get("updated_at", ""), reverse=True)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        session_file = self.session_dir / f"{session_id}.json"

        if session_file.exists():
            session_file.unlink()
            return True

        return False