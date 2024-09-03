import json
import time
import random
import os
from colorama import Fore

'''with open('STF_data') as f:
    data = json.load(f)
    print(data)'''

upgrades = {"Mining Laser": 1, "Health": 1, "Phaser": 1}  
costs = {"Mining Laser": 15, "Health": 10, "Phaser": 20}  
deltas = {"Mining Laser": 1.5, "Health": 2, "Phaser": 2}  
systems = {
    1: 'Sol', 
    2: 'Vulcan', 
    3: 'Tellar', 
    4: 'Andor', 
    5: 'Omicron II', 
    6: 'Regula', 
    7: 'Solaria', 
    8: 'Tarkalea XII', 
    9: 'Xindi Starbase 9', 
    10: 'Altor IV'
}

   
coins = 100
health = 1000
materials = 5

'''data = {
    'coins': coins,
    'materials': materials,
    'health': health,
    'upgrades': upgrades,
}

file_name = 'STF_data'

with open(file_name, 'w') as f:
    json.dump(data, f, indent=4)'''
 

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

def income_display():
    print(f'{Fore.YELLOW}Coins:{Fore.WHITE}', coins)
    print(f'{Fore.GREEN}Materials:{Fore.WHITE}', materials)
    print(f'{Fore.BLUE}Health:{Fore.WHITE} {health}/{max_health}')
    print(f'{Fore.CYAN}Current System:{Fore.WHITE} {systems[current_system]}')

def ask(question):
        response = input(question)
        return response.lower() in ["y", "yes"] 

def upgrade(type):
        global coins
        current_upgrade_level = upgrades[type]
        current_upgrade_cost = costs[type] * (deltas[type] **  current_upgrade_level) 
        if coins >= current_upgrade_cost: 
                print(f"{Fore.YELLOW}You are upgrading your {type} from level {current_upgrade_level} to {current_upgrade_level + 1}.\n {Fore.RED}This upgrade will cost you {current_upgrade_cost} coins. ({coins} -> {coins - current_upgrade_cost}){Fore.WHITE} ")
                if ask(f"{Fore.RED}Are you sure you want to continue?{Fore.WHITE} "):  
                        coins -= current_upgrade_cost
                        upgrades[type] += 1   
                        return True  
        else:
                print(f"{Fore.YELLOW}You can't upgrade your {type} from level {current_upgrade_level} to {current_upgrade_level + 1} because you don't have enough coins (current: {coins}, required: {current_upgrade_cost}).{Fore.WHITE}")
                return False

def view_upgrades():
    clear()
    print(f"{Fore.GREEN}Your upgrades:{Fore.WHITE}\n{chr(10).join([u + ': Level '+str(upgrades[u]) for u in upgrades.keys()])}")
    continue_1 = ask(f'{Fore.RED}Continue? {Fore.WHITE}')
    if continue_1 == ('y', 'yes'):
        time.sleep(0.001)

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
        
def battle(opponent_health, opponent_name, oppenent_damage, income): # This function is not ready yet. This will be avalible soon. The current version you are reading is the version that got rid of the bug where when you buy something, it actually takes away the ammount of money you spent.
    global health
    global materials
    print(f'{Fore.YELLOW}You are attacking the {opponent_name}! This ship has {opponent_health} health, and if you win, you get {income} materials.{Fore.WHITE}')
    time.sleep(3)
    while health > 0:
        clear()
        if opponent_health <= 0:
            break
        print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
        print(f'{Fore.BLUE}{opponent_name} health:{Fore.WHITE}', opponent_health)
        print(f'{Fore.GREEN}Your health:{Fore.WHITE}', health)
        print('You are attacking.')
        damage_input = ask_sanitize(question_ask='Pick a number between 1 and 10: ')
        damage_gen = random.randint(1,10)
        close_1 = damage_gen + 1
        close_2 = damage_gen + 2
        close_3 = damage_gen - 1
        close_4 = damage_gen - 2
        if damage_input == damage_gen:
            damdelt = (random.randint(100,200) * upgrades['Phaser'])
            print(f'{Fore.GREEN}You Hit! Damage Dealt: {damdelt}{Fore.WHITE}') 
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_1:
            damdelt = (random.randint(50,100) * upgrades['Phaser'])
            print(f'{Fore.GREEN}You Hit! Damage Dealt: {damdelt}{Fore.WHITE}') 
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_3:
            damdelt = (random.randint(50,100) * upgrades['Phaser'])
            print(f'{Fore.GREEN}You Hit! Damage Dealt: {damdelt}{Fore.WHITE}')
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_2:
            damdelt = (random.randint(25,50) * upgrades['Phaser'])
            print(f'{Fore.GREEN}You Hit! Damage Dealt: {damdelt}{Fore.WHITE}')
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_4:
            damdelt = (random.randint(25,50) * upgrades['Phaser'])
            print(f'{Fore.GREEN}You Hit! Damage Dealt: {damdelt}{Fore.WHITE}')
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        else:
            print(f'{Fore.RED}You Missed! {opponent_name}s Ship Turn...{Fore.WHITE}') 
            damrecieve = random.randint(50,200) * oppenent_damage
            health = health - damrecieve
            time.sleep(1)
            print(f'{Fore.RED}The {opponent_name} Ship did {damrecieve} Damage!{Fore.WHITE}')
            time.sleep(1)
            continue
    if health <= 0:
        clear()
        print(f'{Fore.RED}You Lose!{Fore.WHITE}')
        print(f'{Fore.RED}Coins Lost: {coins}{Fore.WHITE}')
        print(f'{Fore.RED}Materials Lost: {materials}{Fore.WHITE}')
        exit()
    if opponent_health <= 0:
        print(f'{Fore.GREEN}You Win!{Fore.WHITE}')
        print(f'{Fore.BLUE}Materials Gained: {Fore.WHITE}', income)
        materials = materials + income
        time.sleep(2)

def homescreen_setup():
     print(f'{Fore.YELLOW}Coins:{Fore.WHITE}', coins)
     print(f'{Fore.GREEN}Materials:{Fore.WHITE}', materials)
     print(f'{Fore.BLUE}Health:{Fore.WHITE} {health}/{max_health}')
     print(f'{Fore.CYAN}Current System:{Fore.WHITE} {systems[current_system]}')
     

def mining_deposit():
    global materials
    income_display()
    print('You have approached a Material Cluster!')
    deposit_materials = random.randint(10,1000)
    deposit_var = deposit_materials / upgrades['Mining Laser']
    time.sleep(1)
    print(f'{Fore.BLUE}This mine has', deposit_materials, f'rescources.{Fore.WHITE}')
    print(f'{Fore.GREEN}Estimated mining time:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')
    if ask(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}'):
        for i in range(deposit_materials):
            clear()
            print('Mining...')
            print('Materials Remaining:', deposit_var)
            print('Total Materials:', materials)
            deposit_var = deposit_var - upgrades['Mining Laser']
            materials = materials + (0.5 * upgrades['Mining Laser'])
            print(f'{Fore.GREEN}Estimated Time remaining:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')
            time.sleep(0.5)
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
            if materials >= 50:
                while materials >= 50:
                    materials = materials - 50
                    coins = coins + 1
                    print('Materials:', materials)
                    print('coins:', coins)
                    time.sleep(0.5)
                    continue
            else:
                print(f'{Fore.RED}You dont have enough materials to get coins.{Fore.WHITE}')
                time.sleep(1.5)
            if trade == 2:
                time.sleep(0.01)
                
current_system = 1
finding_var = 0
                
def find_system_number(system_name):
    """Find the number associated with the given system name."""
    for key, value in systems.items():
        if value == system_name:
            return key
    return None

def navigate():
    global current_system
    global finding_var
    global system_travel
    global warp_time

    print(f'You are currently in {systems[current_system]}')
    
    if ask(f'Would you like to navigate to another system? '):
        clear()
        print(f'{Fore.BLUE}Systems in Warp Range:{Fore.WHITE}')
        for key, value in systems.items():
            print(f'{key}: {value}')
        
        system_travel = input(f'{Fore.BLUE}Which system would you like to travel to? {Fore.WHITE}')
        found = ''
        for key, value in systems.items():
            if system_travel == value:
                target_system = key
                warp_time = (abs(current_system - target_system)*10) 
                print(f'{Fore.RED}Traveling to {value}. Estimated time: {warp_time} seconds.{Fore.WHITE}')
                time.sleep(1)
                for i in range(warp_time):
                    clear()
                    print(f'{Fore.BLUE}Warping... Time Remaining: {warp_time}{Fore.WHITE}')
                    time.sleep(1)
                    warp_time = warp_time - 1
                current_system = target_system 
                print(f'Arrived at {systems[current_system]}.')
                time.sleep(2)
                found = True
                break
        if not found:
            print(f'{system_travel} is not in the list of systems.')
            time.sleep(2)
        
        return True
    else:
        return False
current_system = 1 
finding_var = 0
warp_time = 0

clear()
mission_list = {'1: Mine 100 Materials': 0, '2: Defeat 1 Enemy': 0,}
mission_rewards = {'1: Mine 100 Materials': 25, '2: Defeat 1 Enemy': 25,}
stamina = 100
Win = 0
upgrades['Phaser'] = 1
max_health = 1000
health_up = 0
clear()
while True:
    if health <= 0:
        clear()
        print(f'{Fore.RED}Game over!{Fore.WHITE}')
        exit()
    clear()
    homescreen_setup()
    print('What would you like to do?')
    OpList = ['1: Stay in Current System', '2: Navigate to Another System', '3: Return to Drydock']
    print(*OpList, sep = '\n')
    option = ask_sanitize(question_ask='What would you like to do: ')
    time.sleep(0.1)
    if (option == 1):
        clear()
        if current_system == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 10:
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
                    battle(opponent_health=random.randint(500,900), opponent_name='Orion Pirate', oppenent_damage=1, income=random.randint(100,250))
                if ori_ship == -2:
                    print('Hailing Frequencys are in development.')
        if current_system == 9:
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
                    battle(opponent_health=random.randint(500,900), opponent_name='Orion Pirate', oppenent_damage=1, income=random.randint(100,250))
                if ori_ship == -2:
                    print('Hailing Frequencys are in development.')
    if (option == 2):
        navigate()
    if option == 3:
        clear()
        print("Drydock")
        drydock_option = ['1: Upgrade Mining Laser', '2: Upgrade Phaser', '3: Upgrade Health', '4: View Upgrades', '5: Restore Health', '6: Exit']
        print(*drydock_option, sep = '\n')
        drydock_option_2 = ask_sanitize(question_ask='What would you like to upgrade: ')
        if drydock_option_2 == 1:
            upgrade(type='Mining Laser')
        elif drydock_option_2 == 2:
            upgrade(type='Phaser')
        elif drydock_option_2 == 3:
            upgrade(type='Health')
        elif drydock_option_2 == 4:
            view_upgrades()
        elif drydock_option_2 == 5:
            current_heal_cost = health / max_health
            current_heal_cost = current_heal_cost * 10
            if coins >= current_heal_cost:
                print(f"{Fore.YELLOW}You are healing your ship from {health} to {max_health}.\n {Fore.RED}This upgrade will cost you {current_heal_cost} coins. ({coins} -> {coins - current_heal_cost}){Fore.WHITE}")
                if ask(f"{Fore.RED}Are you sure you want to continue?{Fore.WHITE} "):
                    coins -= current_heal_cost
                    health = max_health
                    continue
                continue
            else: 
                print(f"{Fore.YELLOW}You can't heal your ship because you don't have enough coins (current: {coins}, required: {current_heal_cost}).{Fore.WHITE}")
                continue
            continue
        elif drydock_option_2 == 6:
            continue
        continue
    if health < max_health:
        health = health + health_up