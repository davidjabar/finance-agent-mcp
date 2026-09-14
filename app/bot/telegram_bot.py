from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from loguru import logger

from app.core.config import settings
from app.services.agent_service import handle_chat


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sender_id = update.effective_user.id

    if sender_id != settings.OWNER_TELEGRAM_ID:
        logger.warning(f"Unauthorized access attempt from telegram_user_id={sender_id}")
        await update.message.reply_text("Maaf, kamu tidak punya akses ke bot ini.")
        return

    user_text = update.message.text
    if not user_text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response_text = await handle_chat(user_text)
    except Exception as e:
        logger.exception(f"Error handling chat: {e}")
        response_text = "Maaf, terjadi kesalahan saat memproses pesanmu. Coba lagi ya."

    await update.message.reply_text(response_text)


def build_bot_app() -> Application:
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    return app


def run_bot() -> None:
    logger.info("Starting Telegram bot (polling mode)...")
    app = build_bot_app()
    app.run_polling()