import os
import logging
# from datetime import datetime
from telegram.ext import ApplicationBuilder, CallbackContext

from aichattelegrambot.visa import visa_checker


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def myvisa(context: CallbackContext):
    user_input_data = "26440/TP-2024"
    await context.bot.send_photo(
        chat_id=os.environ["TELEGRAM_ID_CHANNEL"],
        photo=visa_checker(user_input_data)
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()

    job = application.job_queue
    job.run_repeating(callback=myvisa, interval=120.0, first=0.0)
    # job.run_daily(callback=myvisa, time=datetime.time(hour=16))
    application.run_polling()
