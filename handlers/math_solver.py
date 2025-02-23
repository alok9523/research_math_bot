import wolframalpha
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import re
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

# Dictionary to replace math expressions with Unicode and LaTeX representations
MATH_SYMBOLS = {
    r"(\d+)\^(\d+)": lambda m: f"{m.group(1)}^{''.join(m.group(2))}",  # Exponents (LaTeX format)
    r"integral": r"\\int",  # Integral symbol in LaTeX
    r"sin\^(\d+)(.*?)": lambda m: f"\\sin^{m.group(1)}({m.group(2)})",  # sin^2(x) -> sin²(x)
    r"cos\^(\d+)(.*?)": lambda m: f"\\cos^{m.group(1)}({m.group(2)})",  # cos^2(x) -> cos²(x)
    r"tan\^(\d+)(.*?)": lambda m: f"\\tan^{m.group(1)}({m.group(2)})",  # tan^2(x) -> tan²(x)
    r"e\^([+-]?\d*x?)": lambda m: f"e^{m.group(1)}",  # e^x -> eˣ in LaTeX
    r"sqrt(.*?)": r"\\sqrt{\1}",  # Square root in LaTeX
    r"pi": r"\\pi",  # Pi symbol in LaTeX
    r"sum(.*?)": r"\\sum{\1}",  # Summation in LaTeX
    r"lim(.*?)": r"\\lim{\1}",  # Limits in LaTeX
    r"log(.*?)": r"\\log{\1}",  # Logarithm
    r"int(.*?)": r"\\int{\1}",  # Integral
    r"O(.*?)": r"O({\1})",  # Big-O notation
}

def format_math(expression):
    """Replace text-based math symbols with LaTeX representations."""
    for pattern, replacement in MATH_SYMBOLS.items():
        expression = re.sub(pattern, replacement, expression)
    return expression

async def solve_math(expression):
    """Solve math problems using Wolfram Alpha and return formatted results with LaTeX support."""
    try:
        res = await client.aquery(expression)  # Async query
        pods = list(res.pods)

        if not pods:
            return "⚠️ *No solution found. Please check your input.*", None

        # Extract all results and format them
        results = []
        latex_results = []
        for pod in pods:
            if pod.title and pod.text:
                formatted_title = format_math(pod.title)
                formatted_text = format_math(pod.text)
                results.append(f"🔹 *{formatted_title}:*\n{formatted_text}\n")
                latex_results.append(f"\\textbf{{{formatted_title}}} \\\\ {formatted_text}")  # LaTeX output

        formatted_text = f"📌 **Solution for:** `{format_math(expression)}`\n\n" + "\n".join(results)

        # Generate an image with LaTeX rendering
        image_bytes = generate_latex_image(latex_results)
        return formatted_text, image_bytes

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`", None

def generate_latex_image(latex_results):
    """Generate an image using LaTeX rendering for clean math formatting."""
    fig, ax = plt.subplots(figsize=(6, len(latex_results) * 0.8))
    ax.axis("off")  # Hide axes

    # Convert results into proper LaTeX block
    latex_text = "\n".join(latex_results)
    latex_code = f"$${latex_text}$$"

    # Display LaTeX-rendered math
    ax.text(0.05, 0.95, latex_code, verticalalignment='top', fontsize=14, family="serif")

    # Save image to BytesIO
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    img_bytes.seek(0)

    return img_bytes

async def explain_math(concept):
    """Explain a math concept using Gemini AI with LaTeX formatting."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Explain the concept of {concept} in simple terms with examples.")

        explanation = response.text
        formatted_response = (
            f"📖 **Explanation of {format_math(concept)}:**\n\n"
            f"{explanation}\n\n"
            f"📝 *If you need more details, try specifying your request!*"
        )

        return formatted_response

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`"
