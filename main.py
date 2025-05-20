import asyncio
import nest_asyncio
import re

from telegram import Update, Bot, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Apply nested event loop for environments like Replit
nest_asyncio.apply()

# === Bot Tokens ===
BOT_A_TOKEN = "7646385695:AAFV_sgRtysXcU9hJ90nGtGQ39FT_irBGWs"  # Replace with Bot A token
BOT_B_TOKEN = "6812123967:AAFX2dIWIJIFe4aahegIj6hpYqJ-o-uk2Io"  # Replace with Bot B token

# === Target Channels/User IDs ===
TARGET_CHANNELS = [
    -1002233816376,
    -1002056067443,
]

# === Bot B Target Chat ID ===
BOT_B_CHAT_ID = 1317278565  # Replace with valid user/channel ID that started chat with Bot B

# === Caption Processing Function ===
def process_caption(caption: str) -> str:
    lines = caption.split("\n")
    result = []

    for line in lines:
        if line.strip():
            result.append(line.strip())
        else:
            break

    processed_caption = "\n".join(result)

    if '@' in processed_caption:
        processed_caption = re.sub(r'@[\w]+', '@A1Moviescreations', processed_caption)
    else:
        processed_caption = "@A1Moviescreations - " + processed_caption

    marketing_text = """
❤️ Share With Friends ❤️👉‌‌

🍿Join Our Channel For Direct Link ✅ https://t.me/+uYIGxa4X4aA0MWQ9
"""
    processed_caption += "\n" + marketing_text
    processed_caption = f"<b>{processed_caption}</b>"

    return processed_caption

# === Command Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send a file or message with a caption to begin.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send media with a caption, and I will forward it with custom formatting.")

# === Main Message Handler ===
async def forward_to_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    caption_or_text = message.caption if message.caption else message.text or "No caption provided"
    processed_caption = process_caption(caption_or_text)

    # Reply to sender (Bot A)
    if message.document:
        await message.reply_document(document=message.document.file_id, caption=processed_caption, parse_mode="HTML")
    elif message.photo:
        await message.reply_photo(photo=message.photo[-1].file_id, caption=processed_caption, parse_mode="HTML")
    elif message.video:
        await message.reply_video(video=message.video.file_id, caption=processed_caption, parse_mode="HTML")
    elif message.audio:
        await message.reply_audio(audio=message.audio.file_id, caption=processed_caption, parse_mode="HTML")
    else:
        await message.reply_text(processed_caption, parse_mode="HTML")

    # Forward to channels
    for channel in TARGET_CHANNELS:
        try:
            if message.document:
                await context.bot.send_document(chat_id=channel, document=message.document.file_id, caption=processed_caption, parse_mode="HTML")
            elif message.photo:
                await context.bot.send_photo(chat_id=channel, photo=message.photo[-1].file_id, caption=processed_caption, parse_mode="HTML")
            elif message.video:
                await context.bot.send_video(chat_id=channel, video=message.video.file_id, caption=processed_caption, parse_mode="HTML")
            elif message.audio:
                await context.bot.send_audio(chat_id=channel, audio=message.audio.file_id, caption=processed_caption, parse_mode="HTML")
            else:
                await context.bot.send_message(chat_id=channel, text=processed_caption, parse_mode="HTML")
            print(f"Forwarded to {channel}")
        except Exception as e:
            print(f"Failed to forward to {channel}: {e}")

    # === Forward to Bot B ===
    bot_b = Bot(token=BOT_B_TOKEN)
    try:
        if message.document:
            await bot_b.send_document(chat_id=BOT_B_CHAT_ID, document=message.document.file_id, caption=processed_caption, parse_mode="HTML")
        elif message.photo:
            await bot_b.send_photo(chat_id=BOT_B_CHAT_ID, photo=message.photo[-1].file_id, caption=processed_caption, parse_mode="HTML")
        elif message.video:
            await bot_b.send_video(chat_id=BOT_B_CHAT_ID, video=message.video.file_id, caption=processed_caption, parse_mode="HTML")
        elif message.audio:
            await bot_b.send_audio(chat_id=BOT_B_CHAT_ID, audio=message.audio.file_id, caption=processed_caption, parse_mode="HTML")
        else:
            await bot_b.send_message(chat_id=BOT_B_CHAT_ID, text=processed_caption, parse_mode="HTML")
        print("Forwarded to Bot B")
    except Exception as e:
        print(f"Failed to forward to Bot B: {e}")

# === Setup Bot Commands ===
async def set_bot_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help using the bot"),
    ])

# === Main Function ===
async def main():
    app = ApplicationBuilder().token(BOT_A_TOKEN).build()
    await set_bot_commands(app)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.ALL, forward_to_channels))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
