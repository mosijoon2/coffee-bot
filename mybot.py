from bale import Bot, Message, CallbackQuery
from bale.ui import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token="1361182146:PB6Ij4r-d55Q2P6urCUUPoEjpmJ15DXKWDA")

ADMIN_CHAT_ID = "1515323038"  # آیدی چت ادمین

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
        return

    order = pending_orders.get(message.chat.id)
    if not order:
        return

    # مرحله‌ی اول بعد از انتخاب محصول: گرفتن آدرس
    if order["stage"] == "address":
        order["address"] = message.content
        order["stage"] = "phone"
        await message.reply("📞 لطفاً شماره تماس خودتون رو وارد کنید:")
        return

    # مرحله‌ی دوم: گرفتن شماره تماس و نهایی کردن سفارش
    if order["stage"] == "phone":
        order["phone"] = message.content

        # پیام تایید به خود مشتری
        await message.reply(
            f"✅ سفارش شما ثبت شد!\n\n"
            f"📦 محصول: {order['product']}\n"
            f"📍 آدرس: {order['address']}\n"
            f"📞 شماره تماس: {order['phone']}\n\n"
            f"به زودی با شما تماس می‌گیریم 🙏"
        )

        # پیام نوتیفیکیشن به آیدی ادمین
        await bot.send_message(
            ADMIN_CHAT_ID,
            f"🔔 سفارش جدید!\n\n"
            f"👤 نام: {message.chat.first_name}\n"
            f"📦 محصول: {order['product']}\n"
            f"📍 آدرس: {order['address']}\n"
            f"📞 شماره تماس: {order['phone']}"
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

        pending_orders[callback.message.chat.id] = {"product": selected, "stage": "address"}

        await callback.message.reply(
            f"✅ انتخاب شما:\n{selected} — ۲۰۰ گرم\n\n"
            f"📍 حالا آدرس دقیق تحویلت رو بفرست:"
        )

bot.run()
