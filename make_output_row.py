import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from pandas import DataFrame

from type.Term import EMERGENCY_TERM, SEMI_EMERGENCY_TERM
from type.Grouping import Grouping
from type.Prefecture import Prefecture


def _make_graph_row(df_population: DataFrame, df_infected: DataFrame
                    , prefecture: Prefecture, target: Grouping):
    # グラフ全体の設定
    plt.figure(figsize=(10.0, 8.0))  # 横、縦
    plt.plot(df_infected, label=df_infected.columns)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in EMERGENCY_TERM:  # 緊急事態宣言
        plt.axvspan(term.start, term.end, color="orange", alpha=0.3, label=term.name)
    for term in SEMI_EMERGENCY_TERM:  # まん延防止等重点措置
        plt.axvspan(term.start, term.end, color="yellow", alpha=0.3, label=term.name)

    # 左Y軸 主目盛
    plt.ylabel('感染者数')
    plt.ylim(0, 10000)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(2500))
    plt.gca().tick_params(which='major', axis='y', length=6)
    plt.grid(which='major', axis='y')
    # 左Y軸 補助目盛
    plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(500))
    plt.gca().tick_params(which='minor', axis='y', direction='in')
    plt.grid(which='minor', axis='y', linestyle='dotted')
    plt.legend(loc='upper left')

    # X軸 主目盛
    plt.xlim(datetime.date(2020, 3, 1), datetime.date(2022, 5, 1))
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().tick_params(which='major', axis='x', length=6)
    plt.grid(which='major', axis='x')
    # X軸 補助目盛
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gca().tick_params(which='minor', axis='x', direction='in')
    plt.grid(which='minor', axis='x', linestyle='dotted')

    # 右Y軸 主目盛
    ax2 = plt.twinx()
    ax2.plot(df_population, label=df_population.columns, linestyle='dashdot', linewidth=0.8)
    ax2.set_ylim(0, 1000000)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(250000))
    ax2.set_ylabel('人口')

    # 全体設定
    plt.title(f"{prefecture.name} [{target.value.name}]", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"output/row_{prefecture.key}_{target.value.key}.png")
    plt.close('all')


def make_output_row(target_columns: dict[str, str], population: dict[str, DataFrame], infected: dict[str, DataFrame]
                    , prefecture: Prefecture, target: Grouping):
    df_population = population.get(target.value.key)

    df_infected = infected.get(target.value.key)
    df_infected_graph = df_infected.reset_index()\
        .set_index('week_start')\
        .rename(columns=target_columns)[list(target_columns.values())]

    # 出力
    _make_graph_row(df_population, df_infected_graph, prefecture, target)
    df_population\
        .to_csv(f'output/row_{prefecture.key}_{target.value.key}_population.csv', line_terminator="\n")
    df_infected[list(target_columns.keys())]\
        .to_csv(f'output/row_{prefecture.key}_{target.value.key}_infected.csv', line_terminator="\n")
