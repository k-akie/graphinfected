import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from type.Term import EMERGENCY_TERM, SEMI_EMERGENCY_TERM
from type.Grouping import Grouping
from type.Prefecture import Prefecture


def _make_graph_row(df_population: DataFrame, df_infected: DataFrame
                    , prefecture: Prefecture, target: Grouping):
    # グラフ全体の設定
    fig: Figure = plt.figure(figsize=(10.0, 8.0))  # 横、縦
    ax: Axes = fig.add_subplot(111, title=f"{prefecture.name} [{target.value.name}]")
    ax.plot(df_infected, label=df_infected.columns)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in EMERGENCY_TERM:  # 緊急事態宣言
        ax.axvspan(term.start, term.end, color="orange", alpha=0.3, label=term.name)
    for term in SEMI_EMERGENCY_TERM:  # まん延防止等重点措置
        ax.axvspan(term.start, term.end, color="yellow", alpha=0.3, label=term.name)

    # 凡例
    ax.legend(loc='upper left')

    # 左Y軸 主目盛
    ax.set_ylabel('感染者数')
    ax.set_ylim(0, 15000)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5000))
    ax.tick_params(which='major', axis='y', length=6)
    ax.grid(which='major', axis='y')
    # 左Y軸 補助目盛
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1000))
    ax.tick_params(which='minor', axis='y', direction='in')
    ax.grid(which='minor', axis='y', linestyle='dotted')

    # X軸 主目盛
    ax.set_xlim(datetime.date(2020, 3, 1), datetime.date(2022, 5, 1))
    ax.set_xticklabels(labels='', rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    ax.tick_params(which='major', axis='x', length=6)
    ax.grid(which='major', axis='x')
    # X軸 補助目盛
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.tick_params(which='minor', axis='x', direction='in')
    ax.grid(which='minor', axis='x', linestyle='dotted')

    # 右Y軸 主目盛
    ax2 = plt.twinx()
    ax2.plot(df_population, label=df_population.columns, linestyle='dashdot', linewidth=0.8)
    ax2.set_ylim(0, 1500000)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(500000))
    ax2.set_ylabel('人口')

    # 全体設定
    fig.tight_layout()
    fig.savefig(f"output/row_{prefecture.key}_{target.value.key}.png")
    plt.close('all')


def make_output_row(target_columns: dict[str, str], population: dict[str, DataFrame], infected: dict[str, DataFrame]
                    , prefecture: Prefecture, target: Grouping):
    df_population = population.get(target.value.key)
    df_infected = infected.get(target.value.key)

    # CSV出力
    df_population\
        .to_csv(f'output/row_{prefecture.key}_{target.value.key}_population.csv', line_terminator="\n")
    df_infected[list(target_columns.keys())]\
        .to_csv(f'output/row_{prefecture.key}_{target.value.key}_infected.csv', line_terminator="\n")

    # グラフ出力
    df_infected_graph = df_infected.reset_index()\
        .set_index('week_start')\
        .rename(columns=target_columns)[list(target_columns.values())]
    _make_graph_row(df_population, df_infected_graph, prefecture, target)
