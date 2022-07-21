"""
Class for running replays and scraping the data from them using scraper.lua

TODO:
    immediately
        clean up enviroment at the end of replay (kill processes after output json is detected)
    down the line
        add functionality to fetch and scrape replays back-to-back, rather than having to do each one individually
"""
import sys
import json
import os
import subprocess

class Replayscraper:

    def __init__(self, games_json_path):
        self.games_json_path = games_json_path

    def scrape_replay(self, challenge_id):
        """
            scrape a single replay
            
            Args:
                challenge_id (str): The challenge id, should correspond to a game found in the json at "replay json database path"
        """

        # fetch information from ../data/.config.json
        print("loading from config")

        with open("../data/.config.json", "r") as c:
            config = json.load(c)

        fcadefbneo = config["fcadefbneo lua path"]
        scraper = config["scraper lua path"]
        json_database = config["replay json database path"]

        # grab game which is going to be scraped, and output it to .working.json
        # when scraper.lua runs, it will read from .working.json
        print("Scraping {game} from {database}".format(game = challenge_id, database = self.games_json_path))
        
        with open(self.games_json_path, "r") as j:
            replay_database = json.load(j)
        target_game = replay_database[challenge_id]

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
                f'quark:stream,sfiii3nr1,{challenge_id}.2,7100',
                f'{scraper}'
            ],
            env = running_env
        )