from telegram.ext import Application, CommandHandler
from handlers.math_solver import solve_math, explain_math, integrate_expression
from config import TELEGRAM_BOT_TOKEN

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register async handlers
    app.add_handler(CommandHandler("solve", solve_math))
    app.add_handler(CommandHandler("explain", explain_math))
    app.add_handler(CommandHandler("integrate", integrate_expression))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
