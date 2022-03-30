from type.file.FilePath import FilePath
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
        return f'type={self.type}, pref={self.pref}, group={self.group}'

    def __file_suffix(self) -> str:
        return f'{self.pref.key()}/{self.type}_{self.pref.name.key}_{self.group.value.key}'

    def csv(self, suffix: str = '') -> str:
        if suffix:
            return FilePath.output(f'{self.__file_suffix()}_{suffix}.csv')
        return FilePath.output(f'{self.__file_suffix()}.csv')

    def graph(self) -> str:
        return FilePath.output(f'{self.__file_suffix()}.png')
