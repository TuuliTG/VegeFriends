from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, username, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if user[3] == 1 and user[0] == password:
            session["user_id"] = user[1]
            session["username"] = user[2]
            session["user_role"] = user[3]
            return True
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = user[2]
            session["user_role"] = user[3]
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username,"password":hash_value,"role":role})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def get_all_users():
    sql = "SELECT U.id, U.username, U.role FROM users U"
    result = db.session.execute(sql)
    return result.fetchall()

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def delete_user(id):
    sql = "DELETE FROM users USING recipes WHERE users.id=:id AND recipes.user_id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()