from db import db
from flask import make_response

def save_image(file, id):
    name = file.filename
    if not name.endswith((".jpg", ".HEIC", "jpeg")):
        print("Invalid filename" + name)
        return False
    data = file.read()
    if len(data) > 20000*1024:
        print("Too big file")
        return False
    if recipe_has_image(id):
        try:
            sql = "UPDATE images SET name=:name, data=:data WHERE recipe_id=:id"
            db.session.execute(sql, {"name":name,"data":data,"id":id})
            db.session.commit()
        except BaseException as e:
            print("Virhe kuvaa tallennettaessa " + str(e))
            return False
    else:
        try:
            sql = "INSERT INTO images (name,data,recipe_id) VALUES (:name,:data,:id)"
            db.session.execute(sql, {"name":name,"data":data,"id":id})
            db.session.commit()
        except BaseException as e:
            print("Virhe kuvaa tallennettaessa " + str(e))
            return False
    return True

def show(id):
    sql = "SELECT data FROM images WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    row = result.fetchone()
    if row is None:
        response = make_response()
        return None
    else:
        data = row[0]
        response = make_response(bytes(data))
        response.headers.set("Content-Type","image/jpeg")
        return response

def recipe_has_image(id):
    sql = "SELECT * FROM images WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    row = result.fetchone()
    if row is None:
        return False
    return True