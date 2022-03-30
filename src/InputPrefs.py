# 大阪府
from type.prefecture.PrefCode import PrefCode
from type.prefecture.PrefName import PrefName
from type.prefecture.Prefecture import Prefecture
from type.term.Term import Term
from type.term.TermType import TermType


# 緊急事態宣言等の履歴
# https://www.kwm.co.jp/blog/state-of-emergency/
class InputPrefs:
    prefs: [Prefecture] = [
        # 大阪府
        Prefecture(
            PrefName('osaka', '大阪府'),
            PrefCode('27'),
            [
                Term('2020-04-07', '2020-05-21', TermType.EMERGENCY, 1),
                Term('2021-01-14', '2021-02-28', TermType.EMERGENCY, 2),
                Term('2021-04-05', '2021-04-24', TermType.SEMI_EMERGENCY, 1),
                Term('2021-04-25', '2021-06-20', TermType.EMERGENCY, 3),
                Term('2021-06-21', '2021-08-01', TermType.SEMI_EMERGENCY, 2),
                Term('2021-08-02', '2021-09-30', TermType.EMERGENCY, 4),
                Term('2022-01-27', '2022-03-21', TermType.SEMI_EMERGENCY, 3),
            ]
        ),
        # 東京都
        Prefecture(
            PrefName('tokyo', '東京都'),
            PrefCode('13'),
            [
                Term('2020-04-07', '2020-05-25', TermType.EMERGENCY, 1),
                Term('2021-01-08', '2021-03-21', TermType.EMERGENCY, 2),
                Term('2021-04-12', '2021-04-24', TermType.SEMI_EMERGENCY, 1),
                Term('2021-04-25', '2021-06-20', TermType.EMERGENCY, 3),
                Term('2021-06-21', '2021-07-11', TermType.SEMI_EMERGENCY, 2),
                Term('2021-07-12', '2021-09-30', TermType.EMERGENCY, 4),
                Term('2022-01-21', '2022-03-21', TermType.SEMI_EMERGENCY, 3),
            ]
        )
    ]
