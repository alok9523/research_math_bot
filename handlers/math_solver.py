import wolframalpha
import google.generativeai as genai
from config import Config
from telegram import InputMediaPhoto
import requests
import io
from PIL import Image
from .formatter import format_wolfram_response, format_concept_explanation

# Initialize APIs
wolfram_client = wolframalpha.Client(Config.WOLFRAM_APP_ID)
genai.configure(api_key=Config.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

async def solve_command(update, context):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Please provide a math problem after /solve")
        return
    await process_math_query(update, query)

async def explain_command(update, context):
    concept = ' '.join(context.args)
    if not concept:
        await update.message.reply_text("Please provide a concept to explain after /explain")
        return
    await process_concept_explanation(update, concept)

async def handle_message(update, context):
    text = update.message.text
    if text.startswith('/'):
        return
    await process_math_query(update, text)

async def process_math_query(update, query):
    try:
        # Try Wolfram Alpha first
        res = wolfram_client.query(query)
        formatted_text, images = format_wolfram_response(res)
        
        # Send images if available
        media_group = []
        for img_url in images[:4]:  # Telegram allows max 4 images per group
            media_group.append(InputMediaPhoto(media=img_url))
        
        if media_group:
            await update.message.reply_media_group(media=media_group)
        
        # Send formatted text
        await update.message.reply_text(formatted_text, parse_mode='Markdown')
        
    except Exception as e:
        # Fallback to Gemini
        print(f"Wolfram error: {e}")
        response = gemini_model.generate_content(f"Solve this math problem: {query} with detailed explanations")
        await update.message.reply_text(format_concept_explanation(response.text))

async def process_concept_explanation(update, concept):
    try:
        response = gemini_model.generate_content(f"Explain {concept} in simple terms with examples")
        formatted_text = format_concept_explanation(response.text)
        await update.message.reply_text(formatted_text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Sorry, I couldn't process that request. Error: {e}")

def get_wolfram_image(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image
