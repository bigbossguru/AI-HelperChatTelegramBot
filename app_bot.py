import os
import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler

from lib.openai_models import answer, genrandimage
from lib.visa import visa_checker
from lib.translator import translate

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
desc_bot = """<b>AI Chat</b>:
 - type a normal message
<b>AI Generate Image</b>:
 - for a random image, click command /randimage
 - for your own image, type command /myimage [desc]
<b>Check Visa</b>:
 - type command /myvisa [number]
   <i>number format: XXXXX-DP-2023</i>
<b>Translator</b>:
 - type command /translate [text]"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("media/ai.jpeg", "rb").read(),
        caption="Welcome to the Human being AI Chat!\nAsk me anything.\n\n" + desc_bot,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def randimage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    img, msg = genrandimage()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=msg)


async def mycommon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flag = True
    cmd, msg = update.message.text[:8], update.message.text[8:]
    if cmd == "/myimage" and len(msg) > 5:
        flag = False
        img, msg = genrandimage(msg)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=msg)
    cmd, msg = update.message.text[:7], update.message.text[7:]
    if cmd == "/myvisa" and len(msg) > 5:
        flag = False
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=visa_checker(msg))
    cmd, msg = update.message.text[:10], update.message.text[10:]
    if cmd == "/translate" and len(msg) >= 1:
        flag = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text=translate(msg, "ru"))
    if flag:
        await update.effective_message.reply_text("Wrong input data, please try again")


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=desc_bot, parse_mode=telegram.constants.ParseMode.HTML
    )


async def response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer(update.message.text))


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_BOT_TOKEN")).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    randimage_handler = CommandHandler("randimage", randimage)
    application.add_handler(randimage_handler)

    desc_handler = CommandHandler("description", description)
    application.add_handler(desc_handler)

    mycommon_handler = MessageHandler(filters.COMMAND & filters.TEXT, mycommon, False)
    application.add_handler(mycommon_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), response)
    application.add_handler(echo_handler)

    application.run_polling()
