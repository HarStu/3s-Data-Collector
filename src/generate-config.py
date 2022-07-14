# a script to generate a .config.json file
import sys
import json
import os

# function to create a new json config
def create_config_json():
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