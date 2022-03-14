# graph-infected
大阪府の人口情報と新型コロナ感染者数情報からグラフを作成するスクリプトです。

- output
  - 出力形式: 数値データ(CSV), グラフ(PNG)
  - 出力内容: 「人口当たりの感染者数割合」,「人口、感染者数」
  - 集約単位: 男女別、合計

## データ準備
### 人口データ
- 大阪府の毎月推計人口 https://www.pref.osaka.lg.jp/toukei/jinkou/jinkou-xlslist.html
  - 「年齢（５歳階級）別推計人口」のエクセルファイルを`output/jinkou-xlslist`フォルダに格納
### 感染者数データ 
- 厚生労働省 感染者動向 https://covid19.mhlw.go.jp/extensions/public/index.html
  - 「性別・年代別新規陽性者数（週別）」のオープンデータを`output`フォルダに格納

## 実行手順
### 人口データの月毎エクセルファイルを1CSVにまとめる
```
./venv/Scripts/python main_male_population_osaka_fu.py
```

### CSV、グラフを出力する
```
./venv/Scripts/python main.py
``` 

## 出力例
### グラフ
- 大阪府全体の人口当たりの感染者割合
![ratio_osaka_all](https://github.com/k-akie/graphinfected/blob/main/output/ratio_osaka_all.png)
- 大阪府全体の人口、感染者数
![row_osaka_all](https://github.com/k-akie/graphinfected/blob/main/output/row_osaka_all.png)
