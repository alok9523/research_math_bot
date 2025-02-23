import wolframalpha
import google.generativeai as genai
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize APIs
client = wolframalpha.Client(WOLFRAM_APP_ID)
genai.configure(api_key=GEMINI_API_KEY)

async def solve_math(expression):
    """Solve math problems using Wolfram Alpha and return the result in raw LaTeX format."""
    try:
        res = await client.aquery(expression)  # Async query
        pods = list(res.pods)

        if not pods:
            return "No solution found. Please check your input."

        # Try to extract LaTeX result
        latex_result = None
        for pod in pods:
            if "Mathematical notation" in pod.title or "Result" in pod.title:
                latex_result = pod.text
                break  # Stop at first valid LaTeX response

        if not latex_result:
            return "No LaTeX solution found. Please try another query."

        return latex_result  # Returning raw LaTeX output

    except Exception as e:
        return str(e)  # Return error as raw text
