from db import db

def like(user_id, recipe_id):
    sql = "INSERT INTO likes (user_id, recipe_id) VALUES (:user_id,:recipe_id)"
    db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
    db.session.commit()


def dislike(user_id, recipe_id):
    sql = "DELETE FROM likes WHERE user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
    db.session.commit()

def user_likes_recipe(user_id,recipe_id):
    sql = "SELECT id FROM likes WHERE user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
    id = result.fetchone()
    if id is None:
        return False
    else:
        return True

def count_likes(recipe_id):
    sql = "SELECT COUNT(id) FROM likes WHERE recipe_id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    count = result.fetchone()[0]
    return count