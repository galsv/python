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

buttons_city = [["Москва", "Нижний Новгород"], ["Сочи", "Владивосток"]]


def get_weather(city):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return f"В городе <u>{city}</u> сейчас {w.detailed_status}, а температу вохдуха <b>{round(w.temperature('celsius')['temp'])}</b>\xb0"


@dp.message_handler(commands="weather")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(buttons_city)):
        keyboard.add(*buttons_city[i])
    await message.answer("Погода в каком городе вас интересует?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in [element for a_list in buttons_city for element in a_list])
async def without_puree(message: types.Message):
    print(message)
    await message.reply(get_weather(message["text"]), reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
