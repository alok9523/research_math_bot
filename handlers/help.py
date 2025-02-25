async def help(update, context):
    help_text = """
🤖 **Math Solver Bot Help**

🔹 *Commands*:
/solve [problem] - Solve math equations
/explain [concept] - Explain mathematical concepts
/help - Show this help message

🔹 *Examples*:
/solve x^2 + 5x + 6 = 0
/explain Pythagorean theorem

🔹 *Features*:
- Step-by-step solutions
- Visual representations
- Natural language explanations
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
