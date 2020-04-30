from application.server.handle import *
from application.server.MovieTraitNetwork import *
from DataManipulation.build_NN_training_set import build_training_set
import json
from urllib import parse
from flask import jsonify
import pandas as pd
from sql_api import remote_test_read_query, json_api_query
import os
import requests


def test_mtnn_api_functions():
    test_mod, blah = load_model()

    test_dict = {'userId': 0, 'tConst': []}
    test_res = mtnn_run_test(test_dict, test_mod)

    test_dict = {'userId': [1], 'tConst': []}
    test_res = mtnn_run_test(test_dict, test_mod)

    test_dict = {'userId': [0], 'tConst': [24, 28, 31]}
    test_res = mtnn_run_test(test_dict, test_mod)

    test_dict = {'userId': [0, 1], 'tConst': [24, 28, 31]}
    test_res = mtnn_run_test(test_dict, test_mod)


def test_mtnn_api_real():
    # test_mod, blah = load_model()

    test_dict = {'userId': 0, 'tConst': []}
    test_res = mtnn_run_test_real(test_dict)

    test_dict = {'userId': [1], 'tConst': []}
    test_res = mtnn_run_test_real(test_dict)

    test_dict = {'userId': [0], 'tConst': [24, 28, 31]}
    test_res = mtnn_run_test_real(test_dict)

    test_dict = {'userId': [0, 1], 'tConst': [24, 28, 31]}
    test_res = mtnn_run_test_real(test_dict)


def mtnn_run_test_real(json_dict):
    # test_json = json.dumps(json_dict)
    # json_uri = parse.quote(test_json)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("JSON Input:")
    print(json_dict)
    resp_json, code = json_api_query("MTNN", json_dict)
    print(resp_json)
    # result_dict = json.loads(resp_json.json())
    result_df = pd.DataFrame(resp_json)
    print("\nMovieTrait Results::")
    print(result_df)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    return result_df


def mtnn_run_test(json_dict, model):
    # test_json = json.dumps(json_dict)
    # json_uri = parse.quote(test_json)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("JSON Input:")
    print(json_dict)
    result_df = handle_mtnn_api(json_dict, model, 'test')
    # result_dict = json.loads(result_json)
    # result_df = pd.DataFrame(result_dict)
    print("\nMovieTrait Results::")
    print(result_df)
    print(type(result_df.to_json(orient="records")))
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    return result_df


def test_distribution():
    test_mod = load_model()
    test_df = build_training_set(users=1000, movies=200, num_bins=5, group_by_movie=False, save_file=False)
    test_df['compat'] = see_mtnn(test_df, test_mod)
    test_df.to_csv('./MovieTraitModel/test_out/test_distribution.csv')


def test_user_read_api():
    json_dict = {'userId': 0}
    query = build_user_query(json_dict)
    remote_test_read_query(query)

    json_dict = {'userId': [0, 1]}
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


def basic_df():
    resp_json, code = json_api_query("BasicDF", {})
    print(resp_json)
    # result_dict = json.loads(resp_json)
    result_df = pd.DataFrame(resp_json)
    print("\nMovieTrait Results::")
    print(result_df)


if __name__ == "__main__":
    test_mtnn_api_real()


