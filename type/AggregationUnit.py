from enum import Enum

from type.Unit import Unit


class AggregationUnit(Enum):
    ALL = Unit('all', '全体')
    MALE = Unit('male', '男性')
    FEMALE = Unit('female', '女性')
