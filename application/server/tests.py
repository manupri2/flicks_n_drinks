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
    # test_dict = {'userId': 0, 'tConst': []}
    # test_res = run_json_api_test("MTNN", test_dict)
    #
    # test_dict = {'userId': [1], 'tConst': []}
    # test_res = run_json_api_test("MTNN", test_dict)
    #
    # test_dict = {'userId': [0], 'tConst': [24, 28, 31]}
    # test_res = run_json_api_test("MTNN", test_dict)

    test_dict = {'userId': [0, 1], 'tConst': []}
    test_res = run_json_api_test("MTNN", test_dict)
    json_str = test_res.to_json(orient="records")
    json_rec = test_res.to_dict(orient="records")

    print(json_str)
    print(json_rec)
    print(type(json_rec))


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
    json_dict = {'title': {'value': '', 'operator': 'LIKE'},
                 'year': {'value': '2000', 'operator': '='},
                 'rating': {'value': '', 'operator': '>='}}
    table = "Movies"

    # run test on the query used in API
    # query = build_general_read_query(table[:-1], json_dict, "AND")
    # remote_test_read_query(query)

    # run test on actual API without "userId"
    api = "read/" + table
    # res = run_json_api_test(api, json_dict)
    # print(res.columns)

    # run test on actual API with "userId"
    json_dict["userId"] = 1
    res = run_json_api_test(api, json_dict)
    print(res.columns)
    # print(res)
    print(res.loc[:, ["personalRating", "crew"]])
    print(res.loc[:, ["personalRating", "genres"]])
    print(res.loc[:, ["personalRating", "ratesMovie"]])


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
    query = build_general_read_query(table[:-1], json_dict, "AND")
    remote_test_read_query(query)


def test_signup():

    max_id_query = 'SELECT MAX(userId) as max FROM User'
    result = remote_test_read_query(max_id_query)
    # result, message = query_data(max_id_query, conn, 'df')
    max_id = result['max'][0] + 1
    new_input = '%7B%22firstName%22:%22Mjghga%22,%22lastName%22:%22Arbnbora%22,%22emailId%22:%22mari2@illinois.edu%22,%22password%22:%22password%22%7D'
    json_dict = json.loads(parse.unquote(new_input))
    query = "INSERT INTO User (userId, firstName, lastName, emailId, password, trOpen, trCon, trex, trAg, trNe)" \
            " VALUES (%s, %s, %s, %s, %s, 0, 0, 0, 0, 0)" % (max_id, '"'+json_dict['firstName']+'"', '"'+json_dict['lastName']+'"',
                                                             '"'+json_dict['emailId']+'"', '"'+json_dict['password']+'"')
    result1 = remote_test_read_query(query)
    print('User query: %s and Result: %s' % (query,result1))


def test_crud():

    return


def test_read_api_real():
    json_dict = {'userId': 0}
    run_json_api_test("read/User", json_dict)


def test_basic_api():
    json_dict = {}
    run_json_api_test("BasicDF", json_dict)


def new_add():
    api = "add/Movie"
    json_dict = {'title': "Bulldog Heaven Tres Perros",
                 'year': 2020}
    json_api_query(api, json_dict)

    # api = "add/User"
    # json_dict = {'firstName': 'Billy',
    #              'lastName': 'Fresco',
    #              'emailId': 'frescoFresh2@billy.com',
    #              'password': 'test'}
    #
    # json_api_query(api, json_dict)


def test_vote_print_state(json_dict, vote_table, vote_col, state):
    match_filters = preformat_filter_dict(json_dict, "=")
    new_val_filter = {vote_col: match_filters.pop(vote_col)}

    user_filter = {"userId": match_filters["userId"]}
    mov_filter = {"tConst": match_filters["tConst"]}
    check_mov_query = build_general_read_query("Movie", mov_filter, "AND")
    check_vote_query = build_general_read_query(vote_table, user_filter, "AND")

    check_df, message = api_query(check_mov_query)
    print("\nState: %s" % state)
    print(check_df.loc[:, ['tConst', 'rating', 'votes']])
    check_df, message = api_query(check_vote_query)
    print(check_df)
    print()


def test_vote():
    vote_table = "FavoriteMovie"
    vote_col = "ratesMovie"
    json_dict = {"userId": 1, "tConst": 40, "ratesMovie": 10}
    print(json_dict)

    test_vote_print_state(json_dict, vote_table, vote_col, "Before")
    # handle_vote(vote_table, vote_col, json_dict, "conn")
    json_api_query("vote/Movie", json_dict)
    test_vote_print_state(json_dict, vote_table, vote_col, "After")


def test_cocktail_print_state(json_dict, cols, state):
    # cols = list(json_dict.keys())

    match_filters = preformat_filter_dict(json_dict, "=")

    check_query = build_general_read_query("CocktailSummary", match_filters, "AND")
    # print(check_query)
    check_df, message = api_query(check_query)
    print("\nState: %s" % state)
    print(message)
    if check_df.empty:
        print(check_df)
    else:
        print(check_df.loc[:, cols])
    print()


def test_cocktail_add():
    json_dict = {
                  'cocktailName': "New Cocktail Name",
                  'bartender': "Billy Joe",
                  'location': "Chicago",
                  'glasswareName': "Beer Mug"
                 }
    disp_col = list(json_dict.keys())
    match_dict = json_dict.copy()
    match_dict.pop('glasswareName')
    match_dict.pop('cocktailName')
    keys, vals = json_to_cs_str(json_dict)


    test_cocktail_print_state(match_dict, disp_col, "Before")
    # json_api_query("add/Cocktail", json_dict)
    # remote_test_read_query(build_add_recipe_compound(json_dict))
    # prep_query = "PREPARE "
    test_query = "CALL AddCocktailProcedure(%s);" % vals
    # test_query = "EXECUTE PreparedCocktail USING %s;" % vals
    # test_query = """
    #                 SET @v1 = 'WilbucoCHEEEyyahhhTHISITBOI';
    #                 SET @v2 = 'Wilbur';
    #                 SET @v3 = 'Chicago';
    #                 SET @v4 = 'Billys ChalaceBOII';
    #
    #                 PREPARE s FROM 'CALL AddCocktailProcedure(?, ?, ?, ?)';
    #                 EXECUTE s USING @v1, @v2, @v3, @v4;
    #
    #             """
    remote_test_read_query(test_query)
    test_cocktail_print_state(match_dict, disp_col, "After")


def test_edit_movie():
    json_dict = {'tConst': 0,
                'title': 'NewTitle',
                 'year': 2020}
    table = "Movie"
    query = build_update_query(table, json_dict, 'tConst')
    print(query)


def test_user_autocomplete():
    json_dict = {'userId': 1, 'firstName': 'o', 'lastName': 'hu', 'emailId': ''}
    query = build_user_autocomplete(json_dict)
    remote_test_read_query(query)

    json_dict = {'userId': 1, 'firstName': 'o', 'lastName': 'hu', 'emailId': ''}
    api = "read/UserAuto"
    run_json_api_test(api, json_dict)


def test_add_movie():
    json_dict = {'tConst': 0,
                 'genre': 2}

    # handle_add_movie(json_dict, "test")

    genre_query = build_insert_query("MovieCategory", json_dict)
    print(genre_query)

if __name__ == "__main__":
    test_add_movie()


