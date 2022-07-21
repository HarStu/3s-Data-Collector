"""
script to generate a .config.json file
TODO: currently clunky and out of date; does not fill all the necessary fields in .config.json
    probably easier to just modify that file manually
"""
import sys
import json
import os

class Configcreator:

    def __init__(self, config_json_path):
        self.config_json_path = "../data/.config.json"
        self.required_keys = ["fcadefbneo_path", "replay_json_database_path", "scraper_path"]

    # returns true if a valid config json already exists, returns false if it doesn't
    # valid is defined as all the keys existing, and pointing toward existing files. 
    # those files might not actually be the required files, so it's not 100% foolproof
    def check_for_config_json(self):
        if os.path.exists(self.config_json_path):
            print("config json exists. checking validity...")
            with open(self.config_json_path, "r") as j:
                # load existing config json as a dict
                existing_config_json = json.load(j)
            # check if all the required keys exist
            for key in self.required_keys:
                if existing_config_json.get(key) != None and os.path.exists(existing_config_json[key]):
                    print(f"\trequired key '{key}' exists and points to a file")
                else:
                    print(f"\tCONFIG INVALID: required key '{key}' missing or points to nothing")
                    return False
            print("all required keys exist in .config.json and point to existing files")
            return True
        else:
            print("no or invalid config json")
            return False

    def create_new_config_json(self):
        pass
        # TODO
        #most functionality will be taken from create_config_json


    # function to create a new json config
    def create_config_json(self):
        print("\nCreating new config json")

        # paths which will be saved in the json
        fcadefbneo_path = None
        replay_json_database_filename = None

        # retrieve fcadefbneo path
        while True:      
            print("Please input the absolute path to your fcadefbneo.exe installation:")
            fcadefbneo_path = input("> ")
            if os.path.exists(fcadefbneo_path):
                print("\nFile exists at {path}".format(path = fcadefbneo_path))
                print("This program isn't complicated, so we'll just assume it's a valid install")
                break    
            else:        
                print("No file present there! Try again")
                continue 
        
        # retrieve replay_json_database_filename
        while True:      
            print("\nPlease input the filename of your replay json database, located in ../data/:")
            replay_json_database_filename = input("> ")
            if os.path.exists("../data/" + replay_json_database_filename):
                print("\n{name} exists".format(name = replay_json_database_filename))
                print("This program isn't complicated, so we'll just assume it's a valid json full of replays")
                break    
            else:        
                print("No file present there! Try again")
                continue

        # save paths to a dict
        config_json_dict = {
            'fcadefbneo_path':fcadefbneo_path,
            'replay_json_database_filename':replay_json_database_filename
        }
        
        # save json to a file
        with open("../data/.config.json", "w") as j:
            json.dump(config_json_dict, j, ensure_ascii = False, indent = 4)

        print("\nConfig json created!")

"""
    # check if the config json file already exists and confirm if the user would like to overwrite it or not 
    # basically just an entry point for the function above
    print("Checking if config json exists")
    if os.path.exists("../data/.config.json"):
        print("Config json already exists")
        while True: 
            print("Would you like to create a new config json? y/n")
            answer = input("> ")
            if answer == "y":
                create_config_json()
                break 
            elif answer == "n":
                print("Ending program")
                break
            else:
                print("Invalid input!")
                continue
    else:
        print("Config json does not exist")
        create_config_json()
"""