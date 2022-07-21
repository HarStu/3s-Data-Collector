"""
Class providing functionality for creating a .config.json file

TODO:
    function to overwrite specific config values, rather than creating a whole new file from scratch
        (though at that point, might as well just do it manually)
    function to create empty config which can be manually filled
"""
import sys
import json
import os

class Configcreator:

    def __init__(self):
        self.config_json_path = "../data/.config.json"
        self.required_keys = ["fcadefbneo path", "replay json database path", "scraper path"]

    # returns true if a valid config json already exists, returns false if it doesn't
    # valid is defined as all the keys existing, and pointing toward existing files. 
    # those files might not actually be the required files, so it's not 100% foolproof
    def check_config_json(self):
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
            return True
        else:
            print("no or invalid config json")
            return False

    def create_new_config_json(self):
        # disclaimer
        print("\ncreating new config json")
        print("you'll need to provide the following in order to create a working config")
        print("so please make sure you already have these files on your machine")
        print("if you don't, go do that, then run this setup again")
        for key in self.required_keys:
            print(f"\t{key}")

        # create new config as dict
        new_config_dict = {}
        for key in self.required_keys:
            while True:
                print(f"please enter the value for '{key}'")
                input_path = input("> ")
                if os.path.exists(input_path):
                    new_config_dict[key] = input_path
                    break
                else:
                    print(f"there is no file located at '{input_path}', try again")

        # save new config to self.config_json_path
        print("all required keys collected and validated")
        print(f"saving to {self.config_json_path}")
        with open(self.config_json_path, "w") as c:
            json.dump(new_config_dict, c, ensure_ascii = False, indent = 4)

    # check if there's a valid config. If there's not, create one
    def config_setup(self):
        if self.check_config_json() == True:
            print(f"Config json at '{self.config_json_path}' is valid")
        else:
            self.create_new_config_json()