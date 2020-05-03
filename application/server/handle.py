from application.server.MovieTraitNetwork import *
# from MovieTraitNetwork import *
from flask import jsonify
import pandas as pd
# import sql_api


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

        if isinstance(filter_val, str) and filter_val:
            if operator == 'LIKE':
                filter_val = "'%%" + filter_val + "%%'"
            filter_strs.append(filterX + " " + operator + " " + filter_val)

        if isinstance(filter_val, int):
            filter_strs.append(filterX + " " + operator + " " + repr(filter_val))

    return filter_strs


def build_where(filter_strs, relationship="AND"):
    """
    This function builds the WHERE clause string from a list of filters' strings which have been preformmated for the
    SQL WHERE clause.
    :param filter_strs: list of preformatted filter strings ["location LIKE %%Los Angeles%%", "rating >= 5"]
    :param relationship: str "AND", "OR"
    :return: complete, formatted WHERE clause string to be concatenated into SQL query
    """
    where_str = ""
    if filter_strs:
        where_str += "WHERE " + filter_strs[0] + "\n"

        if len(filter_strs) > 1:
            for f in filter_strs[1:]:
                where_str += " " + relationship + " " + f + "\n"
    return where_str


def build_general_read_query(table, json_dict, filter_rel):
    query = "SELECT * FROM %s\n" % table

    filter_str = build_filters(json_dict)
    where_clause_str = build_where(filter_str, relationship=filter_rel)
    query += where_clause_str
    query += "LIMIT 100\n"
    return query

# def build_cocktail_query(json_dict):
#     query = "SELECT CocktailRecipe.recipeId, CocktailRecipe.bartender, CocktailRecipe.location,\n" \
#             " CocktailRecipe.rating, CocktailName.cocktailName,\n" \
#             " GROUP_CONCAT(DISTINCT Ingredient.ingredientName ORDER BY Ingredient.ingredientName DESC) AS ingredients\n" \
#             "FROM CocktailRecipe\n" \
#             " LEFT OUTER JOIN Composition ON CocktailRecipe.recipeId = Composition.recipeId\n" \
#             " LEFT OUTER JOIN Ingredient ON Composition.ingredientId = Ingredient.ingredientId\n" \
#             " LEFT OUTER JOIN CocktailName ON CocktailRecipe.cocktailId = CocktailName.cocktailId\n"
#
#     filter_str = build_filters(json_dict)
#     where_clause_str = build_where(filter_str, relationship="AND")
#     query += where_clause_str
#     query += "GROUP BY CocktailRecipe.recipeId\n" \
#              "LIMIT 100\n"
#     return query
#
#
# def build_movie_query(json_dict):
#     query = "SELECT Movie.tconst, Movie.title, Movie.year, Movie.rating,\n" \
#             " GROUP_CONCAT(DISTINCT Genre.genreName ORDER BY Genre.genreName DESC) AS genres,\n" \
#             " GROUP_CONCAT(DISTINCT People.name ORDER BY People.name DESC) AS crew\n" \
#             "FROM Movie\n" \
#             " LEFT JOIN MovieCategory ON Movie.tconst = MovieCategory.tconst\n" \
#             " LEFT JOIN Genre ON MovieCategory.genreId = Genre.genreId\n" \
#             " LEFT JOIN Crew ON Movie.tconst = Crew.tconst\n" \
#             " LEFT JOIN People ON Crew.nconst = People.nconst\n"
#
#     filter_str = build_filters(json_dict)
#     where_clause_str = build_where(filter_str, relationship="AND")
#     query += where_clause_str
#     query += "GROUP BY Movie.tconst\n" \
#              "LIMIT 100\n"
#     return query


def build_user_query(json_dict):
    query = "SELECT userId, firstName, lastName, emailId, trOpen, trCon, trEx, trAg, trNe\n" \
            "FROM User\n"

    if 'userId' in json_dict.keys():
        user_ids = json_dict['userId']

        # if searching for multiple users, 'user_ids' should be a list of the userId's
        # if searching for a single user, 'user_ids' can be int or int nested in a list
        # this code will convert user_ids to list if it is not
        if not isinstance(user_ids, list):
            user_ids = [user_ids]

        user_filters = []
        for uid in user_ids:
            user_filters += build_filters({'userId': {'value': uid, 'operator': "="}})

        where_str = build_where(user_filters, relationship="OR")
    else:
        filter_dict = {}

        user_email = "'" + json_dict['emailId'] + "'"
        filter_dict['emailId'] = {'value': user_email, 'operator': "="}
        # user_filters = build_filters({'emailId': {'value': user_email, 'operator': "="}})

        user_password = "'" + json_dict['password'] + "'"
        filter_dict['password'] = {'value': user_password, 'operator': "="}
        # user_filters = build_filters({'password': {'value': user_password, 'operator': "="}})

        user_filters = build_filters(filter_dict)
        where_str = build_where(user_filters, relationship="AND")

    query += where_str
    return query


def query_data(query, conn, return_type):
    q_data = conn.execute(query)
    # result = (1, 2, 3,) or result = ((1, 3), (4, 5),)
    result_data = [dict(zip(tuple(q_data.keys()), i)) for i in q_data.cursor]

    if query:
        message = "No results found"
    else:
        message = "Query empty"

    if result_data:
        message = "Results found"

    if return_type == 'json':
        return jsonify({'data': result_data, 'status': message})

    if return_type == 'df':
        return pd.DataFrame(result_data), message


def build_genres_query(tconst_list):
    if tconst_list:
        query = "SELECT MovieCategory.tConst, Movie.rating, Genre.genreName\n" \
                "FROM Genre\n" \
                " LEFT JOIN MovieCategory ON Genre.genreId = MovieCategory.genreId\n" \
                " LEFT JOIN Movie ON MovieCategory.tConst = Movie.tConst\n"

        filter_str = []
        for tconst in tconst_list:
            filter_str.append("MovieCategory.tConst = %d" % tconst)

        where_str = build_where(filter_str, relationship="OR")
        query += where_str
    else:
        query = "SELECT Genre.genreName\n" \
                "FROM Genre"

    return query


def handle_mtnn_api(json_dict, model, conn):
    tconst_list = json_dict.pop('tConst')
    genre_query = build_genres_query(tconst_list)

    user_info_df, message = query_data(build_user_query(json_dict), conn, 'df')
    genre_df, message = query_data(genre_query, conn, 'df')

    result = calc_genre_compat(user_info_df, tconst_list, genre_df, model)

    return result


def build_insert_query(table, json_dict):
    key_str, val_str = json_to_cs_str(json_dict)

    query = "INSERT INTO %s (%s)" \
            " VALUES (%s)" % (table, key_str, val_str)

    return query


def json_to_cs_str(json_dict):
    key_str = ""
    val_str = ""
    count = 0
    for k, v in json_dict.items():
        if count > 0:
            key_str += ", "
            val_str += ", "

        if isinstance(v, str):
            v = "'" + v + "'"
        else:
            v = repr(v)

        key_str += k
        val_str += v
        count += 1

    return key_str, val_str


def personalized_movie_search(table, json_dict, model, conn):
    user_id = json_dict.pop("userId")
    query = build_general_read_query(table, json_dict, "AND")
    result_df, message = query_data(query, conn, 'df')

    if not result_df.empty:
        feat_dict = {"userId": user_id, "tConst": list(result_df["tconst"].values)}
        compat_df = handle_mtnn_api(feat_dict, model, conn)
        result_df["personalRating"] = compat_df["personalRating"]

    json_rec = result_df.to_dict(orient="records")
    return jsonify({'data': json_rec, 'status': message})


def preformat_filter_dict(json_dict, operator):
    filter_dict = {}

    for key, val in json_dict.items():
        filter_dict[key] = {'value': val, 'operator': operator}

    return filter_dict


def handle_vote(vote_table, vote_col, json_dict, conn):
    match_filters = preformat_filter_dict(json_dict, "=")
    new_val_filter = {vote_col: match_filters.pop(vote_col)}

    read_query = build_general_read_query(vote_table, match_filters, "AND")
    check_df, message = query_data(read_query, conn, 'df')
    # check_df, message = sql_api.api_query(read_query)

    if check_df.empty:
        query = build_insert_query(vote_table, json_dict)
    else:
        filter_str = build_filters(match_filters)
        where_clause_str = build_where(filter_str, relationship="AND")
        query = "UPDATE %s SET %s \n" % (vote_table, build_filters(new_val_filter)[0])
        query += where_clause_str

    # check_df, message = sql_api.api_query(query)
    conn.execute(query)



if __name__ == '__main__':
    print("Test with sql_api.py or tests.py")



