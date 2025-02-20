import os
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токены из переменных среды
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Отсутствует TELEGRAM_BOT_TOKEN. Добавьте его в переменные окружения.")
if not OPENAI_API_KEY:
    raise ValueError("Отсутствует OPENAI_API_KEY. Добавьте его в переменные окружения.")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("⚒ Создать персонажа"))
main_menu.add(KeyboardButton("📂 Мои персонажи"), KeyboardButton("🔑 Подписка"))
main_menu.add(KeyboardButton("🌍 Язык"))

# Подменю уточнения деталей
details_menu = ReplyKeyboardMarkup(resize_keyboard=True)
details_menu.add(KeyboardButton("✍ Уточнять детали в чате"), KeyboardButton("📜 Заполнить анкету"))
details_menu.add(KeyboardButton("↩ Вернуться в главное меню"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я CharBot – AI-генератор персонажей.\n\nВыбери, что хочешь сделать:", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "⚒ Создать персонажа")
async def create_character(message: types.Message):
    await message.reply("✨ Функция генерации персонажа скоро будет добавлена!", reply_markup=details_menu)

@dp.message_handler(lambda message: message.text == "↩ Вернуться в главное меню")
async def back_to_main(message: types.Message):
    await message.reply("🔙 Главное меню", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "✍ Уточнять детали в чате")
async def refine_character(message: types.Message):
    await message.reply("📝 Напишите уточняющий запрос для персонажа.")

@dp.message_handler(lambda message: message.text == "📜 Заполнить анкету")
async def fill_form(message: types.Message):
    await message.reply("📜 Анкета скоро будет доступна!")

# Обработка текстовых запросов для генерации персонажей
@dp.message_handler()
async def generate_character(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Ты создаёшь описания персонажей."},
                      {"role": "user", "content": message.text}]
        )
        character_description = response["choices"][0]["message"]["content"]
        await message.reply(f"✅ Вот предварительная версия персонажа:\n\n{character_description}")
    except Exception as e:
        logging.error(f"Ошибка при запросе к OpenAI: {e}")
        await message.reply("❌ Произошла ошибка при генерации персонажа. Попробуйте снова позже.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
