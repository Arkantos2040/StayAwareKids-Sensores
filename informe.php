<?php
//echo date("H:i");
$watt= $_GET["watt"];
$caso= $_GET["caso"];
$costo= $_GET["costo"];
$anio= $_GET["anio"];
$fechamin = $_GET["fechamin"];
$fechamax = $_GET["fechamax"];
$valorkhw = $_GET["valorkwh"];
$valortrans = $_GET["valortrans"];
$valoradmin = $_GET["valoradmin"];

//casos posibles de solicitudeds
switch($caso){
  case "2":
    casoPotenciaActual();
    break;
  case "3":
    casoConsumoPorDia();
    break;
  case "4":
    casoConsumoPorMes($anio);
    break;
  case "5":
    casoValores();
    break;
  case "6":
    casoConsumoPromedio($fechamin, $fechamax);
    break;
  case "7":
    casoUpdateValores($valorkhw, $valortrans, $valoradmin);
    break;
  case "8":
    casoSensoresCondensacion();
    break;
  case "9":
    casoUsuario();
    break;
}

//regresa los datos del Usuario
function casoUsuario(){
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    //$conn = conexion();
    $sql = "SELECT idUsuario, idSensor, Nombre FROM `USUARIO`";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["idUsuario"].",".$row["idSensor"].",".$row["Nombre"];
        }
    } else {
        echo "Error 12";
    }
    $conn->close();
}

//retorna todos los datos de los sensores
function casoSensoresCondensacion(){
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT * FROM `CONDENSACION` ORDER BY idsensor";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["idsensor"].",". $row["temperatura"].",". $row["humedad"].",".$row["ventana"].";";
        }
    } else {
        echo "Error 11";
    }
    $conn->close();
}

//modifica la tabla valores
function casoUpdateValores($valorkhw, $valortrans, $valoradmin){
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connevction
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "UPDATE VALOR SET valorkwh = '$valorkhw', valortransporte = '$valortrans', valoradministracion = '$valoradmin' WHERE idvalor = 1";
    if ($conn->query($sql) === TRUE) {
   	 echo "Modificación de registros exitosa";
    } else {
    	echo "Error modificacion: " . $conn->error;
    }
    $conn->close();
}

//retorna promedio de los ultimos 3 meses
function casoConsumoPromedio($fechamin, $fechamax){
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT ROUND(SUM(costo)/count(fecha)) as promedio FROM `POTENCIA_POR_MES` WHERE fecha BETWEEN '$fechamin' and '$fechamax'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["promedio"];
        }
    } else {
        echo "ERROR 10";
    }
    $conn->close();
}


//regresa los datos utilizados para realizar el calculo de los costos
function casoValores(){
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    //$conn = conexion();
    $sql = "SELECT * FROM `VALOR` WHERE idvalor=1";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["valorkwh"].",".$row["valortransporte"].",".$row["valoradministracion"];
        }
    } else {
        echo "Error 4";
    }
    $conn->close();
}

//regressa el informe del dia actual
function casoPotenciaActual(){ //Android
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    //$conn = conexion();
    //$sql = "SELECT * FROM `POTENCIA_TEMP`"; //falta ingreso de id usuario
    $sql = "SELECT SUM(kwatt) as kwatt FROM `POTENCIA_POR_DIA`";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["kwatt"];
        }
    } else {
        echo "Error 9";
    }
    $conn->close();
}

//retorna todos los dias del mes actual
function casoConsumoPorDia(){
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT DAY(fecha) as dia, kwatt, costo FROM `POTENCIA_POR_DIA` ORDER BY fecha";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["dia"].",". $row["kwatt"].",".$row["costo"].";";
        }
    } else {
        echo "Error 8";
    }
    $conn->close();
}

//retorna todos los meses
function casoConsumoPorMes($anio){ //Android
    // Create connection
    $conn = new mysqli("localhost", "root", "efficient", "efficientbd");
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT MONTH(fecha) as mes, kwatt, costo FROM `POTENCIA_POR_MES` WHERE YEAR(fecha)='$anio' order by MONTH(fecha)";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo $row["mes"].",".$row["kwatt"].",".$row["costo"].";";
        }
    } else {
        echo $result;
    }
    $conn->close();
}


?>