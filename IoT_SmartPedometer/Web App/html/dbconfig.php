<?php
	$mysqli = new mysqli('localhost', 'kic0326', 'awds1329', 'kic0326');
	$mysqli -> query('INSERT INTO gps(latitude, longitude, course) VALUE('.$_GET['latitude'].', '.$_GET['longitude'].', '.$_GET['course'].')');
?>