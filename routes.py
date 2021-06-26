from app import app
from flask import redirect, render_template, request, session
import users
import recipes
import validation
import feedback
import images
import likes


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
    uid = users.user_id()
    list = recipes.get_all_owned_by_user(uid)
    favourites = likes.list_liked_by_user(uid)
    return render_template("homepage.html", recipes=list, likes=favourites)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/newuser", methods=["POST"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    if not validation.is_valid(username, 4,20):
        return render_template("error.html",message="Käyttäjänimen täytyy olla vähintään 4 ja enintään 20 merkkiä pitkä")
    if not validation.is_valid(password, 6, 20):
        return render_template("error.html",message="Salasanan pitää olla vähintään 6 ja enintään 20 merkkiä pitkä") 
    if users.register(username,password,0):
        return redirect("/homepage")
    else:
        return render_template("error.html",message="Rekisteröinti ei onnistunut")


@app.route("/addrecipe", methods=["POST"])
def add_recipe():
    check_CSRF_token()
    title = request.form["title"]
    if not validation.is_valid(title, 4, 25):
        return render_template("error.html", message="Otsikon pituus täytyy olla vähintään 4 ja enintään 25 merkkiä pitkä")
    instructions = request.form["instructions"]
    if not validation.is_valid(instructions, 15, 1000):
        return render_template("error.html", message="Ohjeen pitää olla vähintään 15 ja enintään 1000 merkkiä pitkä")
    uid = users.user_id()

    if recipes.create(title, instructions,uid):
        return redirect("/homepage")
    else:
        return render_template("error.html",message="Reseptin lisääminen ei onnistunut")


@app.route("/recipe/<id>")
def show_recipe(id):
    uid = users.user_id()
    recipe = recipes.get_recipe_by_id(id)
    count_likes = likes.count_likes(id)
    user_likes_recipe = likes.user_likes_recipe(uid,id)
    feedbacks = feedback.get_feedback_by_recipe_id(id)
    for fb in feedbacks:
        print(fb.comment)
    has_image = images.recipe_has_image(id)

    return render_template("recipe.html", recipe=recipe, feedback=feedbacks, has_image=has_image, likes=user_likes_recipe, countLikes=count_likes)


@app.route("/search",methods=["POST"])
def search():
    check_CSRF_token()
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
    check_CSRF_token()
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
    check_CSRF_token()
    users.delete_user(id)
    if id == session.get("user_id",0):
        print("käyttäjä poisti itsensä")
        logout()
        return redirect("/")
    return redirect("/admin")


@app.route("/feedback/<id>",methods=["POST"])
def give_feedback(id):
    check_CSRF_token()
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


@app.route("/like/<recipe_id>", methods=["POST"])
def like(recipe_id):
    user_id = users.user_id()
    likes.like(user_id,recipe_id)
    return redirect("/recipe/"+recipe_id)


@app.route("/dislike/<recipe_id>",methods=["POST"])
def dislike(recipe_id):
    user_id = users.user_id()
    likes.dislike(user_id,recipe_id)
    return redirect("/recipe/"+recipe_id)


def check_CSRF_token():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)