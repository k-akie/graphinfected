import datetime
import glob
import re

import pandas as pd
from pandas import DataFrame

from type.file.FilePath import FilePath
from type.TypeDate import TypeDate


def __read_file(month: datetime, file_path: str, _period_array: list[str]) -> DataFrame:
    filter_index = ['0～4', '5～9', '10～14', '15～19', '20～24', '25～29', '30～34', '35～39', '40～44',
                    '45～49', '50～54', '55～59', '60～64', '65～69', '70～74', '75～79', '80～84', '85～89', '90～94',
                    '95～99', '100以上']

    # 2行目をヘッダーとして使う、0から数えるので1引く
    df_input = pd.read_excel(file_path, index_col=[0, 1, 2], header=(2 - 1)) \
        .filter(regex='[0-9]{5,6}', axis=0) \
        .rename(columns=lambda s: s.replace('歳', '')) \
        .rename_axis(['団体コード', '都道府県名', '性別']) \
        .reset_index(['団体コード']) \
        .rename(index=lambda s: s.replace(r'*', '')) \
        .filter(filter_index)

    # 5歳階級を10歳階級にする
    columnNamesArray = [['0～4', '5～9'],
                        ['10～14', '15～19'],
                        ['20～24', '25～29'],
                        ['30～34', '35～39'],
                        ['40～44', '45～49'],
                        ['50～54', '55～59'],
                        ['60～64', '65～69'],
                        ['70～74', '75～79'],
                        ['80～84', '85～89'],
                        ['90～94', '95～99', '100以上']]
    df_results = pd.DataFrame()
    for period, columnNames in zip(_period_array, columnNamesArray):
        df_temp = pd.DataFrame(df_input, columns=columnNames).sum(axis='columns').to_frame(name=period)
        df_results = pd.concat([df_results, df_temp], axis='columns')

    df_results.insert(0, 'month', month)
    return df_results


def __search_file_list(dir_path: str) -> dict[datetime, str]:
    result = {}
    files = glob.glob(dir_path + '/*02stnen.*')
    repeater = re.compile('[0-9]{2}')  # ファイル名の先頭2桁(西暦の下2桁)を取得
    for file in files:
        target = '20' + repeater.search(file).group(0) + '0101'  # 年月日20yy0101の形式にする
        target_datetime = TypeDate.from_str(target, '%Y%m%d')
        result[target_datetime] = file

    return result


def make_population_all_pref_csv(input_dir: str, temp_file_path: str, encode: str, _period_array: list[str]):
    if FilePath.exists(temp_file_path):
        # 出力先ファイルがあれば、再生成しない
        return

    file_map = __search_file_list(input_dir)
    df_data = pd.DataFrame()
    for key in sorted(file_map.keys()):
        df_data = pd.concat([df_data, __read_file(key, file_map[key], _period_array)])

    df_data.to_csv(temp_file_path, line_terminator="\n", encoding=encode)
