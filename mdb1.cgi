#!C:\xampp\perl\bin\perl.exe
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

my $q = CGI->new;

print $q->header('text/html');
print <<HTML;
<!DOCTYPE html>
<html lang="es">
<html>
<head>
  <title>Consulta 1</title>
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
    .button {
      background-color: #4285f4;
      color: white;
      border: none;
      padding: 10px 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      cursor: pointer;
      border-radius: 24px;
      margin: 5px;
    }
  </style>
</head>
<body>
<div class="c">
  <h1>Resultado de la consulta de Actor por ID</h1>

  <!-- Formulario para agregar actor -->
  <form method="post" action="">
    <input type="hidden" name="action" value="add_actor">
    <input type="submit" value="Agregar Actor con ID 5" class="button">
  </form>

  <!-- Formulario para eliminar actor -->
  <form method="post" action="">
    <input type="hidden" name="action" value="delete_actor">
    <input type="submit" value="Eliminar Actor con ID 5" class="button">
  </form>

HTML

# Conexi&oacute;n con la base de datos
my $user     = 'root';
my $password = 'bugha15';
my $host     = "localhost";
my $db       = "pw_10";
my $mysql    = DBI->connect("DBI:mysql:$db;host=$host", $user, $password);

# Verificar conexi&oacute;n
if ($mysql) {
    print<<HTML;
    <h2 class="yes">Conexi&oacute;n a la base de datos exitosa</h2>
HTML
} else {
    print <<HTML;
    <h2 class="not">Error al conectar a la base de datos</h2>
HTML
}

# Verificar si se hizo clic en el bot&oacute;n de agregar actor
if ($q->param("action") eq "add_actor") {
    # Realizar la inserci&oacute;n del actor con ID 5
    my $sth = $mysql->prepare("INSERT INTO Actor(ActorID, Name) VALUES (?, ?)");
    $sth->execute(5, "Speed Racer");
    print <<HTML;
    <h2 class="yes">Actor con ID 5 agregado correctamente</h2>
HTML
}

# Verificar si se hizo clic en el bot&oacute;n de eliminar actor
elsif ($q->param("action") eq "delete_actor") {
    # Realizar la eliminaci&oacute;n del actor con ID 5
    my $sth = $mysql->prepare("DELETE FROM Actor WHERE ActorID = ?");
    $sth->execute(5);
    print <<HTML;
    <h2 class="yes">Actor con ID 5 eliminado correctamente</h2>
HTML
}

# Consulta a la base de datos
my $actor_id = 5;
my $query = $mysql->prepare("SELECT * FROM Actor WHERE ActorID = ?");    
$query->execute($actor_id);

# Verificar consulta
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
my $actor_nombre;

while (my $row = $query->fetchrow_hashref) {
    $resultados_encontrados = 1;
    $actor_nombre = $row->{Name};
}

if ($resultados_encontrados) {
    print<<HTML;
    <h2 class="res">Nombre del actor con ID $actor_id: $actor_nombre</h2>
HTML
} else {
    print <<HTML;
    <h2 class="not">No se encontr&oacute; actor con ID $actor_id</h2>
HTML
}

# Finalizar el HTML
print <<HTML;
</div>
</body>
</html>
HTML

# Finalizamos
$query->finish;
$mysql->disconnect;