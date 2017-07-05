<?php
	session_start();
?>

<!DOCTYPE html>
<html lang="ko">
	<head>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
		<style>
			.container{
				margin:5px auto;
				width:90%;
				border: 3px solid #ebebeb;
				border-radius:10px;
				padding-top:15px;
				padding-left:50px;
			}
			h2{
				display: inline;
			}
			img{
				margin-left:12px;
				margin-right:12px;
			}
		</style>
		<meta charset="UTF-8">
	</head>
		<body>
		<div class="container">
		<header>
			<h2 class="text-muted">Microprocessor Project : Smart Pedometer with GPS </h2>  
			<img src="http://www.garmin.com.tw/minisite/vivo/vivoactive/images/vivoactive-features-icon-large-gps.png" width="50px" height="50px">
		</header>
			<nav>
				<ul class="nav nav-pills pull-right">
					<li role="presentation"><a href="GPS.html">My Location</a></li>
					<li role="presentation"><a href="record.php">Recorded Information</a></li>
					<li role="presentation"><a href="AntsIndex.html">GEP</a></li>
					<?php	
						if($_SESSION['login_id']){
						echo '<li><a href="logout.php">Logout</a></li>';
						} 
					?>
				</ul>
			</nav>
		</div>
	</body>
</html>

