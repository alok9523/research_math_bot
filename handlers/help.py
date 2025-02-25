# handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "*Available commands:*\n"
        "/solve <expression> - Solve a math expression.\n"
        "/explain <topic> - Explain a math concept.\n"
        "/help - Show this help message."
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
