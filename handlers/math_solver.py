import wolframalpha
import google.generativeai as genai
from config import WOLFRAM_APP_ID, GEMINI_API_KEY
from telegram import Update
from telegram.ext import ContextTypes

# Initialize Wolfram Alpha client
wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

async def solve_with_wolfram(problem: str) -> str:
    response = await wolfram_client.aquery(problem)  # Use await here
    return next(response.results).text
    
async def explain_with_gemini(solution: str) -> str:
    prompt = f"Explain the solution to this math problem step by step: {solution}"
    response = await gemini_model.agenerate_content(prompt)  # Use await here
    return response.text

async def handle_math_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problem = update.message.text
    await update.message.reply_text("Solving your problem... Please wait! ⏳")

    try:
        # Step 1: Get solution from Wolfram Alpha
        wolfram_result = await solve_with_wolfram(problem)  # Use await here

        # Step 2: Get explanation from Gemini AI
        explanation = await explain_with_gemini(wolfram_result)  # Use await here

        # Step 3: Send the results to the user
        await update.message.reply_text(f"**Solution:**\n{wolfram_result}\n\n**Explanation:**\n{explanation}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
