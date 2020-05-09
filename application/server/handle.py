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
                # filter_val = "'%%" + filter_val + "%%'"
                filter_val = "%%" + filter_val + "%%"

            if not ((filter_val[0] == "'" or filter_val[0] == '"') and (filter_val[-1] == "'" or filter_val[-1] == '"')):
                filter_val = repr(filter_val)

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


def build_col_str(columns):
    count = 0
    col_str = ""

    for col in columns:
        if count > 0:
            col_str += ", "
        col_str += col
        count += 1

    return col_str


def build_general_read_query(table, json_dict, filter_rel, columns=None):
    if columns is None:
        columns = []
    if columns:
        col_str = build_col_str(columns)
        query = "SELECT %s FROM %s\n" % (col_str, table)
    else:
        query = "SELECT * FROM %s\n" % table

    filter_str = build_filters(json_dict)
    where_clause_str = build_where(filter_str, relationship=filter_rel)
    query += where_clause_str
    query += "LIMIT 100"
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

        user_password = "'" + json_dict['password'] + "'"
        filter_dict['password'] = {'value': user_password, 'operator': "="}

        user_filters = build_filters(filter_dict)
        where_str = build_where(user_filters, relationship="AND")

    query += where_str
    return query


def query_data(query, conn, return_type):
    q_data = conn.execute(query)
    # result = (1, 2, 3,) or result = ((1, 3), (4, 5),)
    try:
        result_data = [dict(zip(tuple(q_data.keys()), i)) for i in q_data.cursor]
    except TypeError:
        result_data = []

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
            if not (v[0] == '@' or ((v[0] == "'" or v[0] == '"') and (v[-1] == "'" or v[-1] == '"'))):
                # v = "'" + v + "'"
                v = repr(v)
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
    print(result_df)

    vote_filt_dict = {"userId": {'value': user_id, 'operator': '='}}
    votes_query = build_general_read_query("FavoriteMovie", vote_filt_dict, "AND", columns=['tConst', 'ratesMovie'])
    votes_df, message = query_data(votes_query, conn, 'df')
    print(votes_df)

    if not result_df.empty:
        if not votes_df.empty:
            # join votes to the result dataframe
            votes_df.set_index('tConst', inplace=True)
            result_df = result_df.join(votes_df, on='tConst', lsuffix='', rsuffix='_copy')
            print(result_df)
        else:
            result_df['ratesMovie'] = np.nan

        feat_dict = {"userId": user_id, "tConst": list(result_df["tConst"].values)}
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


def check_then_insert(table, check_dict, id_col, conn):

    # format filters for use in build_general_read_query
    filter_dict = preformat_filter_dict(check_dict, "=")

    # build the SELECT query that will check to see if cocktailName/glasswareName exist; return full SQL results
    check_query = build_general_read_query(table, filter_dict, "AND")

    # query_data function executes check_query and returns results as a pandas dataframe
    check_df, message = query_data(check_query, conn, 'df')

    if check_df.empty:
        print("Value not found, inserting new tuple into %s." % table)
        # builds INSERT query to insert new cocktailName/glasswareName
        insert_query = build_insert_query(table, check_dict)
        conn.execute(insert_query)

        # query_data function executes check_query and returns results as a pandas dataframe
        check_df, message = query_data(check_query, conn, 'df')

    else:
        print("Value exists, not inserting new tuple into %s." % table)

    # grabs and returns id value (integer) from results
    return check_df[id_col][0]


def handle_add_recipe(json_dict, conn):
    checks = {"CocktailName": {"checkCol": "cocktailName", "idCol":  "cocktailId"},
              "Glassware": {"checkCol": "glasswareName", "idCol":  "glasswareId"}}

    # loop through all tables where we need to ensure values already exist due to foreign key constraints
    for table_name, check_info in checks.items():
        check_col = check_info["checkCol"]
        id_col = check_info["idCol"]

        if check_col in json_dict.keys():
            # grabs cocktailName/glasswareName (for use in check_then_insert())
            # pops from json_dict as cocktailName/glasswareName do not exist in CocktailRecipe table attributes
            check_val = "'" + json_dict.pop(check_col) + "'"

            # checks if value exists
            #    - if so, returns id
            #    - if not, inserts the new value into its respective table and then returns the id of new tuple
            check_id = check_then_insert(table_name, {check_col: check_val}, id_col, conn)

            # inserts id value into json_dict as cocktailId/glasswareId do exist in CocktailRecipe table attributes
            json_dict[id_col] = check_id

    # builds INSERT query to insert new CocktailRecipe
    insert_query = build_insert_query("CocktailRecipe", json_dict)
    conn.execute(insert_query)


# def build_check_then_insert_query(table, check_dict, id_col, var_name):
#     filter_dict = preformat_filter_dict(check_dict, "=")
#     var_name = "@" + var_name
#
#     check_query = build_general_read_query(table, filter_dict, "AND")
#     insert_query = build_insert_query(table, check_dict)
#     sel_query = build_general_read_query(table, filter_dict, "AND", columns=[id_col])
#
#     compound_str = "\tIF NOT EXISTS (%s) THEN\n" \
#                    "\t\t%s;\n"\
#                    "\tEND IF;\n" \
#                    "\tSET %s = (%s);\n" % (check_query, insert_query, var_name, sel_query)
#
#     return compound_str
#
#
# def build_add_recipe_compound(json_dict):
#     checks = {"CocktailName": {"checkCol": "cocktailName", "idCol":  "cocktailId"},
#               "Glassware": {"checkCol": "glasswareName", "idCol":  "glasswareId"}}
#
#     check_str_list = []
#     base_name = "var"
#     count = 1
#     for table_name, check_info in checks.items():
#         check_col = check_info["checkCol"]
#         id_col = check_info["idCol"]
#
#         if check_col in json_dict.keys():
#             check_val = "'" + json_dict.pop(check_col) + "'"
#             var_name = base_name + repr(count)
#             check_str_list.append(build_check_then_insert_query(table_name, {check_col: check_val}, id_col, var_name))
#             json_dict[id_col] = "@" + var_name
#             count += 1
#
#     insert_query = build_insert_query("CocktailRecipe", json_dict)
#     compound_str = ""
#     # compound_str = "BEGIN\n"
#     for check_str in check_str_list:
#         compound_str += check_str
#     compound_str += insert_query + ";"
#     # compound_str += "\nEND;"
#     # print(compound_str)
#     return compound_str


if __name__ == '__main__':
    print("Test with sql_api.py or tests.py")



