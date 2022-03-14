from datetime import datetime as dt

import pandas as pd


# 性別・年代別新規陽性者数（週別）
# group by 都道府県、性別、10歳階級
# https://covid19.mhlw.go.jp/extensions/public/index.html


def read_infected(file_path: str, encode: str):
    # 27 大阪府
    csv_input = pd.read_csv(filepath_or_buffer=file_path, encoding=encode, sep=",", header=1, index_col=0)
    osaka_fu = csv_input.filter(like='.27', axis='columns')

    # *を0にしてobject -> intにする
    osaka_fu = osaka_fu.replace(['*'], 0).astype(int)

    # 行ごとの月情報
    df_month = pd.DataFrame({
        'week_start': [dt.strptime(week.split('~')[0], '%Y/%m/%d') for week in osaka_fu.index],
        'month': [dt.strptime(week.split('~')[0], '%Y/%m/%d').replace(day=1) for week in osaka_fu.index]
    })

    # https://note.nkmk.me/python-pandas-dataframe-rename/
    male = osaka_fu.filter(like='Male ') \
        .rename(columns=lambda s: s.removeprefix('Male ')) \
        .rename(columns=lambda s: s.removesuffix('.27')) \
        # .reset_index().join([df_month]).set_index('Week')

    female = osaka_fu.filter(like='Female ') \
        .rename(columns=lambda s: s.removeprefix('Female ')) \
        .rename(columns=lambda s: s.removesuffix('.27')) \
        # .reset_index().join([df_month]).set_index('Week')

    result_all = (male + female).reset_index().join([df_month]).set_index('Week')
    result_male = male.reset_index().join([df_month]).set_index('Week')
    result_female = female.reset_index().join([df_month]).set_index('Week')

    return {'male': result_male, 'female': result_female, 'all': result_all}
