import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def _make_graph_row(df_population, df_infected, prefectures, target):
    # グラフ全体の設定
    plt.figure(figsize=(10.0, 8.0))  # 横、縦
    plt.plot(df_population, label=df_population.columns)

    # Y軸 主目盛
    plt.ylabel('population')
    plt.ylim(0, 1000000)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(100000))
    plt.gca().tick_params(which='major', axis='y', length=6)
    plt.grid(which='major', axis='y')
    # Y軸 補助目盛
    plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(50000))
    plt.gca().tick_params(which='minor', axis='y', direction='in')
    plt.grid(which='minor', axis='y', linestyle='dotted')

    # X軸 主目盛
    plt.xlim(datetime.date(2020, 4, 1), datetime.date(2022, 4, 1))
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().tick_params(which='major', axis='x', length=6)
    plt.grid(which='major', axis='x')
    # X軸 補助目盛
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.gca().tick_params(which='minor', axis='x', direction='in')
    plt.grid(which='minor', axis='x', linestyle='dotted')

    # 全体設定
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f"output/row_{prefectures}_{target}.png")
    plt.close('all')


def make_output_row(target_columns, population, infected, prefectures, target):
    df_population = population.get(target)
    df_infected = infected.get(target)

    # 出力
    _make_graph_row(df_population, df_infected, prefectures, target)
    df_population.to_csv(f'output/row_{prefectures}_{target}.csv')
