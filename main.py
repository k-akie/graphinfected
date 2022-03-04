from read_infected import read_infected
from read_population_osaka_fu import read_population_osaka_fu
from make_output import make_graph, data_merge

if __name__ == '__main__':
    # 年代
    _period_array = ['Under 10', '10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', 'Over 90']

    # 人口データ
    population = read_population_osaka_fu(_period_array, 'input/jinkou-xlslist.csv', 'UTF-8')

    # 感染者数データ
    infected = read_infected('input/newly_confirmed_cases_detail_weekly.csv', 'UTF-8')

    # 結合＆グラフ作る
    result_female = data_merge(_period_array, population.get('male'), infected.get('male'))
    make_graph(result_female, 'osaka', 'male')

    result_male = data_merge(_period_array, population.get('female'), infected.get('female'))
    make_graph(result_male, 'osaka', 'female')

