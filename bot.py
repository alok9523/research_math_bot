import logging
from telegram import Update, ForceReply, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, InlineQueryHandler
from config import TOKEN
from handlers.math_solver import solve_equation, explain_concept
from handlers.help import help_command

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm your Math Solver Bot. Use /help to see what I can do.",
        reply_markup=ForceReply(selective=True),
    )

async def inline_query_handler(update: Update, context: CallbackContext) -> None:
    """Handle inline queries."""
    query = update.inline_query.query
    if query:
        results = [
            InlineQueryResultArticle(
                id=1,
                title="Solve Equation",
                input_message_content=InputTextMessageContent(f"/solve {query}"),
            ),
            InlineQueryResultArticle(
                id=2,
                title="Explain Concept",
                input_message_content=InputTextMessageContent(f"/explain {query}"),
            ),
        ]
        await update.inline_query.answer(results)

async def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("solve", solve_equation))
    application.add_handler(CommandHandler("explain", explain_concept))

    # Handle text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_equation))

    # Inline query handler
    application.add_handler(InlineQueryHandler(inline_query_handler))

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
