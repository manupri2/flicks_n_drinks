import urllib.parse
import os

# Import Flask
from flask import Flask, request, render_template
from flask_jsonpify import jasonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

# Location of the js (bundled) files and the html files
# app = Flask(__name__, static_folder = "../static/dist", template_folder = "../static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'

db = SQLAlchemy(app)
eng = db.engine



@app.route('/login')
def login():
    return render_template("index.html")


@app.route('/')
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
    conn = eng.connect()
    if request.method == 'GET':
        # query = request.values.get('query')
        query_data = conn.execute(urllib.parse.unquote(query))
        result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
        return jsonify(result)


@app.route("/indexPage")
def index():
	return render_template("indexPage.html")


if __name__ == '__main__':
    app.run(use_reloader=True)