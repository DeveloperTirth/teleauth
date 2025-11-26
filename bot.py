from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import secrets
import time

OTP_STORE = {}  # { chat_id: {"otp": ..., "expires": ... }}

BOT_TOKEN = "8444317320:AAFQhyWIGwFfZlVtaha69-pd9KuHFok3PnM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Welcome!\nYour chat ID is: {chat_id}")


async def send_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    otp = f"{secrets.randbelow(1000000):06d}"

    OTP_STORE[chat_id] = {
        "otp": otp,
        "expires": time.time() + 300
    }

    await update.message.reply_text(f"Your OTP is: {otp}")


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_otp = update.message.text.split(" ")[1]

    data = OTP_STORE.get(chat_id)
    if not data:
        await update.message.reply_text("No OTP found. Send /otp first.")
        return

    if time.time() > data["expires"]:
        await update.message.reply_text("OTP expired.")
        return

    if user_otp == data["otp"]:
        await update.message.reply_text("OTP Verified 🎉")
    else:
        await update.message.reply_text("Wrong OTP ❌")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("otp", send_otp))
    app.add_handler(CommandHandler("verify", verify))

    print("BOT IS RUNNING…")
    app.run_polling()


if __name__ == "__main__":
    main()
