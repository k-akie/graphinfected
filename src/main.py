import matplotlib
from pandas import DataFrame

from InputPrefs import InputPrefs
from logic.make_output_ratio import make_output_ratio
from logic.make_output_row import make_output_row
from logic.read_infected import read_infected
from logic.read_population import read_population
from type.file.FilePath import FilePath
from type.Generation import generation_dict
from type.Grouping import Grouping


def __make_output(_population: dict[Grouping, DataFrame], _infected: dict[Grouping, DataFrame], pref):
    # グラフに日本語を使う設定
    matplotlib.rc('font', family='BIZ UDGothic')
    for group in Grouping:
        # 割合データで出力
        make_output_ratio(generation_dict, _population, _infected, pref, group)
        # 生値データで出力
        make_output_row(generation_dict, _population, _infected, pref, group)


if __name__ == '__main__':
    input_pref = InputPrefs.prefs[0]

    # 人口データ
    population: dict[Grouping, DataFrame] = read_population(FilePath.input('stnen'), 'UTF-8', input_pref)

    # 感染者数データ
    infected: dict[Grouping, DataFrame] = read_infected(
        FilePath.input('newly_confirmed_cases_detail_weekly.csv'), 'UTF-8', input_pref.code)

    # 出力
    __make_output(population, infected, input_pref)
