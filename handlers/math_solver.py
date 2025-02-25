# handlers/math_solver.py

import requests
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import config

async def solve_equation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expression = ' '.join(context.args)
    if not expression:
        await update.message.reply_text("Please provide a math expression to solve.")
        return

    # Call Wolfram Alpha API
    try:
        response = requests.get(f"http://api.wolframalpha.com/v2/query?input={expression}&format=plaintext&output=JSON&appid={config.WOLFRAM_APP_ID}")
        data = response.json()

        if data['queryresult']['success']:
            pods = data['queryresult']['pods']
            solution = pods[1]['subpods'][0]['plaintext']
            await update.message.reply_text(
                f"*Solution:* {solution}",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text("Sorry, I couldn't solve that expression. Please try another one.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

async def explain_concept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = ' '.join(context.args)
    if not topic:
        await update.message.reply_text("Please provide a math topic to explain.")
        return

    # Call Gemini API (or any other API for explanations)
    try:
        # Example: response = requests.get(f"https://api.gemini.com/explain?topic={topic}&key={config.GEMINI_API_KEY}")
        # For now, let's just send a placeholder response
        explanation = f"Explanation for *{topic}*: [This is a placeholder response.]"
        await update.message.reply_text(explanation, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
