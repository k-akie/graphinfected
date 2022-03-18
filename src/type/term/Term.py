from datetime import datetime as dt, datetime

from type.term.TermType import TermType


class Term:
    """
    期間

    Args:
        start   期間の開始日
        end     期間の終了日
        name    期間名
        time    何回目か
    """
    start: datetime
    end: datetime
    type: TermType
    time: int

    def __init__(self, _start: datetime, _end: datetime, _type: TermType, _time: int):
        self.start = _start
        self.end = _end
        self.type = _type
        self.time = _time

    def __str__(self) -> str:
        return f'{self.start}, {self.end}, {self.type}, {self.time}'


# 緊急事態宣言等の履歴
# https://www.kwm.co.jp/blog/state-of-emergency/
OSAKA_TERMS = [
    Term(dt.fromisoformat('2020-04-07'), dt.fromisoformat('2020-05-21'), TermType.EMERGENCY, 1),
    Term(dt.fromisoformat('2021-01-14'), dt.fromisoformat('2021-02-28'), TermType.EMERGENCY, 2),
    Term(dt.fromisoformat('2021-04-05'), dt.fromisoformat('2021-04-24'), TermType.SEMI_EMERGENCY, 1),
    Term(dt.fromisoformat('2021-04-25'), dt.fromisoformat('2021-06-20'), TermType.EMERGENCY, 3),
    Term(dt.fromisoformat('2021-06-21'), dt.fromisoformat('2021-08-01'), TermType.SEMI_EMERGENCY, 2),
    Term(dt.fromisoformat('2021-08-02'), dt.fromisoformat('2021-09-30'), TermType.EMERGENCY, 4),
    Term(dt.fromisoformat('2022-01-27'), dt.fromisoformat('2022-03-21'), TermType.SEMI_EMERGENCY, 3),
]
