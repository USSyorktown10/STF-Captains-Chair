import json
import time
import random
import os
from colorama import Fore
import subprocess
import sys

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

shuttle_bays = 1
original_crew_file_path = 'crew_list.json'
user_crew_file_path = 'user_crew_data.json'
user_game_file_path = 'user_game_data.json'
ship_selection_default = 'ship_selection_default.json'

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
        with open('user_game_data.json', 'r') as file:
            data = json.load(file)
        # Traverse nested dictionaries if necessary
        if key in data:
            return data[key]
        elif key in data['upgrades']:
            return data['upgrades'][key]
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
        with open('user_game_data.json', 'r+') as file:
            data = json.load(file)  # Read existing data

            # Update the key or nested key
            if key in data:
                data[key] = value
            elif 'upgrades' in data and key in data['upgrades']:
                data['upgrades'][key] = value
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
        with open('ship_selection_default.json', 'r+') as file:
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
        with open('ship_selection_default.json', 'r') as file:
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
        with open('ship_selection_default.json', 'r') as file:
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
        with open('ship_selection_default.json', 'r+') as file:
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
        with open('user_game_data.json', 'r+') as user_file:
            user_data = json.load(user_file)
            
            # Load available ships data
            with open('ship_selection_default.json', 'r') as ship_file:
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
        with open('ship_selection_default.json', 'r+') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name and ship.get('owned', False):
                    if ship_name == 'Galaxy Class':
                        upgrade_cost = 150
                    else:
                        upgrade_cost = 50
                    if load_data('coins') >= upgrade_cost:
                        ship[stat] += 1
                        save_data('coins', load_data('coins') - upgrade_cost)
                        print(f"{Fore.GREEN}{ship_name}'s {stat} has been upgraded to {ship[stat]}.{Fore.WHITE}")
                        time.sleep(2)
                    else:
                        print(f"{Fore.RED}Not enough coins to upgrade {stat}.{Fore.WHITE}")
                        time.sleep(2)

                    break

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    except FileNotFoundError:
        print("Ship data file not found.")
    
    return load_data('coins')

def equip_ship(ship_name):
    try:
        with open('ship_selection_default.json', 'r+') as file:
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
        with open('ship_selection_default.json', 'r+') as file:
            data = json.load(file)

            for ship in data['ship selection']:
                if ship['name'] == ship_name and not ship['owned']:
                    current_coins = load_data('coins')
                    if ship_name == 'Galaxy Class':
                        price = 1500
                    elif ship_name == 'Federation Shuttlecraft':
                        price = 150
                    elif ship_name == 'USS Grissom':
                        price = 100
                    else:
                        price = 100
                    if ask(f"{Fore.RED}Are you sure you want to buy this ship? It costs {price} coins ({load_data('coins')}->{load_data('coins') - price}): {Fore.WHITE}"):
                        if current_coins >= price:
                            clear()
                            ship['owned'] = True
                            save_data('coins', current_coins - price)
                            print(f"{Fore.GREEN}You have purchased {ship_name}.{Fore.WHITE}")
                            time.sleep(2)
                        else:
                            print("Not enough coins to buy this ship.")
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
        with open('ship_selection_default.json', 'r') as file:
            data = json.load(file)

        for ship in data['ship selection']:
            if ship['name'] == ship_name:
                print(f"{Fore.BLUE}{ship_name}{Fore.WHITE}")
                print(f"Firepower: {ship['firepower']}")
                print(f"Accuracy: {ship['accuracy']}")
                print(f"Evasion: {ship['evasion']}")
                print(f"Antimatter: {ship['antimatter']}")
                print(f"Storage: {ship['storage']}")
                print(f"Owned: {ship['owned']}")
                if ask('Type Y or N to exit: '):
                    return


        print(f"Ship '{ship_name}' not found.")
    except FileNotFoundError:
        print("Ship data file not found.")

def display_ship_menu():
    try:
        with open('ship_selection_default.json', 'r') as file:
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

        choice = ask_sanitize(question_ask="\nOptions:\n1. View Ship Details\n2. Buy Ship\n3. Equip Ship\n4. Upgrade Ship\n5. Exit\nSelect an option: ")

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
            ship_num = ask_sanitize(question_ask='What ship would you like to buy? ')
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
            ship_num = ask_sanitize(question_ask='What ship would you like to equip? ')
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

        print(f"\nCurrent coins: {coins}\n")

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

    if load_data('coins') >= cost:
        crew_data['crew'][member_index]['skill_level'] += 5  # Increase skill level
        save_data('coins', load_data('coins') - cost)
        print(f"{Fore.GREEN}\n{crew_data['crew'][member_index]['name']}'s skill level increased to {crew_data['crew'][member_index]['skill_level']}!{Fore.WHITE}")
        print(f"{Fore.YELLOW}Remaining Coins: {load_data('coins')}{Fore.WHITE}")
        time.sleep(2)
    else:
        print(f"{Fore.RED}\nNot enough coins to upgrade.{Fore.WHITE}")
        time.sleep(2)

# Main function
def main():
    global game_state
    game_state = initialize_game_data()
    crew_data = initialize_crew_data()
    
    display_crew(crew_data)

    choice = int(input(f"{Fore.BLUE}\nEnter the number of the crew member to upgrade: {Fore.WHITE}")) - 1  # Convert to 0-based index

    cost = 10
    print(f"{Fore.YELLOW}Upgrading {crew_data['crew'][choice]['name']} will cost {cost} coins.{Fore.WHITE}")
    if ask(f"{Fore.RED}Do you want to proceed? (y/n): {Fore.WHITE}"):
        upgrade_crew_member(game_state, crew_data, choice, cost)
        save_crew_data(user_crew_file_path, crew_data)  # Save updated user crew data to file
        print("\nGame data and crew data saved.")
    else:
        print(f"{Fore.RED}\nUpgrade canceled.{Fore.WHITE}")
        time.sleep(1)

def income_display():
     print(f'{Fore.YELLOW}Coins:{Fore.WHITE}', load_data('coins'))
     print(f'{Fore.GREEN}Materials:{Fore.WHITE}', load_data('materials'))
     print(f"{Fore.BLUE}Health:{Fore.WHITE} {load_data('health')}/{load_data('max_health')}")
     print(f"{Fore.CYAN}Current System:{Fore.WHITE} {systems[load_data('current_system')]}")
     print(f"{Fore.LIGHTBLUE_EX}Current Ship:{Fore.WHITE} {load_data('ship')}")

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
    mission_list = {'1': 'Mine 100 Materials', '2': 'Defeat 1 Enemy', '3': 'Defeat 3 Enemies', '4': 'Deliver 200 Materials to a Trading Post', '5': 'Defeat 5 Enemies', '6': 'Explore 3 New Systems', '7': 'Upgrade Mining Laser to lvl 2', '8': 'Complete 2 Successful Trades'}   
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
        elif mission_name == 'Deliver 200 Materials to a Trading Post' and missions[mission_name]['progress'] >= 200:
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
    mission_rewards = {'Mine 100 Materials': 25, 'Defeat 1 Enemy': 25, 'Defeat 3 Enemies': 45, 'Deliver 200 Materials to a Trading Post': 30, 'Defeat 5 Enemies': 55, 'Explore 3 New Systems': 30, 'Upgrade Mining Laser to lvl 2': 50, 'Complete 2 Sucessful Trades': 60}
    missions = load_data('missions')
    coins = load_data('coins')

    if not missions[mission_name]['completed']:
        missions[mission_name]['completed'] = True
        missions[mission_name]['accepted'] = False
        reward = mission_rewards[mission_name]
        coins += reward
        save_data('missions', missions)
        save_data('coins', coins)
        print(f"{Fore.GREEN}Mission '{mission_name}' completed! You earned {reward} coins.{Fore.WHITE}")
        time.sleep(2)
        
def battle_stat(opponent_health, opponent_name, income, accuracy, firepower, evasion):
    global damdelt
    print(f'{Fore.YELLOW}You are attacking the {opponent_name}! This ship has {opponent_health} health, and if you win, you get {income} materials.{Fore.WHITE}')
    print(f"{Fore.YELLOW}YELLOW ALERT{Fore.WHITE}")
    print(f"{Fore.BLUE}Your ship stats:\nFirepower: {load_ship_stat(ship_name=load_data('ship'), stat_key='firepower')}\nAccuracy: {load_ship_stat(ship_name=load_data('ship'), stat_key='accuracy')}\nEvasion: {load_ship_stat(ship_name=load_data('ship'), stat_key='evasion')}{Fore.WHITE}")
    print(f"{Fore.YELLOW}Enemy ships stats:\nFirepower: {firepower}\nAccuracy: {accuracy}\nEvasion: {evasion}{Fore.WHITE}")
    if ask('Do you want to battle this enemy? '):
        clear()
        print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
        while load_data('health') > 0 or opponent_health > 0:
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
            if load_data('health') <= 0:
                break
            if opponent_health <= 0:
                break
            if turn == 'enemy':
                if random.uniform(0, 1) < (accuracy / (load_ship_stat(ship_name=load_data('ship'), stat_key='accuracy') + 1)):
                    damage = firepower * random.uniform(50, 150)
                    save_data('health', round(load_data('health') - damage))
                    print(f"{Fore.RED}You have been hit! You took {damage:.2f} damage. Your health: {load_data('health'):.2f}{Fore.WHITE}")
                    time.sleep(3)
                    turn = 'player'
                else:
                    print(f"{Fore.GREEN}{opponent_name} missed!{Fore.WHITE}")
                    time.sleep(2)
                    turn = 'player'
            if load_data('health') <= 0:
                break
            if opponent_health <= 0:
                break
    if load_data('health') <= 0:
                clear()
                print(f'{Fore.RED}You Lose!{Fore.WHITE}')
                print(f"{Fore.RED}Coins Lost: {load_data('coins')}{Fore.WHITE}")
                print(f"{Fore.RED}Materials Lost: {load_data('materials')}{Fore.WHITE}")
                save_data('coins', 0)
                save_data('materials', 0)
                save_data('ship', 'Stargazer')
                save_data('health', load_data('max_health'))
                exit()
    if opponent_health <= 0:
                clear()
                print(f'{Fore.GREEN}You Win!{Fore.WHITE}')
                print(f'{Fore.BLUE}Materials Gained: {Fore.WHITE}', income)
                save_data('materials', load_data('materials') + income)
                time.sleep(3)
        
def homescreen_setup():
     print(f'{Fore.YELLOW}Coins:{Fore.WHITE}', load_data('coins'))
     print(f'{Fore.GREEN}Materials:{Fore.WHITE}', load_data('materials'))
     print(f"{Fore.BLUE}Health:{Fore.WHITE} {load_data('health')}/{load_data('max_health')}")
     print(f"{Fore.CYAN}Current System:{Fore.WHITE} {systems[load_data('current_system')]}")
     print(f"{Fore.LIGHTBLUE_EX}Current Ship:{Fore.WHITE} {load_data('ship')}")
     

def mining_deposit():
    global materials
    income_display()
    print('You have approached a Material Cluster!')
    time.sleep(1)
    deposit_materials = ((system_deltas['Material Cluster'] * load_data('current_system')) * random.randint(10, 1000))
    mining_efficiency = load_data('upgrades')['Mining Laser'] 
    deposit_var = deposit_materials / mining_efficiency 

    print(f'{Fore.BLUE}This mine has', deposit_materials, f'resources.{Fore.WHITE}')
    print(f'{Fore.GREEN}Estimated mining time:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')

    if ask(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}'):
        start_time = time.time()
        for i in range(round(deposit_materials)):
            clear()
            print('Mining...')
            print('Materials Remaining:', deposit_materials)
            print('Total Materials:', load_data('materials'))

            materials_gathered = 0.5 * mining_efficiency
            save_data('materials', load_data('materials') + materials_gathered)
            update_mission_progress('Mine 100 Materials', materials_gathered)
            deposit_materials -= mining_efficiency
            
            elapsed_time = time.time() - start_time
            deposit_var = deposit_materials
            estimated_time_remaining = (deposit_var / mining_efficiency) * 0.5
            
            print(f'{Fore.GREEN}Estimated Time remaining:', estimated_time_remaining, f'Seconds {Fore.WHITE}')
            time.sleep(0.5)
            if deposit_materials <= 0:
                break
            continue

def trading_post():
    global coins
    global materials
    income_display()
    print('You have approached a Trading Post!')
    time.sleep(1)
    if ask('Would you like to trade? Y/N: '):
        print('Avalible Items:')
        Avalible = ['1: Sell Materials: 1 coins per 50 materials', '2: Exit']
        print(*Avalible, sep = '\n')
        trade = ask_sanitize(question_ask='Option: ')
        if trade == 1:
            clear()
            if load_data('materials') >= 50:
                while load_data('materials') >= 50:
                    save_data('materials', load_data('materials') - 50) 
                    save_data('coins', load_data('coins') + 1)
                    update_mission_progress('Deliver 200 Materials to a Trading Post', 50)
                    print('Materials:', load_data('materials'))
                    print('Coins:', load_data('coins'))
                    time.sleep(0.5)
                    clear()
                    continue
                update_mission_progress('Complete 2 Sucessful Trades', 1)
                time.sleep(2)
            else:
                print(f'{Fore.RED}You dont have enough materials to get coins.{Fore.WHITE}')
                time.sleep(1.5)
            if trade == 2:
                time.sleep(0.01)
                
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

    warp_range = load_data('upgrades')['Warp Range']
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

finding_var = 0
warp_time = 0

clear()
mission_list_print = ['1: Mine 100 Materials', '2: Defeat 1 Enemy', '3: Defeat 3 Enemies', '4: Deliver 200 Materials to a Trading Post', '5: Defeat 5 Enemies', '6: Explore 3 New Systems', '7: Upgrade Mining Laser to lvl 2', '8: Complete 2 Successful Trades']

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
    if load_data('health') <= 0:
            clear()
            print(f'{Fore.RED}You Lose!{Fore.WHITE}')
            print(f"{Fore.RED}Coins Lost: {load_data('coins')}{Fore.WHITE}")
            print(f"{Fore.RED}Materials Lost: {load_data('materials')}{Fore.WHITE}")
            save_data('coins', 0)
            save_data('materials', 0)
            save_data('ship', 'Stargazer')
            save_data('health', load_data('max_health'))
            exit()
    clear()
    homescreen_setup()
    print('What would you like to do?')
    OpList = ['1: Stay in Current System', '2: Navigate to Another System', '3: Return to Drydock', '4: Shipyard']
    print(*OpList, sep = '\n')
    option = ask_sanitize_lobby(question_ask='Option: ', valid_options=[1, 2, 3, 4])
    time.sleep(0.1)
    if (option == 1):
        clear()
        if load_data('current_system') == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 10:
            system_findings = ['Material Mine', 'Orion Pirate', 'Trading Post', 'Mission Planet'] # Mission planet
            current_system_rand = random.choice(system_findings)
            if current_system_rand == 'Material Mine':
                mining_deposit()
            if current_system_rand == 'Trading Post':
                trading_post()
            if current_system_rand == 'Orion Pirate':
                income_display()
                print('You have approached an Orion Pirate!')
                time.sleep(1)
                print('What do you want to do?')
                op_1 = ['1: Attack the Ship', '2: Ignore the Ship'] #hail the ship
                print(*op_1, sep='\n')
                ori_ship = ask_sanitize(question_ask='What would you like to do: ')
                if ori_ship == 1:
                    if load_data('current_system') == 1:
                        battle_stat(opponent_health=random.randint(500,900), opponent_name='Orion Pirate', firepower=1, accuracy=1, evasion=1, income=((system_deltas['Enemy Ships Loot'] ** load_data('current_system')) * random.randint(100,250)))
                        update_mission_progress('Defeat 1 Enemy', 1)
                        update_mission_progress('Defeat 3 Enemies', 1)
                        update_mission_progress('Defeat 5 Enemies', 1)
                    else:
                        battle_stat(opponent_health=((system_deltas['Enemy Ships Health'] ** load_data('current_system')) * random.randint(500,900)), opponent_name='Orion Pirate', firepower=(1 * (system_deltas['Enemy Ships Health'] ** load_data('current_system'))), accuracy=(1 * (system_deltas['Enemy Ships Health'] ** load_data('current_system'))), evasion=(1 * (system_deltas['Enemy Ships Health'] ** load_data('current_system'))), income=((system_deltas['Enemy Ships Loot'] ** load_data('current_system')) * random.randint(100,250)))
                        update_mission_progress('Defeat 1 Enemy', 1)
                        update_mission_progress('Defeat 3 Enemies', 1)
                        update_mission_progress('Defeat 5 Enemies', 1)
                if ori_ship == -2:
                    print('Hailing Frequencys are in development.')
            if current_system_rand == 'Mission Planet':
                clear()
                income_display()
                print('You have approached a Mission Planet!')
                time.sleep(1)
                print(*mission_list_print, sep = '\n')
                print(f"{len(mission_list_print) + 1}: Exit")
                mission_selection = ask_sanitize('Select mission to accept: ')
                if mission_selection == 1:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('1')
                    else:
                        continue
                if mission_selection == 2:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('2')
                    else:
                        continue
                if mission_selection == 3:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('3')
                    else:
                        continue
                if mission_selection == 4:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('4')
                    else:
                        continue
                if mission_selection == 5:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('5')
                    else:
                        continue
                if mission_selection == 6:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('6')
                    else:
                        continue
                if mission_selection == 7:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('7')
                    else:
                        continue
                if mission_selection == 8:
                    if ask(f'{Fore.YELLOW}Are you sure you want to accept this mission?{Fore.WHITE}'):
                        accept_mission('8')
                    else:
                        continue
                if mission_selection == len(mission_list_print) + 1:
                    continue
                continue
        if load_data('current_system') == 9:
            if ask(f'Would you like to dock with the Xindi Starbase or Explore the system?'):
                clear()
            else:
                system_findings = ['Material Mine', 'Orion Pirate', 'Trading Post'] # Mission planet
                current_system_rand = random.choice(system_findings)
                if current_system_rand == 'Material Mine':
                    mining_deposit()
                if current_system_rand == 'Trading Post':
                    trading_post()
                if current_system_rand == 'Orion Pirate':
                    income_display()
                    print('You have approached an Orion Pirate!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op_1 = ['1: Attack the Ship', '2: Ignore the Ship'] #hail the ship
                    print(*op_1, sep='\n')
                    ori_ship = ask_sanitize(question_ask='What would you like to do: ')
                if ori_ship == 1:
                    battle_stat(opponent_health=((system_deltas['Enemy Ships Health'] ** load_data('current_system')) * random.randint(500,900)), opponent_name='Orion Pirate', firepower=(1 * system_deltas['Enemy Ships Health']), accuracy=(1 * system_deltas['Enemy Ships Health']), evasion=(1 * system_deltas['Enemy Ships Health']), income=((system_deltas['Enemy Ships Loot'] ** load_data('current_system')) * random.randint(100,250)))
                    update_mission_progress('Defeat 1 Enemy', 1)
                    update_mission_progress('Defeat 3 Enemies', 1)
                    update_mission_progress('Defeat 5 Enemies', 1)
                if ori_ship == -2:
                    print('Hailing Frequencys are in development.')
    if (option == 2):
        navigate()
    if option == 3:
        clear()
        print("Drydock")
        drydock_option = ['1: Upgrade Mining Laser', '2: Upgrade Health', '3: Upgrade Warp Range', '4: View Upgrades', '5: Restore Health', '6: Exit']
        print(*drydock_option, sep = '\n')
        drydock_option_2 = ask_sanitize(question_ask='What would you like to upgrade: ')
        if drydock_option_2 == 1:
            upgrade(type='Mining Laser')
            update_mission_progress('Upgrade Mining Laser to lvl 2', 1)
        elif drydock_option_2 == 2:
            upgrade(type='Health')
        elif drydock_option_2 == 4:
            view_upgrades()
        elif drydock_option_2 == 3:
            upgrade(type='Warp Range')
        elif drydock_option_2 == 5:
            current_heal_cost = load_data('health') / load_data('max_health')
            current_heal_cost = current_heal_cost * 10
            if load_data('coins') >= current_heal_cost:
                print(f"{Fore.YELLOW}You are healing your ship from {load_data('health')} to {load_data('max_health')}.\n {Fore.RED}This upgrade will cost you {current_heal_cost} coins. ({load_data('coins')} -> {round(load_data('coins') - current_heal_cost)}){Fore.WHITE}")
                if ask(f"{Fore.RED}Are you sure you want to continue?{Fore.WHITE} "):
                    save_data('coins', round(load_data('coins') - current_heal_cost))
                    save_data('health', load_data('max_health'))
                    continue
                continue
            else: 
                print(f"{Fore.YELLOW}You can't heal your ship because you don't have enough coins (current: {load_data('coins')}, required: {current_heal_cost}).{Fore.WHITE}")
                continue
            continue
        elif drydock_option_2 == 6:
            continue
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
    if option == 4:
        clear()
        income_display()
        ship_management_menu(coins=load_data('coins'))