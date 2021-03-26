<?php

	$mysqlusername = "root";
	$mysqlpassword = "";
	$mysqlserver = "localhost";

	$link = mysql_connect($mysqlserver, $mysqlusername, $mysqlpassword) or die("Unable to connect to MySQL: ".mysql_error());
    $dbname = 'finalproj';
	mysql_select_db($dbname, $link) or die("Could not select examples: ".mysql_error());

?>