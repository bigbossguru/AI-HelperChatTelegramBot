import os
import datetime
import telegram
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
    CallbackContext,
)

# import aichattelegrambot.logger  # type: ignore
from aichattelegrambot.fetch import fetch
from aichattelegrambot.chat import gpt_response
from aichattelegrambot.visa import visa_checker
from aichattelegrambot.translator import translate
from aichattelegrambot.image import image_generator
from aichattelegrambot.voice import voice_recognition
from aichattelegrambot.utils.message_templates import desc_bot

from financeanalysis.analysis import ta_analysis


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("media/ai.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img.read(),
            caption="Welcome to the Human being AI Chat!\nAsk me anything.\n\n" + desc_bot,
            parse_mode=telegram.constants.ParseMode.HTML,
        )


async def randimage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        img, msg = await image_generator()
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img,
            caption=msg,
            reply_to_message_id=update.message.id,
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.id,
            text=str(e),
        )


async def myimage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if not user_input_data:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
            reply_to_message_id=update.message.id,
            text="🌅 To generate image:\n\nType /myimage followed by your prompt.\n\n"
            + "Example:\n`/myimage digital illustration of medieval town, detailed, fantasy, 4K.`",
        )
    try:
        img, _ = await image_generator(user_input_data)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img,
            caption=user_input_data,
            reply_to_message_id=update.message.id,
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.id,
            text=str(e),
        )


async def myvisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    try:
        if not user_input_data:
            raise
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=visa_checker(user_input_data),
            reply_to_message_id=update.message.id,
        )
    except Exception:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode=telegram.constants.ParseMode.HTML,
            reply_to_message_id=update.message.id,
            text="📰 <b>To check visa</b>:\n\nType /myvisa followed by your prompt.\n"
            + "<i>format your number: [12345-XX/CC-YYYY] or [12345/CC-YYYY]</i>\n\n"
            + "Example:\n<code>/myvisa 01581/DP-2023</code>",
        )


async def mytranslate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if not user_input_data:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode=telegram.constants.ParseMode.HTML,
            reply_to_message_id=update.message.id,
            text="📒 <b>To translate text</b>:\n\nType /translate followed by your prompt.\n\n"
            + "Example:\n<code>/translate Hello world!</code>",
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=await translate(user_input_data, "ru"),
        reply_to_message_id=update.message.id,
    )


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=desc_bot,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def magic_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await fetch("http://localhost:4040/api/tunnels")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data["tunnels"][0]["public_url"],
    )


async def myvoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = await context.bot.get_file(update.message.voice.file_id)
    file = await audio.download_to_drive()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=voice_recognition(file),
        reply_to_message_id=update.message.id,
    )


async def gptchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input_data = " ".join(context.args)
    if not user_input_data:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode=telegram.constants.ParseMode.HTML,
            reply_to_message_id=update.message.id,
            text="🧠 <b>To ask on the GPTChat</b>:\n\nType /chat followed by your prompt.\n\n"
            + "Example:\n<code>/chat Hello world!</code>",
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=gpt_response(user_input_data),
        reply_to_message_id=update.message.id,
    )


async def fin_analysis(context: CallbackContext):
    for img in ta_analysis():
        await context.bot.send_photo(
            chat_id=os.environ["TELEGRAM_ID_CHANNEL"],
            photo=img,
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chat", gptchat))
    application.add_handler(CommandHandler("myvisa", myvisa))
    application.add_handler(CommandHandler("myimage", myimage))
    application.add_handler(CommandHandler("randimage", randimage))
    application.add_handler(CommandHandler("translate", mytranslate))
    application.add_handler(CommandHandler("description", description))
    application.add_handler(CommandHandler("url", magic_url))
    application.add_handler(MessageHandler(filters.VOICE & (~filters.COMMAND), myvoice))

    job = application.job_queue
    job.run_repeating(callback=fin_analysis, interval=datetime.timedelta(minutes=1))
    application.run_polling()
