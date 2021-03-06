from db import db
from flask import session


def add_feedback(skill_level, quality, comment, given_by, recipe_id):

    sql = "INSERT INTO feedback (skill_level, quality, comment, given_by, recipe_id)" \
        " VALUES (:skill_level,:quality,:comment,:given_by,:recipe_id)"
    db.session.execute(sql, {"skill_level":skill_level,"quality":quality,"comment":comment,"given_by":given_by,"recipe_id":recipe_id})
    db.session.commit()


def get_feedback_by_recipe_id(id):
    
    sql = "SELECT F.comment, F.given_by, U.username AS written_by, "\
        "(SELECT ROUND(AVG(skill_level),2) FROM feedback WHERE recipe_id=:id) AS skill_level,"\
        "(SELECT ROUND(AVG(quality),2) FROM feedback WHERE recipe_id=:id) AS quality"\
        " FROM feedback F, users U WHERE recipe_id=:id AND F.given_by=U.id"
    result = db.session.execute(sql, {"id":id})
    
    return result.fetchall()