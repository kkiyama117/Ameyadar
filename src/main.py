# Libs
# main
import json
import math
import urllib.request

# divide config
from decouple import config
from scipy.stats import norm

from src.accounts.AccountEditor import TwitterAccountEditor, AccountEditor, \
    MastodonAccountEditor


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


def main():
    """ メインの関数

    :usage: `main()` - defaultのアカウント(Twitter)が呼ばれる.
            `main(account)` - AccountEditorに対応するアカウントが呼ばれる.
                              AccountEditorそのものの場合標準出力のみ行う
    :param account: AccountEditor class
    """
    import argparse
    parser = argparse.ArgumentParser(
        description='Change username with weather change')
    parser.add_argument("service", nargs='?',
                        help="default: twitter. "
                             "You can use 'twitter', 'no_service, 'mastodon'.",
                        default="twitter")
    args = parser.parse_args()
    if "twitter" in args.service:
        account = TwitterAccountEditor()
    elif "mastodon" in args.service:
        # my_account = AccountEditor()
        account = MastodonAccountEditor()
    elif "no_service" in args.service:
        account = AccountEditor()
    else:
        raise ValueError("You can't use this service")

    account.post_name(
        get_new_user_name(get_weather(), account.get_name()))
