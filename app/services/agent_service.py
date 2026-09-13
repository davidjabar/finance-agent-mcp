from app.core.agent import get_agent
from app.core.config import settings
from app.core.prompts import build_system_prompt
from app.core.session_store import get_messages, set_messages, _get_role


async def handle_chat(user_text: str) -> str:
    
    telegram_user_id = settings.OWNER_TELEGRAM_ID
    agent = await get_agent()

    history = get_messages(telegram_user_id)
    # buang system message lama (kalau ada), biar tanggal di prompt selalu fresh
    history = [m for m in history if _get_role(m) != "system"]

    messages = (
        [{"role": "system", "content": build_system_prompt()}]
        + history
        + [{"role": "user", "content": user_text}]
    )

    result = await agent.ainvoke({"messages": messages})
    new_messages = result["messages"]

    set_messages(telegram_user_id, new_messages)

    return new_messages[-1].content