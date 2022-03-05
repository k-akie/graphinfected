import pandas as pd
import matplotlib.pyplot as plt
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

        df_result[infectedRow['week']] = infected_series * 100 / population_series

    return df_result.T


# 緊急事態宣言等の履歴
# https://www.kwm.co.jp/blog/state-of-emergency/
emergency_term = [
    {'2020/4/7~2020/5/21', '緊急事態宣言'},  # 1回目
    {'2021/1/14~2021/2/28', '緊急事態宣言'},  # 2回目
    {'2021/4/25~2021/6/20', '緊急事態宣言'},  # 3回目、2回目のまん防に変わった
    {'2021/8/2~2021/9/30', '緊急事態宣言'},  # 4回目
    {'2021/4/5~2021/4/24', 'まん延防止等重点措置'},  # 1回目、3回目の緊急事態宣言に変わった
    {'2021/6/21~2021/8/1', 'まん延防止等重点措置'},  # 2回目、4回目の緊急事態宣言に変わった
    {'2022/1/27~2022/3/21', 'まん延防止等重点措置'},  # 3回目、延長中
]


def make_graph(df_result, prefectures, gender):
    # グラフ全体の設定
    plt.figure(figsize=(15.0, 8.0))  # 横、縦
    plt.plot(df_result)
    plt.legend(df_result.columns)
    plt.title(f"{prefectures} [{gender}]", fontsize=14)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    # 後ろは次の期間を指定する
    # 緊急事態宣言
    plt.axvspan('2021/1/6~2021/1/12', '2021/2/17~2021/2/23', color="orange", alpha=0.3)
    plt.axvspan('2021/4/21~2021/4/27', '2021/6/23~2021/6/29', color="orange", alpha=0.3)
    plt.axvspan('2021/8/4~2021/8/10', '2021/10/6~2021/10/12', color="orange", alpha=0.3)
    # まん防
    plt.axvspan('2021/4/7~2021/4/13', '2021/4/21~2021/4/27', color="yellow", alpha=0.3)
    plt.axvspan('2021/6/23~2021/6/29', '2021/8/4~2021/8/10', color="yellow", alpha=0.3)
    plt.axvspan('2022/1/26~2022/2/1', '2022/2/23~2022/3/1', color="yellow", alpha=0.3)

    # Y軸
    plt.ylabel('infected persons per population(%)')
    plt.ylim(0, 2)
    plt.grid(which='major', axis='y')

    # X軸
    plt.xlabel('week')
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.savefig(f"output/{prefectures}_{gender}.png")
    plt.close('all')
