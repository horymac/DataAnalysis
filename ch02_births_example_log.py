# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

#csvファイルを読み込み
path_to_names = '/Users/hory/Library/Canopy/data/pydata-book-master/ch02/names/'
names1880 = pd.read_csv(path_to_names + 'yob1880.txt', names=['name', 'sex', 'births'])
names1880[:10]

#1880の性別別出生数
names1880.groupby('sex').births.sum()

#年度ごとのデータファイル郡をひとつのデータフレームオブジェクトにまとめる
#1880-2010まで
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = 'yob%d.txt' % year
    frame = pd.read_csv(path_to_names + path, names=columns)
    
    frame['year'] = year
    pieces.append(frame)
    
#piecesに格納された要素をひとつのデータフレームオブジェクトにまとめる
#pd.concat:行方向に行を追加する
#ignore_index=True:元の行番号は不要なので省略
names = pd.concat(pieces, ignore_index=True)

names[:10]
names

#年度ごとの性別別出生数算出
total_births = names.pivot_table('births', columns='sex', index='year', aggfunc=sum)
total_births.tail()
#グラフにプロットする
total_births.plot(title='Total births by sex and year')

#全出生数に対するその名前の割合を列として追加する
def add_prop(group):
    #integer同士の除算は繰り上げされてしまうためfloat型にキャスト
    births = group.births.astype(float)
    
    group['prop'] = births / births.sum()
    
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

#np.allcloseを使ってグループ内の総和が1となることを検証
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

#年代・性別ごとの上位1000件の名前取得
def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)

# 上位1000件データを男女別に選り分ける
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

#top1000を使った名前付けの傾向分析
#top1000を年代別データとして整理
total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)

#いくつかの名前ごとにプロットする
#John,Harry,Mary,Michel
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn', 'Aaron']]
subset.plot(subplots=True, figsize=(12, 10), grid=False, title="Number of births per year")

#（仮説）一般的な名前が減少している傾向があるのではないか
#その年の上位1000件の名前がその年の名前全体に対して占める割合を算出する
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0,1.2,13), xticks=range(1880,2020,10))

# その年の出生数の半分(50%)が何種類の名前で構成されるかを算出する
# データソースを読み込む
df = boys[boys.year == 2010]
df

# boysを降順にソートして何番目の名前のところで50%に到達するのかを調べる
# Numpy.searchsortedを使って、propの累積和が0.5を超えるところを探す
# cumsum:cumulative sum
prop_cumsum = df.sort_index(by='prop', ascending=False).prop.cumsum()
prop_cumsum.searchsorted(0.5) # AttributeError: 'Series' object has no attribute 'searchsorted' 
np.searchsorted(prop_cumsum, 0.5)[0]

# 出生年・性別ごとに分類し、そのグループごとに50%位置を返す
def get_quantile_count(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False).prop.cumsum()
    return np.searchsorted(group, q)[0] + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

diversity.plot(title='Number of popular names in top 50%')




# Numpy.cumsum():引数の数値の累積和を返す
# 1-10の累積和
a = np.array([1,2,3,4,5,6,7,8,9,10])
np.cumsum(a)

# 配列要素の中で指定要素の追加位置を返す
# 戻り値のインデックスは0から始まるため戻り値＋1番目
a = np.array([1,2,4,5])
np.searchsorted(a,3)





