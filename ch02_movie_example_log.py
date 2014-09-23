# -*- coding: utf-8 -*-
import pandas as pd

path_to_users = '/Users/hory/Library/Canopy/data/pydata-book-master/ch02/movielens/users.dat'
path_to_ratings = '/Users/hory/Library/Canopy/data/pydata-book-master/ch02/movielens/ratings.dat'
path_to_movies = '/Users/hory/Library/Canopy/data/pydata-book-master/ch02/movielens/movies.dat'

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(path_to_users, sep='::', header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(path_to_ratings, sep='::', header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(path_to_movies, sep='::', header=None, names=mnames)

# 読み込み確認
users[:5]
ratings[:5]
movies[:5]

# ３つの表を１つにマージする
# ２つの表に共通列が存在する場合、その列名から推測して結合する
data = pd.merge(pd.merge(ratings, users), movies)

# マージを確認
data[:5]

# ある映画の性別・年齢ごとの平均評価を算出
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
mean_ratings[:5]

# 分析対象をレビューが250件以上の映画にしぼる
# 1 各映画ごとの評価件数をratings_by_titleに格納
# 2 ratings_by_titleから件数が250件以上を抽出しactive_titlesに格納
ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title.index[ratings_by_title >= 250]

# 確認
ratings_by_title[:10]
active_titles

# レビュー250件以上の映画の平均評価
mean_ratings_250 = mean_ratings.ix[active_titles]
mean_ratings_250[:10]

# 女性評価が高い上位10件
top_female_ratings = mean_ratings_250.sort_index(by='F', ascending=False)
top_female_ratings[:10]

# 男女間で評価差が大きかった映画
# mean_ratings_250にdiffという名前の列を追加
mean_ratings_250['diff'] = mean_ratings_250['M'] - mean_ratings_250['F']
sorted_by_diff = mean_ratings_250.sort_index(by='diff')
sorted_by_diff[:15]
#逆順から15件：男性評価が高く、女性評価が低い映画
sorted_by_diff[::-1][:15]

#評価が大きく割れた映画（性別問わない）
#映画タイトルごとの評価値の標準偏差の計算
rating_std_by_title = data.groupby('title')['rating'].std()

#評価件数250件以上の映画のみを抽出
rating_std_by_title = rating_std_by_title.ix[active_titles]
#降順でソート
rating_std_by_title.order(ascending=False)[:10]


