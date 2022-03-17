import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame, Index

from type.Grouping import Grouping
from type.Prefecture import Prefecture
from type.Term import EMERGENCY_TERM, SEMI_EMERGENCY_TERM
from type.TypeDate import TypeDate


def _search_month(target_month: datetime, exists_month: Index):
    if target_month in exists_month:
        return target_month

    # 対象月が存在するデータ範囲より前なら、もっとも古い日付のデータを使う
    start_date = exists_month[0]
    if target_month < start_date:
        return start_date

    # 対象月が存在するデータ範囲より前なら、もっとも新しい日付のデータを使う
    return exists_month[len(exists_month)-1]


def _calc_ratio(target_columns: list[str], df_population: DataFrame, df_infected: DataFrame) -> DataFrame:
    df_result = pd.DataFrame()
    for index, infectedRow in df_infected.iterrows():
        infected_series = infectedRow.loc[target_columns]

        month = _search_month(infectedRow['month'], df_population.index)
        population_series = df_population.loc[month]

        df_result[infectedRow['week_start']] = infected_series * 100 / population_series

    return df_result.T


def _make_graph_ratio(df_result: DataFrame, prefecture: Prefecture, target: Grouping):
    # グラフ全体の設定
    fig: Figure = plt.figure(figsize=(10.0, 8.0))  # 横、縦
    ax: Axes = fig.add_subplot(111, title=f"{prefecture.name} [{target.value.name}]")
    ax.plot(df_result, label=df_result.columns)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in EMERGENCY_TERM:  # 緊急事態宣言
        ax.axvspan(term.start, term.end, color="orange", alpha=0.3, label=term.name)
    for term in SEMI_EMERGENCY_TERM:  # まん延防止等重点措置
        ax.axvspan(term.start, term.end, color="yellow", alpha=0.3, label=term.name)

    # 凡例
    ax.legend(loc='upper left')

    # Y軸 主目盛
    ax.set_ylabel('人口当たり感染者割合(%)')
    ax.set_ylim(0, 2)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.tick_params(which='major', axis='y', length=6)
    ax.grid(which='major', axis='y')
    # Y軸 補助目盛
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax.tick_params(which='minor', axis='y', direction='in')
    ax.grid(which='minor', axis='y', linestyle='dotted')

    # X軸 主目盛
    ax.set_xlim(TypeDate.min(), TypeDate.max())
    ax.set_xticklabels(labels='', rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(TypeDate.format()))
    ax.tick_params(which='major', axis='x', length=6)
    ax.grid(which='major', axis='x')
    # X軸 補助目盛
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.tick_params(which='minor', axis='x', direction='in')
    ax.grid(which='minor', axis='x', linestyle='dotted')

    # 全体設定
    fig.tight_layout()
    fig.savefig(f"output/ratio_{prefecture.key}_{target.value.key}.png")
    plt.close('all')


def make_output_ratio(target_columns: dict[str, str], population: dict[str, DataFrame], infected: dict[str, DataFrame]
                      , prefecture: Prefecture, target: Grouping):
    # 出力用にデータを加工
    df_result = _calc_ratio(list(target_columns.keys()), population.get(target.value.key), infected.get(target.value.key))

    # CSV出力
    df_result.to_csv(f'output/ratio_{prefecture.key}_{target.value.key}.csv', line_terminator="\n")

    # グラフ出力
    df_result_graph = df_result.rename(columns=target_columns)
    _make_graph_ratio(df_result_graph, prefecture, target)
