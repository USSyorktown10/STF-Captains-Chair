            drydock_option1 = ['1: Upgrade Mining Laser', '2: Upgrade Health', '3: Upgrade Warp Range', '4: View Upgrades', '5: Restore Health', '6: Exit']
            print(*drydock_option1, sep = '\n')
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