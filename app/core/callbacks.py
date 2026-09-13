from typing import Any, Dict

from langchain_core.callbacks import AsyncCallbackHandler
from loguru import logger


class LoguruCallbackHandler(AsyncCallbackHandler):
    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        tool_name = serialized.get("name", "unknown_tool")
        logger.info(f"[TOOL CALL] {tool_name} input={input_str}")

    async def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        logger.info(f"[TOOL RESULT] {output}")

    async def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        logger.error(f"[TOOL ERROR] {error}")