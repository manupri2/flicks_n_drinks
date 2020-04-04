from urllib import parse
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


id_dict = {'CocktailName': 'cocktailId', 'CocktailRecipe': 'recipeId', 'Ingredient': 'ingredientId'}
app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
db = SQLAlchemy(app)
eng = db.engine


@app.route("/")
def index():
	# query = 'SELECT * FROM Composition WHERE compositionId > 5 AND compositionId < 100'
	# encoded_query = parse.quote(query)
	# route = "http://cs411ccsquad.web.illinois.edu/api/%s" % encoded_query
	# response = requests.get(route)
	#
	# queried_data_json = response.json()
	# print(queried_data_json)
	# return render_template("indexPage.html", resp=response.text)
	return render_template("indexPage.html")


@app.route('/home')
def home():
	return """<h1>To query database, enter "CocktailName", "CocktailRecipe", or "Ingredient" for {table_name} and 
			  an integer between 0-683 for {id_num} in the route: 
              http://cs411ccsquad.web.illinois.edu/{table_name}/{id_num}</h1>"""


@app.route('/<table_name>/<id_num>')
def basic_api(table_name, id_num):
    message2 = ''
    with eng.connect() as con:
        cur = con.execute('SELECT * FROM %s WHERE %s = %s' % (table_name, id_dict[table_name], id_num))
        for i in cur:
            message2 += repr(i) + "\n"
    return message2.encode()


@app.route('/api/<query>', methods=['GET'])
def api_sql(query):
    # conn = eng.connect()
    # if request.method == 'GET':
    #     # query = request.values.get('query')
    #     query_data = conn.execute(parse.unquote(query))
    #     result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
        # return jsonify(result)
    return {'compositionId': 6, 'ingredientId': 1025, 'quantity': '.5', 'recipeId': 1, 'unit': 'oz'}


if __name__ == "__main__":
	app.run()


