from application.server.handle import *
from DataManipulation.build_NN_training_set import build_training_set
import json
from urllib import parse
from flask import jsonify
import pandas as pd
import sql_api
import os


def test_mtnn_api(json_dict, model):
    # test_json = json.dumps(json_dict)
    # json_uri = parse.quote(test_json)
    result_json = handle_mtnn_api(json_dict, model, 'test')
    result_dict = json.loads(result_json)
    result_df = pd.DataFrame(result_dict)
    return result_df


def test_distribution(model):
    test_df = build_training_set(users=1000, movies=200, num_bins=5, group_by_movie=False, save_file=False)
    test_df['compat'] = see_mtnn(test_df, model)
    test_df.to_csv('./MovieTraitModel/test_out/test_distribution.csv')


if __name__ == "__main__":
    test_mod = load_model()
    test_dict = {
                'Openness': 2.0,
                'Conscientiousness': 66.0,
                'Extraversion': 25.0,
                'Agreeableness': 50.0,
                'Neuroticism': 2.0,
                'tConst': []
                }
    test_res = test_mtnn_api(test_dict, test_mod)
    print(test_res)

    test_dict['tConst'] = [24, 28, 31]
    test_res = test_mtnn_api(test_dict, test_mod)
    print(test_res)

    test_distribution(test_mod)


