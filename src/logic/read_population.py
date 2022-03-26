import pandas as pd
from pandas import DataFrame

from logic.make_population_csv import make_population_all_pref_csv
from type.Generation import generation_dict
from type.Grouping import Grouping
from type.prefecture.Prefecture import Prefecture


# 【総計】都道府県別年齢階級別人口
# group by 都道府県、性別、10歳階級
# https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200241&tstat=000001039591&cycle=7&tclass1=000001039601&tclass2val=0
def read_population(input_dir: str, encode: str, pref: Prefecture) -> dict[Grouping, DataFrame]:
    temp_file_path = input_dir + '.csv'

    # エクセル -> CSVにする
    period_array: list[str] = list(generation_dict.keys())
    make_population_all_pref_csv(input_dir, temp_file_path, encode, period_array)

    # CSVを読み込む
    csv_input = pd.read_csv(filepath_or_buffer=temp_file_path, encoding=encode, sep=",", index_col=[2])
    # 元データのインデックスを日付扱いする
    csv_input.index = pd.to_datetime(csv_input.index.to_series())

    csv_pref = csv_input.reset_index().set_index(['都道府県名', '性別', 'month']).loc[pref.name.name]
    csv_all = csv_pref.loc['計']
    csv_male = csv_pref.loc['男']
    csv_female = csv_pref.loc['女']

    return {Grouping.MALE: csv_male, Grouping.FEMALE: csv_female, Grouping.ALL: csv_all}
