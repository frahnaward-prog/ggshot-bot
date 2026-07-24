import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_USER_ID", "0"))

# This will be your Railway URL later (example: https://ggshot-bot.up.railway.app)
MINIAPP_URL = os.getenv("MINIAPP_URL", "http://localhost:8000")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Live Chart", web_app=WebAppInfo(url=f"{MINIAPP_URL}/miniapp"))],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")]
    ]
    await update.message.reply_text(
        "🚀 Welcome to GG-Shot Bot!\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def post_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Only admin can post signals.")
        return

    args = context.args
    if len(args) < 6:
        await update.message.reply_text(
            "Usage:\n/postsignal PAIR DIRECTION ENTRY TARGETS SL ACCURACY\n\n"
            "Example:\n/postsignal VIRTUALUSDT Long 0.5691-0.5972 0.6050,0.6127,0.6205,0.6438 0.5617 93"
        )
        return

    pair = args[0].upper()
    direction = args[1]
    entry = args[2]
    targets = args[3]
    sl = args[4]
    accuracy = args[5]

    targets_list = targets.split(",")
    targets_text = "\n".join([f"🎯 Target {i+1}: {t.strip()}" for i, t in enumerate(targets_list)])

    text = f"""<b>#{pair} 1h | Mid-Term</b>

📈 <b>{direction} Entry Zone:</b> {entry}

{targets_text}

🛑 <b>Stop-Loss:</b> {sl}

📊 Strategy Accuracy: {accuracy}%
"""

    miniapp_link = (
        f"{MINIAPP_URL}/miniapp"
        f"?pair={pair}&direction={direction}&entry={entry}"
        f"&targets={targets}&sl={sl}&accuracy={accuracy}"
    )

    keyboard = [[
        InlineKeyboardButton("📈 Live Chart", web_app=WebAppInfo(url=miniapp_link)),
        InlineKeyboardButton("📊 Full Analysis", callback_data="analysis")
    ]]

    await update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("✅ Signal posted successfully!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("postsignal", post_signal))

    # Check if running on Railway
    if os.getenv("RAILWAY_ENVIRONMENT"):
        # Production mode (Webhook)
        port = int(os.getenv("PORT", 8080))
        domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        webhook_url = f"https://{domain}/webhook"

        print(f"✅ Starting in Production mode with webhook: {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path="webhook",
            webhook_url=webhook_url
        )
    else:
        # Local mode
        print("✅ GG-Shot Bot is running in Local mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
