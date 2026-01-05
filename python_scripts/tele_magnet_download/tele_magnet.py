import re
import os
from pathlib import Path
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from functions import get_torrentDownload, get_torrentID
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler, ContextTypes

# initialise "telePython.env", raises a message if .env is not found
REPO_ROOT = Path(__file__).resolve().parents[2]
ENV = os.getenv("ENV", "prod")
env_path = REPO_ROOT / "gitops" / "env" / ENV / "telePython.env"

if not env_path.exists():
    raise FileNotFoundError(f"telePython.env file not found: {env_path}")

# from "telePython.env", populates the env vars
load_dotenv(env_path)
magnet = os.getenv('MAGNET_TEST')
TELE_BOT_TOKEN = os.getenv('TELE_BOT_TOKEN')

INLINE_KB  = InlineKeyboardMarkup([
    [InlineKeyboardButton("Example Magnet (Big Buck Bunny)", callback_data="EXAMPLE_BBB")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "IDLE"
    await update.message.reply_text(
        "Send / start the flow.\n\nTap **📥 Paste Magnet** to begin.",
        reply_markup=INLINE_KB,
        parse_mode="Markdown",
    )
    
async def message_handler(update, context):
    receivedMessage = update.message.text
    if receivedMessage == "Example Magnet (Big Buck Bunny)":
        receivedMessage = "magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c&dn=Big Buck Bunny"
    
    get_torrent = get_torrentID(receivedMessage)
    downloadLink = get_torrentDownload(get_torrent['torrentID'])
    text = downloadLink['downloadLink']
    await update.message.reply_text(f"Download Link: {text}")
    print(downloadLink)

def main():
    app = Application.builder().token(TELE_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()