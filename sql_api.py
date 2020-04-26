import pandas as pd
from urllib import parse
import requests
import json
# from application.server.handle import *


# Status Code 500 - Error in SQL query or error in connecting to database
# Status Code 404 - Error connecting to URL
# Status Code 200 - Successful connection and query


def json_api_query(api, json_data):

    query_str = json.dumps(json_data)
    encoded_query = parse.quote(query_str)
    # print(encoded_query)
    # print(parse.unquote(encoded_query))
    route = "http://cs411ccsquad.web.illinois.edu/%s/%s" % (api, encoded_query)
    # print(route)
    response = requests.get(route)

    queried_data_df = pd.DataFrame()
    if response.status_code == 200:
        queried_data_json = response.json()
        # print(queried_data_json['data'])
        queried_data_df = pd.DataFrame(queried_data_json['data'])
        # print(queried_data_df)
    return queried_data_df, response.status_code


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

    query = """SELECT Movie.tconst, Movie.title, Movie.year, Movie.rating,
                 GROUP_CONCAT(DISTINCT Genre.genreName ORDER BY Genre.genreName DESC) AS genres,
               GROUP_CONCAT(DISTINCT People.name ORDER BY People.name DESC) AS crew
                FROM Movie
                 LEFT JOIN MovieCategory ON Movie.tconst = MovieCategory.tconst
                 LEFT JOIN Genre ON MovieCategory.genreId = Genre.genreId
                 LEFT JOIN Crew ON Movie.tconst = Crew.tconst
                 LEFT JOIN People ON Crew.nconst = People.nconst
                WHERE title LIKE '%%Bulldog Heaven%%'
                GROUP BY Movie.tconst
                 LIMIT 100"""
    print("\nQuery:\n%s" % query)
    df, code = api_query(query)
    print("Status Code: %d" % code)
    print(df)

    # //////////////////////////////////////////////////////////////////////////////////////////////
    # json_dict = {'title': {'value': 'ca', 'operator': 'LIKE'},
    #              'year': {'value': '2005', 'operator': '='},
    #              'rating': {'value': '', 'operator': '>='}}
    # query = build_movie_query(json_dict)
    # print("\nQuery:\n%s" % query)
    # df, code = json_api_query('Movies', json_dict)
    # print("Status Code: %d" % code)
    # print(df)

    # //////////////////////////////////////////////////////////////////////////////////////////////
    # json_dict = {
    #               'cocktailName': {'value': 'a', 'operator': 'LIKE'},
    #               'ingredients': {'value': '', 'operator': 'LIKE'},
    #               'bartender': {'value': 'raul', 'operator': 'LIKE'},
    #               'location': {'value': '', 'operator': 'LIKE'},
    #               'rating': {'value': '', 'operator': '>='}
    #             }
    # query = build_cocktail_query(json_dict)
    # print("\nQuery:\n%s" % query)
    # df, code = json_api_query('Cocktails', json_dict)
    # print("Status Code: %d" % code)
    # print(df)






