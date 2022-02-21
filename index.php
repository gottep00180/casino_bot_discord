<?php 
    //PHP API FOR CASINO BOT
    //DEVELOP ON XAMPP 
    //กำหนดตัวแปรต่างๆ เพื่อทำการเชื่อมต่อกำฐานข้อมูล
    $host = "localhost"; //ที่อยู่ฐานข้อมูล
    $user = "root"; //username ที่จะใช้เข้าถึงฐานข้อมูล หากใช้ xampp ค่าเดิมคือ root
    $pass = ""; //password ฐานข้อมูล หากใช้ xampp ค่าเดิมจะไม่มี password ทิ้งไว้แบบนี้ได้เลย
    $db = "casino"; //ชื่อ database ในกรณีนี้ชื่อ casino 
    //กำหนดตัวแปรที่ใช้เชื่อมต่อฐานข้อมูล
    $conn = mysqli_connect($host, $user,$pass,$db);
    //หากมีการขอสร้างโปรไฟล์ให้ผู้เล่น
    if ($_POST['action'] == "create_profile"){
        //กำหนดตัวแปรเกี่ยวกับข้อมูลผู้เล่น
        $player_name = mysqli_real_escape_string($conn, $_POST['player_name']);
        $player_id = mysqli_real_escape_string($conn, $_POST['userid']);
        //เพิ่มข้อมูลผู้เล่นลงฐานข้อมูล
        $sql = "INSERT INTO profile (userid,username,points) VALUES ('$player_id','$player_name',500)";
        $insert = mysqli_query($conn,$sql);
        
    }
    //api หักเงินผู้เล่น
    if ($_POST['action'] == "submoney"){
        //id ผู้เล่นที่จะหักเงิน
        $player_id = mysqli_real_escape_string($conn, $_POST['player_id']);
        //จำนวนเงินที่จะหัก
        $money = mysqli_real_escape_string($conn, $_POST['money']);
        //sql หักเงินผู้เล่น
        $sql = "UPDATE profile SET points = points - $money WHERE userid = '$player_id'";
        $insert = mysqli_query($conn,$sql);
    }
    //api เพิ่มเงินให้กับผู้เล่น
    if ($_POST['action'] == "addmoney"){
        //ตรงนี้เหมือนกันกับ api หักเงินเพียงแต่ เปลี่ยนจาก - เป็น + ครับ
        $player_id = mysqli_real_escape_string($conn, $_POST['userid']);
        $money = mysqli_real_escape_string($conn, $_POST['money']);
        $sql = "UPDATE profile SET points = points + $money WHERE userid = '$player_id'";
        $insert = mysqli_query($conn,$sql);
    }
    //เช็คข้อมูลผู้เล่น
    if($_POST['action'] == "userdata"){
        //ตรงนี้ไม่ต้องตกใจครับผมแค่เปลี่ยนวิธีการเขียนให้มันสั้นกว่าเดิมเฉยๆ หลักการทำงานเหมือนเดิมคับ
        //กำหนด id ผู้เล่นที่ต้องการหา
        $player_id = $conn->real_escape_string($_POST['player_id']);
        //ทำการหาข้อมูลผู้เล่น
        $select = $conn->query("SELECT * FROM profile WHERE userid = '$player_id'");
        //ตัวแปร row ก็คือการนับว่าเจอกี่ตัว
        //ตัวแปร row ก็เหมือนกับการหาคนนั่นแหละครับ ถ้าเราจะหาคนชื่อต้น ใน สวนสาธารณะ ถ้าเราจะหาโดยใช้ข้อมูลแค่ว่า คนนั้นชื่อต้น
        //เราอาจจะเจอต้น หลายคน ก็เหมือนกับเจอ row หลาย row นั่นแหละครับ
        $row = $select->num_rows;
        //หากเจอ row หรือ คนที่เรากำลังตามหา 1 คน ทำไมต้องเป็น 1 เพราะ 1 คน มีแค่ 1 ข้อมูลครับ หากเจอมากกว่า 1 แสดงว่าโค้ดพังครับ55555
        if($row == 1){
            //ทำการ fetch ข้อมูลออกมา (เอาข้อมูลของ player มาเก็บในตัวแปร data) 
            $data = $select->fetch_assoc();
            //เริ่มใช้ json
            $myObj = new stdClass();
            //ค่า found ใช้กำหนดว่าเราเจอข้อมูลหรือไม่ Yes คือเจอ No คือไม่เจอ
            $myObj->found = "Yes";
            //ค่า money คือเงินของผู้เล่น
            $myObj->money = $data['points'];
            //ทำการ encode json จำเป็นต้อง encode เพื่อที่จะให้ python load json ออกมาได้
            $myJSON = json_encode($myObj);
            //ทำการแสดงค่า json 
            echo $myJSON;
        }else{
            //หากไม่เจอข้อมูลเลย 
            $myObj = new stdClass();
            $myObj->found = "No";   
            //ทำการ encode json จำเป็นต้อง encode เพื่อที่จะให้ python load json ออกมาได้
            $myJSON = json_encode($myObj);
            //ทำการแสดงค่า json 
            echo $myJSON;
            
        }
    }
?>
