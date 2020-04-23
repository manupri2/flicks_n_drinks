import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras.layers import Input, Dense, DenseFeatures
from tensorflow.keras.models import model_from_json, Model
from sklearn.model_selection import train_test_split
from sql_api import api_query
from DataManipulation.build_NN_training_set import *
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from DataManipulation.BuildModel import get_data_df, df_to_dataset, model_traits, num_cats


def get_model():
    model_file = './MovieTraitModel'
    mt_model = tf.keras.models.load_model(model_file)

    rebuild_df = pd.read_csv('./MovieTraitModel/MovieTraitRebuild.csv')
    rebuild_ds = df_to_dataset(rebuild_df)

    loss, accuracy = mt_model.evaluate(rebuild_ds)
    print("\nAccuracy on loaded model: ", accuracy)

    return mt_model


if __name__ == "__main__":
    new_mod = get_model()
    new_mod.summary()
