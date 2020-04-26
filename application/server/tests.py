from application.server.handle import *
from DataManipulation.build_NN_training_set import build_training_set
import json
from urllib import parse
from flask import jsonify
import pandas as pd
from sql_api import remote_test_read_query
import os


def test_nn():
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


def test_user_read_api():
    json_dict = {'userId': 0}
    query = build_user_query(json_dict)
    remote_test_read_query(query)

    json_dict = {'userId': [0, 3, 5]}
    query = build_user_query(json_dict)
    remote_test_read_query(query)

    json_dict = {'emailId': "ohuang2@illinois.edu"}
    query = build_user_query(json_dict)
    remote_test_read_query(query)


def test_movie_read_api():
    json_dict = {'title': {'value': 'ca', 'operator': 'LIKE'},
                 'year': {'value': '2005', 'operator': '='},
                 'rating': {'value': '', 'operator': '>='}}
    query = build_movie_query(json_dict)
    remote_test_read_query(query)


def test_cocktail_read_api():
    json_dict = {
                  'cocktailName': {'value': 'a', 'operator': 'LIKE'},
                  'ingredients': {'value': '', 'operator': 'LIKE'},
                  'bartender': {'value': 'raul', 'operator': 'LIKE'},
                  'location': {'value': '', 'operator': 'LIKE'},
                  'rating': {'value': '', 'operator': '>='}
                }
    query = build_cocktail_query(json_dict)
    remote_test_read_query(query)


def test_crud():

    return


if __name__ == "__main__":
    test_user_read_api()


