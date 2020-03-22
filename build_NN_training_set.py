from io import StringIO
import csv
import pandas as pd
import numpy as np
import re
from urllib import parse
import requests
from sql_api import api_query

query = 'SELECT Movie.tConst FROM Movie'
movie_ids, code = api_query(query)

query = 'SELECT MovieCategory.tConst, MovieCategory.genreId, Genre.genreName' \
        ' FROM MovieCategory' \
        ' INNER JOIN Genre ON MovieCategory.genreId = Genre.genreId'
movie_cat, code = api_query(query)
movie_cat.set_index('tConst', inplace=True)

num_users = 500
num_movies = 100
total_num_movies = movie_ids.shape[0]

user_ids = np.arange(num_users)
opennness = np.random.uniform(0, 100, size=user_ids.shape)
conscientiousness = np.random.uniform(0, 100, size=user_ids.shape)
extraversion = np.random.uniform(0, 100, size=user_ids.shape)
agreeableness = np.random.uniform(0, 100, size=user_ids.shape)
neuroticism = np.random.uniform(0, 100, size=user_ids.shape)
user_array = np.array([user_ids, opennness, conscientiousness, extraversion, agreeableness, neuroticism])
print(user_array.shape)
print(user_array[:, 0])
# training_set = pd.DataFrame

# for i in user_ids:
#     for j in np.arange(num_movies):
# ri_movie = np.random.randint(0, total_num_movies)

# print(user_ids)
# print(opennness)

movie_trait_matrix = pd.read_csv('./static/MovieTraitMatrix.csv')
# cocktail_raw['recipeId'] = range(0, cocktail_raw.shape[0])
# categorized_ing.set_index('word', inplace=True)
print(movie_trait_matrix)