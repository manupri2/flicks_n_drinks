from application.server.handle import *
from application.server.MovieTraitNetwork import *
from DataManipulation.build_NN_training_set import build_training_set
import json
from urllib import parse
from flask import jsonify
import pandas as pd
from sql_api import remote_test_read_query, json_api_query, api_query, run_json_api_test
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
    test_dict = {'userId': 0, 'tConst': []}
    test_res = run_json_api_test("MTNN", test_dict)

    test_dict = {'userId': [1], 'tConst': []}
    test_res = run_json_api_test("MTNN", test_dict)

    test_dict = {'userId': [0], 'tConst': [24, 28, 31]}
    test_res = run_json_api_test("MTNN", test_dict)

    test_dict = {'userId': [0, 1], 'tConst': [24, 28, 31]}
    test_res = run_json_api_test("MTNN", test_dict)


def mtnn_run_test(json_dict, model):
    # test_json = json.dumps(json_dict)
    # json_uri = parse.quote(test_json)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("JSON Input:")
    print(json_dict)

    tconst_list = json_dict.pop('tConst')
    genre_query = build_genres_query(tconst_list)

    user_info_df, code = api_query(build_user_query(json_dict))
    genre_df, code = api_query(genre_query)
    result_df = handle_mtnn_api(model, user_info_df, genre_df, tconst_list)

    print("\nMovieTrait Results:")
    print(result_df)
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
    # query = build_movie_query(json_dict)
    # remote_test_read_query(query)

    # json_dict = {}
    table = "Movies"
    query = build_read_query_from_view(table[:-1], json_dict)
    remote_test_read_query(query)


def test_cocktail_read_api():
    json_dict = {
                  'cocktailName': {'value': 'a', 'operator': 'LIKE'},
                  'ingredients': {'value': '', 'operator': 'LIKE'},
                  'bartender': {'value': 'raul', 'operator': 'LIKE'},
                  'location': {'value': '', 'operator': 'LIKE'},
                  'rating': {'value': '', 'operator': '>='}
                }
    # query = build_cocktail_query(json_dict)
    # remote_test_read_query(query)

    table = "Cocktails"
    query = build_read_query_from_view(table[:-1], json_dict)
    remote_test_read_query(query)


def test_crud():

    return


def test_read_api_real():
    json_dict = {'userId': 0}
    run_json_api_test("read/User", json_dict)


def test_basic_api():
    json_dict = {}
    run_json_api_test("BasicDF", json_dict)


if __name__ == "__main__":
    test_cocktail_read_api()


