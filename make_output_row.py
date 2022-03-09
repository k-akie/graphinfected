import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from graph_option import emergency_term, semi_emergency_term


def _make_graph_row(df_population, df_infected, prefectures, target):
    # グラフ全体の設定
    plt.figure(figsize=(10.0, 8.0))  # 横、縦
    plt.plot(df_infected, label=df_infected.columns)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in emergency_term:  # 緊急事態宣言
        plt.axvspan(term[0], term[1], color="orange", alpha=0.3, label=term[2])
    for term in semi_emergency_term:  # まん延防止等重点措置
        plt.axvspan(term[0], term[1], color="yellow", alpha=0.3, label=term[2])

    # 左Y軸 主目盛
    plt.ylabel('infected')
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
    ax2.plot(df_population, label=df_population.columns, linestyle='dashdot', linewidth =0.8)
    ax2.set_ylim(0, 1000000)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(250000))
    ax2.set_ylabel('population')

    # 全体設定
    plt.title(f"{prefectures} [{target}]", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"output/row_{prefectures}_{target}.png")
    plt.close('all')


def make_output_row(target_columns, population, infected, prefectures, target):
    df_population = population.get(target)

    df_infected = infected.get(target)
    df_infected.reset_index(inplace=True)
    df_infected.set_index('week_start', inplace=True)

    # 出力
    _make_graph_row(df_population, df_infected[target_columns], prefectures, target)
    df_population.to_csv(f'output/row_{prefectures}_{target}.csv')
