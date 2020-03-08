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

# from flask import Flask, jsonify, request
# from flask_mysqldb import MySQL
#
# app = Flask(__name__)
#
# app.config['MYSQL_USER'] = 'cs411ccsquad_admin'
# app.config['MYSQL_PASSWORD'] = 'password;uiuc'
# app.config['MYSQL_HOST'] = 'cs411ccsquad.web.illinois.edu'
# # app.config['MYSQL_PORT'] = 3306
# app.config['MYSQL_DB'] = 'cs411ccsquad_FlicksNDrinks'
# # app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#
# mysql = MySQL(app)
#
# @app.route('/')
# def Home():
#     print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
#     conn = mysql.connection
#     print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
#     print(repr(conn))
#     cur = conn.cursor()
#     print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

#     cur.execute("SELECT cocktailName FROM CocktailName WHERE cocktailId < 10")
#     print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
#     fetchdata = cur.fetchall()
#     print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
#     cur.close()
#     print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
#     return fetchdata

# from flask import Flask, render_template, request
# from flask_mysqldb import MySQL
# app = Flask(__name__)
#
#
# app.config['MYSQL_HOST'] = 'cs411ccsquad.web.illinois.edu'
# app.config['MYSQL_USER'] = 'cs411ccsquad_admin'
# app.config['MYSQL_PASSWORD'] = 'password;uiuc'
# app.config['MYSQL_DB'] = 'cs411ccsquad_FlicksNDrinks'
#
# mysql = MySQL(app)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # if request.method == "POST":
#     #     details = request.form
#     #     firstName = details['fname']
#     #     lastName = details['lname']
#     #     cur = mysql.connection.cursor()
#     #     cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
#     #     mysql.connection.commit()
#     #     cur.close()
#         return 'success'
#     return render_template('index.html')
#
#
# if __name__ == '__main__':
#     app.run()

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)
#
#
# app.config['MYSQL_HOST'] = 'cs411ccsquad.web.illinois.edu'
# app.config['MYSQL_USER'] = 'cs411ccsquad_admin'
# app.config['MYSQL_PASSWORD'] = 'password;uiuc'
# app.config['MYSQL_DB'] = 'cs411ccsquad_FlicksNDrinks'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks'
# engine = create_engine('mysql+pymysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks', echo=True)
db = SQLAlchemy(app)


@app.route('/')
def Home():
    print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    engine = db.engine
    print(engine)
    print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    conn = db.engine.connect()
    print(conn)
    print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(conn)
    print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    result = conn.execute(text("SELECT cocktailName FROM CocktailName WHERE cocktailId < 10"))
    print(result)
    fetchdata = result.fetchall()
    print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    result.close()
    print("HELLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    return fetchdata


app.run()

# if __name__ == '__main__':

