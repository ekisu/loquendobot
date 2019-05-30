from .secrets import TOKEN
from .tts import loquendo_tts
from .config import GTTS_LANGUAGE
from .utils import audio_segment_to_voice
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, InlineQueryHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hola! I'm a bot!")

def tts_command(update: Update, context: CallbackContext):
    logging.info("uhhh")
    query = " ".join(context.args)
    if not query:
        return
    
    logging.info("Inline: got {}".format(query))
    tts_segment = loquendo_tts(query, GTTS_LANGUAGE)
    tts_bytes = audio_segment_to_voice(tts_segment)
    context.bot.send_voice(chat_id=update.message.chat_id, voice=tts_bytes)

start_handler = CommandHandler("start", start, pass_args=True)
dispatcher.add_handler(start_handler)

tts_handler = CommandHandler("tts", tts_command)
dispatcher.add_handler(tts_handler)
updater.start_polling()
