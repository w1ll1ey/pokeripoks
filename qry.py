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

def add_car(manufacturer, model, gen, type, avgconsumption, fuel, grossweight, co2nedc, nedcprice):
    sql = "INSERT INTO cars (manufacturer, model, generation, type, avgconsumption, fuel, grossweight, co2nedc, nedcprice) VALUES (:manufacturer, :model, :generation, :type, :avgconsumption, :fuel, :grossweight, :co2nedc, :nedcprice)"
    db.session.execute(text(sql), {"manufacturer":manufacturer, "model":model, "generation":gen, "type":type, "avgconsumption":avgconsumption, "fuel":fuel, "grossweight":grossweight, "co2nedc":co2nedc, "nedcprice":nedcprice})
    db.session.commit()

def get_user_id(email):
    sql = text("SELECT id FROM users WHERE email=:email")
    result = db.session.execute(sql, {"email":email})
    extract = result.fetchone()
    user_id = str(extract).replace("(", "").replace(")", "").replace(",", "")
    return user_id

def add_comparison(name, userid, kmyear, gasprice, dieselprice):
    sql = text("INSERT INTO comparisons (name, userid, kmyear, gasprice, dieselprice) VALUES (:name, :userid, :kmyear, :gasprice, :dieselprice)")
    db.session.execute(sql, {"name":name, "userid":userid, "kmyear":kmyear, "gasprice":gasprice, "dieselprice":dieselprice})
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

def update_comparison(comparisonid, carid, insurance):
    sql = text("INSERT INTO comparisoncars (comparisonid, carid, insurance) VALUES (:comparisonid, :carid, :insurance)")
    db.session.execute(sql, {"comparisonid":comparisonid, "carid":carid, "insurance":insurance})
    db.session.commit()

def get_comparison_id(userid):
    sql = text("SELECT name, id FROM comparisons WHERE userid=:userid")
    result = db.session.execute(sql, {"userid":userid})
    extract = result.fetchall()
    return extract

def get_comparison_data(id):
    sql = text("SELECT name, kmyear, gasprice, dieselprice FROM comparisons WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    extract = result.fetchone()
    return extract

def get_comparison_cars(comparisonid):
    sql = text("SELECT carid, insurance FROM comparisoncars WHERE comparisonid=:comparisonid")
    result = db.session.execute(sql, {"comparisonid":comparisonid})
    extract = result.fetchall()
    return extract

def get_car_data(carid):
    ids = tuple(carid)
    sql = text("SELECT * FROM cars WHERE id IN :id")
    result = db.session.execute(sql, {"id":ids})
    extract = result.fetchall()
    return extract

def get_nedcprice(co2nedc):
    sql = text("SELECT price FROM nedctaxes WHERE co2<=:co2nedc ORDER BY price DESC")
    result = db.session.execute(sql, {"co2nedc":co2nedc})
    extract = result.fetchone()
    for value in extract:
        nedcprice = value
    return nedcprice