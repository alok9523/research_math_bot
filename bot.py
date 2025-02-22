from telegram.ext import Application, CommandHandler
from handlers.math_solver import solve_math, explain_math, simplify_expression, differentiate, integrate_expression
from config import TELEGRAM_BOT_TOKEN

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register Commands
    app.add_handler(CommandHandler("solve", solve_math))
    app.add_handler(CommandHandler("explain", explain_math))
    app.add_handler(CommandHandler("simplify", simplify_expression))
    app.add_handler(CommandHandler("diff", differentiate))
    app.add_handler(CommandHandler("integrate", integrate_expression))

    app.run_polling()

if __name__ == "__main__":
    main()
