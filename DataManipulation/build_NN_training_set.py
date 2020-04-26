from io import StringIO
import csv
import pandas as pd
import numpy as np
import tensorflow as tf
import re
from urllib import parse
import requests
from sql_api import api_query
import os


def load_mt_matrix():
    path_str = repr(os.path.dirname(os.path.abspath(__file__)))
    path_str = path_str.replace("\\\\", "/")
    path_str = path_str.replace("'", "")
    return pd.read_csv(path_str + "/static/MovieTraitMatrix.csv")


def bin_traits(traits, df):
    bin_labels = list(np.linspace(0, 98, 50))
    print("Trait bin labels: %s" % repr(bin_labels))
    bin_vals = np.linspace(0, 100, 51)
    bin_intervals = []
    for i in range(bin_vals.shape[0] - 1):
        bin_intervals.append((bin_vals[i], bin_vals[i + 1]))
    print("Trait bin intervals: %s\n" % repr(bin_intervals))

    for trait in traits:
        df[trait] = pd.cut(df[trait], bin_vals, labels=bin_labels, include_lowest=True)

    return df


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
def build_training_set(users=200, movies=200, num_bins=5, group_by_movie=False, save_file=False):
    # load matrix mapping peronality traits to genres
    # movie_trait_matrix = pd.read_csv('./static/MovieTraitMatrix.csv')

    movie_trait_matrix = load_mt_matrix()

    new_traits = np.array(movie_trait_matrix['trait_name'])
    new_traits[0::2] = new_traits[0::2] + 'H'
    new_traits[1::2] = new_traits[1::2] + 'L'

    movie_trait_matrix['trait_name'] = pd.Series(new_traits)
    movie_trait_matrix.set_index('trait_name', inplace=True)
    # print(movie_trait_matrix)

    query = 'SELECT Movie.tConst FROM Movie'
    movie_ids, code = api_query(query)

    # bring in all movies and their ratings
    query = 'SELECT Movie.tConst, Movie.rating FROM Movie'
    ratings, code3 = api_query(query)
    ratings.set_index('tConst', inplace=True)

    # bring in all movies and their corresponding genres
    query = 'SELECT MovieCategory.tConst, Genre.genreName, Genre.genreId' \
            ' FROM MovieCategory' \
            ' INNER JOIN Genre ON MovieCategory.genreId = Genre.genreId'
    movie_cat, code2 = api_query(query)
    movie_cat.set_index('tConst', inplace=True)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # initialize size of dataset of 60,000 total records
    num_users = users  # 250 users with randomized personality traits
    num_movies = movies  # randomly assign 200 movies to each user
    total_num_movies = movie_ids.shape[0]

    # initialize users with random personality traits
    traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    user_traits = pd.DataFrame(np.random.uniform(0, 100, size=(num_users, 5)), columns=traits)
    user_traits['user_id'] = pd.Series(np.arange(0, user_traits.shape[0]))
    user_traits.set_index('user_id', inplace=True)
    # print(user_traits)

    # randomly assign each user the given number of movies
    cols = ['user_id', 'movie_i']
    user_ids = np.array(sorted(list(range(0, num_users))*num_movies)).reshape((num_movies*num_users, 1))
    ri_movies = np.random.randint(0, high=total_num_movies, size=(num_movies*num_users, 1))
    training_set = np.concatenate([user_ids, ri_movies], axis=1)
    training_set = pd.DataFrame(training_set, columns=cols)
    # print(training_set)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # grab genres from the corresponding random movie id's tht were assigned
    training_set['tConst'] = training_set.loc[:, 'movie_i'].apply(lambda x: movie_ids['tConst'][x])
    training_set = training_set.join(movie_cat, on='tConst', how='inner')
    training_set = training_set.join(user_traits, on='user_id', how='inner')
    training_set.sort_values('user_id', inplace=True)
    training_set.reset_index(drop=True, inplace=True)
    # print(training_set)

    # join MovieTraitMatrix to bring in corresponding relationships between traits and the given genre
    genre_df = movie_trait_matrix.T
    training_set = training_set.join(genre_df, on='genreName', how='inner')
    training_set.sort_index(inplace=True)
    # print(training_set)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # interpolate probabilities based on the MovieTraitMatrix values that were just joined in
    prob_traits = np.array(pd.Series(np.array(traits)))
    prob_traits = 'prob' + prob_traits
    prob = pd.DataFrame()

    for trait in traits:
        # print(trait)
        highY = training_set[trait + 'H']
        # print(highY)
        highX = 100
        lowY = training_set[trait + 'L']
        # print(lowY)
        lowX = 0
        mag = training_set[trait]
        # print(mag)
        prob_vals = (lowY + (highY - lowY) / (highX - lowX) * mag) / 100
        # print(prob_vals)
        prob['prob' + trait] = prob_vals
    # print(prob)

    training_set['prob'] = prob.mean(axis=1)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # reduce dataframe down to required columns
    final_df = training_set.loc[:, ['user_id', 'tConst', 'genreId', 'genreName', 'prob', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']]

    if group_by_movie:
        final_df = final_df.groupby(['user_id', 'tConst']).mean()

    # calculate original mean, std dev, and z score of the distribution
    # (probability user will like random movie based solely on their personality traits and the movie's genres)
    avg = final_df['prob'].mean()
    std = final_df['prob'].std()
    # print("Original statistics:")
    # print('Avg: %s' % repr(avg))
    # print('Std: %s\n' % repr(std))
    final_df['z_score'] = (final_df['prob'] - avg) / std

    # adjust the distribution to fit the parameters below
    target_avg = 0.50
    target_std = 0.23
    final_df['new_prob'] = final_df['z_score'] * target_std + target_avg
    # print("Adjusted statistics:")
    # print('Avg: %s' % repr(final_df['new_prob'].mean()))
    # print('Std: %s\n' % repr(final_df['new_prob'].std()))

    # clean data to ensure nothing greater than 1 and nothing below 0
    idx = pd.IndexSlice
    mask = final_df['new_prob'] > 1
    final_df.loc[idx[mask], 'new_prob'] = 1
    mask = final_df['new_prob'] < 0
    final_df.loc[idx[mask], 'new_prob'] = 0
    # print(final_df)

    # add original ratings for comparison
    final_df = final_df.join(ratings, on='tConst', how='inner')
    # print(final_df)

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # bring in all movies and their corresponding genres (if movies were grouped by movie previously)
    if group_by_movie:
        query = 'SELECT MovieCategory.tConst, GROUP_CONCAT(Genre.genreName) AS Genres' \
                ' FROM MovieCategory' \
                ' INNER JOIN Genre ON MovieCategory.genreId = Genre.genreId' \
                ' GROUP  BY tconst'
        movie_cat, code4 = api_query(query)
        movie_cat.set_index('tConst', inplace=True)
        print(movie_cat)

        final_df = final_df.join(movie_cat, on='tConst', how='inner')
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # bin_labels = list(range(0, num_bins))
    # print("Bin labels: %s" % repr(bin_labels))
    # bin_vals = np.linspace(0, 10, num_bins + 1)
    # bin_intervals = []
    # for i in range(bin_vals.shape[0] - 1):
    #     bin_intervals.append((bin_vals[i], bin_vals[i + 1]))
    # print("Bin intervals: %s\n" % repr(bin_intervals))
    #
    # # bins = pd.IntervalIndex.from_tuples(bin_intervals)
    # final_df['BinProb'] = pd.cut(final_df['new_prob']*10, bin_vals, labels=bin_labels, include_lowest=True)
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    bin_labels = list(range(0, num_bins))
    # print("Bin labels: %s" % repr(bin_labels))
    bin_vals = np.linspace(0, 1, num_bins + 1)
    bin_intervals = []
    for i in range(bin_vals.shape[0] - 1):
        bin_intervals.append((bin_vals[i], bin_vals[i + 1]))
    # print("Bin intervals: %s\n" % repr(bin_intervals))

    # bins = pd.IntervalIndex.from_tuples(bin_intervals)
    final_df['BinProb'] = pd.cut(final_df['new_prob'], bin_vals, labels=bin_labels, include_lowest=True)
    # print(final_df)

    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if final_df['BinProb'].isnull().any():
        print("WARNING: Dataset has null classifications.")
    else:
        print("Items successfully binned. No null classifications detected.")

    export_df = final_df.loc[:, ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism',
                                 'genreId', 'genreName', 'BinProb']]

    export_df = export_df.astype({'genreId': 'float32'})

    if save_file:
        export_df.to_csv('../application/server/MovieTraitModel/MovieTraitTrainingSet.csv')

    return export_df


if __name__ == "__main__":
    test_df = build_training_set(users=200, movies=200, num_bins=20, save_file=True)
    feats = test_df.iloc[:, 0:6].values.astype(np.float32)
    print(feats)
    print(feats.shape)
    print(type(feats))
    print(feats[0, 5])
    print(type(feats[0, 5]))

    labels = np.array(test_df.iloc[:, 6].values)
    labels = labels.reshape((labels.shape[0], 1))
    print(labels.shape)
    print(type(labels))
