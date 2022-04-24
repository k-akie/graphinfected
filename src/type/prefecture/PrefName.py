class PrefName:
    """
    都道府県の名称

    Args:
        key     データに指定しているキー値
        name    表示に使う日本語名称(都道府県まで含めること)
    """
    key: str
    name: str

    def __init__(self, key: str, name: str):
        self.key = key
        self.name = name

    def __str__(self):
        return self.key + ':' + self.name
