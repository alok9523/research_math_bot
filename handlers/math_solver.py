import wolframalpha
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import tempfile
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
            return "⚠️ *No solution found. Please check your input.*"

        # Extract all results and format for display
        results = []
        for pod in pods:
            if pod.title and pod.text:
                results.append(f"🔹 *{pod.title}:*\n\n${pod.text}$\n")

        formatted_text = f"📌 **Solution for:** `{expression}`\n\n" + "\n".join(results)

        # Generate an image with the formatted text
        image_path = generate_math_image(results)
        return formatted_text, image_path

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`", None

def generate_math_image(math_results):
    """Generate an image with LaTeX-rendered math output."""
    fig, ax = plt.subplots(figsize=(6, len(math_results) * 0.8))
    ax.axis("off")

    # Display formatted LaTeX text
    text = "\n".join(math_results)
    ax.text(0.05, 0.95, text, verticalalignment='top', fontsize=14, family="monospace")

    # Save image
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name, bbox_inches="tight", dpi=300)
    plt.close(fig)

    return temp_file.name

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
