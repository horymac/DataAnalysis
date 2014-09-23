# -*- coding: utf-8 -*-
path = 'Library/Canopy/data/pydata-book-master/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
open(path).readline()
import json
records = [json.loads(line) for line in open(path)]
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

#sequenceの数をカウントする
def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

#標準ライブラリを使用してカウントする
from collections import defaultdict

def get_counts2(sequence):
    counts = defaultdict(int) #values will initialize to 0
    for x in sequence:
        counts[x] += 1
    return counts
    
#上位10位をカウントする
def top_counts(count_dict, n=10):
        value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
        value_key_pairs.sort()
        return value_key_pairs[-n:]

#collections.Counterを使用して上位10位をカウントする
from collections import Counter
counts = Counter(time_zones)
counts.most_common(10)

#pandasを使用してタイムゾーンを集計する
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
frame = DataFrame(records)
frame

#空欄、存在していない箇所⇒fillnaメソッドで'Missing'の文字列で置換
#存在するが中身が空文字列⇒真偽値の配列によるインデックス参照を使って'Unknown'に置換
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
tz_counts[:10]

#ユーザーエージェントの先頭トークンを切り出して表示する
results = Series([x.split()[0] for x in frame.a.dropna()])
results[:5]
results.value_counts()[:8] #上位8位のカウントを表示

#Windowsユーザと非Windowsユーザを分類
#Windowsユーザ分類条件：UAに'Windows'の文字列が含まれるか
#frmaeオブジェクトを基にしてUAが存在しないレコードを除外
cframe = frame[frame.a.notnull()]
#numpy.where()を使用
operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')
operating_system[:5]

#タイムゾーンと稼働OSの組み合わせごとにグループ化する
#pandas.DataFrame.unstack()を使う
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)

#昇順のソートを使う
indexer = agg_counts.sum(1).argsort()
indexer[:10]
#ユーザー合計数昇順
count_subset = agg_counts.take(indexer)[-10:]
count_subset
#積み上げ棒グラフで表示
count_subset.plot(kind='barh', stacked=True)

#各行の合計が1になるように正規化
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)

