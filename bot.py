import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TOKEN
from handlers.math_solver import solve_equation, explain_concept
from handlers.help import help_command

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm your Math Solver Bot. Use /help to see what I can do.",
        reply_markup=ForceReply(selective=True),
    )

def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("solve", solve_equation))
    dispatcher.add_handler(CommandHandler("explain", explain_concept))

    # Handle text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, solve_equation))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
