import time
import random
import os
from colorama import Fore
def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
def battle(opponent_health, opponent_name, oppenent_damage, income): # This function is not ready yet. This will be avalible soon. The current version you are reading is the version that got rid of the bug where when you buy something, it actually takes away the ammount of money you spent.
    print(f'{Fore.RED}You are attacking the {Fore.WHITE}', opponent_name, f'{Fore.RED} ! This ship has {Fore.WHITE}', opponent_health, f'{Fore.RED} health, and if you win, you get {Fore.WHITE}', income, f'{Fore.RED}.{Fore.WHITE}')
    while Health > 0:
        if opponent_health <= 0:
            break
        print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
        print(f'{Fore.BLUE}Federation Health:{Fore.WHITE}', FedHealth)
        print(f'{Fore.GREEN}Your Health:{Fore.WHITE}', Health)
        time.sleep(0.5)
        print('You are attacking.')
        damO = int(input("Pick a number between 1 and 10: "))
        damInt = random.randint(1,10)
        Close1 = damInt + 1
        Close2 = damInt + 2
        Close3 = damInt - 1
        Close4 = damInt - 2
        if damO == damInt:
            damdelt = (random.randint(100,200) * PhaserUpgrade)
            print('You Hit! Damage Dealt:', damdelt) 
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damO == Close1:
            damdelt = (random.randint(50,100) * PhaserUpgrade)
            print('You Hit! Damage Dealt:', damdelt) 
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damO == Close3:
            damdelt = (random.randint(50,100) * PhaserUpgrade)
            print('You Hit! Damage Dealt:', damdelt)
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damO == Close2:
            damdelt = (random.randint(25,50) * PhaserUpgrade)
            print('You Hit! Damage Dealt:', damdelt)
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        elif damO == Close4:
            damdelt = (random.randint(25,50) * PhaserUpgrade)
            print('You Hit! Damage Dealt:', damdelt)
            time.sleep(1)
            opponent_health = opponent_health - damdelt
            continue
        else:
            print('You Missed!', opponent_name, 'Ships Turn...') 
            damrecieve = random.randint(50,200) * oppenent_damage
            Health = Health - damrecieve
            time.sleep(0.5)
            print('The ', opponent_name, ' Ship did ', damrecieve, ' Damage!')
            continue
    if Health <= 0:
        print(f'{Fore.RED}You Lose!{Fore.WHITE}')
        exit()
    if opponent_health <= 0:
        print(f'{Fore.GREEN}You Win!{Fore.WHITE}')
        print('Materials Gained: ', income)
        Materials = Materials + income
clear()
missionlist = ['Mission: '] # Missions arent avalible yet and will be ready in v. 0.5
Coin = 0
Health = 1000
Stamina = 100
Materials = 5
Win = 0
LaserUpgrade = 1
PhaserUpgrade = 1
MaxHealth = 1000
HealthUp = 10
clear()
while True:
    if Health <= 0:
        clear()
        print(f'{Fore.RED}Game over!{Fore.WHITE}')
        exit()
    clear()
    print('What would you like to do?')
    OpList = ['1: Explore', '2: Drydock']
    print(*OpList, sep = '\n')
    Option = int(input('Option: '))
    time.sleep(0.1)
    if (Option == 1):
        clear()
        print('Explore')
        Sectors = ['1: Alpha Sector', '2: Beta Sector', '3: Delta Sector'] #Alpha sector (mining, fed ships, planets and missions, sol) Beta Sector (Kilngon, Romulan, Mining, planet, mission) Delta Sec (Vulcan, mining, planet mission)
        print(*Sectors, sep = '\n')
        ChoiceSector = int(input('Option: '))
        if (ChoiceSector == 1):
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            if (selected_item == 'Good'):
                op2 = ['Material Cluster', 'Trading Post', 'Federation Ship'] #, 'Mission Planet'
                selecteditem = random.choice(op2) #
                if (selecteditem == 'Material Cluster'):
                      print('You have approached a Material Cluster!')
                      DepositMat = random.randint(10,1000)
                      a = DepositMat / LaserUpgrade
                      time.sleep(1)
                      print('This mine has', DepositMat, 'rescources.')
                      mine = input('Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: ')
                      if (mine == "y"):
                            for i in range(DepositMat):
                                clear()
                                print('Mining...')
                                print('Materials Remaining:', a)
                                print('Total Materials:', Materials)
                                a = a - LaserUpgrade
                                Materials = Materials + (0.5 * LaserUpgrade)
                                time.sleep(0.5)
                            continue
                if (selecteditem == 'Trading Post'):
                      print('You have approached a Trading Post!')
                      time.sleep(1)
                      tradepost = input('Would you like to trade? Y/N: ')
                      if tradepost == 'y':
                          print('Avalible Items:')
                          Avalible = ['1: Laser Upgrade: 10 coins', '2: Sell Materials: 1 coin per 50 materials', '3: Exit']
                          print(*Avalible, sep = '\n')
                          trade = int(input('Option: '))
                          if trade == 1:
                              clear()
                              if Coin > 10:
                                  Coin = Coin - 10
                                  LaserUpgrade = LaserUpgrade + 1
                                  print('Laser Upgrade Bought!')
                                  print('Laser Level:', LaserUpgrade)
                                  time.sleep(1)
                                  continue
                              else:
                                  print('You dont have enough money to purchase this.')
                                  time.sleep(1)
                                  continue
                          if trade == 2:
                              clear()
                              if Materials >= 50:
                                  while Materials >= 50:
                                      Materials = Materials - 50
                                      Coin = Coin + 1
                                      print('Materials:', Materials)
                                      print('Coins:', Coin)
                                      time.sleep(0.5)
                                  continue
                              else:
                                print('You dont have enough materials to get coins.')
                                time.sleep(1)
                                continue
                          if trade == 3:
                                continue
                          continue
                      continue
                if (selecteditem == 'Mission Planet'): # Mission arent avalible yet and will be ready v. 0.5
                    print('You have approached a planet!')
                    time.sleep(1)
                    missplanet = input('Are you willing to accept a mission? Y/N: ')
                    if missplanet == 'y':
                        clear()
                        print('Missions Avalible:')
                if (selecteditem == "Federation Ship"):
                    print('You have approached a Federation ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    fedship = int(input('Option: '))
                    if fedship == 1:
                        clear()
                        print('You are attacking the Federation Ship!')
                        time.sleep(1)
                        FedHealth = random.randint(500,1000)
                        b = FedHealth
                        Win = 0
                        while Win == 0:
                            clear()
                            print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
                            print(f'{Fore.BLUE}Federation Health:{Fore.WHITE}', FedHealth)
                            print(f'{Fore.GREEN}Your Health:{Fore.WHITE}', Health)
                            print('(1) Attack or (2) Defend')
                            atordef = int(input('Option: '))
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                exit()
                            if atordef == 1:
                                print('You are Attacking.')
                                damO = int(input("Pick a number between 1 and 10: "))
                                damInt = random.randint(1,10)
                                Close1 = damInt + 1
                                Close2 = damInt + 2
                                Close3 = damInt - 1
                                Close4 = damInt - 2
                                if damO == damInt:
                                    damdelt = (random.randint(100,200) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    FedHealth = FedHealth - damdelt
                                    continue
                                elif damO == Close1:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    FedHealth = FedHealth - damdelt
                                    continue
                                elif damO == Close3:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    FedHealth = FedHealth - damdelt
                                    continue   
                                elif damO == Close2:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    FedHealth = FedHealth - damdelt
                                    continue
                                elif damO == Close4:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    FedHealth = FedHealth - damdelt
                                    continue 
                                else:
                                     print('You Missed! Federation Ship Turn...') 
                                     damrecieve = random.randint(50,200) 
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue
                            if atordef == 2:
                                print('You are defending.')
                                defO = int(input('Pick a number between 1 and 10: '))
                                defInt = random.randint(1,10)
                                Far1 = defInt + 1
                                Far2 = defInt + 2
                                Far3 = defInt - 1
                                Far4 = defInt - 2
                                if defO == defInt:
                                    defdelt = (random.randint(100,200))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far1:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far3:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue   
                                elif defO == Far2:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue  
                                elif defO == Far4:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue 
                                else:
                                     damrecieve = random.randint(100,300)
                                     print('You have been Hit!')  
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue 
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                break
                            if FedHealth <= 0:
                                clear()
                                print(f'{Fore.GREEN}Battle Won!{Fore.WHITE}')
                                Win = 1
                                Coin = Coin + random.randint(10,50)
                                Materials = Materials + random.randint(50,100)
                                Health = Health + random.randint(10,80)
                                time.sleep(1)
                                continue
                        if fedship == -2: #This option will be avalible in v. 0.2 NOTE: Should be 2
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
        if ChoiceSector == 2: #Beta Sector (Kilngon, Romulan, Mining, planet, mission)
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            if selected_item == 'Good':
                op3 = ['Material Cluster', 'Klingon Ship', 'Romulan Ship'] #, 'Mission Planet'
                selecteditem2 = random.choice(op3) #
                if (selecteditem2 == 'Material Cluster'):
                      print('You have approached a Material Cluster!')
                      DepositMat = random.randint(10,1000)
                      a = DepositMat / LaserUpgrade
                      time.sleep(1)
                      print('This mine has', DepositMat, 'rescources.')
                      mine = input('Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: ')
                      if (mine == "y"):
                            for i in range(DepositMat):
                                clear()
                                print('Mining...')
                                print('Materials Remaining:', a)
                                print('Total Materials:', Materials)
                                a = a - LaserUpgrade
                                Materials = Materials + (0.5 * LaserUpgrade)
                                time.sleep(0.5)
                            continue
                if (selecteditem2 == 'Klingon Ship'):
                    print('You have approached a Klingon ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    klingship = int(input('Option: '))
                    if klingship == 1:
                        clear()
                        print('You are attacking the Federation Ship!')
                        time.sleep(1)
                        KlingHealth = random.randint(1000,2000)
                        b = KlingHealth
                        Win = 0
                        while Win == 0:
                            clear()
                            print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
                            print(f'{Fore.BLUE}Klingon Health:{Fore.WHITE}', KlingHealth)
                            print(f'{Fore.GREEN}Your Health:{Fore.WHITE}', Health)
                            print('(1) Attack or (2) Defend')
                            atordef = int(input('Option: '))
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                exit()
                            if atordef == 1:
                                print('You are Attacking.')
                                damO = int(input("Pick a number between 1 and 10: "))
                                damInt = random.randint(1,10)
                                Close1 = damInt + 1
                                Close2 = damInt + 2
                                Close3 = damInt - 1
                                Close4 = damInt - 2
                                if damO == damInt:
                                    damdelt = (random.randint(100,200) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    KlingHealth = KlingHealth - damdelt
                                    continue
                                elif damO == Close1:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    KlingHealth = KlingHealth - damdelt
                                    continue
                                elif damO == Close3:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    KlingHealth = KlingHealth - damdelt
                                    continue   
                                elif damO == Close2:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    KlingHealth = KlingHealth - damdelt
                                    continue
                                elif damO == Close4:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    KlingHealth = KlingHealth - damdelt
                                    continue 
                                else:
                                     print('You Missed! Klingon Ship Turn...') 
                                     damrecieve = random.randint(50,200) 
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue
                            if atordef == 2:
                                print('You are defending.')
                                defO = int(input('Pick a number between 1 and 10: '))
                                defInt = random.randint(1,10)
                                Far1 = defInt + 1
                                Far2 = defInt + 2
                                Far3 = defInt - 1
                                Far4 = defInt - 2
                                if defO == defInt:
                                    defdelt = (random.randint(100,200))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far1:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far3:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue   
                                elif defO == Far2:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue  
                                elif defO == Far4:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue 
                                else:
                                     damrecieve = random.randint(100,300)
                                     print('You have been Hit!')  
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue 
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                break
                            if KlingHealth <= 0:
                                clear()
                                print(f'{Fore.GREEN}Battle Won!{Fore.WHITE}')
                                Win = 1
                                Coin = Coin + random.randint(20,30)
                                Materials = Materials + random.randint(100,200)
                                Health = Health + random.randint(50,100)
                                time.sleep(1)
                                continue
                if (selecteditem2 == 'Romulan Ship'):
                    print('You have approached a Romulan ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    klingship = int(input('Option: '))
                    if klingship == 1:
                        clear()
                        print('You are attacking the Romulan Ship!')
                        time.sleep(1)
                        RomHealth = random.randint(1000,2000)
                        b = RomHealth
                        Win = 0
                        while Win == 0:
                            clear()
                            print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
                            print(f'{Fore.BLUE}Romulan Health:{Fore.WHITE}', RomHealth)
                            print(f'{Fore.GREEN}Your Health:{Fore.WHITE}', Health)
                            print('(1) Attack or (2) Defend')
                            atordef = int(input('Option: '))
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                exit()
                            if atordef == 1:
                                print('You are Attacking.')
                                damO = int(input("Pick a number between 1 and 10: "))
                                damInt = random.randint(1,10)
                                Close1 = damInt + 1
                                Close2 = damInt + 2
                                Close3 = damInt - 1
                                Close4 = damInt - 2
                                if damO == damInt:
                                    damdelt = (random.randint(100,200) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    RomHealth = RomHealth - damdelt
                                    continue
                                elif damO == Close1:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    RomHealth = RomHealth - damdelt
                                    continue
                                elif damO == Close3:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    RomHealth = RomHealth - damdelt
                                    continue   
                                elif damO == Close2:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    RomHealth = RomHealth - damdelt
                                    continue
                                elif damO == Close4:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    RomHealth = RomHealth - damdelt
                                    continue 
                                else:
                                     print('You Missed! Romulan Ship Turn...') 
                                     damrecieve = random.randint(50,200) 
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue
                            if atordef == 2:
                                print('You are defending.')
                                defO = int(input('Pick a number between 1 and 10: '))
                                defInt = random.randint(1,10)
                                Far1 = defInt + 1
                                Far2 = defInt + 2
                                Far3 = defInt - 1
                                Far4 = defInt - 2
                                if defO == defInt:
                                    defdelt = (random.randint(100,200))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far1:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far3:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue   
                                elif defO == Far2:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue  
                                elif defO == Far4:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue 
                                else:
                                     damrecieve = random.randint(100,300)
                                     print('You have been Hit!')  
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue 
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                break
                            if RomHealth <= 0:
                                clear()
                                print(f'{Fore.GREEN}Battle Won!{Fore.WHITE}')
                                Win = 1
                                Coin = Coin + random.randint(20,60)
                                Materials = Materials + random.randint(100,200)
                                Health = Health + random.randint(50,100)
                                time.sleep(1)
                                continue
                            continue
                        continue
                    continue
                else:
                    print('Bad')
                    continue
            continue
        if ChoiceSector == 3: #Delta Sec (Vulcan, mining, planet mission)
            clear()
            op1 = ['Good', 'Good']
            selected_item = random.choice(op1) 
            op3 = ['Material Cluster', 'Vulcan Ship'] #, 'Mission Planet'
            selecteditem3 = random.choice(op3) #
            if (selecteditem3 == 'Material Cluster'):
                      print('You have approached a Material Cluster!')
                      DepositMat = random.randint(10,1000)
                      a = DepositMat / LaserUpgrade
                      time.sleep(1)
                      print('This mine has', DepositMat, 'rescources.')
                      mine = input('Would you like to mine? (Once you start mining, you cannot stop until finished) Y/N: ')
                      if (mine == "y"):
                            for i in range(DepositMat):
                                clear()
                                print('Mining...')
                                print('Materials Remaining:', a)
                                print('Total Materials:', Materials)
                                a = a - LaserUpgrade
                                Materials = Materials + (0.5 * LaserUpgrade)
                                time.sleep(0.5)
                            continue
            if (selecteditem3 == 'Vulcan Ship'):
                    print('You have approached a Klingon ship!')
                    time.sleep(1)
                    print('What do you want to do?')
                    op3 = ['1: Attack the Ship', '2: Ignore the Ship'] #, '2: Hail the Ship'
                    print(*op3, sep = '\n')
                    Vulcship = int(input('Option: '))
                    if Vulcship == 1:
                        clear()
                        print('You are attacking the Vulcan Ship!')
                        time.sleep(1)
                        VulcanHealth = random.randint(1000,2000)
                        b = VulcanHealth
                        Win = 0
                        while Win == 0:
                            clear()
                            print(f"{Fore.RED}RED ALERT{Fore.WHITE}")
                            print(f'{Fore.BLUE}Vulcan Health:{Fore.WHITE}', VulcanHealth)
                            print(f'{Fore.GREEN}Your Health:{Fore.WHITE}', Health)
                            print('(1) Attack or (2) Defend')
                            atordef = int(input('Option: '))
                            if Health <= 0:
                                clear()
                                print(f'{Fore.RED}Game over!{Fore.WHITE}')
                                exit()
                            if atordef == 1:
                                print('You are Attacking.')
                                damO = int(input("Pick a number between 1 and 10: "))
                                damInt = random.randint(1,10)
                                Close1 = damInt + 1
                                Close2 = damInt + 2
                                Close3 = damInt - 1
                                Close4 = damInt - 2
                                if damO == damInt:
                                    damdelt = (random.randint(100,200) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    VulcanHealth = VulcanHealth - damdelt
                                    continue
                                elif damO == Close1:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    VulcanHealth = VulcanHealth - damdelt
                                    continue
                                elif damO == Close3:
                                    damdelt = (random.randint(50,100) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    VulcanHealth = VulcanHealth - damdelt
                                    continue   
                                elif damO == Close2:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    VulcanHealth = VulcanHealth - damdelt
                                    continue
                                elif damO == Close4:
                                    damdelt = (random.randint(10,50) * PhaserUpgrade)
                                    print('You Hit! Damage Dealt:', damdelt) 
                                    time.sleep(1)
                                    VulcanHealth = VulcanHealth - damdelt
                                    continue 
                                else:
                                     print('You Missed! Klingon Ship Turn...') 
                                     damrecieve = random.randint(50,200) 
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue
                            if atordef == 2:
                                print('You are defending.')
                                defO = int(input('Pick a number between 1 and 10: '))
                                defInt = random.randint(1,10)
                                Far1 = defInt + 1
                                Far2 = defInt + 2
                                Far3 = defInt - 1
                                Far4 = defInt - 2
                                if defO == defInt:
                                    defdelt = (random.randint(100,200))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far1:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue
                                elif defO == Far3:
                                    defdelt = (random.randint(50,100))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue   
                                elif defO == Far2:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue  
                                elif defO == Far4:
                                    defdelt = (random.randint(10,50))
                                    print('You Dodged! Health Regained:', defdelt) 
                                    time.sleep(1)
                                    Health = Health + defdelt
                                    continue 
                                else:
                                     damrecieve = random.randint(100,300)
                                     print('You have been Hit!')  
                                     Health = Health - damrecieve
                                     time.sleep(1)
                                     continue 
                            if VulcanHealth <= 0:
                                clear()
                                print(f'{Fore.GREEN}Battle Won!{Fore.WHITE}')
                                Win = 1
                                Coin = Coin + random.randint(20,60)
                                Materials = Materials + random.randint(100,200)
                                Health = Health + random.randint(50,100)
                                time.sleep(1)
                                continue
                            continue
                        continue
                    continue
            else:
                print('Bad')
                continue
        continue
    if Option == 2:
        clear()
        print("Drydock")
        DryOp = ['1: Repair Ship', '2: Upgrade Ship', '3: Check Inventory', '4: Exit']
        print(*DryOp, sep = '\n')
        DryInt = int(input('Option: '))
        if DryInt == 1:
            clear()
            print('Repair Ship')
            print('Ship Health:', Health, '/', MaxHealth)
            if Health > MaxHealth:
                Repair = input('Repair? (Y/N)')
            else:
                print('Your Health is full.')
                time.sleep(2)
                continue
            continue
        if DryInt == 2:
            clear()
            print('Upgrade Ship')
            print('What would you like to upgrade?')
            UpOp = ['1: Phaser Upgrade', '2: Max Health Upgrade', '3: Mining Laser Upgrade']
            print(*UpOp, sep = '\n')
            UpOpInt = int(input('Which Upgrade do you Choose?'))
            if UpOpInt == 1:
                clear()
                print('Phaser Upgrade')
                print('Cost: 10')
                print('Current Level:', PhaserUpgrade)
                if Coin > 10:
                    buyconfirm = input('Are you sure you want to buy this? (Y/N)')
                    if buyconfirm == 'y':
                        PhaserUpgrade = PhaserUpgrade + 1
                        Coin = Coin-10
                        print('Upgrade Bought! Current Phaser Level:', PhaserUpgrade)
                        time.sleep(2)
                        continue
                    continue
                else:
                    print('You do not have enough coins to buy this.')
                    time.sleep(2)
                    continue
            if UpOpInt == 2:
                clear()
                print('Max Health Upgrade')
                print('Cost: 15')
                print('Current Max Health:', MaxHealth)
                if Coin > 15:
                    buyconfirm = input('Are you sure you want to buy this? (Y/N)')
                    if buyconfirm == 'y':
                        MaxHealth = MaxHealth + 500
                        Coin = Coin-15
                        print('Upgrade Bought! Current Health Level:', MaxHealth)
                        time.sleep(2)
                        continue
                    continue
                else:
                    print('You do not have enough coins to buy this.')
                    time.sleep(2)
                    continue
                continue
            if UpOpInt == 3:
                clear()
                print('Mining Laser Upgrade')
                print('Cost: 10')
                print('Current Laser:', LaserUpgrade)
                if Coin > 10:
                    buyconfirm = input('Are you sure you want to buy this? (Y/N)')
                    if buyconfirm == 'y':
                        LaserUpgrade = LaserUpgrade + 1
                        Coint = Coin-10
                        print('Upgrade Bought! Current Laser Level:', LaserUpgrade)
                        time.sleep(2)
                        continue
                    continue
                else:
                    print('You do not have enough coins to buy this.')
                    time.sleep(2)
                    continue
                continue
            continue
        if DryInt == 4:
            continue
        continue
    if Health < MaxHealth:
        Health = Health + HealthUp