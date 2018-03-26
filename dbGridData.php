<?php
        $servername = "162.241.217.12";
        $username = "nuinstig_goat";
        $password = "kzzgBq_o]uVF";
        $database = "nuinstig_goats";
        $port = "3306";
        
        $dat = array();
        
        $conn = mysqli_connect($servername, $username, $password, $database, $port);
        
        if(!$conn){
                die("Connection Failed: " . mysqli_connect_error());
        }
        
        $sql = "SELECT * FROM `locations`";
        
        $result = $conn->query($sql);
        
        if ($result->num_rows > 0){
                while ($row = $result->fetch_assoc()){
                    echo '[,' . $row["health_change"] . ", " . $row["plant_type"]
                        . ", " . $row["x_coord"] . ", " . $row["y_coord"] . ", " . $row["location_no"] . ",]-" ;
                }
        }
?>