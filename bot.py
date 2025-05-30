import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
import logging

BOT_TOKEN = "7796296335:AAFFUdOI_Qnj95VkGA8JaRzh-jJAclVOqug"
ADMINS = [7752032178]

foydalanuvchilar = set()

ADMIN_CONTACTS = """
📞 +998 94 089-81-19
"""

async def start_handler(message: Message):
    foydalanuvchilar.add(message.from_user.id)
    await message.answer(
        "👋 <b>Salom!</b>\n\n"
        "🛍 Kerakli mahsulot yoki xizmat nomini yozing.\n"
        "📨 Biz uni administratorlarga yetkazamiz va ular siz bilan tez orada bog‘lanadi.\n\n"
        "✏️ Marhamat, yozishni boshlang!",
        parse_mode=ParseMode.HTML
    )

async def text_handler(message: Message, bot: Bot):
    foydalanuvchilar.add(message.from_user.id)

    # Foydalanuvchi haqida ma'lumot: username yoki id
    user_identifier = f"@{message.from_user.username}" if message.from_user.username else f"id: <a href='tg://user?id={message.from_user.id}'>{message.from_user.id}</a>"

    user_info = (
        f"💬 <b>Yangi so‘rov!</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user_identifier}\n"
        f"{ADMIN_CONTACTS}\n"
        f"📩 <b>Xabar:</b> <i>{message.text}</i>"
    )

    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, user_info, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.warning(f"Admin xatoligi: {e}")

    await message.answer(
        "🆗 <b>So‘rovingiz yuborildi!</b>\n"
        "📞 So‘rovingiz bo‘yicha adminlar bilan bog'laning.\n" \
        "spam bolsez admnlar ozi boglnadi sz biln",
        parse_mode=ParseMode.HTML
    )

async def reklama_handler(message: Message, bot: Bot):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 Siz bu buyruqdan foydalana olmaysiz.")

    matn = message.text.replace("/reklama", "").strip()
    if not matn:
        return await message.answer("❗ Iltimos, reklama matnini yozing.\nMasalan:\n/reklama 🎉 Yangi aksiyalar boshlandi!")

    reklama_xabar = f"""
📢 <b>YANGI REKLAMA!</b>

{matn}

🔔 Bizni kuzatib boring!
"""

    count = 0
    for user_id in foydalanuvchilar:
        try:
            await bot.send_message(user_id, reklama_xabar, parse_mode=ParseMode.HTML)
            count += 1
        except:
            pass

    await message.answer(f"✅ Reklama {count} ta foydalanuvchiga yuborildi!")

async def foydalanuvchilar_handler(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 Bu buyruq faqat administratorlar uchun.")

    await message.answer(
        f"👥 Botdan hozirgacha <b>{len(foydalanuvchilar)}</b> ta foydalanuvchi foydalangan.",
        parse_mode=ParseMode.HTML
    )

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.message.register(start_handler, Command("start"))
    dp.message.register(reklama_handler, F.text.startswith("/reklama"))
    dp.message.register(foydalanuvchilar_handler, Command("foydalanuvchilar"))
    dp.message.register(text_handler)

    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
