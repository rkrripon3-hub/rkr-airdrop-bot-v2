import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask
import threading
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# Render ২৪/৭ সচল রাখার ফ্লাস্ক সার্ভার
app = Flask(__name__)

@app.route('/')
def home():
    return "RKR Airdrop Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# চ্যানেল সাবস্ক্রিপশন চেক ফাংশন
async def is_user_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=config.CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception:
        return False

# /start কমান্ড হ্যান্ডলার
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    
    subscribed = await is_user_subscribed(user_id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("📢 Join Official Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@', '')}"),
            InlineKeyboardButton("🔄 Verify Membership", callback_data="check_sub")
        )
        await message.answer(
            "🔒 **RKR Airdrop Center**-এ প্রবেশ করতে প্রথমে আমাদের অফিশিয়াল চ্যানেলে জয়েন করুন:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return

    await send_main_menu(message)

# মেইন মেনু মেসেজ (মিনি অ্যাপ বাটনসহ)
async def send_main_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🚀 Open RKR Mini App", web_app=WebAppInfo(url=config.WEB_APP_URL)),
        InlineKeyboardButton("📢 Join Official Channel", url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@', '')}")
    )
    
    welcome_text = (
        f"🎉 **Welcome to RKR Airdrop Center!**\n\n"
        f"💰 **Rate:** 1 $RKR ≈ ${config.RKR_RATE_USD} USD\n"
        f"👥 **Referral Reward:** Get {config.REFERRAL_RKR_REWARD} $RKR + {config.REFERRAL_SPIN_REWARD} Spins!\n\n"
        f"নিচের **Open RKR Mini App** বাটনে ক্লিক করে কাজ শুরু করুন 👇"
    )
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

# ভেরিফাই বাটন হ্যান্ডলার
@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def process_callback_check_sub(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    subscribed = await is_user_subscribed(user_id)
    if subscribed:
        await bot.answer_callback_query(callback_query.id, "✅ Membership Verified!")
        await send_main_menu(callback_query.message)
    else:
        await bot.answer_callback_query(callback_query.id, "❌ আপনি এখনো চ্যানেলে জয়েন করেননি!", show_alert=True)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    executor.start_polling(dp, skip_updates=True)
    
