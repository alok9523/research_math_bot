import requests
from config import DEEPSEEK_API_KEY
from telegram import Update
from telegram.ext import ContextTypes

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /ai command"""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please ask a question after /ai.")
        return

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={"model": "deepseek", "messages": [{"role": "user", "content": query}]}
    )

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    await update.message.reply_text(f"🤖 AI: {answer}")