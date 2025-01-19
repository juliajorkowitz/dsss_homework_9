from telegram import Update
import torch
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hi! I am an AI assistant. How can I help you today?")


async def process(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
   
    prompt = f"The following is a conversation between a helpful AI assistant and a user.\nUser: {user_message}\nAI:"
    response = pipe(prompt, max_length=300, num_return_sequences=1)[0]['generated_text']
    
    bot_response = response.split("AI:")[1].strip() if "AI:" in response else response
    bot_response = bot_response.split("User:")[0].split("AI:")[-1].strip()
    await update.message.reply_text(bot_response)

def main() -> None:
    API_TOKEN = "7443919973:AAE9-UOdQxZ291JqFIpWl1ZCWldwnXpOTKQ" 
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process))

    application.run_polling()

if __name__ == "__main__":
    main()