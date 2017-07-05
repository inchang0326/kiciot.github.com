<?php
header("Content-Type: text/html; charset=UTF-8");

$mysql = new mysqli('localhost', 'kic0326', 'awds1329', 'kic0326');
$result = $mysql -> query("SELECT * FROM user WHERE `id` = '".addslashes($_POST['id'])."'");

$row = $result -> fetch_assoc();

if($row['pw'] == $_POST['pw']) {
	session_start();
	$_SESSION['login_id'] = $_POST['id'];
	header('location:/GPS.html');
} else {
	header('location:/index.html?err=1');
}

?>
