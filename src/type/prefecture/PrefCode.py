class PrefCode:
    """
    都道府県コード

    Args:
        value   都道府県コード(2桁の数字)
    """
    value: str

    def __init__(self, _value: str):
        self.value = _value

    def __str__(self):
        return self.value
