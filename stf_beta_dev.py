import json
import time
import random
import os
from colorama import Fore
import subprocess
import sys
from datetime import datetime, timedelta

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

shuttle_bays = 1
original_crew_file_path = 'crew_list.json'
user_crew_file_path = 'user_crew_data.json'
user_game_file_path = 'user_data.json'
ship_save = 'ship_save.json'
json_file_path = 'system_data.json'

# Function to load the JSON data from the file
def load_json_data():
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return None

# Function to load the material amount from a specific mining node
def get_material_in_node(system_name, mine_name):
    data = load_json_data()
    
    if data is None:
        return None

    # Find the system with the given name
    for system in data["system data"]:
        if system["name"] == system_name:
            # Check if the specified mine exists in the system
            if mine_name in system:
                return system[mine_name]
            else:
                print(f"Error: {mine_name} does not exist in {system_name}.")
                return None
    else:
        print(f"Error: System {system_name} not found.")
        return None

# Function to save the updated JSON data back to the file
def save_json_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to update the mining node materials
def update_materials(system_name, mine_name, amount):
    data = load_json_data()
    
    if data is None:
        return

    # Find the system with the given name
    for system in data["system data"]:
        if system["name"] == system_name:
            # Update the material in the specified mine
            if mine_name in system:
                system[mine_name] -= amount

                # Reset the mine to 100 if the materials go below or equal to 0
                if system[mine_name] <= 0:
                    system[mine_name] = 100
                    print(f"{mine_name} in {system_name} has been reset to 100.")

                save_json_data(data)  # Save the updated data
            else:
                print(f"Error: {mine_name} does not exist in {system_name}.")
            break
    else:
        print(f"Error: System {system_name} not found.")


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

# Load data from JSON file
def load_data(key):
    try:
        with open('user_data.json', 'r') as file:
            data = json.load(file)
        # Traverse nested dictionaries if necessary
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

# Save data to JSON file
def save_data(key, value):
    try:
        # Use 'r+' for both reading and writing without truncating the file
        with open('user_data.json', 'r+') as file:
            data = json.load(file)  # Read existing data

            # Update the key or nested key
            if key in data:
                data[key] = value
            else:
                print(f"Key '{key}' not found. Adding it at the top level.")
                data[key] = value  # Add new key if not found

            # Seek back to the beginning to overwrite the file
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()  # Ensure file size is adjusted

    except FileNotFoundError:
        print("Game data file not found.")

def increment_upgrade(upgrade_type):
    """Increment the value of a specified upgrade type by 1 and save it to the JSON file."""
    # Load the existing upgrades dictionary
    upgrades = load_data('upgrades')
    
    if upgrades is None:
        return
    
    # Check if the upgrade_type exists in the dictionary
    if upgrade_type in upgrades:
        # Increment the value of the specified upgrade type
        upgrades[upgrade_type] += 1
    else:
        return
    
    # Save the updated upgrades dictionary back to the JSON file
    save_data('upgrades', upgrades)

def save_ship_data(ship_name, stat_key, value):
    try:
        with open('ship_save.json', 'r+') as file:
            data = json.load(file)

            # Find the ship and update the stat
            for ship in data['ship selection']:
                if ship['name'] == ship_name:
                    if stat_key in ship:
                        ship[stat_key] = value
                    else:
                        print(f"Stat '{stat_key}' not found for ship '{ship_name}'.")
                        return
            
            # Save updated data back to the JSON file
            file.seek(0)  # Move the file pointer to the beginning
            json.dump(data, file, indent=4)
            file.truncate()  # Remove any leftover data from the previous file size

    except FileNotFoundError:
        print("Ship data file not found.")

def load_ship_stat(ship_name, stat_key):
    try:
        with open('ship_save.json', 'r') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name:
                    return ship.get(stat_key, None)  # Return None if the stat doesn't exist

        print(f"Ship '{ship_name}' not found.")
        return None
    except FileNotFoundError:
        print("Ship data file not found.")
        return None

def is_ship_owned(ship_name):
    try:
        with open('ship_save.json', 'r') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name:
                    return ship.get('owned', False)  # Return False if 'owned' key is missing

        print(f"Ship '{ship_name}' not found.")
        return False
    except FileNotFoundError:
        print("Ship data file not found.")
        return False
    
def set_ship_owned_status(ship_name, owned_status):
    try:
        with open('ship_save.json', 'r+') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name:
                    ship['owned'] = owned_status  # Update the 'owned' status

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")

def equip_ship_in_game(ship_name):
    try:
        # Load user game data
        with open('user_data.json', 'r+') as user_file:
            user_data = json.load(user_file)
            
            # Load available ships data
            with open('ship_save.json', 'r') as ship_file:
                ship_data = json.load(ship_file)

            # Check if the selected ship is owned
            for ship in ship_data['ship selection']:
                if ship['name'] == ship_name and ship.get('owned', False):
                    # Equip the ship by updating the user game data
                    user_data['ship'] = ship_name
                    print(f"{ship_name} is now equipped in your game data!")
                    break
            else:
                print(f"You do not own the ship: {ship_name}")

            # Save the updated game data back to the JSON file
            user_file.seek(0)
            json.dump(user_data, user_file, indent=4)
            user_file.truncate()

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def upgrade_ship(ship_name, stat, coins):
    try:
        with open('ship_save.json', 'r+') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name and ship.get('owned', False):
                    if ship_name == 'Galaxy Class':
                        upgrade_cost = 150
                    else:
                        upgrade_cost = 50
                    if load_data('parsteel') >= upgrade_cost:
                        ship[stat] += 1
                        save_data('parsteel', load_data('parsteel') - upgrade_cost)
                        print(f"{Fore.GREEN}{ship_name}'s {stat} has been upgraded to {ship[stat]}.{Fore.WHITE}")
                        time.sleep(2)
                    else:
                        print(f"{Fore.RED}Not enough parsteel to upgrade {stat}.{Fore.WHITE}")
                        time.sleep(2)

                    break

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")
    
    return load_data('parsteel')

def equip_ship(ship_name):
    try:
        with open('ship_save.json', 'r+') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name and ship.get('owned', False):
                    # Set all ships to not equipped
                    for s in data['ship selection']:
                        s['equipped'] = False

                    # Equip the selected ship
                    ship['equipped'] = True
                    save_data('ship', ship_name)
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
        with open('ship_save.json', 'r+') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name and not ship['owned']:
                    current_coins = load_data('tritanium')
                    if ship_name == 'Galaxy Class':
                        price = 2000
                    elif ship_name == 'Federation Shuttlecraft':
                        price = 400
                    elif ship_name == 'USS Grissom':
                        price = 350
                    else:
                        price = 200
                    if ask(f"{Fore.RED}Are you sure you want to buy this ship? It costs {price} tritanium ({load_data('tritanium')}->{load_data('tritanium') - price}): {Fore.WHITE}"):
                        if current_coins >= price:
                            clear()
                            ship['owned'] = True
                            save_data('tritanium', current_coins - price)
                            print(f"{Fore.GREEN}You have purchased {ship_name}.{Fore.WHITE}")
                            time.sleep(2)
                        else:
                            print("Not enough tritanium to buy this ship.")
                            time.sleep(2)
                        break
                    else:
                        break

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")
    
    return coins

def view_ship_details(ship_name):
    try:
        with open('ship_save.json', 'r') as file:
            data = json.load(file)

        for ship in data['ship selection']:
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
        with open('ship_save.json', 'r') as file:
            data = json.load(file)
        print('')
        for i, ship in enumerate(data['ship selection'], 1):
            print(f"{Fore.BLUE}{i}. {ship['name']} (Owned: {ship.get('owned', False)}){Fore.WHITE}")

    except FileNotFoundError:
        print("Ship data file not found.")

def ship_management_menu(coins):
    global ship_name
    while True:
        clear()
        income_display()
        display_ship_menu()

        choice = ask_sanitize(question_ask="\nOptions:\n1. View Ship Details\n2. Build Ship\n3. Equip Ship\n4. Upgrade Ship\n5. Exit\nSelect an option: ")

        if choice == 1:
            clear()
            display_ship_menu()
            ship_num = ask_sanitize(question_ask='What ship would you like to view? ')
            if ship_num == 1:
                ship_name = 'Stargazer'
            elif ship_num == 2:
                ship_name = 'USS Grissom'
            elif ship_num == 3:
                ship_name = 'Federation Shuttlecraft'
            elif ship_num == 4:
                ship_name = 'Galaxy Class'
            view_ship_details(ship_name)

        elif choice == 2:
            clear()
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize(question_ask='What ship would you like to build? ')
            if ship_num == 1:
                ship_name = 'Stargazer'
            elif ship_num == 2:
                ship_name = 'USS Grissom'
            elif ship_num == 3:
                ship_name = 'Federation Shuttlecraft'
            elif ship_num == 4:
                ship_name = 'Galaxy Class'
            buy_ship(ship_name, coins)

        elif choice == 3:
            clear()
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize(question_ask='What ship would you like to equip? ')
            if ship_num == 1:
                ship_name = 'Stargazer'
            elif ship_num == 2:
                ship_name = 'USS Grissom'
            elif ship_num == 3:
                ship_name = 'Federation Shuttlecraft'
            elif ship_num == 4:
                ship_name = 'Galaxy Class'
            equip_ship(ship_name)

        elif choice == 4:
            clear()
            income_display()
            display_ship_menu()
            ship_num = ask_sanitize(question_ask='What ship would you like to upgrade? ')
            if ship_num == 1:
                ship_name = 'Stargazer'
            elif ship_num == 2:
                ship_name = 'USS Grissom'
            elif ship_num == 3:
                ship_name = 'Federation Shuttlecraft'
            elif ship_num == 4:
                ship_name = 'Galaxy Class'
            stat_num = ask_sanitize("Enter the stat to upgrade (1. firepower, 2. accuracy, 3. evasion, 4. antimatter, 5. storage): ")
            if stat_num == 1:
                stat = 'firepower'
            if stat_num == 2:
                stat = 'accuracy'
            if stat_num == 3:
                stat = 'evasion'
            if stat_num == 4:
                stat = 'antimatter'
            if stat_num == 5:
                stat = 'storage'
            upgrade_ship(ship_name, stat, coins)

        elif choice == 5:
            break
        else:
            print("Invalid option. Please try again.")
            time.sleep(2)


# Upgrades, Costs, Deltas, Systems, and Other Game Data
costs = {"Mining Laser": 15, "Health": 10, "Phaser": 20, "Warp Range": 15}
deltas = {"Mining Laser": 1.5, "Health": 2, "Phaser": 2, "Warp Range": 2}
system_deltas = {'Material Cluster': 1.5, 'Trading Post': 2, 'Enemy Ships Loot': 1.5, 'Enemy Ships Health': 1.3}
systems = {
    1: 'Sol', 2: 'Vulcan', 3: 'Tellar', 4: 'Andor', 5: 'Omicron II', 
    6: 'Regula', 7: 'Solaria', 8: 'Tarkalea XII', 9: 'Xindi Starbase 9', 10: 'Altor IV'
}

def load_crew_data(file_path): #load crew
    with open(file_path, 'r') as file:
        return json.load(file)

def save_crew_data(file_path, data): #save crew
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_game_data(file_path): #load game state
    with open(file_path, 'r') as file:
        return json.load(file)

def save_game_data(file_path, data): #save game state
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def has_played_before(file_path): #check if personal file path exists
    return os.path.exists(file_path)

def initialize_game_data(): #initialize load or save data
    if has_played_before(user_game_file_path):
        with open(user_game_file_path, 'r') as file:
            return json.load(file)
    else:
        return game_state

def initialize_crew_data(): #initialize load or save crew
    if has_played_before(user_crew_file_path):
        with open(user_crew_file_path, 'r') as file:
            return json.load(file)
    else:
        original_crew_data = load_crew_data(original_crew_file_path)
        save_crew_data(user_crew_file_path, original_crew_data)
        return original_crew_data

def display_crew(crew_data): #display crew
    print("\nCurrent Crew Members:")
    for index, member in enumerate(crew_data['crew']):
        print(f"{index + 1}. {member['name']} (Skill: {member['skill']}, Skill Level: {member['skill_level']}, Rarity: {member['rarity']})")

def upgrade_crew_member(game_state, crew_data, member_index, cost):

    if load_data('recruit_tokens') >= cost:
        crew_data['crew'][member_index]['skill_level'] += 5  # Increase skill level
        save_data('recruit_tokens', load_data('recruit_tokens') - cost)
        print(f"{Fore.GREEN}\n{crew_data['crew'][member_index]['name']}'s skill level increased to {crew_data['crew'][member_index]['skill_level']}!{Fore.WHITE}")
        print(f"{Fore.YELLOW}Remaining Recruit Tokens: {load_data('recruit_tokens')}{Fore.WHITE}")
        time.sleep(2)
    else:
        print(f"{Fore.RED}\nNot enough recruit tokens to upgrade.{Fore.WHITE}")
        time.sleep(2)

# Main function
def main():
    global game_state
    game_state = initialize_game_data()
    crew_data = initialize_crew_data()
    
    display_crew(crew_data)

    choice = int(input(f"{Fore.BLUE}\nEnter the number of the crew member to upgrade: {Fore.WHITE}")) - 1  # Convert to 0-based index

    cost = 10
    print(f"{Fore.YELLOW}Upgrading {crew_data['crew'][choice]['name']} will cost {cost} recruit tokens.{Fore.WHITE}")
    if ask(f"{Fore.RED}Do you want to proceed? (y/n): {Fore.WHITE}"):
        upgrade_crew_member(game_state, crew_data, choice, cost)
        save_crew_data(user_crew_file_path, crew_data)  # Save updated user crew data to file
        print("\nGame data and crew data saved.")
    else:
        print(f"{Fore.RED}\nUpgrade canceled.{Fore.WHITE}")
        time.sleep(1)

def income_display():
     print(f"{Fore.YELLOW}Parsteel:{Fore.WHITE} {load_data('parsteel')} || {Fore.GREEN}Tritanium:{Fore.WHITE} {load_data('tritanium')} || {Fore.CYAN}Dilithium:{Fore.WHITE} {load_data('dilithium')} || {Fore.YELLOW}Latnium:{Fore.WHITE} {load_data('latnium')} || {Fore.LIGHTBLUE_EX}Current Ship:{Fore.WHITE} {load_data('ship')} || {Fore.LIGHTBLUE_EX}Current System:{Fore.WHITE} {systems[load_data('current_system')]} || {Fore.BLUE}Health:{Fore.WHITE} {load_ship_stat(ship_name=load_data('ship'), stat_key='health')}/{load_ship_stat(ship_name=load_data('ship'), stat_key='max_health')} || {Fore.GREEN}Storage Avalible:{Fore.WHITE} {load_ship_stat(ship_name=load_data('ship'), stat_key='storage')}/{load_ship_stat(ship_name=load_data('ship'), stat_key='max_storage')}")

def ask(question):
        response = input(question)
        return response.lower() in ["y", "yes"] 

def upgrade(type):
        current_upgrade_level = load_data('upgrades')[type]
        current_upgrade_cost = costs[type] * (deltas[type] **  current_upgrade_level) 
        if load_data('coins') >= current_upgrade_cost: 
                print(f"{Fore.YELLOW}You are upgrading your {type} from level {current_upgrade_level} to {current_upgrade_level + 1}.\n {Fore.RED}This upgrade will cost you {current_upgrade_cost} coins. ({load_data('coins')} -> {load_data('coins') - current_upgrade_cost}){Fore.WHITE} ")
                if ask(f"{Fore.RED}Are you sure you want to continue?{Fore.WHITE} "):  
                        save_data('coins', load_data('coins') - current_upgrade_cost)
                        increment_upgrade(type)  
                        return True  
        else:
                print(f"{Fore.YELLOW}You can't upgrade your {type} from level {current_upgrade_level} to {current_upgrade_level + 1} because you don't have enough coins (current: {load_data('coins')}, required: {current_upgrade_cost}).{Fore.WHITE}")
                return False

def view_upgrades():
    clear()
    upgrades = load_data('upgrades')
    print(f"{Fore.GREEN}Your upgrades:{Fore.WHITE}\n{chr(10).join([u + ': Level ' + str(upgrades[u]) for u in upgrades.keys()])}")
    continue_1 = ask(f'{Fore.RED}Continue? {Fore.WHITE}')
    if continue_1 == ('y', 'yes'):
        time.sleep(0.001)
        
def accept_mission(mission_id):
    mission_list = {'1': 'Mine 100 Materials', '2': 'Defeat 1 Enemy', '3': 'Defeat 3 Enemies', '4': 'Trade 200 Materials With a Ship', '5': 'Defeat 5 Enemies', '6': 'Explore 3 New Systems', '7': 'Upgrade Mining Laser to lvl 2', '8': 'Complete 2 Successful Trades'}   
    missions = load_data('missions')

    mission_name = mission_list.get(mission_id)
    if mission_name and not missions[mission_name]['completed']:
        missions[mission_name]['accepted'] = True
        save_data('missions', missions)
        print(f"{Fore.GREEN}Mission '{mission_name}' accepted.{Fore.WHITE}")
        time.sleep(2)
    else:
        print("Mission either doesn't exist or is already completed.")
        time.sleep(1)

def update_mission_progress(mission_name, progress_increment):
    missions = load_data('missions')

    # Only update if the mission is accepted and not completed
    if mission_name in missions and missions[mission_name]['accepted'] and not missions[mission_name]['completed']:
        missions[mission_name]['progress'] += progress_increment
        save_data('missions', missions)

        # Check if mission is complete
        if mission_name == 'Mine 100 Materials' and missions[mission_name]['progress'] >= 100:
            complete_mission(mission_name)
        elif mission_name == 'Defeat 1 Enemy' and missions[mission_name]['progress'] >= 1:
            complete_mission(mission_name)
        elif mission_name == 'Defeat 3 Enemies' and missions[mission_name]['progress'] >= 3:
            complete_mission(mission_name)
        elif mission_name == 'Trade 200 Materials With a Ship' and missions[mission_name]['progress'] >= 200:
            complete_mission(mission_name)
        elif mission_name == 'Defeat 5 Enemies' and missions[mission_name]['progress'] >= 5:
            complete_mission(mission_name)
        elif mission_name == 'Explore 3 New Systems' and missions[mission_name]['progress'] >= 3:
            complete_mission(mission_name)
        elif mission_name == 'Upgrade Mining Laser to lvl 2' and missions[mission_name]['progress'] >= 1:
            complete_mission(mission_name)
        elif mission_name == 'Complete 2 Sucessful Trades' and missions[mission_name]['progress'] >= 2:
            complete_mission(mission_name)
    else:
        print()


def complete_mission(mission_name):
    mission_rewards = {'Mine 100 Materials': 100, 'Defeat 1 Enemy': 100, 'Defeat 3 Enemies': 150, 'Deliver 200 Materials to a Trading Post': 125, 'Defeat 5 Enemies': 250, 'Explore 3 New Systems': 125, 'Upgrade Mining Laser to lvl 2': 225, 'Complete 2 Sucessful Trades': 300}
    missions = load_data('missions')
    coins = load_data('parsteel')

    if not missions[mission_name]['completed']:
        missions[mission_name]['completed'] = True
        missions[mission_name]['accepted'] = False
        reward = mission_rewards[mission_name]
        coins += reward
        save_data('missions', missions)
        save_data('parsteel', coins)
        print(f"{Fore.GREEN}Mission '{mission_name}' completed! You earned {reward} parsteel.{Fore.WHITE}")
        time.sleep(2)
        
def display_missions():
    # Load mission data from JSON
    mission_data = load_data('missions')

    if mission_data is None:
        print("No missions available.")
        return

    print("Current Missions:")

    for mission_name, mission_info in mission_data.items():
        # Check mission status
        if mission_info["accepted"]:
            status = "Accepted"
            progress = mission_info["progress"]
            progress_message = f"Progress: {progress}"  # Or use the actual number if more detailed
        else:
            status = "Not Accepted"
            progress_message = "Progress: N/A"

        if mission_info["completed"]:
            status = "Completed"
            progress_message = "Progress: 100%"  # If completed, progress is 100%

        # Print mission information
        print(f"{Fore.BLUE}{mission_name}: {Fore.GREEN}{status} - {Fore.YELLOW}{progress_message}{Fore.WHITE}")


        
def load_explored(system):
    if load_data('explored')[system] == 1:
        return 1
    elif load_data('explored')[system] == 2:
        return 2
    
def save_explored(system):
    systems1 = load_data('explored')
    
    if systems1 is None:
        return
    
    if system in systems1:
        systems1[system] = 1
    else:
        return
    
    save_data('explored', systems1)
        
def battle_stat(opponent_health, opponent_name, income, accuracy, firepower, evasion):
    global damdelt
    print(f'{Fore.YELLOW}You are attacking the {opponent_name}! This ship has {opponent_health} health, and if you win, you get {income} materials.{Fore.WHITE}')
    print(f"{Fore.YELLOW}YELLOW ALERT{Fore.WHITE}")
    print(f"{Fore.BLUE}Your ship stats:\nFirepower: {load_ship_stat(ship_name=load_data('ship'), stat_key='firepower')}\nAccuracy: {load_ship_stat(ship_name=load_data('ship'), stat_key='accuracy')}\nEvasion: {load_ship_stat(ship_name=load_data('ship'), stat_key='evasion')}{Fore.WHITE}")
    print(f"{Fore.YELLOW}Enemy ships stats:\nFirepower: {firepower}\nAccuracy: {accuracy}\nEvasion: {evasion}{Fore.WHITE}")
    if ask('Do you want to battle this enemy? '):
        clear()
        print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
        while load_ship_stat(ship_name=load_data('ship'), stat_key='health') > 0 or opponent_health > 0:
            clear
            turn = 'player'
            if turn == 'player':
                if random.uniform(0, 1) < (load_ship_stat(ship_name=load_data('ship'), stat_key='accuracy') / evasion + 1):
                    damage = load_ship_stat(ship_name=load_data('ship'), stat_key='firepower') * random.uniform(50, 200)  # Random damage variation
                    opponent_health -= damage
                    print(f"{Fore.GREEN}Enemy Hit! {opponent_name} took {damage:.2f} damage. Enemy health: {opponent_health:.2f}{Fore.WHITE}")
                    time.sleep(3)
                    turn = 'enemy'
                else:
                    print(f"{Fore.RED}You missed!{Fore.RED}")
                    time.sleep(2)
                    turn = 'enemy'
            if load_ship_stat(ship_name=load_data('ship'), stat_key='health') <= 0:
                break
            if opponent_health <= 0:
                break
            if turn == 'enemy':
                if random.uniform(0, 1) < (accuracy / (load_ship_stat(ship_name=load_data('ship'), stat_key='accuracy') + 1)):
                    damage = firepower * random.uniform(50, 150)
                    save_ship_data(stat_key='health', value=round(load_ship_stat(ship_name=load_data('ship'), stat_key='health') - damage), ship_name=load_data('ship'))
                    print(f"{Fore.RED}You have been hit! You took {damage:.2f} damage. Your health: {load_ship_stat(ship_name=load_data('ship'), stat_key='health'):.2f}{Fore.WHITE}")
                    time.sleep(3)
                    turn = 'player'
                else:
                    print(f"{Fore.GREEN}{opponent_name} missed!{Fore.WHITE}")
                    time.sleep(2)
                    turn = 'player'
            if load_ship_stat(ship_name=load_data('ship'), stat_key='health') <= 0:
                break
            if opponent_health <= 0:
                break
    if load_ship_stat(stat_key='health', ship_name=load_data('ship')) <= 0:
            clear()
            print(f"{Fore.RED}Ship {load_data('ship')} has been destroyed!{Fore.WHITE}")
            print(f"{Fore.RED}Materials Lost: {load_ship_stat(ship_name=load_data('ship'), stat_key='parsteel_storage') + load_ship_stat(ship_name=load_data('ship'), stat_key='tritanium_storage') + load_ship_stat(ship_name=load_data('ship'), stat_key='dilithium_storage')}{Fore.WHITE}")
            save_ship_data(ship_name=load_data('ship'), stat_key='parsteel_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='tritanium_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='dilithium_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_storage'))
            save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
            save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
            if load_data('ship') == 'Stargazer':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=2)
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            if load_data('ship') == 'USS Grissom':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=4)
                save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
                save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            if load_data('ship') == 'Federation Shuttlecraft':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=3)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=4)
                save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
                save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            if load_data('ship') == 'Galaxy Class':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=5)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=6)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=5)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=4)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=8)
                save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
                save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            time.sleep(5)
            return
    if opponent_health <= 0:
                clear()
                print(f'{Fore.GREEN}You Win!{Fore.WHITE}')
                print(f'{Fore.BLUE}Parsteel Gained: {Fore.WHITE}', income)
                print(f'{Fore.BLUE}Dilithium Gained: {Fore.WHITE}', (income/2))
                save_ship_data(ship_name=load_data('ship'), stat_key='parsteel_storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='parsteel_storage') + income)
                save_ship_data(ship_name=load_data('ship'), stat_key='dilithium_storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='dilithium_storage') + (income/2))
                time.sleep(3)
        
def homescreen_setup():
     print(f"{Fore.YELLOW}Parsteel:{Fore.WHITE} {load_data('parsteel')} || {Fore.GREEN}Tritanium:{Fore.WHITE} {load_data('tritanium')} || {Fore.CYAN}Dilithium:{Fore.WHITE} {load_data('dilithium')} || {Fore.YELLOW}Latnium:{Fore.WHITE} {load_data('latnium')} || {Fore.LIGHTBLUE_EX}Current Ship:{Fore.WHITE} {load_data('ship')} || {Fore.LIGHTBLUE_EX}Current System:{Fore.WHITE} {systems[load_data('current_system')]} || {Fore.BLUE}Health:{Fore.WHITE} {load_ship_stat(ship_name=load_data('ship'), stat_key='health')}/{load_ship_stat(ship_name=load_data('ship'), stat_key='max_health')} || {Fore.GREEN}Storage Avalible:{Fore.WHITE} {load_ship_stat(ship_name=load_data('ship'), stat_key='storage')}/{load_ship_stat(ship_name=load_data('ship'), stat_key='max_storage')}")

def mining_deposit_parsteel(parsteel_mine_num):
    income_display()
    print('You have approached a Parsteel Mine!')
    deposit_materials = get_material_in_node(system_name=systems[load_data('current_system')], mine_name=parsteel_mine_num)
    mining_efficiency = load_ship_stat(ship_name=load_data('ship'), stat_key='mining_efficiency') 
    deposit_var = deposit_materials / mining_efficiency 

    print(f'{Fore.BLUE}This mine has', deposit_materials, f'parsteel.{Fore.WHITE}')
    print(f'{Fore.GREEN}Estimated mining time:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')
    if ask(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}'):
        mine_depo_mats = ask_sanitize(f'{Fore.GREEN}How much would you like to mine? (1 - {deposit_materials}){Fore.WHITE}')
        start_time = time.time()
        while mine_depo_mats or get_material_in_node(system_name=systems[load_data('current_system')], mine_name=parsteel_mine_num) <= 0:
            clear()
            print('Mining...')
            print('Parsteel Remaining:', mine_depo_mats)
            print('Total Storage Remaining:', load_ship_stat(ship_name=load_data('ship'), stat_key='storage'))

            materials_gathered = 1 * mining_efficiency
            save_ship_data(ship_name=load_data('ship'), stat_key='parsteel_storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='parsteel_storage') + materials_gathered)
            save_ship_data(ship_name=load_data('ship'), stat_key='storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='storage') - materials_gathered)
            update_mission_progress('Mine 100 Materials', materials_gathered)
            mine_depo_mats -= mining_efficiency
            
            elapsed_time = time.time() - start_time
            deposit_var = mine_depo_mats
            estimated_time_remaining = (deposit_var / mining_efficiency) * 0.5
            update_materials(system_name=systems[load_data('current_system')], mine_name=parsteel_mine_num, amount=mining_efficiency)
            
            print(f'{Fore.GREEN}Estimated Time remaining:', estimated_time_remaining, f'Seconds {Fore.WHITE}')
            time.sleep(0.5)
            if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') < 0:
                clear()
                print(f'{Fore.RED}Your ship has run out of storage. Please return to drydock to empty your cargo to your station.{Fore.WHITE}')
                time.sleep(2)
                break
            continue

def mining_deposit_tritanium(tritanium_mine_num):
    income_display()
    print('You have approached a Tritanium Mine!')
    deposit_materials = get_material_in_node(system_name=systems[load_data('current_system')], mine_name=tritanium_mine_num)
    mining_efficiency = load_ship_stat(ship_name=load_data('ship'), stat_key='mining_efficiency') 
    deposit_var = deposit_materials / mining_efficiency 

    print(f'{Fore.BLUE}This mine has', deposit_materials, f'tritanium.{Fore.WHITE}')
    print(f'{Fore.GREEN}Estimated mining time:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')
    if ask(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}'):
        mine_depo_mats = ask_sanitize(f'{Fore.GREEN}How much would you like to mine? (1 - {deposit_materials}){Fore.WHITE}')
        start_time = time.time()
        while mine_depo_mats or get_material_in_node(system_name=systems[load_data('current_system')], mine_name=tritanium_mine_num) <= 0:
            clear()
            print('Mining...')
            print('Tritanium Remaining:', mine_depo_mats)
            print('Total Storage Remaining:', load_ship_stat(ship_name=load_data('ship'), stat_key='storage'))

            materials_gathered = 1 * mining_efficiency
            save_ship_data(ship_name=load_data('ship'), stat_key='tritanium_storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='tritanium_storage') + materials_gathered)
            save_ship_data(ship_name=load_data('ship'), stat_key='storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='storage') - materials_gathered)
            update_mission_progress('Mine 100 Materials', materials_gathered)
            mine_depo_mats -= mining_efficiency
            
            elapsed_time = time.time() - start_time
            deposit_var = mine_depo_mats
            estimated_time_remaining = (deposit_var / mining_efficiency) * 0.5
            update_materials(system_name=systems[load_data('current_system')], mine_name=tritanium_mine_num, amount=mining_efficiency)
            
            print(f'{Fore.GREEN}Estimated Time remaining:', estimated_time_remaining, f'Seconds {Fore.WHITE}')
            time.sleep(0.5)
            if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') < 0:
                clear()
                print(f'{Fore.RED}Your ship has run out of storage. Please return to drydock to empty your cargo to your station.{Fore.WHITE}')
                time.sleep(2)
                break
            continue

def mining_deposit_dilithium(dilithium_mine_num):
    income_display()
    print('You have approached a Dilithium Mine!')
    deposit_materials = get_material_in_node(system_name=systems[load_data('current_system')], mine_name=dilithium_mine_num)
    mining_efficiency = load_ship_stat(ship_name=load_data('ship'), stat_key='mining_efficiency') 
    deposit_var = deposit_materials / mining_efficiency 

    print(f'{Fore.BLUE}This mine has', deposit_materials, f'dilithium.{Fore.WHITE}')
    print(f'{Fore.GREEN}Estimated mining time:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')
    if ask(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}'):
        mine_depo_mats = ask_sanitize(f'{Fore.GREEN}How much would you like to mine? (1 - {deposit_materials}){Fore.WHITE}')
        start_time = time.time()
        while mine_depo_mats or get_material_in_node(system_name=systems[load_data('current_system')], mine_name=dilithium_mine_num) <= 0:
            clear()
            print('Mining...')
            print('Dilithium Remaining:', mine_depo_mats)
            print('Total Storage Remaining:', load_ship_stat(ship_name=load_data('ship'), stat_key='storage'))

            materials_gathered = 1 * mining_efficiency
            save_ship_data(ship_name=load_data('ship'), stat_key='dilithium_storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='dilithium_storage') + materials_gathered)
            save_ship_data(ship_name=load_data('ship'), stat_key='storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='storage') - materials_gathered)
            update_mission_progress('Mine 100 Materials', materials_gathered)
            mine_depo_mats -= mining_efficiency
            
            elapsed_time = time.time() - start_time
            deposit_var = mine_depo_mats
            estimated_time_remaining = (deposit_var / mining_efficiency) * 0.5
            update_materials(system_name=systems[load_data('current_system')], mine_name=dilithium_mine_num, amount=mining_efficiency)
            
            print(f'{Fore.GREEN}Estimated Time remaining:', estimated_time_remaining, f'Seconds {Fore.WHITE}')
            time.sleep(0.5)
            if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') < 0:
                clear()
                print(f'{Fore.RED}Your ship has run out of storage. Please return to drydock to empty your cargo to your station.{Fore.WHITE}')
                time.sleep(2)
                break
            continue
        
def accept_missions():
    mission_selection = ask_sanitize('Select mission to accept: ')
    if mission_selection == 1:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('1')
                else:
                    return
    if mission_selection == 2:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('2')
                else:
                        return
    if mission_selection == 3:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('3')
                else:
                        return
    if mission_selection == 4:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('4')
                else:
                        return
    if mission_selection == 5:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('5')
                else:
                        return
    if mission_selection == 6:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('6')
                else:
                        return
    if mission_selection == 7:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('7')
                else:
                        return
    if mission_selection == 8:
                if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('8')
                else:
                        return
    if mission_selection == len(mission_list_print) + 1:
                return
    return

def scan_system():
    exploration_time = random.randint(10, 60)
    if ask(f"{Fore.RED}System {systems[load_data('current_system')]} has not been explored. Would you like to scan this system? This will take you {exploration_time} seconds. (Y/N): {Fore.WHITE}"):
        while exploration_time > 0:
            clear()
            income_display()
            print(f"{Fore.GREEN}Scanning {systems[load_data('current_system')]}...{Fore.WHITE}")
            print(f"{Fore.YELLOW}Time Remaining: {exploration_time}{Fore.WHITE}")
            exploration_time -= 0.5
            time.sleep(0.5)
        print(f"{Fore.GREEN}Scan complete! You may now navigate the system.{Fore.WHITE}")
        save_explored(systems[load_data('current_system')])
        time.sleep(2)


def trading(dil_trade_am, tri_trade_am, par_trade_am):
        income_display()
        print('Avalible Items:')
        avalible = [f"Trade {dil_trade_am} Dilithium for {tri_trade_am} Tritanium", f"Trade {par_trade_am} Parsteel for {tri_trade_am} Tritanium", f"Trade {tri_trade_am} Tritanium for {par_trade_am} Parsteel", f"Trade {par_trade_am} Parsteel for {dil_trade_am} Dilithium"]
        for i, option in enumerate(avalible, 1):  # Start enumeration at 1
            print(f"{i}. {option}")
        print(f"{len(avalible) + 1}. Exit")
        trade_input = ask_sanitize(f"Option: ")
        if trade_input == 1 and (load_ship_stat(load_data('ship'), 'dilithium_storage') > dil_trade_am or load_data('dilithium') > dil_trade_am):
            if ask(f"{Fore.YELLOW}You are going to trade {dil_trade_am} dilithium for {tri_trade_am} tritanium. Are you sure you want to do this? (Y/N): {Fore.WHITE}"):
                if load_ship_stat(load_data('ship'), 'dilithium_storage') > dil_trade_am:
                    save_ship_data(load_data('ship'), 'dilithium_storage',load_ship_stat(load_data('ship'), 'dilithium_storage') - dil_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
                else:
                    save_data('dilithium', load_data('dilithium') - dil_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
            else:
                print('Trade Canceled.')
                time.sleep(1)
                return
        elif trade_input == 2 and (load_ship_stat(load_data('ship'), 'parsteel_storage') > par_trade_am or load_data('parsteel') > par_trade_am):
            if ask(f"{Fore.YELLOW}You are going to trade {par_trade_am} parsteel for {tri_trade_am} tritanium. Are you sure you want to do this? (Y/N): {Fore.WHITE}"):
                if load_ship_stat(load_data('ship'), 'parsteel_storage') > par_trade_am:
                    save_ship_data(load_data('ship'), 'parsteel_storage',load_ship_stat(load_data('ship'), 'parsteel_storage') - par_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
                else:
                    save_data('parsteel', load_data('parsteel') - par_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
            else:
                print('Trade Canceled.')
                time.sleep(1)
                return
        elif trade_input == 3 and (load_ship_stat(load_data('ship'), 'tritanium_storage') > tri_trade_am or load_data('tritanium') > tri_trade_am):
            if ask(f"{Fore.YELLOW}You are going to trade {tri_trade_am} tritanium for {par_trade_am} parsteel. Are you sure you want to do this? (Y/N): {Fore.WHITE}"):
                if load_ship_stat(load_data('ship'), 'tritanium_storage') > tri_trade_am:
                    save_ship_data(load_data('ship'), 'tritanium_storage',load_ship_stat(load_data('ship'), 'tritanium_storage') - tri_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
                else:
                    save_data('tritanium', load_data('tritanium') - tri_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
            else:
                print('Trade Canceled.')
                time.sleep(1)
                return
        elif trade_input == 4 and (load_ship_stat(load_data('ship'), 'parsteel_storage') > dil_trade_am or load_data('parsteel') > dil_trade_am):
            if ask(f"{Fore.YELLOW}You are going to trade {par_trade_am} parsteel for {dil_trade_am} dilithium. Are you sure you want to do this? (Y/N): {Fore.WHITE}"):
                if load_ship_stat(load_data('ship'), 'parsteel_storage') > par_trade_am:
                    save_ship_data(load_data('ship'), 'parsteel_storage',load_ship_stat(load_data('ship'), 'parsteel_storage') - par_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
                else:
                    save_data('parsteel', load_data('parsteel') - par_trade_am)
                    print(f"{Fore.GREEN}Trade Completed.{Fore.WHITE}")
                    time.sleep(2)
                    return
            else:
                print('Trade Canceled.')
                time.sleep(1)
                return
        elif trade_input == 5:
            print('Exiting Trade.')
            time.sleep(1)
            return
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

    warp_range = load_ship_stat(ship_name=load_data('ship'), stat_key='warp_range')
    max_system = len(systems)  

    reachable_systems = {
        key: value for key, value in systems.items()
        if load_data('current_system') - warp_range <= key <= warp_range
    }

    print(f"{Fore.BLUE}You are currently in {systems[load_data('current_system')]}{Fore.WHITE}")

    if ask(f'{Fore.BLUE}Would you like to navigate to another system? {Fore.WHITE}'):
        clear()
        print(f'{Fore.BLUE}Systems in Warp Range:{Fore.WHITE}')
        for key, value in reachable_systems.items():
            print(f'{key}: {value}')
        
        while True:
            try:
                system_number = int(input(f'{Fore.BLUE}Which system number would you like to travel to? {Fore.WHITE}'))
                if system_number in reachable_systems:
                    target_system = system_number
                    warp_time = abs(load_data('current_system') - target_system) * 10
                    print(f'{Fore.RED}Traveling to {reachable_systems[target_system]}. Estimated time: {warp_time} seconds.{Fore.WHITE}')
                    time.sleep(1)
                    for i in range(warp_time):
                        clear()
                        print(f'{Fore.BLUE}Warping... Time Remaining: {warp_time - i}{Fore.WHITE}')
                        time.sleep(1)
                    save_data('current_system', target_system)
                    print(f"Arrived at {systems[load_data('current_system')]}.")
                    time.sleep(2)
                    break
                else:
                    print(f'{Fore.RED}Invalid system number. Please choose a number from the list.{Fore.WHITE}')
            except ValueError:
                print(f'{Fore.RED}Please enter a valid number.{Fore.WHITE}')
    else:
        return False


# Global player reputation
player_reputation = load_data('reputation')  # Starts neutral, range from 0 (hostile) to 100 (friendly)

def ship_reply(choice, ship_type, progress):
    global player_reputation

    # Define possible dialogue based on progression and player choices
    if choice == 1:  # "Greet the ship"
        if ship_type == "friendly":
            clear()
            income_display()
            progress['greeted'] = True
            return "Hello, traveler! How can we assist you today?"
        elif ship_type == "neutral":
            if progress['greeted']:
                clear()
                income_display()
                return "We’ve already exchanged greetings. What do you want?"
            else:
                progress['greeted'] = True
                clear()
                income_display()
                return "Greetings. Do not cause trouble."
        else:
            if progress['greeted']:
                clear()
                income_display()
                return "Still trying to talk? We are not interested!"
            else:
                clear()
                income_display()
                progress['greeted'] = True
                return "Your pleasantries are useless here!"
    
    elif choice == 2:  # "Ask to trade"
        if ship_type == "friendly":
            clear()
            income_display()
            trading(dil_trade_am=random.randint(10, 100), tri_trade_am=random.randint(10, 100), par_trade_am=random.randint(10, 100))
            return "Glad to trade with you!"
        elif ship_type == "neutral":
            if progress['greeted']:
                clear()
                income_display()
                trading(dil_trade_am=random.randint(10, 100), tri_trade_am=random.randint(10, 100), par_trade_am=random.randint(10, 100))
                return "We're neutral, but we might trade."
            else:
                clear()
                income_display()
                return "We are not traders. Move along."
        else:
            clear()
            income_display()
            return "We do not deal with your kind."

    elif choice == 3:  # "Request help"
        if ship_type == "friendly":
            clear()
            income_display()
            return "We can offer assistance. What do you need?"
        elif ship_type == "neutral":
            if progress['greeted']:
                clear()
                income_display()
                return "We are neutral. You should seek help elsewhere."
            else:
                clear()
                income_display()
                return "You didn’t greet us, and now you need help?"
        else:
            clear()
            income_display()
            return "Help? From us? Prepare to be attacked!"
    
    elif choice == 4:  # "Leave the ship"
        if ship_type == "friendly":
            clear()
            income_display()
            return "Safe travels, friend."
        else:
            clear()
            income_display()
            return "Good choice. Stay away."

    return "That choice does not seem to apply here."


def hailing_frequency():
    global player_reputation

    ship_types = ["friendly", "neutral", "hostile"]
    current_ship = random.choice(ship_types)  # Randomize the type of ship encountered
    hailing = True
    clear()
    income_display()

    print(f"{Fore.GREEN}Hailing frequency opened. You've encountered a {current_ship} ship.{Fore.WHITE}")
    
    # Reputation affects initial ship behavior
    if current_ship == "hostile" and player_reputation > 70:
        current_ship = "neutral"
        print("This hostile ship recognizes your reputation and is neutral for now.")
        time.sleep(2)

    # Track conversation progress
    progress = {
        'greeted': False,
        'traded': False,
        'help_requested': False,
    }
    
    while hailing:
        player_reputation = load_data('reputation')

        # Present dialogue options to the player
        print("\nWhat would you like to say?")
        print("1. Greet the ship")
        print("2. Ask to trade")
        print("3. Request help")
        print("4. Leave the ship")
        print("5. Exit the conversation")

        # Get player's choice as an integer
        try:
            choice = int(input("\nSelect an option by entering the number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 5:
            print("Hailing frequency closed.")
            time.sleep(2)
            hailing = False
            break

        if choice in [1, 2, 3, 4]:
            npc_reply = ship_reply(choice, current_ship, progress)
            print(f"{Fore.YELLOW}Ship: {npc_reply}{Fore.WHITE}")

            # Build up events based on choices
            if choice == 1 and progress['greeted'] and current_ship == "friendly":
                print("The ship is beginning to trust you.")
                player_reputation += 5
                save_data('reputation', player_reputation)

            elif choice == 2 and current_ship == "neutral" and progress['greeted']:
                print(f"The neutral ship is considering trading with you.")
                player_reputation += 5
                save_data('reputation', player_reputation)

            elif choice == 3 and current_ship == "friendly" and not progress['help_requested']:
                print("The friendly ship offers help.")
                progress['help_requested'] = True
                player_reputation += 10
                save_data('reputation', player_reputation)

            elif choice == 4 and current_ship == "hostile":
                player_reputation += 10
                save_data('reputation', player_reputation)
                print(f"{Fore.GREEN}Your peaceful withdrawal improved your reputation.{Fore.WHITE}")
                print(f"Current Reputation: {player_reputation}")
            else:
                print(f"Current Reputation: {player_reputation}")
        else:
            print("Invalid option. Please select a number between 1 and 5.")

def load_building_data(key, building_name=None):
    try:
        with open('buildings.json', 'r') as file:
            data = json.load(file)

        if building_name:  # If building_name is specified, return that specific building's data
            if building_name in data['buildings']:
                return data['buildings'][building_name]
            else:
                print(f"Building '{building_name}' not found in buildings data.")
                return None
        else:  # If no building_name is specified, return the whole 'buildings' section
            return data.get(key, None)
        
    except FileNotFoundError:
        print("Buildings data file not found.")
        return None
    except KeyError as e:
        print(f"Key '{key}' not found in buildings data.")
        return None

def save_building_data(key, value, building_name=None):
    try:
        with open('buildings.json', 'r+') as file:
            data = json.load(file)

            if building_name:  # Update a specific building's data
                if building_name in data['buildings']:
                    data['buildings'][building_name][key] = value
                else:
                    print(f"Building '{building_name}' not found in buildings data.")
                    return
            else:  # Update general data (if necessary)
                data[key] = value

            # Rewind file pointer and write updated data
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            print(f"Data for {building_name if building_name else 'buildings'} saved successfully.")

    except FileNotFoundError:
        print("Buildings data file not found.")


def start_construction(building_name, completion_time, upgrade_part=None):
    user_data = load_data('construction_queue')

    # Check if the construction queue is empty
    if user_data['building'] is None:
        current_time = datetime.now()
        start_time = current_time.isoformat()  # Record start time
        end_time = (current_time + timedelta(seconds=completion_time)).isoformat()  # Record end time

        # Update the construction queue in user data
        construction_data = {
            'building': building_name,
            'start_time': start_time,
            'end_time': end_time
        }
        save_data('construction_queue', construction_data)

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
    construction_data = load_data('construction_queue')
    
    if construction_data['building'] is not None and construction_data['end_time'] is not None:
        # Convert the end_time string to a datetime object
        end_time = datetime.fromisoformat(construction_data['end_time'])
        current_time = datetime.now()

        # Check if the current time is greater than or equal to the end time
        if current_time >= end_time:
            building_name = construction_data['building']
            upgrade_part = construction_data.get('upgrade_part', None)  # Get the upgrade part if it exists
            
            print(f"{Fore.GREEN}Construction of {building_name} is complete!{Fore.WHITE}")

            if upgrade_part:
                apply_upgrade(building_name, upgrade_part)  # Apply the specific upgrade

            # Reset the construction queue to null after completion
            save_data('construction_queue', {
                'building': None,
                'start_time': None,
                'end_time': None,
                'upgrade_part': None  # Reset the upgrade part
            })
            
            time.sleep(2)  # Optional: wait for a moment before continuing the game loop

        else:
            # Calculate remaining time
            remaining_time = (end_time - current_time).total_seconds()
            print(f"{Fore.YELLOW}Construction in progress. Time remaining: {round(remaining_time)} seconds.{Fore.WHITE}")
    else:
        print(f"{Fore.RED}No construction is in progress.{Fore.WHITE}")


# Function to apply the upgrade
def apply_upgrade(building_name, upgrade_part):
    # Load the current buildings data from buildings.json
    buildings_data = load_building_data('buildings')  # Loading the buildings data from buildings.json
    
    if building_name in buildings_data['buildings']:
        building = buildings_data['buildings'][building_name]
        
        # Check if the upgrade part exists in the building
        if upgrade_part in building['upgrades']:
            current_level = building['upgrades'][upgrade_part]
            new_level = current_level + 1  # Increase the upgrade level by 1
            
            # Update the building's upgrade level
            building['upgrades'][upgrade_part] = new_level
            print(f"Upgrade '{upgrade_part}' for {building_name} is now at level {new_level}.")
            
            # Save the updated building data back to buildings.json
            save_building_data('upgrades', building['upgrades'], building_name)  # Save only the updates
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
            base_rate = 10  # Base rate of production per minute (can be customized per building)
            
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

def calculate_production(upgrade_level):
    base_rate = 10  # The base production rate per minute for level 1
    production_rate = base_rate * upgrade_level
    return production_rate

def background_production():
    global last_production_time
    last_production_time = load_data('last_production_time')

    # Get the current time
    current_time = datetime.now()

    # Check if last_production_time is empty (""), and if so, set it to the current time
    if load_data('last_production_time') == "":
        last_production_time = current_time.isoformat()
        save_data('last_production_time', last_production_time)
        print("Last production time was empty. Setting to current time.")

    # Calculate the time difference since the last production update
    last_production_time_obj = datetime.fromisoformat(last_production_time)
    time_diff = current_time - last_production_time_obj

    # Check if 1 minute (or your desired interval) has passed
    if time_diff >= timedelta(minutes=1):
        # Load saved storage values (check if there's any saved material)
        parsteel_storage = load_data('parsteel_storage') or 0
        tritanium_storage = load_data('tritanium_storage') or 0
        dilithium_storage = load_data('dilithium_storage') or 0

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
        save_data('parsteel_storage', parsteel_storage)
        save_data('tritanium_storage', tritanium_storage)
        save_data('dilithium_storage', dilithium_storage)

        # Save the current time as the last production time
        last_production_time = current_time.isoformat()
        save_data('last_production_time', last_production_time)


def claim_resources():
    # Load stored materials and actual materials from user data
    parsteel_storage = load_data('parsteel_storage') or 0
    tritanium_storage = load_data('tritanium_storage') or 0
    dilithium_storage = load_data('dilithium_storage') or 0

    parsteel = load_data('parsteel') or 0
    tritanium = load_data('tritanium') or 0
    dilithium = load_data('dilithium') or 0

    # Add stored materials to the actual resources
    parsteel += parsteel_storage
    tritanium += tritanium_storage
    dilithium += dilithium_storage

    # Save the updated resources back to user data
    save_data('parsteel', parsteel)
    save_data('tritanium', tritanium)
    save_data('dilithium', dilithium)

    # Reset the storage to 0
    save_data('parsteel_storage', 0)
    save_data('tritanium_storage', 0)
    save_data('dilithium_storage', 0)

    print(f"{Fore.GREEN}All rescources have been claimed. Parsteel claimed: {parsteel_storage} | Tritanium claimed: {tritanium_storage} | Dilithium claimed: {dilithium_storage}{Fore.WHITE}")


finding_var = 0
warp_time = 0

clear()
mission_list_print = ['1: Mine 100 Materials', '2: Defeat 1 Enemy', '3: Defeat 3 Enemies', '4: Trade 200 Materials With a Ship', '5: Defeat 5 Enemies', '6: Explore 3 New Systems', '7: Upgrade Mining Laser to lvl 2', '8: Complete 2 Successful Trades']

current_dir = os.path.dirname(os.path.realpath(__file__))

requirements_path = os.path.join(current_dir, 'requirements.txt')

print("Checking package requirements...")
try:
    subprocess.check_output([sys.executable, "-m", "pip", "install", "-r", requirements_path])
except subprocess.CalledProcessError:
    input('Something went wrong with PIP. Press enter to exit program...')
    sys.exit(1)

print('Necessary packages imported')

while True:
    if load_ship_stat(stat_key='health', ship_name=load_data('ship')) <= 0:
            clear()
            print(f"{Fore.RED}Ship {load_data('ship')} has been destroyed!{Fore.WHITE}")
            print(f"{Fore.RED}Materials Lost: {load_ship_stat(ship_name=load_data('ship'), stat_key='parsteel_storage') + load_ship_stat(ship_name=load_data('ship'), stat_key='tritanium_storage') + load_ship_stat(ship_name=load_data('ship'), stat_key='dilithium_storage')}{Fore.WHITE}")
            save_ship_data(ship_name=load_data('ship'), stat_key='parsteel_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='tritanium_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='dilithium_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_storage'))
            save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
            save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
            if load_data('ship') == 'Stargazer':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=2)
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            if load_data('ship') == 'USS Grissom':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=4)
                save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
                save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            if load_data('ship') == 'Federation Shuttlecraft':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=1)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=3)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=2)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=4)
                save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
                save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            if load_data('ship') == 'Galaxy Class':
                save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                save_ship_data(ship_name=load_data('ship'), stat_key='firepower', value=5)
                save_ship_data(ship_name=load_data('ship'), stat_key='accuracy', value=6)
                save_ship_data(ship_name=load_data('ship'), stat_key='evasion', value=5)
                save_ship_data(ship_name=load_data('ship'), stat_key='mining_efficiency', value=4)
                save_ship_data(ship_name=load_data('ship'), stat_key='warp_range', value=8)
                save_ship_data(ship_name=load_data('ship'), stat_key='owned', value='false')
                save_ship_data(ship_name=load_data('ship'), stat_key='equipped', value='false')
                save_data('ship', 'Stargazer')
                save_ship_data(ship_name='Stargazer', stat_key='owned', value='true')
                save_ship_data(ship_name='Stargazer', stat_key='equipped', value='true')
            time.sleep(5)
            continue
    clear()
    homescreen_setup()
    check_construction_completion()
    background_production()
    print('What would you like to do?')
    OpList = [f"1: Explore {systems[load_data('current_system')]}", "2: Navigate to Another System", "3: Return to Drydock", "4: Display Missions"]
    print(*OpList, sep = '\n')
    option = ask_sanitize_lobby(question_ask='Option: ', valid_options=[1, 2, 3, 4])
    time.sleep(0.1)
    if (option == 1):
        clear()
        if load_data('current_system') == 1:
            if load_explored(systems[load_data('current_system')]) == 1:
                system_findings = ['1. Parsteel Mine', '2. Mission Planet', '3. Orion Pirate']
                income_display()
                print(f"What would you like to navigate to in {systems[load_data('current_system')]}?")
                print(*system_findings, sep='\n')
                current_system_rand = ask_sanitize('Option: ')
                if current_system_rand == 1:
                    if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') > 0:
                        clear()
                        rand_min = ['parsteel_mine1', 'parsteel_mine2', 'parsteel_mine3', 'parsteel_mine4', 'parsteel_mine5']
                        mining_deposit_parsteel(parsteel_mine_num=random.choice(rand_min))
                    else:
                        clear()
                        income_display()
                        print(f'{Fore.RED}You do not have enouh storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')
                if current_system_rand == 3:
                    clear()
                    income_display()
                    print('You have approached an Orion Pirate!')
                    print('What do you want to do?')
                    op_1 = ['1: Attack the Ship', '2: Hail the Ship'] #hail the ship
                    print(*op_1, sep='\n')
                    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
                    if ori_ship == 1:
                        battle_stat(opponent_health=random.randint(500,900), opponent_name='Orion Pirate', firepower=1, accuracy=1, evasion=1, income=((system_deltas['Enemy Ships Loot'] ** load_data('current_system')) * random.randint(100,250)))
                        update_mission_progress('Defeat 1 Enemy', 1)
                        update_mission_progress('Defeat 3 Enemies', 1)
                        update_mission_progress('Defeat 5 Enemies', 1)
                    if ori_ship == 2:
                        hailing_frequency()
                if current_system_rand == 2:
                    clear()
                    income_display()
                    print('You have approached a Mission Planet!')
                    print(*mission_list_print, sep = '\n')
                    print(f"{len(mission_list_print) + 1}: Exit")
                    accept_missions()
            elif load_explored(systems[load_data('current_system')]) == 2:
                income_display()
                scan_system()
        if load_data('current_system') == 2: # vulcan dev
            if load_explored(systems[load_data('current_system')]) == 1:
                system_findings = ['1. Parsteel Mine', '2. Mission Planet', '3. Orion Pirate', '4. Tritanium Mine']
                income_display()
                print(f"What would you like to navigate to in {systems[load_data('current_system')]}?")
                print(*system_findings, sep='\n')
                current_system_rand = ask_sanitize('Option: ')
                if current_system_rand == 1:
                    if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') > 0:
                        clear()
                        rand_min = ['parsteel_mine1', 'parsteel_mine2', 'parsteel_mine3']
                        mining_deposit_parsteel(parsteel_mine_num=random.choice(rand_min))
                    else:
                        clear()
                        income_display()
                        print(f'{Fore.RED}You do not have enouh storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')
                if current_system_rand == 4:
                    if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') > 0:
                        clear()
                        rand_min = ['tritanium_mine1', 'tritanium_mine2', 'tritanium_mine3']
                        mining_deposit_tritanium(tritanium_mine_num=random.choice(rand_min))
                    else:
                        clear()
                        income_display()
                        print(f'{Fore.RED}You do not have enouh storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')
                if current_system_rand == 3:
                    clear()
                    income_display()
                    print('You have approached an Orion Pirate!')
                    print('What do you want to do?')
                    op_1 = ['1: Attack the Ship', '2: Ignore the Ship'] #hail the ship
                    print(*op_1, sep='\n')
                    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
                    if ori_ship == 1:
                        battle_stat(opponent_health=random.randint(500,900), opponent_name='Orion Pirate', firepower=1, accuracy=1, evasion=1, income=((system_deltas['Enemy Ships Loot'] ** load_data('current_system')) * random.randint(100,250)))
                        update_mission_progress('Defeat 1 Enemy', 1)
                        update_mission_progress('Defeat 3 Enemies', 1)
                        update_mission_progress('Defeat 5 Enemies', 1)
                    if ori_ship == -2:
                        print('Hailing Frequencys are in development.')
                if current_system_rand == 2:
                    clear()
                    income_display()
                    print('You have approached a Mission Planet!')
                    print(*mission_list_print, sep = '\n')
                    print(f"{len(mission_list_print) + 1}: Exit")
                    accept_missions()
            elif load_explored(systems[load_data('current_system')]) == 2:
                income_display()
                scan_system()
        if load_data('current_system') == 3: # tellar dev
            if load_explored(systems[load_data('current_system')]) == 1:
                system_findings = ['1. Dilithium Mine', '2. Mission Planet', '3. Orion Pirate', '4. Tritanium Mine']
                income_display()
                print(f"What would you like to navigate to in {systems[load_data('current_system')]}?")
                print(*system_findings, sep='\n')
                current_system_rand = ask_sanitize('Option: ')
                if current_system_rand == 1:
                    if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') > 0:
                        clear()
                        rand_min = ['dilithium_mine1', 'dilithium_mine2', 'dilithium_mine3', 'dilithium_mine4']
                        mining_deposit_dilithium(dilithium_mine_num=random.choice(rand_min))
                    else:
                        clear()
                        income_display()
                        print(f'{Fore.RED}You do not have enouh storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')
                if current_system_rand == 4:
                    if load_ship_stat(ship_name=load_data('ship'), stat_key='storage') > 0:
                        clear()
                        rand_min = ['tritanium_mine1', 'tritanium_mine2']
                        mining_deposit_tritanium(tritanium_mine_num=random.choice(rand_min))
                    else:
                        clear()
                        income_display()
                        print(f'{Fore.RED}You do not have enouh storage to mine. Please return to drydock and empty your storage.{Fore.WHITE}')
                if current_system_rand == 3:
                    clear()
                    income_display()
                    print('You have approached an Orion Pirate!')
                    print('What do you want to do?')
                    op_1 = ['1: Attack the Ship', '2: Ignore the Ship'] #hail the ship
                    print(*op_1, sep='\n')
                    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
                    if ori_ship == 1:
                        battle_stat(opponent_health=random.randint(500,900), opponent_name='Orion Pirate', firepower=2, accuracy=2, evasion=3, income=((system_deltas['Enemy Ships Loot'] ** load_data('current_system')) * random.randint(100,250)))
                        update_mission_progress('Defeat 1 Enemy', 1)
                        update_mission_progress('Defeat 3 Enemies', 1)
                        update_mission_progress('Defeat 5 Enemies', 1)
                    if ori_ship == -2:
                        print('Hailing Frequencys are in development.')
                if current_system_rand == 2:
                    clear()
                    income_display()
                    print('You have approached a Mission Planet!')
                    print(*mission_list_print, sep = '\n')
                    print(f"{len(mission_list_print) + 1}: Exit")
                    accept_missions()
            elif load_explored(systems[load_data('current_system')]) == 2:
                income_display()
                scan_system()
    if (option == 2):
        navigate()
    if option == 3:
        if ask(f"{Fore.RED}Are you sure you want to travel back to Sol? (Y/N) {Fore.WHITE}"):
            warp_time = abs(load_data('current_system') - 1) * 10
            time.sleep(warp_time)
            clear()
            save_data('parsteel', (load_data('parsteel') + load_ship_stat(ship_name=load_data('ship'), stat_key='parsteel_storage')))
            save_data('tritanium', (load_data('tritanium') + load_ship_stat(ship_name=load_data('ship'), stat_key='tritanium_storage')))
            save_data('dilithium', (load_data('dilithium') + load_ship_stat(ship_name=load_data('ship'), stat_key='dilithium_storage')))
            save_ship_data(ship_name=load_data('ship'), stat_key='parsteel_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='tritanium_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='dilithium_storage', value=0)
            save_ship_data(ship_name=load_data('ship'), stat_key='storage', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_storage'))
            income_display()
            save_data('current_system', 1)
            drydock_option = ['1: Enter Station', '2: Enter Shipyard', '3: Open Research', '4: Repair Ship', '5: Exit']
            print(f"{Fore.RED}The Station is currently not functional.{Fore.WHITE}")
            print(*drydock_option, sep='\n')
            drydock_selection = ask_sanitize('Option: ')
            if drydock_selection == 1: #Enter station
                clear()
                income_display()
                station_options = ['1: Enter Generators', '2: Enter Shipyard', '3: Enter R&D Department', '4: Enter Academy', '5: Enter Ops', '6: Exit']
                print(*station_options, sep='\n')
                station_selection = ask_sanitize('Option: ')
                if station_selection == 1:
                    clear()
                    income_display()
                    print('Generator Menu')
                    print('1. Claim all generator material\n2. Upgrade Generators')
                    generator_option = ask_sanitize("Option: ")
                    if generator_option == 1:
                        claim_resources()
                        time.sleep(2)
                    if generator_option == 2:
                        start_construction('generators', 10, 'Mining Speed')
            if drydock_selection == 2: #Shipyard
                clear()
                income_display()
                ship_management_menu(coins=load_data('parsteel'))
            #rest of station code
            if drydock_selection == 4:
                clear()
                income_display()
                if ask(f"{Fore.RED}Are you sure you want to repair your ship? This will cost you {round((load_ship_stat(ship_name=load_data('ship'), stat_key='max_health') - load_ship_stat(ship_name=load_data('ship'), stat_key='health')) / 5)} parsteel. (Y/N): "):
                    save_data('parsteel', load_data('parsteel') - round((load_ship_stat(ship_name=load_data('ship'), stat_key='max_health') - load_ship_stat(ship_name=load_data('ship'), stat_key='health')) / 5))
                    save_ship_data(ship_name=load_data('ship'), stat_key='health', value=load_ship_stat(ship_name=load_data('ship'), stat_key='max_health'))
                    print(f"{Fore.GREEN}Repair Completed. You now have {load_ship_stat(load_data('ship'), 'health')} health.{Fore.WHITE}")
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
    if option == 800:
        clear()
        with open('user_crew_data.json', 'r') as file:
            data = json.load(file)
        for crew_member in data["crew"]:
            print("- " + crew_member["name"])
        manifest_option = ask_sanitize(question_ask='Would you like to view crew stats (1) or upgrade crew (2) or exit (3)? ')
        if manifest_option == 1:
            clear()
            for crew_member in data["crew"]:
                print(f"- {crew_member['name']}'s Stats:")
                for key, value in crew_member.items():
                    print(f"  {key.capitalize()}: {value}")
                print() 
            if ask(question='Type Y or N to exit: '):
                continue
            continue
        elif manifest_option == 2:
            if __name__ == "__main__":
                main()
        elif manifest_option == 3:
            clear()
            continue
        continue