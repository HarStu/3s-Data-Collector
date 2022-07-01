import sys
import requests
import json

"""
Retrieve replays from FC API. Run as follows:
    python3 get-replays.py <player> <gameid>

    defaults:
        no arguments throws error
        gameid defaults to sfiii3nr1
        rank cutoff defaults to S (6)

TODO:
    only fetch replays from a specific gameid
        - command line argument added, functionality not yet implemented (i.e, all replays for all games will still be grabbed)
    option to download replays to individual player json, or master database json
"""

player = None
gameid = 'sfiii3nr1'

# handle command line arguments
# TODO - add option for database/individual json
argv_len = len(sys.argv)
if argv_len == 1:
    print("No player specified! Please try again. Use the following format:")
    print("    python3 get-replays.py <player> <gameid> <rank cutoff> <individual/master json>")
    sys.exit()
elif argv_len == 2:
    player = sys.argv[1]
elif argv_len == 3:
    player = sys.argv[1]
    gameid = sys.argv[2]
print("retrieving {_player}'s {_gameid} replays".format(_player = player, _gameid = gameid))

# call function
games = get_player_replays(player, gameid)

# save retrieved games to json files
# TODO - overhaul this to accomodate for saving to database/individual JSONs
print('Creating ' + player + '-original-games.json')
with open('./data/' + player + '-original-games.json', 'w', encoding='utf-8') as f:
    json.dump(games[0], f, ensure_ascii=False, indent=4)
if len(games[1]) > 0:
    print('Repeated games present. Creating ' + player + '-repeated-games.json')
    with open('./data/' + player + '-repeated-games.json', 'w', encoding='utf-8') as f:
        json.dump(games[1], f, ensure_ascii=False, indent=4)
else:
    print("No repeated games present")


def get_player_replays(player, gameid):
    # create empty dict to hold retrieved games
    retrieved_games = {}

    # create empty dict to hold repeated games (for debugging)
    repeated_games = {}

    # for escaping while loop once all games have been retrieved
    redundancy_achieved = False

    # offset to retrieve each batch of games, and the amount of games to fetch each loop
    # 100 is the maximum
    offset = 0
    fetch_count = 100

    # variables for debug
    repeated_games_count = 0
    original_games_count = 0

    # Loop through multiple API calls
    while redundancy_achieved == False:

        # set up query to be posted
        query = {
            'req':'searchquarks',
            'best':'false',
            'offset':offset,
            'limit':offset + fetch_count,
            'username':player
        }
    
        # post query
        r = requests.post(
            "https://www.fightcade.com/api/",
            json=query
        )
        
        # convert response into json
        response_json = r.json()

        # assuming this is the finale batch of games until proven otherwise
        redundancy_achieved = True

        # if a game in response_json is NOT in retrieved_games, add it and set redundancy_achieved to False
        # if a game in response_json is in retrieved_json, add it to repeated_games
        # in both cases, iterate the respective counts for debugging
        for game in response_json['results']['results']:
            if game in retrieved_games.values():
                # assuming offset is iterated properly, this is never entered unless there is an issue on FC's end
                # there seems to be such an issue on certain accounts (exodus3rd)
                repeated_games[game['quarkid']] = game
                repeated_games_count = repeated_games_count + 1
            else:
                # the game doesn't exist in retrieved_games
                # so we add it, and this loop is not redundant
                retrieved_games[game['quarkid']] = game
                redundancy_achieved = False
                original_games_count = original_games_count + 1
        
        print("as of this loop, we have " + str(repeated_games_count) + " repeated games and " + str(original_games_count) + " original games")

        offset = offset + 100

    return retrieved_games, repeated_games