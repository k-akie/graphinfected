from datetime import datetime as dt


# 緊急事態宣言等の履歴
# https://www.kwm.co.jp/blog/state-of-emergency/
emergency_term = [  # 緊急事態宣言
    [dt.fromisoformat('2020-04-07'), dt.fromisoformat('2020-05-21'), 'emergency'],  # 1回目
    [dt.fromisoformat('2021-01-14'), dt.fromisoformat('2021-02-28'), None],  # 2回目
    [dt.fromisoformat('2021-04-25'), dt.fromisoformat('2021-06-20'), None],  # 3回目、2回目のまん防に変わった
    [dt.fromisoformat('2021-08-02'), dt.fromisoformat('2021-09-30'), None],  # 4回目
]
semi_emergency_term = [  # まん延防止等重点措置
    [dt.fromisoformat('2021-04-05'), dt.fromisoformat('2021-04-24'), 'semi emergency'],  # 1回目、3回目の緊急事態宣言に変わった
    [dt.fromisoformat('2021-06-21'), dt.fromisoformat('2021-08-01'), None],  # 2回目、4回目の緊急事態宣言に変わった
    [dt.fromisoformat('2022-01-27'), dt.fromisoformat('2022-03-21'), None],  # 3回目、延長中
]