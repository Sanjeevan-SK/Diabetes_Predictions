from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import subprocess
import json

# 🔑 Replace with your Telegram bot token
BOT_TOKEN = "8338984623:AAH0kGmoTJ1xctPDAbhtjO8HI7FRm2VbLjg"

# In-memory user session tracking
user_sessions = {}

# ✅ Simple check: only reply to health-related questions
def is_health_related(text):
    keywords = ["health", "diet", "glucose", "sugar", "exercise", "bmi", "diabetes",
                "sleep", "doctor", "food", "heart", "bp", "body", "weight", "fitness", "insulin"]
    return any(k in text.lower() for k in keywords)

# 🦙 Use Ollama's LLaMA model for response
def ask_llama(prompt):
    try:
        # Run Ollama with LLaMA model (returns JSON)
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"⚠️ Error communicating with LLaMA: {str(e)}"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to your AI Health Assistant!\nPlease enter your name to continue:")

# Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_text = update.message.text.strip()

    # Step 1: Handle name input (first message)
    if user_id not in user_sessions:
        name = user_text
        user_sessions[user_id] = name

        # Check if name exists in database
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_records WHERE user_name=? ORDER BY date DESC LIMIT 1", (name,))
        row = cursor.fetchone()
        conn.close()

        if row:
            msg = (
                f"🩺 Hello {name}! Here's your latest health record:\n"
                f"📅 Date: {row[-1]}\n"
                f"Glucose: {row[4]} mg/dL\n"
                f"BMI: {row[3]}\n"
                f"Blood Pressure: {row[5]} mmHg\n"
                f"Risk Level: {row[10]}"
            )
            await update.message.reply_text(msg + "\n\n💬 You can now ask me any health-related question!")
        else:
            await update.message.reply_text(
                f"⚠️ Sorry {name}, I couldn’t find your records.\nPlease enter your details in the Streamlit app first."
            )
        return

    # Step 2: Handle general queries after name
    if not is_health_related(user_text):
        await update.message.reply_text("🚫 I can only answer health-related questions. Please ask about diet, glucose, or fitness.")
        return

    # Step 3: Generate AI response using Ollama (LLaMA)
    prompt = f"You are a helpful health assistant. Only give factual, general wellness and diabetes-related advice. Avoid diagnosing. User asked: {user_text}"
    answer = ask_llama(prompt)
    await update.message.reply_text("💡 " + answer)

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot running... Talk to it in Telegram!")
    app.run_polling()

if __name__ == "__main__":
    main()
