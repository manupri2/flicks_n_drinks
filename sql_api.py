import pandas as pd
from urllib import parse
import requests
import json
from flask import jsonify


# Status Code 500 - Error in SQL query or error in connecting to database
# Status Code 404 - Error connecting to URL
# Status Code 200 - Successful connection and query


def json_api_query(api, json_data):

    encoded_query = ""
    if json_data:
        query_str = json.dumps(json_data)
        encoded_query = parse.quote(query_str)
    # print(encoded_query)
    # print(parse.unquote(encoded_query))
    route = "http://cs411ccsquad.web.illinois.edu/" + api

    if encoded_query:
        route += "/" + encoded_query

    print(route)
    response = requests.get(route)
    print("Status code: %d" % response.status_code)
    return response.json(), response.status_code


def api_query(query_str):
    encoded_query = parse.quote(query_str)
    # print(encoded_query)
    # print(parse.unquote(encoded_query))
    route = "http://cs411ccsquad.web.illinois.edu/api/%s" % encoded_query
    # print(route)
    response = requests.get(route)

    queried_data_df = pd.DataFrame()
    if response.status_code == 200:
        queried_data_json = response.json()
        # print(queried_data_json['data'])
        queried_data_df = pd.DataFrame(queried_data_json['data'])
        # print(queried_data_df)
    return queried_data_df, response.status_code


def test_database_tables(tables):
    for table in tables:
        test_query = "SELECT * FROM %s LIMIT 10000" % table
        test_df, code = api_query(test_query)
        if code == 200:
            print('Table %s was a success!' % table)
        else:
            print('Table %s was a fail!' % table)


def remote_test_read_query(test_query):
    """This is the general API for the REMOTE testing of any read query (testing from your machine w/o the need to push)
       The server must be running for this to work"""
    print("//////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("Query:\n%s" % test_query)
    df, code = api_query(test_query)
    print("Status Code: %d" % code)
    print("Query Results:")
    print(df)
    print("//////////////////////////////////////////////////////////////////////////////////////////////////////////")
    return df


def run_json_api_test(api, json_dict):
    # test_json = json.dumps(json_dict)
    # json_uri = parse.quote(test_json)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("JSON Input:")
    print(json_dict)
    resp_json, code = json_api_query(api, json_dict)
    result_df = pd.DataFrame(resp_json['data'])
    print("\nResults:")
    print(result_df)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
    return result_df


if __name__ == "__main__":
    table_list = ['CocktailDecoration',
    'CocktailName',
    'CocktailRecipe',
    'Composition',
    'Connection',
    'Crew',
    'FavoriteCocktail',
    'FavoriteMovie',
    'FavoritePair',
    'Garnish',
    'Genre',
    'Glassware',
    'Ingredient',
    'IngredientClassification',
    'IngredientType',
    'Movie',
    'MovieCategory',
    'MovieCocktailPairing',
    'People',
    'Role',
    'User']
    # test_database_tables(table_list)
    # //////////////////////////////////////////////////////////////////////////////////////////////
    json_dict = {'emailId': "ohuang2@illinois.edu"}
    user_email = json_dict['emailId']

    query = "SELECT * FROM CocktailRecipe"
    remote_test_read_query(query)







