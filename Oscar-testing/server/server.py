from urllib import parse
import os
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

id_dict = {'CocktailName': 'cocktailId', 'CocktailRecipe': 'recipeId', 'Ingredient': 'ingredientId'}

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
db = SQLAlchemy(app)
eng = db.engine


# @app.route('/<table_name>/<id_num>')
# def basic_api(table_name, id_num):
#     message2 = ''
#     with eng.connect() as con:
#         cur = con.execute('SELECT * FROM %s WHERE %s = %s' % (table_name, id_dict[table_name], id_num))
#         for i in cur:
#             message2 += repr(i) + "\n"
#     return message2.encode()


@app.route("/")
def index():
	message2 = ''
	with eng.connect() as con:
		cur = con.execute('SELECT * FROM CocktailName')
		for i in cur:
			message2 += repr(i) + "\n"
	return message2.encode()

	# route = "http://cs411ccsquad.web.illinois.edu/CocktailName/5"
	# response = requests.get(route)
	#
	# return render_template("indexPage.html", resp = response.text)


@app.route("/hello")
def hello():
	return "Hello World from Flask!"


if __name__ == "__main__":
	app.run()


