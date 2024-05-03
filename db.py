from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text
from dotenv import load_dotenv
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

def nedctaxvalues():
    sql = text("INSERT INTO nedctaxes (co2, price) VALUES ('0', '5329'), ('10', '5730'), ('20'. '6168'), ('30' '6679'), ('40', '7263'), ('50', '7920'), ('60', '8650'), ('70', '9453'), ('80', '10366'), ('90', '11388'), ('100', '12556'), ('110', '13797'), ('120', '15184'), ('130', '16717'), ('140', '18396'), ('150', '20221'), ('160', '22228'), ('170', '24345'), ('180', '26645'), ('190', '29090'), ('200', '31609'), ('210', '33726'), ('250', '42522'), ('300', '52815'), ('350', '60553'), ('400', '65444')")
    db.session.execute(sql)
    db.session.commit()