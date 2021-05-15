from app import app
from flask import redirect, render_template, request, session
import users
import recipes


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
    list = recipes.get_all_owned_by_user(users.user_id())
    return render_template("homepage.html", recipes=list)

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
    instructions = request.form["instructions"]
    uid = users.user_id()
    if recipes.create(title, instructions,uid):
        return redirect("/homepage")
    else:
        return render_template("error.html",message="Reseptin lisääminen ei onnistunut")

@app.route("/recipes/<id>")
def show_recipe(id):
    recipe = recipes.get_recipe_by_id(id)
    return render_template("recipe.html", recipe=recipe)