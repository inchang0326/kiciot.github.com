<?php
session_start();
unset($_SESSION['login_id']);
header("location:/index.html");
?>