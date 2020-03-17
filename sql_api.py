import pandas as pd
from urllib import parse
import requests


# if there is an error in SQL query it will return error code 500
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
        # print(queried_data_json)
        queried_data_df = pd.DataFrame(queried_data_json)
        # print(queried_data_df)
    return queried_data_df, response.status_code


def test_df(tables):
    for table in tables:
        test_query = "SELECT * FROM %s" % table
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
    test_df(table_list)

    query = 'SELECT * FROM Composition WHERE compositionId > 5 AND compositionId < 100'
    print("\nQuery:\n%s" % query)
    df, code = api_query(query)
    print("Status Code:%d" % code)
    print(df)

    query = 'SELECT * FROM People WHERE name LIKE "%%Ast%%" LIMIT 10'
    print("\nQuery:\n%s" % query)
    df, code = api_query(query)
    print("Status Code: %d" % code)
    print(df)



