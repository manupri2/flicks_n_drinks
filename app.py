from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import urllib.parse

id_dict = {'CocktailName': 'cocktailId',
            'CocktailRecipe': 'recipeId',
            'Ingredient': 'ingredientId'}
# Table_id ranges: 0-683, 0-686, 0-1223

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
db = SQLAlchemy(app)
eng = db.engine
# api = Api(app)

# class Access_FlicksNDrinks(Resource):
#     def get(self, query):
#         conn = eng.connect()
#         query_data = conn.execute(urllib.parse.unquote(query))
#         result = {'data': [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]}
#         return jsonify(result)


@app.route('/login')
def login():
    return """<h1>To query database, enter "CocktailName", "CocktailRecipe", or "Ingredient" for {table_name} and 
              an integer between 0-683 for {id_num} in the route:    
              http://cs411ccsquad.web.illinois.edu/{table_name}/{id_num}</h1>"""


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


@app.route('/API_SQL/<query>')
def api_sql(self, query):
    conn = eng.connect()
    # if request.method == 'GET':
        # query = request.values.get('query')
        # query_data = conn.execute(urllib.parse.unquote(query))
        # result = {'data': [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]}
        # return jsonify(result)
    cur = conn.execute(urllib.parse.unquote(query))
    message2 = ''
    for i in cur:
        message2 += repr(i) + "\n"
    return message2.encode()



# api.add_resource(Access_FlicksNDrinks, '/SQL_QUERY/<query>')
    # import urllib.parse
    # query = 'Hellö Wörld@Python'
    # urllib.parse.quote(query) # encodes query into URL format, returns encoded string
    # urllib.parse.unquote(encodedStr) # decodes query from URL format, returns decoded string


if __name__ == '__main__':
    app.run(use_reloader=True)
