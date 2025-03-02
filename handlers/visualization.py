import matplotlib.pyplot as plt
import numpy as np
from telegram import Update
from telegram.ext import ContextTypes

async def plot_graph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /graph command"""
    try:
        expr = " ".join(context.args)
        if not expr:
            await update.message.reply_text("Please enter a function (e.g., /graph x**2).")
            return

        x = np.linspace(-10, 10, 400)
        y = eval(expr, {"x": x, "np": np})

        plt.plot(x, y)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title(f"Graph of {expr}")
        plt.grid(True)
        
        plt.savefig("graph.png")
        plt.close()

        await update.message.reply_photo(photo=open("graph.png", "rb"))
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")