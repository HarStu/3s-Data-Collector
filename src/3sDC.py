"""
Starts a replay w/ the scraping lua running. To scrape a single game, run as follows:
    python3 3sDC.py <challenge id>


TODO:
    immediately
        start scraper.lua along w/ replay
        clean up enviroment at the end (kill processes)
        reorganize this file (wrap everything in a class, make sure variable names are consistent)
    down the line
        add functionality to fetch and scrape replays back-to-back, rather than having to do each one individually
"""
import sys
import json
import os
import subprocess


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
    scraper = config["scraper_path"]
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

    # start replay
    # current doesn't start scraper lua
    print("starting fcadefbneo")
    running_env = os.environ.copy()
    running_env["WINEDLLOVERRIDES"] = "avifil32=n,b"
    subprocess.run(
        [
            "/usr/bin/wine",
            f'{fcadefbneo}',
            f'quark:stream,sfiii3nr1,{_challenge_id}.2,7100',
            f'{scraper}'
        ],
        env = running_env
    )

scrape_individual_replay(challenge_id)