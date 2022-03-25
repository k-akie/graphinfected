from type.Grouping import Grouping
from type.prefecture.Prefecture import Prefecture


class OutputFileName:
    type: str
    pref: Prefecture
    group: Grouping

    def __init__(self, _type: str, _pref: Prefecture, _group: Grouping):
        self.type = _type
        self.pref = _pref
        self.group = _group

    def __str__(self):
        return f'{self.pref.key()}/{self.type}_{self.pref.name.key}_{self.group.value.key}'

    def csv(self, suffix: str = ''):
        if suffix:
            return f'{self}_{suffix}.csv'
        return f'{self}.csv'

    def graph(self):
        return f'{self}.png'
