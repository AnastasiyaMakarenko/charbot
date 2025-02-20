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

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("🛠 Создать персонажа"))
main_menu.add(KeyboardButton("📂 Мои персонажи"), KeyboardButton("🔑 Подписка"))
main_menu.add(KeyboardButton("🌍 Язык"))

# Меню после запроса создания персонажа
character_menu = ReplyKeyboardMarkup(resize_keyboard=True)
character_menu.add(KeyboardButton("📝 Уточнять детали в чате"))
character_menu.add(KeyboardButton("📜 Заполнить анкету"))
character_menu.add(KeyboardButton("🔙 Вернуться в главное меню"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я CharBot – AI-генератор персонажей.\n\nВыбери, что хочешь сделать:", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🛠 Создать персонажа")
async def create_character(message: types.Message):
    await message.reply("✨ Функция генерации персонажа скоро будет добавлена!", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "📂 Мои персонажи")
async def my_characters(message: types.Message):
    await message.reply("📂 У вас пока нет сохранённых персонажей.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🔑 Подписка")
async def subscription_info(message: types.Message):
    await message.reply("🔑 Подписка: 5$ в месяц.\n✅ Неограниченные персонажи и вариации.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🌍 Язык")
async def change_language(message: types.Message):
    await message.reply("🌍 Функция смены языка скоро появится!", reply_markup=main_menu)

@dp.message_handler()
async def handle_text(message: types.Message):
    user_text = message.text.strip()
    if user_text:
        response = f"✅ Отлично! Бот предварительная версия персонажа:\n\n🔹 \"{user_text}\"\n\nДальше ты сможешь его уточнить или изменить!"
        await message.reply(response, reply_markup=character_menu)

@dp.message_handler(lambda message: message.text == "🔙 Вернуться в главное меню")
async def return_to_main(message: types.Message):
    await message.reply("🔙 Главное меню", reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
