import json

import requests
from decouple import config
from scipy.stats import norm


def get_weather():
    # Yahoo API
    YAHOO_APP_ID = config("YAHOO_APP_ID")

    COORDINATES = '135.7849,35.02799'  # longitude and latitude of KU

    rain_url = 'https://map.yahooapis.jp/weather/V1/place'
    payload = {'coordinates': COORDINATES, 'appid': YAHOO_APP_ID,
               'output': 'json', 'interval': '10'}
    content = json.loads(
        requests.get(rain_url, params=payload).text)
    rainfall = 0
    for var in range(7):
        x = norm.pdf(var, 0, 5) / norm.pdf(0, 0, 5)
        # mm/h
        y = content['Feature'][0]['Property']['WeatherList']['Weather'][var][
            'Rainfall']
        # 過去の雨量を足す
        rainfall += x * y
    return rainfall


if __name__ == '__main__':
    print(get_weather())
