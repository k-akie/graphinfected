import datetime


class TypeDate:
    @staticmethod
    def format() -> str:
        return '%Y/%m/%d'

    @staticmethod
    def min() -> datetime.date:
        return datetime.date(2020, 3, 1)

    @staticmethod
    def max() -> datetime.date:
        return datetime.date(2022, 5, 1)

    @staticmethod
    def from_str(_value: str, _format: str = '%Y/%m/%d'):  # TODO v3.10に上げたら format() を初期値にする
        return datetime.datetime.strptime(_value, _format)

    @staticmethod
    def first_of_month(_value: str):
        return datetime.datetime.strptime(_value, TypeDate.format()).replace(day=1)
