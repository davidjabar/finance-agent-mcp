from datetime import datetime, timedelta
from typing import Any, Dict, List


class _SessionData:
    def __init__(self) -> None:
        self.messages: List[Any] = []
        self.last_active: datetime = datetime.utcnow()


_sessions: Dict[int, _SessionData] = {}

MAX_HISTORY = 20
SESSION_TTL_MINUTES = 30


def get_messages(telegram_user_id: int) -> List[Any]:
    session = _sessions.get(telegram_user_id)

    if session is None:
        return []

    if _is_expired(session.last_active):
        clear_messages(telegram_user_id)
        return []

    return session.messages


def set_messages(telegram_user_id: int, messages: List[Any]) -> None:
    # Persistent history hanya menyimpan user/assistant messages.
    # Jangan simpan tool messages atau assistant tool-call messages.
    conversation_messages = [
        message
        for message in messages
        if _get_role(message) in ("user", "assistant")
    ]

    # Keep the latest MAX_HISTORY conversation messages.
    trimmed = (
        conversation_messages[-MAX_HISTORY:]
        if len(conversation_messages) > MAX_HISTORY
        else conversation_messages
    )

    session = _sessions.setdefault(telegram_user_id, _SessionData())
    session.messages = trimmed
    session.last_active = datetime.utcnow()

def clear_messages(telegram_user_id: int) -> None:
    _sessions.pop(telegram_user_id, None)


def _is_expired(last_active: datetime) -> bool:
    return datetime.utcnow() - last_active > timedelta(minutes=SESSION_TTL_MINUTES)


def _get_role(message: Any) -> str:
    if isinstance(message, dict):
        role = message.get("role", "")

        # Normalize OpenAI-style roles
        if role == "human":
            return "user"
        if role == "ai":
            return "assistant"

        return role

    message_type = getattr(message, "type", "")

    # Normalize LangChain message types
    if message_type == "human":
        return "user"

    if message_type == "ai":
        return "assistant"

    return message_type