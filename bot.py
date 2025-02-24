from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, CallbackContext
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from handlers.math_solver import solve_math, explain_math
from config import TELEGRAM_BOT_TOKEN
import re
import io


def escape_markdown_v2(text):
    """Escape MarkdownV2 special characters to prevent Telegram parsing errors."""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(special_chars), r'\\\1', text)


async def start(update: Update, context: CallbackContext):
    """Start command with bot info and menu."""
    keyboard = [
        [InlineKeyboardButton("🧮 Solve Math", callback_data="solve")],
        [InlineKeyboardButton("📖 Explain Concept", callback_data="explain")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🔹 *Welcome to Math Solver Bot!* 🔹\n\n"
        "I'm created to help you solve math problems and explain concepts.\n\n"
        "📌 *What I can do:*\n"
        "✅ Solve mathematical equations.\n"
        "✅ Explain math concepts in simple terms.\n\n"
        "📎 Use the buttons below to get started!"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)


async def handle_callback(update: Update, context: CallbackContext):
    """Handles button clicks from the inline keyboard."""
    query = update.callback_query
    await query.answer()

    if query.data == "solve":
        await query.message.reply_text("🧮 *Send me a math problem to solve!*", parse_mode=ParseMode.MARKDOWN_V2)
    elif query.data == "explain":
        await query.message.reply_text("📖 *Send me a math concept to explain!*", parse_mode=ParseMode.MARKDOWN_V2)


async def formatted_solve_math(update: Update, context: CallbackContext):
    """Handles math solving requests and sends both text and images separately."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math expression!*", parse_mode=ParseMode.MARKDOWN_V2)
        return

    expression = " ".join(context.args)
    result, image_bytes = await solve_math(expression)  # Get text + image

    # Escape Markdown special characters
    safe_result = escape_markdown_v2(result)

    # Send text result with proper Markdown formatting
    if len(safe_result) > 4096:  # Telegram text limit
        for i in range(0, len(safe_result), 4096):
            await update.message.reply_text(safe_result[i:i + 4096], parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await update.message.reply_text(safe_result, parse_mode=ParseMode.MARKDOWN_V2)

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

    # Escape Markdown characters
    safe_explanation = escape_markdown_v2(explanation)

    await update.message.reply_text(safe_explanation, parse_mode=ParseMode.MARKDOWN_V2)


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("solve", formatted_solve_math))
    app.add_handler(CommandHandler("explain", formatted_explain_math))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🤖 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
