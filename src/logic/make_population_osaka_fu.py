import datetime
import glob
import re

import pandas as pd
from pandas import DataFrame

from type.FilePath import FilePath
from type.TypeDate import TypeDate


def __read_file(month: datetime, file_path: str) -> DataFrame:
    # 3行目をヘッダーとして使う、0から数えるので1引く
    df_input = pd.read_excel(file_path, index_col=0, header=(3 - 1)) \
        .loc['大阪府'] \
        .set_axis(['全体', '男性', '女性'], axis='index') \
        .loc[['男性', '女性']]
    df_input.insert(0, 'month', month)
    df_input.index.type = 'gender'

    return df_input


def __search_file_list(dir_path: str) -> dict[datetime, str]:
    result = {}
    files = glob.glob(dir_path + '/*.xlsx')
    repeater = re.compile('[0-9]{6}')  # ファイル名の年月yyyymm部分を抽出
    for file in files:
        target = repeater.search(file).group(0) + '01'  # 年月日yyyymm01の形式にする
        target_datetime = TypeDate.from_str(target, '%Y%m%d')
        result[target_datetime] = file

    return result


def make_population_csv(input_dir: str, temp_file_path: str, encode: str):
    # https://www.pref.osaka.lg.jp/toukei/jinkou/jinkou-xlslist.html
    # ひと月ごとにエクセルファイルがある
    # group by 性別、5歳階級

    if FilePath.exists(temp_file_path):
        # 出力先ファイルがあれば、再生成しない
        return

    file_map = __search_file_list(input_dir)
    df_data = pd.DataFrame()
    for key in sorted(file_map.keys()):
        df_data = pd.concat([df_data, __read_file(key, file_map[key])])

    df_data.sort_values('month', inplace=True)
    df_data.to_csv(temp_file_path, line_terminator="\n", encoding=encode)
