import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

movie = pd.read_csv("movie.csv")

rating = pd.read_csv("rating.csv")

df = movie.merge(rating, how="left", on="movieId")

comment_counts = pd.DataFrame(df["title"].value_counts())

rare_movies = comment_counts[comment_counts["title"] < 10000].index

common_movies = df[~df["title"].isin(rare_movies)]

user_movie_df = common_movies.pivot_table(values="rating", index="userId", columns="title")

random_user = int(pd.Series(user_movie_df.index).sample(1).values)

# 28941

random_user_df = user_movie_df[user_movie_df.index == random_user]

movies_watched = list(random_user_df.columns[random_user_df.notna().any()])

movies_watched_df = user_movie_df[movies_watched]

user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]

user_movie_count[user_movie_count["userId"] == random_user]

percentage = 60
user_same_movies = user_movie_count[user_movie_count["movie_count"] > (len(movies_watched) * percentage / 100)]["userId"]

final_df = movies_watched_df[movies_watched_df.index.isin(user_same_movies)]

corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ["userId_1", "userId_2"]
corr_df = corr_df.reset_index()

corr_df[corr_df["userId_1"] == random_user]

corr_th = 0.65
top_users = corr_df[(corr_df["userId_1"] == random_user) & (corr_df["corr"] > corr_th)][["userId_2", "corr"]].sort_values("corr", ascending=False)
top_users.shape

top_users.columns = ["userId", "corr"]
top_users_ratings = top_users.merge(rating, how="left", on="userId")

top_users_ratings["weighted_rating"] = top_users_ratings["corr"] * top_users_ratings["rating"]


recommendation_df = top_users_ratings[["movieId", "weighted_rating"]]

rating_th = 3.5
movies_to_be_recommended = recommendation_df[recommendation_df["weighted_rating"] > rating_th]. \
    sort_values("weighted_rating", ascending=False).head()

movies_to_be_recommended.merge(movie[["movieId", "title"]])

user = 28941

movie = pd.read_csv("movie.csv")
rating = pd.read_csv("rating.csv")
df = movie.merge(rating, how="left", on="movieId")

top_rated_movies = df[(df["userId"] == user) & (df["rating"] == 5)]
last_top_rated_movie_id = top_rated_movies.sort_values(by="timestamp", ascending=False)["movieId"][0:1].values[0]

movie[movie["movieId"] == last_top_rated_movie_id]["title"].values[0]
movie_df = user_movie_df[movie[movie["movieId"] == last_top_rated_movie_id]["title"].values[0]]

recommended_movies = user_movie_df.corrwith(movie_df).sort_values(ascending=False)

recommended_movies[1:6].index
