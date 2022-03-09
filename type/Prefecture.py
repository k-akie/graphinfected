class Prefecture:
    """
    都道府県

    Args:
        key(str) データに指定しているキー値
        name(str) 表記に使う日本語名称
    """
    key: str
    name: str

    def __init__(self, key: str, name: str):
        self.key = key
        self.name = name

    def __str__(self):
        return self.key + ':' + self.name
