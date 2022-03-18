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
    repeater = re.compile('[0-9]{6}')

    result = {}
    files = glob.glob(dir_path + '/*.xlsx')
    for file in files:
        target = repeater.search(file).group(0) + '01'
        target_datetime = TypeDate.from_str(target, '%Y%m%d')
        result[target_datetime] = file

    return result


if __name__ == '__main__':
    # https://www.pref.osaka.lg.jp/toukei/jinkou/jinkou-xlslist.html
    # ひと月ごとにエクセルファイルがある
    file_map = __search_file_list(FilePath.input('jinkou-xlslist'))

    df_data = pd.DataFrame()
    for key in sorted(file_map.keys()):
        df_data = pd.concat([df_data, __read_file(key, file_map[key])])
    df_data.sort_values('month', inplace=True)

    df_data.to_csv(FilePath.input('jinkou-xlslist.csv'), line_terminator="\n")
