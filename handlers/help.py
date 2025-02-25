from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "I can help you with the following commands:\n"
        "/solve <expression> - Solve a math expression.\n"
        "/explain <concept> - Explain a math concept.\n"
        "Just send me a message with a math expression, and I'll do my best to help!"
    )
    await update.message.reply_text(help_text)
