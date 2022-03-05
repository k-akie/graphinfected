import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import datetime as dt


def _search_month(target_month, exists_month):
    if target_month in exists_month:
        return target_month

    # 対象月が存在するデータ範囲より前なら、もっとも古い日付のデータを使う
    date_format = '%Y/%m/%d'
    target_date = dt.strptime(target_month, date_format)
    start_date = dt.strptime(exists_month[0], date_format)
    if target_date < start_date:
        return exists_month[0]

    # 対象月が存在するデータ範囲より前なら、もっとも新しい日付のデータを使う
    return exists_month[len(exists_month)-1]


def data_merge(target_columns, df_population, df_infected):
    df_result = pd.DataFrame()
    for index, infectedRow in df_infected.iterrows():
        infected_series = infectedRow.loc[target_columns]

        month = _search_month(infectedRow['month'], df_population.index)
        population_series = df_population.loc[month]

        df_result[infectedRow['week_start']] = infected_series * 100 / population_series

    return df_result.T


# 緊急事態宣言等の履歴
# https://www.kwm.co.jp/blog/state-of-emergency/
emergency_term = [  # 緊急事態宣言
    [dt.fromisoformat('2020-04-07'), dt.fromisoformat('2020-05-21')],  # 1回目
    [dt.fromisoformat('2021-01-14'), dt.fromisoformat('2021-02-28')],  # 2回目
    [dt.fromisoformat('2021-04-25'), dt.fromisoformat('2021-06-20')],  # 3回目、2回目のまん防に変わった
    [dt.fromisoformat('2021-08-02'), dt.fromisoformat('2021-09-30')],  # 4回目
]
semi_emergency_term = [  # まん延防止等重点措置
    [dt.fromisoformat('2021-04-05'), dt.fromisoformat('2021-04-24')],  # 1回目、3回目の緊急事態宣言に変わった
    [dt.fromisoformat('2021-06-21'), dt.fromisoformat('2021-08-01')],  # 2回目、4回目の緊急事態宣言に変わった
    [dt.fromisoformat('2022-01-27'), dt.fromisoformat('2022-03-21')],  # 3回目、延長中
]


def make_graph(df_result, prefectures, gender):
    # グラフ全体の設定
    plt.figure(figsize=(10.0, 8.0))  # 横、縦
    plt.plot(df_result)
    plt.legend(df_result.columns, loc='upper left')
    plt.title(f"{prefectures} [{gender}]", fontsize=14)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in emergency_term:  # 緊急事態宣言
        plt.axvspan(term[0], term[1], color="orange", alpha=0.3)
    for term in semi_emergency_term:  # まん延防止等重点措置
        plt.axvspan(term[0], term[1], color="yellow", alpha=0.3)

    # Y軸 主目盛
    plt.ylabel('infected persons per population(%)')
    plt.ylim(0, 2)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.gca().tick_params(which='major', axis='y', length=6)
    plt.grid(which='major', axis='y')
    # Y軸 補助目盛
    plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    plt.gca().tick_params(which='minor', axis='y', direction='in')
    plt.grid(which='minor', axis='y', linestyle='dotted')

    # X軸 主目盛
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().tick_params(which='major', axis='x', length=6)
    plt.grid(which='major', axis='x')
    # X軸 補助目盛
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gca().tick_params(which='minor', axis='x', direction='in')
    plt.grid(which='minor', axis='x', linestyle='dotted')

    plt.tight_layout()
    plt.savefig(f"output/{prefectures}_{gender}.png")
    plt.close('all')
