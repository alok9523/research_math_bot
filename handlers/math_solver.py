import wolframalpha
import google.generativeai as genai
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

async def solve_math(expression):
    """Solve math problems using Wolfram Alpha with detailed results."""
    try:
        res = client.query(expression)
        pods = list(res.pods)

        if not pods:
            return "⚠️ *No solution found. Please check your input.*"

        # Extract primary and additional results
        main_result = next(res.results).text  # First direct result
        sub_results = []
        for pod in pods[1:]:  # Skip primary pod
            if pod.title and pod.text:
                sub_results.append(f"🔹 *{pod.title}:* `{pod.text}`")

        # Format the response
        formatted_response = (
            f"📌 **Solution for:** `{expression}`\n\n"
            f"✅ **Primary Result:** `{main_result}`\n\n"
        )

        if sub_results:
            formatted_response += "\n".join(sub_results)

        return formatted_response

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`"

async def explain_math(concept):
    """Explain a math concept using Gemini AI with better formatting."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Explain the concept of {concept} in simple terms with examples.")

        # Format explanation properly
        explanation = response.text
        formatted_response = (
            f"📖 **Explanation of {concept}:**\n\n"
            f"{explanation}\n\n"
            f"📝 *If you need more details, try specifying your request!*"
        )

        return formatted_response

    except Exception as e:
        return f"⚠️ *Error:* `{str(e)}`"
