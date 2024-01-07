#!C:\xampp\perl\bin\perl.exe
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

my $q = CGI->new;

my $year = $q->param("year");

print $q->header('text/html');
print <<HTML;
<!DOCTYPE html>
<html lang="es">
<html>
<head>
  <title>Consulta 4</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" type="text/css" href="../styles.css">
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }

    h1 {
      color: #4285f4;
    }

    table {
      border-collapse: collapse;
      width: 100%;
      font-size: 14px;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #dddddd;
      text-align: center;
      padding: 8px;
    }

    th {
      background-color: #f2f2f2;
    }
    .not {
      text-align: center;
      font-size: 15px;
      color: red;
    }
    .yes {
      text-align: center;
      margin: 15px;
      font-size: 13px;
      color: green;
    }
    .c {
      max-height: auto;
      max-width: 80%;
      margin: 50px auto;
      text-align: center;
      background-color: white;
      padding: 20px;
      border-radius: 40px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .res {
      text-align: center;
      margin: 15px;
      font-size: 20px;
      color: black;
    }
  </style>
</head>
<body>
<div class="c">
  <h1>Resultado de su consulta</h1>
  <h1 class="res">Pel&iacute;culas del a&ntilde;o:  $year</h1>
HTML

#Conexion con la base de datos
my $user = 'root';
my $password = 'bugha15';
my $host = "localhost";
my $db = "pw_10";
my $mysql = DBI->connect("DBI:mysql:$db;host=$host", $user, $password);

#Verificar conexion
if ($mysql) {
  print<<HTML;
  <h2 class="yes">Conexi&oacute;n a la base de datos exitosa</h2>
HTML
} else {
  print <<HTML;
  <h2 class="not">Error al conectar a la base de datos</h2>
HTML
}

#Consulta a la base de datos
my $query = $mysql->prepare("SELECT * FROM Movie WHERE Year = ?");	
$query->execute($year);

#Verificar consulta
if ($query) {
  print <<HTML;
  <h2 class="yes">Consulta realizada correctamente</h2>
HTML
} else {
  print <<HTML;
  <h2 class="not">Error en la consulta: $mysql->errstr</h2>
HTML
}
my $resultados_encontrados = 0;
while (my $row = $query->fetchrow_hashref) {
  $resultados_encontrados = 1;  
}

if ($resultados_encontrados) {
  print<<HTML;
  <table>
    <thead>
      <tr>
        <th>TITLE</th>
        <th>YEAR</th>
        <th>SCORE</th>
        <th>VOTES</th>
      </tr>
    </thead>
    <tbody>
HTML
  my $query = $mysql->prepare("SELECT * FROM Movie WHERE Year = ?");	
  $query->execute($year);
  while (my $row1 = $query->fetchrow_hashref) {
    print <<HTML;
      <tr>
        <td>$row1->{Title}</td>
        <td>$row1->{Year}</td>
        <td>$row1->{Score}</td>
        <td>$row1->{Votes}</td>
      </tr>
HTML
      } 
} else {
  print <<HTML;
    <h2 class="not">No se encontraron resultados para el a&ntilde;o $year</h2>
HTML
}


# Finalizar la tabla y el HTML
print <<HTML;
    </tbody>
  </table>
</body>
</html>
HTML


#Finalizamos
$query->finish;
$mysql->disconnect;