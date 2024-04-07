from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE email=:email")
    result = db.session.execute(sql, {"email":email})
    user = result.fetchone()
    if not user:
        return "Sähköpostiosoitteeseen ei ole liitetty tiliä!"
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["email"] = email
            return redirect("/")
        else:
            return "Väärä salasana!"

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (email, password) VALUES (:email, :password)")
    db.session.execute(sql, {"email":email, "password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["email"]
    return redirect("/")

@app.route("/createcar")
def createcar():
    return render_template("createcar.html")

@app.route("/submit", methods=["POST"])
def submit():
    manufacturer = request.form["manufacturer"]
    model = request.form["model"]
    gen = request.form["generation"]
    type = request.form["type"]
    sql = "INSERT INTO cars (manufacturer, model, generation, type) VALUES (:manufacturer, :model, :generation, :type)"
    db.session.execute(text(sql), {"manufacturer":manufacturer, "model":model, "generation":gen, "type":type})
    db.session.commit()
    return redirect("/createcar")

#@app.route("/result", methods=["POST"])
#def result():
#    return render_template("createcarresult.html", manufacturer=request.form["manufacturer"], model=request.form["model"], type=request.form["type"])

@app.route("/comparison")
def comparison():
    result = db.session.execute(text("SELECT manufacturer FROM cars"))
    list_of_manufacturers = result.fetchall()
    return render_template("selection.html", list_of_manufacturers = list_of_manufacturers)





@app.route("/registered", methods=["POST"])
def registered():
    return "Vahvistussähköposti lähetetty osoitteeseen " + request.form["email"] + "."

@app.route("/signin")
def signin():
    return render_template("signin.html", username=request.form["username"])
