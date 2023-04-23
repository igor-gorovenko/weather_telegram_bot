import datetime
import requests
from pprint import pprint
from config import open_weather_token

def get_weather(city, open_weather_token):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

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

        print(f"***{datetime.datetime.now().strftime(' %Y-%m-%d %H:%M ')}***\n"
              f"Weather in city: {city}, {country}\n"
              f"Temperature now: {round(temp_cur)} C {wd} \n"
              f"min: {round(temp_min)}, max: {round(temp_max)}\n"
              f"Sunset time: {sunset_timestamp}"
              )

    except Exception as ex:
        print(ex)
        print("Check city name")

def main():
    city = input("City: ")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()

