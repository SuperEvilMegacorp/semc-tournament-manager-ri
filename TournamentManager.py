from bottle import Bottle, route, run, template, get, post, put, delete, request, response, error, redirect
import json
import requests
import sys
sys.path.append("/Users/vera.wang/Development/Projects/Evil_Trunk/Development/Trunk/Platform/Source")
import ServerUtils
from TimeUtils import *
from datetime import datetime, timedelta
import time

app = Bottle()
time = isoNow()

@app.get('/')
def start_login():
    return template("login.tpl")

@app.post('/login')
def handle_login():
    username = request.forms.get('email')
    password = request.forms.get('password')
    region = request.forms.get('region').lower()
    def login(username, password):

        if username + "_" + password not in test_users:
            url = "https://api.dc01.gamelockerapp.com/shards/" + region + "/players"
            header = {
                "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNWQxNTdkMC02ZGMzLTAxMzYtNGIyMi0wYTU4NjQ2MGZjMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTMyMDMzNzE1LCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJ0b3VybmFtZW50LW1hbmFnZXIiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.Cu1aGjGEQTkubF6BqJmm-ogJlx6lj2qCLuWXzDS5OLM",
                "Accept": "application/vnd.api+json",
                "Accept-Encoding": "gzip"
            }
            query = {
                "filter[playerNames]": username
            }
            r = requests.get(url, headers=header, params=query)
            resp = r.json()
            print(resp)
            assert resp['data'][0]['type'] == "player"
            if resp['data'][0]['attributes']['stats']['level'] < 10:
                print("YOU MUST BE HIGHER LEVELED THAN 10")
            test_users[username + "_" + password] = {
                "uuid" : username + "_" + password,
                "name" : username,
                "tier" : resp['data'][0]['attributes']['stats']['skillTier'],
                "hosting" : False,
                "tournament_id": '0',
                'team_id': '0',
                "team_status": "none",
                "tournament_status": "none"
            }
            response.set_cookie('uuid', username + "_" + password, secret="a")
            response.set_cookie('username', username, secret="a")
        else:
            response.set_cookie('uuid', username + "_" + password, secret="a")
            response.set_cookie('username', username, secret="a")


    def dummy_login(username, password):
        response.set_cookie('uuid', username, secret="a")
        response.set_cookie('username', username,  secret="a")

    if True:
        login(username, password)
        redirect('/home')
    else:
        return "<p>Login failed.</p>"

def create_account_for_player():
    pass

def find_player_region():
    pass
'''
Player Structure: (these are all Strings unless otherwise specified)
uuid                :   The key to find the player, a main identifier.
name                :   The player's name.
team_id             :   The key to find the team the player is associated with.
                            If the player doesn't have a team then the team_id is "none".
team_status         :   "none" for no team, "team" for team member, "captain" for team owner.
tournament_id       :   Key for the tournament the player is associated with.
tournament_status   :   "none" no tournament, "hosting" for hosting, "registered" for registered in a tournament
                        but not checked in currently.
                        "idle" for in a tournament but waiting for next match, "matched" for in a match
'''

def get_player_id():
    return request.get_cookie('uuid', secret='a')
def get_player(player_id):
    return test_users[player_id]

def get_team_status(player_id): # options: "none", "team", "captain"
    return get_player(player_id)['team_status']
def get_team_id(player_id): # options: "0" for no team, else "a string of any other integer"
    return get_player(player_id)['team_id']
def get_team(team_id):
    return test_teams[team_id]
def get_player_team(player_id):
    return get_team(get_team_id(player_id))
def set_team_status(uuid, team_status):
    get_player(uuid)['team_status'] = team_status

def get_tournament_status(player_id): # options: "none", "hosting", "registered", "ready", "in_match"
    return get_player(player_id)['tournament_status']
def get_tournament_id(player_id): # options: "0" for no team, else "a string of any other integer"
    return get_player(player_id)['tournament_id']

def get_tournament(tournament_id):
    return test_tournaments[tournament_id]

'''
 skaarfs_tournament = {
        'id' : '999',
        'name' : "Skaarf's Tourney",
        "start_date" : "03/07/2018 13:43:15",
        "rewards" : "Gold Chest",
        "entry_price" : "1000 Glory",
        "number_of_teams" : 1,
        "max_number_of_teams" : 1000,
        "teams" : [team1, team2, team3, team4],

        "game_type" : "3v3",
        "tournament_type" : "Double-Elimination",
        "region" : "NA",
        "about" : "Rawr zzzzz",
        "host" : "Skaarf",
        "host_uuid" : "9000",
        "status" : "idle",
        "matches" : [
    [[1,0,'Match 1'], [0,1,'Match 2']],
    [[0,1,'Final'], [1,0,'Consolation final']]
  ]
    }
Tournament Structure: (these are all Strings unless otherwise specified)
id - The identifier for this tournament
name - The name for the tournament
start_date - when the tournament starts
teams - a list of teams
'''


def get_ids_of_last_matches(player_name, region):
    print("Am searching for last 3 matches for " + player_name + " in " + region + "... beep boop.")
    url = "https://api.dc01.gamelockerapp.com/shards/" + region + "/matches?page[limit]=3&page[offset]=0"
    header = {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNWQxNTdkMC02ZGMzLTAxMzYtNGIyMi0wYTU4NjQ2MGZjMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTMyMDMzNzE1LCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJ0b3VybmFtZW50LW1hbmFnZXIiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.Cu1aGjGEQTkubF6BqJmm-ogJlx6lj2qCLuWXzDS5OLM",
        "Accept": "application/vnd.api+json",
        "Accept-Encoding": "gzip"
    }
    query = {
        "sort" : "-createdAt",
        "filter[playerNames]": player_name
    }
    r = requests.get(url, headers=header, params=query)
    print(r)
    ids = []
    for i in range(3):
        try:
             ids.append(r.json()['data'][i]['id'])
        except KeyError:
            print("KeyError: There aren't any matches. Tried: " + str(i))
            break
        except ValueError:
            print("ValueError: the api isn't working this time, refresh")
            break
    return ids

def get_match_json(match_id, region):
    url = "https://api.dc01.gamelockerapp.com/shards/" + region + "/matches/" + match_id
    header = {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNWQxNTdkMC02ZGMzLTAxMzYtNGIyMi0wYTU4NjQ2MGZjMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTMyMDMzNzE1LCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJ0b3VybmFtZW50LW1hbmFnZXIiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.Cu1aGjGEQTkubF6BqJmm-ogJlx6lj2qCLuWXzDS5OLM",
        "Accept": "application/vnd.api+json",
        "Accept-Encoding": "gzip"
    }
    r = requests.get(url, headers=header)
    try:
        return r.json()
    except ValueError:
        print("_______cannot get this match json")

def get_match_participant_ids(match_json):
    winning_team = []
    losing_team = []
    if match_json == None:
        print("NONE")
        return {}
    for obj in match_json['included']:
        if obj['type'] == 'roster' and obj['attributes']['won'] == 'true':
            for participant in obj['relationships']['participants']['data']:
                winning_team.append(participant['id'])

        if obj['type'] =='roster' and obj['attributes']['won'] == 'false':
            for participant in obj['relationships']['participants']['data']:
                losing_team.append(participant['id'])
    return {
        "winning_team" : winning_team,
        "losing_team" : losing_team
    }

def get_match_player_ids(match_json):
    winning_team = []
    losing_team = []
    for participant_id in get_match_participant_ids(match_json)['winning_team']:
        for obj in match_json['included']:
            if obj['id'] == participant_id and obj['type'] == 'participant':
                winning_team.append(obj['relationships']['player']['data']['id'])
    for participant_id in get_match_participant_ids(match_json)['losing_team']:
        for obj in match_json['included']:
            if obj['id'] == participant_id and obj['type'] == 'participant':
                losing_team.append(obj['relationships']['player']['data']['id'])
    return {
        "winning_team" : winning_team,
        "losing_team" : losing_team
    }

def get_match_player_names(match_json):
    winning_team = []
    losing_team = []
    for player_id in get_match_player_ids(match_json)['winning_team']:
        for obj in match_json['included']:
            if obj['type'] == 'player' and obj['id']==player_id:
                winning_team.append(obj['attributes']['name'])
    for player_id in get_match_player_ids(match_json)['losing_team']:
        for obj in match_json['included']:
            if obj['type'] == 'player' and obj['id']==player_id:
                losing_team.append(obj['attributes']['name'])
    return {
        "winning_team" : [player.encode('UTF8') for player in winning_team],
        "losing_team" : [player.encode('UTF8') for player in losing_team]
    }

def get_match_json_start_time(match_json):
    return match_json['data']['attributes']['createdAt']

def get_match_id_start_time(match_id, region):
    return get_match_json_start_time(get_match_json(match_id, region))

def get_match_json_duration(match_json):
    return match_json['data']['attributes']['duration']

def get_match_id_duration(match_id, region):
    return get_match_json_duration(get_match_json(match_id, region))

def later_than_current_time(time):
    return datetime.utcnow().isoformat() < time

def tournament_utc_time_to_iso8601(time):
    return time[:10] + "T" + time[11:] + "00Z"

def time_within_range(current_time, range_start_time, range_end_time):
    return (range_start_time <= current_time) and (current_time <= range_end_time)

def current_time_within_range(range_start_time, range_end_time):
    current_time = datetime.utcnow().isoformat().replace("T", " ")
    print(current_time)
    return (range_start_time < current_time) and (current_time < range_end_time)

def is_match_json_valid(match_json, team1_players, team2_players, range_start_time, range_end_time):
    import datetime
    player_names = get_match_player_names(match_json)
    winning_team = [player.encode('UTF8') for player in player_names['winning_team']]
    losing_team = [player.encode('UTF8') for player in player_names['losing_team']]
    current_time = datetime.datetime.utcnow().isoformat().replace("T", " ")[:16]
    print("     Here are our 1 players" + str(team1_players))
    print("     Here are our 2 players" + str(team2_players))
    print("         winning team from the match json" + str(winning_team))
    print("         losing team from the match json" + str(losing_team))
    if not time_within_range(current_time, range_start_time, range_end_time):
       return {
            "valid" : "false",
            "error" : "not within time range"
            }
    if (set(winning_team) == set(team1_players)) and (set(losing_team) == set(team2_players)):
        return {
            "valid" : "true",
            "winning_team" : team1_players,
            "losing_team" : team2_players
        }
    elif (set(winning_team) == set(team2_players)) and (set(losing_team) == set(team1_players)):
        return {
            "valid": "true",
            "winning_team": team2_players,
            "losing_team": team1_players
        }
    else:
        return {
            "valid": "false",
            "error": "player names incorrect"
        }

def check_if_match_submitted(team1_players, team2_players, range_start_time, range_end_time, region):
    match_ids = get_ids_of_last_matches(team1_players[0], region)
    for id in match_ids:
        json = get_match_json(id.encode('UTF8'), region)
        match_data = is_match_json_valid(json, team1_players, team2_players, range_start_time, range_end_time)
        if match_data['valid'] == 'true':
            return match_data
        else:
            print(match_data['error'])
    return {'valid' : 'false',
            'error' : 'no match json is valid'}

def update_teams_in_tournament(tournament):
    for team in tournament['teams']:
        print("!!!!!! UPDATING TEAM " + str(team['name']) + " IN THE TOURNAMENT")
        if team['name'] != "" and team['status'] != "inactive":
            team_number = find_team_number(tournament, team['names'])
            stage = tournament['stages'][int(team_number)]
            print("the team number is: " + str(team_number) + ", and the stage number is " + str(stage))
            odd = True if team_number % 2 == 1 else False
            if odd and 0 <= (team_number - 2**stage):
                team['next_opponent'] = tournament['teams'][team_number - 2**stage]
                tournament['teams'][team_number - 2 ** stage]['next_opponent'] = team
            elif len(tournament['teams']) > (team_number + 2**stage):
                team['next_opponent'] = tournament['teams'][team_number + 2**stage]
                tournament['teams'][team_number + 2 ** stage]['next_opponent'] = team
            try:
                print("This team's opponent is " + str(team['next_opponent']["name"]))
            except TypeError:
                print("the team doesn't have a next_opponent")


#MOST IMPORTANT FUNCTION
@app.get("/update-tournament/<tournament_id>")
def check_tournament_progress(tournament_id):
    import time
    tournament = get_tournament(tournament_id)
    region = tournament['region']
    teams = tournament['teams']
    team_stages = tournament['stages']
    max_size = tournament['max_number_of_teams']
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    current_time = datetime.utcnow().isoformat().replace("T", " ")[:16]
    end_time = (datetime.strptime(current_time, '%Y-%m-%d %H:%M') + timedelta(minutes = 60)).strftime('%Y-%m-%d %H:%M')
    teams_editable = tournament['teams_editable']

    print("Updating the tournament.")
    stages = range(0, int(math.log(float(tournament['max_number_of_teams']), 2)))
    for stage in stages:
        step = 2**stage
        for i in range(0, len(teams) - step, step):
            print("The current stage is: " + str(stage) + ", and the current index is " + str(i) + ".")

            #TODO Support byes and forfeits

            if (teams_editable[i]['id'] != 0 and teams_editable[i + step]['id'] != 0) and (team_stages[i] == stage) and (team_stages[i + step] == stage):
                print("Have found the right pair the team I'm looking at is " + str(teams_editable[i]['id']))
                print("the other team I'm looking at is " + str(teams_editable[i + step]['id']))
                query = check_if_match_submitted(teams_editable[i]["names"], teams_editable[i + step]["names"], current_time, end_time, region)
                if query['valid'] == "true":
                    print("HAVE FOUND A MATCH!")
                    team_names = [x['name'] for x in teams_editable]
                    print("here are what the teams looked like before the update: " + str(team_names))
                    update_matches(tournament, query['winning_team'], query['losing_team'])
                    team_names = [x['name'] for x in teams_editable]
                    print("and here are how the teams are changed: " + str(team_names))
                else:
                    print("this is not a valid match")

    update_teams_in_tournament(tournament)

def insert_result(bracket, winner_number, stage, max_size): #winner_number and stage are zero indexed, max_size is not
    odd = True if (winner_number % 2) == 1 else False
    print("Insert result and update the match bracket:")
    print("Previously: " + str(bracket))
    print("The winner is number: " + str(winner_number))
    print("The current stage is " + str(stage))
    bracket[stage][winner_number/(2*(stage + 1))] = [0,1] if odd else [1,0]
    print("After change: " + str(bracket))

def find_team_number(tournament, team):
    print("Finding the team numbers" + str(team))
    for i in range(len(tournament['teams'])):
        if (set(tournament['teams'][i]['names'])) == set(team):
            return i
    return "THERE IS NO TEAM NUMBER"

def update_matches(tournament, winning_team, losing_team):
    max_size = tournament['max_number_of_teams']
    bracket = tournament['matches']
    region  = tournament['region']
    stages = tournament['stages']
    time = tournament['start_date']
    print(" Am updating the matches")

    #CALCULATE WINNER NUMBER
    winner_number = int(find_team_number(tournament, winning_team))
    loser_number = int(find_team_number(tournament, losing_team))
    print("     winner is " + str(winner_number) + " loser is " + str(loser_number))
    insert_result(bracket, winner_number, stages[winner_number], max_size)
    print("         stages are: " + str(stages))
    stages[winner_number] += 1
    stages[loser_number] += 1
    print("         stages are: " +str(stages))
    tournament['teams_editable'][loser_number] = tournament['teams_editable'][winner_number]

    teams_editable = tournament['teams_editable']

def update_tournament_status(tournament):
    for team in tournament['teams']:
        if team['status'] != 'done':
            return
    tournament['status'] = 'closed'

@app.get('/start-tournament')
def start_tournament(tournament_id):
    tournament = get_tournament(tournament_id)
    tournament['status'] = 'ready'
    bracket_ready_teams(tournament)
    for team in tournament['teams']:
        team['stage'] = 0
    redirect('/tournament/' + tournament_id)

def check_if_registration_open(tournament_id):
    tournament = get_tournament(tournament_id)
    start_date = tournament["start_date"]
    print(start_date)
    print((datetime.strptime(start_date, '%Y-%m-%d %H:%M') + timedelta(minutes = 15)).strftime('%Y-%m-%d %H:%M'))
    return current_time_within_range(start_date, (datetime.strptime(start_date, '%Y-%m-%d %H:%M') + timedelta(minutes = 15)).strftime('%Y-%m-%d %H:%M') )

@app.get('/home')
def home():
    player_id = get_player_id()
    player = get_player(player_id)

    if get_team_id(player_id) == "0" or get_team_status(player_id) == "none":
        team = {
            'id' : '0',
            'players' : [],
            'name' : "empty_team",
            'tier' : 0
        }
        set_team_status(player_id, "none")
    else:
        team = get_player_team(player_id)

    team_players = []
    for uuid in team['players']:
        team_players.append(test_users[uuid])
    return template(
        'home.tpl',
        tournaments=test_tournaments,
        tournament_status=player['tournament_status'],
        team_status= player['team_status'],
        team = team,
        team_players = team_players,
        player = player
    )

@app.get('/create-tournament')
def customize_tournament():
    return template('createtournament.tpl', current_time = datetime.utcnow().isoformat()[:16].replace("T", " "))

def create_placeholder_team():
    placeholder_team = {
        "name" : "",
        "players" : "",
        "names" : "",
        "tier" : 0,
        "tournament_status" : "",
        'current_stage' : 0,
        'next_opponent' : "",
        'last_match_time' : ""
    }
    return placeholder_team

@app.post('/tournament')
def create_tournament():
    import uuid
    tournament_id = str(uuid.uuid4())
    tournament_name= request.forms.get('tournament_name')
    about = request.forms.get('about')
    game_type = request.forms.get('game_type')
    rewards = request.forms.get('rewards')
    entry_price = request.forms.get('entry_price')
    max_number_of_teams = request.forms.get('number_of_teams')
    region = request.forms.get('region').lower()
    start_date = request.forms.get('start_date')

    host = request.get_cookie('username', secret="a")
    uuid = request.get_cookie('uuid', secret='a')
    response.set_cookie('tournament_status', tournament_id, secret="a")

    new_tournament = {
        'id' : tournament_id,
        'name' : tournament_name,
        "start_date" : start_date,
        "rewards" : rewards,
        "entry_price" : entry_price,
        "number_of_teams" : 0,
        "max_number_of_teams" : max_number_of_teams,
        "teams" : [create_placeholder_team()] * int(max_number_of_teams),
        "teams_editable" : [create_placeholder_team()] * int(max_number_of_teams),
        "game_type" : game_type,
        "tournament_type" : "Double-Elimination",
        "region" : region,
        "about" : about,
        "host" : host,
        "host_uuid" : uuid,
        "status" : "registering",
        "matches" : new_empty_bracket(int(max_number_of_teams))
    }

    uuid = request.get_cookie('uuid', secret="a")
    test_users[uuid]['tournament_status'] = 'hosting'
    test_users[uuid]['tournament_id'] = tournament_id

    test_tournaments[tournament_id] = new_tournament
    redirect('/tournament/' + tournament_id)

@app.get('/tournament/<tournament_id>')
def view_tournament(tournament_id):
    response.set_cookie('tournament_id', tournament_id, secret='a')
    tournament = test_tournaments[tournament_id]
    tournament["teams"] = sorted(tournament["teams"], key=lambda k: k['tier'], reverse=True)
    bracket_teams = bracket_ready_teams(tournament)
    uuid = request.get_cookie('uuid', secret='a')
    player = test_users[uuid]
    if player['team_id'] != '0':
        player_team = test_teams[player['team_id']]
    else:
        player_team = {}
    return template(
        'tournamentpage.tpl',
         tournament = tournament,
         teams = test_tournaments[tournament_id]['teams'],
         bracket_teams = json.dumps(bracket_teams),
         matches = tournament["matches"],
         player = player,
         player_team = player_team,
         current_time = str(datetime.now())
    )

@app.get('/tournament/<tournament_id>/open')
def open_tournament(tournament_id):
    response.set_cookie('tournament_id', tournament_id, secret='a')
    tournament = test_tournaments[tournament_id]
    bracket_teams = bracket_ready_teams(tournament)
    uuid = request.get_cookie('uuid', secret='a')
    player = test_users[uuid]
    return template(
        'tournamentpage.tpl',
         tournament = tournament,
         teams = test_tournaments[tournament_id]['teams'],
         bracket_teams = json.dumps(bracket_teams),
         matches = tournament["matches"],
         player = player,
         current_time = str(datetime.now())
    )

def sort_teams_by_tier(tournament):
    teams = tournament['teams'][:int(tournament['max_number_of_teams'])]
    teams_ordered = sorted(teams, key=lambda k: k['tier'], reverse=True)
    tournament['teams'] = teams_ordered
    team_names = [team['name'] for team in teams_ordered]
    return team_names

def format_teams(team_names):
    formatted_names = []
    for i in range(len(team_names)/2):
        formatted_names.append([team_names[2*i], team_names[(2*i) + 1]])
    return formatted_names

def bracket_ready_teams(tournament):
    team_names_ordered = sort_teams_by_tier(tournament)
    return(format_teams(team_names_ordered))

@app.get('/manage-tournament')
def manage_tournament():
    uuid = request.get_cookie('uuid', secret='a')
    player = test_users[uuid]
    return template('managetournament.tpl', host=player, tournament= test_tournaments[player['tournament_id']])

@app.post('/cancel-tournament')
def cancel_tournament():
    host_id = request.get_cookie('uuid', secret="a")
    test_users[host_id]['tournament_status'] = 'none'
    tournament_id = test_users[host_id]['tournament_id']
    del test_tournaments[tournament_id]
    test_users[host_id]['tournament_id'] = '0'
    redirect('/home')

def insert_team(tournament, team):
    done = False
    for i in range(len(tournament['teams'])):
        if tournament['teams'][i]['tier'] > 0 and not done:
            break
        if tournament['teams'][i]['name'] == "" and not done:
            tournament['teams'][i] = team
            done = True
    if not done:
        tournament['teams'].append(team)
    tournament['teams'] = sorted(tournament['teams'], key=lambda k: k['tier'])

@app.get('/tournament/register')
def register_for_tournament():
    player = test_users[request.get_cookie('uuid', secret='a')]
    tournament_id = request.get_cookie('tournament_id', secret='a')
    tournament = test_tournaments[tournament_id]
    team = test_teams[player['team_id']]
    for player in team['players']:
        test_users[player]['tournament_status'] = 'registered'
        test_users[player]['tournament_id'] = tournament_id
    insert_team(tournament, team)
    redirect('/tournament/' + tournament_id)

@app.post('/team')
def create_team():
    import uuid
    team_id= str(uuid.uuid4())
    captain = test_users[request.get_cookie('uuid', secret='a')]
    team_name = request.forms.get('team_name')
    new_team = {
        'id': team_id,
        'name': team_name,
        'players': [captain['uuid']],
        'names' : [captain['name']],
        'captain': captain,
        'tier' : captain['tier'],
        'tournament_status' : "checked-in",
        'next_opponent' : { "name" : "", "names" : "" },
        'last_match_time' : ""
    }
    test_teams[team_id] = new_team
    captain['team_id'] = team_id
    captain['team_status'] = 'captain'
    redirect('/home')

def deep_delete_team(team_id):
    for uuid in test_teams[team_id]['players']:
        print(uuid)
        test_users[uuid]['team_id'] = 'none'
        test_users[uuid]['team_status'] = 'no_team'
    del test_teams[team_id]

@app.get('/disband-team')
def disband_team():
    uuid = request.get_cookie('uuid', secret='a')
    player = test_users[uuid]
    if player['team_status'] == 'captain':
        team_id = player['team_id']
        print(team_id)
        print('team_id')
        deep_delete_team(team_id)
        player['team_status'] = 'none'
        player['team_id'] = '0'
    redirect('/home')

@app.get('/leave-team')
def leave_team():
    uuid = request.get_cookie('uuid', secret='a')
    player = test_users[uuid]
    if player['team_status'] == 'team':
        team_id = player['team_id']
        test_teams[team_id]['players'].remove(uuid)
        player['team_status'] = 'none'
        player['team_id'] = 'none'
    redirect('/home')

@app.post('/join-team')
def join_team():
    team_id = request.forms.get('team_id_request')
    print(team_id)
    uuid = request.get_cookie('uuid', secret='a')
    player = test_users[uuid]
    if team_id not in test_teams.keys():
        pass
    else:
        team = test_teams[team_id]
        team['players'].append(player['uuid'])
        team['names'].append(player['name'])
        player['team_status'] = 'team'
        player['team_id'] = team_id
    redirect('/home')

def add_brackets_to_tournament(tournament):
    size = tournament['max_number_of_teams']
    tournament['matches'] = new_empty_bracket(size)

def new_empty_bracket(size):
    matches = []
    while ((size % 2) == 0) and (size > 0):
        submatches = []
        for i in range(size/2):
            submatches.append([0, 0])
        matches.append(submatches)
        size = size/2
    return matches

def organize_teams_by_tier(list_of_teams):
    return sorted(list_of_teams, key=lambda k: k['tier'], reverse=True)

def seed_bracket(bracket, max_size, teams):
    pass

@app.get('/tournament/check_in')
def check_in_tournament():
    player = test_users[request.get_cookie('uuid', secret='a')]
    tournament_id = request.get_cookie('tournament_id', secret='a')
    tournament = test_tournaments[tournament_id]
    team = test_teams[player['team_id']]
    team['tournament_status'] = "checked-in"
    for player in team['players']:
        test_users[player]['tournament_status'] = 'checked-in'
        test_users[player]['tournament_id'] = tournament_id
    redirect('/tournament/' + tournament_id)

def check_if_registration_valid():
    player_id = get_player_id()
    player = get_player(player_id)
    pass


@app.error(403)
def mistake403(code):
    return 'There is a mistake in your url!'
@app.error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'



# Player Parameters:
# hosting : Are they hosting a tournament? can be True or False
# tournament_id : The id of the tournament in question, is a string of a number or a string of "none"
# team_id : id of the team, a string of a number, or a string of "none"
# team_status :  "team", "none", or "captain"
# tournament_ status: "none", "hosting", "registered", "checked_in"

if __name__ == '__main__':
    p1 = {
        "uuid" : 'AngeIZ_',
        "name" : 'AngeIZ',
        "tier" : '1',
        "hosting" : False,
        "tournament_id": '900',
        'team_id': '48',
        "team_status": "captain",
        "tournament_status": "none"
    }
    p2 = {
        "uuid": '002',
        "name": "p2",
        "tier": "2",
        "hosting": False,
        "tournament_id": 0,
        'team_status' : 'team',
        'team_id': '45',
        "tournament_status": "none"
    }
    p3 = {
        "uuid": '003',
        "name": "p3",
        "tier": "3",
        "hosting": False,
        "tournament_id": 0,
        'team_status': 'team',
        'team_id': '45'
    }
    p4 = {
        "uuid": '004',
        "name": "p4",
        "tier": "4",
        "hosting": False,
        "tournament_id": 0,
        'team_status': 'team',
        'team_id': '45'
    }
    p5 = {
        "uuid": '005',
        "name": "p5",
        "tier": "5",
        "hosting": False,
        "tournament_id": 0,
        'team_status': 'team',
        'team_id': '45'
    }

    p6 = {
        "uuid": '006',
        "name": "p6",
        "tier": "6",
        "hosting": False,
        "tournament_id": 0,
        'team_status': 'team',
        'team_id': '45'
    }

    test_users = {
        p1['uuid'] : p1,
        p2['uuid'] : p2,
        p3['uuid'] : p3,
        p4['uuid']: p4,
        p5['uuid']: p5,
        p6['uuid']: p6
    }

    p1team = {
        'id' : "44",
        'name' : 'p1\'s team',
        'players' : [p1['name']],
        'tier' : p1['tier'],
        'captain' : p1,
        'status' : 'idle',
        'tournament_status' : "idle",
        'current_stage' : 0,
        'next_opponent' : ""
    }

    team45 = {
        'id' : '45',
        'name' : 'tier 5 potato team',
        'players' : ['MCassVG', 'DreadEdge', 'Ultrajulio', 'BestProBoss', 'PurplePandaOG'],
        'names': ['MCassVG', 'DreadEdge', 'Ultrajulio', 'BestProBoss', 'PurplePandaOG'],
        'tier' : 5,
        'captain' : p2,
        'tournament_status' : "registered",
        'current_stage' : 0,
        'next_opponent': "",
        'status' : 'active'
    }

    team46 = {
        'id': '46',
        'name': 'tier 6 team',
        'players': ['AllyPeterson', 'MICSHE', 'Arkaik', 'TetriS', 'DoctorGamer'],
        'names': ['AllyPeterson', 'MICSHE', 'Arkaik', 'TetriS', 'DoctorGamer'],
        'tier': 6,
        'captain': p6,
        'tournament_status' : "registered",
        'current_stage' : 0,
        'next_opponent': "",
        'status' : 'active'
    }

    team47 = {
        'id': '47',
        'name': 'tier 7 team',
        'players': ['DannyInfinity', ],
        'names' : ['DannyInfinity'],
        'tier': 7,
        'captain': p6,
        'tournament_status' : "registered",
        'current_stage' : 0,
        'next_opponent': "",
        'status' : 'active'
    }

    team48 = {
        'id': '48',
        'name': 'tier 8 team',
        'players': ['AngeIZ_'],
        'names': ['AngeIZ', 'ChaIlenge', 'markz34'],
        'tier': 8,
        'captain': p1,
        'tournament_status' : "registered",
        'current_stage' : 0,
        'next_opponent': { "name" : "n/a", "names" : ["Pending..."]},
        'status' : 'active',
        'last_match_time' : "Time Pending..."
    }

    test_teams = {
        '44' : p1team,
        '45': team45,
        '46' : team46,
        '47' : team47,
        '48' : team48
    }

    steams = [team48, team47, team46, team45]
    steamsV2 = [team48, team47, team46, team45]
    skaarfs_tournament = {
        'id' : '900',
        'name' : "Skaarf's Tourney",
        "start_date" : datetime.utcnow().isoformat().replace("T", " ")[:16],
        "rewards" : "Gold Chest",
        "entry_price" : "1000 Glory",
        "number_of_teams" : 1,
        "max_number_of_teams" : 4,
        "teams" : steams,
        "teams_editable" : steamsV2,
        "game_type" : "3v3",
        "tournament_type" : "Double-Elimination",
        "region" : "na",
        "about" : "Rawr zzzzz",
        "host" : "Skaarf",
        "host_uuid" : "9000",
        "status" : "idle",
        "matches" : new_empty_bracket(4),
        "stages" : [0,0,0,0]
    }

    testing_teams = []

    testing_tournament = {
        'id': '1000',
        'name': "WOW Tournament",
        "start_date": "2018-08-03 20:59",
        "rewards": "Gold Chest",
        "entry_price": "1000 Glory",
        "number_of_teams": 0,
        "max_number_of_teams": 32,
        "teams": [create_placeholder_team()] * int(32),
        "teams_editable": [create_placeholder_team()]* int(32),
        "game_type": "3v3",
        "tournament_type": "Double-Elimination",
        "region": "na",
        "about": "Rawr zzzzz",
        "host": "Skaarf",
        "host_uuid": "9000",
        "status": "idle",
        "matches": new_empty_bracket(32),
        "stages": [0, 0, 0, 0]
    }

    test_tournaments = {
        '900': skaarfs_tournament,
        '1000': testing_tournament
    }

    app.run(debug=True, reloader=True)
