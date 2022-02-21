<?php 
    $host = "localhost";
    $user = "root";
    $pass = "";
    $db = "casino";
    
    $conn = mysqli_connect($host, $user,$pass,$db);
    if ($_POST['action'] == "create_profile"){
        $player_name = mysqli_real_escape_string($conn, $_POST['player_name']);
        $player_id = mysqli_real_escape_string($conn, $_POST['userid']);
        $sql = "INSERT INTO profile (userid,username,points,profile_make) VALUES ('$player_id','$player_name',500,NOW())";
        $insert = mysqli_query($conn,$sql);
        
    }
    if ($_POST['action'] == "submoney"){
        $player_id = mysqli_real_escape_string($conn, $_POST['player_id']);
        $money = mysqli_real_escape_string($conn, $_POST['money']);
        $sql = "UPDATE profile SET points = points - $money WHERE userid = '$player_id'";
        $insert = mysqli_query($conn,$sql);
    }
    if ($_POST['action'] == "addmoney"){
        $player_id = mysqli_real_escape_string($conn, $_POST['userid']);
        $money = mysqli_real_escape_string($conn, $_POST['money']);
        $sql = "UPDATE profile SET points = points + $money WHERE userid = '$player_id'";
        $insert = mysqli_query($conn,$sql);
    }
    if($_POST['action'] == "userdata"){
        $player_id = $conn->real_escape_string($_POST['player_id']);
        $select = $conn->query("SELECT * FROM profile WHERE userid = '$player_id'");
        $row = $select->num_rows;
        if($row == 1){
            $data = $select->fetch_assoc();
            $myObj = new stdClass();
            $myObj->found = "Yes";
            $myObj->money = $data['points'];
            $myJSON = json_encode($myObj);
            echo $myJSON;
        }else{
            $myObj = new stdClass();
            $myObj->found = "No";   
        }
    }
?>