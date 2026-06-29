from bale import Bot, Message, CallbackQuery
from bale.ui import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token="2028859092:UgoIEu76EzRSCwkFSP1uRfqoT8EWaRDxbso")

pending_orders = {}

@bot.event
async def on_before_ready():
    await bot.delete_webhook()

@bot.event
async def on_message(message: Message):
    if message.content == "/start":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("☕ سفارش قهوه", callback_data="order"))
        await message.reply("سلام! به فروشگاه قهوه مارکو خوش اومدی ☕", components=keyboard)

    elif message.chat.id in pending_orders:
        order = pending_orders[message.chat.id]
        address = message.content

        await message.reply(
            f"✅ سفارش شما ثبت شد!\n\n"
            f"📦 محصول: {order['product']}\n"
            f"📍 آدرس: {address}\n\n"
            f"به زودی با شما تماس می‌گیریم 🙏"
        )

        await bot.send_message(
            "1678159237",
            f"🔔 سفارش جدید!\n\n"
            f"👤 نام: {message.chat.first_name}\n"
            f"📦 محصول: {order['product']}\n"
            f"📍 آدرس: {address}"
        )

        del pending_orders[message.chat.id]

@bot.event
async def on_callback(callback: CallbackQuery):

    if callback.data == "order":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("روبوستا ۱۰۰٪", callback_data="robusta"))
        keyboard.add(InlineKeyboardButton("ترکیبی ۸۰/۲۰", callback_data="blend"))
        await callback.message.reply(
            "📦 بسته‌های موجود:\n\n"
            "🟤 روبوستا ۱۰۰٪ — ۲۰۰ گرم\n"
            "🫘 ترکیب ۸۰/۲۰ — ۲۰۰ گرم\n\n"
            "یکی رو انتخاب کن 👇",
            components=keyboard
        )

    elif callback.data == "robusta":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("✅ آسیاب شده", callback_data="robusta_ground"))
        keyboard.add(InlineKeyboardButton("🫘 دانه", callback_data="robusta_bean"))
        await callback.message.reply(
            "🟤 روبوستا ۱۰۰٪\n\nآسیاب شده یا دانه؟ 👇",
            components=keyboard
        )

    elif callback.data == "blend":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("✅ آسیاب شده", callback_data="blend_ground"))
        keyboard.add(InlineKeyboardButton("🫘 دانه", callback_data="blend_bean"))
        await callback.message.reply(
            "🫘 ترکیبی ۸۰/۲۰\n\nآسیاب شده یا دانه؟ 👇",
            components=keyboard
        )

    elif callback.data in ["robusta_ground", "robusta_bean", "blend_ground", "blend_bean"]:
        products = {
            "robusta_ground": "🟤 روبوستا ۱۰۰٪ — آسیاب شده",
            "robusta_bean": "🟤 روبوستا ۱۰۰٪ — دانه",
            "blend_ground": "🫘 ترکیبی ۸۰/۲۰ — آسیاب شده",
            "blend_bean": "🫘 ترکیبی ۸۰/۲۰ — دانه",
        }
        selected = products[callback.data]

        pending_orders[callback.message.chat.id] = {"product": selected}

        await callback.message.reply(
            f"✅ انتخاب شما:\n{selected} — ۲۰۰ گرم\n\n"
            f"📍 حالا آدرس دقیق تحویلت رو بفرست:"
        )

bot.run()
