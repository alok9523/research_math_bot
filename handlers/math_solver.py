import wolframalpha
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import re
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

# Dictionary for replacing mathematical symbols with proper Unicode equivalents
MATH_SYMBOLS = {
    r"(\d+)\^(\d+)": r"\1⁰¹²³⁴⁵⁶⁷⁸⁹",  # Exponents like x^2 -> x²
    r"sqrt(.*?)": r"√(\1)",  # Square root
    r"pi": "π",  # Pi
    r"e\^": "e",  # Euler’s number
    r"sum(.*?)": r"∑(\1)",  # Summation
    r"lim(.*?)": r"lim (\1)",  # Limits
    r"log(.*?)": r"log(\1)",  # Logarithm
    r"sin(.*?)": r"sin(\1)",  # Sine
    r"cos(.*?)": r"cos(\1)",  # Cosine
    r"tan(.*?)": r"tan(\1)",  # Tangent
    r"int(.*?)": r"∫(\1)",  # Integral
}

def format_math(expression):
    """Replace text-based math symbols with Unicode representations."""
    for pattern, replacement in MATH_SYMBOLS.items():
        expression = re.sub(pattern, replacement, expression)
    return expression

async def solve_math(expression):
    """Solve math problems using Wolfram Alpha and return formatted results with an image."""
    try:
        res = await client.aquery(expression)  # Async query
        pods = list(res.pods)

        if not pods:
            return "⚠️ *No solution found. Please check your input.*", None

        # Extract all results and format them
        results = []
        for pod in pods:
            if pod.title and pod.text:
                formatted_title = format_math(pod.title)
                formatted_text = format_math(pod.text)
                results.append(f"🔹 *{formatted_title}:*\n{formatted_text}\n")

        formatted_text = f"📌 **Solution for:** `{format_math(expression)}`\n\n" + "\n".join(results)

        # Generate an image and return as BytesIO
        image_bytes = generate_math_image(results)
        return formatted_text, image_bytes

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`", None

def generate_math_image(math_results):
    """Generate an image with properly formatted math output using LaTeX-like rendering."""
    fig, ax = plt.subplots(figsize=(6, len(math_results) * 0.8))
    ax.axis("off")  # Hide axes

    # Convert results to LaTeX-style formatting
    formatted_text = "\n".join([f"${format_math(line)}$" for line in math_results])  

    # Display formatted text
    ax.text(0.05, 0.95, formatted_text, verticalalignment='top', fontsize=14, family="monospace")

    # Save image to BytesIO
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    img_bytes.seek(0)

    return img_bytes

async def explain_math(concept):
    """Explain a math concept using Gemini AI with proper formatting."""
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
