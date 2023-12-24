
import requests
import datetime

from config import tg_bot_token, open_weather_token
from aiogram import Bot, types, Dispatcher, executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")

@dp.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        country = data["sys"]["country"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "See in window"

        temp_cur = data["main"]["temp"]
        temp_max = data["main"]["temp_max"]
        temp_min = data["main"]["temp_min"]
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f"***{datetime.datetime.now().strftime(' %Y-%m-%d %H:%M ')}***\n"
              f"Weather in city: {city}, {country}\n"
              f"Temperature now: {round(temp_cur)} C {wd} \n"
              f"min: {round(temp_min)}, max: {round(temp_max)}\n"
              f"Sunset time: {sunset_timestamp}"
              )

    except:
        await message.reply("\U00002628 Проверьте название города \U00002628")

if __name__ == '__main__':
    executor.start_polling(dp)