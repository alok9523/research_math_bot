import wolframalpha
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import re
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

# Readable math symbols
READABLE_SYMBOLS = {
    r"(\d+)\^(\d+)": r"\1^\2",  # Exponents
    r"integral": "∫",  
    r"sin\^(\d+)(.*?)": r"sin^\1(\2)",  
    r"cos\^(\d+)(.*?)": r"cos^\1(\2)",  
    r"tan\^(\d+)(.*?)": r"tan^\1(\2)",  
    r"e\^([+-]?\d*x?)": r"e^\1",  
    r"sqrt(.*?)": r"√(\1)",  
    r"pi": "π",  
    r"sum(.*?)": r"∑(\1)",  
    r"lim(.*?)": r"lim(\1)",  
    r"log(.*?)": r"log(\1)",  
    r"O(.*?)": r"O(\1)",  
}

# LaTeX math symbols
LATEX_SYMBOLS = {
    r"(\d+)\^(\d+)": r"{\1}^{\2}",  
    r"integral": r"\int",  
    r"sin\^(\d+)(.*?)": r"\sin^{\1}(\2)",  
    r"cos\^(\d+)(.*?)": r"\cos^{\1}(\2)",  
    r"tan\^(\d+)(.*?)": r"\tan^{\1}(\2)",  
    r"e\^([+-]?\d*x?)": r"e^{\1}",  
    r"sqrt(.*?)": r"\sqrt{\1}",  
    r"pi": r"\pi",  
    r"sum(.*?)": r"\sum{\1}",  
    r"lim(.*?)": r"\lim{\1}",  
    r"log(.*?)": r"\log{\1}",  
    r"O(.*?)": r"O({\1})",  
}

def format_expression(expression, symbol_dict):
    """Replaces math symbols based on the provided dictionary."""
    for pattern, replacement in symbol_dict.items():
        expression = re.sub(pattern, replacement, expression)
    return expression

async def solve_math(expression):
    """Solve any math-related query using Wolfram Alpha."""
    try:
        res = await client.aquery(expression)  # Async query
        pods = list(res.pods)

        if not pods:
            return "⚠️ *No solution found. Please check your input.*", None

        # Extract results
        results = []
        latex_results = []
        for pod in pods:
            if pod.title and pod.text:
                readable_title = format_expression(pod.title, READABLE_SYMBOLS)
                readable_text = format_expression(pod.text, READABLE_SYMBOLS)

                latex_title = format_expression(pod.title, LATEX_SYMBOLS)
                latex_text = format_expression(pod.text, LATEX_SYMBOLS)

                results.append(f"🔹 *{readable_title}:*\n{readable_text}\n")
                latex_results.append(f"\\textbf{{{latex_title}}} \\\\ {latex_text}")  # LaTeX output

        formatted_text = f"📌 Solution for: {format_expression(expression, READABLE_SYMBOLS)}\n\n" + "\n".join(results)

        # Generate LaTeX image
        image_bytes = generate_latex_image(latex_results)
        return formatted_text, image_bytes

    except Exception as e:
        return f"⚠️ *Error:* {str(e)}", None

async def formatted_solve_math(update: Update, context: CallbackContext):
    """Handles math-solving requests and sends both text and images separately."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math expression!*", parse_mode=ParseMode.MARKDOWN)
        return

    expression = " ".join(context.args)
    result, image_bytes = await solve_math(expression)

    # Send formatted text
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN_V2)

    # Send generated image
    if image_bytes:
        image_bytes.seek(0)
        await update.message.reply_photo(photo=image_bytes)

async def formatted_explain_math(update: Update, context: CallbackContext):
    """Explains mathematical concepts using Gemini AI."""
    if not context.args:
        await update.message.reply_text("⚠️ *Please provide a math concept!*", parse_mode=ParseMode.MARKDOWN)
        return

    concept = " ".join(context.args)
    explanation = await explain_math(concept)

    await update.message.reply_text(explanation, parse_mode=ParseMode.MARKDOWN_V2)

def generate_latex_image(latex_results):
    """Generate a LaTeX-rendered image for better math visualization."""
    fig, ax = plt.subplots(figsize=(6, len(latex_results) * 0.8))
    ax.axis("off")
latex_code = "$$" + "\n".join(latex_results) + "$$"
    ax.text(0.05, 0.95, latex_code, verticalalignment='top', fontsize=14, family="serif")

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    img_bytes.seek(0)

    return img_bytes

async def explain_math(concept):
    """Explain math concepts with LaTeX formatting using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Explain the concept of {concept} in simple terms with examples.")

        explanation = response.text
        formatted_response = f"📖 Explanation of {format_expression(concept, READABLE_SYMBOLS)}:\n\n{explanation}\n\n📝 *If you need more details, try specifying your request!*"

        return formatted_response

    except Exception as e:
        return f"⚠️ *Error:* {str(e)}"
