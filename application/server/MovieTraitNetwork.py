import numpy as np
import pandas as pd
import tensorflow as tf
from DataManipulation.BuildModel import df_to_dataset


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
