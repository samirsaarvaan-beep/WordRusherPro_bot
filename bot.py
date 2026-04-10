from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN = "8709888043:AAF-qZKL4pu1LgpwtY8n-fU6XWXL2vQqjC8"

words = ["game", "lion", "code", "tree", "rock", "star", "moon"]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to WordRush 🎮\nType /play to start")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = random.choice(words)
    user_data[update.effective_user.id] = {
        "word": word,
        "chances": 20
    }
    hidden = "_" * len(word)
    await update.message.reply_text(f"Guess the word: {hidden}\nChances: 20")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    
    if user not in user_data:
        await update.message.reply_text("Type /play first")
        return
    
    guess_word = update.message.text.lower()
    data = user_data[user]

    if guess_word == data["word"]:
        await update.message.reply_text("🎉 Correct! You win!")
        del user_data[user]
    else:
        data["chances"] -= 1
        if data["chances"] == 0:
            await update.message.reply_text(f"❌ Game Over! Word was: {data['word']}")
            del user_data[user]
        else:
            await update.message.reply_text(f"Wrong ❌\nChances left: {data['chances']}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

app.run_polling(poll_interval=0.5, timeout=10)