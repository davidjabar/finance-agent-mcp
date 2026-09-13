from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from loguru import logger

from app.core.config import settings
from app.routers.api import router as transactions_router


logger.add("logs/app.log", rotation="10 MB")

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(transactions_router, prefix=settings.API_V1_STR)

mcp = FastApiMCP(
    app,
    name="FinanceTrackerMCP",
    description="A Model Context Protocol (MCP) server integration to track income, expenses, and generate financial reports directly via Telegram.",
)
mcp.mount()
