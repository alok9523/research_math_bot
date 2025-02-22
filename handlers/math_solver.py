import wolframalpha
import google.generativeai as genai
from sympy import symbols, Eq, solve, simplify, diff, integrate
from telegram import Update
from telegram.ext import CallbackContext
from config import WOLFRAM_API_KEY, GEMINI_API_KEY

# Initialize APIs
wolfram_client = wolframalpha.Client(WOLFRAM_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

def wolfram_query(query):
    """Fetch structured results from Wolfram Alpha."""
    try:
        res = wolfram_client.query(query)
        if res["@success"] == "false":
            return "Wolfram Alpha couldn't solve this."

        output = []
        for pod in res["pod"]:
            title = pod["@title"]
            content = "\n".join(sub["@plaintext"] for sub in pod["subpod"] if "@plaintext" in sub)
            output.append(f"*{title}:*\n{content}")

        return "\n\n".join(output)
    except Exception as e:
        return f"Error: {e}"

def gemini_explain(query):
    """Use Gemini AI to provide detailed explanations."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def solve_math(update: Update, context: CallbackContext) -> None:
    """Solves math problems using Wolfram Alpha."""
    if not context.args:
        update.message.reply_text("Usage: /solve equation")
        return

    query = " ".join(context.args)
    result = wolfram_query(query)
    update.message.reply_text(result, parse_mode="Markdown")

def explain_math(update: Update, context: CallbackContext) -> None:
    """Provides step-by-step explanation using Gemini AI."""
    if not context.args:
        update.message.reply_text("Usage: /explain math_topic")
        return

    query = " ".join(context.args)
    explanation = gemini_explain(query)
    update.message.reply_text(explanation)

def simplify_expression(update: Update, context: CallbackContext) -> None:
    """Simplifies a given expression using SymPy."""
    if not context.args:
        update.message.reply_text("Usage: /simplify (x^2 - 4)/(x - 2)")
        return
    
    try:
        expression = " ".join(context.args)
        simplified_expr = simplify(expression)
        update.message.reply_text(f"Simplified: {simplified_expr}")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def differentiate(update: Update, context: CallbackContext) -> None:
    """Finds the derivative of an expression using SymPy."""
    if not context.args:
        update.message.reply_text("Usage: /diff x^3 + 3*x^2 + 5")
        return

    try:
        x = symbols('x')
        expression = " ".join(context.args)
        derivative = diff(expression, x)
        update.message.reply_text(f"Derivative: {derivative}")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def integrate_expression(update: Update, context: CallbackContext) -> None:
    """Finds the integral of an expression using SymPy."""
    if not context.args:
        update.message.reply_text("Usage: /integrate x^3 + 3*x^2 + 5")
        return

    try:
        x = symbols('x')
        expression = " ".join(context.args)
        integral = integrate(expression, x)
        update.message.reply_text(f"Integral: {integral} + C")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")
