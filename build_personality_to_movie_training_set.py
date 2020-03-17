from io import StringIO
import csv
import pandas as pd
import re
from urllib import parse
import requests


movie_trait_matrix = pd.read_csv('./static/MovieTraitMatrix.csv')
# cocktail_raw['recipeId'] = range(0, cocktail_raw.shape[0])
# categorized_ing.set_index('word', inplace=True)


test_query = "SELECT * FROM CocktailName"
encoded_query = parse.quote(test_query)
print(encoded_query)
print(parse.unquote(encoded_query))
route = "http://cs411ccsquad.web.illinois.edu/API_SQL/%s" % encoded_query
print(route)
response = requests.get(route)
print(response)
