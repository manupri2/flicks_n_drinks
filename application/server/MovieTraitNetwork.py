import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras.models as models
# from DataManipulation.BuildModel import df_to_dataset, model_feats, num_cats


trait_names = {'trOpen': 'Openness',
               'trCon': 'Conscientiousness',
               'trEx': 'Extraversion',
               'trAg': 'Agreeableness',
               'trNe': 'Neuroticism'}

model_traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
model_feats = model_traits + ['genreName']
num_cats = 20


def df_to_dataset(df, shuffle=False, batch_size=32):
    """Utility function to convert pandas df to tensorflow dataset"""
    df = df.copy()
    labels = df.pop('BinProb')
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(df))
    ds = ds.batch(batch_size)
    return ds


def load_model():
    # model_file = './MovieTraitModel'
    model_file = './application/server/MovieTraitModel'
    mt_model = models.load_model(model_file)

    # rebuild_df = pd.read_csv('./MovieTraitModel/MovieTraitRebuild.csv')
    rebuild_df = pd.read_csv('./application/server/MovieTraitModel/MovieTraitRebuild.csv')
    rebuild_df = rebuild_df.loc[:, model_feats + ['BinProb']]
    rebuild_ds = df_to_dataset(rebuild_df)

    # need to evaluate in order to re-establish expected input
    loss, accuracy = mt_model.evaluate(rebuild_ds)
    print("\nAccuracy on loaded model: ", accuracy)

    return mt_model, rebuild_df


def see_mtnn(features_df, mt_model):
    """calculates compatibility between genres and personality traits and returns as numpy array"""
    batch_size = 1  # traits_df.shape[0]

    # transform features from pandas df to a tenorflow dataset
    df = features_df.loc[:, model_feats].copy()
    traits_ds = tf.data.Dataset.from_tensor_slices(dict(df))
    traits_ds = traits_ds.batch(batch_size)

    # predict compatibility, return as numpy array
    compat = mt_model.predict(traits_ds, verbose=1)

    # convert values from integer labels into percentages
    compat = (np.argmax(compat, axis=1) + 1)/num_cats

    return compat


def build_features_df(user_df, tconst_list, genre_df):
    """build the features df which serves as input for the NN"""

    if tconst_list:
        # if movies supplied, map each movie's genre to each user (if given multiple users)
        feats_df = pd.DataFrame()

        # this essentially joins user_df to tConst (performed this way incase there are multiple users)
        for tconst in tconst_list:
            temp = user_df.copy()
            temp['tConst'] = tconst
            feats_df = pd.concat([feats_df, temp])

        # join 'genreName' and movie 'rating' on 'tConst'
        genre_df.set_index('tConst', inplace=True)
        feats_df = feats_df.join(genre_df, on='tConst', how='inner')
    else:
        # if no movies were supplied, simply map all genres to each user
        # (to calculate compatibility for a user on all genres)
        feats_df = pd.DataFrame()
        for gen in list(genre_df['genreName'].values):
            temp = user_df.copy()
            temp['genreName'] = gen
            feats_df = pd.concat([feats_df, temp])

    feats_df.reset_index(inplace=True)
    return feats_df


def calc_personalized_rating(df):
    """Scales the population-voted 'rating' with the calculated compatibility to return a 'personalRating'"""
    compat = df['compatibility']
    df['personalRating'] = df['rating'] * (-0.8 * compat**2 + 2.4 * compat)
    return df


def calc_genre_compat(user_df, tconst_list, genre_df, model):
    """
    The main function that coordinates calculating compatibility through the NN
        - calculate the user's compatability with each movie; ultimately joins 'user_df' and 'genre_df'
        - group by movie if movies supplied, return top 5 genres if no movies supplied
        - add new column for 'personalRating'

    :param user_df: pandas df of user_info including personality traits, can be one or more users
    :param tconst_list: list of movie's tConst values to map to users, can also be empty
    :param genre_df:
    :param model: instantiated neural network model
    :return: pandas df as described above
    """
    # rename column labels to match those defined in the NN features
    user_df = rename_trait_cols(user_df)

    # build features dataframe for NN
    results_df = build_features_df(user_df, tconst_list, genre_df)

    # calculate compatility through NN
    results_df['compatibility'] = see_mtnn(results_df, model)

    if tconst_list:
        # if movies were given in tConst, group values by user and movie (averaging compatibilities)
        results_df = results_df.groupby(['userId', 'tConst'], as_index=False).mean()
        results_df = results_df.loc[:, ['userId', 'tConst', 'rating', 'compatibility']]
        results_df = calc_personalized_rating(results_df)
    else:
        # if no movies given in tConst, return top 5 results (top 5 genres)
        num_results = 5
        results_df.sort_values('compatibility', inplace=True, ascending=False)
        results_df.reset_index(inplace=True)
        results_df = results_df.loc[0:num_results - 1, ['userId', 'genreName', 'compatibility']]

    return results_df


def rename_trait_cols(df):
    """
    Simply renames column labels to match those defined in the neural network features
    """
    new_names = trait_names.copy()
    for col in df:
        if col not in new_names.keys():
            new_names[col] = col
    df.rename(columns=new_names, inplace=True)

    return df


if __name__ == "__main__":
    test_mod = load_model()
    test_mod.summary()
