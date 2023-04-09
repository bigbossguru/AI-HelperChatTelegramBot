async def unavailable_service(update, context) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.id,
        text="Temporarily unavailable all OPENAI Services",
    )
