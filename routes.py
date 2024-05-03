from app import app
import qry
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
from os import abort
import re

##TODO: WLTP:n lisääminen NEDC-mittauksen rinnalle if elif lauseilla
##TODO: dropdown-menut auton lisäämiseksi vertailuun


@app.route("/")
def index():
    try:
        email = session["email"]
        user_id = qry.get_user_id(email)
        comparisons = qry.get_comparison_id(user_id)
        return render_template("index.html", comparisons = comparisons)
    except KeyError:
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if not qry.get_userdata(email):
        return "Sähköpostiosoitteeseen ei ole liitetty tiliä!"
    else:
        hash_value = qry.get_userdata(email).password
        if check_password_hash(hash_value, password):
            session["email"] = email
            session["csrf_token"] = token_hex(16)
            return redirect("/")
        else:
            return "Väärä salasana!"

@app.route("/register", methods=["POST"])
def register():
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    email = request.form["email"]
    password = request.form["password"]
    mat = re.search(pat, password)
    if len(email) > 320:
        return render_template("error.html", error="Sähköpostiosoite on liian pitkä.")
    if not mat:
        return render_template("error.html", error="Salasanan täytyy olla 6-20 merkkiä pitkä ja sisältää vähintään yksi erikoismerkki, yksi kirjain ja yksi iso kirjain.")
    hash_value = generate_password_hash(password)
    qry.add_userdata(email, hash_value)
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    manufacturer = request.form["manufacturer"]
    model = request.form["model"]
    gen = request.form["generation"]
    type = request.form["type"]
    avgconsumption = float(request.form["avgconsumption"]) * 10
    fuel = request.form["fuel"]
    co2nedc = request.form["CO2NEDC"]
    grossweight = request.form["grossweight"]
    nedcprice = qry.get_nedcprice(co2nedc)
    qry.add_car(manufacturer, model, gen, type, avgconsumption, fuel, grossweight, co2nedc, nedcprice)
    success = True
    return render_template("createcar.html", manufacturer = manufacturer, model = model, type = type, success = success)

@app.route("/createcomparison", methods=["POST"])
def createcomparison():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    email = session["email"]
    name = request.form["name"]
    kmyear = request.form["kmyear"]
    gasprice = float(request.form["gasprice"]) * 100
    dieselprice = float(request.form["dieselprice"]) * 100
    userid = qry.get_user_id(email)
    qry.add_comparison(name, userid, kmyear, gasprice, dieselprice)
    value = qry.get_comparisonid(name)
    session["comparisonid"] = value
    return redirect("/editcomparison")

@app.route("/editcomparison")
def editcomparison():
    return render_template("selection.html")

@app.route("/addcar", methods=["POST"])
def addcar():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    manufacturer = request.form["manufacturer"]
    model = request.form["model"]
    gen = request.form["generation"]
    type = request.form["type"]
    insurance = float(request.form["insurance"]) * 100
    carid = qry.get_carid(manufacturer, model, gen, type)
    comparisonid = session["comparisonid"]
    if carid == "None":
        return render_template("error.html", error = "Lisäämääsi autoa ei löydy tietokannasta.")
    else:
        qry.update_comparison(comparisonid, carid, insurance)
        success = True
        return render_template("selection.html", success = success)

@app.route("/comparison", methods=["POST"])
def comparison():
    comparison = request.form["comparison"]
    comparisoncars = qry.get_comparison_cars(comparison)
    comparisondata = qry.get_comparison_data(comparison)
    session["comparisonid"] = comparison
    if comparisoncars:
        ids = [id[0] for id in comparisoncars]
        insurances = [insurance[1] for insurance in comparisoncars]
        cardata = qry.get_car_data(ids)
        cardatazip = zip(cardata, insurances)
        return render_template("comparison.html", cardatazip = cardatazip, comparisondata = comparisondata, comparisoncars = comparisoncars)
    else:
        return render_template("comparison.html", comparisondata = comparisondata)






@app.route("/registered", methods=["POST"])
def registered():
    return "Vahvistussähköposti lähetetty osoitteeseen " + request.form["email"] + "."

@app.route("/signin")
def signin():
    return render_template("signin.html", username=request.form["username"])
