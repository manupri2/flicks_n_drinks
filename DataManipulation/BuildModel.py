import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras.layers import Input, Dense, DenseFeatures
from tensorflow.keras.models import model_from_json, Model
from sklearn.model_selection import train_test_split
# from sql_api import api_query
from DataManipulation.build_NN_training_set import *
import tensorflow_hub as hub
import matplotlib.pyplot as plt


model_traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
model_feats = model_traits + ['genreName']
num_cats = 20
model_genres = ['Romance', 'Biography', 'Crime', 'Drama', 'Adventure', 'Family', 'History', 'Fantasy', 'War',
                'Thriller', 'Documentary', 'Comedy', 'Mystery', 'Horror', 'Western', 'Music', 'Action', 'Sci-Fi',
                'Animation', 'Musical', 'Sport', 'Film-Noir', 'News', 'Talk-Show', 'Adult', 'Reality-TV', 'Short',
                'Game-Show']


def df_to_dataset(df, shuffle=False, batch_size=32):
    df = df.copy()
    labels = df.pop('BinProb')
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(df))
    ds = ds.batch(batch_size)
    return ds


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def serialize_example(f1, f2, f3, f4, f5, f6):
    """
    Creates a tf.Example message ready to be written to a file.
    """

    # ser_ex = serialize_example(58.1405369, 71.62862, 31.579641, 60.0137228, 58.140536, b'Documentary')
    # features = tf.io.parse_example(ser_ex, features=tf.feature_column.make_parse_example_spec(feature_columns))

    # Create a dictionary mapping the feature name to the tf.Example-compatible data type.
    feature = {
        'Openness': _float_feature(f1),
        'Conscientiousness': _float_feature(f2),
        'Extraversion': _float_feature(f3),
        'Agreeableness': _float_feature(f4),
        'Neuroticism': _float_feature(f5),
        'genreName': _bytes_feature(f6),
    }

    # Create a Features message using tf.train.Example.
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


def compile_model(model):
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model


def demo(feat_column, train_ds_demo, print_res=True):
    example_batch = next(iter(train_ds_demo))[0]
    feat_layer = DenseFeatures(feat_column)
    if print_res:
        print(feat_layer(example_batch).numpy().shape)


def split_data(full_set, split_val=0.3):
    # split dataframe into training set, testing set, and validation set
    train, test = train_test_split(full_set, test_size=0.25)
    train, val = train_test_split(train, test_size=0.33)
    train, rebuild = train_test_split(train, test_size=0.01)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')
    return train, val, test, rebuild


def get_data_df(traits, genre_type, users=50, movies=10, num_cat=11, load_ts="", save=False):
    if load_ts:
        training_set = pd.read_csv(load_ts)
    else:
        training_set = build_training_set(users=users, movies=movies, num_bins=num_cat, save_file=save)

    training_set = training_set.loc[:, traits + [genre_type, 'BinProb']]

    if genre_type == "genreId":
        training_set = bin_traits(traits, training_set)

    # print(training_set)
    # print(training_set.columns)
    return training_set


def build_model(genres, traits, num_cat=10):
    """
    :param genres: list of genre names
    :param traits: list of personality trait names
    :param num_cat: int, number of categories for classification
    :return:
    """
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # load training set data
    # train, val, test = split_data(training_set)



    # create a small batch for test purposes prior to build
    # train_ds_demo = df_to_dataset(train, batch_size=5)

    # for feature_batch, label_batch in train_ds_demo.take(1):
    #     print('Every feature:', list(feature_batch.keys()))
    #     print('A batch of Openness:', feature_batch['Openness'])
    #     print('A batch of BinProbs:', label_batch)

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # build model features

    # create bucketized trait columns

    # create personality trait columns
    bounds = list(np.linspace(0, 100, 51))
    trait_buckets = []
    for trait in traits:
        trait_feat = feature_column.numeric_column(trait)
        bucketized_feat = feature_column.bucketized_column(trait_feat, boundaries=bounds)
        trait_buckets.append(bucketized_feat)

    # create categorical genre columns
    genre_feat = feature_column.categorical_column_with_vocabulary_list('genreName', genres)
    genre_one_hot = feature_column.indicator_column(genre_feat)

    feature_columns = trait_buckets + [genre_one_hot]
    feature_layer = DenseFeatures(feature_columns)
    model = tf.keras.Sequential([
                                  feature_layer,
                                  Dense(128, activation='relu'),
                                  Dense(128, activation='relu'),
                                  Dense(num_cat)
                                ])

    model = compile_model(model)

    return model


def plot_mod(history, ep):
    epochs = range(ep)

    plt.title('Accuracy')
    plt.plot(epochs, history.history['accuracy'], color='blue', label='Train')
    plt.plot(epochs, history.history['val_accuracy'], color='orange', label='Val')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    _ = plt.figure()
    plt.title('Loss')
    plt.plot(epochs, history.history['loss'], color='blue', label='Train')
    plt.plot(epochs, history.history['val_loss'], color='orange', label='Val')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()


def fit_model(training_set, model, save_model="", initialize=False):
    train, val, test, rebuild = split_data(training_set)

    batch_size = 32
    train_ds = df_to_dataset(train, batch_size=batch_size)
    val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    # if save_model:
    #     checkpoint_path = "training_1/cp.ckpt"
    #     # checkpoint_dir = os.path.dirname(checkpoint_path)
    #
    #     # Create a callback that saves the model's weights
    #     cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
    #                                                      save_weights_only=True,
    #                                                      verbose=1)
    #
    #     model.fit(train_ds, validation_data=val_ds, epochs=5, callbacks=[cp_callback])

    history = model.fit(train_ds, validation_data=val_ds, epochs=7)
    # plot_mod(history, 10)

    if save_model:
        model.save(save_model)

    loss, accuracy = model.evaluate(test_ds)
    print("\nAccuracy on build: ", accuracy)

    return model, rebuild


def build_model_new(training_set, num_cat=10, load_ts="", save_model=""):
    """
    :param genres: list of genre names
    :param traits: list of personality trait names
    :param num_cat: int, number of categories for classification
    :param load_ts: string of filepath, if you want to load training set from .csv (i.e. './trainingSet/MovieTraitTrainingSet.csv')
    :param save_model:
    :return:
    """
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # load training set data
    # training_set = training_set.iloc[:, 0:6].values.astype(np.float32)

    # train, val, test = split_data(training_set)

    train_feats = training_set.iloc[:, 0:6].values.astype(np.float32)
    # print(train_feats)
    # print(train_feats.shape)
    # print(type(train_feats))
    train_labels = np.array(training_set.iloc[:, 6].values)
    train_labels = train_labels.reshape((train_labels.shape[0], 1))
    # print(train_labels.shape)
    # print(type(train_labels))

    # test_feats = test.iloc[:, 0:6].values
    # test_labels = np.array(test.iloc[:, 6].values)
    # test_labels = test_labels.reshape((test_labels.shape[0], 1))


    # train model
    batch_size = 32
    # train_ds = df_to_dataset(train, batch_size=batch_size)
    # val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    # test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    # model = tf.keras.models.Sequential()
    # model.add(Dense(128, input_dim=6, activation='relu'))
    # model.add(Dense(128, activation='relu'))
    # model.add(Dense(num_cat))

    visible = Input(shape=(6,))
    hidden1 = Dense(128, activation='relu')(visible)
    hidden2 = Dense(128, activation='relu')(hidden1)
    final_layer = Dense(num_cat)(hidden2)
    model = Model(inputs=visible, outputs=final_layer)

    model = compile_model(model)
    model.fit(train_feats, train_labels, epochs=5, batch_size=batch_size)
    # loss, accuracy = model.evaluate(test_ds)
    # print("\nAccuracy on build: ", accuracy)

    if save_model:
        # serialize model to JSON
        model_json = model.to_json()

        with open("%s.json" % save_model, "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        model.save_weights("%s.h5" % save_model)
        print("Saved model to JSON.")
        # tf.keras.models.save_model(model, "/" + save_model)
        # model.save("./" + save_model)

    return model


if __name__ == "__main__":
    model_file = 'test_model/MovieTraitModel'
    build_mod = True
    if build_mod:
        training_df = get_data_df(model_traits, "genreName", users=10000, movies=400, num_cat=num_cats, save=True)
        live_model = build_model(model_genres, model_traits, num_cat=num_cats)
        live_model, rebuild_ds = fit_model(training_df, live_model, save_model=model_file)
        # rebuild_ds.to_csv('../application/server/MovieTraitModel/MovieTraitRebuild.csv')

        live_model.summary()
        original_weights = live_model.get_weights()

    if model_file:
        test_df = get_data_df(model_traits, "genreName", users=400, movies=400, num_cat=num_cats)
        retest_df, re_val, re_test, re_build = split_data(test_df)
        test_data_set = df_to_dataset(retest_df)
        loss, accuracy = live_model.evaluate(test_data_set)
        print("\nAccuracy on live model: ", accuracy)
        print("/////////////////////////////////////////////////////////////////////////////////////////////////")

        new_model = tf.keras.models.load_model(model_file)
        test_df = get_data_df(model_traits, "genreName", users=20, movies=20, num_cat=num_cats)
        test_data_set = df_to_dataset(test_df)
        loss, accuracy = new_model.evaluate(test_data_set)
        print("\nAccuracy on loaded model: ", accuracy)
        new_model.summary()
