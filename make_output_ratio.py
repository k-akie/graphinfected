import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from graph_option import emergency_term, semi_emergency_term


def _search_month(target_month, exists_month):
    if target_month in exists_month:
        return target_month

    # 対象月が存在するデータ範囲より前なら、もっとも古い日付のデータを使う
    start_date = exists_month[0]
    if target_month < start_date:
        return start_date

    # 対象月が存在するデータ範囲より前なら、もっとも新しい日付のデータを使う
    return exists_month[len(exists_month)-1]


def _calc_ratio(target_columns, df_population, df_infected):
    df_result = pd.DataFrame()
    for index, infectedRow in df_infected.iterrows():
        infected_series = infectedRow.loc[target_columns]

        month = _search_month(infectedRow['month'], df_population.index)
        population_series = df_population.loc[month]

        df_result[infectedRow['week_start']] = infected_series * 100 / population_series

    return df_result.T


def _make_graph_ratio(df_result, prefectures, target):
    # グラフ全体の設定
    plt.figure(figsize=(10.0, 8.0))  # 横、縦
    plt.plot(df_result, label=df_result.columns)

    # 背景 https://bunsekikobako.com/axvspan-and-axhspan/
    for term in emergency_term:  # 緊急事態宣言
        plt.axvspan(term[0], term[1], color="orange", alpha=0.3, label=term[2])
    for term in semi_emergency_term:  # まん延防止等重点措置
        plt.axvspan(term[0], term[1], color="yellow", alpha=0.3, label=term[2])

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
    plt.xlim(datetime.date(2020, 3, 1), datetime.date(2022, 5, 1))
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
    plt.title(f"{prefectures} [{target}]", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"output/ratio_{prefectures}_{target}.png")
    plt.close('all')


def make_output_ratio(target_columns, population, infected, prefectures, target):
    # 出力用にデータを加工
    df_result = _calc_ratio(target_columns, population.get(target), infected.get(target))

    # 出力
    _make_graph_ratio(df_result, prefectures, target)
    df_result.to_csv(f'output/ratio_{prefectures}_{target}.csv')
