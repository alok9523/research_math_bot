import wolframalpha
from config import WOLFRAM_APP_ID
from telegram import Update
from telegram.ext import ContextTypes

client = wolframalpha.Client(WOLFRAM_APP_ID)

async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /math command"""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please enter a math query after /math.")
        return

    try:
        res = client.query(query)
        answer = next(res.results).text
        await update.message.reply_text(f"📌 Answer: {answer}")
    except:
        await update.message.reply_text("❌ Could not solve the math problem.")