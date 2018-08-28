# Libs
# main
import math

# local files import
from src.accounts.AccountEditor import TwitterAccountEditor, AccountEditor, \
    MastodonAccountEditor
from src.weather.yahoo import get_weather


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

    argparce によってコマンドラインの変数の取得を行う

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
        account = MastodonAccountEditor()
    elif "no_service" in args.service:
        account = AccountEditor()
    else:
        raise ValueError("You can't use this service")

    account.post_name(
        get_new_user_name(get_weather(), account.get_name()))
