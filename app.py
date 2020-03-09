# sys.path.insert(0, os.path.dirname(__file__))


# def app(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python v' + sys.version.split()[0] + '\n'
#     response = '\n'.join([message, version])
#     return [response.encode()]


import os
import sys
import sqlalchemy

eng = sqlalchemy.create_engine('mysql://cs411ccsquad_admin:password;uiuc@localhost/cs411ccsquad_FlicksNDrinks')


def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    
    message = ''
    with eng.connect() as con:
        cur = con.execute('SELECT * FROM Genres')
        for i in cur:
            message += repr(i) + "\n"

    message += '\nIt works!\n'
    version = 'Python v' + sys.version.split()[0] + '\n'
    response = '\n'.join([message, version])
    return [response.encode()]


