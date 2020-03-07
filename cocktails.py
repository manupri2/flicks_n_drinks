from io import StringIO
import csv
import pandas as pd
import re


cocktail_raw = pd.read_csv('./static/hotaling_cocktails.csv')
cocktail_raw['recipeId'] = range(0, cocktail_raw.shape[0])
categorized_ing = pd.read_csv('./static/words_cat.csv')
categorized_ing.set_index('word', inplace=True)
units = list(pd.read_csv('./static/units.csv').values)


def set_type(ingr_name):
    ing_types = []
    for kword in list(categorized_ing.index.values):
        if re.search(kword, ingr_name, flags=re.IGNORECASE):
            ing_types = list(set(ing_types + list(categorized_ing.loc[kword, :].dropna().values)))
    return ing_types


def search_type(ing_word):
    if ing_word in list(categorized_ing.index.values):
        return list(categorized_ing.loc[ing_word, :].dropna().values)
    else:
        return []


def explode_csv_col(csv_string, delim=', '):
    if isinstance(csv_string, str):
        return csv_string.split(delim)
    else:
        return []


def reduce_col_of_list_to_col(orig_col, drop_na=True):
    temp = pd.DataFrame(orig_col.tolist())
    new_df = pd.DataFrame()
    for col in temp.columns:
        new_df = pd.concat([new_df, temp[col]])
        if drop_na:
            new_df = new_df.dropna()
    return new_df


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# setup Composition table

ing_dict = {}
# loop through each tuple
for i in range(0, cocktail_raw.shape[0]):
    ing_list = []
    ing_string = cocktail_raw.loc[i, 'Ingredients']
    ing_string = re.sub(r'\*', '', ing_string, flags=re.IGNORECASE)
    # f = StringIO(ing_string)
    # ingredients = csv.reader(f, delimiter=',')
    ingredients = ing_string.split(', ')

    for ingred in ingredients:
        f2 = StringIO(ingred)
        ing_comp = csv.reader(f2, delimiter=' ')

        comp_list = []
        for comp in ing_comp:
            while '' in comp:
                comp.pop(comp.index(''))
            ing_list.append(comp)
    ing_dict[i] = ing_list

idx = ['recipeId', 'quantity', 'unit', 'ingredientName']
composition = pd.DataFrame(columns=idx)
all_words = []
for recipe_id, ingredients in ing_dict.items():
    for ingredient in ingredients:
        temp = []
        quantity = None
        unit = None

        if re.findall('[0-9]', ingredient[0]):
            quantity = ingredient.pop(0)
            if ingredient:
                if ingredient[0] in units:
                    unit = ingredient.pop(0)

        ing_name = ''
        for word in ingredient:
            if len(ing_name) > 0:
                ing_name += ' '
            ing_name += word

            # save indiviual words to map ingredientType to specific keywords
            new_word = re.sub(r'[()]', '', word, flags=re.IGNORECASE).lower()
            all_words.append(new_word)

        ing_item = [recipe_id, quantity, unit, ing_name]
        ing_tuple = dict(zip(idx, ing_item))
        # print(ing_tuple)
        composition = composition.append(ing_tuple, ignore_index=True)

words = pd.DataFrame(sorted(list(set(all_words))), columns=['word'])
words['categories'] = words.loc[:, 'word'].apply(search_type)

composition['compositionId'] = range(0, composition.shape[0])
composition.set_index(['compositionId'], drop=True, inplace=True)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# setup IngredientClassification and IngredientType tables

temp = composition['ingredientName'].apply(set_type)
ingredient_class = reduce_col_of_list_to_col(temp)
ingredient_class['iClassificationId'] = range(0, ingredient_class.shape[0])
ingredient_class.reset_index(inplace=True)
ingredient_class.columns = ['ingredientId', 'ingredientTypeName', 'iClassificationId']
ingredient_class.set_index(['iClassificationId'], drop=True, inplace=True)

ingredient_type = pd.DataFrame(list(set(list(ingredient_class['ingredientTypeName'].values))), columns=['ingredientTypeName'])
ingredient_type['ingredientTypeId'] = range(0, ingredient_type.shape[0])
ingredient_type.set_index(['ingredientTypeName'], drop=False, inplace=True)

ingredient_class.loc[:, 'ingredientTypeName'] = ingredient_class.loc[:, 'ingredientTypeName'].apply(lambda x: ingredient_type.loc[x, 'ingredientTypeId'])
ingredient_class.columns = ['ingredientId', 'ingredientTypeId']

ingredient_type.set_index(['ingredientTypeId'], drop=True, inplace=True)

# print(ingredient_class)
# print(ingredient_type)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# setup Ingredient table
ingredient_df = pd.DataFrame(list(set(list(composition['ingredientName'].values))), columns=['ingredientName'])
ingredient_df['ingredientId'] = range(0, ingredient_df.shape[0])
ingredient_df.set_index(['ingredientName'], drop=False, inplace=True)

composition.loc[:, 'ingredientName'] = composition.loc[:, 'ingredientName'].apply(lambda x: ingredient_df.loc[x, 'ingredientId'])
composition.columns = ['recipeId', 'quantity', 'unit', 'ingredientId']

ingredient_df.set_index(['ingredientId'], drop=True, inplace=True)

# print(ingredient_df)
# print(composition)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# setup CocktailDecoration and Garnish Tables

cocktail_dec = cocktail_raw.loc[:, ['recipeId', 'Garnish']].copy()
cocktail_dec = cocktail_dec['Garnish'].apply(explode_csv_col)
cocktail_dec = reduce_col_of_list_to_col(cocktail_dec)
cocktail_dec['decorationId'] = range(0, cocktail_dec.shape[0])
cocktail_dec.reset_index(inplace=True)
cocktail_dec.columns = ['recipeId', 'garnishName', 'decorationId']
cocktail_dec.set_index(['decorationId'], drop=True, inplace=True)

garnish = pd.DataFrame(list(set(list(cocktail_dec['garnishName'].values))), columns=['garnishName'])
garnish['garnishId'] = range(0, garnish.shape[0])
garnish.set_index(['garnishName'], drop=False, inplace=True)

cocktail_dec.loc[:, 'garnishName'] = cocktail_dec.loc[:, 'garnishName'].apply(lambda x: garnish.loc[x, 'garnishId'])
cocktail_dec.columns = ['recipeId', 'garnishId']

garnish.set_index(['garnishId'], drop=True, inplace=True)

# print(garnish)
# print(cocktail_dec)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# setup CocktailRecipe, CocktailName, Glassware tables

cocktail_recipe = cocktail_raw.loc[:, ['recipeId', 'Cocktail Name', 'Bartender', 'Bar/Company', 'Location', 'Glassware', 'Preparation']].copy()
cocktail_recipe.columns = ['recipeId', 'cocktailName', 'bartender', 'company', 'location', 'glasswareName', 'instruction']
cocktail_recipe['votes'] = 0
cocktail_recipe['rating'] = 0
cocktail_recipe.set_index(['recipeId'], drop=True, inplace=True)

cocktail_name = pd.DataFrame(list(set(list(cocktail_recipe['cocktailName'].values))), columns=['cocktailName'])
cocktail_name['cocktailId'] = range(0, cocktail_name.shape[0])
cocktail_name.set_index(['cocktailName'], drop=False, inplace=True)

cocktail_recipe.loc[:, 'cocktailName'] = cocktail_recipe.loc[:, 'cocktailName'].apply(lambda x: cocktail_name.loc[x, 'cocktailId'])
cocktail_recipe.columns = ['cocktailId', 'bartender', 'company', 'location', 'glasswareName', 'instruction', 'votes', 'rating']

cocktail_name.set_index(['cocktailId'], drop=True, inplace=True)

# print(cocktail_name)
# print(cocktail_recipe)

glassware = pd.DataFrame(list(set(list(cocktail_recipe['glasswareName'].values))), columns=['glasswareName'])
glassware['glasswareId'] = range(0, glassware.shape[0])
glassware.set_index(['glasswareName'], drop=False, inplace=True)

cocktail_recipe.loc[:, 'glasswareName'] = cocktail_recipe.loc[:, 'glasswareName'].apply(lambda x: glassware.loc[x, 'glasswareId'])
cocktail_recipe.columns = ['cocktailId', 'bartender', 'company', 'location', 'glasswareId', 'instruction', 'votes', 'rating']

glassware.set_index(['glasswareId'], drop=True, inplace=True)

# print(glassware)
# print(cocktail_recipe)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# export each table to their own .csv file
cocktail_name.to_csv('./CocktailDataTables/CocktailName.csv')
cocktail_recipe.to_csv('./CocktailDataTables/CocktailRecipe.csv')
glassware.to_csv('./CocktailDataTables/Glassware.csv')
ingredient_df.to_csv('./CocktailDataTables/Ingredient.csv')
composition.to_csv('./CocktailDataTables/Composition.csv')
ingredient_type.to_csv('./CocktailDataTables/IngredientType.csv')
ingredient_class.to_csv('./CocktailDataTables/IngredientClassification.csv')
garnish.to_csv('./CocktailDataTables/Garnish.csv')
cocktail_dec.to_csv('./CocktailDataTables/CocktailDecoration.csv')

words.to_csv('./CocktailDataTables/words.csv')
