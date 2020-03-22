import urllib.parse

from flask import Flask, request
from flask_jsonpify import jsonify
from flask_sqlalchemy import SQLAlchemy



import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from math import pi
import base64
from io import BytesIO



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


@app.route('/api/<query>', methods=['GET'])
def api_sql(query):
    conn = eng.connect()
    if request.method == 'GET':
        # query = request.values.get('query')
        query_data = conn.execute(urllib.parse.unquote(query))
        #result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
        #return jsonify(result)
        
    # message2 = ''
    # with eng.connect() as con:
    #     cur = con.execute(urllib.parse.unquote(query))
    #     for i in cur:
    #         message2 += repr(i) + "\n"
    # return message2.encode()



# api.add_resource(Access_FlicksNDrinks, '/SQL_QUERY/<query>')
    # import urllib.parse
    # query = 'Hellö Wörld@Python'
    # urllib.parse.quote(query) # encodes query into URL format, returns encoded string
    # urllib.parse.unquote(encodedStr) # decodes query from URL format, returns decoded string




@app.route("/radarChart")
def hello():
   
    # Generate the figure **without using pyplot**.
    fig = Figure()
    categories = ['trOpen','trCon','trEx','trAg', 'trNe']
    values = [83,67,91,52,76,83]
    N = 5

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]


    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi/2)
    plt.rcParams["axes.axisbelow"] = False

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)
    
    # Draw ylabels
    plt.yticks( color="grey", size=7)
    plt.ylim(0,100)
    #ax.set_rlabel_position(90)
        
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == '__main__':
    app.run(use_reloader=True)
