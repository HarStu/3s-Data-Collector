"""
Starts a replay w/ the scraping lua running. To scrape a single game, run as follows:
    python3 3sDC.py <challenge id>


TODO:
    immediately
        after .working.json has been created, start the emulator with the scraping lua
        retrieve the json database being worked on, and the location of the fc install, from ../data/.config.json
    down the line
        add functionality to fetch and scrape replays back-to-back, rather than having to do each one individually
"""
import sys
import json
import os


challenge_id = None


# handle command line arguments
argv_len = len(sys.argv)
if argv_len != 2:
    print("invalid number of arguments!")
    sys.exit()
else:
    challenge_id = sys.argv[1]

# run a single replay w/ the scraper lua
def scrape_individual_replay(_challenge_id):

    # fetch information from ../data/.config.json
    print("loading from config")

    with open("../data/.config.json", "r") as c:
        config = json.load(c)

    fcadefbneo = config["fcadefbneo_path"]
    json_database = "../data/" + config["replay_json_database_filename"]

    # grab game which is going to be scraped, and output it to .working.json
    # when scraper.lua runs, it will read from .working.json
    print("Scraping {game} from {database}".format(game = _challenge_id, database = json_database))
    
    with open(json_database, "r") as j:
        replay_database = json.load(j)
    target_game = replay_database[_challenge_id]

    print("json loaded. targeted game entry: ")
    print(json.dumps(target_game, indent = 2))
    print("saving targeted game entry to ../data/.working.json")

    with open("../data/.working.json", "w") as w:
        json.dump(target_game, w, ensure_ascii = False, indent = 4)

scrape_individual_replay(challenge_id)