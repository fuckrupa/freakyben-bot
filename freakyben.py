import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.filters import CommandStart
from aiogram import F
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Voice note directory
VOICE_DIR = "voices"

# Set bot commands
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Get started and see what I do"),
    ]
    await bot.set_my_commands(commands)

# /start command
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton(text="Support", url="https://t.me/TheCryptoElders")
        ],
        [
            InlineKeyboardButton(
                text="➕ Add Me To Your Group",
                url=f"https://t.me/{(await bot.me()).username}?startgroup=true"
            )
        ]
    ])

    welcome_text = (
        "<b>👋 Welcome to Ben Bot!</b>\n\n"
        "Just type something like:\n"
        "<code>ben... are you real?</code>\n\n"
        "I'll reply with a voice just like Talking Ben 🐶"
    )
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# Listen for messages starting with "ben..."
@dp.message(F.text.regexp(r"(?i)^ben\.\.\."))
async def ben_voice_reply(message: types.Message):
    try:
        voice_files = [f for f in os.listdir(VOICE_DIR) if f.endswith(".ogg")]
        if not voice_files:
            await message.reply("⚠️ No voice files found.")
            return

        selected_file = random.choice(voice_files)
        file_path = os.path.join(VOICE_DIR, selected_file)
        voice = FSInputFile(file_path)

        # Show "sending voice..." action
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_VOICE)
        await asyncio.sleep(1)  # Optional delay for realism

        # Send the voice note
        await message.answer_voice(voice)
    except Exception as e:
        await message.reply("❌ Something went wrong.")
        print(f"Error: {e}")

# Entry point
async def main():
    print("🚀 Bot is starting...")
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
