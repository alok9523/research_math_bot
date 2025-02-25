from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from config import config
import handlers.help as help_handler
import handlers.math_solver as math_solver
import handlers.formatter as formatter

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Solve Equation", callback_data='solve')],
        [InlineKeyboardButton("Explain Concept", callback_data='explain')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Math Solver Bot! 🧮\n\n"
        "Choose an option or use commands:\n"
        "/solve - Solve math problems\n"
        "/explain - Explain mathematical concepts",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'solve':
        await query.message.reply_text("Please send your math problem to solve")
    elif query.data == 'explain':
        await query.message.reply_text("What mathematical concept would you like explained?")

def main():
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_handler.help))
    application.add_handler(CommandHandler("solve", math_solver.solve_command))
    application.add_handler(CommandHandler("explain", math_solver.explain_command))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, math_solver.handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
