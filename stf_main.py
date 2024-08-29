import time
import random
import os
from colorama import Fore
upgrades = {"Mining Laser": 1, "Health": 1, "Phaser": 1}  # this is a dictionary
costs = {"Mining Laser": 15, "Health": 10, "Phaser": 20}  # the costs
deltas = {"Mining Laser": 1.5, "Health": 2, "Phaser": 2}  # the amount to multiply by for each level, to make the higher levels cost more

coins = 100
health = 1000
materials = 5

def income_display():
    print(f'{Fore.YELLOW}Coins:{Fore.WHITE}', coins)
    print(f'{Fore.GREEN}Materials:{Fore.WHITE}', materials)
    print(f'{Fore.BLUE}Health:{Fore.WHITE} {health}/{max_health}')

def ask(question):
        response = input(question)
        return response.lower() in ["y", "yes"]  # lol

def upgrade(type):
        global coins
        current_upgrade_level = upgrades[type]
        current_upgrade_cost = costs[type] * (deltas[type] **  current_upgrade_level)  # ** = raise to the power of, this multiplies the base cost by the delta the number of upgrade times
        if coins >= current_upgrade_cost:  # Can we afford it?
                print(f"{Fore.YELLOW}You are upgrading your {type} from level {current_upgrade_level} to {current_upgrade_level + 1}.\n {Fore.RED}This upgrade will cost you {current_upgrade_cost} coins. ({coins} -> {coins - current_upgrade_cost}){Fore.WHITE} ")
                if ask(f"{Fore.RED}Are you sure you want to continue?{Fore.WHITE} "):  # extra space so it looks nicer
                        coins -= current_upgrade_cost  # take the cost away
                        upgrades[type] += 1   # actually upgrade
                        return True  # we did it!
        else:
                print(f"{Fore.YELLOW}You can't upgrade your {type} from level {current_upgrade_level} to {current_upgrade_level + 1} because you don't have enough coins (current: {coins}, required: {current_upgrade_cost}).{Fore.WHITE}")
                return False

def view_upgrades():
    clear()
    print(f"{Fore.GREEN}Your upgrades:{Fore.WHITE}\n{chr(10).join([u + ': Level '+str(upgrades[u]) for u in upgrades.keys()])}")
    continue_1 = input(f'{Fore.RED}Continue? {Fore.WHITE}')
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
        damage_input = int(input("Pick a number between 1 and 10: "))
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
            print('You Hit! Damage Dealt:', damdelt)
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
     

def mining_deposit():
    global materials
    income_display()
    print('You have approached a Material Cluster!')
    deposit_materials = random.randint(10,1000)
    deposit_var = deposit_materials / upgrades['Mining Laser']
    time.sleep(1)
    print(f'{Fore.BLUE}This mine has', deposit_materials, f'rescources.{Fore.WHITE}')
    print(f'{Fore.GREEN}Estimated mining time:', deposit_var * 0.5, f'Seconds {Fore.WHITE}')
    mine = input(f'{Fore.RED}Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: {Fore.WHITE}')
    if (mine == "y"):
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
    global materials
    income_display()
    print('You have approached a Trading Post!')
    time.sleep(1)
    trade_post = input('Would you like to trade? Y/N: ')
    if trade_post == 'y':
        print('Avalible Items:')
        Avalible = ['1: Sell Materials: 1 coins per 50 materials', '2: Exit']
        print(*Avalible, sep = '\n')
        trade = int(input('Option: '))
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
    
clear()
mission_list = {'1: Mine 100 Materials': 0, '2: Defeat 1 Enemy': 0,}
mission_rewards = {'1: Mine 100 Materials': 25, '2: Defeat 1 Enemy': 25,}
stamina = 100
Win = 0
upgrades['Phaser'] = 1
max_health = 1000
health_up = 10
clear()
while True:
    if health <= 0:
        clear()
        print(f'{Fore.RED}Game over!{Fore.WHITE}')
        exit()
    clear()
    homescreen_setup()
    print('What would you like to do?')
    OpList = ['1: Explore', '2: Drydock']
    print(*OpList, sep = '\n')
    option = int(input('Option: '))
    time.sleep(0.1)
    if (option == 1):
        clear()
        income_display()
        print('Explore')
        Sectors = ['1: Alpha Sector', '2: Beta Sector', '3: Delta Sector'] #Alpha sector (mining, fed ships, planets and missions, sol) Beta Sector (Kilngon, Romulan, Mining, planet, mission) Delta Sec (Vulcan, mining, planet mission)
        print(*Sectors, sep = '\n')
        choice_sector = int(input('Option: '))
        if (choice_sector == 1):
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            if (selected_item == 'Good'):
                op2 = ['Material Cluster', 'Trading Post', 'Raider Ship'] #, 'Mission Planet'
                encounter = random.choice(op2) #
                if (encounter == 'Material Cluster'):
                    mining_deposit()
                if (encounter == 'Trading Post'):
                      trading_post()
                if (encounter == 'Mission Planet'): # Mission arent avalible yet and will be ready v. 0.5
                    income_display()
                    print('You have approached a planet!')
                    time.sleep(1)
                    miss_planet = input('Would you like to veiw the mission list? Y/N: ')
                    if miss_planet == 'y':
                        clear()
                        print('Missions Avalible:')
                        print(*mission_list, sep = '\n')
                        print(f'{len(mission_list)+1}: Exit')
                        int(input('What mission would you like? '))
                if (encounter == "Raider Ship"):
                    income_display()
                    print('You have approached a Raider ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    raid_ship = int(input('Option: '))
                    if raid_ship == 1:
                        battle(opponent_health=random.randint(500,900), opponent_name='Raider Ship', oppenent_damage=1, income=random.randint(100,250))
                        if raid_ship == -2: #This option will be avalible in v. 0.2 NOTE: Should be 2
                            clear()
                            print(f"{Fore.GREEN}Hailing Frequency Open{Fore.WHITE}")
                            hailing = random.randint(1,5)
                            if hailing == 1:
                                clear()
                                print('')
                            time.sleep(0)
                            continue
                        continue
                    continue
                else: #Still trying to figure out what would be bad
                    clear()
                    print('')
            continue
        if choice_sector == 2: #Beta Sector (Kilngon, Romulan, Mining, planet, mission)
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            if selected_item == 'Good':
                op3 = ['Material Cluster', 'Klingon Ship', 'Romulan Ship'] #, 'Mission Planet'
                selected_item_2 = random.choice(op3) #
                if (selected_item_2 == 'Material Cluster'):
                     mining_deposit()
                if (selected_item_2 == 'Klingon Ship'):
                    income_display()
                    print('You have approached a Klingon ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    kling_ship = int(input('Option: '))
                    if kling_ship == 1:
                        battle(opponent_health=random.randint(700,1100), opponent_name='Klingon Ship', oppenent_damage=1.5, income=random.randint(250,300))
                if (selected_item_2 == 'Romulan Ship'):
                    income_display()
                    print('You have approached a Romulan ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    rom_ship = int(input('Option: '))
                    if rom_ship == 1:
                        battle(opponent_health=random.randint(1000,1500), opponent_name='Romulan Ship', oppenent_damage=2, income=random.randint(350,500))
                        continue
                    continue
                else:
                    print('Bad')
                    continue
            continue
        if choice_sector == 3: #Delta Sec (Vulcan, mining, planet mission)
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            op3 = ['Material Cluster', 'Vulcan Ship'] #, 'Mission Planet'
            encounter_3 = random.choice(op3) #
            if (encounter_3 == 'Material Cluster'):
                      mining_deposit()
            if (encounter_3 == 'Vulcan Ship'):
                    income_display()
                    print('You have approached a Vulcan ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    vulcan_ship = int(input('Option: '))
                    if vulcan_ship == 1:
                        battle(opponent_health=random.randint(1000,1600), opponent_name='Vulcan Ship', oppenent_damage=2.5, income=random.randint(450,600))
                        continue
                    continue
            else:
                print('Bad')
                continue
        continue
    if option == 2:
        clear()
        print("Drydock")
        drydock_option = ['1: Upgrade Mining Laser', '2: Upgrade Phaser', '3: Upgrade Health', '4: View Upgrades', '5: Restore Health', '6: Exit']
        print(*drydock_option, sep = '\n')
        drydock_option_2 = int(input('What would you like to upgrade: '))
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