# divide config
import json

from decouple import config
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
