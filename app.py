import os
import sys
import sqlalchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# eng = sqlalchemy.create_engine('mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks')

id_dict = {'CocktailName': 'cocktailId',
            'CocktailRecipe': 'recipeId',
            'Ingredient': 'ingredientId'}

# 0-683, 0-686, 0-1223

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'

db = SQLAlchemy(app)
eng = db.engine


@app.route('/')
def stanford_page():
    return """<h1>To query database, enter "CocktailName", "CocktailRecipe", or "Ingredient" for {table_name} and an integer between 0-683 for {id_num} in the route:    http://cs411ccsquad.web.illinois.edu/{table_name}/{id_num}</h1>"""


@app.route('/<table_name>/<id_num>')
def Home(table_name, id_num):
    message2 = ''
    with eng.connect() as con:
        cur = con.execute('SELECT * FROM %s WHERE %s = %s' % (table_name, id_dict[table_name], id_num))
        # cur = con.execute('SELECT * FROM CocktailName')
        for i in cur:
            message2 += repr(i) + "\n"

    return message2.encode()


# @app_obj.route('/')
# def app(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])

#     message = ''
#     with eng.connect() as con:
#         cur = con.execute('SELECT * FROM Role')
#         for i in cur:
#             message += repr(i) + "\n"

#     message += '\nIt works!\n'
#     version = 'Python v' + sys.version.split()[0] + '\n'
#     response = '\n'.join([message, version])

#     return [response.encode()]
# app = app_obj.run

if __name__ == '__main__':
    app.run(use_reloader=True)
