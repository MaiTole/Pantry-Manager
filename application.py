import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproj.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")

#@app.route("/", methods=["POST", "GET"])
#@login_required
#def index():
#    "TODO"
#    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    """Register user"""
    if request.method == "POST":

        #Check if all fields in form have been filled
        myvar = ['name', 'email', 'username', 'password']
        for var in myvar:
            if not request.form.get(f"{var}"):
                return apology(f"Please provide a {var}", 403)
             #Check if username and password are confirmed correctly
            elif request.form.get("username") != request.form.get("confirm-username"):
                return apology("Please confirm username")
            elif request.form.get("password") != request.form.get("confirm-password"):
                return apology("Please confirm username")

        rowcheck = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rowcheck) != 0:
            return apology("This username is taken, please enter a different username.", 403)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
            return apology("success!")

    return render_template("register.html")

@app.route("/addtopantry", methods=["POST", "GET"])
@login_required
def addtopantry():
    if request.method == "POST":
        userid = session["user_id"]
        typeadd = request.form.get("type")
        itemadd = request.form.get("item")
        unitadd = request.form.get("units")
        quantityadd = request.form.get("amount")

        #Check if there is already existing item
        rows = db.execute("SELECT * FROM pantry WHERE id=:id AND item=:item", id=userid, item=itemadd)
        if len(rows) != 0:
            return apology("Sorry, this item is already in your pantry. Use the update pantry option instead!")
        else:
            db.execute("INSERT INTO pantry (id, type, item, unit, quantity) VALUES(:userid, :type, :item, :unit, :quantity)", userid=session["user_id"], type=typeadd, item=itemadd, unit=unitadd, quantity=quantityadd)
        return render_template("index.html")
    return render_template("addtopantry.html")

@app.route("/updatepantry", methods=["POST", "GET"])
@login_required
def updatepantry():
    if request.method == "POST":
        #Update SQL table with pantry update.
        typeadd = request.form.get('type')
        n = len(str(request.form.get('item')).split()) - 1 - 3
        myitem = str(request.form.get('item')).split()[n]
        newqty = request.form.get('newqty')
        userid = session["user_id"]
        db.execute(f"UPDATE pantry SET quantity = {newqty} WHERE id=:id AND type=:type AND item=:item", id=session["user_id"], type=typeadd, item=myitem)

        #Get data for index page/table
        beverages = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="beverages")
        dairy = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="dairy")
        deli = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="deli")
        fruits = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="fruits")
        vegetables = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="vegetables")
        meat = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="meat")
        drygoods = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="dry goods")
        spices = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="spices")
        packagedfood = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="packaged food")
        return render_template("index.html", beverages=beverages, dairy=dairy, deli=deli, fruits=fruits, vegetables=vegetables, meat=meat, drygoods=drygoods, spices=spices, packagedfood = packagedfood)
        #return render_template("editpantry.html", type=typeadd, myitem=myitem) # quantity=selection[0]['quantity'], units=selection[0]['unit'])
    else:
        userid = session["user_id"]
        rowoptions = ["beverages", "dairy", "deli", "dry goods", "fruit", "meat", "packaged foods", "spices", "vegetables"]
        userrows = []
        rows = db.execute("SELECT * FROM pantry WHERE id=:id", id=userid)
        for r in rows:
            if (r['type'] in rowoptions) and (r['type'] not in userrows):
                userrows.append(r['type'])
        beverageitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="beverages")
        dairyitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="dairy")
        deliitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="deli")
        vegetableitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="vegetable")
        fruititems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="fruits")
        meatitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="meat")
        spiceitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="spices")
        drygoodsitems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="dry goods")
        packagedfooditems = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type="packaged food")
        ## ADD DATA FOR ALL TYPES E.G. FRUITS, VEGGIES, MEATS ETC.

        #itemrows = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=userid, type=request.form.get('type'))
        return render_template("updatepantry.html", userrows = userrows, beverageitems=beverageitems, dairyitems=dairyitems, deliitems=deliitems, vegetableitems=vegetableitems, fruititems=fruititems, meatitems=meatitems, spiceitems=spiceitems, drygoodsitems=drygoodsitems, packagedfooditems=packagedfooditems)

    return render_template("index.html")

@app.route("/editpantry", methods=["POST", "GET"])
@login_required
def editpantry():
    if request.method == "POST":
        userid = session["user_id"]
        quantityadd = request.form.get("amount")
        #Check if there is already existing item
        db.execute(f"UPDATE pantry SET quantity = {quantityadd} WHERE id =:id AND item=:item", id = session['user_id'], item = itemadd)
        return render_template("index.html")
    return render_template("editpantry.html")
    #else:
     #   selection = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type AND item=:item", id=userid, type=typeadd, item=itemadd)

@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    beverages = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="beverages")
    #bevmin = []
    #for b in beverages:
        #rows = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type AND item=:item", id=session['user_id'], type="beverages", item=beverages)
        #for r in rows:
        #    if r['quantity'] != NULL:
        #        bevmin.append(r['quantity'])
        #    else:
        #        bevmin.append("0")
    dairy = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="dairy")
    dairymin = []
    for i in dairy:
        rows = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type AND item=:item", id=session['user_id'], type="dairy", item=dairy)
        for r in rows:
            if r['quantity'] != NULL:
                dairymin.append(r['quantity'])
            else:
                dairymin.append("0")
    deli = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="deli")
    fruits = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="fruits")
    vegetables = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="vegetables")
    meat = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="meat")
    drygoods = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="dry goods")
    spices = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="spices")
    packagedfood = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="packaged food")
    return render_template("index.html", beverages=beverages, dairy=dairy, deli=deli, fruits=fruits, vegetables=vegetables, meat=meat, drygoods=drygoods, spices=spices, packagedfood = packagedfood) #, bevmin=bevmin, dairymin=dairymin)

@app.route("/pantryreqmt", methods=["POST", "GET"])
@login_required
def pantryreqmt():
    if request.method == "POST":

        typemin = request.form.get('typemin')
        quantitymin = request.form.get('quantitymin')
        itemmin = request.form.get('itemmin')
        unitmin = request.form.get('unitmin')
        unitlen = len(str(request.form.get('unitmin')).split())

        if unitlen != 1:
            return apology("Please enter only one letter/word for units")
        elif quantitymin == None:
            return apology("Please enter a valid quantity")
        elif itemin == None:
            return apology("Please enter a valid item")
        else:
            db.execute("INSERT INTO pantrymin (id, type, item, quantity, units) VALUES(:id, :type, :item, :quantity, :units)", id=session["user_id"], type =typemin, item=itemmin, quantity=quantitymin, units=unitmin)
            return render_template("index.html")
    elif request.method == "GET":
        return render_template("pantryreqmt.html")

@app.route("/pantryreqmtedit2", methods=["POST", "GET"])
@login_required
def pantryreqmtedit2():
    if request.method == "POST":
        typemin = request.form.get('typemin')
        n = len(str(request.form.get('itemmin')).split()) - 4 - 1
        itemmin = str(request.form.get('itemmin')).split()[n]
        quantitymin = request.form.get('newqty')
        db.execute(f"UPDATE pantrymin SET quantity = {quantitymin} WHERE id=:id AND type=:type AND item=:item", id=session["user_id"], type=typemin, item=itemmin)
        return render_template("index.html")
    else:
        userid = session["user_id"]
        rowoptions = ["beverages", "dairy", "deli", "dry goods", "fruit", "meat", "packaged foods", "spices", "vegetables"]
        userrows = []
        rows = db.execute("SELECT * FROM pantrymin WHERE id=:id", id=userid)
        for r in rows:
            if (r['type'] in rowoptions) and (r['type'] not in userrows):
                userrows.append(r['type'])
        beveragemin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="beverages")
        dairymin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="dairy")
        delimin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="deli")
        vegmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="vegetables")
        fruitmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="fruits")
        meatmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="meat")
        spicemin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="spice")
        drygoodmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="dry goods")
        packagedfoodmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="packaged food")
        ## ADD DATA FOR ALL TYPES E.G. FRUITS, VEGGIES, MEATS ETC.
        return render_template("pantryreqmtedit2.html", userrows=userrows, beveragemin=beveragemin, dairymin=dairymin, delimin=delimin, vegmin=vegmin, fruitmin=fruitmin, meatmin=meatmin, spicemin=spicemin, drygoodmin=drygoodmin, packagedfoodmin=packagedfoodmin)

@app.route("/findameal", methods=["POST", "GET"])
@login_required
def findameal():
    if request.method == "GET":
        return render_template("findameal.html")
    else:
        ingredients = db.execute("SELECT * FROM pantry WHERE id=:id", id=session['user_id'])
        ingredlist = []
        urlnew = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=37f60b0e3dd64d389ab6dacc259cb9f5&ingredients="
        for i in ingredients:
            ingredlist.append(i['item']+",")
        for i in ingredlist:
            urlnew = urlnew + str(i)
        def get(searchurl):
            try:
                res = requests.get(searchurl)
                return res.json()
            except:
                return False
        data = get(urlnew)

        return render_template("recipes.html", data=data)

@app.route("/restocklist")
def restocklist():
    ##PANTRY MIN REQUIREMENTS
    beveragemin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="beverages")
    dairymin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="dairy")
    delimin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="deli")
    vegmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="vegetables")
    fruitmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="fruits")
    meatmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="meat")
    spicemin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="spice")
    drygoodmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="dry goods")
    packagedfoodmin = db.execute("SELECT * FROM pantrymin WHERE id=:id AND type=:type", id=userid, type="packaged food")
    arrmin = [beveragemin, dairymin, delimin, vegmin, fruitmin, meatmin, spicemin, drygoodmin, packagedfoodmin]
    ## PANTRY ACTUALS
    beverages = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="beverages")
    dairy = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="dairy")
    deli = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="deli")
    fruits = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="fruits")
    vegetables = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="vegetables")
    meat = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="meat")
    drygoods = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="dry goods")
    spices = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="spices")
    packagedfood = db.execute("SELECT * FROM pantry WHERE id=:id AND type=:type", id=session['user_id'], type="packaged food")
    arrpantry = [beverages, dairy, deli, vegetables, fruits, meat, spices, drygoods, packagedfood]

    for i in range(arrmin):
        ##if arrpantry[i] =

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")