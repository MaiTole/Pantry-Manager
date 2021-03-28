<?php

	$mysqlusername = "root";
	$mysqlpassword = "";
	$mysqlserver = "localhost";

	$link = mysql_connect($mysqlserver, $mysqlusername, $mysqlpassword) or die("Unable to connect to MySQL: ".mysql_error());
    $dbname = 'finalproj';
	mysql_select_db($dbname, $link) or die("Could not select examples: ".mysql_error());

?>

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

    ##for i in range(arrmin):
        ##if arrpantry[i] =

###################

@app.route("/restocklist")
@login_required
def restocklist():
    ##PANTRY MIN REQUIREMENTS
    userid = session["user_id"]
    bevreqmt = dict()
    rows = db.execute("SELECT * FROM pantrymin WHERE id=:id AND item NOT IN (SELECT item FROM pantry WHERE id=:id)", id=userid)
    for r in rows:
        bevreqmt['item'] = r['item']
        bevreqmt['quantity'] = r['quantity']
        bevreqmt['unit'] = r['units']

    intersection = db.execute("SELECT * FROM pantrymin WHERE id=:id AND item IN (SELECT item FROM pantry WHERE id=:id)", id=userid)
    for i in intersection:
        match = db.execute("SELECT * FROM pantry WHERE id=:id AND item=:item", id=userid, item=i['item'])
        if i['quantity'] > match[0]['quantity']:
            #bevreqmt['item'].append(i['item'])
            if i['units'] != match[0]['unit']:
                bevreqmt['item'] = (i['item'])
                bevreqmt['quantity'] = ("")
                bevreqmt['unit'] = ("")
            else:
                bevreqmt['item'] = (i['item'])
                bevreqmt['quantity'] = (i['quantity'] - match[0]['quantity'])
                bevreqmt['unit'] = (i['units'])
            #bevreqmt.append
                return render_template("restocklist.html", bevreqmt=bevreqmt)
