from telegram.ext import Updater, CommandHandler
from handlers.math_solver import solve_math, explain_math, simplify_expression, differentiate, integrate_expression
from config import TELEGRAM_BOT_TOKEN

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register Commands
    dp.add_handler(CommandHandler("solve", solve_math))
    dp.add_handler(CommandHandler("explain", explain_math))
    dp.add_handler(CommandHandler("simplify", simplify_expression))
    dp.add_handler(CommandHandler("diff", differentiate))
    dp.add_handler(CommandHandler("integrate", integrate_expression))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
