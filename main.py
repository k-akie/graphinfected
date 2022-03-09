import matplotlib

from make_output_row import make_output_row
from read_infected import read_infected
from read_population_osaka_fu import read_population_osaka_fu
from make_output_ratio import make_output_ratio
from type.AggregationUnit import AggregationUnit
from type.Prefecture import Prefecture

if __name__ == '__main__':
    osaka = Prefecture('osaka', '大阪')

    # 年代
    _period_array = ['Under 10', '10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', 'Over 90']

    # 人口データ
    population = read_population_osaka_fu(_period_array, 'input/jinkou-xlslist.csv', 'UTF-8')

    # 感染者数データ
    infected = read_infected('input/newly_confirmed_cases_detail_weekly.csv', 'UTF-8')

    # グラフに日本語を使う設定
    matplotlib.rc('font', family='BIZ UDGothic')

    # 出力(割合)
    make_output_ratio(_period_array, population, infected, osaka, AggregationUnit.MALE)
    make_output_ratio(_period_array, population, infected, osaka, AggregationUnit.FEMALE)
    make_output_ratio(_period_array, population, infected, osaka, AggregationUnit.ALL)

    # 出力(生値)
    make_output_row(_period_array, population, infected, osaka, AggregationUnit.MALE)
