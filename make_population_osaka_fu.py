import pandas as pd
import glob
import re
import datetime


def _read_file(month, file_path):
    # 3行目をヘッダーとして使う、0から数えるので1引く
    df_input = pd.read_excel(file_path, index_col=0, header=(3 - 1)) \
        .loc['大阪府'] \
        .set_axis(['全体', '男性', '女性'], axis='index') \
        .loc[['男性', '女性']]
    df_input.insert(0, 'month', month)
    df_input.index.name = 'gender'

    return df_input


def _search_file_list(dir_path):
    repeater = re.compile('[0-9]{6}')

    result = {}
    files = glob.glob(dir_path + '/*')
    for file in files:
        target = repeater.search(file).group(0) + '01'
        target_datetime = datetime.datetime.strptime(target, '%Y%m%d')
        year_str = target_datetime.strftime('%Y')
        month_str = target_datetime.strftime('%m').lstrip("0")
        day_str = target_datetime.strftime('%d').lstrip("0")
        result[(year_str + '/' + month_str + '/' + day_str)] = file

    return result


if __name__ == '__main__':
    # https://www.pref.osaka.lg.jp/toukei/jinkou/jinkou-xlslist.html
    # ひと月ごとにエクセルファイルがある
    file_map = _search_file_list('input/jinkou-xlslist')

    df_data = pd.DataFrame()
    for key in sorted(file_map.keys()):
        df_data = pd.concat([df_data, _read_file(key, file_map[key])])

    df_data.to_csv('input/jinkou-xlslist.csv')
