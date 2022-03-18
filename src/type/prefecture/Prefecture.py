from type.prefecture.PrefCode import PrefCode
from type.prefecture.PrefName import PrefName


class Prefecture:
    """
    都道府県

    Args:
        key     データに指定しているキー値
        name    表記に使う日本語名称
        code    都道府県コード(2桁の数字)
    """
    name: PrefName
    code: PrefCode

    def __init__(self, name: PrefName, code: PrefCode):
        self.name = name
        self.code = code

    def __str__(self):
        return self.name + ', ' + self.code
