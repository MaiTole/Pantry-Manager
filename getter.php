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