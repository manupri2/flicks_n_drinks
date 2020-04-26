from urllib import parse
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from application.server.handle import *
# from handle import *
import application.server.MovieTraitNetwork as MovieTraitNetwork
from flask import jsonify


# rebuild NN
mt_model = MovieTraitNetwork.load_model()

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


@app.route("/loginPage.html")
def login():
	return render_template("./pages/loginPage.html")


@app.route("/signupPage.html")
def signup():
	return render_template("./pages/signupPage.html")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# API routes
@app.route('/<table_name>', methods=['GET'])
def basic_api(table_name):
    conn = eng.connect()
    if request.method == 'GET':
        query = 'SELECT * FROM %s' % table_name
        return query_data(query, conn, 'json')


@app.route('/api/<query_uri>', methods=['GET'])
def api_sql(query_uri):
    conn = eng.connect()
    if request.method == 'GET':
        query = parse.unquote(query_uri)
        return query_data(query, conn, 'json')


# client passes JSON file of filters and their values
@app.route('/MTNN/<json_uri>', methods=['GET'])
def movie_trait_network(json_uri):
    """
    if 'tConst' empty, returns compatibilities for top 5 most compatible genres
    if 'tConst' non-empty, calculates personalized ratings for movies in 'tConst'
    :param json_uri: {'Openness':[float], ..., 'Neuroticism': [float], 'tConst': [int, int, ...]}
    :return:
    """
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))
        result = handle_mtnn_api(json_dict, mt_model, conn)
        return result


# client passes JSON file of filters and their values
@app.route('/read/<table>/<json_uri>', methods=['GET'])
def movie_query(table, json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))

        if table == "Movies":
            query = build_movie_query(json_dict)
        else:
            query = build_cocktail_query(json_dict)

        return query_data(query, conn, 'json')


# client passes JSON file of filters and their values
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
    else:
        max_id_query = 'SELECT MAX(cocktailId) as max FROM CocktailName'
        max_recipe_id_query = 'SELECT MAX(recipeId) as max FROM CocktailRecipe'

        # query_d = conn.execute(max_recipe_id_query)
        # result = [dict(zip(tuple(query_d.keys()), i)) for i in query_d.cursor]
        # max_recipe_id = result[0]['max'] + 1
        result = query_data(max_recipe_id_query, conn, 'df')
        max_recipe_id = result['max'][0] + 1

    # query_d = conn.execute(max_id_query)
    # result = [dict(zip(tuple(query_d.keys()), i)) for i in query_d.cursor]
    # max_id = result[0]['max'] + 1
    result = query_data(max_id_query, conn, 'df')
    max_id = result['max'][0] + 1

    # insert new value
    if table == "Movie":
        query = "INSERT INTO %s (tconst, title)" \
                " VALUES (%s , '%s')" % (table, max_id, parse.unquote(new_input))
        conn.execute(query)
    else:
        query = "INSERT INTO CocktailName (cocktailId, cocktailName)" \
                " VALUES (%s, '%s')" % (max_id, parse.unquote(new_input))
        conn.execute(query)

        query = "INSERT INTO CocktailRecipe (recipeId, cocktailId)" \
                " VALUES (%s, %s)" % (max_recipe_id, max_id)
        conn.execute(query)

    response = {'status': 'success', 'message': 'Product added successfully'}
    return response


@app.route('/edit/<table>/<item_id>/<title>', methods=['GET'])
def edit(table, item_id, title):
    conn = eng.connect()

    query = ""
    if table == "Movie":
        query = "UPDATE Movie SET title = '%s' WHERE (tconst = %s)" % (parse.unquote(title), item_id)
    else:
        query = "UPDATE CocktailName SET cocktailName = '%s' WHERE (cocktailId = %s)" % (parse.unquote(title), item_id)
  
    conn.execute(query)
    response = {'status': 'success', 'message': 'Product edit successfully'}
    return jsonify(response)


if __name__ == "__main__":
    app.run()
