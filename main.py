import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# আপনার বটের টোকেন এবং চ্যানেল ইউজারনেম/আইডি
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHANNEL_USERNAME = "@YOUR_CHANNEL_USERNAME" # যেমন: @rkr_official_channel

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # চ্যানেল জয়েন চেক
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            keyboard = [
                [InlineKeyboardButton("📢 Join Official Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
                [InlineKeyboardButton("🔄 Check Membership", callback_data="check_membership")]
            ]
            await update.message.reply_text(
                "⚠️ অ্যাপ ব্যবহার করতে এবং রেফারেল বোনাস পেতে হলে আপনাকে অবশ্যই আমাদের চ্যানেলে জয়েন করতে হবে!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
    except Exception as e:
        pass

    # জয়েন করা থাকলে মিনি অ্যাপ ওপেন করার বাটন
    await update.message.reply_text("welcome to RKR Airdrop Center!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
