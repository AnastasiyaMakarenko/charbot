from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os

# Получаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Отсутствует TELEGRAM_BOT_TOKEN. Добавьте его в переменные окружения.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("✍ Ввести описание"), KeyboardButton("📋 Ответить на вопросы"))

# Клавиатура уточнения после генерации
refine_menu = ReplyKeyboardMarkup(resize_keyboard=True)
refine_menu.add(KeyboardButton("✍ Продолжить уточнения текстом"), KeyboardButton("📋 Заполнить анкету"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Я CharBot – AI-генератор персонажей.\n\nКак вы хотите создать персонажа?", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "✍ Ввести описание")
async def create_character_text(message: types.Message):
    await message.reply("✍ Напишите описание персонажа, и я попробую его сгенерировать!")

@dp.message_handler(lambda message: message.text == "📋 Ответить на вопросы")
async def start_character_quiz(message: types.Message):
    await message.reply("📋 Давайте создадим персонажа!\n\nКакой у него пол?", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True)
                         .add("🚹 Мужской", "🚺 Женский", "❓ Другой"))

@dp.message_handler(lambda message: message.text in ["🚹 Мужской", "🚺 Женский", "❓ Другой"])
async def ask_age(message: types.Message):
    await message.reply("🧑 Какой возраст у персонажа?", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True)
                         .add("👶 Ребёнок", "🧑 Взрослый", "👴 Пожилой"))

# (Здесь можно продолжить остальные вопросы...)

@dp.message_handler(lambda message: message.text == "Готово")  # Когда пользователь завершит анкету
async def finish_character_quiz(message: types.Message):
    await message.reply("✨ Персонаж создан!\n\nХотите уточнить детали?", reply_markup=refine_menu)

@dp.message_handler(lambda message: message.text == "✍ Продолжить уточнения текстом")
async def refine_character_text(message: types.Message):
    await message.reply("✍ Напишите дополнительные уточнения о персонаже!")

@dp.message_handler(lambda message: message.text == "📋 Заполнить анкету")
async def refine_character_quiz(message: types.Message):
    await start_character_quiz(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
