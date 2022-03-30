import matplotlib
from pandas import DataFrame

from InputPrefs import InputPrefs
from logic.make_output_ratio import make_output_ratio
from logic.make_output_row import make_output_row
from logic.read_infected import read_infected
from logic.read_population import read_population
from type.TypeDate import TypeDate
from type.file.FilePath import FilePath
from type.Generation import generation_dict
from type.Grouping import Grouping


def __make_output(_population: dict[Grouping, DataFrame], _infected: dict[Grouping, DataFrame], pref):
    # グラフに日本語を使う設定
    matplotlib.rc('font', family='BIZ UDGothic')
    for group in Grouping:
        target_population = _population.get(group).xs(pref.name.name, level='都道府県名', axis='index')

        # FIXME 月情報のまとめてつけたいけどいったんここで
        df_temp = _infected.get(group)
        df_month = DataFrame({
            'Week': df_temp.index,
            'week_start': [TypeDate.from_str(week.split('~')[0]) for week in df_temp.index],
            'month': [TypeDate.first_of_month(week.split('~')[0]) for week in df_temp.index]
        }).set_index('Week')
        target_infected = df_temp.xs(pref.code.value, level=1, axis='columns').join(df_month)

        # 割合データで出力
        make_output_ratio(generation_dict, target_population, target_infected, pref, group)
        # 生値データで出力
        make_output_row(generation_dict, target_population, target_infected, pref, group)


if __name__ == '__main__':
    # 読み込み
    # 人口データ
    population: dict[Grouping, DataFrame] = read_population(FilePath.input('stnen'), 'UTF-8')
    # 感染者数データ
    infected: dict[Grouping, DataFrame] = read_infected(
        FilePath.input('newly_confirmed_cases_detail_weekly.csv'), 'UTF-8')

    # # 出力
    input_pref = InputPrefs.prefs[0]
    __make_output(population, infected, input_pref)
