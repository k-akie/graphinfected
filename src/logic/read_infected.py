import pandas as pd

from type.Grouping import Grouping
from type.TypeDate import TypeDate


# 性別・年代別新規陽性者数（週別）
# group by 都道府県、性別、10歳階級
# https://covid19.mhlw.go.jp/extensions/public/index.html
def read_infected(file_path: str, encode: str) -> dict[Grouping, pd.DataFrame]:
    csv_input = pd.read_csv(filepath_or_buffer=file_path, encoding=encode, sep=",", header=1, index_col=0)

    # 'Male Under 10' -> ('', 'Male', 'Under 10', '', '') -> ('Male', 'Under 10', '')
    # 'Female 10s.47' -> ('', 'Female', '10s', '47', '')  -> ('Female', '10s', '47')
    csv_input.columns = csv_input.columns.str\
        .split(r'(Male|Female)\s(.*[0s])\.?([0-9]*)', expand=True)\
        .droplevel([0, 4])

    # *を0にしてobject -> intにする
    csv_input = csv_input.replace(to_replace='*', regex=False, value=0).fillna(0).astype(int)

    male: pd.DataFrame = csv_input.xs('Male', level=0, axis='columns')
    female: pd.DataFrame = csv_input.xs('Female', level=0, axis='columns')

    # FIXME mainでの処理とダブってる
    # 行ごとの月情報
    df_month = pd.DataFrame({
        'Week': csv_input.index,
        'week_start.': [TypeDate.from_str(week.split('~')[0]) for week in csv_input.index],
        'month.': [TypeDate.first_of_month(week.split('~')[0]) for week in csv_input.index]
    }).set_index('Week')
    df_month.columns = df_month.columns.str.split('.', n=1, expand=True)

    result_male: pd.DataFrame = male.join(df_month)
    result_female: pd.DataFrame = female.join(df_month)
    result_all: pd.DataFrame = (male + female).join(df_month)

    return {Grouping.MALE: result_male, Grouping.FEMALE: result_female, Grouping.ALL: result_all}
