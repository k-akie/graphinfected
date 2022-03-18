import pandas as pd
# 大阪府毎月推計人口
# 大阪府 group by 性別、5歳階級
# https://www.pref.osaka.lg.jp/toukei/jinkou/jinkou-xlslist.html
from pandas import DataFrame

from logic.make_population_osaka_fu import make_population_csv


def __joined_population(period_array: list[str], df_input: DataFrame) -> DataFrame:
    columnNamesArray = [['０～４歳', '５～９歳'],
                        ['10～14歳', '15～19歳'],
                        ['20～24歳', '25～29歳'],
                        ['30～34歳', '35～39歳'],
                        ['40～44歳', '45～49歳'],
                        ['50～54歳', '55～59歳'],
                        ['60～64歳', '65～69歳'],
                        ['70～74歳', '75～79歳'],
                        ['80～84歳', '85～89歳'],
                        ['90～94歳', '95歳以上']]

    # 元データのインデックスを日付扱いする
    df_input.index = pd.to_datetime(df_input.index.to_series())

    # 行ごとの月情報
    df_results = pd.DataFrame()
    for period, columnNames in zip(period_array, columnNamesArray):
        df_temp = pd.DataFrame(df_input, columns=columnNames).sum(axis='columns').to_frame(name=period)
        df_results = pd.concat([df_results, df_temp], axis='columns')

    return df_results


def read_population_osaka_fu(period_array: list[str], file_path: str, encode: str):
    # エクセル -> CSVにする
    make_population_csv()

    # CSVを読み込む
    csv_input = pd.read_csv(filepath_or_buffer=file_path, encoding=encode, sep=",", index_col=[0, 1])
    osaka_fu_male = csv_input.loc['男性']
    osaka_fu_female = csv_input.loc['女性']

    male = __joined_population(period_array, osaka_fu_male)
    female = __joined_population(period_array, osaka_fu_female)

    return {'male': male, 'female': female, 'all': male + female}
