import os
import sys


<<<<<<< Updated upstream:app1.py
# app.config['MYSQL_USER'] = 'cs411ccsquad_admin'
# app.config['MYSQL_PASSWORD'] = 'password;uiuc'
app.config['MYSQL_HOST'] = 'cs411ccsquad.web.illinois.edu'
app.config['MYSQL_DB'] = 'cs411ccsquad_FlicksNDrinks'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
=======
sys.path.insert(0, os.path.dirname(__file__))
>>>>>>> Stashed changes:app.py


def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'It works!\n'
    version = 'Python v' + sys.version.split()[0] + '\n'
    response = '\n'.join([message, version])
    return [response.encode()]
