from enum import Enum


class GroupingUnit:
    """
    集約単位

    Args:
        key     データに指定しているキー値
        name    表記に使う日本語名称
    """
    key: str
    name: str

    def __init__(self, key: str, name: str):
        self.key = key
        self.name = name

    def __str__(self):
        return self.key + ':' + self.name


class Grouping(Enum):
    """
    出力の集約単位
    """
    ALL = GroupingUnit('all', '全体')
    MALE = GroupingUnit('male', '男性')
    FEMALE = GroupingUnit('female', '女性')
