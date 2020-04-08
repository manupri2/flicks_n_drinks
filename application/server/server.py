from urllib import parse
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from handle import *


id_dict = {'CocktailName': 'cocktailId', 'CocktailRecipe': 'recipeId', 'Ingredient': 'ingredientId'}
app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
db = SQLAlchemy(app)
eng = db.engine


@app.route("/")
def about():
	return render_template("aboutPage.html")


@app.route("/index")
def index():
	return render_template("indexPage.html")


@app.route('/xxx')
def home():
	return """<h1>To query database, enter "CocktailName", "CocktailRecipe", or "Ingredient" for {table_name} and 
			  an integer between 0-683 for {id_num} in the route: 
              http://cs411ccsquad.web.illinois.edu/{table_name}/{id_num}</h1>"""


@app.route('/<table_name>', methods=['GET'])
def basic_api(table_name):
    conn = eng.connect()
    if request.method == 'GET':
        query = 'SELECT * FROM %s' % table_name
        return query_data(query, conn)


@app.route('/api/<query_uri>', methods=['GET'])
def api_sql(query_uri):
    conn = eng.connect()
    if request.method == 'GET':
        query = parse.unquote(query_uri)
        return query_data(query, conn)


@app.route('/json/<json_uri>', methods=['GET'])
def json_query(json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))
        query = build_query(json_dict)
        return query_data(query, conn)


if __name__ == "__main__":
	app.run()


