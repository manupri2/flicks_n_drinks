from urllib import parse
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


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


@app.route('/<table_name>')
def basic_api(table_name):
    message2 = ''
    with eng.connect() as con:
        cur = con.execute('SELECT * FROM %s' % table_name)
        for i in cur:
            message2 += repr(i) + "\n"
    return message2.encode()


@app.route('/api/<query>', methods=['GET'])
def api_sql(query):
    conn = eng.connect()
    if request.method == 'GET':
        query_data = conn.execute(parse.unquote(query))
        result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
        return jsonify({'data': result})


if __name__ == "__main__":
	app.run()


