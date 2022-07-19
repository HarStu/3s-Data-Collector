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
    option to download replays to individual player json, or main database json
        or to player/game instead of player/main database?
    verify that we're only retrieving ranked games?
    split this into two files (one defining the class/function, and another entry point for the program)
"""

player = None
gameid = 'sfiii3nr1'

# handle command line arguments
# TODO - add option for database/individual json
argv_len = len(sys.argv)
if argv_len == 1:
    print("No player specified! Please try again. Use the following format:")
    print("    python3 get-replays.py <player> (<gameid>)")
    sys.exit()
elif argv_len == 2:
    player = sys.argv[1]
elif argv_len == 3:
    player = sys.argv[1]
    gameid = sys.argv[2]
print("Retrieving {_player}'s {_gameid} replays".format(_player = player, _gameid = gameid))

def get_player_replays(player, gameid):
    # create empty dict to hold retrieved games
    retrieved_games = {}

    # create empty dict to hold repeated games (for debugging)
    discarded_games = {}

    # for escaping while loop once all games have been retrieved
    redundancy_achieved = False

    # offset to retrieve each batch of games, and the amount of games to fetch each loop
    # 100 is the maximum
    offset = 0
    fetch_count = 100

    # variables for debug
    discarded_games_count = 0
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

        # assuming this is the final batch of games until proven otherwise
        redundancy_achieved = True

        """
        add new games in response_json to retrieved_games

        criteria for adding a game to the retrieved_games
            - game is NOT already in retrieved_games
            - game[gameid] matches the gameid we're looking for 
        """
        for game in response_json['results']['results']:
            if game in retrieved_games.values():
                # assuming offset is iterated properly, this is never entered unless there is an issue on FC's end
                # there seems to be such an issue on certain accounts (exodus3rd)
                discarded_games_count = discarded_games_count + 1
            elif game['gameid'] == gameid:
                # the game doesn't exist in retrieved_games, and the gameid matches our target
                # so we add it, and this loop is not redundant
                retrieved_games[game['quarkid']] = game
                redundancy_achieved = False
                original_games_count = original_games_count + 1
            else:
                # gameid doesn't match    
                discarded_games_count = discarded_games_count + 1 
                
        print("as of this loop, we have " + str(discarded_games_count) + " discarded games and " + str(original_games_count) + " original games")

        offset = offset + 100

    return retrieved_games

# call function
games = get_player_replays(player, gameid)

# save retrieved games to json files
# TODO - overhaul this to accomodate for saving to database/individual JSONs
print('Creating {_player}-{_gameid}.json'.format(_player = player, _gameid = gameid))
with open('../data/{_player}-{_gameid}.json'.format(_player = player, _gameid = gameid), 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=4)