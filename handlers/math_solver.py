import wolframalpha
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import tempfile
import matplotlib.font_manager as fm
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

async def solve_math(expression):
    """Solve math problems using Wolfram Alpha and return all extracted results in a formatted image."""
    try:
        res = await client.aquery(expression)  # Async query
        pods = list(res.pods)

        if not pods:
            return "⚠️ *No solution found. Please check your input.*", None

        # Extract all results and format them
        results = []
        for pod in pods:
            if pod.title and pod.text:
                results.append(f"🔹 *{pod.title}:*\n{pod.text}\n")

        formatted_text = f"📌 **Solution for:** `{expression}`\n\n" + "\n".join(results)

        # Generate an image and return as BytesIO
        image_bytes = generate_math_image(results)
        return formatted_text, image_bytes

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`", None

def generate_math_image(math_results):
    """Generate an image with formatted math output and return it as BytesIO."""
    fig, ax = plt.subplots(figsize=(6, len(math_results) * 0.8))
    ax.axis("off")

    # Use a font that supports Unicode
    plt.rcParams["font.family"] = "Arial"  # Use "Noto Sans" if Arial fails

    # Display formatted text
    text = "\n".join(math_results)
    ax.text(0.05, 0.95, text, verticalalignment='top', fontsize=14, family="monospace")

    # Save image to BytesIO instead of a temp file
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    img_bytes.seek(0)

    return img_bytes

async def explain_math(concept):
    """Explain a math concept using Gemini AI with better formatting."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Explain the concept of {concept} in simple terms with examples.")

        explanation = response.text
        formatted_response = (
            f"📖 **Explanation of {concept}:**\n\n"
            f"{explanation}\n\n"
            f"📝 *If you need more details, try specifying your request!*"
        )

        return formatted_response

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`"
