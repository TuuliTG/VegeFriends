from app import app
from flask import redirect, render_template, request, session
import users
import recipes
import security
import feedback
import images


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
    users.logout()
    return redirect("/")

@app.route("/newuser", methods=["POST"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    
    if not security.is_valid(username, 4,20):
        return render_template("error.html",message="Käyttäjänimen täytyy olla vähintään 4 ja enintään 20 merkkiä pitkä")
    if not security.is_valid(password, 6, 20):
        return render_template("error.html",message="Salasanan pitää olla vähintään 6 ja enintään 20 merkkiä pitkä") 
    if users.register(username,password,0):
        return redirect("/homepage")
    else:
        return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/addrecipe", methods=["POST"])
def add_recipe():
    
    title = request.form["title"]
    if not security.is_valid(title, 4, 25):
        return render_template("error.html", message="Otsikon pituus täytyy olla vähintään 4 ja enintään 25 merkkiä pitkä")
    instructions = request.form["instructions"]
    uid = users.user_id()

    if recipes.create(title, instructions,uid):
        return redirect("/homepage")
    else:
        return render_template("error.html",message="Reseptin lisääminen ei onnistunut")

@app.route("/recipe/<id>")
def show_recipe(id):
    recipe = recipes.get_recipe_by_id(id)
    feedbacks = feedback.get_feedback_by_recipe_id(id)
    return render_template("recipe.html", recipe=recipe, feedback=feedbacks)


@app.route("/search",methods=["POST"])
def search():
    text = request.form["search"]
    
    return redirect("recipes"+"?search="+text)

@app.route("/recipes")
def show_all_recipes():
    
    search = request.args.get("search")
    if search == "all":
        
        list = recipes.get_all()
    else:
        list = recipes.search_by_text(search)
    return render_template("recipes.html", recipes=list)

@app.route("/delete/<id>",methods=["POST"])
def delete_recipe(id):
    recipes.delete_by_id(id)
    return redirect("/homepage")


@app.route("/admin")
def admin_page():
    if users.is_required_role(1):
        list = users.get_all_users()
        return render_template("admin.html", users=list)
    else:
        return render_template("error.html",message="Sinulla ei ole oikeuksia tälle sivulle")

@app.route("/deleteuser/<id>", methods=["POST"])
def delete_user(id):
    users.delete_user(id)
    return redirect("/admin")

@app.route("/feedback/<id>",methods=["POST"])
def give_feedback(id):
    skill_level = int(request.form["skill_level"])
    quality = int(request.form["quality"])
    comment = request.form["comment"]
    given_by = users.user_id()
    feedback.add_feedback(skill_level,quality,comment,given_by,id)
    return redirect("/recipe/"+id)

@app.route("/create_admin")
def show_create_admin_page():
    return render_template("create_admin.html")

@app.route("/newadmin",methods=["POST"])
def new_admin():
    username = request.form["username"]
    password = request.form["password"]
    users.register(username,password,1)
    return redirect("/")

@app.route("/image/<recipe_id>")
def show_image(recipe_id):
    img = images.show(recipe_id)
    return img

@app.route("/send_image/<id>",methods=["POST"])
def send_image(id):
    file = request.files["file"]
    if (images.save_image(file,id)):
        return redirect("/recipe/" + id)
    else:
        return render_template("error.html",message="Kuvan lisääminen ei onnistunut")