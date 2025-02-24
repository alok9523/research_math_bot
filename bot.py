from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, CallbackContext
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from handlers.math_solver import solve_math, explain_math
from config import TELEGRAM_BOT_TOKEN

import re

def escape_markdown(text):
    """Escapes special characters for Telegram Markdown v2 formatting."""
    special_chars = r"[*_()~`>#+\-=|{}.!]"
    return re.sub(f"([{special_chars}])", r"\\\1", text)

async def formatted_solve_math(update: Update, context: CallbackContext):
    """Handles math solving requests and sends both text and images separately."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math expression!*", parse_mode=ParseMode.MARKDOWN_V2)
        return

    expression = " ".join(context.args)
    result, image_bytes = await solve_math(expression)  # Get text + image

    # Escape special characters before sending
    formatted_result = escape_markdown(result)

    # Send text result in chunks (if needed)
    if len(formatted_result) > 4096:
        for i in range(0, len(formatted_result), 4096):
            await update.message.reply_text(formatted_result[i:i + 4096], parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await update.message.reply_text(formatted_result, parse_mode=ParseMode.MARKDOWN_V2)

    # Send the image separately if available
    if image_bytes:
        image_bytes.seek(0)  # Reset BytesIO pointer
        await update.message.reply_photo(photo=image_bytes)

async def formatted_explain_math(update: Update, context: CallbackContext):
    """Handles math explanation requests."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math concept!*", parse_mode=ParseMode.MARKDOWN_V2)
        return

    concept = " ".join(context.args)
    explanation = await explain_math(concept)

    # Escape special characters before sending
    formatted_explanation = escape_markdown(explanation)

    await update.message.reply_text(formatted_explanation, parse_mode=ParseMode.MARKDOWN_V2)
