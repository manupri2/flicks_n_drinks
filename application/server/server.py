from urllib import parse
from flask import Flask, request, render_template, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json

if __name__ == "__main__":
    from MovieTraitNetwork import *
    from handle import *
else:
    from application.server.MovieTraitNetwork import *
    from application.server.handle import *


mt_model, test_df = load_model()
# mt_model.summary()
# print("Enter Name:")
# user_name = str(input())
# print("Hello " + user_name)
# test_df['compat'] = see_mtnn(test_df, mt_model)
# print(test_df)

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:oscarhuang1212@localhost/MP1'

db = SQLAlchemy(app)
eng = db.engine

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# page routes
@app.route("/")
def home():
	return render_template("./pages/home.html")


@app.route("/login")
def login():
	return render_template("./pages/loginPage.html")


@app.route("/signup")
def signup():
	return render_template("./pages/signupPage.html")


@app.route("/CRUDAPP")
def crud_app():
	return render_template("./pages/CRUDPage.html")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# API routes
@app.route('/BasicDF', methods=['GET'])
def basic_api(json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        test_df['compat'] = see_mtnn(test_df, mt_model)
        return Response(test_df.to_json(orient="records"), mimetype='application/json')


@app.route('/api/<query_uri>', methods=['GET'])
def api_sql(query_uri):
    conn = eng.connect()
    if request.method == 'GET':
        query = parse.unquote(query_uri)
        return query_data(query, conn, 'json')


@app.route('/MTNN1/<json_uri>', methods=['GET'])
def movie_trait_network(json_uri):
    """
    if 'tConst' empty, returns compatibilities for top 5 most compatible genres
    if 'tConst' non-empty, calculates personalized ratings for movies in 'tConst'
    :param json_uri: {'userId':[int, ...], 'tConst': [int, int, ...]}
    :return:
    """
    # rebuild NN
    # mt_model, test_df = load_model()
    # print("Enter Name:")
    # user_name = str(input())
    # print("Hello " + user_name)
    # test_df['compat'] = MovieTraitNetwork.see_mtnn(test_df, mt_model)
    # print(test_df)

    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))

        tconst_list = json_dict.pop('tConst')
        genre_query = build_genres_query(tconst_list)
        user_info_df = query_data(build_user_query(json_dict), conn, 'df')
        # genre_df = query_data(genre_query, conn, 'df')

        # mt_model, test_df = load_model()
        # result_df = handle_mtnn_api(json_dict, mt_model, user_info_df, genre_df, tconst_list)
        result_df = user_info_df
        return Response(result_df.to_json(orient="records"), mimetype='application/json')


@app.route('/MTNN2/<json_uri>', methods=['GET'])
def movie_trait_network(json_uri):
    """
    if 'tConst' empty, returns compatibilities for top 5 most compatible genres
    if 'tConst' non-empty, calculates personalized ratings for movies in 'tConst'
    :param json_uri: {'userId':[int, ...], 'tConst': [int, int, ...]}
    :return:
    """
    # rebuild NN
    # mt_model, test_df = load_model()
    # print("Enter Name:")
    # user_name = str(input())
    # print("Hello " + user_name)
    # test_df['compat'] = MovieTraitNetwork.see_mtnn(test_df, mt_model)
    # print(test_df)

    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))

        tconst_list = json_dict.pop('tConst')
        genre_query = build_genres_query(tconst_list)
        # user_info_df = query_data(build_user_query(json_dict), conn, 'df')
        genre_df = query_data(genre_query, conn, 'df')

        # mt_model, test_df = load_model()
        # result_df = handle_mtnn_api(json_dict, mt_model, user_info_df, genre_df, tconst_list)
        result_df = genre_df
        return Response(result_df.to_json(orient="records"), mimetype='application/json')


@app.route('/read/<table>/<json_uri>', methods=['GET'])
def read(table, json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))

        query = ""
        if table == "Movies":
            query = build_movie_query(json_dict)
        if table == "Cocktails":
            query = build_cocktail_query(json_dict)
        if table == "User":
            query = build_user_query(json_dict)

        return query_data(query, conn, 'json')


@app.route('/delete/<table>/<item_id>', methods=['GET'])
def delete(table, item_id):
    if request.method == 'GET':
        conn = eng.connect()

        if table == 'Movie':
            sel_query = 'SELECT * FROM Movie WHERE tConst = %s' % item_id
            result = query_data(sel_query, conn, 'json')
            del_query = 'DELETE FROM Movie WHERE tConst = %s' % item_id
        else:
            sel_query = 'SELECT * FROM CocktailRecipe WHERE recipeId = %s' % item_id
            result = query_data(sel_query, conn, 'json')
            del_query = 'DELETE FROM CocktailRecipe WHERE recipeId = %s' % item_id

        conn.execute(del_query)
        return result


@app.route('/add/<table>/<new_input>', methods=['GET'])
def add(table, new_input):
    conn = eng.connect()

    max_recipe_id = ""

    # find maximum
    if table == "Movie":
        max_id_query = 'SELECT MAX(tconst) as max FROM Movie'
    if table == "Cocktails":
        max_id_query = 'SELECT MAX(cocktailId) as max FROM CocktailName'
        max_recipe_id_query = 'SELECT MAX(recipeId) as max FROM CocktailRecipe'

        result = query_data(max_recipe_id_query, conn, 'df')
        max_recipe_id = result['max'][0] + 1

    if table == "User":
        max_id_query = 'SELECT MAX(userId) as max FROM User'

    result = query_data(max_id_query, conn, 'df')
    max_id = result['max'][0] + 1

    # insert new value
    if table == "Movie":
        query = "INSERT INTO %s (tconst, title)" \
                " VALUES (%s , '%s')" % (table, max_id, parse.unquote(new_input))
        conn.execute(query)

    if table == "Cocktails":
        query = "INSERT INTO CocktailName (cocktailId, cocktailName)" \
                " VALUES (%s, '%s')" % (max_id, parse.unquote(new_input))
        conn.execute(query)

        query = "INSERT INTO CocktailRecipe (recipeId, cocktailId)" \
                " VALUES (%s, %s)" % (max_recipe_id, max_id)
        conn.execute(query)

    if table == "User":
        json_dict = json.loads(parse.unquote(new_input))
        query = "INSERT INTO User (userId, firstName, lastName, emailId, password, trOpen, trCon, trex, trAg, trNe)" \
                " VALUES (%s, %s, %s, %s, %s, 0, 0, 0, 0, 0)" % (max_id, json_dict['firstName'], json_dict['lastName'],
                                        json_dict['emailId'], json_dict['password'])
        conn.execute(query)

    response = {'status': 'success', 'message': 'Record added successfully'}
    return response


@app.route('/edit/<table>/<item_id>/<title>', methods=['GET'])
def edit(table, item_id, title):
    conn = eng.connect()

    query = ""
    if table == "Movie":
        query = "UPDATE Movie SET title = '%s' WHERE (tconst = %s)" % (parse.unquote(title), item_id)
    elif table == "Cocktail":
        query = "UPDATE CocktailName SET cocktailName = '%s' WHERE (cocktailId = %s)" % (parse.unquote(title), item_id)
    elif table == "User":
        trs = title.split(':')
        query = "UPDATE User SET trOpen = '%s',trCon = '%s',trex = '%s',trAg = '%s',trNe = '%s' WHERE (userId = %s)" % (trs[0],trs[1],trs[2],trs[3],trs[4], item_id)
    
        
    conn.execute(query)
    response = {'status': 'success', 'message': 'Product edit successfully'}
    return jsonify(response)


if __name__ == "__main__":
    app.run()
