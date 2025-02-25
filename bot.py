# bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers.math_solver import solve_equation, explain_concept
from handlers.help import help_command
import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Math Solver Bot! Use /help to see available commands.",
        parse_mode='Markdown'  # Using string for simplicity
    )

def main():
    app = ApplicationBuilder().token(config.API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("solve", solve_equation))
    app.add_handler(CommandHandler("explain", explain_concept))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()

if __name__ == "__main__":
    main()
