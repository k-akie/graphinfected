import matplotlib

from logic.make_output_ratio import make_output_ratio
from logic.make_output_row import make_output_row
from logic.read_infected import read_infected
from logic.read_population_osaka_fu import read_population_osaka_fu
from type.FilePath import FilePath
from type.Generation import generation_dict
from type.Grouping import Grouping
from type.Prefecture import Prefecture

if __name__ == '__main__':
    osaka = Prefecture('osaka', '大阪')
    # 人口データ
    population = read_population_osaka_fu(list(generation_dict.keys()), FilePath.input('jinkou-xlslist.csv'), 'UTF-8')

    # 感染者数データ
    infected = read_infected(FilePath.input('newly_confirmed_cases_detail_weekly.csv'), 'UTF-8')

    # グラフに日本語を使う設定
    matplotlib.rc('font', family='BIZ UDGothic')

    # 出力(割合)
    make_output_ratio(generation_dict, population, infected, osaka, Grouping.MALE)
    make_output_ratio(generation_dict, population, infected, osaka, Grouping.FEMALE)
    make_output_ratio(generation_dict, population, infected, osaka, Grouping.ALL)

    # 出力(生値)
    make_output_row(generation_dict, population, infected, osaka, Grouping.MALE)
    make_output_row(generation_dict, population, infected, osaka, Grouping.FEMALE)
    make_output_row(generation_dict, population, infected, osaka, Grouping.ALL)
