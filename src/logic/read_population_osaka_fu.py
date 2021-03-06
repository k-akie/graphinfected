import pandas as pd
from pandas import DataFrame

from logic.make_population_osaka_fu import make_population_csv
from type.Grouping import Grouping


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


def read_population_osaka_fu(period_array: list[str], input_dir: str) -> dict[Grouping, DataFrame]:
    encode = 'UTF-8'
    temp_file_path = input_dir + '.csv'

    # エクセル -> CSVにする
    make_population_csv(input_dir, temp_file_path, encode)

    # CSVを読み込む
    csv_input = pd.read_csv(filepath_or_buffer=temp_file_path, encoding=encode, sep=",", index_col=[0, 1])
    osaka_fu_male = csv_input.loc['男性']
    osaka_fu_female = csv_input.loc['女性']

    male = __joined_population(period_array, osaka_fu_male)
    female = __joined_population(period_array, osaka_fu_female)

    return {Grouping.MALE: male, Grouping.FEMALE: female, Grouping.ALL: male + female}
