import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras.models as models
# from DataManipulation.BuildModel import df_to_dataset, model_feats, num_cats


# model_traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
trait_names = {'trOpen': 'Openness',
               'trCon': 'Conscientiousness',
               'trEx': 'Extraversion',
               'trAg': 'Agreeableness',
               'trNe': 'Neuroticism'}

model_traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
model_feats = model_traits + ['genreName']
num_cats = 20
# model_genres = ['Romance', 'Biography', 'Crime', 'Drama', 'Adventure', 'Family', 'History', 'Fantasy', 'War',
#                 'Thriller', 'Documentary', 'Comedy', 'Mystery', 'Horror', 'Western', 'Music', 'Action', 'Sci-Fi',
#                 'Animation', 'Musical', 'Sport', 'Film-Noir', 'News', 'Talk-Show', 'Adult', 'Reality-TV', 'Short',
#                 'Game-Show']


def df_to_dataset(df, shuffle=False, batch_size=32):
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
    # print(repr(mt_model))

    # rebuild_df = pd.read_csv('./MovieTraitModel/MovieTraitRebuild.csv')
    rebuild_df = pd.read_csv('./application/server/MovieTraitModel/MovieTraitRebuild.csv')
    rebuild_df = rebuild_df.loc[:, model_feats + ['BinProb']]
    # print(rebuild_df)
    rebuild_ds = df_to_dataset(rebuild_df)

    loss, accuracy = mt_model.evaluate(rebuild_ds)
    print("\nAccuracy on loaded model: ", accuracy)
    # mt_model.summary()
    return mt_model, rebuild_df


def see_mtnn(features_df, mt_model):
    """calculates compatibility and returns as numpy array"""
    batch_size = 1  # traits_df.shape[0]
    print("Pre Index:")
    print(features_df)
    print("Post Index:")
    features_df.reset_index(inplace=True)
    print(features_df)

    df = features_df.loc[:, model_feats].copy()
    print(df)
    traits_ds = tf.data.Dataset.from_tensor_slices(dict(df))
    traits_ds = traits_ds.batch(batch_size)

    compat = mt_model.predict(traits_ds, verbose=1)
    compat = (np.argmax(compat, axis=1) + 1)/num_cats

    return compat


def build_features_df(user_df, tconst_list, genre_df):
    if tconst_list:
        feats_df = pd.DataFrame()
        for tconst in tconst_list:
            temp = user_df.copy()
            temp['tConst'] = tconst
            feats_df = pd.concat([feats_df, temp])

        genre_df.set_index('tConst', inplace=True)
        feats_df = feats_df.join(genre_df, on='tConst', how='inner')
    else:
        # feats_df = pd.DataFrame([trait_dict for i in range(genre_df.shape[0])])
        feats_df = pd.DataFrame()
        for gen in list(genre_df['genreName'].values):
            temp = user_df.copy()
            temp['genreName'] = gen
            feats_df = pd.concat([feats_df, temp])

    return feats_df


def calc_personalized_rating(df):
    compat = df['compatibility']
    df['personalRating'] = df['rating'] * (-0.8 * compat**2 + 2.4 * compat)
    return df


def calc_genre_compat(user_df, tconst_list, genre_df, model):
    user_df = rename_trait_cols(user_df)
    results_df = build_features_df(user_df, tconst_list, genre_df)  # build features dataframe for NN
    results_df['compatibility'] = see_mtnn(results_df, model)  # calculate compatility through NN

    if tconst_list:
        results_df = results_df.groupby(['userId', 'tConst'], as_index=False).mean()
        results_df = results_df.loc[:, ['userId', 'tConst', 'rating', 'compatibility']]
        results_df = calc_personalized_rating(results_df)
    else:
        num_results = 5
        results_df.sort_values('compatibility', inplace=True, ascending=False)
        results_df.reset_index(inplace=True)
        results_df = results_df.loc[0:num_results - 1, ['userId', 'genreName', 'compatibility']]

    return results_df


def rename_trait_cols(df):
    new_names = trait_names.copy()
    for col in df:
        if col not in new_names.keys():
            new_names[col] = col
    df.rename(columns=new_names, inplace=True)

    return df


if __name__ == "__main__":
    test_mod = load_model()
    test_mod.summary()
