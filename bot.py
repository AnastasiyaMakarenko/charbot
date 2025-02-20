import os
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токены из переменных среды
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise ValueError("Отсутствует TELEGRAM_BOT_TOKEN. Убедитесь, что он добавлен в переменные окружения.")

if not OPENAI_API_KEY:
    raise ValueError("Отсутствует OPENAI_API_KEY. Добавьте его в переменные окружения.")

# Инициализация бота и OpenAI API
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("🛠 Создать персонажа"), KeyboardButton("🔑 Подписка"))
main_menu.add(KeyboardButton("📁 Мои персонажи"), KeyboardButton("🌍 Язык"))

# Меню генерации
generation_menu = ReplyKeyboardMarkup(resize_keyboard=True)
generation_menu.add(KeyboardButton("📝 Уточнять детали в чате"), KeyboardButton("📜 Заполнить анкету"))
generation_menu.add(KeyboardButton("⬅️ Вернуться в главное меню"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Я CharBot – AI-генератор персонажей.\n\nВыбери, что хочешь сделать:", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "🛠 Создать персонажа")
async def create_character(message: types.Message):
    await message.reply("✨ Введи описание персонажа или выбери вариант ниже:", reply_markup=generation_menu)

@dp.message_handler(lambda message: message.text == "⬅️ Вернуться в главное меню")
async def back_to_main(message: types.Message):
    await message.reply("🏠 Главное меню", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "📜 Заполнить анкету")
async def fill_survey(message: types.Message):
    await message.reply("📝 Анкета скоро появится!")

@dp.message_handler(lambda message: message.text == "📝 Уточнять детали в чате")
async def refine_character(message: types.Message):
    await message.reply("✏️ Введи уточняющие детали.")

@dp.message_handler()
async def generate_character(message: types.Message):
    user_input = message.text.lower()

    # Если пользователь хочет сгенерировать изображение
    if any(keyword in user_input for keyword in ["нарисуй", "сгенерируй", "изображение", "арт"]):
        await message.reply("🎨 Генерирую изображение... Подождите.")

        try:
            response = openai.Image.create(
                prompt=user_input,
                n=1,
                size="1024x1024"
            )
            image_url = response["data"][0]["url"]
            await message.reply_photo(photo=image_url, caption="✅ Вот ваш персонаж!", reply_markup=generation_menu)

        except Exception as e:
            logging.error(f"Ошибка при генерации изображения: {e}")
            await message.reply("⚠️ Ошибка при генерации изображения. Попробуйте снова.")

    # Если пользователь хочет текстовое описание
    else:
        await message.reply("🔄 Генерация ответа... Пожалуйста, подождите.")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=500
            )
            gpt_reply = response["choices"][0]["message"]["content"]
            await message.reply(f"✅ Вот ваш персонаж:\n\n{gpt_reply}", reply_markup=generation_menu)

        except Exception as e:
            logging.error(f"Ошибка при запросе к OpenAI: {e}")
            await message.reply("⚠️ Произошла ошибка при генерации персонажа. Попробуйте снова.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
