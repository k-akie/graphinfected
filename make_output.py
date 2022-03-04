import pandas as pd
import matplotlib.pyplot as plt


def data_merge(target_columns, df_population, df_infected):
    df_result = pd.DataFrame()
    for index, infectedRow in df_infected.iterrows():
        infected_series = infectedRow.loc[target_columns]
        population_series = df_population.loc[infectedRow['month']]
        df_result[infectedRow['week']] = infected_series * 100 / population_series

    return df_result.T


def make_graph(df_result, prefectures, gender):
    # グラフ全体の設定
    plt.figure(figsize=(12.0, 8.0))  # 横、縦
    plt.plot(df_result)
    plt.legend(df_result.columns)
    plt.title(f"{prefectures} [{gender}]", fontsize=14)

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
