import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers import start, wolfram, gpt, math_solver, visualization, chat

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def unknown(update: Update, context):
    """Handles unknown commands"""
    await update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    """Main function to run the bot"""
    app = Application.builder().token(TOKEN).build()

    # Register Handlers
    app.add_handler(CommandHandler("start", start.handle_start))
    app.add_handler(CommandHandler("math", wolfram.solve_math))
    app.add_handler(CommandHandler("ai", gpt.ask_ai))
    app.add_handler(CommandHandler("graph", visualization.plot_graph))
    app.add_handler(CommandHandler("chat", chat.chat_ai))

    # Handle unknown messages
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()