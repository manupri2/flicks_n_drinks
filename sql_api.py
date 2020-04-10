import pandas as pd
from urllib import parse
import requests
from application.server.handle import *


# Status Code 500 - Error in SQL query or error in connecting to database
# Status Code 404 - Error connecting to URL
# Status Code 200 - Successful connection and query


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
        print(queried_data_json['data'])
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

    # query = 'SELECT * FROM Movie WHERE title LIKE "%%ca%%"'
    # print("\nQuery:\n%s" % query)
    # df, code = api_query(query)
    # print("Status Code: %d" % code)
    # print(df)
    #
    # query = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'cs411ccsquad_FlicksNDrinks'"
    # print("\nQuery:\n%s" % query)
    # df, code = api_query(query)
    # print("Status Code: %d" % code)
    # table_schema = {}
    # print(df)

    json_dict = {'year': "", 'rating': "", "title": "dude"}
    query = build_movie_query(json_dict)
    print("\nQuery:\n%s" % query)
    df, code = api_query(query)
    print("Status Code: %d" % code)
    table_schema = {}
    print(df)
    print(df['title'])





