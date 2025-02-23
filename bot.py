from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.constants import ParseMode
from handlers.math_solver import solve_math, explain_math
from config import TELEGRAM_BOT_TOKEN

async def start(update: Update, context: CallbackContext):
    """Start command with bot info and menu."""
    keyboard = [
        [InlineKeyboardButton("🧮 Solve Math", callback_data="solve")],
        [InlineKeyboardButton("📖 Explain Concept", callback_data="explain")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🔹 *Welcome to Math Solver Bot!* 🔹\n\n"
        "I'm created by *Alok Ojha* to help you solve math problems and explain concepts.\n\n"
        "📌 *What I can do:*\n"
        "✅ Solve mathematical equations.\n"
        "✅ Explain math concepts in simple terms.\n\n"
        "📎 Use the buttons below to get started!"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_callback(update: Update, context: CallbackContext):
    """Handles button clicks from the inline keyboard."""
    query = update.callback_query
    await query.answer()

    if query.data == "solve":
        await query.message.reply_text("🧮 *Send me a math problem to solve!*", parse_mode=ParseMode.MARKDOWN)
    elif query.data == "explain":
        await query.message.reply_text("📖 *Send me a math concept to explain!*", parse_mode=ParseMode.MARKDOWN)

async def formatted_solve_math(update: Update, context: CallbackContext):
    """Handles math solving requests and sends both text and images if available."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math expression!*", parse_mode=ParseMode.MARKDOWN)
        return

    expression = " ".join(context.args)
    result, image_path = await solve_math(expression)  # Get both text and image

    if image_path:
        await update.message.reply_photo(photo=open(image_path, "rb"), caption=result, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

async def formatted_explain_math(update: Update, context: CallbackContext):
    """Handles math explanation requests."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math concept!*", parse_mode=ParseMode.MARKDOWN)
        return

    concept = " ".join(context.args)
    explanation = await explain_math(concept)
    
    await update.message.reply_text(explanation, parse_mode=ParseMode.MARKDOWN)

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
