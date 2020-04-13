from flask import jsonify


# use sql_api.py for testing

def build_filters(filter_dict):
    """
    This function takes a dictionary of filters where each filter stores a dictionary containing the filter value and
    SQL operator to be used on the filter.
    :param filter_dict: dictionary of filters { filterX: { value: "filterX_value", operator: "filterX_operator" }, ...}
    :return: list of filters formatted for SQL WHERE clause
    """
    filter_strs = []
    for (filterX, options) in filter_dict.items():
        filter_val = options['value']
        operator = options['operator']

        if filter_val:
            if operator == 'LIKE':
                filter_val = "'%%" + filter_val + "%%'"
            filter_strs.append(filterX + " " + operator + " " + filter_val)

    return filter_strs


def build_where_and(filter_strs):
    """
    This function builds the WHERE clause string from a list of filters' strings which have been preformmated for the
    SQL WHERE clause. This assumes all filters in the list have an AND relations
    :param filter_strs: list of preformatted filter strings ["location LIKE %%Los Angeles%%", "rating >= 5"]
    :return: complete, formatted WHERE clause string to be concatenated into SQL query
    """
    where_str = ""
    if filter_strs:
        where_str += "WHERE " + filter_strs[0] + "\n"

        if len(filter_strs) > 1:
            for f in filter_strs[1:]:
                where_str += " AND " + f + "\n"
    return where_str


def build_cocktail_query(json_dict):
    query = "SELECT CocktailRecipe.recipeId, CocktailRecipe.bartender, CocktailRecipe.location,\n" \
            " CocktailRecipe.rating, CocktailName.cocktailName,\n" \
            " GROUP_CONCAT(DISTINCT Ingredient.ingredientName ORDER BY Ingredient.ingredientName DESC) AS ingredients\n" \
            "FROM CocktailRecipe\n" \
            " FULL OUTER JOIN Composition ON CocktailRecipe.recipeId = Composition.recipeId\n" \
            " FULL OUTER JOIN Ingredient ON Composition.ingredientId = Ingredient.ingredientId\n" \
            " FULL OUTER JOIN CocktailName ON CocktailRecipe.cocktailId = CocktailName.cocktailId\n"

    filter_str = build_filters(json_dict)
    where_clause_str = build_where_and(filter_str)
    query += where_clause_str
    query += "GROUP BY CocktailRecipe.recipeId\n" \
             "LIMIT 100\n"
    return query


def build_movie_query(json_dict):
    query = "SELECT Movie.tconst, Movie.title, Movie.year, Movie.rating,\n" \
            " GROUP_CONCAT(DISTINCT Genre.genreName ORDER BY Genre.genreName DESC) AS genres,\n" \
            " GROUP_CONCAT(DISTINCT People.name ORDER BY People.name DESC) AS crew\n" \
            "FROM Movie\n" \
            " FULL OUTER JOIN MovieCategory ON Movie.tconst = MovieCategory.tconst\n" \
            " FULL OUTER JOIN Genre ON MovieCategory.genreId = Genre.genreId\n" \
            " FULL OUTER JOIN Crew ON Movie.tconst = Crew.tconst\n" \
            " FULL OUTER JOIN People ON Crew.nconst = People.nconst\n"

    filter_str = build_filters(json_dict)
    where_clause_str = build_where_and(filter_str)
    query += where_clause_str
    query += "GROUP BY Movie.tconst\n" \
             " LIMIT 100\n"
    return query


def query_data(query, conn):
    query_data = conn.execute(query)
    result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
    return jsonify({'data': result})


if __name__ == '__main__':
    print("Test with sql_api.py")
