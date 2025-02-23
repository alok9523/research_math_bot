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

        # Extract LaTeX result
        latex_result = None
        for pod in pods:
            if "Mathematical notation" in pod.title or "Result" in pod.title:
                latex_result = pod.text
                break

        if not latex_result:
            return "No LaTeX solution found. Please try another query."

        return latex_result

    except Exception as e:
        return str(e)  # Ensure this is the last statement before function ends

async def explain_math(concept):
    """Explain a math concept using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Explain the concept of {concept} in simple terms with examples.")
        return response.text

    except Exception as e:
        return str(e)  # No extra text after this line

async def explain_math(concept):
    """Explain a math concept using Gemini AI with better formatting."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Explain the concept of {concept} in simple terms with examples.")
        return response.text

    except Exception as e:
        return str(e)
