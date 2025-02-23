import wolframalpha
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import re
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

# Dictionary to replace math expressions with Unicode symbols
MATH_SYMBOLS = {
    r"(\d+)\^(\d+)": lambda m: f"{m.group(1)}{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(d)] for d in m.group(2))}",  # Exponents
    r"integral": "∫",  # Integral symbol
    r"sin\^(\d+)(.*?)": lambda m: f"sin{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(d)] for d in m.group(1))}({m.group(2)})",  # sin^2(x) -> sin²(x)
    r"cos\^(\d+)(.*?)": lambda m: f"cos{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(d)] for d in m.group(1))}({m.group(2)})",  # cos^2(x) -> cos²(x)
    r"tan\^(\d+)(.*?)": lambda m: f"tan{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(d)] for d in m.group(1))}({m.group(2)})",  # tan^2(x) -> tan²(x)
    r"e\^([+-]?\d*x?)": lambda m: f"e{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(d)] for d in m.group(1))}" if m.group(1) else "e",  # e^x -> eˣ
    r"sqrt(.*?)": r"√(\1)",  # Square root
    r"pi": "π",  # Pi
    r"sum(.*?)": r"∑(\1)",  # Summation
    r"lim(.*?)": r"lim (\1)",  # Limits
    r"log(.*?)": r"log(\1)",  # Logarithm
    r"int(.*?)": r"∫(\1)",  # Integral
    r"O(.*?)": r"O(\1)",  # Big-O notation
}

def format_math(expression):
    """Replace text-based math symbols with proper Unicode representations."""
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
