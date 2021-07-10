import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import os
from os.path import join, dirname

from pyowm import OWM
from pyowm.utils.config import get_config_from


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


# Объект погоды
config_dict = get_config_from('config.json')
owm = OWM(get_from_env("WEATHER_TOKEN"), config_dict)
mgr = owm.weather_manager()

# Объект бота
bot = Bot(token=get_from_env("BOT_TOKEN"), parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


def get_weather(city):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return f"В городе <u>{city}</u> сейчас  {w.detailed_status}, а температу вохдуха <b>{round(w.temperature('celsius')['temp'])}</b>\xb0"


@dp.message_handler(commands="weather")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Москва", "Нижний Новгород"]
    keyboard.add(*buttons)
    await message.answer("Погоду в каком городе вас интересует?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Москва")
async def without_puree(message: types.Message):
    await message.reply(get_weather("Москва"), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == "Нижний Новгород")
async def without_puree(message: types.Message):
    await message.reply(get_weather("Нижний Новгород"), reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
