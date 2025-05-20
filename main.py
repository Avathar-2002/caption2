import asyncio
import nest_asyncio  # Ensure this is imported and applied
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

# Apply nest_asyncio to allow nested event loops (needed for environments like Jupyter)
nest_asyncio.apply()

# API Token for your bot (Bot A)
API_TOKEN = "7646385695:AAFV_sgRtysXcU9hJ90nGtGQ39FT_irBGWs"

# List of target channels (by username or channel ID)
TARGET_CHANNELS = [
    "@A1MoviescreationBot"
    -1002233816376,
    -1002056067443,
]

# Bot B API Token
BOT_B_API_TOKEN = "6511502428:AAFwzUFMsFcXlI1IGPBqRbBlWs1I5OeY_pc"

def process_caption(caption: str) -> str:
    """
    Process the caption:
    - Extract meaningful content from the caption up to an empty line.
    - Replace any username with '@A1Moviescreations' or append it if absent.
    - Add marketing content at the end.
    """
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

    processed_caption += "\n"

    marketing_text = """
❤️ Share With Friends ❤️👉‌‌

🍿Join Our Channel For Direct Link ✅ https://t.me/+uYIGxa4X4aA0MWQ9
"""
    processed_caption += marketing_text
    processed_caption = f"<b>{processed_caption}</b>"

    return processed_caption

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a file or message with a caption, and I'll process it.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot processes captions for your files. Just send me a file and a caption!")

async def forward_to_multiple_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text and file messages and forward them to multiple channels.
    """
    message_text = update.message.text  # Check for regular text message
    if not message_text:
        # If it's a media file, check for a caption or other content
        if update.message.caption:
            message_text = update.message.caption
        else:
            message_text = "Message does not contain any text or caption"

    # Process the caption if it's present
    processed_caption = process_caption(message_text)

    # First send the edited content to Bot A (the sender of the message)
    if update.message.document:
        await update.message.reply_document(
            document=update.message.document.file_id,
            caption=processed_caption,
            parse_mode="HTML"
        )
    elif update.message.photo:
        await update.message.reply_photo(
            photo=update.message.photo[-1].file_id,
            caption=processed_caption,
            parse_mode="HTML"
        )
    elif update.message.video:
        await update.message.reply_video(
            video=update.message.video.file_id,
            caption=processed_caption,
            parse_mode="HTML"
        )
    elif update.message.video_note:
        await update.message.reply_video_note(
            video_note=update.message.video_note.file_id,
            caption=processed_caption,
            parse_mode="HTML"
        )
    elif update.message.audio:
        await update.message.reply_audio(
            audio=update.message.audio.file_id,
            caption=processed_caption,
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(processed_caption, parse_mode="HTML")

    # Then forward the content (text or media) to each target channel
    for channel in TARGET_CHANNELS:
        try:
            if update.message.document:
                # Forward document to channels with the edited caption
                await context.bot.send_document(
                    chat_id=channel,
                    document=update.message.document.file_id,
                    caption=processed_caption,  # Edited caption
                    parse_mode="HTML"
                )
            elif update.message.photo:
                # Forward photo to channels with the edited caption
                await context.bot.send_photo(
                    chat_id=channel,
                    photo=update.message.photo[-1].file_id,  # Highest resolution photo
                    caption=processed_caption,  # Edited caption
                    parse_mode="HTML"
                )
            elif update.message.video:
                # Forward video to channels with the edited caption
                await context.bot.send_video(
                    chat_id=channel,
                    video=update.message.video.file_id,
                    caption=processed_caption,  # Edited caption
                    parse_mode="HTML"
                )
            elif update.message.video_note:
                # Forward video note to channels with the edited caption
                await context.bot.send_video_note(
                    chat_id=channel,
                    video_note=update.message.video_note.file_id,
                    caption=processed_caption,  # Edited caption
                    parse_mode="HTML"
                )
            elif update.message.audio:
                # Forward audio to channels with the edited caption
                await context.bot.send_audio(
                    chat_id=channel,
                    audio=update.message.audio.file_id,
                    caption=processed_caption,  # Edited caption
                    parse_mode="HTML"
                )
            else:
                # Forward text message to channels with the edited caption
                await context.bot.send_message(
                    chat_id=channel,
                    text=processed_caption,  # Edited text
                    parse_mode="HTML"
                )
            print(f"Message forwarded to {channel}")
        except Exception as e:
            print(f"Failed to forward to {channel}: {e}")

    # Forward the message to Bot B (send the complete media with the edited caption)
    bot_b = ApplicationBuilder().token(BOT_B_API_TOKEN).build()
    try:
        if update.message.document:
            # Forward document to Bot B with the edited caption
            await bot_b.bot.send_document(
                chat_id=1317278565,  # Replace with Bot B's actual chat ID
                document=update.message.document.file_id,
                caption=processed_caption,  # Edited caption
                parse_mode="HTML"
            )
        elif update.message.photo:
            # Forward photo to Bot B with the edited caption
            await bot_b.bot.send_photo(
                chat_id=1317278565,  # Replace with Bot B's actual chat ID
                photo=update.message.photo[-1].file_id,  # Highest resolution photo
                caption=processed_caption,  # Edited caption
                parse_mode="HTML"
            )
        elif update.message.video:
            # Forward video to Bot B with the edited caption
            await bot_b.bot.send_video(
                chat_id=1317278565,  # Replace with Bot B's actual chat ID
                video=update.message.video.file_id,
                caption=processed_caption,  # Edited caption
                parse_mode="HTML"
            )
        elif update.message.video_note:
            # Forward video note to Bot B with the edited caption
            await bot_b.bot.send_video_note(
                chat_id=1317278565,  # Replace with Bot B's actual chat ID
                video_note=update.message.video_note.file_id,
                caption=processed_caption,  # Edited caption
                parse_mode="HTML"
            )
        elif update.message.audio:
            # Forward audio to Bot B with the edited caption
            await bot_b.bot.send_audio(
                chat_id=1317278565,  # Replace with Bot B's actual chat ID
                audio=update.message.audio.file_id,
                caption=processed_caption,  # Edited caption
                parse_mode="HTML"
            )
        else:
            # Forward text message to Bot B with the edited caption
            await bot_b.bot.send_message(
                chat_id=1317278565,  # Replace with Bot B's actual chat ID
                text=processed_caption,  # Edited text message
                parse_mode="HTML"
            )
        print("Message forwarded to Bot B")
    except Exception as e:
        print(f"Failed to forward to Bot B: {e}")

async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help using the bot"),
    ]
    await app.bot.set_my_commands(commands)

async def main():
    tg_app = ApplicationBuilder().token(API_TOKEN).build()

    # Set bot commands
    await set_bot_commands(tg_app)

    # Command handlers
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CommandHandler("help", help_command))

    # Handle all incoming messages and forward them to the channels
    tg_app.add_handler(MessageHandler(filters.ALL, forward_to_multiple_channels))

    print("Bot is running...")

    # Start polling the bot
    await tg_app.run_polling()

if __name__ == "__main__":
    # Replace asyncio.run with await main() since an event loop is already running
    asyncio.get_event_loop().run_until_complete(main())
