<DOCTYPE! html>
<head>
	<title>Tournament Home Page</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-1.3.2.min.js"></script>
    <script type="text/javascript" src="https://unpkg.com/jquery-bracket@0.11.1/dist/jquery.bracket.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/jquery-bracket@0.11.1/dist/jquery.bracket.min.css"/>
    <link href="https://fonts.googleapis.com/css?family=Varela+Round" rel="stylesheet">
    <style type="text/css">
            html,
            body {
                    background-repeat: no-repeat;
                    background-size: cover;
                    height: 100%;
                    font-family: 'Varela Round', sans-serif;
                 }
            .col-centered {
                margin: 0 auto;
                float: none;
                }


            .movebutton {
                position: relative;
                bottom: 12px;
            }

            .movefont {
                position: relative;
                bottom: 4px;
            }
            .btn-sq {
                width: 50px !important;
                height: 50px !important;
                font-size: 30px;
            }

        </style>
</head>


<body>



<div class="row">
<div class="col-md-4" align="center">


<div class="jumbotron column centered" align="center">
	<h1 class="display-4">{{tournament['name']}}</h1>
 	<p class="lead">Hosted by {{tournament['host']}}.</p>
  	<hr class="my-4">
  		<p align="center">
  			<b>About:</b> {{tournament['about']}}
            <br>
			<b>Start Date:</b> {{tournament['start_date'] + " (UTC)"}}
            <br>
			<b>Rewards:</b> {{tournament['rewards']}}
            <br>
			<b>Type:</b> Double Elimination
            <br>
			<b>Entry Price:</b> {{tournament['entry_price']}}
            <br>
			<b>Region:</b> {{tournament['region']}}
		</p>

		%if tournament['host_uuid'] == player['uuid']:
		    <form class="lead" action="/manage-tournament" method="get">
    	        <button class="btn btn-info btn-lg" role="button">Manage Tournament</button>
            </form>
    	%elif (player['tournament_status'] == 'none') and (player['team_status'] == 'captain'):
    		 <form class="lead" action="/tournament/register" method="get">
    	        <button class="btn btn-primary btn-lg" role="button">Register for Tournament</button>
            </form>

    	%end

    	%if (current_time) and (player['tournament_status'] == 'registered' and player['team_status'] == 'captain') : #this is checking if the tournament has started, and can change the tournament status accordingly also should check if the person a captain
    	        <form class="lead" action="/tournament/check_in" method="get">
                     <button class="btn btn-primary btn-lg" role="button">Check-in Team</button>
                </form>
        %end

    	<a class="btn btn-secondary btn-lg" href="/home" role="button">Back Home</a>
        <br>

</div>
</div>
<div class="col-md-8" align="center">
<br>
<br>

%if player['tournament_id'] == tournament['id']:

<div class="alert alert-success" role="alert">
<h2 align="left">Current Status: {{player_team["tournament_status"]}}</h2><br>
  You are registered for this tournament. <br>
  Your next opponent is : {{player_team['next_opponent']['name']}}<br>
  Their members are:
   %for i in range(len(player_team['next_opponent']['names'])):
        {{player_team['next_opponent']['names'][i]}}
        %if i < (len(player_team['next_opponent']['names']) - 1):
            -
        %end
    %end
<br>
  Friend them in-game and start a private party match. It doesn't matter who is on which side, as long as all the teammates are the same. <br>
  You should begin the match by :  {{player_team['last_match_time']}}

</div>
%else:

<div class="alert alert-success" role="alert">
<h2 align="left">Current Status:</h2><br>
  You aren't registered. Create a team and join a tournament, or host your own tournament.
</div>
%end

<br>
<br>

<h2 align="left">Bracket:</h2>
<script>
var bigData = {
  teams : {{!bracket_teams}},
  results : {{!matches}}
}
$(function() { $('.demo').bracket({init: bigData}) })
</script>

<div class='demo' align="center"></div>

<script>
var resizeParameters = {
  teamWidth: 130,
  scoreWidth: 30,
  matchMargin: 30,
  roundMargin: 60,
  init: bigData
};

function updateResizeDemo() {
  $('.demo').bracket(resizeParameters);
}

$(updateResizeDemo)
</script>

</div>
</div>
<br>
<br>
<h2 align="left" style="padding-left:5em">Registered Teams:</h2
<br>

<table id="myTable" class="table table-light table-striped">
  <thead class="thead-dark">
  <tr>
    <th scope="col" width="10%">#</th>
    <th scope="col" width="20%">Team Name</th>
    <th scope="col" width="35%">Players</th>
    <th scope="col" width="10%">Tier</th>
    <th scope="col" width="25%">Registration Status</th>
  </tr>
  </thead>
  <tbody id="myTable" align="center">
  %counter = 1
  %for team in teams:
    <tr>
    <td>{{counter}}</td>
    <td>{{team['name']}}</td>
    <td>
    %for i in range(len(team["names"])):
        {{team["names"][i]}}
        %if i < (len(team["names"]) - 1):
            -
        %end
    %end

    </td>
    <td>{{team['tier']}}</td>
    <td>{{team['tournament_status']}}</td>
    %counter+=1
  </tr>
  %end
  <tbody>
</table>

<script>
var number = 0;
function fn60sec() {
    number += 1;
    console.log(number);
    $.ajax({
    type: "get",
    url: "/update-tournament/" + {{tournament['id']}}

});


}
fn60sec();

</script>


</body>
</html>