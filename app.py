# import os
# import sys
#
#
# sys.path.insert(0, os.path.dirname(__file__))
#
#
# def app(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python v' + sys.version.split()[0] + '\n'
#     response = '\n'.join([message, version])
#     return [response.encode()]

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# app.config['MYSQL_USER'] = 'cs411ccsquad_admin'
# app.config['MYSQL_PASSWORD'] = 'password;uiuc'
app.config['MYSQL_HOST'] = 'cs411ccsquad.web.illinois.edu'
app.config['MYSQL_DB'] = 'cs411ccsquad_FlicksNDrinks'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def Home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT cocktailName FROM CocktailName WHERE cocktailId < 10")
    fetchdata = cur.fetchall()
    cur.close()
    return fetchdata