import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import settings
from app.core.llm import llm

_agent = None
_lock = asyncio.Lock()


async def get_agent():
    global _agent
    if _agent is not None:
        return _agent

    async with _lock:
        if _agent is not None:
            return _agent

        client = MultiServerMCPClient({
            "finance_tracker": {
                "url": settings.MCP_SERVER_URL,
                "transport": "sse",
            }
        })
        tools = await client.get_tools()
        _agent = create_agent(llm, tools)
        return _agent