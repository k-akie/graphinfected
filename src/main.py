import matplotlib

from logic.make_output_ratio import make_output_ratio
from logic.make_output_row import make_output_row
from logic.read_infected import read_infected
from logic.read_population_osaka_fu import read_population_osaka_fu
from type.file.FilePath import FilePath
from type.Generation import generation_dict
from type.Grouping import Grouping
from type.prefecture.PrefCode import PrefCode
from type.prefecture.PrefName import PrefName
from type.prefecture.Prefecture import Prefecture
from type.term.Term import Term
from type.term.TermType import TermType


def __make_output(_population, pref):
    # 感染者数データ
    infected = read_infected(FilePath.input('newly_confirmed_cases_detail_weekly.csv'), 'UTF-8', pref.code)

    # グラフに日本語を使う設定
    matplotlib.rc('font', family='BIZ UDGothic')
    for group in Grouping:
        # 割合データで出力
        make_output_ratio(generation_dict, _population, infected, pref, group)
        # 生値データで出力
        make_output_row(generation_dict, _population, infected, pref, group)


if __name__ == '__main__':
    # 都道府県設定
    # 大阪府
    osaka = Prefecture(
        PrefName('osaka', '大阪'),
        PrefCode('27'),
        # 緊急事態宣言等の履歴
        # https://www.kwm.co.jp/blog/state-of-emergency/
        [
            Term('2020-04-07', '2020-05-21', TermType.EMERGENCY, 1),
            Term('2021-01-14', '2021-02-28', TermType.EMERGENCY, 2),
            Term('2021-04-05', '2021-04-24', TermType.SEMI_EMERGENCY, 1),
            Term('2021-04-25', '2021-06-20', TermType.EMERGENCY, 3),
            Term('2021-06-21', '2021-08-01', TermType.SEMI_EMERGENCY, 2),
            Term('2021-08-02', '2021-09-30', TermType.EMERGENCY, 4),
            Term('2022-01-27', '2022-03-21', TermType.SEMI_EMERGENCY, 3),
        ]
    )
    # 人口データ(大阪府)
    population = read_population_osaka_fu(list(generation_dict.keys()), FilePath.input(osaka.key() + '/jinkou-xlslist'))

    # 出力
    __make_output(population, osaka)
