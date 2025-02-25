import wolframalpha
import google.generativeai as genai
from config import WOLFRAM_APP_ID, GEMINI_API_KEY

# Initialize Wolfram Alpha client
wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

def solve_with_wolfram(problem: str) -> str:
    response = wolfram_client.query(problem)
    return next(response.results).text

def explain_with_gemini(solution: str) -> str:
    prompt = f"Explain the solution to this math problem step by step: {solution}"
    response = gemini_model.generate_content(prompt)
    return response.text

async def handle_math_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problem = update.message.text
    await update.message.reply_text("Solving your problem... Please wait! ⏳")

    try:
        # Step 1: Get solution from Wolfram Alpha
        wolfram_result = solve_with_wolfram(problem)

        # Step 2: Get explanation from Gemini AI
        explanation = explain_with_gemini(wolfram_result)

        # Step 3: Send the results to the user
        await update.message.reply_text(f"**Solution:**\n{wolfram_result}\n\n**Explanation:**\n{explanation}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
