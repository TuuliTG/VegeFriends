from db import db
from flask import make_response

def save_image(file, id):
    name = file.filename
    if not name.endswith(".jpg"):
        print("Invalid filename")
        return False
    data = file.read()
    if len(data) > 100*1024:
        print("Too big file")
        return False
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
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type","image/jpeg")
    return response