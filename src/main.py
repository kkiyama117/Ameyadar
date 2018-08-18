# Libs
# main
import json
import math
import urllib.request

# divide config
from decouple import config
from scipy.stats import norm

from src.AccountEditor import TwitterAccountEditor, AccountEditor


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


def get_new_user_name(rainfall, old_name):
    rain_emoji = ['🌂', '🌦', '☂️', '🌧', '☔', '⛈', '🌀']
    emoji = ''

    if rainfall != 0:
        cubed = min(math.ceil(math.log(math.ceil(rainfall), 3)), 6)
        emoji = rain_emoji[int(cubed)]
    for emoji in rain_emoji:
        old_name = old_name.replace(emoji, "")
    return old_name + emoji


def main(account: AccountEditor = TwitterAccountEditor()):
    """ メインの関数

    :usage: `main()` - defaultのアカウント(Twitter)が呼ばれる.
            `main(account)` - AccountEditorに対応するアカウントが呼ばれる.
                              AccountEditorそのものの場合標準出力のみ行う
    :param account: AccountEditor class
    """
    account.post_name(
        get_new_user_name(get_weather(), account.get_name()))


if __name__ == '__main__':
    from src.AccountEditor import AccountEditor

    my_account = AccountEditor()
    main(my_account)
