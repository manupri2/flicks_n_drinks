
from urllib import parse
import os
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__, static_folder = "../static/dist", template_folder = "../static")


@app.route("/")
def index():
	route = "http://cs411ccsquad.web.illinois.edu/CocktailName/5"
	response = requests.get(route)

	return render_template("indexPage.html", resp = response.text)


@app.route("/hello")
def hello():
	return "Hello World from Flask!"

if __name__ == "__main__":
	app.run()


