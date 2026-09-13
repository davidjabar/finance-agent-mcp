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
    # NOTE: trimming simpel begini secara teori bisa "memotong" di tengah
    # pasangan tool_call/tool_result kalau history kepanjangan. Untuk personal
    # use dengan MAX_HISTORY=20 ini masih longgar & jarang jadi masalah nyata,
    # tapi worth diketahui kalau nanti ada error aneh soal "orphaned tool call".
    trimmed = messages[-MAX_HISTORY:] if len(messages) > MAX_HISTORY else messages

    session = _sessions.setdefault(telegram_user_id, _SessionData())
    session.messages = trimmed
    session.last_active = datetime.utcnow()


def clear_messages(telegram_user_id: int) -> None:
    _sessions.pop(telegram_user_id, None)


def _is_expired(last_active: datetime) -> bool:
    return datetime.utcnow() - last_active > timedelta(minutes=SESSION_TTL_MINUTES)


def _get_role(message: Any) -> str:
    if isinstance(message, dict):
        return message.get("role", "")
    return getattr(message, "type", "")  # LangChain BaseMessage: system/human/ai/tool