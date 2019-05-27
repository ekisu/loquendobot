from .config import TOKEN
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hola! I'm a bot!")

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

updater.start_polling()
