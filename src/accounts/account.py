class AccountEditor:
    """Account用Interface 兼 動作確認の出来るモック
    """
    def __init__(self):
        self.name = "default"

    def get_name(self):
        return self.name

    def post_name(self, name):
        self.name = name
        print(name)
        return True




