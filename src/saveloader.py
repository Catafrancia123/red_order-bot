import json, os, datetime
from rich import print as rprint

SAVE = "config.json"

def find_save():
    save_found = False
    current_directory_files = os.listdir("./")
    if SAVE in current_directory_files:
        save_found = True
    elif SAVE not in current_directory_files:
        save_found = False

    if not save_found:
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[bright_red]NOT FOUND[/bright_red]] Save files doesn\'t exists and creating save file.')
        with open(SAVE, mode="w", encoding="utf-8") as outfile:
            raise FileNotFoundError("File \"config.json\" was not found, please contact catamapp ASAP.")
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]CREATED[/light_green]] Save files have been created and continuing session.')
    else:
        rprint(f'[grey]{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/grey] [[light_green]FOUND[/light_green]] Save files exists and continuing session.')

def load_json(path : str, to_load : str, library : str = None) -> any: #* loads stuff from json
    with open(path, mode="r", encoding="utf-8") as read_file:
        load = json.load(read_file)
        
    #* json throws a keyerror if the data is not found.
    if library != None:
        data = load[library][to_load]
    elif library == None:
        data = load[to_load]

    read_file.close()
    return data
            
def edit_json(path : str, to_change : str, value, library : str = None): #* Can edit/add
    with open(path, mode="r", encoding="utf-8") as read_file:
        data = json.load(read_file)
        
    if library != None:
        data[library][to_change] = value
    elif library == None:
        data[to_change] = value
    read_file.close()

    with open(path, "w") as outfile:
        json.dump(data, outfile)
    outfile.close()

#! Search algorithms (may come in handy later on). DONT DELETE THIS.

def binary_search(array : list, target):
    low = 0
    high = len(array)

    while low <= high:
        mid = low + (high - low) // 2

        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    raise KeyError("Data not found.")