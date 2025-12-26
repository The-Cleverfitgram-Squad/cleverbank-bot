from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8364602653:AAHfPX6WvCsm4TgnoqP1TGD5EOHHoV0eTlE"
CHANNEL_USERNAME = "@CleverBank_Community"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

    if member.status in ["left", "kicked"]:
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")]
        ]
        await update.message.reply_text(
            "👋 Привет!\n\nЧтобы разблокировать функции CleverBank — подпишись на наш канал 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await cabinet(update, context)

async def cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💎 Фармить CleverCoin"],
        ["🔁 Обменять CC"],
        ["🛒 Купить валюту"],
        ["👥 Реферальная ссылка"],
        ["🧾 Создать чек"],
        ["🆘 SOS by TCSupport"]
    ]
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text, callback_data=text)] for row in keyboard for text in row]
    )

    if update.message:
        await update.message.reply_text("🎆 Добро пожаловать в CleverBank!", reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(
            "🎆 Добро пожаловать в CleverBank!",
            reply_markup=reply_markup
        )

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

    if member.status not in ["left", "kicked"]:
        await cabinet(update, context)
    else:
        await query.answer("❌ Ты ещё не подписался", show_alert=True)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_sub, pattern="check_sub"))
    app.run_polling()

if __name__ == "__main__":
    main()
