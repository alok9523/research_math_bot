from telegram import Update
from telegram.ext import ContextTypes

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command"""
    await update.message.reply_text(
        "Welcome to the Math & AI Bot! 🧠\n"
        "Use the following commands:\n"
        "/math - Solve a math problem\n"
        "/ai - Ask AI a question\n"
        "/graph - Generate a graph\n"
        "/chat - Chat with AI"
    )