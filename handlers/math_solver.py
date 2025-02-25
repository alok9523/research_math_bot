import requests
from telegram import Update
from telegram.ext import CallbackContext
from config import WOLFRAM_APP_ID, GEMINI_API_KEY
import logging

logger = logging.getLogger(__name__)

async def solve_equation(update: Update, context: CallbackContext) -> None:
    """Solve a math equation using Wolfram Alpha."""
    equation = ' '.join(context.args)
    if not equation:
        await update.message.reply_text("Please provide a math expression to solve.")
        return

    try:
        response = requests.get(f"http://api.wolframalpha.com/v2/query", params={
            'input': equation,
            'format': 'plaintext',
            'output': 'JSON',
            'appid': WOLFRAM_APP_ID
        })
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Process the response and extract the solution
        pods = data.get('queryresult', {}).get('pods', [])
        if not pods:
            await update.message.reply_text("No results found.")
            return

        solution = ""
        for pod in pods:
            title = pod.get('title', '')
            subpods = pod.get('subpods', [])
            if subpods:
                solution += f"{title}: {subpods[0].get('plaintext', 'No solution available')}\n"

        await update.message.reply_text(solution.strip())

    except requests.RequestException as e:
        logger.error(f"Error fetching from Wolfram Alpha: {e}")
        await update.message.reply_text("There was an error processing your request.")

async def explain_concept(update: Update, context: CallbackContext) -> None:
    """Explain a math concept using Gemini AI."""
    concept = ' '.join(context.args)
    if not concept:
        await update.message.reply_text("Please provide a math concept to explain.")
        return

    try:
        response = requests.post("https://api.gemini.ai/ex
