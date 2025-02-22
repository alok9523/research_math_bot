from telegram.ext import Application, CommandHandler
from telegram import Update
from handlers.math_solver import solve_math, explain_math, simplify_expression, differentiate, integrate_expression
from config import TELEGRAM_BOT_TOKEN

def escape_markdown(text):
    """Escapes special characters for MarkdownV2 formatting."""
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register async handlers with Markdown formatting
    async def formatted_solve_math(update: Update, context):
        result = await solve_math(update, context)
        await update.message.reply_text(f"**Solution:**\n```{escape_markdown(result)}```", parse_mode="MarkdownV2")

    async def formatted_explain_math(update: Update, context):
        explanation = await explain_math(update, context)
        await update.message.reply_text(f"**Explanation:**\n{escape_markdown(explanation)}", parse_mode="MarkdownV2")

    async def formatted_integrate_expression(update: Update, context):
        result = await integrate_expression(update, context)
        await update.message.reply_text(f"**Integral:**\n```{escape_markdown(result)}```", parse_mode="MarkdownV2")

    # Register handlers
    app.add_handler(CommandHandler("solve", formatted_solve_math))
    app.add_handler(CommandHandler("explain", formatted_explain_math))
    app.add_handler(CommandHandler("simplify", simplify_expression))
    app.add_handler(CommandHandler("diff", differentiate))
    app.add_handler(CommandHandler("integrate", formatted_integrate_expression))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
