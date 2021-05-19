from db import db
from flask import session

def add_feedback(skill_level, quality, comment, given_by, recipe_id):

    sql = "INSERT INTO feedback (skill_level, quality, comment, given_by, recipe_id)" \
        " VALUES (:skill_level,:quality,:comment,:given_by,:recipe_id)"
    db.session.execute(sql, {"skill_level":skill_level,"quality":quality,"comment":comment,"given_by":given_by,"recipe_id":recipe_id})
    db.session.commit()


