from io import StringIO
import csv
import pandas as pd
import re
from urllib import parse
import requests
from sql_api import api_query


# movie_trait_matrix = pd.read_csv('./static/MovieTraitMatrix.csv')
# cocktail_raw['recipeId'] = range(0, cocktail_raw.shape[0])
# categorized_ing.set_index('word', inplace=True)


query = 'SELECT * FROM Composition WHERE compositionId > 5 AND compositionId < 100'
df, code = api_query(query)
print(code)
print(df)


query = 'SELECT * FROM People WHERE name LIKE "%%Ast%%" LIMIT 10'
df, code = api_query(query)
print(code)
print(df)