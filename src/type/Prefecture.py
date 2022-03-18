class Prefecture:
    """
    都道府県

    Args:
        key     データに指定しているキー値
        name    表記に使う日本語名称
        code    都道府県コード(2桁の数字)
    """
    key: str
    name: str
    code: str

    def __init__(self, key: str, name: str, code: str):
        self.key = key
        self.name = name
        self.code = code

    def __str__(self):
        return self.key + ':' + self.name + '(code: ' + self.code + ')'
