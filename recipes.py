from db import db
from flask import session

def get_all_owned_by_user(user_id):
    sql = "SELECT R.id, R.title FROM recipes R, users U WHERE R.user_id =:user_id AND U.id =:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_all():
    print("haetaan kaikki")
    sql = "SELECT R.id, R.title FROM recipes R"
    result = db.session.execute(sql)
    return result.fetchall()

def create(title, instructions, writer_id):
    try:
        print("suoritetaan sql komentoa")
        sql = "INSERT INTO recipes (title, instructions, user_id) VALUES (:title,:instructions,:writer_id)"
        db.session.execute(sql, {"title":title,"instructions":instructions,"writer_id":writer_id})
        db.session.commit()
    except:
        print("ei onnistunut")
        return False
    return True

def get_recipe_by_id(id):
    
    sql = "SELECT R.title, R.instructions, U.username FROM recipes R, users U WHERE R.id=:id AND R.user_id = U.id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def search_by_text(text):
    
    search_text = "%"+text+"%"
   
    sql = "SELECT R.id, R.title FROM recipes R WHERE title LIKE (:search) OR instructions LIKE (:search)"
    result = db.session.execute(sql, {"search":search_text})
    return result.fetchall()