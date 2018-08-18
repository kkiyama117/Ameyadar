# Libs
# main
import json, os, math, urllib.request
from requests_oauthlib import OAuth1Session
from scipy.stats import norm
# devide config
from decouple import config


def get_weather():
    # Yahoo API
    YAHOO_APP_ID = config("YAHOO_APP_ID")

    COORDINATES = '135.7849,35.02799'  # longitude and latitude of KU

    RAIN_URL_BASE = 'https://map.yahooapis.jp/weather/V1/place?coordinates=%s' \
                    '&appid=%s&output=json&interval=10'
    rain_url = RAIN_URL_BASE % (COORDINATES, YAHOO_APP_ID)
    content = json.loads(
        urllib.request.urlopen(rain_url).read().decode('utf-8'))
    rainfall = 0
    for var in range(7):
        x = norm.pdf(var, 0, 5) / norm.pdf(0, 0, 5)
        y = content['Feature'][0]['Property']['WeatherList']['Weather'][var][
            'Rainfall']
        rainfall += x * y
    return rainfall


def get_twitter():
    # Twitter API
    twitter = OAuth1Session(config("CONSUMER_KEY"), config("CONSUMER_SECRET"),
                            config("ACCESS_TOKEN"),
                            config("ACCESS_TOKEN_SECRET"))
    return twitter


def get_username(twitter):
    req0 = twitter.get(
        'https://api.twitter.com/1.1/account/verify_credentials.json')
    return json.loads(req0.text)['name']


def get_new_user_name(rainfall, old_name):
    rain_emoji = ['🌂', '🌦', '☂️', '🌧', '☔', '⛈', '🌀']
    emoji = ''

    if rainfall != 0:
        cubed = min(math.ceil(math.log(math.ceil(rainfall), 3)), 6)
        emoji = rain_emoji[int(cubed)]
    for emoji in rain_emoji:
        old_name = old_name.replace(emoji, "")
    return old_name + emoji


def rename_user(new_name):
    twitter = OAuth1Session(config("CONSUMER_KEY"), config("CONSUMER_SECRET"),
                            config("ACCESS_TOKEN"),
                            config("ACCESS_TOKEN_SECRET"))
    twitter.post(
        'https://api.twitter.com/1.1/account/update_profile.json?name=%s'
        % new_name)
    print("new name: " + new_name)


def main():
    rename_user(get_new_user_name(get_weather(), get_username(get_twitter())))


if __name__ == '__main__':
    main()
