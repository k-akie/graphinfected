from type.prefecture.PrefCode import PrefCode
from type.prefecture.PrefName import PrefName
from type.prefecture.Prefecture import Prefecture
from type.term.Term import Term
from type.term.TermType import TermType


# 都道府県コード
# https://ja.wikipedia.org/wiki/%E5%85%A8%E5%9B%BD%E5%9C%B0%E6%96%B9%E5%85%AC%E5%85%B1%E5%9B%A3%E4%BD%93%E3%82%B3%E3%83%BC%E3%83%89#%E9%83%BD%E9%81%93%E5%BA%9C%E7%9C%8C%E3%82%B3%E3%83%BC%E3%83%89
# 緊急事態宣言等の履歴
# https://www.kwm.co.jp/blog/state-of-emergency/
class InputPrefs:
    prefs: [Prefecture] = [
        Prefecture(
            PrefName('osaka', '大阪府'),
            PrefCode('27'),
            [
                Term('2020-04-07', '2020-05-21', TermType.EMERGENCY),
                Term('2021-01-14', '2021-02-28', TermType.EMERGENCY),
                Term('2021-04-05', '2021-04-24', TermType.SEMI_EMERGENCY),
                Term('2021-04-25', '2021-06-20', TermType.EMERGENCY),
                Term('2021-06-21', '2021-08-01', TermType.SEMI_EMERGENCY),
                Term('2021-08-02', '2021-09-30', TermType.EMERGENCY),
                Term('2022-01-27', '2022-03-21', TermType.SEMI_EMERGENCY),
            ]
        ),
        Prefecture(
            PrefName('tokyo', '東京都'),
            PrefCode('13'),
            [
                Term('2020-04-07', '2020-05-25', TermType.EMERGENCY),
                Term('2021-01-08', '2021-03-21', TermType.EMERGENCY),
                Term('2021-04-12', '2021-04-24', TermType.SEMI_EMERGENCY),
                Term('2021-04-25', '2021-06-20', TermType.EMERGENCY),
                Term('2021-06-21', '2021-07-11', TermType.SEMI_EMERGENCY),
                Term('2021-07-12', '2021-09-30', TermType.EMERGENCY),
                Term('2022-01-21', '2022-03-21', TermType.SEMI_EMERGENCY),
            ]
        ),
        Prefecture(
            PrefName('hyogo', '兵庫県'),
            PrefCode('28'),
            [
                Term('2020-04-07', '2020-05-21', TermType.EMERGENCY),
                Term('2021-01-14', '2021-02-28', TermType.EMERGENCY),
                Term('2021-04-05', '2021-04-24', TermType.SEMI_EMERGENCY),
                Term('2021-04-25', '2021-06-20', TermType.EMERGENCY),
                Term('2021-06-21', '2021-07-11', TermType.SEMI_EMERGENCY),
                Term('2021-08-02', '2021-08-19', TermType.SEMI_EMERGENCY),
                Term('2021-08-20', '2021-09-30', TermType.EMERGENCY),
                Term('2022-01-27', '2022-03-21', TermType.SEMI_EMERGENCY),
            ]
        )
    ]
