<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css"><title>Log in!</title>
    <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">
  </head>

<style type="text/css">

html,
body {
height: 100%;
}

h1 {
  font-family: "Lato";
  }

body {
background: linear-gradient(
 #020202,#020202,  transparent, transparent, transparent, #020202), url("https://jd3sljkvzi-flywheel.netdna-ssl.com/wp-content/uploads/2016/07/Halcyon-Lore1000px.jpg");
background-repeat: no-repeat;
background-size: cover;
}



</style>


  <body style="color:#c2c3c4;">

  <div class="text-center pagination-centered">
        <br>
        <h1><strong>Vainglory Tournament Manager</strong></h1>

            <p align="center">Welcome! Sign-up with your in-game username, and create a PIN lock for your account <br> If you have already logged in before, log in with your previous credentials.  credit to whoever drew this</p>
            <div>
            <form action="/login" method="post" class="form-inline" >

            <div class="form-group">
                <label for="exampleInputEmail1">Username:</label>
                <input  type="text" class="form-control" name="email" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter username">
                </div>
            <div class="form-group">
                <label for="exampleInputPassword1">PIN:</label>
                <input  type="password" class="form-control" name="password" id="exampleInputPassword1" placeholder="Enter pin">
                </div>
            <select  name="region" >
                <option value="NA">NA</option>
                <option value="EU">EU</option>
                <option value="SA">SA</option>
                <option value="SEA">SEA</option>
                <option value="CN">CN</option>
                </select>
            <button   value="/login" type="submit" class="btn btn-primary" >Submit</button>
            </div>
        </form>

    </body>

</html>
