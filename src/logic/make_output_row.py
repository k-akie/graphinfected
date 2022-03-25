import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from type.OutputFileName import OutputFileName
from type.FilePath import FilePath
from type.Grouping import Grouping
from type.TypeDate import TypeDate
from type.prefecture.Prefecture import Prefecture
from type.term.TermType import TermType


def __make_graph_row(df_population: DataFrame, df_infected: DataFrame
                     , pref: Prefecture, target: Grouping):
    # グラフ全体の設定
    fig: Figure = plt.figure(figsize=(10.0, 8.0))  # 横、縦
    ax: Axes = fig.add_subplot(111, title=f"{pref.name.name} [{target.value.name}]")
    ax.plot(df_infected, label=df_infected.columns)

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
    ax.set_xlim(mdates.date2num(TypeDate.min()), mdates.date2num(TypeDate.max()))
    ax.set_xticklabels(labels='', rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(TypeDate.format()))
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
    fig.savefig(FilePath.output(OutputFileName('row', pref, target).graph()))
    plt.close('all')


def make_output_row(target_columns: dict[str, str]
                    , population: dict[Grouping, DataFrame], infected: dict[Grouping, DataFrame]
                    , pref: Prefecture, target: Grouping):
    df_population = population.get(target)
    df_infected = infected.get(target)
    outputFileName = OutputFileName('row', pref, target)

    # CSV出力
    df_population\
        .to_csv(FilePath.output(outputFileName.csv('population')), line_terminator="\n")
    df_infected[list(target_columns.keys())]\
        .to_csv(FilePath.output(outputFileName.csv('infected')), line_terminator="\n")

    # グラフ出力
    df_infected_graph = df_infected.reset_index()\
        .set_index('week_start')\
        .rename(columns=target_columns)[list(target_columns.values())]
    __make_graph_row(df_population, df_infected_graph, pref, target)
