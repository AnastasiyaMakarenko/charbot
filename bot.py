import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных среды
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Отсутствует TELEGRAM_BOT_TOKEN. Убедись, что он добавлен в переменные окружения.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📝 Создать персонажа"))
main_menu.add(KeyboardButton("📂 Мои персонажи"), KeyboardButton("🔑 Подписка"))
main_menu.add(KeyboardButton("🌍 Язык"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я CharBot – AI-генератор персонажей.\n\nВыбери, что хочешь сделать:",
        reply_markup=main_menu
    )

# Обработчик кнопки "Создать персонажа"
@dp.message_handler(lambda message: message.text == "📝 Создать персонажа")
async def create_character_choice(message: types.Message):
    await message.reply(
        "Как ты хочешь создать персонажа?\n\n📝 Напиши текстом описание\n📋 Заполни анкету",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("📝 Написать текстом"),
            KeyboardButton("📋 Заполнить анкету"),
            KeyboardButton("⬅️ Назад")
        )
    )

# Обработчик текстового ввода для персонажа
@dp.message_handler(lambda message: message.text == "📝 Написать текстом")
async def create_character_text(message: types.Message):
    await message.reply("✍️ Напиши описание персонажа. Например:\n\n'Высокий воин с огненно-рыжими волосами и татуировками, одетый в доспехи будущего'.")

# Обработчик, если пользователь отправил текстовое описание
@dp.message_handler()
async def process_character_description(message: types.Message):
    user_input = message.text.strip()
    if len(user_input) < 10:
        await message.reply("Описание слишком короткое. Напиши чуть подробнее!")
    else:
        await message.reply(f"✅ Отлично! Вот предварительная версия персонажа:\n\n🔹 {user_input}\n\n🚀 Дальше ты сможешь его уточнить или изменить!")

# Обработчик анкеты (пока заглушка)
@dp.message_handler(lambda message: message.text == "📋 Заполнить анкету")
async def create_character_form(message: types.Message):
    await message.reply("📋 Функция заполнения анкеты скоро появится!")

# Обработчик кнопки "Мои персонажи"
@dp.message_handler(lambda message: message.text == "📂 Мои персонажи")
async def my_characters(message: types.Message):
    await message.reply("📂 У вас пока нет сохранённых персонажей.")

# Обработчик кнопки "Подписка"
@dp.message_handler(lambda message: message.text == "🔑 Подписка")
async def subscription_info(message: types.Message):
    await message.reply("🔑 Подписка: 5$ в месяц.\n✅ Неограниченные персонажи и вариации.")

# Обработчик кнопки "Язык"
@dp.message_handler(lambda message: message.text == "🌍 Язык")
async def change_language(message: types.Message):
    await message.reply("🌍 Функция смены языка скоро появится!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
