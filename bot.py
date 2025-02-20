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

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("⚒ Создать персонажа"), KeyboardButton("📁 Мои персонажи"))
main_menu.add(KeyboardButton("🔑 Подписка"), KeyboardButton("🌍 Язык"))

# Подменю создания персонажа
create_menu = ReplyKeyboardMarkup(resize_keyboard=True)
create_menu.add(KeyboardButton("✍ Уточнять детали в чате"), KeyboardButton("📜 Заполнить анкету"))
create_menu.add(KeyboardButton("🔙 Вернуться в главное меню"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я CharBot – AI-генератор персонажей.\n\nВыбери, что хочешь сделать:", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "⚒ Создать персонажа")
async def create_character_menu(message: types.Message):
    await message.reply("✨ Функция генерации персонажа скоро будет добавлена!", reply_markup=create_menu)

@dp.message_handler(lambda message: message.text == "📁 Мои персонажи")
async def my_characters(message: types.Message):
    await message.reply("📂 У вас пока нет сохранённых персонажей.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🔑 Подписка")
async def subscription_info(message: types.Message):
    await message.reply("🔑 Подписка: 5$ в месяц.\n✅ Неограниченные персонажи и вариации.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🌍 Язык")
async def change_language(message: types.Message):
    await message.reply("🌍 Функция смены языка скоро появится!", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🔙 Вернуться в главное меню")
async def back_to_main(message: types.Message):
    await message.reply("🔙 Главное меню", reply_markup=main_menu)

@dp.message_handler()
async def process_text_request(message: types.Message):
    text_request = message.text
    response_text = f"✅ Отлично! Вот предварительная версия персонажа:\n\n🔹 \"{text_request}\""
    await message.reply(response_text, reply_markup=create_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
