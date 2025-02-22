import asyncio
import wolframalpha
import google.generativeai as genai
from sympy import symbols, simplify, diff, integrate
from telegram import Update
from telegram.ext import CallbackContext
from config import WOLFRAM_API_KEY, GEMINI_API_KEY

# Initialize APIs
wolfram_client = wolframalpha.Client(WOLFRAM_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

async def wolfram_query(query):
    """Fetch structured results from Wolfram Alpha, ensuring full response."""
    try:
        res = await asyncio.to_thread(wolfram_client.query, query)  # Run sync function in async
        if res.success:
            results = [pod.text for pod in res.pods if pod.text]  # Extract non-empty text responses
            return "\n\n".join(results) if results else "No results found."
        else:
            return "No results found."
    except Exception as e:
        return f"Error: {e}"

async def gemini_explain(query):
    """Use Gemini AI to provide detailed explanations."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        return response.text if response else "No response from Gemini."
    except Exception as e:
        return f"Error: {e}"

async def solve_math(update: Update, context: CallbackContext):
    """Solves math problems using Wolfram Alpha."""
    if not context.args:
        await update.message.reply_text("Usage: /solve equation")
        return

    query = " ".join(context.args)
    result = await wolfram_query(query)
    await update.message.reply_text(result, parse_mode="Markdown")

async def explain_math(update: Update, context: CallbackContext):
    """Provides step-by-step explanation using Gemini AI."""
    if not context.args:
        await update.message.reply_text("Usage: /explain math_topic")
        return

    query = " ".join(context.args)
    explanation = await gemini_explain(query)
    await update.message.reply_text(explanation)

async def simplify_expression(update: Update, context: CallbackContext):
    """Simplifies a given expression using SymPy."""
    if not context.args:
        await update.message.reply_text("Usage: /simplify (x^2 - 4)/(x - 2)")
        return
    
    try:
        expression = " ".join(context.args)
        simplified_expr = simplify(expression)
        await update.message.reply_text(f"Simplified: {simplified_expr}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def differentiate(update: Update, context: CallbackContext):
    """Finds the derivative of an expression using SymPy."""
    if not context.args:
        await update.message.reply_text("Usage: /diff x^3 + 3*x^2 + 5")
        return

    try:
        x = symbols('x')
        expression = " ".join(context.args)
        derivative = diff(expression, x)
        await update.message.reply_text(f"Derivative: {derivative}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def integrate_expression(update: Update, context: CallbackContext):
    """Finds the integral of an expression using SymPy."""
    if not context.args:
        await update.message.reply_text("Usage: /integrate x^3 + 3*x^2 + 5")
        return

    try:
        x = symbols('x')
        expression = " ".join(context.args)
        integral = integrate(expression, x)
        await update.message.reply_text(f"Integral: {integral} + C")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
