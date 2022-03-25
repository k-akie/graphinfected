import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame, Index

from type.OutputFileName import OutputFileName
from type.FilePath import FilePath
from type.Grouping import Grouping
from type.TypeDate import TypeDate
from type.prefecture.Prefecture import Prefecture
from type.term.TermType import TermType


def __search_month(target_month: datetime, exists_month: Index):
    if target_month in exists_month:
        return target_month

    # 対象月が存在するデータ範囲より前なら、もっとも古い日付のデータを使う
    start_date = exists_month[0]
    if target_month < start_date:
        return start_date

    # 対象月が存在するデータ範囲より前なら、もっとも新しい日付のデータを使う
    return exists_month[len(exists_month)-1]


def __calc_ratio(target_columns: list[str], df_population: DataFrame, df_infected: DataFrame) -> DataFrame:
    df_result = pd.DataFrame()
    for index, infectedRow in df_infected.iterrows():
        infected_series = infectedRow.loc[target_columns]

        month = __search_month(infectedRow['month'], df_population.index)
        population_series = df_population.loc[month]

        df_result[infectedRow['week_start']] = infected_series * 100 / population_series

    return df_result.T


def __make_graph_ratio(df_result: DataFrame, pref: Prefecture, target: Grouping):
    # グラフ全体の設定
    fig: Figure = plt.figure(figsize=(10.0, 8.0))  # 横、縦
    ax: Axes = fig.add_subplot(111, title=f"{pref.name.name} [{target.value.name}]")
    ax.plot(df_result, label=df_result.columns)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in pref.terms:
        # label設定した数だけ凡例にも追加されてしまうため、2回目以降はNoneにする
        lines, labels = ax.get_legend_handles_labels()
        label = None if term.type.value in labels else term.type.value

        if term.type == TermType.EMERGENCY:
            ax.axvspan(mdates.date2num(term.start), mdates.date2num(term.end)
                       , color="orange", alpha=0.3, label=label)
        if term.type == TermType.SEMI_EMERGENCY:
            ax.axvspan(mdates.date2num(term.start), mdates.date2num(term.end)
                       , color="yellow", alpha=0.3, label=label)

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
    ax.set_xlim(mdates.date2num(TypeDate.min()), mdates.date2num(TypeDate.max()))
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
    fig.savefig(FilePath.output(OutputFileName('ratio', pref, target).graph()))
    plt.close('all')


def make_output_ratio(target_columns: dict[str, str]
                      , population: dict[Grouping, DataFrame], infected: dict[Grouping, DataFrame]
                      , pref: Prefecture, target: Grouping):
    # 出力用にデータを加工
    df_result = __calc_ratio(list(target_columns.keys()), population.get(target), infected.get(target))
    outputFileName = OutputFileName('ratio', pref, target)

    # CSV出力
    df_result.to_csv(FilePath.output(outputFileName.csv()), line_terminator="\n")

    # グラフ出力
    df_result_graph = df_result.rename(columns=target_columns)
    __make_graph_ratio(df_result_graph, pref, target)
