<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/css/bootstrap.min.css" integrity="sha384-Smlep5jCw/wG7hdkwQ/Z5nLIefveQRIY9nfy6xoR1uRYBtpZgI6339F5dgvm/e9B" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>My Tournament</h1>
    {{tournament}}
    % for team in tournament['teams']:
    <br>
    {{team}}



    %end
<div class="container column">
<br>
<h2>Registered Teams</h2>
<br>

<table id="myTable" class="table table-light table-striped">
  <thead class="thead-dark">
  <tr>
    <th scope="col" width="10">#</th>
    <th scope="col" width="45%">Team Name</th>
    <th scope="col" width="35%">Registration Status</th>
    <th scope="col" width="10%">Manage</th>
  </tr>
  </thead>
  <tbody id="myTable" align="center">
  %counter = 1
  %for team in tournament['teams']:
    <tr>
    <td>{{counter}}</td>
    <td>{{team['name']}}</td>
    <td>{{team['tournament_status']}}</td>
    <td><button class="btn btn-secondary btn-lg" role="button">Kick</button><button class="btn btn-secondary btn-lg" role="button">Reorder Up</button></td>
    %counter+=1
  </tr>
  %end
  <tbody>
</table>
</div>





    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/js/bootstrap.min.js" integrity="sha384-o+RDsa0aLu++PJvFqy8fFScvbHFLtbvScb8AjopnFD+iEQ7wo/CG0xlczd+2O/em" crossorigin="anonymous"></script>
  </body>
</html>