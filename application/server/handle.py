from flask import jsonify


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
            " INNER JOIN Composition ON CocktailRecipe.recipeId = Composition.recipeId\n" \
            " INNER JOIN Ingredient ON Composition.ingredientId = Ingredient.ingredientId\n" \
            " INNER JOIN CocktailName ON CocktailRecipe.cocktailId = CocktailName.cocktailId\n"

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
            " INNER JOIN MovieCategory ON Movie.tconst = MovieCategory.tconst\n" \
            " INNER JOIN Genre ON MovieCategory.genreId = Genre.genreId\n" \
            " INNER JOIN Crew ON Movie.tconst = Crew.tconst\n" \
            " INNER JOIN People ON Crew.nconst = People.nconst\n"

    filter_str = build_filters(json_dict)
    where_clause_str = build_where_and(filter_str)
    query += where_clause_str
    query += "GROUP BY Movie.title\n" \
             " LIMIT 100\n"
    return query


def build_movie_query_old(json_dict):
    query = "SELECT Movie.tconst, Movie.title, Movie.year, Movie.rating,\n" \
            " GROUP_CONCAT(DISTINCT Genre.genreName ORDER BY Genre.genreName DESC) AS genres,\n" \
            " GROUP_CONCAT(DISTINCT People.name ORDER BY People.name DESC) AS crew\n" \
            "FROM Movie\n" \
            " INNER JOIN MovieCategory ON Movie.tconst = MovieCategory.tconst\n" \
            " INNER JOIN Genre ON MovieCategory.genreId = Genre.genreId\n" \
            " INNER JOIN Crew ON Movie.tconst = Crew.tconst\n" \
            " INNER JOIN People ON Crew.nconst = People.nconst\n"

    year = json_dict['year']
    rating = json_dict['rating']
    title = json_dict['title']

    filter_q = ""
    filters = []
    if title:
        title = "%%" + title + "%%"
        filters.append("title LIKE '%s'" % title)
    if year:
        filters.append("year = " + year)
    if rating:
        filters.append("rating >= " + rating)

    if filters:
        filter_q += "WHERE " + filters[0] + "\n"

        if len(filters) > 1:
            for f in filters[1:]:
                filter_q += " AND " + f + "\n"

    query += filter_q
    query += "GROUP BY Movie.title\n" \
             " LIMIT 100\n"
    return query


def query_data(query, conn):
    query_data = conn.execute(query)
    result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
    return jsonify({'data': result})

if __name__ == '__main__':

    json_dict = {'title': 'ca', 'year': '2005', 'rating': ''}
    old = build_movie_query_old(json_dict)

    json_dict = {
                  'title': {'value': 'ca', 'operator': 'LIKE'},
                  'year': {'value': '2005', 'operator': '='},
                  'rating': {'value': '', 'operator': '>='}}
    new = build_movie_query(json_dict)

    print(old)
    print(new)
    print(old == new)

    # json_dict = {
    #               'cocktailName': {'value': 'Manhattan', 'operator': 'LIKE'},
    #               'ingredients': {'value': 'cherry', 'operator': 'LIKE'},
    #               'bartender': {'value': 'Johnny Rocket', 'operator': 'LIKE'},
    #               'location': {'value': 'Los Angeles', 'operator': 'LIKE'},
    #               'rating': {'value': '5', 'operator': '>='}
    #             }
    # print(build_cocktail_query(json_dict))
    #
    # json_dict = {
    #               'cocktailName': {'value': '', 'operator': 'LIKE'},
    #               'ingredients': {'value': '', 'operator': 'LIKE'},
    #               'bartender': {'value': '', 'operator': 'LIKE'},
    #               'location': {'value': '', 'operator': 'LIKE'},
    #               'rating': {'value': '', 'operator': '>='}
    #             }
    # print(build_cocktail_query(json_dict))
    #
    # json_dict = {
    #               'cocktailName': {'value': 'a', 'operator': 'LIKE'},
    #               'ingredients': {'value': '', 'operator': 'LIKE'},
    #               'bartender': {'value': '', 'operator': 'LIKE'},
    #               'location': {'value': '', 'operator': 'LIKE'},
    #               'rating': {'value': '', 'operator': '>='}
    #             }
    # print(build_cocktail_query(json_dict))
    # #
    # # api_q = "http://cs411ccsquad.web.illinois.edu/Movies/%7B%22title%22:%22da%22,%22year%22:%22%22,%22rating%22:%22%22%7D"