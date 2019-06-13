from pathlib import Path

from decouple import config
from mastodon import Mastodon

from src.accounts.account import AccountEditor


def initialize_mastodon():
    server_url = config("MASTODON_SERVER")
    # make data dir
    mastodon_data_path = Path(__file__).parents[2] / "data" / "mastodon"
    # フォルダの方は Error を回避
    try:
        Path(mastodon_data_path.parent).mkdir()
        Path(mastodon_data_path).mkdir()
    except FileExistsError:
        print("you have already make mastodon data folder")
    mastodon_client_data_path = mastodon_data_path / "my_clientcred.txt"
    mastodon_user_data_path = mastodon_data_path / "my_usercred.txt"
    # If you already have data file, Raise error
    for path in (mastodon_user_data_path, mastodon_client_data_path):
        if path.exists():
            print(path.as_posix(), "is already exists")
            return False
    # get mastodon data
    Mastodon.create_app("client name", api_base_url=server_url,
                        to_file=mastodon_client_data_path.as_posix())
    mastodon = Mastodon(client_id=mastodon_client_data_path.as_posix(),
                        api_base_url=server_url)
    mastodon.log_in(config("MASTODON_EMAIL"), config("MASTODON_PASS"),
                    to_file=mastodon_user_data_path.as_posix())
    return True


class MastodonAccountEditor(AccountEditor):
    def __init__(self):
        super().__init__()
        initialize_mastodon()
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
