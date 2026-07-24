import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_USER_ID", "0"))
MINIAPP_URL = os.getenv("MINIAPP_URL", "http://localhost:8000")

# ==================== START (Premium Promo like screenshot) ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Live Chart", web_app=WebAppInfo(url=f"{MINIAPP_URL}/miniapp"))],
        [InlineKeyboardButton("🤖 Ask AI (coming soon)", callback_data="ai")],
        [InlineKeyboardButton("📊 Stats & Accuracy", callback_data="stats")],
        [InlineKeyboardButton("💎 Grab Your Membership", url="https://your-payment-link.com")],  # ← change this
    ]
    
    text = """🚀 <b>GG-Shot | Predictum</b>

<b>Bot is Live !!!</b> 🌱

<b>Extreme Accurate futures Call</b>
10X Low-Risk Leverage 🧲

<b>timeframe for Accurate Position</b> 📱
5m | Scalp
15m | Short-Term
30m | Mid-Term
1h | Mid-Term
4h | Long-Term

<b>Back-Test for Accurate Position</b> 📚
Last 5  → 92% Accurate
Last 10 → 93% Accurate
Last 20 → 94% Accurate

<b>Grab Your Membership Here</b> 📦
Purchase & Delivery is instant 💿"""

    await update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


# ==================== POST SIGNAL (Premium format like screenshot) ====================
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
    targets_text = "\n".join([f"🎯 Target {i+1}: <b>{t.strip()}</b>" for i, t in enumerate(targets_list)])

    text = f"""<b>GG-Shot LEAK</b> 📩 <b>Predictum LEAK</b>

<b>Extreme Accurate futures Call</b>
10X Low-Risk Leverage 🧲

<b>timeframe for Accurate Position</b> 📱
5m | Scalp
15m | Short-Term
30m | Mid-Term
1h | Mid-Term
4h | Long-Term

{targets_text}

🛑 <b>Stop-Loss:</b> {sl}
📊 <b>Strategy Accuracy:</b> {accuracy}%

<b>Back-Test for Accurate Position</b> 📚
Last 5 → 92% | Last 10 → 93% | Last 20 → 94%

Bot is Live !!! 🌱
Grab Your Membership Here 📦 (instant delivery)"""

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
    await update.message.reply_text("✅ Signal posted successfully! (premium style)")


# ==================== STATS COMMAND ====================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📊 <b>GG-Shot | Predictum Back-Test Stats</b>

Last 5 signals  → 92% Accurate
Last 10 signals → 93% Accurate
Last 20 signals → 94% Accurate

Bot is Live !!! 🌱
Join the winning side!"""
    await update.message.reply_text(text, parse_mode="HTML")


# ==================== MAIN ====================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("postsignal", post_signal))
    app.add_handler(CommandHandler("stats", stats))

    # AI is temporarily disabled to prevent crashes (we'll fix it later)
    # app.add_handler(MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), ai_support))

    print("✅ GG-Shot Bot is running... (Polling mode)")
    app.run_polling()


if __name__ == "__main__":
    main()
