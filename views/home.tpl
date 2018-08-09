<!DOCTYPE html>
<html lang="en">

    <head>
	    <title>Vainglory Tournament Home</title>
	    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <link rel="stylesheet" href="../home.css" type="text/css">
        <link href="https://fonts.googleapis.com/css?family=Varela+Round" rel="stylesheet">
        <style type="text/css">
            html,
            body {
                background: linear-gradient(#d2e0f7, #c5d8f7, #cfdef7);
                background-repeat: no-repeat;
                background-size: cover;
                height: 100%;
                font-family: 'Varela Round', sans-serif;
            }
            .col-centered {
                margin: 0 auto;
                float: none;
                }
            .col-md-4 {
                background: #e0e6ff;
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
        <br>
        <br>
        <br>
<div class="row">
<div class="col-md-4" align="center">
        <br>
        <br>


        %if tournament_status != 'hosting':
            <h1 align="center">Team Status</h1>


        %if team_status == "none":
            <div align="center">
                Create a New Team:
                <form action="/team" method="post" class="form-inline" align="center">
                    <div class="input-group mb-3 col-sm-12">
                        <input type="text" name="team_name" class="form-control" placeholder="Team Name">
                        <div class="input-group-append">
                            <button class="btn btn-primary btn-lg" type="submit">Create</button>
                        </div>
                    </div>
                </form>

                <br>
                Join An Existing Team:
                <form action="/join-team" method="post" class="form-inline" align="center">
                    <div class="input-group mb-3 col-sm-12">
                        <input type="text" name="team_id_request" class="form-control" placeholder="Team ID" >
                        <div class="input-group-append">
                            <button class="btn btn-primary btn-lg" type="submit">Join</button>
                        </div>
                    </div>
                </form>
            </div>
        %else:
            <div align="center">

                <strong>Name:</strong> {{ team['name'] }}
                <br>
                <strong>ID:</strong> {{ team['id'] }}

                <strong>Tier:</strong> {{ team['tier'] }}


                <table class="table table-dark table-hover table-striped table-bordered">
                    <thead align="center">
                        <tr>
                        <th class="active">Player Names</th>
                        <th class="active">Tier</th>
                        </tr>
                    </thead>
                %for player in team_players:
                    <tbody align="center">
                        <tr>
                        <td class="active">{{player['name']}}</td>
                        <td class="active">{{player['tier']}}</td>
                        </tr>
                    </tbody>
                %end
                </table>
            </div>
        %end


        <div align="center">
            %if team_status == "captain":
                <form class="lead" action="/disband-team" method="get">
    	            <button class="btn btn-secondary btn-lg" role="button">Disband Team</button>
                </form>

            %elif team_status == "team":
                <form class="lead" action="/leave-team" method="get">
    	            <button class="btn btn-secondary btn-lg" role="button">Leave Team</button>
                </form>
            %end

        </div>

        %end

    %if tournament_status == 'hosting':

        <h3>My Tournament Status</h3>
        <form action="/manage-tournament" method="get">
            <button type="submit" class="btn btn-info btn-lg">Manage Tournament</button>
        </form>

        <form action="/cancel-tournament" method="post">
            <button class="btn btn-secondary btn-lg" type="submit">Cancel Tournament</button>
        </form>

    %elif player['team_status'] == "none":
        <br>
    %end
    <br>
    <br>
</div>

<div class="col-md-8" align="center">
<form action="/create-tournament" method="get" align=center>
  <font size="+4">Open Tournaments </font>
            <button type="submit" class="btn btn-primary movebutton btn-sq"> <p class="movefont">+</p> </button>
        </form>
<br>
<table align="center" class="table table-lg table-hover table-light table-bordered">
   <thead>
   <th class="active">Tournament Name</th>
   <th class="active">Start Date/Time (24h UTC)</th>
   <th class="active">Region</th>
   <th class="active">Capacity</th>
   <th class="active">Game Type</th>
   <th class="active">Tournament Type</th>
   </thead>
%for tournament in tournaments:
  <tr align="center">
    % link = "/tournament/" + tournaments[tournament]['id']
    <td class="active"><a href= {{link}}> {{tournaments[tournament]['name']}} </a></td>
    <td class="active"> {{tournaments[tournament]['start_date']}}</td>
    <td class="active">{{tournaments[tournament]['region']}}</td>
    <td class="active">{{tournaments[tournament]['number_of_teams']}} / {{tournaments[tournament]['max_number_of_teams']}}</td>
    <td class="active">{{tournaments[tournament]['game_type']}}</td>
    <td class="active">{{tournaments[tournament]['tournament_type']}}</td>
  </tr>
%end
</table>

</div>
</div>
</div>

<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/js/bootstrap.min.js" integrity="sha384-o+RDsa0aLu++PJvFqy8fFScvbHFLtbvScb8AjopnFD+iEQ7wo/CG0xlczd+2O/em" crossorigin="anonymous"></script>


</body>

</html>
