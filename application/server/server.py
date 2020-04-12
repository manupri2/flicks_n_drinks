from urllib import parse
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from application.server.handle import *
from flask import jsonify


id_dict = {'CocktailName': 'cocktailId', 'CocktailRecipe': 'recipeId', 'Ingredient': 'ingredientId'}
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


@app.route("/index")
def crud():
	return render_template("./pages/CRUDPage.html")


@app.route("/stageFour")
def stageFour():
	return render_template("stage4Page.html")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# API routes


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


@app.route('/Movies/<json_uri>', methods=['GET'])
def movie_query(json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))
        query = build_movie_query(json_dict)
        return query_data(query, conn)


@app.route('/Cocktails/<json_uri>', methods=['GET', 'POST'])
def cocktail_query(json_uri):
    conn = eng.connect()
    if request.method == 'GET':
        json_dict = json.loads(parse.unquote(json_uri))
        query = build_cocktail_query(json_dict)
        return query_data(query, conn)


@app.route('/delete/<database>/<id>', methods = ['GET'])
def delete(database, id):
    if request.method == 'GET':
        conn = eng.connect()
        # data = request.get_json()
        # productId = data['product_id']
        # database = data['database']
        # if database == 'Movies':
        query = 'DELETE FROM {} WHERE tconst = {}'.format(database,id)
        # else:
        #     query = 'DELETE FROM CocktailName WHERE cocktailId = %s' %productId
        print(query)
        query_data = conn.execute(query)
        return 'Data id {} in database {} is deleted'.format(id,database)


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


