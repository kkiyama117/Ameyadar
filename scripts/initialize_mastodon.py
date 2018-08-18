from pathlib import Path

from mastodon import Mastodon
from decouple import config


def initialize_mastodon():
    server_url = config("MASTODON_SERVER")
    # make data dir
    mastodon_data_path = Path(__file__).parents[1] / "data" / "mastodon"
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
            raise FileExistsError(path.as_posix(), "is already exists")

    # get mastodon data
    Mastodon.create_app("client name", api_base_url=server_url,
                        to_file=mastodon_client_data_path.as_posix())
    mastodon = Mastodon(client_id=mastodon_client_data_path.as_posix(),
                        api_base_url=server_url)
    mastodon.log_in(config("MASTODON_EMAIL"), config("MASTODON_PASS"),
                    to_file=mastodon_user_data_path.as_posix())


if __name__ == '__main__':
    initialize_mastodon()
