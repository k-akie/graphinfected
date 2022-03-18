from enum import Enum


class TermType(Enum):
    """
    期間の種類

    Args:
        name    期間名
    """
    EMERGENCY = '緊急事態宣言'
    SEMI_EMERGENCY = 'まん延防止等重点措置'

    def __str__(self):
        return self.name
