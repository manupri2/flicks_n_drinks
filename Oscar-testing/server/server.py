from flask import Flask, render_template

app = Flask(__name__, static_folder = "../static/dist", template_folder = "../static")


@app.route("/")
def index():
	return render_template("indexPage.html")


@app.route("/hello")
def hello():
	return "Hello World from Flask!"

if __name__ == "__main__":
	app.run()