from urllib import parse
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from handle import *
from flask import jsonify


id_dict = {'CocktailName': 'cocktailId', 'CocktailRecipe': 'recipeId', 'Ingredient': 'ingredientId'}
app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:oscarhuang1212@localhost/MP1'

db = SQLAlchemy(app)
eng = db.engine


@app.route("/")
def about():
	return render_template("CRUDPage.html")


@app.route("/index")
def index():
	return render_template("indexPage.html")


@app.route("/stageFour")
def stageFour():
	return render_template("stage4Page.html")


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


@app.route('/Movie/<json_uri>', methods=['GET'])
def movie_query(json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))
        query = build_movie_query(json_dict)
        return query_data(query, conn)


@app.route('/Cocktail/<json_uri>', methods=['GET'])
def cocktail_query(json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))
        query = build_cocktail_query(json_dict)
        return query_data(query, conn)


@app.route('/delete', methods = ['POST'])
def delete():
    if request.method =='POST':
        conn = eng.connect()
        data = request.get_json()
        productId = data['product_id']
        query = 'DELETE FROM CocktailName WHERE cocktailId = %s' %productId
        query_data = conn.execute(query)
        return 'Data id %s is deleted' %productId


@app.route('/getProduct', methods = ['POST'])
def getProduct():
    conn = eng.connect()
    data = request.get_json()
    productId = data['product_id']
    query = 'SELECT * FROM CocktailName where cocktailId = %s' %productId
    query_data = conn.execute(query)
    
    for row in query_data:
        row_as_dict = dict(row)

    return row_as_dict

@app.route('/editProduct', methods = ['POST'])
def editProduct():
    
    data = request.get_json()
    if(data!=None):
        conn = eng.connect()    
        productId = data['cocktailId']
        productNewName = data['cocktailName']
        print(productId)
        print(productNewName)

        query = f"UPDATE `CocktailName` SET `cocktailName` = '{productNewName}' WHERE (`cocktailId` = '{productId}')"
        
        print(query)
        print("UPDATE `CocktailName` SET `cocktailName` = 'Mauritius Sour2' WHERE (`cocktailId` = '0')")
        conn.execute(query)   

        response={'status':'success', 'message':'Product updated successfully'}
    else:
        response = {'status':'error'}

    return response

    return 'Data id %s is deleted' %productId


@app.route('/createProduct', methods = ['POST'])
def createProduct():
    data = request.get_json()
    if(data!=None):
        
        inputName  = data['cocktailName']
        conn = eng.connect()
        maxId_query = 'SELECT MAX(cocktailId) as max FROM CocktailName'

        maxIdQueryResult = conn.execute(maxId_query)
        for row in maxIdQueryResult:
            maxDic = dict(row)
        maxId = maxDic['max']+1
        
        query = f"INSERT INTO CocktailName(`cocktailId`, `cocktailName`) VALUES ('{maxId}' , '{inputName}')"

        conn.execute(query)
        response = {'status':'success', 'message':'Product added successfully'}
    
    else:
        response = {'status':'error'}
    
    return response

if __name__ == "__main__":
	app.run()


