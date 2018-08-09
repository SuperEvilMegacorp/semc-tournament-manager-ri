<!DOCTYPE HTML>
<html>
  <head>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/css/bootstrap.min.css"
	integrity="sha384-Smlep5jCw/wG7hdkwQ/Z5nLIefveQRIY9nfy6xoR1uRYBtpZgI6339F5dgvm/e9B" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/css/bootstrap-datetimepicker.min.css">

    <style type="text/css">
        html,
        body {
            height: 100%;

        }
        body {
        background: linear-gradient(#b3ccff,#c6d6ef);
        background-repeat: no-repeat;
        background-size: cover;
        }

    </style>

</head>

  <body>
    <h1 align="center"> Create Your Tournament </h1>
    <form action="/tournament" method="post" align="center">


        <div class="form-group" align="center">
            <label for="tournament_name">Tournament Name</label>
            <input style="width:440px;" required type="text" class="form-control" id="tournament_name" name="tournament_name" placeholder="">
        </div>


        <div class="form-group" align="center">
            <label for="about">About</label>
            <textarea required style="width:440px;" type="text" rows="3" class="form-control" id="about" name="about"></textarea>
        </div>


<div class="container" style="width:550px;">
<div class="row">
<div class="col-sm">
        <div class="form-group" align="center">
            <label for="game_type">Game Type</label>
            <select name="game_type" style="width:170px;" class="form-control select-small" id="exampleFormControlSelect1">
            <option value="3v3">3v3</option>
            <option value="5v5">5v5</option>
            <option value="blitz">Blitz</option>
            <option value="br">Battle Royale</option>
            </select>
        </div>
</div>
<div class="col-sm">
        <div class="form-group" align="center">
            <label for="rewards">Rewards</label>
            <select name="rewards" style="width:170px;" class="form-control select-small">
            <option value="None">None</option>
            <option value="Bronze Chest">Bronze Chest</option>
            <option value="Silver Chest">Silver Chest</option>
            <option value="Gold Chest">Gold Chest</option>
            </select>
        </div>
</div>
</div>
<div class="row">
<div class="col-sm">
        <div class="form-group" align="center">
            <label for="entry_price">Entry Price</label>
            <select name="entry_price" style="width:170px;" class="form-control select-small">
             <option value="None">None</option>
             <option value="Entry Ticket">Entry Ticket</option>
             <option value="1000 Glory">1000 Glory</option>
             <option value="30 ICE">30 ICE</option>
             <option value="100 ICE">100 ICE</option>
            </select>
        </div>
</div>
<div class="col-sm">
        <div class="form-group" align="center">
            <label for="number_of_teams">Number of Teams</label>
            <select name="number_of_teams" style="width:170px;" class="form-control select-small">
             <option value="4">4</option>
             <option value="8">8</option>
             <option value="16">16</option>
             <option value="32">32</option>
            </select>
        </div>
</div>
</div>
<div class="row">
<div class="col-sm">
        <div class="form-group" align="center">
            <label for="region">Region</label>
            <select name="region" style="width:170px;" class="form-control select-small">
             <option value="NA">NA</option>
             <option value="SA">SA</option>
             <option value="SEA">SEA</option>
             <option value="EU">EU</option>
             <option value="CN">CN</option>
            </select>
        </div>
    </div>
<div class="col-sm">


      <div class="form-group">
        <label for="start_date">Date and Time (UTC)</label>
        <div class='input-group date' id='datetimepicker1'>
          <input type='text' name="start_date" class="form-control" />
          <span class="input-group-addon" >
            <span class="glyphicon glyphicon-calendar"></span>
          </span>
        </div>
      </div>


    </div>
</div>
</div>
</div>

    <button class="btn btn-primary btn-lg" style="width:440px;"role="button" type="submit">Create</button>
   </form>


<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.15.1/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/js/bootstrap-datetimepicker.min.js"></script>

<script>$(function() {
   var help = '{{current_time}}'
  $('#datetimepicker1').datetimepicker( {format: 'Y-MM-DD HH:mm', defaultDate:help} );

});</script>

  </body>

<html>

