<?php
        $servername = "162.241.217.12";
        $username = "nuinstig_goat";
        $password = "kzzgBq_o]uVF";
        $database = "nuinstig_goats";
        $port = "3306";
		$loc_no = $_POST['loc'];
        
        $conn = mysqli_connect($servername, $username, $password, $database, $port);
        
        if(!$conn){
                die("Connection Failed: " . mysqli_connect_error());
        }
        
        $sql = "SELECT * FROM measurements where `location_no`=".$loc_no." ORDER BY tstamp ASC LIMIT 7";
        
        $result = $conn->query($sql);
        
        if ($result->num_rows > 0){
                while ($row = $result->fetch_assoc()){
                    echo '[,' . $row["tstamp"] . "," . $row["insects_present"] . "," . $row["ndvi_val"] . "," . $row["ir_val"] . "," . $row["healthy_leaf_count"] . "," . $row["unhealthy_leaf_count"] . ",];";
                }
        }
?>