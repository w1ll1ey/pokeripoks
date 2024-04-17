from db import db
from sqlalchemy.sql import text


def get_userdata(email):
    sql = text("SELECT id, password FROM users WHERE email=:email")
    result = db.session.execute(sql, {"email":email})
    user = result.fetchone()
    return user

def add_userdata(email, hash_value):
    sql = text("INSERT INTO users (email, password) VALUES (:email, :password)")
    db.session.execute(sql, {"email":email, "password":hash_value})
    db.session.commit()

def add_car(manufacturer, model, gen, type):
    sql = "INSERT INTO cars (manufacturer, model, generation, type) VALUES (:manufacturer, :model, :generation, :type)"
    db.session.execute(text(sql), {"manufacturer":manufacturer, "model":model, "generation":gen, "type":type})
    db.session.commit()

def get_user_id(email):
    sql = text("SELECT id FROM users WHERE email=:email")
    result = db.session.execute(sql, {"email":email})
    extract = result.fetchone()
    user_id = str(extract).replace("(", "").replace(")", "").replace(",", "")
    return user_id

def add_comparison(name, userid):
    sql = text("INSERT INTO comparisons (name, userid) VALUES (:name, :userid)")
    db.session.execute(sql, {"name":name, "userid":userid})
    db.session.commit()

def get_comparisonid(name):
    sql = text("SELECT id FROM comparisons WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    extract = result.fetchone()
    comparison_id = str(extract).replace("(", "").replace(")", "").replace(",", "")
    return comparison_id

def get_carid(manufacturer, model, gen, type):
    sql = text("SELECT id FROM cars WHERE manufacturer=:manufacturer AND model=:model AND generation=:generation AND type=:type")
    result = db.session.execute(sql, {"manufacturer":manufacturer, "model":model, "generation":gen, "type":type})
    extract = result.fetchone()
    car_id = str(extract).replace("(", "").replace(")", "").replace(",", "")
    return car_id


def update_comparison(comparisonid, carid):
    sql = text("INSERT INTO comparisoncars (comparisonid, carid) VALUES (:comparisonid, :carid)")
    db.session.execute(sql, {"comparisonid":comparisonid, "carid":carid})
    db.session.commit()

def get_comparison_data(userid):
    sql = text("SELECT name, id FROM comparisons WHERE userid=:userid")
    result = db.session.execute(sql, {"userid":userid})
    extract = result.fetchall()
    return extract

def get_comparison_cars(comparisonid):
    sql = text("SELECT carid FROM comparisoncars WHERE comparisonid=:comparisonid")
    result = db.session.execute(sql, {"comparisonid":comparisonid})
    extract = result.fetchall()
    carids = []
    for value in extract:
        id = str(value).replace("(", "").replace(")", "").replace(",", "")
        carids.append(id)
    return carids

def get_car_data(carid):
    ids = tuple(carid)
    sql = text("SELECT * FROM cars WHERE id IN :id")
    result = db.session.execute(sql, {"id":ids})
    extract = result.fetchall()
    return extract