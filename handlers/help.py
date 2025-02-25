from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **Math Solver Bot Help**\n\n"
        "Send me a math problem, and I'll solve it using Wolfram Alpha and explain it with Gemini AI.\n\n"
        "Examples:\n"
        "- Solve `2 + 2`\n"
        "- Solve `x^2 + 5x + 6 = 0`\n"
        "- Solve `integrate x^2 dx`\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )
