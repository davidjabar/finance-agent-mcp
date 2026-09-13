from langchain_openai import ChatOpenAI

from app.core.config import settings

llm = ChatOpenAI(
    model=settings.CHAT_MODEL,
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
    temperature=0,
)