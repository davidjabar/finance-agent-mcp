from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from loguru import logger
from pydantic import BaseModel

from app.core.config import settings
from app.routers.api import router as transactions_router
from app.services.agent_service import handle_chat

logger.add("logs/app.log", rotation="10 MB")

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(transactions_router, prefix=settings.API_V1_STR)

mcp = FastApiMCP(
    app,
    name="FinanceTrackerMCP",
    description="A Model Context Protocol (MCP) server integration to track income, expenses, and generate financial reports directly via Telegram.",
)
mcp.mount()

class ChatRequest(BaseModel):
    message: str


@app.post("/debug/chat", include_in_schema=True)
async def debug_chat(payload: ChatRequest):
    response = await handle_chat(payload.message)
    return {"response": response}
