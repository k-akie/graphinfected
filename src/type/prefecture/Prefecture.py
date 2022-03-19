from type.prefecture.PrefCode import PrefCode
from type.prefecture.PrefName import PrefName
from type.term.Term import Term


class Prefecture:
    """
    都道府県に依存した情報

    Args:
        name    名称
        code    都道府県コード
        terms   その都道府県の緊急事態宣言などの期間
    """
    name: PrefName
    code: PrefCode
    terms: list[Term]

    def __init__(self, _name: PrefName, _code: PrefCode, _terms: list[Term]):
        self.name = _name
        self.code = _code
        self.terms = _terms

    def __str__(self):
        return self.name + ', ' + self.code + ', terms: ' + len(self.terms)

    def key(self) -> str:
        return self.code.value + '_' + self.name.key
