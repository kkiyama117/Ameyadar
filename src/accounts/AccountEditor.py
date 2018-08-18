# divide config
import json
from pathlib import Path

from decouple import config
from mastodon import Mastodon
from requests_oauthlib import OAuth1Session


class AccountEditor:
    def __init__(self):
        self.name = "default"

    def get_name(self):
        return self.name

    def post_name(self, name):
        self.name = name
        print(name)
        return True


class TwitterAccountEditor(AccountEditor):
    def __init__(self):
        super().__init__()
        self.account = OAuth1Session(config("CONSUMER_KEY"),
                                     config("CONSUMER_SECRET"),
                                     config("ACCESS_TOKEN"),
                                     config("ACCESS_TOKEN_SECRET"))
        get_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        self.name = json.loads(self.account.get(get_url).text)['name']

    def post_name(self, name):
        super().post_name(name)
        post_url = 'https://api.twitter.com/1.1/account/' \
                   'update_profile.json?name=%s' % name
        try:
            self.account.post(post_url)
        except Exception:
            raise Exception
        return True


class MastodonAccountEditor(AccountEditor):
    def __init__(self):
        super().__init__()
        self.server_url = config("MASTODON_SERVER")
        mastodon_data_path = Path(__file__).parents[
                                 2] / "data" / "mastodon"
        self.mastodon = Mastodon(
            client_id=(mastodon_data_path / "my_clientcred.txt").as_posix(),
            access_token=(mastodon_data_path / "my_usercred.txt").as_posix(),
            api_base_url=self.server_url
        )
        self.name = self.mastodon.account_verify_credentials()['username']

    def post_name(self, name):
        super().post_name(name)
        self.mastodon.account_update_credentials(display_name=name)

