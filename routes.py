from app import app
from flask import redirect, render_template, request, session
import users


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        return redirect("/homepage")
    else:
        return render_template("error.html", message="Väärä tunnus tai salasana")
    
    

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/newuser", methods=["POST"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    if users.register(username,password):
        return redirect("/")
    else:
        return render_template("error.html",message="Rekisteröinti ei onnistunut")

    @app.route("/addrecipe", methods=["POST"])
    def add_recipe():
        title = request.form["title"]
        description = request.form["description"]
        sql = "INSERT INTO recipes (title, description) VALUES (:title, :description)"
        db.session.execute(sql, {"title":title,"description":description})
        db.session.commit()
        return redirect("/homepage")