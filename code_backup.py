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
