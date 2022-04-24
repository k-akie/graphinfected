from datetime import datetime as dt, datetime

from type.term.TermType import TermType


class Term:
    """
    期間

    Args:
        start   期間の開始日
        end     期間の終了日
        name    期間名
    """
    start: datetime
    end: datetime
    type: TermType

    def __init__(self, _start: str, _end: str, _type: TermType):
        self.start = dt.fromisoformat(_start)
        self.end = dt.fromisoformat(_end)
        self.type = _type

    def __str__(self) -> str:
        return f'{self.start}, {self.end}, {self.type}'
