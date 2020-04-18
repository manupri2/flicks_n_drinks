import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sql_api import api_query
from Data Manipulation.build_NN_training_set import *


def df_to_dataset(df, shuffle=True, batch_size=32):
    df = df.copy()
    labels = df.pop('BinProb')
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(df))
    ds = ds.batch(batch_size)
    return ds


def demo(feat_column, print_res=True):
    example_batch = next(iter(train_ds_demo))[0]
    feat_layer = layers.DenseFeatures(feat_column)
    if print_res:
        print(feat_layer(example_batch).numpy())


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# load in list of all available genres
# query = 'SELECT Genre.genreName' \
#         ' FROM Genre'
# genres, code2 = api_query(query)
# genres = list(genres['genreName'].values)
# print(genres)
genres = ['Romance', 'Biography', 'Crime', 'Drama', 'Adventure', 'Family', 'History', 'Fantasy', 'War', 'Thriller',
          'Documentary', 'Comedy', 'Mystery', 'Horror', 'Western', 'Music', 'Action', 'Sci-Fi', 'Animation', 'Musical',
          'Sport', 'Film-Noir', 'News', 'Talk-Show', 'Adult', 'Reality-TV', 'Short', 'Game-Show']

# initialize personality traits
traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

# load training set
# training_set = pd.read_csv('./trainingSet/MovieTraitTrainingSet.csv')
num_cat = 5
training_set = build_training_set(users=300, movies=300, num_bins=num_cat)
training_set = training_set.loc[:, traits + ['genreName', 'BinProb']]
print(training_set)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# split dataframe into training set, testing set, and validation set
train, test = train_test_split(training_set, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')

# create a small batch for demonstration purposes
demo_batch_size = 5
train_ds_demo = df_to_dataset(train, batch_size=demo_batch_size)
val_ds_demo = df_to_dataset(val, shuffle=False, batch_size=demo_batch_size)
test_ds_demo = df_to_dataset(test, shuffle=False, batch_size=demo_batch_size)

# for feature_batch, label_batch in train_ds.take(1):
#     print('Every feature:', list(feature_batch.keys()))
#     print('A batch of Openness:', feature_batch['Openness'])
#     print('A batch of BinProbs:', label_batch)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# build model

# create bucketized trait columns
bounds = list(np.linspace(0, 100, 51))
trait_buckets = []
for feat in traits:
    print(feat)
    trait_feat = feature_column.numeric_column(feat)
    bucketized_feat = feature_column.bucketized_column(trait_feat, boundaries=bounds)
    trait_buckets.append(bucketized_feat)
    demo(bucketized_feat)

# create categorical genre columns
genre_feat = feature_column.categorical_column_with_vocabulary_list('genreName', genres)
genre_one_hot = feature_column.indicator_column(genre_feat)
print("Genres")
demo(genre_one_hot)

feature_columns = trait_buckets + [genre_one_hot]
# feature_columns = []
for trait in trait_buckets:
    crossed_feature = feature_column.crossed_column([trait, genre_feat], hash_bucket_size=1000)
    crossed_feature = feature_column.indicator_column(crossed_feature)
    demo(crossed_feature)
    feature_columns.append(crossed_feature)

# put feature columns into input layer
for feat in feature_columns:
    print(type(feat))
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# train model
# batch_size = 32
# train_ds = df_to_dataset(train, batch_size=batch_size)
# val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
# test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)
#
# model = tf.keras.Sequential([
#                               feature_layer,
#                               layers.Dense(356, activation='relu'),
#                               layers.Dense(356, activation='relu'),
#                               layers.Dense(num_cat)
#                             ])
#
# model.compile(optimizer='adam',
#               loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#               metrics=['accuracy'])
#
# model.fit(train_ds,
#           validation_data=val_ds,
#           epochs=5)
#
# loss, accuracy = model.evaluate(test_ds)
# print("Accuracy", accuracy)
