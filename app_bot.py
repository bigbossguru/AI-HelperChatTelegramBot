import os
import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler

from lib.openai_models import answer, genrandimage
from lib.visa import visa_checker
from lib.translator import translate
from lib.utils.text_formatting import text_reduce, text_validation
from lib.speech import voice_recognition

from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

desc_bot = """🧠 <b>AI Chat</b>:
 - type command /chat [text]\n
🌅 <b>AI Generate Image</b>:
 - for a random image, click command /randimage
 - for your image, type command /myimage [desc]\n
📰 <b>Check Visa</b>:
 - type command /myvisa [number]
   <i>number format: XXXXX-DP-2023</i>\n
📒 <b>Translator</b>:
 - type command /translate [text]\n
🗣 <b>Voice message to text</b>:
 - send a normal voice message"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("media/ai.jpeg", "rb").read(),
        caption="Welcome to the Human being AI Chat!\nAsk me anything.\n\n" + desc_bot,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def randimage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    img, msg = genrandimage()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=img,
        caption=text_reduce(msg),
        reply_to_message_id=update.message.id,
    )


async def myimage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if user_input_data:
        img, _ = genrandimage(user_input_data)
        return await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img,
            caption=user_input_data,
            reply_to_message_id=update.message.id,
        )
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_to_message_id=update.message.id,
        text="🌅 To generate image:\n\nType /myimage followed by your prompt to generate an image using DALL-E.\n\n"
        + "Example:\n`/myimage digital illustration of medieval town, detailed, fantasy, 4K, trending on artstation`",
    )


async def myvisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if user_input_data and text_validation(user_input_data):
        return await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=visa_checker(user_input_data),
            reply_to_message_id=update.message.id,
        )
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_to_message_id=update.message.id,
        text="📰 <b>To check visa</b>:\n\nType /myvisa followed by your prompt.\n"
        + "<i>format your number: XXXXX-DP-2023</i>\n\n"
        + "Example:\n<code>/myvisa 01581-DP-2023</code>",
    )


async def mytranslate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if user_input_data:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translate(user_input_data, "ru"),
            reply_to_message_id=update.message.id,
        )
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_to_message_id=update.message.id,
        text="📒 <b>To translate text</b>:\n\nType /translate followed by your prompt.\n\n"
        + "Example:\n<code>/translate Hello world!</code>",
    )


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=desc_bot,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def myvoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = await context.bot.get_file(update.message.voice.file_id)
    file = await audio.download_to_drive()
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=voice_recognition(file),
        reply_to_message_id=update.message.id,
    )


async def gptchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if user_input_data:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=answer(user_input_data),
            reply_to_message_id=update.message.id,
        )
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_to_message_id=update.message.id,
        text="🧠 <b>To ask on the GPTChat</b>:\n\nType /chat followed by your prompt.\n\n"
        + "Example:\n<code>/chat Hello world!</code>",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chat", gptchat))
    application.add_handler(CommandHandler("myvisa", myvisa))
    application.add_handler(CommandHandler("myimage", myimage))
    application.add_handler(CommandHandler("randimage", randimage))
    application.add_handler(CommandHandler("translate", mytranslate))
    application.add_handler(CommandHandler("description", description))
    application.add_handler(MessageHandler(filters.VOICE & (~filters.COMMAND), myvoice))
    application.run_polling()
