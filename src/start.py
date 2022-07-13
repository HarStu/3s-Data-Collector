import sys
import json

"""
Starts a replay w/ the scraping lua running. To scrape a single game, run as follows:
    python3 start.py <replays json> <challenge id>


TODO:
    immediately
        after .working.json has been created, start the emulator with the scraping lua
    down 
        add functionality to fetch and scrape replays back-to-back, rather than having to do each one individually
"""

json_database = None
challenge_id = None

# handle command line arguments
argv_len = len(sys.argv)
if argv_len != 3:
    print("invalid number of arguments!")
    print("you've provided {length} args".format(length = len(sys.argv)))
    sys.exit()
else:
    json_database = sys.argv[1]
    challenge_id = sys.argv[2]

def scrape_individual_replay(_json_database, _challenge_id):

    print("Scraping {game} from {database}".format(game = _challenge_id, database = _json_database))
    
    with open(_json_database, "r") as j:
        replay_database = json.load(j)
    target_game = replay_database[_challenge_id]

    print("json loaded. targeted game entry: ")
    print(json.dumps(target_game, indent = 2))
    print("saving targeted game entry to ../data/.working.json")

    with open("../data/.working.json", "w") as w:
        json.dump(target_game, w, ensure_ascii = False, indent = 4)


scrape_individual_replay(json_database, challenge_id)