import time
import random
import os
from colorama import Fore
upgrades = {"Mining Laser": 0, "Health": 0, "Phaser": 0}  # this is a dictionary
costs = {"Mining Laser": 15, "Health": 10, "Phaser": 20}  # the costs
deltas = {"Mining Laser": 1.5, "Health": 2, "Phaser": 2}  # the amount to multiply by for each level, to make the higher levels cost more

coins = 100  # pretend we start with money

def ask(question):
        response = input(question)
        return response.lower() in ["y", "yes", "sure"]  # lol

def upgrade(type):
        current_upgrade_level = upgrades[type]
        current_upgrade_cost = costs[type] * (deltas[type] **  current_upgrade_level)  # ** = raise to the power of, this multiplies the base cost by the delta the number of upgrade times
        if coins >= current_upgrade_cost:  # Can we afford it?
                print(f"{Fore.YELLOW}You are upgrading your {type} from level {current_upgrade_level} to {current_upgrade_level + 1}.\n {Fore.RED}This upgrade will cost you {current_upgrade_cost} coinss. ({coins} -> {coins - current_upgrade_cost}){Fore.WHITE} ")
                if ask(f"{Fore.BOLD+Fore.RED}Are you sure you want to continue?{Fore.WHITE} "):  # extra space so it looks nicer
                        coins -= current_upgrade_cost  # take the cost away
                        upgrades[type] += 1   # actually upgrade
                        return True  # we did it!
        else:
                print(f"{Fore.YELLOW}You can't upgrade your {type} from level {current_upgrade_level} to {current_upgrade_level + 1} because you don't have enough coinss (current: {coins}, required: {current_upgrade_cost}).{Fore.WHITE}")
                return False

def view_upgrades():
        print(f"{Fore.GREEN}Your upgrades:{Fore.WHITE}\n{'\n'.join([u + ': level '+str(upgrades[u]) for u in upgrades.keys()])}")  # I was tired, OK?

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
def battle(opponent_health, opponent_name, oppenent_damage, income): # This function is not ready yet. This will be avalible soon. The current version you are reading is the version that got rid of the bug where when you buy something, it actually takes away the ammount of money you spent.
    print(f'{Fore.RED}You are attacking the {Fore.WHITE}', opponent_name, f'{Fore.RED} ! This ship has {Fore.WHITE}', opponent_health, f'{Fore.RED} health, and if you win, you get {Fore.WHITE}', income, f'{Fore.RED}.{Fore.WHITE}')
    while health > 0:
        if opponent_health <= 0:
            break
        print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
        print(f'{Fore.BLUE}{opponent_name} health:{Fore.WHITE}', opponent_health)
        print(f'{Fore.GREEN}Your health:{Fore.WHITE}', health)
        time.sleep(0.5)
        print('You are attacking.')
        damage_input = int(input("Pick a number between 1 and 10: "))
        damage_gen = random.randint(1,10)
        close_1 = damage_gen + 1
        close_2 = damage_gen + 2
        close_3 = damage_gen - 1
        close_4 = damage_gen - 2
        if damage_input == damage_gen:
            damdelt = (random.randint(100,200) * phaser_upgrade)
            print('You Hit! Damage Dealt:', damdelt) 
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_1:
            damdelt = (random.randint(50,100) * phaser_upgrade)
            print('You Hit! Damage Dealt:', damdelt) 
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_3:
            damdelt = (random.randint(50,100) * phaser_upgrade)
            print('You Hit! Damage Dealt:', damdelt)
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_2:
            damdelt = (random.randint(25,50) * phaser_upgrade)
            print('You Hit! Damage Dealt:', damdelt)
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damage_input == close_4:
            damdelt = (random.randint(25,50) * phaser_upgrade)
            print('You Hit! Damage Dealt:', damdelt)
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        else:
            print('You Missed!', opponent_name, 'Ships Turn...') 
            damrecieve = random.randint(50,200) * oppenent_damage
            health = health - damrecieve
            time.sleep(0.5)
            print('The ', opponent_name, ' Ship did ', damrecieve, ' Damage!')
            continue
    if health <= 0:
        print(f'{Fore.RED}You Lose!{Fore.WHITE}')
        exit()
    if opponent_health <= 0:
        print(f'{Fore.GREEN}You Win!{Fore.WHITE}')
        print('Materials Gained: ', income)
        materials = materials + income
clear()
mission_list = ['Mission: '] # Missions arent avalible yet and will be ready in v. 0.5
health = 1000
stamina = 100
materials = 5
Win = 0
laser_upgrade = 1
phaser_upgrade = 1
max_health = 1000
health_up = 10
clear()
while True:
    if health <= 0:
        clear()
        print(f'{Fore.RED}Game over!{Fore.WHITE}')
        exit()
    clear()
    print('What would you like to do?')
    OpList = ['1: Explore', '2: Drydock']
    print(*OpList, sep = '\n')
    option = int(input('Option: '))
    time.sleep(0.1)
    if (option == 1):
        clear()
        print('Explore')
        Sectors = ['1: Alpha Sector', '2: Beta Sector', '3: Delta Sector'] #Alpha sector (mining, fed ships, planets and missions, sol) Beta Sector (Kilngon, Romulan, Mining, planet, mission) Delta Sec (Vulcan, mining, planet mission)
        print(*Sectors, sep = '\n')
        choice_sector = int(input('Option: '))
        if (choice_sector == 1):
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            if (selected_item == 'Good'):
                op2 = ['Material Cluster', 'Trading Post', 'Federation Ship'] #, 'Mission Planet'
                selecteditem = random.choice(op2) #
                if (selecteditem == 'Material Cluster'):
                      print('You have approached a Material Cluster!')
                      deposit_materials = random.randint(10,1000)
                      deposit_var = deposit_materials / laser_upgrade
                      time.sleep(1)
                      print('This mine has', deposit_materials, 'rescources.')
                      mine = input('Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: ')
                      if (mine == "y"):
                            for i in range(deposit_materials):
                                clear()
                                print('Mining...')
                                print('Materials Remaining:', deposit_var)
                                print('Total Materials:', materials)
                                deposit_var = deposit_var - laser_upgrade
                                materials = materials + (0.5 * laser_upgrade)
                                time.sleep(0.5)
                            continue
                if (selecteditem == 'Trading Post'):
                      print('You have approached a Trading Post!')
                      time.sleep(1)
                      trade_post = input('Would you like to trade? Y/N: ')
                      if trade_post == 'y':
                          print('Avalible Items:')
                          Avalible = ['1: Laser Upgrade: 10 coinss', '2: Sell Materials: 1 coins per 50 materials', '3: Exit']
                          print(*Avalible, sep = '\n')
                          trade = int(input('Option: '))
                          if trade == 1:
                              clear()
                              if coins > 10:
                                  coins = coins - 10
                                  laser_upgrade = laser_upgrade + 1
                                  print('Laser Upgrade Bought!')
                                  print('Laser Level:', laser_upgrade)
                                  time.sleep(1)
                                  continue
                              else:
                                  print('You dont have enough money to purchase this.')
                                  time.sleep(1)
                                  continue
                          if trade == 2:
                              clear()
                              if materials >= 50:
                                  while materials >= 50:
                                      materials = materials - 50
                                      coins = coins + 1
                                      print('Materials:', materials)
                                      print('coinss:', coins)
                                      time.sleep(0.5)
                                  continue
                              else:
                                print('You dont have enough materials to get coinss.')
                                time.sleep(1)
                                continue
                          if trade == 3:
                                continue
                          continue
                      continue
                if (selecteditem == 'Mission Planet'): # Mission arent avalible yet and will be ready v. 0.5
                    print('You have approached a planet!')
                    time.sleep(1)
                    miss_planet = input('Are you willing to accept a mission? Y/N: ')
                    if miss_planet == 'y':
                        clear()
                        print('Missions Avalible:')
                if (selecteditem == "Federation Ship"):
                    print('You have approached a Federation ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    federation_ship = int(input('Option: '))
                    if federation_ship == 1:
                        battle() #Figuring this out, will be possible soon
                        if federation_ship == -2: #This option will be avalible in v. 0.2 NOTE: Should be 2
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
                      print('You have approached a Material Cluster!')
                      deposit_materials = random.randint(10,1000)
                      deposit_var = deposit_materials / laser_upgrade
                      time.sleep(1)
                      print('This mine has', deposit_materials, 'rescources.')
                      mine = input('Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: ')
                      if (mine == "y"):
                            for i in range(deposit_materials):
                                clear()
                                print('Mining...')
                                print('Materials Remaining:', deposit_var)
                                print('Total Materials:', materials)
                                deposit_var = deposit_var - laser_upgrade
                                materials = materials + (0.5 * laser_upgrade)
                                time.sleep(0.5)
                            continue
                if (selected_item_2 == 'Klingon Ship'):
                    print('You have approached a Klingon ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    kling_ship = int(input('Option: '))
                    if kling_ship == 1:
                        battle()
                if (selected_item_2 == 'Romulan Ship'):
                    print('You have approached a Romulan ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    rom_ship = int(input('Option: '))
                    if rom_ship == 1:
                        battle()
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
            selecteditem3 = random.choice(op3) #
            if (selecteditem3 == 'Material Cluster'):
                      print('You have approached a Material Cluster!')
                      deposit_materials = random.randint(10,1000)
                      deposit_var = deposit_materials / laser_upgrade
                      time.sleep(1)
                      print('This mine has', deposit_materials, 'rescources.')
                      mine = input('Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: ')
                      if (mine == "y"):
                            for i in range(deposit_materials):
                                clear()
                                print('Mining...')
                                print('Materials Remaining:', deposit_var)
                                print('Total Materials:', Materials)
                                deposit_var = deposit_var - laser_upgrade
                                Materials = Materials + (0.5 * laser_upgrade)
                                time.sleep(0.5)
                            continue
            if (selecteditem3 == 'Vulcan Ship'):
                    print('You have approached a Vulcan ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    vulcan_ship = int(input('Option: '))
                    if vulcan_ship == 1:
                        battle()
                        continue
                    continue
            else:
                print('Bad')
                continue
        continue
    if option == 2:
        clear()
        print("Drydock")
        DryOp = ['1: Repair Ship', '2: Upgrade Ship', '3: Check Inventory', '4: Exit']
        ask('What would you like to upgrade?')
    if health < max_health:
        health = health + health_up