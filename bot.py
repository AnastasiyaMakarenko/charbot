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
    raise ValueError("Отсутствует TELEGRAM_BOT_TOKEN. Убедитесь, что он добавлен в переменные окружения.")

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("🆕 Создать персонажа"))
main_menu.add(KeyboardButton("📁 Мои персонажи"), KeyboardButton("🔑 Подписка"))
main_menu.add(KeyboardButton("🌍 Язык"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Привет! Я CharBot – AI-генератор персонажей.\n"
        "Выбери, что хочешь сделать:",
        reply_markup=main_menu
    )

@dp.message_handler(lambda message: message.text == "🆕 Создать персонажа")
async def create_character(message: types.Message):
    await message.reply("✨ Функция генерации персонажа скоро будет добавлена!")

@dp.message_handler(lambda message: message.text == "📁 Мои персонажи")
async def my_characters(message: types.Message):
    await message.reply("📂 У вас пока нет сохранённых персонажей.")

@dp.message_handler(lambda message: message.text == "🔑 Подписка")
async def subscription_info(message: types.Message):
    await message.reply("💎 Подписка: 5$ в месяц.\n✅ Неограниченные персонажи и вариации.")

@dp.message_handler(lambda message: message.text == "🌍 Язык")
async def change_language(message: types.Message):
    await message.reply("🌎 Функция смены языка скоро появится!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
