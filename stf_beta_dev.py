import json
import time
import random
import os
from colorama import init, Fore
import subprocess
import sys
from datetime import datetime, timedelta

init()

# Clear the terminal for a new menu or screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

shuttle_bays = 1
original_crew_file_path = 'crew_list.json'
user_crew_file_path = 'user_crew_data.json'
user_game_file_path = 'user_data.json'
ship_save = 'ship_save.json'
json_file_path = 'system_data.json'
ship_sel = 'ship selection'
buildings_path = 'buildings.json'

# Load data from the user data
def load_json_data():
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return None
    
def load_json_user_data():
    try:
        with open(user_game_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return None

# load a specific piece of data from user_data.json
def load_data(key):
    try:
        with open(user_game_file_path, 'r') as file:
            data = json.load(file)
        if key in data:
            return data[key]
        else:
            raise KeyError(f"Key '{key}' not found.")
    except FileNotFoundError:
        print("Game data file not found. Loading default values.")
        time.sleep(1)
        return None
    except KeyError as e:
        print(e)

# save a specific value directly to user_data.json
def save_data(key, value):
    try:
        # writes and reads as r+ so that it doesn't rewrite the entire file
        with open(user_game_file_path, 'r+') as file:
            data = json.load(file)
            if key in data:
                data[key] = value
            else:
                print(f"Key '{key}' not found. Adding it at the top level.")
                data[key] = value
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Game data file not found.")

def initialize_cache():
    # Load JSON data
    data = load_json_user_data()

    # Populate the cache with all keys from the JSON
    cache = {key: data[key] for key in data.keys()}

    return cache

# Initialize cache
cache = initialize_cache()

def check_update_mats():
    current_time = datetime.now()

    # Load and parse the next update time
    next_update_time_str = load_data('next_update_time')
    if not next_update_time_str:
        save_data('next_update_time', current_time.isoformat())  # Save as ISO format
        return  # Exit the function since it's the first run

    # Convert the stored ISO string back to a datetime object
    next_update_time = datetime.fromisoformat(next_update_time_str)

    # Check if it's time to update
    if next_update_time <= current_time:
        update_mats()  # Perform your material update logic
        new_next_update_time = current_time + timedelta(seconds=30)
        save_data('next_update_time', new_next_update_time.isoformat())  # Save new update time


def update_mats():
    for key in cache.keys():
        # Check if the key exists in the loaded data to prevent saving unknown keys
        if key in load_json_user_data():  
            save_data(key, cache[key])

# Get materials in a mining node in a certain system
def get_material_in_node(system_name, mine_name):
    data = load_json_data()

    if data is None:
        return None

    for system in data["system data"]:
        if system["name"] == system_name:
            if mine_name in system:
                return system[mine_name]
            else:
                print(f"Error: {mine_name} does not exist in {system_name}.")
                return None

# Save data to the user data
def save_json_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Update the materials for a mining node in the system_data.json file
def update_materials(system_name, mine_name, amount):
    data = load_json_data()
    if data is None:
        return
    for system in data["system data"]:
        if system["name"] == system_name:
            if mine_name in system:
                system[mine_name] -= amount
                if system[mine_name] <= 0:
                    system[mine_name] = 100
                    print(f"{mine_name} in {system_name} has been reset to 100.")
                save_json_data(data)
            else:
                print(f"Error: {mine_name} does not exist in {system_name}.")
            break
    else:
        print(f"Error: System {system_name} not found.")

# input for an int, but keeps program from crashing when words are entered
def ask_sanitize(question_ask, follow_up_question=None):
    if follow_up_question is None:
        follow_up_question = question_ask
        response = input(question_ask)
        while True:
            try:
                response = int(response)
                break
            except ValueError:
                response = input(follow_up_question)
                continue
        return response

# input for an int but for the lobby so that the player knows what integers to input for future reference too.
def ask_sanitize_lobby(question_ask, follow_up_question=None, valid_options=None):
    if follow_up_question is None:
        follow_up_question = question_ask
    while True:
        response = input(question_ask)
        try:
            response = int(response)
            if valid_options and response not in valid_options:
                print(f'Choose an option {", ".join(map(str, valid_options))}')
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
            continue
    return response

# save data specific data for ships to the ship file
def save_ship_data(ship_name, stat_key, value):
    try:
        with open(ship_save, 'r+') as file:
            data = json.load(file)
            for ship in data[ship_sel]:
                if ship['name'] == ship_name:
                    if stat_key in ship:
                        ship[stat_key] = value
                    else:
                        print(f"Stat '{stat_key}' not found for ship '{ship_name}'.")
                        return
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except FileNotFoundError:
        return

# resets all positions of all crew on board a ship when your ship dies
def reset_crew_positions(ship_name: str) -> str:
    try:
        with open(ship_save, 'r+') as file:
            data = json.load(file)

            for ship in data[ship_sel]:
                if ship['name'] == ship_name:
                    if "crew" in ship:
                        ship['crew'] = {
                            "captain": None,
                            "bridge1": None,
                            "bridge2": None,
                            "bridge3": None
                        }
                        print(f"Crew positions for '{ship_name}' have been reset to null.")
                        break
                    else:
                        print(f"No crew data found for '{ship_name}'.")
                        break
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        return ""

# load data for a specific ship from the ship save file
def load_ship_stat(ship_name, stat_key):
    try:
        with open(ship_save, 'r') as file:
            data = json.load(file)

            for ship in data[ship_sel]:
                if ship['name'] == ship_name:
                    return ship.get(stat_key, None)
        print(f"Ship '{ship_name}' not found.")
        return None
    except FileNotFoundError:
        return None

def is_ship_owned(ship_name):
    try:
        with open(ship_save, 'r') as file:
            data = json.load(file)

            for ship in data[ship_sel]:
                if ship['name'] == ship_name:
                    return ship.get('owned', False)
        print(f"Ship '{ship_name}' not found.")
        return False
    except FileNotFoundError:
        return False

def set_ship_owned_status(ship_name, owned_status):
    try:
        with open(ship_save, 'r+') as file:
            data = json.load(file)

            for ship in data[ship_sel]:
                if ship['name'] == ship_name:
                    ship['owned'] = owned_status

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        return

def equip_ship_in_game(ship_name):
    try:
        with open(user_game_file_path, 'r+') as user_file:
            user_data = json.load(user_file)
            with open(ship_save, 'r') as ship_file:
                ship_data = json.load(ship_file)
            for ship in ship_data[ship_sel]:
                if ship['name'] == ship_name and ship.get('owned', False):
                    user_data['ship'] = ship_name
                    print(f"{ship_name} is now equipped in your game data!")
                    break
            else:
                print(f"You do not own the ship: {ship_name}")
            user_file.seek(0)
            json.dump(user_data, user_file, indent=4)
            user_file.truncate()

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def upgrade_ship(ship_name, stat):
    try:
        with open(ship_save, 'r+') as file:
            data = json.load(file)

            ship_blueprints = {
                "Stargazer": ("stargazer_blueprints", 20),
                "Daedalus Class Medical": ("daedalus_class_medical_blueprints", 30),
                "Ambassadors Shuttle": ("ambassadors_shuttle_blueprints", 40),
                "Realta": ("realta_blueprints", 50),
                "USS Grissom": ("uss_grissom_blueprints", 60),
                "Federation Shuttlecraft": ("federation_shuttlecraft_blueprints", 70),
                "USS Constitution": ("uss_constitution_blueprints", 80),
                "Ferengi DKora": ("ferengi_dkora_blueprints", 90),
                "Galaxy Class": ("galaxy_class_blueprints", 100),
                "Klingon KVort": ("klingon_kvort_blueprints", 110),
                "USS Excelsior": ("uss_excelsior_blueprints", 120),
                "Romulan Warbird": ("romulan_warbird_blueprints", 130),
                "USS Enterprise (NCC-1701 D)": ("uss_enterprise_(ncc-1701_d)_blueprints", 140),
            }

            # Find the ship in the data
            for ship in data[ship_sel]:
                if ship['name'] == ship_name and ship.get('owned', False):
                    if ship_name not in ship_blueprints:
                        raise ValueError("Invalid ship name provided.")

                    json_save_data, upgrade_cost = ship_blueprints[ship_name]

                    if cache[json_save_data] >= upgrade_cost:
                        ship[stat] += 1
                        cache[json_save_data] -= upgrade_cost
                        print(f"{Fore.GREEN}{ship_name}'s {stat} has been upgraded to {ship[stat]}.{Fore.WHITE}")
                    else:
                        print(f"{Fore.RED}Not enough blueprints to upgrade {stat}.{Fore.WHITE}")
                    time.sleep(2)
                    break

            # Save updated data back to the file
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return cache['parsteel']

def equip_ship(ship_name):
    try:
        with open(ship_save, 'r+') as file:
            data = json.load(file)

            for ship in data[ship_sel]:
                if ship['name'] == ship_name and ship.get('owned', False):
                    for s in data[ship_sel]:
                        s['equipped'] = False
                    ship['equipped'] = True
                    cache['ship'] = ship_name
                    print(f"{Fore.GREEN}{ship_name} is now equipped.{Fore.GREEN}")
                    time.sleep(2)
                    break

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")

def buy_ship(ship_name, coins):
    global current_coins
    try:
        with open(ship_save, 'r+') as file:
            data = json.load(file)

            ship_prices = {
                "Stargazer": ("stargazer_blueprints", 200),
                "Daedalus Class Medical": ("daedalus_class_medical_blueprints", 250),
                "Ambassadors Shuttle": ("ambassadors_shuttle_blueprints", 300),
                "Realta": ("realta_blueprints", 350),
                "USS Grissom": ("uss_grissom_blueprints", 400),
                "Federation Shuttlecraft": ("federation_shuttlecraft_blueprints", 450),
                "USS Constitution": ("uss_constitution_blueprints", 600),
                "Ferengi DKora": ("ferengi_dkora_blueprints", 750),
                "Galaxy Class": ("galaxy_class_blueprints", 1000),
                "Klingon KVort": ("klingon_kvort_blueprints", 1200),
                "USS Excelsior": ("uss_excelsior_blueprints", 1500),
                "Romulan Warbird": ("romulan_warbird_blueprints", 2000),
                "USS Enterprise (NCC-1701 D)": ("uss_enterprise_(ncc-1701_d)_blueprints", 2500),
            }

            for ship in data[ship_sel]:
                if ship['name'] == ship_name and not ship['owned']:
                    if ship_name not in ship_prices:
                        raise ValueError("Invalid ship name provided.")

                    json_save_data, price = ship_prices[ship_name]
                    current_coins = cache[json_save_data]

                    confirmation_message = (
                        f"{Fore.RED}Are you sure you want to buy this ship? It costs {price} {ship_name} blueprints "
                        f"({current_coins}->{current_coins - price}): {Fore.WHITE}"
                    )
                    
                    if ask(confirmation_message):
                        if current_coins >= price:
                            clear()
                            ship['owned'] = True
                            cache[json_save_data] = current_coins - price
                            print(f"{Fore.GREEN}You have purchased {ship_name}.{Fore.WHITE}")
                            time.sleep(2)
                        else:
                            print(f"{Fore.RED}Not enough blueprints to buy this ship.{Fore.WHITE}")
                            time.sleep(2)
                        break  # Exit the loop after the transaction
                    else:
                        break  # Exit the loop if the user cancels

            # Save updated data back to the file
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return coins


def view_ship_details(ship_name):
    try:
        with open(ship_save, 'r') as file:
            data = json.load(file)

        for ship in data[ship_sel]:
            if ship['name'] == ship_name:
                print(f"{Fore.BLUE}{ship_name}{Fore.WHITE}")
                print(f"Firepower: {ship['firepower']}")
                print(f"Accuracy: {ship['accuracy']}")
                print(f"Evasion: {ship['evasion']}")
                print(f"Max Health: {ship['max_health']}")
                print(f"Max Storage: {ship['max_storage']}")
                print(f"Owned: {ship['owned']}")
                if ask('Type Y or N to exit: '):
                    return
        print(f"Ship '{ship_name}' not found.")
    except FileNotFoundError:
        print("Ship data file not found.")

def display_ship_menu():
    try:
        with open(ship_save, 'r') as file:
            data = json.load(file)
        print('')
        for i, ship in enumerate(data[ship_sel], 1):
            print(f"{i}. {ship['name']} (Owned: {ship.get('owned', False)})")

    except FileNotFoundError:
        print("Ship data file not found.")
            
def ship_management_menu(coins):
    global tutorial_highlight7
    global ship_name

    # Ship dictionary for lookup
    ships = {
        1: 'Stargazer',
        2: 'USS Grissom',
        3: 'Realta',
        4: 'Federation Shuttlecraft',
        5: 'Daedalus Class Medical',
        6: 'Ambassadors Shuttle',
        7: 'USS Constitution',
        8: 'Galaxy Class',
        9: 'Ferengi DKora',
        10: 'Klingon KVort',
        11: 'Romulan Warbird',
        12: 'USS Excelsior',
        13: 'USS Enterprise (NCC-1701 D)'
    }

    # Stat dictionary for lookup
    stats = {
        1: 'firepower',
        2: 'accuracy',
        3: 'evasion',
        4: 'warp_range',
        5: 'storage',
        6: 'mining_efficiency'
    }

    while True:
        clear()

        # Tutorial logic
        tutorial_step = cache['tutorial']
        if tutorial_step == 7:
            print(f"{Fore.YELLOW}Welcome to the shipyard! You can see ship's details, build ships, equip them, change their crew, and upgrade it.\n"
                  f"Right now, you are going to upgrade the Stargazer. Type 4 to upgrade a ship.{Fore.WHITE}")
            time.sleep(2)
            tutorial_highlight7, tutorial_highlight8 = Fore.YELLOW, Fore.WHITE
        elif tutorial_step == 8:
            print(f"{Fore.YELLOW}Great job upgrading your ship! As you get more blueprints, you will be able to upgrade your ship more. "
                  f"Now that you have done that, let's assign some crew to your ship.\nSelect 5 to enter the crew menu.{Fore.WHITE}")
            time.sleep(2)
            tutorial_highlight7, tutorial_highlight8 = Fore.WHITE, Fore.YELLOW
        else:
            if tutorial_step == 9:
                print(f"{Fore.YELLOW}Type 7 to exit the shipyard.{Fore.WHITE}")
            tutorial_highlight7, tutorial_highlight8 = Fore.WHITE, Fore.WHITE

        # Display income and ship blueprints
        income_display()
        ship_blueprints = " || ".join([f"{Fore.BLUE}{ship} BP:{Fore.WHITE} {cache[ship.lower().replace(' ', '_') + '_blueprints']}" for ship in ships.values()])
        center_text(ship_blueprints)
        
        # Display menu
        display_ship_menu()
        choice = ask_sanitize(
            question_ask=f"\nOptions:\n1. View Ship Details\n2. Build Ship\n3. Equip Ship\n"
                         f"{tutorial_highlight7}4. Upgrade Ship{Fore.WHITE}\n"
                         f"{tutorial_highlight8}5. Change Crew on {cache['ship']}{Fore.WHITE}\n"
                         "6. View Ship Manifest\n7. Exit\nSelect an option: ")

        def get_ship_name(ship_num):
            return ships.get(ship_num, 'Stargazer')

        if choice == 1:
            # View Ship Details
            clear()
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize("What ship would you like to view? ")
            ship_name = get_ship_name(ship_num)
            clear()
            income_display()
            view_ship_details(ship_name)

        elif choice == 2:
            # Build Ship
            clear()
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize("What ship would you like to build? ", valid_inputs=list(ships.keys()))
            ship_name = get_ship_name(ship_num)
            buy_ship(ship_name, coins)

        elif choice == 3:
            # Equip Ship
            clear()
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize("What ship would you like to equip? ", valid_inputs=list(ships.keys()))
            ship_name = get_ship_name(ship_num)
            equip_ship(ship_name)

        elif choice == 4:
            # Upgrade Ship
            clear()
            if tutorial_step == 7:
                print(f"{Fore.YELLOW}Upgrade the Stargazer by typing 1.{Fore.WHITE}")
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize("What ship would you like to upgrade? ", valid_inputs=list(ships.keys()))
            ship_name = get_ship_name(ship_num)

            if tutorial_step == 7:
                print(f"{Fore.YELLOW}Let's upgrade the warp range. Type 4.{Fore.WHITE}")
            stat_num = ask_sanitize(
                "Enter the stat to upgrade (1. Firepower, 2. Accuracy, 3. Evasion, "
                f"{tutorial_highlight7}4. Warp Range{Fore.WHITE}, 5. Storage, 6. Mining Efficiency): ",
                valid_inputs=list(stats.keys())
            )
            stat = stats[stat_num]
            if ask(f"{Fore.YELLOW}Are you sure you want to upgrade {stat}? (Y/N): "):
                upgrade_ship(ship_name, stat)
                if tutorial_step == 7:
                    cache['tutorial'] = 8
            else:
                print(f"{Fore.RED}Upgrade Canceled.{Fore.WHITE}")
                time.sleep(1)

        elif choice == 5:
            # Assign Crew
            clear()
            income_display()
            assign_crew_and_adjust_stats("user_crew_data.json", "ship_save.json")

        elif choice == 6:
            # View Ship Manifest
            clear()
            income_display()
            display_crew_assignments(ship_save)
            ask(f"{Fore.BLUE}Type any letter to exit {Fore.WHITE}")

        elif choice == 7:
            break

        else:
            print("Invalid option. Please try again.")
            time.sleep(2)


costs = {"Mining Laser": 15, "Health": 10, "Phaser": 20, "Warp Range": 15}
deltas = {"Mining Laser": 1.5, "Health": 2, "Phaser": 2, "Warp Range": 2}
system_deltas = {'Material Cluster': 1.5, 'Trading Post': 2, 'Enemy Ships Loot': 1.5, 'Enemy Ships Health': 1.3}
systems = {
    1: 'Sol', 2: 'Vulcan', 3: 'Tellar', 4: 'Andor', 5: 'Omicron II',
    6: 'Regula', 7: 'Solaria', 8: 'Tarkalea XII', 9: 'Xindi Starbase 9', 10: 'Altor IV'
}

def load_crew_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_crew_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_game_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_game_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def has_played_before(file_path):
    return os.path.exists(file_path)

def initialize_game_data():
    if has_played_before(user_game_file_path):
        with open(user_game_file_path, 'r') as file:
            return json.load(file)
    else:
        return game_state

def initialize_crew_data():
    if has_played_before(user_crew_file_path):
        with open(user_crew_file_path, 'r') as file:
            return json.load(file)
    else:
        original_crew_data = load_crew_data(original_crew_file_path)
        save_crew_data(user_crew_file_path, original_crew_data)
        return original_crew_data

def display_crew(crew_data):
    print("\nCurrent Crew Members:")
    for index, member in enumerate(crew_data['crew']):
        print(f"{index + 1}. {member['name']} (Skill: {member['skill']}, Skill Level: {member['skill_level']}, Rarity: {member['rarity']})")

def display_available_crew(crew_data, available_crew):
    print("\nAvailable Crew for Purchase:")
    owned_crew_names = [member['name'] for member in crew_data['crew']]
    for index, member in enumerate(available_crew):
        if member['name'] not in owned_crew_names:
            print(f"{index + 1}. {member['name']} (Skill: {member['skill']}, Rarity: {member['rarity']}, Price: {member['price']} Recruit Tokens)")

def upgrade_crew_member(crew_data, member_index, cost):
    if cache['recruit_tokens'] >= cost:
        crew_data['crew'][member_index]['skill_level'] += 5
        crew_data['crew'][member_index]['ability']['boost'] += 0.3
        cache['recruit_tokens'] -= cost
        print(f"{Fore.GREEN}\n{crew_data['crew'][member_index]['name']}'s skill level increased to {crew_data['crew'][member_index]['skill_level']}!{Fore.WHITE}")
        print(f"{Fore.YELLOW}Remaining Recruit Tokens: {cache['recruit_tokens']}{Fore.WHITE}")
        if cache['tutorial'] == 9:
            cache['tutorial'] = 10
        time.sleep(2)
    else:
        print(f"{Fore.RED}\nNot enough recruit tokens to upgrade.{Fore.WHITE}")
        time.sleep(2)

def purchase_crew_member(crew_data, available_crew, member_index):
    if cache['recruit_tokens'] >= available_crew[member_index]['price']:
        cache['recruit_tokens'] -= available_crew[member_index]['price']
        crew_data['crew'].append(available_crew[member_index])
        save_crew_data(user_crew_file_path, crew_data)
        print(f"{Fore.GREEN}\n{available_crew[member_index]['name']} has been recruited!{Fore.WHITE}")
        print(f"{Fore.YELLOW}Remaining Recruit Tokens: {cache['recruit_tokens']}{Fore.WHITE}")
        time.sleep(2)
    else:
        print(f"{Fore.RED}\nNot enough recruit tokens to purchase this crew member.{Fore.WHITE}")
        time.sleep(2)

def main():
    global game_state
    game_state = initialize_game_data()
    crew_data = initialize_crew_data()

    #crew that can be purchases
    available_crew = [
    {"name": "Uhura", "skill_level": 10, "skill": "Communication", "rarity": "Rare", "price": 100},
    {"name": "Sulu", "skill_level": 10, "skill": "Pilot", "rarity": "Common", "price": 50},
    {"name": "Chekov", "skill_level": 10, "skill": "Navigation", "rarity": "Uncommon", "price": 70},
    {"name": "Kirk", "skill_level": 10, "skill": "Command", "rarity": "Common", "ability": {"stat": "firepower", "boost": 0.1}},
    {"name": "Spock", "skill_level": 10, "skill": "Science", "rarity": "Common", "ability": {"stat": "mining_efficiency", "boost": 0.1}},
    {"name": "Scotty", "skill_level": 10, "skill": "Engineering", "rarity": "Common", "ability": {"stat": "accuracy", "boost": 0.1}},
    {"name": "McCoy", "skill_level": 10, "skill": "Medical", "rarity": "Common", "ability": {"stat": "max_health", "boost": 0.1}},
    {"name": "Chapel", "skill_level": 9, "skill": "Medical", "rarity": "Uncommon", "price": 80},
    {"name": "M'Benga", "skill_level": 12, "skill": "Medicine", "rarity": "Rare", "ability": {"stat": "crew_recovery_speed", "boost": 0.2}},
    {"name": "LaForge", "skill_level": 11, "skill": "Engineering", "rarity": "Rare", "ability": {"stat": "evasion", "boost": 0.15}},
    {"name": "Data", "skill_level": 13, "skill": "AI Systems", "rarity": "Epic", "ability": {"stat": "scanning_efficiency", "boost": 0.25}},
    {"name": "T'Pol", "skill_level": 12, "skill": "Science", "rarity": "Rare", "ability": {"stat": "mining_output", "boost": 0.2}},
    {"name": "Mayweather", "skill_level": 8, "skill": "Navigation", "rarity": "Common", "price": 60},
    {"name": "Reed", "skill_level": 10, "skill": "Weapons", "rarity": "Uncommon", "ability": {"stat": "critical_hit_chance", "boost": 0.1}},
    {"name": "Pike", "skill_level": 12, "skill": "Command", "rarity": "Rare", "ability": {"stat": "crew_morale", "boost": 0.2}},
    {"name": "Archer", "skill_level": 13, "skill": "Diplomacy", "rarity": "Epic", "ability": {"stat": "trade_bonus", "boost": 0.3}},
    {"name": "Hoshi", "skill_level": 11, "skill": "Linguistics", "rarity": "Rare", "ability": {"stat": "hailing_success_rate", "boost": 0.2}},
    {"name": "Riker", "skill_level": 11, "skill": "Tactics", "rarity": "Rare", "ability": {"stat": "evasion", "boost": 0.2}},
    {"name": "Troi", "skill_level": 10, "skill": "Empathy", "rarity": "Uncommon", "ability": {"stat": "crew_morale", "boost": 0.15}},
    {"name": "Worf", "skill_level": 12, "skill": "Combat", "rarity": "Rare", "ability": {"stat": "boarding_damage", "boost": 0.2}},
    {"name": "Seven of Nine", "skill_level": 14, "skill": "Borg Systems", "rarity": "Epic", "ability": {"stat": "efficiency", "boost": 0.3}},
    {"name": "Paris", "skill_level": 10, "skill": "Pilot", "rarity": "Uncommon", "price": 85},
    {"name": "Janeway", "skill_level": 13, "skill": "Leadership", "rarity": "Epic", "ability": {"stat": "max_shield", "boost": 0.3}},
    {"name": "Tuvok", "skill_level": 12, "skill": "Security", "rarity": "Rare", "ability": {"stat": "resistance_to_hacking", "boost": 0.2}},
    {"name": "Phlox", "skill_level": 12, "skill": "Medicine", "rarity": "Rare", "ability": {"stat": "healing_rate", "boost": 0.25}}
]


    while True:
        clear()
        if cache['tutorial'] == 9:
            print(f"{Fore.YELLOW}Select 1 to upgrade crew.\n{Fore.WHITE}")
        if cache['tutorial'] == 10:
            print(f"{Fore.YELLOW}Type 3 to exit.\n{Fore.WHITE}")
        income_display()
        display_crew(crew_data)

        choice = ask_sanitize(f"{Fore.BLUE}\nEnter 1 to upgrade crew or 2 to purchase new crew 3 to exit: {Fore.WHITE}")
        if choice == 1:
            choice = 'upgrade'
        elif choice == 2:
            choice = 'buy'
        elif choice == 3:
            choice = 'exit'
        if choice == 'upgrade':
            # Upgrade crew
            # Convert to 0-based index
            if cache['tutorial'] == 9:
                print(f"{Fore.YELLOW}Upgrade any crew member:{Fore.WHITE}")
            crew_choice = ask_sanitize(f"{Fore.BLUE}Enter the number of the crew member to upgrade: {Fore.WHITE}") - 1
            cost = 10
            print(f"{Fore.YELLOW}Upgrading {crew_data['crew'][crew_choice]['name']} will cost {cost} recruit tokens. ({cache['recruit_tokens']}->{cache['recruit_tokens'] - cost}){Fore.WHITE}")
            if ask(f"{Fore.RED}Do you want to proceed? (y/n): {Fore.WHITE}") and cache['recruit_tokens'] >= cost:
                upgrade_crew_member(crew_data, crew_choice, cost)
                # Save updated user crew data to file
                save_crew_data(user_crew_file_path, crew_data)
                if cache['tutorial'] == 9:
                    print(f"{Fore.GREEN}Great job upgrading {crew_data['crew'][crew_choice]['name']}. Now you know how to upgrade crew. Exit the crew menu by typing 3 at the menu.{Fore.WHITE}")
                    cache['tutorial'] = 10
                    time.sleep(2)
            else:
                print(f"{Fore.RED}\nRather the Upgrade canceled or you do not have enough recruit tokens.{Fore.WHITE}")
                time.sleep(1)

        elif choice == 'buy':
            # Purchase new crew
            display_available_crew(crew_data, available_crew)
            # Convert to 0-based index
            crew_choice = int(input(f"{Fore.BLUE}Enter the number of the crew member to buy: {Fore.WHITE}")) - 1
            if ask(f"{Fore.RED}Do you want to proceed? (y/n): {Fore.WHITE}"):
                purchase_crew_member(crew_data, available_crew, crew_choice)
            else:
                print(f"{Fore.RED}\nPurchase canceled.{Fore.WHITE}")
                time.sleep(1)

        elif choice == 'exit':
            print(f"{Fore.GREEN}\nExiting...{Fore.WHITE}")
            return
        else:
            print(f"{Fore.RED}Invalid choice{Fore.WHITE}")
            time.sleep(1)


def get_ship_stats_with_crew_effects(ship_name, ship_file):
    try:
        with open(ship_file, 'r') as file:
            data = json.load(file)
            for ship in data[ship_sel]:
                if ship['name'] == ship_name:
                    stats_with_effects = ship.copy()
                    for position, crew_member in ship['crew'].items():
                        if crew_member:
                            crew_data = next((c for c in data['crew'] if c['name'] == crew_member), None)
                            if crew_data:
                                ability = crew_data['ability']
                                boost = crew_data['skill_level'] * ability['boost']
                                stats_with_effects[ability['stat']] *= (1 + boost)

                    return stats_with_effects

        print(f"Ship '{ship_name}' not found.")
        return None
    except FileNotFoundError:
        print("Ship data file not found.")
        return None

def format_position(position):
    if 'bridge' in position.lower():
        return f"Bridge {position[-1]}"
    return position.capitalize()

def format_ability(ability):
    return ' '.join(word.capitalize() for word in ability.split('_'))

def assign_crew_and_adjust_stats(user_crew_file, ship_file):
    try:
        with open(user_crew_file, 'r') as crew_file, open(ship_file, 'r+') as ship_file:
            crew_data = json.load(crew_file)
            ship_data = json.load(ship_file)
            owned_crew = [member for member in crew_data['crew']]
            owned_ships = [ship for ship in ship_data[ship_sel] if ship['owned']]

            if not owned_crew:
                print("No owned crew members available.")
                return
            if not owned_ships:
                print("No owned ships available.")
                return
            if cache['tutorial'] == 8:
                print(f"{Fore.YELLOW}Select the stargazer to assign crew to.{Fore.WHITE}")
            print("\nOwned Ships:")
            for idx, ship in enumerate(owned_ships, start=1):
                print(f"{idx}. {ship['name']}")

            ship_choice = ask_sanitize("\nEnter the number of the ship you want to assign crew to: ") - 1
            selected_ship = owned_ships[ship_choice]
            available_positions = [pos for pos, member in selected_ship['crew'].items() if member is None]
            if not available_positions:
                print(f"{Fore.RED}No available crew positions on this ship.{Fore.WHITE}")
                time.sleep(2)
                return
            if cache['tutorial'] == 8:
                print(f"{Fore.YELLOW}Select any crew member to assign.{Fore.WHITE}")
            print("\nOwned Crew Members:")
            for idx, member in enumerate(owned_crew, start=1):
                ability = format_ability(member['ability']['stat'])
                print(f"{idx}. {member['name']} - {ability} Boost")
            crew_choice = int(input("\nEnter the number of the crew member to assign: ")) - 1
            selected_crew = owned_crew[crew_choice]['name']
            crew_ability = owned_crew[crew_choice]['ability']
            skill_level = owned_crew[crew_choice]['skill_level']

            if selected_crew in selected_ship['crew'].values():
                print(f"{Fore.RED}{selected_crew} is already assigned to this ship.{Fore.WHITE}")
                time.sleep(2)
                return
            if cache['tutorial'] == 8:
                print(f"{Fore.YELLOW}Select any position to assign.{Fore.WHITE}")
            print("\nAvailable Crew Positions:")
            for idx, position in enumerate(available_positions, start=1):
                print(f"{idx}. {format_position(position)}")
            position_choice_index = int(input(f"Choose position for {selected_crew} (enter the number): ")) - 1
            if position_choice_index < 0 or position_choice_index >= len(available_positions):
                print(f"{Fore.RED}Invalid position selected.{Fore.WHITE}")
                time.sleep(2)
                return

            position_choice = available_positions[position_choice_index]

            selected_ship['crew'][position_choice] = selected_crew

            stat_key = crew_ability['stat']
            stat_boost = crew_ability['boost'] * skill_level
            selected_ship[stat_key] = selected_ship.get(stat_key, 1) * (1 + stat_boost)

            ship_file.seek(0)
            json.dump(ship_data, ship_file, indent=4)
            ship_file.truncate()
            print(f"{Fore.BLUE}\nAssigned {selected_crew} to {format_position(position_choice)} on {selected_ship['name']} and increased {format_ability(stat_key)} by {stat_boost * 100}%.{Fore.WHITE}")
            cache['tutorial'] = 9
            time.sleep(3)

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except (IndexError, ValueError) as e:
        print("Invalid input. Please enter a valid number.")

def display_crew_assignments(ship_file):
    try:
        with open(ship_file, 'r') as file:
            ship_data = json.load(file)
            owned_ships = [ship for ship in ship_data[ship_sel] if ship['owned']]
            if not owned_ships:
                print("No owned ships available.")
                return
            print("\nCrew Assignments on Owned Ships:")
            for ship in owned_ships:
                print(f"\n{ship['name']} Crew Assignments:")
                for position, crew_member in ship['crew'].items():
                    if crew_member:
                        print(f"  {format_position(position)}: {crew_member}")
                    else:
                        print(f"  {format_position(position)}: Unassigned")

    except FileNotFoundError:
        print("Ship data file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the ship data file.")

def format_position(position):
    if position == 'captain':
        return 'Captain'
    else:
        return position.capitalize().replace('bridge', 'Bridge')

def income_display():
     print(f"{Fore.YELLOW}Parsteel:{Fore.WHITE} {cache['parsteel']} || {Fore.GREEN}Tritanium:{Fore.WHITE} {cache['tritanium']} || {Fore.CYAN}Dilithium:{Fore.WHITE} {cache['dilithium']} || {Fore.YELLOW}Latinum:{Fore.WHITE} {cache['latinum']} || {Fore.LIGHTBLUE_EX}Current Ship:{Fore.WHITE} {cache['ship']} || {Fore.LIGHTBLUE_EX}Current System:{Fore.WHITE} {systems[cache['current_system']]} || {Fore.BLUE}Health:{Fore.WHITE} {load_ship_stat(ship_name=cache['ship'], stat_key='health') * research_multi('Sheild Dynamics')}/{research_multi('Sheild Dynamics') * load_ship_stat(ship_name=cache['ship'], stat_key='max_health')} || {Fore.GREEN}Storage Avalible:{Fore.WHITE} {load_ship_stat(ship_name=cache['ship'], stat_key='storage')}/{research_multi('Inventory Management Systems') * load_ship_stat(ship_name=cache['ship'], stat_key='max_storage')}")

def ask(question):
        response = input(question)
        return response.lower() in ["y", "yes"]

def view_upgrades():
    clear()
    upgrades = cache['upgrades']
    print(f"{Fore.GREEN}Your upgrades:{Fore.WHITE}\n{chr(10).join([u + ': Level ' + str(upgrades[u]) for u in upgrades.keys()])}")
    continue_1 = ask(f'{Fore.RED}Continue? {Fore.WHITE}')
    if continue_1 == ('y', 'yes'):
        time.sleep(0.001)

def accept_mission(mission_id):
    mission_list = {'1': 'Mine 100 Materials', '2': 'Defeat 1 Enemy', '3': 'Defeat 3 Enemies', '4': 'Trade 200 Materials With a Ship', '5': 'Defeat 5 Enemies', '6': 'Explore 3 New Systems', '7': 'Buy a new Ship', '8': 'Complete 2 Successful Trades', '9': 'Respond to the Distress Signal in Regula', '10': 'Survey the Rings of Tarkalea XII', '11': 'Protect Dilithium Convoy', '12': 'Scan for Anomalies', '13': 'Recover Lost Data', '14': 'The Starship Graveyard', '15': 'First Contact', '16': 'Sabotage Mission', '17': 'Emergency Supply Run', '18': 'Latinum Heist', '19': 'Minefield Mapping', '20': 'The Alien Probe', '21': 'Temporal Anomaly'}
    missions = cache['missions']
    mission_name = mission_list.get(mission_id)
    if mission_name and not missions[mission_name]['completed']:
        missions[mission_name]['accepted'] = True
        cache['missions'] = missions
        print(f"{Fore.GREEN}Mission '{mission_name}' accepted.{Fore.WHITE}")
        time.sleep(2)
    else:
        print("Mission either doesn't exist or is already completed.")
        time.sleep(1)

def update_mission_progress(mission_name, progress_increment):
    missions = cache['missions']

    if mission_name in missions and missions[mission_name]['accepted'] and not missions[mission_name]['completed']:
        missions[mission_name]['progress'] += progress_increment
        cache['missions'] = missions
        # Define mission completion targets in a dictionary
        mission_targets = {'Mine 100 Materials': 100, 'Defeat 1 Enemy': 1, 'Defeat 3 Enemies': 3, 'Trade 200 Materials With a Ship': 200, 'Defeat 5 Enemies': 5, 'Explore 3 New Systems': 3, 'Buy a new Ship': 1, 'Complete 2 Successful Trades': 2, 'Respond to the Distress Signal in Regula': 1, 'Survey the Rings of Tarkalea XII': 1, 'Protect Dilithium Convoy': 4, 'Scan for Anomalies': 3, 'Recover Lost Data': 5, 'The Starship Graveyard': 3, 'First Contact': 4, 'Sabotage Mission': 1, 'Emergency Supply Run': 1, 'Latinum Heist': 1, 'Minefield Mapping': 1, 'The Alien Probe': 1, 'Temporal Anomaly': 1}
        # Check if mission meets completion criteria
        if mission_name in mission_targets and missions[mission_name]['progress'] >= mission_targets[mission_name]:
            complete_mission(mission_name)
    else:
        return


def complete_mission(mission_name):
    mission_rewards = {'Mine 100 Materials': 10, 'Defeat 1 Enemy': 10, 'Defeat 3 Enemies': 20, 'Trade 200 Materials With a Ship': 25, 'Defeat 5 Enemies': 40, 'Explore 3 New Systems': 40, 'Buy a new Ship': 50, 'Complete 2 Successful Trades': 70, 'Respond to the Distress Signal in Regula': 50, 'Survey the Rings of Tarkalea XII': 50, 'Protect Dilithium Convoy': 75, 'Scan for Anomalies': 50, 'Recover Lost Data': 100, 'The Starship Graveyard': 35, 'First Contact': 80, 'Sabotage Mission': 60, 'Emergency Supply Run': 40, 'Latinum Heist': 120, 'Minefield Mapping': 60, 'The Alien Probe': 100, 'Temporal Anomaly': 140}
    missions = cache['missions']
    coins = cache['latinum']

    if not missions[mission_name]['completed']:
        missions[mission_name]['completed'] = True
        missions[mission_name]['accepted'] = False
        reward = load_building_data('buildings')['starbase']['upgrades']['Ops'] * mission_rewards[mission_name]
        coins += reward
        cache['missions'] = missions
        save_data('missions', missions)
        cache['latinum'] = coins
        print(f"{Fore.GREEN}Mission '{mission_name}' completed! You earned {reward} latinum.{Fore.WHITE}")
        time.sleep(2)

def display_missions():
    mission_data = cache['missions']

    if mission_data is None:
        print("No missions available.")
        return

    print("Current Missions:")

    for mission_name, mission_info in mission_data.items():
        if mission_info["accepted"]:
            status = "Accepted"
            progress = mission_info["progress"]
            progress_message = f"Progress: {progress}"
        else:
            status = "Not Accepted"
            progress_message = "Progress: N/A"

        if mission_info["completed"]:
            status = "Completed"
            progress_message = "Progress: 100%"

        print(f"{Fore.BLUE}{mission_name}: {Fore.GREEN}{status} - {Fore.YELLOW}{progress_message}{Fore.WHITE}")


def load_explored(system):
    if cache['explored'][system] == 1:
        return 1
    else:
        return 2

def save_explored(system):
    systems1 = cache['explored']
    if systems1 is None:
        return
    if system in systems1:
        systems1[system] = 1
    else:
        return
    cache['explored'] = systems1

def battle_stat(opponent_health, opponent_name, income, accuracy, firepower, evasion):
    if cache['tutorial'] == 2:
        print(f"{Fore.YELLOW}Type y and start the battle! The computer will fight for you based on your stats.{Fore.WHITE}")
    print(f'{Fore.RED}You are attacking the {opponent_name}! This ship has {opponent_health} health, and if you win, you get {income} materials.{Fore.WHITE}')
    time.sleep(3)
    print(f"{Fore.YELLOW}YELLOW ALERT{Fore.WHITE}")
    time.sleep(2)
    print(f"{Fore.BLUE}Your ship stats:\nFirepower: {(research_multi('Phaser Calibration') * load_ship_stat(ship_name=cache['ship'], stat_key='firepower'))}\nAccuracy: {(research_multi('Targeting Matrix') * load_ship_stat(ship_name=cache['ship'], stat_key='accuracy'))}\nEvasion: {(research_multi('Evasive Maneuvers') * load_ship_stat(ship_name=cache['ship'], stat_key='evasion'))}{Fore.WHITE}")
    print(f"{Fore.YELLOW}Enemy ships stats:\nFirepower: {firepower}\nAccuracy: {accuracy}\nEvasion: {evasion}{Fore.WHITE}")
    if cache['missions']['Respond to the Distress Signal in Regula']['progress'] == 2 or cache['missions']['Protect Dilithium Convoy']['progress'] == 1:
        time.sleep(3)
        input("Press Enter to Fight... ")
        fight = 1
    else:
        if ask('Do you want to battle this enemy? '):
            fight = 1
        else:
            fight = 2
    if fight == 1:
        clear()
        print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
        while (load_ship_stat(ship_name=cache['ship'], stat_key='health')) > 0 or opponent_health > 0:
            turn = 'player'
            if turn == 'player':
                if random.uniform(0, 1) < (research_multi('Targeting Matrix') / evasion + 1):
                    damage = research_multi('Phaser Calibration') * random.uniform(50, 200)
                    opponent_health -= damage
                    print(f"{Fore.GREEN}Enemy Hit! {opponent_name} took {damage:.2f} damage. Enemy health: {opponent_health:.2f}{Fore.WHITE}")
                    time.sleep(3)
                    turn = 'enemy'
                else:
                    print(f"{Fore.RED}You missed!{Fore.RED}")
                    time.sleep(2)
                    turn = 'enemy'
            if (load_ship_stat(cache['ship'], 'health')) <= 0:
                break
            if opponent_health <= 0:
                break
            if turn == 'enemy':
                if random.uniform(0, 1) < (accuracy / (research_multi('Targeting Matrix') + 1)):
                    damage = firepower * random.uniform(50, 150)
                    save_ship_data(stat_key='health', value=round(load_ship_stat(cache['ship'], 'health') - damage), ship_name=cache['ship'])
                    print(f"{Fore.RED}You have been hit! You took {damage:.2f} damage. Your health: {load_ship_stat(cache['ship'], 'health'):.2f}{Fore.WHITE}")
                    time.sleep(3)
                    turn = 'player'
                else:
                    print(f"{Fore.GREEN}{opponent_name} missed!{Fore.WHITE}")
                    time.sleep(2)
                    turn = 'player'
            if (load_ship_stat(cache['ship'], 'health')) <= 0:
                break
            if opponent_health <= 0:
                break
    if (load_ship_stat(cache['ship'], 'health')) <= 0:
            check_health()
            return
    if opponent_health <= 0:
                clear()
                if cache['tutorial'] == 2:
                    print(f"{Fore.GREEN}Great job! You won the battle. In a moment, you will get the rewards for your battle. You have 5 seconds to view them, then you automatically exit.\nAfter these rewards, return to drydock.{Fore.WHITE}")
                    time.sleep(3)
                print(f'{Fore.GREEN}You Win!{Fore.WHITE}')
                print(f'{Fore.BLUE}Parsteel Gained: {Fore.WHITE}', income)
                print(f'{Fore.BLUE}Dilithium Gained: {Fore.WHITE}', (income/2))
                lat_reward = random.randint(1, 5)
                print(f'{Fore.BLUE}Latinum Gained: {Fore.WHITE}', lat_reward)
                save_ship_data(ship_name=cache['ship'], stat_key='storage', value=load_ship_stat(ship_name=cache['ship'], stat_key='storage') - (income + (income/2) + lat_reward))
                save_ship_data(ship_name=cache['ship'], stat_key='parsteel_storage', value=load_ship_stat(ship_name=cache['ship'], stat_key='parsteel_storage') + income)
                save_ship_data(ship_name=cache['ship'], stat_key='dilithium_storage', value=load_ship_stat(ship_name=cache['ship'], stat_key='dilithium_storage') + (income/2))
                save_ship_data(ship_name=cache['ship'], stat_key='latinum_storage', value=load_ship_stat(cache['ship'], 'latinum_storage') + lat_reward)
                update_mission_progress('Defeat 1 Enemy', 1)
                update_mission_progress('Defeat 3 Enemies', 1)
                update_mission_progress('Defeat 5 Enemies', 1)
                update_mission_progress('Protect Dilithium Convoy', 1)
                cache['tutorial'] = 3
                time.sleep(5)

ship_attributes = ["firepower", "accuracy", "evasion", "health", "storage", "mining", "warp"]

base_ship_stats = {
    "Stargazer": (1, 1, 1, 1000, 750, 1, 2),
    "USS Grissom": (1, 2, 2, 2000, 800, 2, 4),
    "Realta": (2, 2, 3, 1500, 600, 2, 3),
    "Federation Shuttlecraft": (1, 2, 3, 3500, 750, 2, 4),
    "Daedalus Class Medical": (1, 1, 2, 1000, 500, 1, 3),
    "Ambassadors Shuttle": (2, 2, 3, 1200, 600, 1, 4),
    "USS Constitution": (3, 4, 4, 2500, 1000, 3, 6),
    "Galaxy Class": (5, 6, 5, 5000, 2500, 4, 8),
    "Ferengi D'Kora": (4, 4, 5, 2200, 1000, 3, 5),
    "Klingon K'Vort": (6, 5, 6, 3000, 1500, 4, 7),
    "Romulan Warbird": (8, 7, 8, 4000, 1800, 5, 10),
    "USS Excelsior": (6, 6, 7, 3500, 1600, 4, 9),
    "USS Enterprise (NCC-1701 D)": (10, 9, 10, 6000, 2500, 6, 12)
}

def get_ship_stats(ship_name):
    stats = base_ship_stats.get(ship_name)
    if stats:
        return dict(zip(ship_attributes, stats))
    return None

def check_health():
    ship_name = cache['ship']
    if load_ship_stat(ship_name, 'health') <= 0:
        clear()
        print(f"{Fore.RED}Ship {ship_name} has been destroyed!{Fore.WHITE}")
        materials_lost = sum([
            load_ship_stat(ship_name, stat) for stat in ['parsteel_storage', 'tritanium_storage', 'dilithium_storage', 'latinum_storage']
        ])
        print(f"{Fore.RED}Materials Lost: {materials_lost}{Fore.WHITE}")
        
        reset_stats = get_ship_stats(ship_name)
        if reset_stats:
            reset_stats.update({
                'parsteel_storage': 0,
                'tritanium_storage': 0,
                'dilithium_storage': 0,
                'latinum_storage': 0,
                'mining_efficiency': reset_stats.pop('mining'),
                'warp_range': reset_stats.pop('warp'),
                'owned': 'false',
                'equipped': 'false'
            })
            for stat, value in reset_stats.items():
                save_ship_data(ship_name, stat, value)
        
        reset_crew_positions(ship_name)
        cache['ships'] = 'Stargazer'
        save_ship_data('Stargazer', 'owned', 'true')
        save_ship_data('Stargazer', 'equipped', 'true')
        time.sleep(5)


def mining_deposit(mine_type, mine_num, mine_capitalize):
    global tutorial_highlight1, tutorial_highlight
    income_display()

    # Cache some frequently used values
    current_system = cache['current_system']
    ship_name = cache['ship']
    tutorial_stage = cache['tutorial']

    # Tutorial messages
    if tutorial_stage == 0:
        print(f"{Fore.YELLOW}Type y to enter mining mode, and then select how much parsteel you want to mine.\n{Fore.WHITE}")
    elif tutorial_stage == 6:
        print("Type y to enter mining mode, and then select how much tritanium you want to mine.\n")

    print(f"You have approached a {mine_capitalize} Mine!")
    deposit_materials = get_material_in_node(system_name=systems[current_system], mine_name=mine_num)
    mining_efficiency = research_multi('Mining Laser') * load_ship_stat(ship_name, 'mining_efficiency')
    deposit_var = deposit_materials / mining_efficiency
    print(f"{Fore.BLUE}This mine has {deposit_materials} {mine_type}.{Fore.WHITE}")
    print(f"{Fore.GREEN}Estimated mining time: {deposit_var * 0.5} seconds{Fore.WHITE}")
    if ask(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}'):
        mine_depo_mats = ask_sanitize(f'{Fore.GREEN}How much would you like to mine? (1 - {deposit_materials}){Fore.WHITE}')
        while mine_depo_mats > 0 and get_material_in_node(system_name=systems[current_system], mine_name=mine_num) > 0:
            clear()
            print("Mining...")
            print(f"{mine_capitalize} Remaining: {mine_depo_mats}")
            print(f'Total Storage Remaining: {load_ship_stat(ship_name, "storage")}')
            materials_gathered = 1 * mining_efficiency
            save_ship_data(ship_name, f'{mine_type}_storage', load_ship_stat(ship_name, f'{mine_type}_storage') + materials_gathered)
            save_ship_data(ship_name, 'storage', load_ship_stat(ship_name, 'storage') - materials_gathered)
            update_mission_progress('Mine 100 Materials', materials_gathered)
            update_materials(system_name=systems[current_system], mine_name=mine_num, amount=mining_efficiency)
            estimated_time_remaining = (mine_depo_mats / mining_efficiency) * 0.5
            print(f'{Fore.GREEN}Estimated Time remaining: {estimated_time_remaining} Seconds {Fore.WHITE}')
            if research_multi('Inventory Management Systems') < 0:
                clear()
                print(f'{Fore.RED}Your ship has run out of storage. Please return to drydock to empty your cargo to your station.{Fore.WHITE}')
                time.sleep(2)
                break
            mine_depo_mats -= mining_efficiency
            time.sleep(0.5)
        if tutorial_stage == 0:
            cache['tutorial'] = 1
        elif tutorial_stage == 6:
            cache['tutorial'] = 7
        tutorial_highlight1 = Fore.WHITE
        tutorial_highlight = Fore.WHITE

def accept_missions():
    mission_selection = ask_sanitize('Select mission to accept: ')
    # Check if the selection is valid
    if 1 <= mission_selection <= len(mission_list_print):
        if ask(f"{Fore.YELLOW}Are you sure you want to accept this mission? (Y/N): {Fore.WHITE}"):
            accept_mission(str(mission_selection))
    elif mission_selection == len(mission_list_print) + 1:
        return


def scan_system():
    exploration_time = random.randint(10, 60)
    if cache['tutorial'] == 6:
        print(f"{Fore.YELLOW}When you come across a new system and you haven't explored it, you need to scan the system. Type y to explore it.{Fore.WHITE}")
        time.sleep(2)
    if ask(f"{Fore.RED}System {systems[cache['current_system']]} has not been explored. Would you like to scan this system? This will take you {exploration_time} seconds. (Y/N): {Fore.WHITE}"):
        while exploration_time > 0:
            clear()
            income_display()
            print(f"{Fore.GREEN}Scanning {systems[cache['current_system']]}...{Fore.WHITE}")
            print(f"{Fore.YELLOW}Time Remaining: {exploration_time}{Fore.WHITE}")
            exploration_time -= 0.5
            time.sleep(0.5)
        print(f"{Fore.GREEN}Scan complete! You may now navigate the system.{Fore.WHITE}")
        update_mission_progress('Explore 3 New Systems', 1)
        save_explored(systems[cache['current_system']])
        time.sleep(2)


def execute_trade(storage_type, trade_am, item_name, give_am, trade_type):
    if load_ship_stat(cache['ship'], storage_type) >= trade_am or load_data(item_name) >= trade_am:
        if ask(f"{Fore.YELLOW}You are going to trade {trade_am} {item_name} for {give_am} {trade_type}. Are you sure you want to do this? (Y/N): {Fore.WHITE}"):
            if load_ship_stat(cache['ship'], storage_type) >= trade_am:
                save_ship_data(cache['ship'], storage_type, load_ship_stat(cache['ship'], storage_type) - trade_am)
                save_ship_data(cache['ship'], f'{trade_type.lower()}_storage', load_ship_stat(cache['ship'], f'{trade_type.lower()}_storage') + give_am)
                save_ship_data(cache['ship'], 'storage', load_ship_stat(cache['ship'], 'storage') - give_am)
            else:
                cache[item_name] -= trade_am
                cache[f'{trade_type.lower()}'] += give_am

            print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
            update_mission_progress('Complete 2 Successful Trades', 1)
            update_mission_progress('Trade 200 Materials With a Ship', trade_am)
            time.sleep(2)
        else:
            print('Trade Canceled.')
            time.sleep(1)
    else:
        print(f"{Fore.RED}Not enough {item_name} for trade.{Fore.WHITE}")
        time.sleep(1)


def trading(dil_trade_am, tri_trade_am, par_trade_am):
    income_display()
    print('Available Items:')
    avalible = [
        f"Trade {dil_trade_am} Dilithium for {tri_trade_am} Tritanium",
        f"Trade {par_trade_am} Parsteel for {tri_trade_am} Tritanium",
        f"Trade {tri_trade_am} Tritanium for {par_trade_am} Parsteel",
        f"Trade {par_trade_am} Parsteel for {dil_trade_am} Dilithium"
    ]
    for i, option in enumerate(avalible, 1):
        print(f"{i}. {option}")
    print(f"{len(avalible) + 1}. Exit")
    trade_input = ask_sanitize("Option: ")
    if trade_input == 1:
        execute_trade('dilithium_storage', dil_trade_am, 'dilithium', tri_trade_am, 'Tritanium')
    elif trade_input == 2:
        execute_trade('parsteel_storage', par_trade_am, 'parsteel', tri_trade_am, 'Tritanium')
    elif trade_input == 3:
        execute_trade('tritanium_storage', tri_trade_am, 'tritanium', par_trade_am, 'Parsteel')
    elif trade_input == 4:
        execute_trade('parsteel_storage', par_trade_am, 'parsteel', dil_trade_am, 'Dilithium')
    elif trade_input == 5:
        print('Exiting Trade.')
        time.sleep(1)
    else:
        print('Please input a valid number.')

finding_var = 0
def find_system_number(system_name):
    for key, value in systems.items():
        if value == system_name:
            return key
    return None

def navigate():
    global current_system
    global warp_time
    global max_system
    global tutorial_highlight6

    warp_range = round(research_multi('Warp Mathematics') * load_ship_stat(cache['ship'], 'warp_range'))
    max_system = len(systems)

    reachable_systems = {
        key: value for key, value in systems.items()
        if cache['current_system'] - warp_range <= key <= warp_range
    }

    print(f"{Fore.BLUE}You are currently in {systems[cache['current_system']]}{Fore.WHITE}")

    if ask(f'{Fore.BLUE}Would you like to navigate to another system? {Fore.WHITE}'):
        clear()
        print(f'{Fore.BLUE}Systems in Warp Range:{Fore.WHITE}')
        for key, value in reachable_systems.items():
            print(f'{key}: {value}')

        while True:
            try:
                if cache['tutorial'] == 5:
                    print(f"{Fore.YELLOW}Type 2 to navigate to vulcan.{Fore.WHITE}")
                system_number = ask_sanitize(f'{Fore.BLUE}Which system number would you like to travel to? {Fore.WHITE}')
                if system_number in reachable_systems:
                    target_system = system_number
                    warp_time = abs(cache['current_system'] - target_system) * 10
                    print(f'{Fore.RED}Traveling to {reachable_systems[target_system]}. Estimated time: {warp_time} seconds.{Fore.WHITE}')
                    time.sleep(1)
                    travel_bar(systems[cache['current_system']], systems[target_system], warp_time, 30)
                    cache['current_system'] = target_system
                    print(f"Arrived at {systems[cache['current_system']]}.")
                    if cache['current_system'] == 2 and cache['tutorial'] == 5:
                        cache['tutorial'] = 6
                    time.sleep(2)
                    break
                else:
                    print(f'{Fore.RED}Invalid system number. Please choose a number from the list.{Fore.WHITE}')
            except ValueError:
                print(f'{Fore.RED}Please enter a valid number.{Fore.WHITE}')
    else:
        return False

# Load user resources like parsteel, tritanium, etc.
def load_user_data():
    user_data = {}

    try:
        # Load resource and user data keys
        keys = [
            'parsteel', 'tritanium', 'dilithium', 'latinum',
            'recruit_tokens', 'ship', 'current_system', 'reputation', 
            'stargazer_blueprints', 'uss_grissom_blueprints',
            'federation_shuttlecraft_blueprints', 'galaxy_class_blueprints',
            'realta_blueprints', 'daedalus_medical_blueprints',
            'ambassadors_shuttle_blueprints', 'uss_constitution_blueprints',
            'ferengi_dkora_blueprints', 'klingon_kvort_blueprints',
            'romulan_warbird_blueprints', 'uss_excelsior_blueprints',
            'ncc_1701_d_blueprints'
        ]

        # Dynamically load all keys
        for key in keys:
            user_data[key] = load_data(key)

        return user_data
    except Exception as e:
        print(f"Error loading user data: {e}")
        return None

# Save user resources back to user_data.json
def save_user_data(user_data):
    try:
        # Get all keys from user_data and save them
        for key, value in user_data.items():
            cache[key] = value # Dynamically save each key-value pair
    except Exception as e:
        print(f"Error saving user data: {e}")


def load_shop():
    try:
        with open('daily_shop.json', 'r') as file:
            shop_data = json.load(file)
        return shop_data
    except FileNotFoundError:
        print("Shop data not found. Creating new shop.")
        return create_new_shop()

# Save shop data to JSON
def save_shop(shop_data):
    with open('daily_shop.json', 'w') as file:
        json.dump(shop_data, file, indent=4)

# Create a new daily shop with predefined items
def create_new_shop():
    # List of available shop items
    shop_items = [
        {"item_name": f"{amount} {item} Blueprints", "price": price, "resource_key": item.lower().replace(' ', '_').replace("'", "") + '_blueprints', "amount": amount}
        for item, price, amounts in [
            ("Stargazer", 10, [5, 10, 20, 50, 100]),
            ("USS Grissom", 10, [5, 15, 30, 60, 100]),
            ("Realta", 15, [5, 10, 20, 50, 100]),
            ("Federation Shuttlecraft", 20, [5, 15, 30, 50, 100]),
            ("Daedalus Class Medical", 25, [5, 10, 20, 50, 100]),
            ("Ambassadors Shuttle", 30, [5, 10, 20, 50, 100]),
            ("USS Constitution", 40, [5, 10, 20, 50, 100]),
            ("Galaxy Class", 50, [10, 20, 30, 50, 100]),
            ("Ferengi DKora", 60, [5, 10, 20, 50, 100]),
            ("Klingon KVort", 70, [5, 10, 20, 50, 100]),
            ("Romulan Warbird", 80, [5, 10, 20, 50, 100]),
            ("USS Excelsior", 90, [5, 10, 20, 50, 100]),
            ("USS Enterprise (NCC-1701 D)", 100, [10, 20, 30, 50, 100]),
        ]
        for amount in amounts
    ]
    
    recruit_token_addon = [
        {"item_name": f"{amount} {item}", "price": price, "resource_key": item.lower().replace(' ', '_').replace("'", ""), "amount": amount}
        for item, price, amounts in [
            ("Recruit Tokens", 5, [50, 100, 200, 300, 400])
        ]
        for amount in amounts
    ]

    # Randomly select 5-8 items
    selected_items = random.sample(shop_items, random.randint(5, 8)) + random.sample(recruit_token_addon, random.randint(1, 1))

    # Create and save shop data
    shop_data = {"last_updated": str(datetime.now().date()), "items": selected_items}
    save_shop(shop_data)
    return shop_data


# Update the shop daily (based on system date)
def update_shop_daily():
    shop_data = load_shop()
    last_updated = shop_data["last_updated"]

    # Check if the shop needs to be updated (compare the dates)
    if last_updated != str(datetime.now().date()):
        print("Updating shop for the new day...")
        shop_data = create_new_shop()

    return shop_data

# Display the shop
def display_shop(shop_data):
    clear()
    income_display()
    print(f"\n{Fore.BLUE}Daily Shop{Fore.WHITE}")
    print('')
    for index, item in enumerate(shop_data["items"], start=1):
        print(f"{index}. {item['item_name']} - {item['price']} latinum")
    print("")

# Purchase an item from the shop and update user resources
def purchase_item(item_index, shop_data, user_data):

    # Ensure the index is valid
    if item_index < 1 or item_index > len(shop_data["items"]):
        print("Invalid item number.")
        return

    # Get the selected item
    item = shop_data["items"][item_index - 1]
    item_name = item["item_name"]
    item_price = item["price"]
    resource_key = item["resource_key"]
    amount = item["amount"]

    # Check if the player has enough currency
    if cache['latinum'] >= item_price:

        # Update the user's resource (e.g., Parsteel, Tritanium, etc.)
        if resource_key in user_data:
            if resource_key == "health" and amount == "full":
                # Assuming 100 is full health
                user_data["health"] = 100
            else:
                user_data[resource_key] += amount

            cache['latinum'] -= item_price
            print(f"Purchased {item_name} for {item_price} latinum.")
            print(f"Remaining latinum: {cache['latinum']}")
            cache[resource_key] += amount
            time.sleep(2)
        else:
            print(f"Invalid resource key: {resource_key}.")
            time.sleep(2)
    else:
        print(f"{Fore.RED}Not enough latinum to buy this item.{Fore.WHITE}")

# Main shop loop
def shop_loop():
    # Load user resources like Parsteel, Tritanium, etc.
    user_data = load_user_data()

    if not user_data:
        # Exit if user data can't be loaded
        return

    # Check for daily update
    shop_data = update_shop_daily()

    while True:
        if cache['tutorial'] == 11:
            print(f"{Fore.YELLOW}This is the ship! Here, everything costs latinum. To get latinum, you need to complete missions by exploring a system, and accepting missions from a mission planet.{Fore.WHITE}")
        display_shop(shop_data)
        command = input("Enter the number to buy, or 'e' to leave: ")

        if command.lower() == "e":
            print("Exiting shop.")
            if cache['tutorial'] == 11:
                cache['tutorial'] = 12
            break

        if command.isdigit():
            if ask(f"{Fore.YELLOW}Are you sure you want to buy this? (Y/N): {Fore.WHITE}"):
                purchase_item(int(command), shop_data, user_data)

player_reputation = cache['reputation']

def ship_reply(choice, ship_type, progress):
    global player_reputation

    # Ship interaction templates
    ship_reactions = {
        "greet": {
            "friendly": "Hello, traveler! How can we assist you today?",
            "neutral": "Greetings. Do not cause trouble." if not progress['greeted'] else "We’ve already exchanged greetings. What do you want?",
            "hostile": "Your pleasantries are useless here!" if not progress['greeted'] else "Still trying to talk? We are not interested!"
        },
        "trade": {
            "friendly": "Glad to trade with you!",
            "neutral": "We're neutral, but we might trade." if progress['greeted'] else "We are not traders. Move along.",
            "hostile": "We do not deal with your kind."
        }
    }

    # Default replies based on the choice and ship type
    if choice == 1:
        reply = ship_reactions["greet"].get(ship_type, "That choice does not seem to apply here.")
    elif choice == 2:
        reply = ship_reactions["trade"].get(ship_type, "That choice does not seem to apply here.")
    else:
        reply = "That choice does not seem to apply here."

    clear()
    income_display()
    return reply

def hailing_frequency():
    global player_reputation

    ship_types = ["friendly", "neutral", "hostile"]
    current_ship = random.choice(ship_types)

    # Reputation affects initial ship behavior
    if current_ship == "hostile" and player_reputation > 70:
        current_ship = "neutral"
        print("This hostile ship recognizes your reputation and is neutral for now.")
        time.sleep(2)

    # Track conversation progress
    progress = {'greeted': False, 'traded': False}
    clear()
    income_display()

    print(f"{Fore.GREEN}Hailing frequency opened. You've encountered a {current_ship} ship.{Fore.WHITE}")

    # Handle the conversation
    while True:
        print("\nWhat would you like to say?")
        print("1. Greet the ship")
        print("2. Ask to trade")
        print("3. Exit the conversation")

        try:
            choice = int(input("\nSelect an option by entering the number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 3:
            print("Hailing frequency closed.")
            time.sleep(2)
            break

        if choice in [1, 2]:
            npc_reply = ship_reply(choice, current_ship, progress)
            print(f"{Fore.YELLOW}Ship: {npc_reply}{Fore.WHITE}")

            # Handle player reputation and progress
            if choice == 1 and progress['greeted'] and current_ship == "friendly":
                print("The ship is beginning to trust you.")
                player_reputation += 5
                cache['reputation'] = player_reputation

            elif choice == 2 and current_ship == "neutral" and progress['greeted']:
                print("The neutral ship is considering trading with you.")
                # Randomize the trade amounts
                dil_trade_am = random.randint(10, 100)
                tri_trade_am = random.randint(10, 100)
                par_trade_am = random.randint(10, 100)
                # Call the trading function with random amounts
                trading(dil_trade_am, tri_trade_am, par_trade_am)
                player_reputation += 5
                cache['reputation'] = player_reputation

            else:
                print(f"Current Reputation: {player_reputation}")
        else:
            print("Invalid option. Please select a number between 1 and 3.")

def load_building_data(key, building_name=None):
    try:
        with open(buildings_path, 'r') as file:
            data = json.load(file)

        if building_name:
            if building_name in data['buildings']:
                return data['buildings'][building_name]
            else:
                print(f"Building '{building_name}' not found in buildings data.")
                return None
        else:
            return data.get(key, None)

    except FileNotFoundError:
        print("Buildings data file not found.")
        return None
    except KeyError as e:
        print(f"Key '{key}' not found in buildings data.")
        return None

def load_specific_upgrade(building_name, upgrade_part):
    try:
        with open(buildings_path, 'r') as file:
            data = json.load(file)
        if building_name in data['buildings']:
            building = data['buildings'][building_name]
            if upgrade_part in building['upgrades']:
                return building['upgrades'][upgrade_part]
            else:
                print(f"Upgrade '{upgrade_part}' not found for {building_name}.")
                return None
        else:
            print(f"Building '{building_name}' not found.")
            return None

    except FileNotFoundError:
        print("Buildings data file not found.")
        return None


def save_building_data(key, value, building_name=None):
    try:
        with open(buildings_path, 'r+') as file:
            data = json.load(file)

            if building_name:
                if building_name in data['buildings']:
                    data['buildings'][building_name][key] = value
                else:
                    print(f"Building '{building_name}' not found in buildings data.")
                    return
            else:
                data[key] = value

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Buildings data file not found.")


def start_construction(building_name, completion_time, upgrade_part=None):
    user_data = cache['construction_queue']


    if user_data['building'] is None:
        current_time = datetime.now()
        start_time = current_time.isoformat()
        end_time = (current_time + timedelta(seconds=completion_time)).isoformat()

        # Update the construction queue in user data
        construction_data = {
            'building': building_name,
            'upgrade_part': upgrade_part,
            'start_time': start_time,
            'end_time': end_time
        }
        cache['construction_queue'] = construction_data

        # If an upgrade part is provided, record it
        if upgrade_part:
            # Check if the upgrade exists in the building's upgrades
            building_data = load_building_data('buildings', building_name)
            if upgrade_part in building_data['upgrades']:
                print(f"{Fore.GREEN}Starting upgrade of {upgrade_part} for {building_name}. Estimated completion: {end_time}{Fore.WHITE}")
                time.sleep(2)
            else:
                print(f"Upgrade '{upgrade_part}' does not exist for {building_name}.")
        else:
            print(f"Starting construction of {building_name}. Estimated completion: {end_time}")
    else:
        print(f"{Fore.RED}Construction queue is already occupied.{Fore.WHITE}")

def check_construction_completion():
    # Load the current construction queue data
    construction_data = cache['construction_queue']

    if construction_data['building'] is not None and construction_data['end_time'] is not None:
        # Convert the end_time string to a datetime object
        end_time = datetime.fromisoformat(construction_data['end_time'])
        current_time = datetime.now()

        # Check if the current time is greater than or equal to the end time
        if current_time >= end_time:
            building_name = construction_data['building']
            # Get the upgrade part if it exists
            upgrade_part = construction_data.get('upgrade_part')

            print(f"{Fore.GREEN}Construction of {upgrade_part} is complete!{Fore.WHITE}")
            if upgrade_part == 'Academy':
                random_val = random.randint((load_building_data('buildings')['starbase']['upgrades']['Academy']) * 10, (load_building_data('buildings')['starbase']['upgrades']['Academy']) * 20)
                print(f"{Fore.GREEN}Recruit Tokens Earned: {random_val}{Fore.WHITE}")
                cache['recruit_tokens'] += random_val
                random_val = random.randint((load_building_data('buildings')['starbase']['upgrades']['Academy']), (load_building_data('buildings')['starbase']['upgrades']['Academy']) * 3)
                print(f"{Fore.GREEN}Latinum Earned: {random_val}{Fore.WHITE}")
                cache['latinum'] += random_val

            # Apply the specific upgrade
            apply_upgrade(building_name, upgrade_part)

            # Reset the construction queue to null after completion
            cache['construction_queue'] = ('construction_queue', {
                'building': None,
                'start_time': None,
                'end_time': None,
                'upgrade_part': None
            })

            time.sleep(2)

        else:
            # Calculate remaining time
            remaining_time = (end_time - current_time).total_seconds()
            print(f"{Fore.YELLOW}Construction in progress. Time remaining: {round(remaining_time)} seconds.{Fore.WHITE}")
    else:
        print(f"{Fore.RED}No construction is in progress.{Fore.WHITE}")


# Function to apply the upgrade
def apply_upgrade(building_name, upgrade_part):
    # Load the current buildings data from buildings.json
    buildings_data = load_building_data('buildings')

    if building_name in buildings_data:
        building = buildings_data[building_name]

        # Check if the upgrade part exists in the building
        if upgrade_part in building['upgrades']:
            current_level = building['upgrades'][upgrade_part]
            # Increase the upgrade level by 1
            new_level = current_level + 1

            # Update the building's upgrade level
            building['upgrades'][upgrade_part] = new_level
            print(f"{Fore.GREEN}Upgrade '{upgrade_part}' for {building_name} is now at level {new_level}.{Fore.WHITE}")

            # Save the updated building data back to buildings.json
            save_building_data('upgrades', building['upgrades'], building_name)
        else:
            print(f"Upgrade '{upgrade_part}' not found for {building_name}.")
    else:
        print(f"Building '{building_name}' not found.")

def calculate_production_rate(building_name, upgrade_part):
    # Load the building data
    building_data = load_building_data('buildings', building_name)

    if building_name in building_data['buildings']:
        building = building_data['buildings'][building_name]

        # Check if the upgrade part exists in the building
        if upgrade_part in building['upgrades']:
            upgrade_level = building['upgrades'][upgrade_part]

            # Define the base production rate (could vary per building)
            base_rate = 10

            # Multiply the base rate by the upgrade level to get the new production rate
            new_rate = base_rate * upgrade_level

            print(f"With '{upgrade_part}' upgrade at level {upgrade_level}, the production rate is {new_rate} per minute.")
            return new_rate
        else:
            print(f"Upgrade '{upgrade_part}' not found for {building_name}.")
            return None
    else:
        print(f"Building '{building_name}' not found.")
        return None

starbase_upgrades = load_building_data('buildings')['starbase']['upgrades']

def calculate_production(upgrade_level):
    # The base production rate per minute for level 1
    base_rate = 10
    production_rate = base_rate * upgrade_level
    return production_rate

def background_production():
    global last_production_time
    last_production_time = cache['last_production_time']

    # Get the current time
    current_time = datetime.now()

    # Check if last_production_time is empty (""), and if so, set it to the current time
    if cache['last_production_time'] == "":
        last_production_time = current_time.isoformat()
        cache['last_production_time'] = last_production_time
        print("Last production time was empty. Setting to current time.")

    # Calculate the time difference since the last production update
    last_production_time_obj = datetime.fromisoformat(last_production_time)
    time_diff = current_time - last_production_time_obj

    # Check if 1 minute (or your desired interval) has passed
    if time_diff >= timedelta(minutes=1):
        # Load saved storage values (check if there's any saved material)
        parsteel_storage = cache['parsteel_storage'] or 0
        tritanium_storage = cache['tritanium_storage'] or 0
        dilithium_storage = cache['dilithium_storage'] or 0

        # Load the upgrade levels from the buildings data
        generators_upgrades = load_building_data('buildings')['generators']['upgrades']

        # Calculate the production for each material based on its upgrade level
        parsteel_prod = calculate_production(generators_upgrades['Parsteel Generator'])
        tritanium_prod = calculate_production(generators_upgrades['Tritanium Generator'])
        dilithium_prod = calculate_production(generators_upgrades['Dilithium Generator'])

        # Increment the storage by the respective production rate
        parsteel_storage += parsteel_prod
        tritanium_storage += tritanium_prod
        dilithium_storage += dilithium_prod

        # Save the updated storage values
        cache['parsteel_storage'] = parsteel_storage
        cache['tritanium_storage'] = tritanium_storage
        cache['dilithium_storage'] = dilithium_storage

        # Save the current time as the last production time
        last_production_time = current_time.isoformat()
        cache['last_production_time'] = last_production_time


def claim_resources():
    # Load stored materials and actual materials from user data
    parsteel_storage = cache['parsteel_storage'] or 0
    tritanium_storage = cache['tritanium_storage'] or 0
    dilithium_storage = cache['dilithium_storage'] or 0

    parsteel = cache['parsteel'] or 0
    tritanium = cache['tritanium'] or 0
    dilithium = cache['dilithium'] or 0

    # Add stored materials to the actual resources
    parsteel += parsteel_storage
    tritanium += tritanium_storage
    dilithium += dilithium_storage

    # Save the updated resources back to user data
    cache['parsteel'] = parsteel
    cache['tritanium'] = tritanium
    cache['dilithium'] = dilithium

    # Reset the storage to 0
    cache['parsteel_storage'] = 0
    cache['tritanium_storage'] = 0
    cache['dilithium_storage'] = 0

    print(f"{Fore.GREEN}All resources have been claimed. Parsteel claimed: {parsteel_storage} | Tritanium claimed: {tritanium_storage} | Dilithium claimed: {dilithium_storage}{Fore.WHITE}")
    if cache['tutorial'] == 10:
        print(f"{Fore.GREEN}Great job! Every once and awhile, come back here to claim your materials.{Fore.WHITE}")
        cache['tutorial'] = 11
        time.sleep(2)

def load_research_data(key, research_name=None):
    try:
        with open('research.json', 'r') as file:
            data = json.load(file)

        if research_name:
            if research_name in data['research']:
                return data['research'][research_name]
            print(f"Research topic '{research_name}' not found.")
            return None
        return data.get(key, None)

    except FileNotFoundError:
        print("Research data file not found.")
        return None


def save_research_data(key, value, research_name=None):
    try:
        with open('research.json', 'r+') as file:
            data = json.load(file)

            if research_name:
                if research_name in data['research']:
                    data['research'][research_name][key] = value
                else:
                    print(f"Research topic '{research_name}' not found.")
                    return
            else:
                data[key] = value

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Research data file not found.")

def start_research(research_name, duration):
    user_data = cache['research_queue']

    if user_data['research'] is None:
        current_time = datetime.now()
        end_time = (current_time + timedelta(seconds=duration)).isoformat()

        research_data = {
            'research': research_name,
            'start_time': current_time.isoformat(),
            'end_time': end_time
        }
        cache['research_queue'] = research_data

        print(f"{Fore.YELLOW}Researching {research_name}. Completion expected at {end_time}{Fore.WHITE}")
        time.sleep(2)
    else:
        print(f"{Fore.RED}Research queue is already occupied.{Fore.WHITE}")
        time.sleep(2)

def check_research_completion():
    research_data = cache['research_queue']

    if research_data['research'] is not None:
        end_time = datetime.fromisoformat(research_data['end_time'])
        current_time = datetime.now()

        if current_time >= end_time:
            research_name = research_data['research']
            apply_research(research_name)

            cache['research_queue'] = ('research_queue', {
                'research': None,
                'start_time': None,
                'end_time': None
            })
            print(f"{Fore.GREEN}Research of {research_name} is complete.{Fore.WHITE}")
            time.sleep(2)
        else:
            remaining_time = (end_time - current_time).total_seconds()
            print(f"{Fore.YELLOW}Research in progress. Time remaining: {round(remaining_time)} seconds.{Fore.WHITE}")
    else:
        print(f"{Fore.RED}No research is in progress.{Fore.WHITE}")

def apply_research(research_name):
    research_data = load_research_data('research', research_name)

    if research_data and research_data['level'] >= 0:
        research_data['level'] += 1
        save_research_data('level', research_data['level'], research_name)
        save_research_data('cost', round((research_data['cost'] ** 1.5)), research_name)
        print(f"{research_name} level increased to {research_data['level']}.")

def display_available_research():
    research_data = load_research_data('research')
    available_research = []
    unavailable_research = []

    # Categorize research based on prerequisites
    for name, details in research_data.items():
        if prerequisites_met(name):
            available_research.append((name, details))
        else:
            # Collect missing prerequisites
            missing_prereqs = [
                prereq for prereq in details.get('prerequisites', [])
                if load_research_data('research', prereq)['level'] < 1
            ]
            unavailable_research.append((name, details, missing_prereqs))
    if cache['tutorial'] == 4:
        print(f"{Fore.YELLOW}Now select 1 and start the research, because you have this one ready. As you go through research, more will become avalible as you progress through the research tree.{Fore.WHITE}")
    # Display available research
    print("\nAvailable Research:")
    for index, (name, details) in enumerate(available_research, start=1):
        print(f"{index}. {name} - Cost: {details['cost']} dilithium")

    # Display unavailable research with unmet prerequisites
    print("\nUnavailable Research (Prerequisites Required):")
    for index, (name, details, missing_prereqs) in enumerate(unavailable_research, start=len(available_research) + 1):
        print(f"{index}. {name} - Missing prerequisites: {', '.join(missing_prereqs)}")

    print(f"{len(available_research) + len(unavailable_research) + 1}. Exit")

    # Get user selection
    choice = int(input("\nEnter the number of the research you wish to start, or choose the Exit option: ")) - 1

    # Check if the user chose to exit
    if choice == len(available_research) + len(unavailable_research):
        print("Exiting research menu.")
        return

    # Determine if choice is available
    if choice < len(available_research) and ask(f"{Fore.YELLOW}Are you sure you want to research this? This costs {available_research[choice][1]['cost']} dilithium. ({cache['dilithium']} -> {cache['dilithium'] - available_research[choice][1]['cost']}) (Y/N): {Fore.WHITE}"):
        selected_research = available_research[choice][0]
        cost = available_research[choice][1]['cost']

        # Check if the player has enough dilithium
        if cache['dilithium'] >= cost:
            cache['dilithium'] -= cost
            start_research(selected_research, duration=round((cost ** 1.5)))
            print(f"{Fore.GREEN}Research on {selected_research} has started.{Fore.WHITE}")
            print(f"Remaining Dilithium: {cache['dilithium']}")
            if cache['tutorial'] == 4:
                print(f"{Fore.GREEN}Great work! Research will improve your stats on what you are researching. Look at the Wiki to see what each part of the research tree affects.{Fore.WHITE}")
                cache['tutorial'] = 5
            time.sleep(2)
        else:
            print(f"{Fore.RED}Not enough dilithium to start this research.{Fore.WHITE}")
            time.sleep(2)
    else:
        print(f"{Fore.RED}Selected research is unavailable or prerequisites have not been met.{Fore.WHITE}")
        time.sleep(2)


# Function to check prerequisites
def prerequisites_met(research_name):
    research_data = load_research_data('research', research_name)

    if research_data:
        prerequisites = research_data.get('prerequisites', [])
        for prereq in prerequisites:
            prereq_data = load_research_data('research', prereq)
            if prereq_data['level'] < 1:
                return False
        return True
    return False

# Define the mapping of research names to JSON stat keys
research_to_stat_key = {
    "Warp Mathematics": "warp_range",
    "Mining Laser": "mining_efficiency",
    "Inventory Management Systems": "max_storage",
    "Sheild Dynamics": "max_health",
    "Phaser Calibration": "firepower",
    "Targeting Matrix": "accuracy",
    "Evasive Maneuvers": "evasion",
}

def research_multi(research_name):
    # Map the research name to the corresponding JSON key
    stat_key = research_to_stat_key.get(research_name)

    # Ensure the research name has a mapped stat key
    if not stat_key:
        print(f"No stat key found for research '{research_name}'.")
        return None

    # Load research data and base value from JSON
    research_data = load_research_data('research')
    base_value = load_ship_stat(cache['ship'], stat_key)

    # Check if the research exists in the data and retrieve the level
    if research_name in research_data:
        research_level = research_data[research_name]['level']

        # If the research level is 0, set total_multiplier to 1
        if research_level == 0:
            total_multiplier = 1
        else:
            total_multiplier = research_level

        return round(total_multiplier)

    else:
        print(f"No research found for '{research_name}'. Returning base value.")
        return round(base_value)

def calculate_repair_cost(base_repair_cost):
    # Load the current shipyard level
    shipyard_level = load_specific_upgrade("starbase", "Shipyard")

    if shipyard_level is None or shipyard_level == 0:
        print("Invalid shipyard level. Defaulting repair cost to base amount.")
        return base_repair_cost

    # Calculate adjusted repair cost
    adjusted_repair_cost = base_repair_cost // shipyard_level

    return adjusted_repair_cost


def colored_gradient_loading_bar(total=30, duration=5):
    # ANSI escape sequences for colors
    RESET = "\033[0m"

    end_time = time.time() + duration

    while time.time() < end_time:
        for i in range(total + 1):
            # Calculate the percentage of completion
            percent = (i / total)

            # Calculate RGB values for the gradient
            red = int(255 * (1 - percent))
            green = int(255 * percent)
            # RGB color
            color_code = f"\033[38;2;{red};{green};0m"

            # Create the loading bar
            hashes = color_code + '#' * i + RESET
            spaces = ' ' * (total - i)

            loading_bar = f"[{hashes}{spaces}] {percent * 100:.2f}%"
            # Overwrite the current line
            sys.stdout.write('\r' + loading_bar)
            # Force the output to be printed
            sys.stdout.flush()
            # Control the speed of the loading bar
            time.sleep(duration / total)

    # Print completion message
    sys.stdout.write('\nDone!          \n')

def typing_animation(text, delay=0.06):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    
def typing_animation_fast(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

def distress_call_scenario():
    print(f"{Fore.YELLOW}You have arrived at the coordinates for the distress call.{Fore.WHITE}")
    typing_animation(f"Transmission: {Fore.RED}██████████ ████ e∩c🜔🜃u∩t€r3d an ███☥wn sh!p! ᚼᔪ ███ h#&@ve a ███ br€@ch! ⬞ P!€@s€! @ny☇ne! H3lp ███! ⚠️✧ %&*†₧@! ███████ █████ ⊗☒☭∩ ⨀⇌⍸❝₳𝓧𒅗✸† █████████{Fore.WHITE}")
    typing_animation('Ship Computer: "The transmission is garbled. Attempting to parse..."')
    time.sleep(2)
    typing_animation(f"Parsing Terminal: ██████████ e∩c🜔🜃u∩t€r3d an unknown/(unkn☥wn) ship!\n{Fore.BLUE}Status: {Fore.RED}[DATA CORRUPTED]{Fore.WHITE}\n{Fore.GREEN}Words Detected:{Fore.WHITE} - hull breach! - (Please) - (anyone) - Help us!\n{Fore.YELLOW}Warning: ⚠️ Additional Data: %&*†₧@! ██████████{Fore.WHITE}{Fore.WHITE}")

    first_iteration = True
    while True:
        if not first_iteration:
            clear()
            income_display()
        distress_option = ask_sanitize("1. Scan the area for hostiles\n2. Get into transporter range of the ship\nOption: ")
        if distress_option == 1:
            print("Scanning...")
            colored_gradient_loading_bar(duration=5)
            typing_animation(f"{Fore.GREEN}Scans found no other ships in the area other than the current ship you are helping.{Fore.WHITE}")
            time.sleep(2)
            first_iteration = False
        elif distress_option == 2:
            print("Moving closer to the ship...")
            colored_gradient_loading_bar(duration=4)
            print(f"{Fore.GREEN}Within transporter range. Beaming the crew on board...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=7)
            print(f"{Fore.GREEN}All crew has been beamed on board. They give you valuable insight as to where the unknown ship has gone, and thank you for your rescue.\n{Fore.YELLOW}They give you 15 latinum!{Fore.WHITE}")
            save_ship_data(cache['ship'], 'latinum_storage', load_ship_stat(cache['ship'], 'latinum_storage') + 15)
            save_ship_data(cache['ship'], 'storage', load_ship_stat(cache['ship'], 'storage') - 15)
            print(f"{Fore.BLUE}Continue the mission by traveling to the Solaria system. (Requires a warp range of 7){Fore.WHITE}")
            update_mission_progress('Respond to the Distress Signal in Regula', 1)
            print('Exiting in 5 seconds...')
            time.sleep(5)
            return

def center_text(text):
    # Get the width of the terminal
    terminal_width = os.get_terminal_size().columns

    # Calculate the padding needed to center the text
    text_length = len(text)
    padding = (terminal_width - text_length) // 2

    # Create the centered text with padding
    centered_text = ' ' * padding + text

    # Print the centered text
    print(centered_text)

def mission_briefing():
    if cache['missions']['Respond to the Distress Signal in Regula']['accepted'] and not cache['missions']['Respond to the Distress Signal in Regula']['completed'] and cache['missions']['Respond to the Distress Signal in Regula']['progress'] == 0:
        center_text(f"{Fore.BLUE}<========== Starfleet Mission Briefing ==========>{Fore.WHITE}")
        center_text(f"{Fore.RED}A distress call has been received from the system Regula. (Warp range needs to be at least 6).{Fore.WHITE}")
        time.sleep(2)
        typing_animation("You must travel to the system Regula, explore the system, and you will find an option that says 'Respond to Distress call in Regula.' You will select that option, and complete that part of the mission. It may take you to other systems as you go.")
        print()
        time.sleep(2)
        center_text("Good luck Captain.")
        time.sleep(5)
        center_text(f"{Fore.BLUE}<========== Starfleet Mission Briefing - END TRANSMISSION ==========>{Fore.WHITE}")
        input("Press enter to exit.")
        update_mission_progress('Respond to the Distress Signal in Regula', 1)
        clear()
    elif cache['missions']['Survey the Rings of Tarkalea XII']['accepted'] and not cache['missions']['Survey the Rings of Tarkalea XII']['completed'] and cache['missions']['Survey the Rings of Tarkalea XII']['progress'] == 0:
        center_text(f"{Fore.BLUE}<========== UFP Galactic Survey ==========>")
        center_text("The UFPGS is calling independents to survey the rings of Tarkalea XII.")
        time.sleep(2)
        center_text("You must travel to Tarkalea XII and start the survey of the rings. Once you have completed that, you may return to drydock with your findings.")
        time.sleep(3)
        center_text("<========== End Transmission ==========>")
        input("Press enter to exit.")
        update_mission_progress('Survey the Rings of Tarkalea XII', 1)
        clear()
    elif cache['missions']['Scan for Anomalies']['accepted'] and not cache['missions']['Scan for Anomalies']['completed'] and cache['missions']['Scan for Anomalies']['progress'] == 0:
        center_text(f"{Fore.BLUE}<========== Starfleet Mission Briefing ==========>")
        print("")
        center_text(f"{Fore.BLUE}Starfleet Command has tasked your crew with scanning and analyzing unexplored anomalies in nearby sectors.{Fore.GREEN}\nThese phenomena hold the potential to uncover scientific breakthroughs and enhance our understanding of the galaxy.{Fore.YELLOW}\nEquip your sensors, navigate with precision, and report all findings back to Starfleet for further study.{Fore.RED}\nProceed with caution, as anomalies may pose unexpected challenges.{Fore.WHITE}")
        print("")
        time.sleep(3)
        center_text("Travel to Omicron II for this mission.")
        print("")
        time.sleep(2)
        center_text(f"{Fore.BLUE}<========== End Transmission ==========>{Fore.WHITE}")
        time.sleep(2)
        input("Press enter to exit.")
        update_mission_progress('Scan for Anomalies', 1)
        clear()
    elif cache['missions']['Recover Lost Data']['accepted'] and not cache['missions']['Recover Lost Data']['completed'] and cache['missions']['Recover Lost Data']['progress'] == 0:
        center_text(f"{Fore.BLUE}<========== Incoming Transmission ==========>{Fore.WHITE}")
        center_text(f"{Fore.RED}Source: Vulcan Science Academy{Fore.WHITE}")
        time.sleep(2)
        center_text(f"{Fore.YELLOW}We have lost contact with a research vessel in the system of Vulcan. We need you to travel to the system and recover the lost data from the ship.{Fore.WHITE}")
        time.sleep(2)
        center_text(f"{Fore.GREEN}The data is vital to the Vulcan Science Academy, and we need it back as soon as possible.{Fore.WHITE}")
        time.sleep(2)
        center_text(f"{Fore.BLUE}Travel to Vulcan to begin the mission.{Fore.WHITE}")
        time.sleep(2)
        center_text(f"{Fore.BLUE}<========== End Transmission ==========>{Fore.WHITE}")
        time.sleep(2)
        input("Press enter to exit.")
        update_mission_progress('Recover Lost Data', 1)
        clear()
    elif cache['missions']['The Starship Graveyard']['accepted'] and not cache['missions']['The Starship Graveyard']['completed'] and cache['missions']['The Starship Graveyard']['progress'] == 0:
        center_text(f"{Fore.BLUE}<========== Starfleet Mission Briefing ==========>")
        print("")
        center_text(f"{Fore.BLUE}Starfleet Command has tasked your crew with exploring the Mutara Nebula in the Solaria system.{Fore.GREEN}\nThe long-forgotten Talarian Conflict took place here, and scans have shown there are still components of starships in the nebula.{Fore.YELLOW}\nYou must retrieve vital pieces of the destroyed starships, and bring them back to Sol for Federation inspection.{Fore.RED}\nTo retrieve these pieces you must preform EVAs, as transporters are non-functional within the nebula.{Fore.WHITE}")
        print("")
        time.sleep(3)
        center_text("Travel to Solaria for this mission.")
        print("")
        time.sleep(2)
        center_text(f"{Fore.BLUE}<========== End Transmission ==========>{Fore.WHITE}")
        time.sleep(2)
        input("Press enter to exit.")
        update_mission_progress('The Starship Graveyard', 1)
        clear()
    elif cache['missions']['First Contact']['accepted'] and not cache['missions']['First Contact']['completed'] and cache['missions']['First Contact']['progress'] == 0:
        center_text(f"{Fore.BLUE}<========== Starfleet Mission Briefing ==========>{Fore.WHITE}")
        time.sleep(2)
        center_text(f"{Fore.BLUE}Starfleet has found possible evidence for an emerging warp-capable technology civilization.{Fore.GREEN}\nStarfleet thinks initiating First Contact procedures with the civlization.{Fore.YELLOW}\nWe want you to be a liaison to represent the UFP.{Fore.WHITE}")
        time.sleep(3)
        center_text(f"{Fore.RED}If anything goes wrong, contact Starfleet immidatley. DO NOT USE WEAPONS UNLESS YOU AND YOUR CREW ARE IN JEOPARDY.{Fore.WHITE}")
        time.sleep(2)
        center_text("Travel to Altor IV for this mission")
        print("")
        time.sleep(2)
        center_text(f"{Fore.BLUE}<========== End Transmission ==========>{Fore.WHITE}")
        input("Press enter to exit.")
        update_mission_progress('First Contact', 1)
        clear()
        

def distress_call_scenario_pt2():
    print("You have arrived at the coordinates of the unknown ship.")
    time.sleep(1)
    print("Scanning the area...")
    colored_gradient_loading_bar(duration=5)
    print(f"{Fore.RED}Scans have located 2 ships!{Fore.WHITE}")
    print(f"{Fore.YELLOW}YELLOW ALERT{Fore.WHITE}")
    time.sleep(2)
    print("Scans have show the ships shields are up, and weapons are armed.")
    if ask("Attack the ships? Health: 2000, Firepower: 5, Accuracy 6, Evasion 5 (Y/N): "):
        battle_stat(2000, 'Unknown Ship', random.randint(300, 500), 6, 5, 5)
        if load_ship_stat(cache['ship'], 'health') <= 0:
            return
        print(f"{Fore.GREEN}You have defeated one of the enemy ships!{Fore.WHITE}")
        time.sleep(2)
        print(f"{Fore.GREEN}The second ship is fleeing!\nVictory!{Fore.WHITE}")
        update_mission_progress('Respond to Distress Signal in Regula', 1)
        time.sleep(2)
    else:
        print(f"{Fore.RED}The ships have fired on you!{Fore.WHITE}")
        save_ship_data(cache['ship'], 'health', load_ship_stat(cache['ship'], 'health') - random.randint(100, 350))
        print("Prepare for battle!")
        time.sleep(4)
        battle_stat(2000, 'Unknown Ship', random.randint(300, 500), 6, 5, 5)
        if load_ship_stat(cache['ship'], 'health') <= 0:
            return
        print(f"{Fore.GREEN}You have defeated one of the enemy ships!{Fore.WHITE}")
        time.sleep(2)
        print(f"{Fore.GREEN}The second ship is fleeing!\nVictory!{Fore.WHITE}")
        update_mission_progress('Respond to Distress Signal in Regula', 1)
        time.sleep(2)

def dilithium_convoypt1():
    mission_stage = cache['missions']['Protect Dilithium Convoy']['progress']
    if cache['missions']['Protect Dilithium Convoy']['completed'] == False and cache['missions']['Protect Dilithium Convoy']['accepted'] == True:
        if mission_stage == 0:
            center_text(f"{Fore.BLUE}<=============== Incoming Transmission ===============>")
            time.sleep(2)
            center_text(f"Starfleet Command\n{Fore.WHITE}")
            time.sleep(1)
            center_text(f"{Fore.YELLOW}You have accepted Starfleet Command's assignment to protect their dilithium convoy.\n{Fore.WHITE}")
            time.sleep(2)
            center_text(f"{Fore.GREEN}Make sure your ship is battle ready in case pirates attack the freighters. Then, travel to {Fore.YELLOW}Andor{Fore.GREEN} and accompany the convoy through Andor to ---.\nYou will pass though an Astroid Felid on the way there.\nYou will be rewarded 75 latinum for your efforts.\nGood Luck capitan.{Fore.WHITE}")
            time.sleep(5)
            input("Press enter to continue... ")
            update_mission_progress('Protect Dilithium Convoy', 1)
            clear()

def tarkalea_survey():
    clear()
    income_display()
    if ask("Would you like to begin the survey? (y/n): "):
        colored_gradient_loading_bar(duration=random.randint(10,25))
        print(f"{Fore.GREEN}Survey complete! Return to your station with your findings.{Fore.WHITE}")
        update_mission_progress('Survey the Rings of Tarkalea XII', 1)
        time.sleep(2)
    else:
        print(f"{Fore.RED}Survey canceled. When you a ready, come back and take the survey.{Fore.WHITE}")
        time.sleep(2)

# Xindi station will be part of v1 Galaxy Unleashed.
def xindi_station():
    clear()
    income_display()
    first_itteration = True
    while True:
        if first_itteration == True:
            center_text(f"{Fore.BLUE}<=============== Welcome to Xindi Starbase 9! ===============>{Fore.WHITE}")
            first_itteration = False
            time.sleep(2)
        else:
            center_text(f"{Fore.BLUE}<=============== Xindi Starbase 9 ===============>{Fore.WHITE}")
        xindi_option = ask_sanitize("1. Trade\n2. Get briefed on Xindi Missions\n3. Participate in Training Drills\n4. Apply for Xindi Mission Board\n5. Search for classified Xindi knowledge\n6. Get info on all of these topics\n7. Undock and Exit\nOption: ")
        if xindi_option == 6:
            clear()
            income_display()
            typing_animation("Accessing LCARS...")
            time.sleep(2)
            typing_animation("All information will be displayed in 5 seconds.")
            time.sleep(5)
            clear()
            time.sleep(0.5)
            print(f"{Fore.BLUE}TRADE INFO{Fore.WHITE}\nTrade materials such as parsteel, tritanium, dilithium, and latinum for one another.\n{Fore.BLUE}XINDI MISSIONS{Fore.WHITE}\nTake part in missions with the Xindi, and help your relations with them as you help.")

tutorial_highlight11 = False
tutorial_highlight2 = False
tutorial_highlight1 = False
tutorial_highlight4 = False
tutorial_highlight6 = False

def tutorial():
    global tutorial_highlight1, tutorial_highlight2, tutorial_highlight4, tutorial_highlight6, tutorial_highlight11

    # Define tutorial steps
    tutorial_steps = {
        0: {
            "message": (
                f"{Fore.BLUE}Welcome to STF: Captain's Chair. You are an independent commander. Your job is to build up your ships, expand your fleet, "
                f"and become one of the strongest independent commanders the universe has ever seen, with even the factions fearing you. Explore new worlds "
                f"and collect valuable materials!{Fore.WHITE}\n\n"
                "Welcome to your new command on board the starship Stargazer. The ship computer will help you get oriented with your ship, and your station.\n\n"
                f"{Fore.YELLOW}This below is what the menu looks like. Start by pressing 1 to explore Sol.\n\n{Fore.WHITE}"
            ),
            "highlights": {"tutorial_highlight2": Fore.YELLOW},
            "sleep": 8,
        },
        1: {
            "message": f"{Fore.YELLOW}Now that you know how to mine, return to drydock by pressing 3 and enter.\n{Fore.WHITE}",
            "highlights": {"tutorial_highlight1": Fore.YELLOW},
        },
        2: {
            "message": (
                f"{Fore.YELLOW}Now that you have upgraded your generators and know the basics of upgrading, it's time to battle.\n"
                f"Press 1 to explore Sol.{Fore.WHITE}"
            ),
            "highlights": {"tutorial_highlight2": Fore.YELLOW, "tutorial_highlight4": Fore.YELLOW},
        },
        # Add more steps here in similar format...
        12: {
            "message": (
                f"{Fore.WHITE}Great job! You have finished the tutorial.\n"
                f"{Fore.BLUE}There are many more functions than just these, so feel free to explore them all! You can upgrade all buildings, start research to boost stats, "
                f"and buy more crew.\n{Fore.YELLOW}Also, if you approach a ship, type 2 to hail it, and if it's friendly, you can trade with it.\n"
                f"{Fore.GREEN}Once again, great job with the tutorial, Commander! If you have any questions, ideas, or bugs, please report an issue on GitHub. "
                f"Check the wiki for more info on the whole game.{Fore.WHITE}\n\n"
                f"{Fore.GREEN}This counts as your first mission, so here are some rewards!{Fore.WHITE}\n"
                f"{Fore.GREEN}Parsteel Reward: 300 | Tritanium Reward: 200 | Dilithium Reward: 100 | All types of BP's: 25 | Recruit Tokens: 50 | Latinum: 50{Fore.WHITE}"
            ),
            "highlights": {},
            "rewards": {
                "parsteel": 300,
                "tritanium": 200,
                "dilithium": 100,
                "stargazer_blueprints": 25,
                "uss_grissom_blueprints": 25,
                "federation_shuttlecraft_blueprints": 25,
                "galaxy_class_blueprints": 50,
                "realta_blueprints": 25,
                "daedalus_class_medical_blueprints": 30,
                "ambassadors_shuttle_blueprints": 40,
                "uss_constitution_blueprints": 60,
                "ferengi_dkora_blueprints": 60,
                "klingon_kvort_blueprints": 60,
                "romulan_warbird_blueprints": 70,
                "uss_excelsior_blueprints": 70,
                "uss_enterprise_(ncc-1701_d)_blueprints": 80,
                "recruit_tokens": 50,
                "latinum": 50,
            },
            "end_tutorial": True,
        },
    }

    tutorial_step = load_data("tutorial")
    step_data = tutorial_steps.get(tutorial_step)

    if step_data:
        # Display message
        print(step_data["message"])
        time.sleep(step_data.get("sleep", 2))

        # Set highlight colors
        global_vars = globals()
        for var in ["tutorial_highlight1", "tutorial_highlight2", "tutorial_highlight4", "tutorial_highlight6", "tutorial_highlight11"]:
            global_vars[var] = step_data["highlights"].get(var, Fore.WHITE)

        # Handle rewards and tutorial completion
        if "rewards" in step_data:
            for key, value in step_data["rewards"].items():
                cache[key] = value
            input("Press Enter to finish the tutorial.")
            cache['tutorial'] = 50
            clear()

        if step_data.get("end_tutorial"):
            print(f"{Fore.GREEN}Tutorial complete!{Fore.WHITE}")
    else:
        # Reset highlights if no step matches
        tutorial_highlight1 = tutorial_highlight2 = tutorial_highlight4 = tutorial_highlight6 = tutorial_highlight11 = Fore.WHITE


def upgrade_generator(generator_type):
    # Calculate the upgrade time and cost for the specific generator
    upgrade_time = load_specific_upgrade('generators', generator_type) * generator_upgrade_delta * 10
    upgrade_cost = round(load_specific_upgrade('generators', generator_type) * (generator_upgrade_delta + 5) * (generator_upgrade_delta * (generator_upgrade_delta * 10)))

    # Ask the player if they are sure about the upgrade
    if ask(f"{Fore.YELLOW}Are you sure you want to upgrade? This will take {upgrade_time} seconds and cost {upgrade_cost} parsteel. (Y/N): {Fore.WHITE}") and cache['parsteel'] >= upgrade_cost:
        # Deduct the parsteel cost and start the construction
        cache['parsteel'] -= upgrade_cost
        start_construction('generators', upgrade_time, generator_type)
        # Tutorial message
        if cache['tutorial'] == 1:
            print(f"{Fore.BLUE}Great work! You have started construction of the {generator_type.lower()}. This timer will run in the background, and when you come back to the menu and the timer is out, the upgrades will apply.\nNow you know how to upgrade buildings!{Fore.WHITE}")
            cache['tutorial'] = 2
            time.sleep(8)
    else:
        print(f"{Fore.RED}You have either canceled the upgrade, or do not have enough parsteel.{Fore.WHITE}")
        time.sleep(2)


tutorial_highlight3 = False
tutorial_highlight5 = False
tutorial_highlight7 = False
tutorial_highlight9 = False

def process_tutorial_step():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9

    # Define tutorial steps
    tutorial_steps = {
        1: {
            "message": (
                f"{Fore.YELLOW}When you return to drydock, all of the storage in your ship returns to normal, "
                f"and the storage goes into your actual currency.{Fore.WHITE}\n\n"
                "Now that you have some materials, press 1 to enter the station.\n"
            ),
            "highlights": {"tutorial_highlight3": Fore.YELLOW},
        },
        3: {
            "message": f"{Fore.YELLOW}Your ship is damaged from battle. Type 4 to repair your ship.\n{Fore.WHITE}",
            "highlights": {"tutorial_highlight5": Fore.YELLOW},
        },
        4: {
            "message": f"{Fore.YELLOW}Type 3 to open research.\n{Fore.WHITE}",
            "highlights": {},
        },
        7: {
            "message": f"{Fore.YELLOW}Now, it's time to upgrade your ship. Enter the shipyard.\n{Fore.WHITE}",
            "highlights": {"tutorial_highlight7": Fore.YELLOW},
        },
        9: {
            "message": None,
            "highlights": {"tutorial_highlight9": Fore.YELLOW, "tutorial_highlight3": Fore.YELLOW},
        },
        10: {
            "message": None,
            "highlights": {"tutorial_highlight3": Fore.YELLOW},
        },
    }

    # Default highlight values
    default_highlights = {
        "tutorial_highlight3": Fore.WHITE,
        "tutorial_highlight5": Fore.WHITE,
        "tutorial_highlight7": Fore.WHITE,
        "tutorial_highlight9": Fore.WHITE,
    }

    # Get the current tutorial step
    tutorial_step = load_data("tutorial")
    step_data = tutorial_steps.get(tutorial_step, {"highlights": {}})

    # Print the message if it exists
    if "message" in step_data and step_data["message"]:
        print(step_data["message"])
        time.sleep(2)

    # Update highlight colors
    global_vars = globals()
    for var, color in {**default_highlights, **step_data.get("highlights", {})}.items():
        global_vars[var] = color

def transfer_resources_to_storage():
    """
    Transfers resources from the ship's storage to the main storage,
    resets the ship's resource storage to 0, and updates the ship's maximum storage capacity.
    """
    # Load ship name once
    ship_name = cache['ship']

    # List of resources to transfer
    resources = ['parsteel', 'tritanium', 'dilithium', 'latinum']

    # Transfer resources
    for resource in resources:
        ship_storage_key = f'{resource}_storage'
        current_storage = load_data(resource)
        ship_storage = load_ship_stat(ship_name=ship_name, stat_key=ship_storage_key)

        # Special handling for latinum
        if resource == 'latinum':
            ship_storage = round(ship_storage / 2)

        # Update main storage and reset ship's storage
        cache[resource] = current_storage + ship_storage
        save_ship_data(ship_name=ship_name, stat_key=ship_storage_key, value=0)

    # Update overall ship storage capacity
    max_storage = load_ship_stat(ship_name=ship_name, stat_key='max_storage')
    new_storage = research_multi('Inventory Management Systems') * max_storage
    save_ship_data(ship_name=ship_name, stat_key='storage', value=new_storage)

import time
import sys

def travel_bar(start_label="Start", end_label="End", travel_time=10, bar_length=30):
    """
    Displays a travel progress bar in the console.
    
    Args:
        start_label (str): Label for the starting position.
        end_label (str): Label for the ending position.
        travel_time (int): Total travel time in seconds.
        bar_length (int): The length of the progress bar in characters.
    """
    for i in range(bar_length + 1):
        # Calculate current progress
        progress = (i / bar_length) * travel_time
        
        if cache['missions']['Protect Dilithium Convoy']['progress'] == 1:
            if progress == 4:
                break
        
        # Render the progress bar
        bar = f"{start_label} ("
        bar += "-" * i + "0" + "-" * (bar_length - i)
        bar += f") {end_label}"
        
        # Display the bar and progress
        sys.stdout.write(f"\r{bar} {progress:.1f}s elapsed")
        sys.stdout.flush()
        
        # Wait before updating
        time.sleep(travel_time / bar_length)
    
    # End the progress display with a newline
    print()

# Systems functions

def sol():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Ensure the current system is Sol
    if current_system != 1:
        return

    current_system_explored = load_explored(systems[current_system])
    tutorial_state = cache['tutorial']

    # Update tutorial highlights based on the tutorial state
    tutorial_highlight = Fore.YELLOW if tutorial_state == 0 else Fore.WHITE
    tutorial_highlight4 = Fore.YELLOW if tutorial_state == 2 else Fore.WHITE

    # Display tutorial guidance if applicable
    if tutorial_state == 0:
        print(f"{tutorial_highlight}This is what the menu will look like. Navigate to a parsteel mine by typing 1 and pressing enter.{Fore.WHITE}")
    elif tutorial_state == 2:
        print(f"{Fore.YELLOW}Navigate to the enemy ship by typing 3.{Fore.WHITE}")

    # Define menu options
    system_findings = {
        1: (f'{tutorial_highlight}Parsteel Mine{Fore.WHITE}', lambda: handle_mining('parsteel', ['parsteel_mine1', 'parsteel_mine2', 'parsteel_mine3', 'parsteel_mine4', 'parsteel_mine5'], 'Parsteel')),
        2: ('Mission Planet', handle_mission_planet),
        3: (f'{tutorial_highlight4}Orion Pirate{Fore.WHITE}', lambda: handle_orion_pirate(tutorial_state))
    }
    
    if cache['missions']['The Starship Graveyard']['accepted'] == True and cache['missions']['The Starship Graveyard']['progress'] == 2:
        system_findings[4] = (f'{Fore.YELLOW}Give Components to Starfleet Command{Fore.WHITE}', starship_graveyard)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()
    elif current_system_explored == 2:
        # If unexplored, scan the system
        income_display()
        scan_system()


# Helper Functions
def handle_mining(resource, mining_locations, resource_name):
    """Handles mining operations."""
    if load_ship_stat(ship_name=cache['ship'], stat_key='storage') > 0:
        clear()
        mining_deposit(resource, random.choice(mining_locations), resource_name)
    else:
        clear()
        income_display()
        print(f'{Fore.RED}You do not have enough storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')


def handle_mission_planet():
    """Handles the Mission Planet interaction."""
    clear()
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()


def handle_orion_pirate(tutorial_state):
    """Handles the Orion Pirate encounter."""
    tut_health = 700 if tutorial_state == 2 else random.randint(500, 900)
    clear()
    income_display()
    print('You have approached an Orion Pirate!')
    print('What do you want to do?')
    op_1 = [f'{Fore.YELLOW if tutorial_state == 2 else Fore.WHITE}1: Attack the Ship{Fore.WHITE}', '2: Hail the Ship']
    print(*op_1, sep='\n')

    ori_ship = ask_sanitize('What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=tut_health, opponent_name='Orion Pirate',
            firepower=1, accuracy=1, evasion=1,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()

def vulcan():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Ensure the current system is Vulcan
    if current_system != 2:
        return

    current_system_explored = load_explored(systems[current_system])
    tutorial_state = cache['tutorial']

    # Update tutorial highlight if needed
    tutorial_highlight6 = Fore.YELLOW if tutorial_state == 6 else Fore.WHITE

    # Define menu options
    system_findings = {
        1: ('Parsteel Mine', lambda: handle_mining('parsteel', ['parsteel_mine1', 'parsteel_mine2', 'parsteel_mine3'], 'Parsteel')),
        2: ('Mission Planet', handle_mission_planet),
        3: ('Vulcan Dissident', handle_vulcan_dissident),
        4: (f'{tutorial_highlight6}Tritanium Mine{Fore.WHITE}', lambda: handle_mining('tritanium', ['tritanium_mine1', 'tritanium_mine2', 'tritanium_mine3'], 'Tritanium'))
    }
    
    if cache['missions']['Recover Lost Data']['accepted'] == True and cache['missions']['Recover Lost Data']['progress'] in [1, 2]:
        system_findings[5] = (f'{Fore.YELLOW}Recover Lost Data{Fore.WHITE}', recover_lost_data)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()
    elif current_system_explored == 2:
        # If unexplored, scan system
        income_display()
        scan_system()


# Helper Functions
def handle_mining(resource, mining_locations, resource_name):
    """Handles mining operations."""
    if load_ship_stat(ship_name=cache['ship'], stat_key='storage') > 0:
        clear()
        mining_deposit(resource, random.choice(mining_locations), resource_name)
    else:
        clear()
        income_display()
        print(f'{Fore.RED}You do not have enough storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')


def handle_mission_planet():
    """Handles the Mission Planet interaction."""
    clear()
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()


def handle_vulcan_dissident():
    """Handles the Vulcan Dissident encounter."""
    clear()
    income_display()
    print('You have approached a Vulcan Dissident!')
    print('What do you want to do?')
    op_1 = ['1: Attack the Ship', '2: Hail the Ship']
    print(*op_1, sep='\n')

    ori_ship = ask_sanitize('What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(600, 1000),
            opponent_name='Vulcan Dissident',
            firepower=1, accuracy=2, evasion=1,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()

def recover_lost_data():
    while True:
        clear()
        income_display()
        if cache['missions']['Recover Lost Data']['progress'] == 1:
            print(f"{Fore.GREEN}You have arrived at the coordinates of the lost data.")
            time.sleep(2)
            print(f"{Fore.GREEN}Scanning the area...")
            colored_gradient_loading_bar(duration=6)
            print(f"{Fore.RED}Scans have located the data core of the ship.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}Transporting data core on board...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=5)
            print(f"{Fore.GREEN}Transport Complete!{Fore.WHITE}")
            time.sleep(2)
            update_mission_progress('Recover Lost Data', 1)
        if cache['missions']['Recover Lost Data']['progress'] == 2:
            print(f"{Fore.RED}Sensors are picking up an enemy ship!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.RED}The ship has fired on you!{Fore.WHITE}")
            save_ship_data(cache['ship'], 'health', load_ship_stat(cache['ship'], 'health') - random.randint(50, 200))
            print("Prepare for battle!")
            time.sleep(2)
            battle_stat(2000, 'Unknown Ship', random.randint(300, 500), 6, 5, 5)
            if load_ship_stat(cache['ship'], 'health') <= 0:
                return
            print(f"{Fore.GREEN}You have defeated the enemy ship!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.BLUE}Return to drydock to decode the data core.{Fore.WHITE}")
            update_mission_progress('Recover Lost Data', 1)
            break
        if cache['missions']['Recover Lost Data']['progress'] == 3 and cache['current_system'] == 1:
            if ask("Would you like to decode the data core? (y/n): "):
                print(f"{Fore.GREEN}Decoding data core...{Fore.WHITE}")
                colored_gradient_loading_bar(duration=10)
                print(f"{Fore.GREEN}Data core successfully decoded.{Fore.WHITE}")
                time.sleep(2)
                print(f"{Fore.BLUE}Return to Vulcan to give the data to the Vulcan Science Academy.{Fore.WHITE}")
                time.sleep(2)
                update_mission_progress('Recover Lost Data', 1)
                break
            else:
                print(f"{Fore.RED}Data core decoding canceled. You may decode at any time.{Fore.WHITE}")
                time.sleep(2)
                break
        if cache['missions']['Recover Lost Data']['progress'] == 4 and cache['current_system'] == 2:
            print(f"{Fore.GREEN}You have arrived at Vulcan with the data core.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}Delivering data core to Vulcan Science Academy...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=5)
            print(f"{Fore.GREEN}Data core delivered!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}The Vulcan Science Academy thanks you for your help.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}You have been rewarded 100 latinum for your efforts.{Fore.WHITE}")
            time.sleep(2)
            update_mission_progress('Recover Lost Data', 1)
            break
            
        

def tellar():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if the system is not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Define menu options
    system_findings = {
        1: ('Dilithium Mine', lambda: handle_mining('dilithium', ['dilithium_mine1', 'dilithium_mine2', 'dilithium_mine3', 'dilithium_mine4'], 'Dilithium')),
        2: ('Mission Planet', handle_mission_planet),
        3: ('Nausicaan Raider', handle_nausicaan_raider),
        4: ('Tritanium Mine', lambda: handle_mining('tritanium', ['tritanium_mine1', 'tritanium_mine2'], 'Tritanium'))
    }

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_mission_planet():
    """Handles the Mission Planet interaction."""
    clear()
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()


def handle_nausicaan_raider():
    """Handles the Nausicaan Raider encounter."""
    clear()
    income_display()
    print('You have approached a Nausicaan Raider!')
    print('What do you want to do?')
    op_1 = ['1: Attack the Ship', '2: Hail the Ship']
    print(*op_1, sep='\n')

    ori_ship = ask_sanitize('What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(700, 1100),
            opponent_name='Nausicaan Raider',
            firepower=2, accuracy=2, evasion=3,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()


def handle_mining(resource, mining_locations, resource_name):
    """Handles mining operations."""
    if load_ship_stat(ship_name=cache['ship'], stat_key='storage') > 0:
        clear()
        mining_deposit(resource, random.choice(mining_locations), resource_name)
    else:
        clear()
        income_display()
        print(f'{Fore.RED}You do not have enough storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')


def andor():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if the system is not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Define menu options
    system_findings = {
        1: ('Dilithium Mine', lambda: handle_mining('dilithium', ['dilithium_mine1', 'dilithium_mine2', 'dilithium_mine3'], 'Dilithium')),
        2: ('Mission Planet', handle_mission_planet),
        3: ('Tholian Incursion Ship', handle_tholian_ship),
        4: ('Parsteel Mine', lambda: handle_mining('parsteel', ['parsteel_mine1', 'parsteel_mine2', 'parsteel_mine3'], 'Parsteel'))
    }

    if cache['missions']['Protect Dilithium Convoy']['accepted'] == True and cache['missions']['Protect Dilithium Convoy']['progress'] == 1:
        system_findings[5] = (f'{Fore.YELLOW}Protect Dilithium Convoy{Fore.WHITE}', handle_dilithium_convoy)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_mission_planet():
    """Handles the Mission Planet interaction."""
    clear()
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()


def handle_tholian_ship():
    """Handles the Tholian Incursion Ship encounter."""
    clear()
    income_display()
    print('You have approached a Tholian Incursion Ship!')
    print('What do you want to do?')
    op_1 = ['1: Attack the Ship', '2: Hail the Ship']
    print(*op_1, sep='\n')

    ori_ship = ask_sanitize('What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(800, 1200),
            opponent_name='Tholian Incursion Ship',
            firepower=3, accuracy=3, evasion=3,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()

def handle_dilithium_convoy():
    """Handles the Dilithium Convoy Mission"""
    clear()
    income_display()
    while True:
        mission_step = cache['missions']['Protect Dilithium Convoy']['progress']
        if mission_step == 1:
            typing_animation(f"Federation Destroyer: Thank you for the support, independent. We will support you if you need, but your {cache['ship']} appears to be stronger than our destroyers.")
            typing_animation("Hopefully this will be smooth sailing. Lets move.")
            travel_bar("Andor", "Astroid Field", 60, 30)
            typing_animation(f"{Fore.RED}Federation Destroyer: Pirate has been spotted on sensors. Go to red alert. Charge weapons.")
            time.sleep(2)
            battle_stat(1000, 'Shadow of Praxis Pirate', ((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250)), 2, 3, 2)
        elif mission_step == 2:
            clear()
            income_display()
            typing_animation(f"{Fore.GREEN}Federation Destroyer: I owe you one, captain. Lets keep moving. Once we get to the astroid field, pirates wont bother us anymore.{Fore.WHITE}")
            time.sleep(2)
            travel_bar("Andor", "Astroid Field", 54, 30)
            typing_animation("Federation Destroyer: We have made it to the astroid field. Should be smooth sailing from here. If you want to gather some science on the astroid field, go ahead.")
            if ask("Would you like to take a risk and possibly gather valuables from the science? (Y/N): "):
                colored_gradient_loading_bar(duration=15)
                asteroid_find = [
                    {"description": "Mineralogical Breakthrough: Discover a new alloy.", "type": "good", "reward": {"tritanium": 50}},
                    {"description": "Rare Isotopes: Boost warp core efficiency.", "type": "good", "reward": {"dilithium": 40}},
                    {"description": "Micrometeorite Storm: Damages ship systems.", "type": "bad", "penalty": {"health": -20}},
                    {"description": "Radiation Exposure: Compromises crew health.", "type": "bad", "penalty": {"health": -10}},
                    {"description": "Dilithium Deposits: Rich resource bonus.", "type": "good", "reward": {"dilithium": 100}},
                    {"description": "Explosive Gas Pockets: Causes hull damage.", "type": "bad", "penalty": {"health": -30}},
                    {"description": "Ancient Artifact: Unlocks cultural insights.", "type": "good", "reward": {"latinum": 20}},
                    {"description": "Gravitational Anomaly: Risks collision.", "type": "bad", "penalty": {"health": -15}},
                ]

                materials = {"tritanium": load_ship_stat(cache['ship'], 'tritanium_storage'), "dilithium": load_ship_stat(cache['ship'], 'dilithium_storage'), "health": load_ship_stat(cache['ship'], 'health')}

                def explore_asteroid_field():
                    outcome = random.choice(asteroid_find)
                    print(f"Outcome: {outcome['description']}")
                    if outcome["type"] == "good":
                        for key, value in outcome["reward"].items():
                            save_ship_data(cache['ship'], key, materials.get(key, 0) + value)
                            print(f"Reward: {value} {key}")
                            time.sleep(2)
                    elif outcome["type"] == "bad":
                        for key, value in outcome["penalty"].items():
                            save_ship_data(cache['ship'], key, materials.get(key, 0) + value)
                            print(f"Penalty: {value} {key}")
                            time.sleep(2)
                            
                explore_asteroid_field()
            else:
                print("You have missed an opportunity to gain, but you could have lost things too.")
                time.sleep(3)
            update_mission_progress('Protect Dilithium Convoy', 1)
        elif mission_step == 3:
                clear()
                income_display()
                travel_bar("Astroid Felid", "Tellar", 20, 30)
                cache['current_system'] = 3
                typing_animation("Federation Destroyer: Thanks for the help independent. We could not have done it without you. Here is your reward for helping us out.")
                update_mission_progress('Protect Dilithium Convoy', 1)
        else:
            return

def omicron_ii():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if the system is not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Define menu options
    system_findings = {
        1: ('Dilithium Mine', lambda: handle_mining('dilithium', ['dilithium_mine1', 'dilithium_mine2'], 'Dilithium')),
        2: ('Mission Planet', handle_mission_planet),
        3: ('Tritanium Mine', lambda: handle_mining('tritanium', ['tritanium_mine1', 'tritanium_mine2'], 'Tritanium')),
        4: ('Parsteel Mine', lambda: handle_mining('parsteel', ['parsteel_mine1', 'parsteel_mine2'], 'Parsteel')),
        5: ('Latinum Mine', lambda: handle_mining('latinum', ['latinum_mine1', 'latinum_mine2'], 'Latinum'))
    }
    
    if cache['missions']['Scan for Anomalies']['accepted'] == True and cache['missions']['Scan for Anomalies']['progress'] == 1:
        system_findings[6] = (f'{Fore.YELLOW}Scan for Anomalies{Fore.WHITE}', scan_for_anomalies)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_mission_planet():
    """Handles the Mission Planet interaction."""
    clear()
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()

def scan_for_anomalies():
    """Handles the Mission to scan for anomalies"""
    while True:
        clear()
        income_display()
        if cache['missions']['Scan for Anomalies']['progress'] == 1:
            print("Calibrating Sensors to Start Scans...")
            colored_gradient_loading_bar(duration=18)
            print(f"{Fore.GREEN}Calibration Complete!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.BLUE}Starting Scan of Anomaly...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=15)
            print(f"{Fore.GREEN}Scan Complete!{Fore.WHITE}")
            time.sleep(2)
            print("Return to drydock to report your findings to Starfleet.")
            time.sleep(2)
            input("Press enter to continue...")
            update_mission_progress('Scan for Anomalies', 1)
        elif cache['missions']['Scan for Anomalies']['progress'] == 2:
            print(f"{Fore.BLUE}Sending data to Starfleet...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=14)
            print(f"{Fore.GREEN}Upload Complete!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}Starfleet appreciates your work. They reward you with 50 latinum.{Fore.WHITE}")
            update_mission_progress('Scan for Anomalies', 1)
            time.sleep(2)
            input("Press enter to exit...")
        else:
            return
            
def regula():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if system not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Load mission data
    mission_data = cache['missions'].get("Respond to the Distress Signal in Regula", {})
    mission_available = mission_data.get("accepted") and mission_data.get("progress") == 1

    # Define menu options
    system_findings = {
        1: ('Klingon Intelligence Operative', handle_klingon_operative),
        2: ('Latinum Mine', lambda: handle_mining('latinum', ['latinum_mine1'], 'Latinum')),
        3: ('Dilithium Mine', lambda: handle_mining('dilithium', ['dilithium_mine1', 'dilithium_mine2', 'dilithium_mine3', 'dilithium_mine4'], 'Dilithium'))
    }

    if mission_available:
        system_findings[4] = (f'{Fore.YELLOW}Respond to Distress Call{Fore.WHITE}', distress_call_scenario)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_klingon_operative():
    """Handles interaction with the Klingon Intelligence Operative."""
    income_display()
    print('You have approached a Klingon Intelligence Operative!')
    print('What do you want to do?')
    options = ['1: Attack the Ship', '2: Hail the Ship']
    print(*options, sep='\n')
    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(900, 1300),
            opponent_name='Klingon Intelligence Operative',
            firepower=4,
            accuracy=3,
            evasion=4,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()


def solaria():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if system not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Load mission data
    mission_data = cache['missions'].get("Respond to the Distress Signal in Regula", {})
    mission_available = mission_data.get("accepted") and mission_data.get("progress") == 2

    # Define menu options
    system_findings = {
        1: ('Hirogen Tracker', handle_hirogen_tracker),
        2: ('Parsteel Mine', lambda: handle_mining('parsteel', ['parsteel_mine1', 'parsteel_mine2', 'parsteel_mine3'], 'Parsteel')),
        3: ('Tritanium Mine', lambda: handle_mining('tritanium', ['tritanium_mine1', 'tritanium_mine2', 'tritanium_mine3'], 'Tritanium'))
    }

    if mission_available:
        system_findings[4] = (f'{Fore.YELLOW}Scan for the unknown ship{Fore.WHITE}', distress_call_scenario_pt2)
    if cache['missions']['The Starship Graveyard']['accepted'] == True and cache['missions']['The Starship Graveyard']['progress'] == 1:
        system_findings[5] = (f'{Fore.YELLOW}Enter Mutara Nebula{Fore.WHITE}', starship_graveyard)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_hirogen_tracker():
    """Handles the logic for engaging with a Hirogen Tracker."""
    income_display()
    print('You have approached a Hirogen Tracker!')
    print('What do you want to do?')
    options = ['1: Attack the Ship', '2: Hail the Ship']
    print(*options, sep='\n')
    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(1000, 1400),
            opponent_name='Hirogen Tracker',
            firepower=4,
            accuracy=5,
            evasion=4,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()

def starship_graveyard():
        clear()
        income_display()
        if cache['missions']['The Starship Graveyard']['progress'] == 1:
            print(f"{Fore.RED}Sensors and Transporters have gone offline!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.YELLOW}Veiwscreen shows remains of a starship. It appears to be at the designated coordinates.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}You have arrived at the Starship Graveyard.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.BLUE}Beginning EVAs to investigate the wreckage...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=13)
            print(f"{Fore.GREEN}Investigation of area complete. Beginning to extract major parts...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=20)
            print(f"{Fore.GREEN}Extraction complete!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}Return to Sol to give the pieces to Starfleet Command.{Fore.WHITE}")
            time.sleep(2)
            update_mission_progress('The Starship Graveyard', 1)
        elif cache['missions']['The Starship Graveyard']['progress'] == 2 and cache['current_system'] == 1:
            print(f"{Fore.GREEN}You have arrived at Sol with the parts.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}Delivering parts to Starfleet Command...{Fore.WHITE}")
            colored_gradient_loading_bar(duration=5)
            print(f"{Fore.GREEN}Parts delivered!{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}Starfleet Command thanks you for your help.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}You have been rewarded 35 latinum for your efforts.{Fore.WHITE}")
            time.sleep(2)
            update_mission_progress('The Starship Graveyard', 1)
            input("Press enter to exit...")

def tarkalea_xii():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if system not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Load mission data
    mission_data = cache['missions'].get("Survey the Rings of Tarkalea XII", {})
    mission_available = mission_data.get("accepted") and mission_data.get("progress") == 1

    # Define menu options
    system_findings = {
        1: ('Orion Slaver', handle_orion_slaver),
        2: ('Dilithium Mine', lambda: handle_mining('dilithium', ['dilithium_mine1', 'dilithium_mine2', 'dilithium_mine3', 'dilithium_mine4'], 'Dilithium')),
        3: ('Mission Planet', handle_mission_planet)
    }

    if mission_available:
        system_findings[4] = (f'{Fore.YELLOW}Survey the Rings of Tarkalea XII{Fore.WHITE}', handle_survey_mission)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_orion_slaver():
    """Handles the logic for engaging with an Orion Slaver."""
    income_display()
    print('You have approached an Orion Slaver!')
    print('What do you want to do?')
    options = ['1: Attack the Ship', '2: Hail the Ship']
    print(*options, sep='\n')
    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(1100, 1500),
            opponent_name='Orion Slaver',
            firepower=5,
            accuracy=5,
            evasion=6,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()


def handle_mission_planet():
    """Handles the logic for navigating to a mission planet."""
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()


def handle_survey_mission():
    """Handles the logic for the Survey the Rings of Tarkalea XII mission."""
    income_display()
    tarkalea_survey()


def xindi_starbase_9():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if system not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Define menu options
    system_findings = {
        1: ('Xindi Patroller', handle_xindi_patroller),
        2: ('Latinum Mine', lambda: handle_mining('latinum', ['latinum_mine1', 'latinum_mine2', 'latinum_mine3', 'latinum_mine4'], 'Latinum')),
        3: ('Dock with the Starbase', handle_starbase_docking)
    }

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_xindi_patroller():
    """Handles the logic for engaging with a Xindi Patroller."""
    income_display()
    print('You have approached an Xindi Patroller!')
    print('What do you want to do?')
    options = ['1: Attack the Ship', '2: Hail the Ship']
    print(*options, sep='\n')
    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(1200, 1600),
            opponent_name='Xindi Patroller',
            firepower=6,
            accuracy=7,
            evasion=5,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()


def handle_starbase_docking():
    """Handles the logic for docking with the starbase."""
    income_display()
    print(f"{Fore.BLUE}Requesting permission for docking...{Fore.WHITE}")
    time.sleep(2)
    print(f"{Fore.RED}Request Denied. Turn back now.{Fore.WHITE}")
    time.sleep(2)


def altor_iv():
    global tutorial_highlight3, tutorial_highlight5, tutorial_highlight7, tutorial_highlight9, tutorial_highlight4
    current_system = cache['current_system']
    check_update_mats()

    # Early return if system not fully explored
    if load_explored(systems[current_system]) != 1:
        if load_explored(systems[current_system]) == 2:
            income_display()
            scan_system()
        return

    # Define menu options
    system_findings = {
        1: ('Parsteel Mine', lambda: handle_mining('parsteel', ['parsteel_mine1'], 'Parsteel')),
        2: ('Mission Planet', handle_mission_planet),
        3: ('Latinum Mine', lambda: handle_mining('latinum', ['latinum_mine1'], 'Latinum')),
        4: ('Jem\'Hadar Vanguard', handle_jemhadar_vanguard),
        5: ('Tritanium Mine', lambda: handle_mining('tritanium', ['tritanium_mine1'], 'Tritanium')),
    }
    
    if cache['missions']['First Contact']['accepted'] == True:
        system_findings[6] = (f'{Fore.YELLOW}Establish First Contact{Fore.WHITE}', first_contact)

    # Display menu
    income_display()
    print(f"What would you like to navigate to in {systems[current_system]}?")
    for option, (description, _) in system_findings.items():
        print(f"{option}. {description}")

    # Get user choice and execute corresponding action
    current_system_rand = ask_sanitize('Option: ')
    if current_system_rand in system_findings:
        clear()
        action = system_findings[current_system_rand][1]
        action()


# Helper Functions
def handle_mission_planet():
    """Handles the logic for Mission Planet selection."""
    income_display()
    print('You have approached a Mission Planet!')
    print(*mission_list_print, sep='\n')
    print(f"{len(mission_list_print) + 1}: Exit")
    accept_missions()


def handle_jemhadar_vanguard():
    """Handles the logic for Jem'Hadar Vanguard interaction."""
    income_display()
    print("You have approached a Jem'Hadar Vanguard!")
    print('What do you want to do?')
    options = ['1: Attack the Ship', '2: Hail the Ship']
    print(*options, sep='\n')
    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
    if ori_ship == 1:
        battle_stat(
            opponent_health=random.randint(1300, 1700),
            opponent_name="Jem'Hadar Vanguard",
            firepower=8,
            accuracy=7,
            evasion=7,
            income=((system_deltas['Enemy Ships Loot'] ** cache['current_system']) * random.randint(100, 250))
        )
    elif ori_ship == 2:
        hailing_frequency()

def first_contact():
    while True:
        clear()
        income_display()
        if cache['missions']['First Contact']['progress'] == 1:
            clear()
            income_display()
            print(f"{Fore.YELLOW}You have arrived at the planet Altor IV. The planet is inhabited by a humanoid species.{Fore.WHITE}")
            time.sleep(1)
            print(f"{Fore.YELLOW}The inhabitants of Altor IV are hailing you.{Fore.WHITE}")
            time.sleep(1)
            typing_animation("Altor IV: Unknown ship, please identify yourself.")
            time.sleep(1)
            typing_animation("You: We are explorers from the United Federation of Planets. We come in peace. We would like to establish a diplomatic relationship with your people.")
            time.sleep(1)
            typing_animation("Altor IV: Welcome. We are cautious of outsiders. What are your true intentions?")
            time.sleep(1)
            typing_animation("You: Our goal is to share knowledge and culture. We believe both our civilizations can benefit from each other.")
            time.sleep(1)
            typing_animation("Altor IV: Knowledge can be powerful. How can we be sure it will not disrupt our way of life?")
            time.sleep(1)
            typing_animation("You: We are committed to respecting your traditions. We can offer technologies that enhance your current practices sustainably.")
            time.sleep(1)
            typing_animation("Altor IV: Sustainable technologies sound promising. But how can we maintain our independence while using them?")
            time.sleep(1)
            typing_animation("You: We can provide knowledge transfer, allowing your scientists to adapt any technology to suit your needs without reliance on outside help.")
            time.sleep(1)
            typing_animation("Altor IV: That is a fair approach. Though, we also value our culture deeply. Will you ensure it is respected during any exchanges?")
            time.sleep(1)
            typing_animation("You: Absolutely. Cultural exchange is vital. We want to learn from you and share our own traditions without imposing our ways.")
            time.sleep(1)
            typing_animation("Altor IV: I appreciate that perspective. Perhaps we could arrange to introduce you to our elders for further discussions?")
            time.sleep(1)
            typing_animation("You: I would be honored to meet your elders. Their wisdom will guide our discussions.")
            time.sleep(1)
            typing_animation("Altor IV: Very well, Cpatain. Let’s proceed with caution and mutual respect. Our future may depend on it.")
            update_mission_progress('First Contact', 1)  
        if cache['missions']['First Contact']['progress'] == 2:
            print(f"{Fore.YELLOW}You meet with the elders of Altor IV in a grand chamber adorned with rich tapestries.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.YELLOW}Time acceleration has been engaged and negotiations will run faster.{Fore.WHITE}")
            time.sleep(2)
            typing_animation_fast("Elder Zorak: Captain, we have heard about your intentions. What assurances can you provide us?")
            typing_animation_fast("You: We respect your sovereignty and aim to enhance your way of life without interference.")
            typing_animation_fast("Elder Zorak: Many outsiders make grand promises but do not deliver. How will you prove your sincerity?")
            typing_animation_fast("You: We come with our technology and knowledge, ready to demonstrate their potential benefits for your people.")
            typing_animation_fast("Elder Vela: Demonstrations are useful, but we seek to understand your culture. What values guide the Federation?")
            typing_animation_fast("You: The Federation values diversity, cooperation, and the pursuit of knowledge. We believe that all cultures enrich one another.")
            typing_animation_fast("Elder Vela: Words are powerful, but actions speak louder. If we proceed, can we set terms that protect our culture?")
            typing_animation_fast("You: Absolutely. We propose a formal agreement ensuring that your cultural practices are upheld and respected.")
            typing_animation_fast("Elder Zorak: Those terms sound reasonable. However, we will require time to consider and consult among ourselves.")
            typing_animation_fast("You: Take all the time you need. We are here to support you through this process.")
            typing_animation_fast("Elder Vela: We will reconvene shortly. Your patience is noted, Captain. May wisdom guide our decisions.")
            typing_animation_fast("You: Thank you, Elders. I look forward to working together as partners in this endeavor.")
            update_mission_progress('First Contact', 1)
            input("Press enter to exit...")
        if cache['missions']['First Contact']['progress'] == 3:
            print(f"{Fore.GREEN}You have successfully established First Contact with the inhabitants of Altor IV.{Fore.WHITE}")
            time.sleep(2)
            print(f"{Fore.GREEN}The Federation has recognized your efforts and rewarded you with 80 latinum.{Fore.WHITE}")
            update_mission_progress('First Contact', 1)
            time.sleep(2)
            input("Press enter to exit...")
            break


finding_var = 0
warp_time = 0

clear()
mission_list_print = ['1: Mine 100 Materials', '2: Defeat 1 Enemy', '3: Defeat 3 Enemies', '4: Trade 200 Materials With a Ship', '5: Defeat 5 Enemies', '6: Explore 3 New Systems', '7: Buy a new Ship', '8: Complete 2 Successful Trades', '9: Respond to the Distress Signal in Regula', '10: Survey the Rings of Tarkalea XII', '11: Protect Dilithium Convoy', '12: Scan for Anomalies', '13: Recover Lost Data', '14: The Starship Graveyard', '15: First Contact']

current_dir = os.path.dirname(os.path.realpath(__file__))

requirements_path = os.path.join(current_dir, 'requirements.txt')

try:
    subprocess.check_output([sys.executable, "-m", "pip", "install", "-r", requirements_path])
except subprocess.CalledProcessError:
    input('Something went wrong with PIP. Press enter to exit program...')
    sys.exit(1)

print('Necessary packages imported')

while True:
    if (load_ship_stat(cache['ship'], 'health')) <= 0:
        check_health()
    clear()
    mission_briefing()
    tutorial()
    dilithium_convoypt1()
    income_display()
    check_construction_completion()
    check_update_mats()
    check_research_completion()
    background_production()
    print('What would you like to do?')
    OpList = [f"{tutorial_highlight2}1: Explore {systems[cache['current_system']]}{Fore.WHITE}", f"{tutorial_highlight6}2: Navigate to Another System{Fore.WHITE}", f"{tutorial_highlight1}3: Return to Drydock{Fore.WHITE}", "4: Display Missions", f"{tutorial_highlight11}5: Open Shop{Fore.WHITE}"]
    print(*OpList, sep = '\n')
    option = ask_sanitize_lobby(question_ask='Option: ', valid_options=[1, 2, 3, 4, 5])
    time.sleep(0.1)
    if option == 1:
        clear()
        system_functions = {
        1: sol,
        2: vulcan,
        3: tellar,
        4: andor,
        5: omicron_ii,
        6: regula,
        7: solaria,
        8: tarkalea_xii,
        9: xindi_starbase_9,
        10: altor_iv,
        }
        current_system = cache['current_system']
        if current_system in system_functions:
            system_functions[current_system]()
    if option == 2:
        navigate()
    if option == 3:
        if ask(f"{Fore.RED}Are you sure you want to travel back to Sol? (Y/N) {Fore.WHITE}"):
            warp_time = abs(cache['current_system'] - 1) * 10
            clear()
            income_display()
            print(f"{Fore.BLUE}Traveling...{Fore.WHITE}")
            travel_bar(systems[cache['current_system']], "Sol", warp_time, 30)
            clear()
            cache['current_system'] = 1
            transfer_resources_to_storage()
            income_display()
            cache['current_system'] = 1
            process_tutorial_step()
            scan_for_anomalies()
            recover_lost_data()
            mission_data = cache['missions'].get("Survey the Rings of Tarkalea XII", {})
            if mission_data.get("accepted") and mission_data.get("progress") == 2:
                update_mission_progress('Survey the Rings of Tarkalea XII', 1)
            drydock_option = [f'{tutorial_highlight3}1: Enter Station{Fore.WHITE}', f'{tutorial_highlight7}2: Enter Shipyard{Fore.WHITE}', '3: Open Research', f'{tutorial_highlight5}4: Repair Ship{Fore.WHITE}', '5: Exit']
            print(*drydock_option, sep='\n')
            drydock_selection = ask_sanitize('Option: ')
            if drydock_selection == 1: #Enter station
                clear()
                income_display()
                if cache['tutorial'] == 1:
                    print(f"{Fore.YELLOW}Now that you are inside of the station, lets upgrade the generators. These produce parsteel, tritanium, and dilithium every few minutes. When you upgrade them, they produce more.\nPress 1 and enter the generators.{Fore.WHITE}")
                    time.sleep(2)
                elif cache['tutorial'] == 10:
                    print(f"{Fore.YELLOW}Enter generators.{Fore.WHITE}")
                else:
                    tutorial_highlight3 = Fore.WHITE
                station_options = [f'{tutorial_highlight3}1: Enter Generators{Fore.WHITE}', '2: Enter Shipyard', '3: Enter R&D Department', f'{tutorial_highlight9}4: Enter Academy{Fore.WHITE}', '5: Enter Ops', '6: Exit']
                print(*station_options, sep='\n')
                station_selection = ask_sanitize('Option: ')
                if station_selection == 1:
                    clear()
                    income_display()
                    if cache['tutorial'] == 1:
                        print(f"{Fore.YELLOW}Every once and awhile, comeback to claim all generator material. For now, press 2 to upgrade a generator.{Fore.WHITE}")
                    if cache['tutorial'] == 10:
                        print("Now you can claim your generator material.")
                        tutorial_highlight3 = Fore.WHITE
                        tutorial_highlight10 = Fore.YELLOW
                    else:
                        tutorial_highlight10 = Fore.WHITE
                    print('Generator Menu')
                    print(f'{tutorial_highlight10}1. Claim all generator material{Fore.WHITE}\n{tutorial_highlight3}2. Upgrade a Generator{Fore.WHITE}\n3. Exit')
                    generator_option = ask_sanitize("Option: ")
                    if generator_option == 1:
                        claim_resources()
                        time.sleep(2)
                    if generator_option == 2:
                        clear()
                        income_display()
                        if cache['tutorial'] == 1:
                            print("Now, press 1 to upgrade the parsteel generator.")
                        print(f'{tutorial_highlight3}1: Upgrade Parsteel Generator{Fore.WHITE}\n2: Upgrade Tritanium Generator\n3: Upgrade Dilithium Generator\n4: Exit')
                        generator_upgrade_delta = 1.5
                        generator_upgrade = ask_sanitize(f"{Fore.BLUE}What would you like to do: {Fore.WHITE}")
                        if generator_upgrade == 1:
                            upgrade_generator('Parsteel Generator')
                        elif generator_upgrade == 2:
                            upgrade_generator('Tritanium Generator')
                        elif generator_upgrade == 3:
                            upgrade_generator('Dilithium Generator')
                        elif generator_upgrade == 4:
                            continue
                    if generator_option == 3:
                        continue
                if station_selection == 2:
                    clear()
                    income_display()
                    shipyard_delta = 2.4
                    shipyard_op = ask_sanitize("1. Enter Shipyard\n2. Upgrade Shipyard\n3. Exit\nOption: ")
                    if shipyard_op == 1:
                        ship_management_menu(coins=cache['parsteel'])
                    elif shipyard_op == 2:
                        if ask(f"{Fore.YELLOW}Are you sure you want to upgrade? This will take {(load_specific_upgrade('starbase', 'Shipyard') ** shipyard_delta) * 10} seconds and will cost you {round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 10)} parsteel and {round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 5)} tritanium. (Y/N): {Fore.WHITE}") and cache['parsteel'] >= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 10) and cache['tritanium'] >= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 5):
                            cache['parsteel'] -= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 10)
                            cache['tritanium'] -= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 5)
                            start_construction('starbase', (load_specific_upgrade('starbase', 'Shipyard') ** shipyard_delta) * 10, 'Shipyard')
                        else:
                            print(f"{Fore.RED}You either canceled the upgrade, or you do not have enough parsteel or tritanium.{Fore.WHITE}")
                            time.sleep(2)
                    elif shipyard_op == 3:
                        continue
                if station_selection == 3: #R&D
                    clear()
                    if cache['tutorial'] == 4:
                        print(f"{Fore.YELLOW}Press 1 to enter research.{Fore.WHITE}")
                    income_display()
                    rd_delta = 2
                    print('R&D Menu')
                    print(f'{tutorial_highlight1}1. Enter Research{Fore.WHITE}\n2. Upgrade R&D Department\n3. Exit')
                    rd_option = ask_sanitize("Option: ")
                    if rd_option == 1:
                        clear()
                        if cache['tutorial'] == 4:
                            print(f"{Fore.YELLOW}Press 1 to View and Start research.{Fore.WHITE}")
                        income_display()
                        research_path = ask_sanitize(f"Research Menu\n{tutorial_highlight1}1. View Research - Start Research{Fore.WHITE}\n2. Exit\nOption: ")
                        if research_path == 1:
                            display_available_research()
                        if research_path == 2:
                            continue
                    if rd_option == 2:
                        if ask(f"{Fore.YELLOW}Are you sure you want to upgrade? This will take {(load_specific_upgrade('starbase', 'R&D') ** rd_delta) * 10} seconds and cost {round(((load_specific_upgrade('starbase', 'R&D') * rd_delta) ** rd_delta) * 10)} parsteel and {round(((load_specific_upgrade('starbase', 'R&D') * rd_delta) ** rd_delta) * 5)} tritanium. (Y/N): ") and cache['parsteel'] >= round(((load_specific_upgrade('starbase', 'R&D') * rd_delta) ** rd_delta) * 10) and cache['tritanium'] >= round(((load_specific_upgrade('starbase', 'R&D') * rd_delta) ** rd_delta) * 5):
                            cache['parsteel'] -= round(((load_specific_upgrade('starbase', 'R&D') * rd_delta) ** rd_delta) * 10)
                            cache['tritanium'] -= round(((load_specific_upgrade('starbase', 'R&D') * rd_delta) ** rd_delta) * 5)
                            start_construction('starbase', (load_specific_upgrade('starbase', 'R&D') ** rd_delta) * 10, 'R&D')
                        else:
                            print(f"{Fore.RED}You have either canceled the upgrade, or do not have enough parsteel or tritanium.{Fore.WHITE}")
                            time.sleep(2)
                    if rd_option == 3:
                        continue
                if station_selection == 4: #academy
                    clear()
                    if cache['tutorial'] == 9:
                        print(f"{Fore.YELLOW}View the officer menu by typing 1.{Fore.WHITE}")
                    income_display()
                    academy_delta = 2.3
                    print('Academy Menu')
                    academy_option = ask_sanitize(f'{tutorial_highlight9}1. View Officers{Fore.WHITE}\n2. Enter Shop\n3. Upgrade Academy\n4. Exit\nOption: ')
                    if academy_option == 1:
                        clear()
                        if __name__ == "__main__":
                            main()
                        continue
                    if academy_option == 2:
                        shop_loop()
                    if academy_option == 3:
                        if ask(f"{Fore.YELLOW}Are you sure you want to upgrade? This will take {(load_specific_upgrade('starbase', 'Academy') ** academy_delta) * 10} seconds and cost {round(((load_specific_upgrade('starbase', 'Academy') * academy_delta) ** academy_delta) * 10)} parsteel and {round(((load_specific_upgrade('starbase', 'Academy') * academy_delta) ** academy_delta) * 5)} tritanium. (Y/N): ") and cache['parsteel'] >= round(((load_specific_upgrade('starbase', 'Academy') * academy_delta) ** academy_delta) * 10) and cache['tritanium'] >= round(((load_specific_upgrade('starbase', 'Academy') * academy_delta) ** academy_delta) * 5):
                            cache['parsteel'] -= round(((load_specific_upgrade('starbase', 'Academy') * academy_delta) ** academy_delta) * 10)
                            cache['tritanium'] -= round(((load_specific_upgrade('starbase', 'Academy') * academy_delta) ** academy_delta) * 5)
                            start_construction('starbase', (load_specific_upgrade('starbase', 'Academy') ** academy_delta) * 10, 'Academy')
                        else:
                            print(f"{Fore.RED}You have either canceled the upgrade, or do not have enough parsteel or tritanium.{Fore.WHITE}")
                            time.sleep(2)
                    if academy_option == 4:
                        continue
                if station_selection == 5: #ops
                    clear()
                    income_display()
                    ops_delta = 2.1
                    print("Ops Menu")
                    ops_option = ask_sanitize("1. Upgrade Ops\n2. Exit\nOption: ")
                    if ops_option == 1:
                        if ask(f"{Fore.YELLOW}Are you sure you want to upgrade? This will take {(load_specific_upgrade('starbase', 'Ops') ** ops_delta) * 10} seconds and cost {round(((load_specific_upgrade('starbase', 'Ops') * ops_delta) ** ops_delta) * 10)} parsteel and {round(((load_specific_upgrade('starbase', 'Ops') * ops_delta) ** ops_delta) * 5)} tritanium. (Y/N): ") and cache['parsteel'] >= round(((load_specific_upgrade('starbase', 'Ops') * ops_delta) ** ops_delta) * 10) and cache['tritanium'] >= round(((load_specific_upgrade('starbase', 'Ops') * ops_delta) ** ops_delta) * 5):
                            cache['parsteel'] -= round(((load_specific_upgrade('starbase', 'Ops') * ops_delta) ** ops_delta) * 10)
                            cache['tritanium'] -= round(((load_specific_upgrade('starbase', 'Ops') * ops_delta) ** ops_delta) * 5)
                            start_construction('starbase', (load_specific_upgrade('starbase', 'Ops') ** ops_delta) * 10, 'Ops')
                        else:
                            print(f"{Fore.RED}You either canceled the upgrade, or do not have enough parsteel or tritanium.{Fore.WHITE}")
                            time.sleep(2)
                    if ops_option == 2:
                        continue
            if drydock_selection == 2: #Shipyard
                clear()
                income_display()
                shipyard_delta = 2.4
                shipyard_op = ask_sanitize(f"{tutorial_highlight7}1. Enter Shipyard{Fore.WHITE}\n2. Upgrade Shipyard\n3. Exit\nOption: ")
                if shipyard_op == 1:
                    ship_management_menu(coins=cache['parsteel'])
                elif shipyard_op == 2:
                    if ask(f"{Fore.YELLOW}Are you sure you want to upgrade? This will take {(load_specific_upgrade('starbase', 'Shipyard') ** shipyard_delta) * 10} seconds and will cost you {round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 10)} parsteel and {round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 5)} tritanium. (Y/N): {Fore.WHITE}") and cache['parsteel'] >= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 10) and cache['tritanium'] >= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 5):
                        cache['parsteel'] -= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 10)
                        cache['tritanium'] -= round(((load_specific_upgrade('starbase', 'Shipyard') * shipyard_delta) ** shipyard_delta) * 5)
                        start_construction('starbase', (load_specific_upgrade('starbase', 'Shipyard') ** shipyard_delta) * 10, 'Shipyard')
                    else:
                        print(f"{Fore.RED}You either canceled the upgrade, or you do not have enough parsteel or tritanium.{Fore.WHITE}")
                        time.sleep(2)
                elif shipyard_op == 3:
                    continue
            if drydock_selection == 3: #research
                clear()
                income_display()
                display_available_research()
            if drydock_selection == 4:
                clear()
                if cache['tutorial'] == 3:
                    print(f"{Fore.YELLOW}Press y to repair your ship.{Fore.WHITE}")
                income_display()
                if ask(f"{Fore.RED}Are you sure you want to repair your ship? This will cost you {calculate_repair_cost(round(research_multi('Sheild Dynamics') * (load_ship_stat(ship_name=cache['ship'], stat_key='max_health') - load_ship_stat(ship_name=cache['ship'], stat_key='health')) / 5))} parsteel. (Y/N): ") and cache['parsteel'] >= calculate_repair_cost(round(research_multi('Sheild Dynamics') * (load_ship_stat(ship_name=cache['ship'], stat_key='max_health') - load_ship_stat(ship_name=cache['ship'], stat_key='health')) / 5)):
                    cache['parsteel'] -= calculate_repair_cost(round(research_multi('Sheild Dynamics') * (load_ship_stat(ship_name=cache['ship'], stat_key='max_health') - load_ship_stat(ship_name=cache['ship'], stat_key='health')) / 5))
                    save_ship_data(ship_name=cache['ship'], stat_key='health', value=(research_multi('Sheild Dynamics') * load_ship_stat(ship_name=cache['ship'], stat_key='max_health')))
                    print(f"{Fore.GREEN}Repair Completed. You now have {load_ship_stat(cache['ship'], 'health')} health.{Fore.WHITE}")
                    if cache['tutorial'] == 3:
                        cache['tutorial'] = 4
                    time.sleep(2)
                    continue
                else:
                    print(f"{Fore.YELLOW}Repair Canceled.{Fore.WHITE}")
                    time.sleep(2)
                    continue
        else:
            continue
    if option == 4:
        clear()
        income_display()
        display_missions()
        if ask("Type Y to exit: "):
            continue
    if option == 5:
        clear()
        shop_loop()
