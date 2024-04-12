from .secrets import TOKEN
from .tts import loquendo_tts
from .config import GTTS_LANGUAGE
from .utils import audio_segment_to_voice
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import asyncio
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id, text="Hola! I'm a bot!")

async def tts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        return
    
    logging.info("Inline: got {}".format(query))
    tts_segment = loquendo_tts(query, GTTS_LANGUAGE)
    tts_bytes = audio_segment_to_voice(tts_segment)
    await context.bot.send_voice(chat_id=update.message.chat_id, voice=tts_bytes)

start_handler = CommandHandler("start", start)
application.add_handler(start_handler)

tts_handler = CommandHandler("tts", tts_command)
application.add_handler(tts_handler)

def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(handle_telegram_update(event['body']))

async def handle_telegram_update(serialized_update: str):
    await application.initialize()

    update = Update.de_json(json.loads(serialized_update), application.bot)
    await application.process_update(update)

    return {
        'statusCode': 200,
        'body': 'success',
    }
