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


class Replayfetcher:

    def __init__(self, output_games_json_path):
        self.gameid = 'sfiii3nr1'
        self.output_games_json_path = output_games_json_path

    # Fetch and return a dict of games for a given username
    def get_username_replays(self, player):
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
                - game[gameid] matches self.gameid
            """
            for game in response_json['results']['results']:
                if game in retrieved_games.values():
                    # assuming offset is iterated properly, this is never entered unless there is an issue on FC's end
                    # there seems to be such an issue on certain accounts (exodus3rd)
                    discarded_games_count = discarded_games_count + 1
                elif game['gameid'] == self.gameid:
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

    # save a dict of games to self.output_games_json_path
    def save_games_to_output_json(self, retrieved_games):
        pass

    # save a dict of games to a throwaway "output" json, rather than the master json
    # here for testing
    def save_games_to_test_json(self, retrieved_games):
        with open('../data/test.json', 'w', encoding = 'utf-8') as t:
            json.dump(retrieved_games, t, ensure_ascii = False, indent = 4)