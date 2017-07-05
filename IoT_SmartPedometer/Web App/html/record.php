<?php include "header.php" ?>

<?php
	if(!$_SESSION['login_id']):
		header('location:/index.html?err=1');
?>

<?php else:
?>

<?php endif; ?>

<?php
	$connect = mysql_connect("localhost", "kic0326", "awds1329");
	$db_con = mysql_select_db("kic0326", $connect);
	$sql = "select * from gps";
	$result = mysql_query($sql, $connect);

	$size = 0;				// 크기
	$latitude = array();	// gps테이블에 있는 위도 값들을 넣을 php배열
	$longitude = array();	// gps테이블에 있는 경도 값들을 넣을 php배열
	$course = array();		// gps테이블에 있는 코스 값들을 너을 php배열
?>

<?php
while($row = mysql_fetch_array($result)){
	$latitude[$size] = $row['latitude'];	// 위도 값 저장
	$longitude[$size] = $row['longitude'];	// 경도 값 저장
	$course[$size] = $row['course'];		// 코스 값 저장
	$size++;								// 크기
}
?>

<!DOCTYPE html>
<html lang="ko">
	<head>
		<style>
			#map{
				margin:15px auto;
			}
		</style>
		<meta charset="UTF-8">
		<title>Recorded information</title>
	</head>
	<body>
		<div id="map" style="width:90%;height:1000px;"></div>
		<script type="text/javascript" src="//apis.daum.net/maps/maps3.js?apikey=82efa9caba9af3640b436747196453bc"></script>
		<script language="JavaScript">
		var latitude = <?php echo json_encode($latitude); ?>;	// php의 위도값 배열을 자바스크립트 배열에 저장
		var longitude = <?php echo json_encode($longitude); ?>;	// php의 경도값 배열을 자바스크립트 배열에 저장
		var course = <?php echo json_encode($course); ?>;		// php의 코스값 배열을 자바스크립트 배열에 저장
		var size = <?=$size?>;									// 크기 저장
		for(var i=0; i<size; i++){
			console.log(latitude[i]);
			console.log(longitude[i]);
			console.log(course[i]);
		}
		window.onload = function() {
              
            // 지도의 중심
            var position = new daum.maps.LatLng(latitude[size-1], longitude[size-1]);
       
            // 기본 지도 표시
            var map = new daum.maps.Map(document.getElementById('map'), {
                center: position,
                level: 1,
                mapTypeId: daum.maps.MapTypeId.ROADMAP
            });

            // 다중 마커와 인포윈도우 표시
            // 위치 정보와 인포윈도우에 표시할 정도
            for(i = 0; i < size; i++) {
                // 다중 마커
                var marker = new daum.maps.Marker({
                    position: new daum.maps.LatLng(latitude[i], longitude[i])
                });
                // 마커 생성
                marker.setMap(map);
       
                // 인포 윈도우와 클릭 이벤트
                daum.maps.event.addListener(marker, 'click', (function(marker, i) {
                    return function() {
                        var infowindow = new daum.maps.InfoWindow({
                            content: '<p style="padding:15px;font:12px/1.5 sans-serif">' + '순서 : ' + i + '<br>' +'방위 : ' + course[i] + '</p>',
                            removable : true
                        });
                        // 인포 윈도우 생성
                      	infowindow.open(map, marker);
                    }
                })(marker, i));
            }
   
        };
		</script>
	</body>
</html>
<?php include "footer.php" ?>