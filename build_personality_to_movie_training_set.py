from io import StringIO
import csv
import pandas as pd
import re
from urllib import parse
import requests


movie_trait_matrix = pd.read_csv('./static/MovieTraitMatrix.csv')
# cocktail_raw['recipeId'] = range(0, cocktail_raw.shape[0])
# categorized_ing.set_index('word', inplace=True)


test_query = '/API_SQL/' + "SELECT * FROM CocktailName"
encoded_query = parse.quote(test_query)
print(encoded_query)
response = requests.get("http://cs411ccsquad.web.illinois.edu/API_SQL/%s" % encoded_query)
print(response)
