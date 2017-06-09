from random import randint
import sys

catk = "\x1b[0;31;40m"
crrl = "\x1b[0;33;40m"
chp = "\x1b[0;32;40m"
cdef = "\x1b[0;36;40m"
cw = "\x1b[0m"

stuff_types = ['weapon', 'armor', 'shield', 'ring']
nb_quest = 0
max_parry = 70
potion = 0
fight_info = ""
stun = 0
potion = 0
prompt = ">>> "
job = ""
gold = 0
zone = 1
w_lvl = 0
player = {'hp':50, 'hp_max': 50, 'atk': 15, 'def': 3, 'reroll' : 1, 'reroll_max': 1}
foe = {'hp':30, 'hp_max': 30, 'atk': 10}
foes = {'hp':30, 'hp_max': 30, 'atk': 10}

def display_stat():
    print("HP : "+chp+str(player['hp'])+"/"+str(player['hp_max'])+cw+"\nATK : "+catk+str(player['atk'])+cw+"\nDEF : "+cdef+str(player['def'])+cw+"\nREROLL : "+crrl+str(player['reroll_max'])+cw)

def clear_screen():
    for b in range(0,100):
        print("\n")

def create_stuff(stuff_type):
    quality = w_lvl + randint(round(-w_lvl * 0.2, 0), round(w_lvl * 0.2, 0))
    primary = randint(round(quality*0.3, 0), quality)
    secondary = quality - primary
    wep = {'type': stuff_type, 'hp_max': 0, 'atk': 0, 'def': 0, 'reroll' : 0}
    if (stuff_type == 'weapon'):
        wep['atk'] += primary
    elif (stuff_type == 'armor'):
        wep['hp_max'] += primary
    elif (stuff_type == 'shield'):
        wep['def'] += primary
    elif (stuff_type == 'ring'):
        wep['reroll'] += primary
    r = randint(0,3)
    if (r == 0):
        wep['atk'] += secondary
    elif (r == 1):
        wep['hp_max'] += secondary
    elif (r == 2):
        wep['def'] += secondary
    elif (r == 3):
        wep['reroll'] += secondary
    wep['atk'] = round(wep['atk'] / 2, 0)
    wep['reroll'] = round(wep['reroll'] / 25, 0)
    wep['def'] = round(wep['def'] / 4, 0)
    return (wep)

def print_wep(st, w):
    print(st +"[Type : ",w['type'],",  HP MAX : +"+chp, w['hp_max'],cw+",  ATK : +"+catk, w['atk'],cw+",  DEF : +"+cdef, w['def'],cw+",  REROLL : +"+crrl, w['reroll'], cw+"]")

def display_fight(patk, pdef, pagi, fatk,):
    global fight_info
    clear_screen()
    print(fight_info)
    fight_info = ""
    print("\n\n\n"+name+" the "+job+" :                         gold : "+str(gold)+"\n\npotion available : "+str(potion)+"\nreroll(s) available this turn : "+crrl+str(player['reroll'])+cw+"\nHP  : "+chp+str(player['hp'])+"/"+str(player['hp_max'])+cw+"\nATK : "+catk+str(patk)+cw+" ("+str(player['atk'])+")\n"+"DEF : "+cdef+str(pdef)+cw+" ("+str(player['def'])+")\n"+"PAR : "+str(pagi)+"% ("+str(max_parry)+"%)")
    print("\n\nCreature lvl "+str(zone)+" : \n\nHP  : "+chp+str(foe['hp'])+"/"+str(foe['hp_max'])+cw+"\nATK : "+catk+str(fatk)+cw+" ("+str(foe['atk'])+")")
    print("\n(Type 'h' for help)")

def turn():
    global gold
    global fight_info
    global stun
    global potion
    player["reroll"] = player["reroll_max"]
    fatk = randint(round(foe['atk'] * 0.2, 0), foe['atk'])
    patk = randint(0, player['atk'])
    pdef = randint(0, player['def'])
    pagi = randint(0, 70)
    if (stun) :
        player["reroll"] = 0
        patk = 0
        pdef = 0
        pagi = 0
        stun = 0
    if (job == "swordsman"):
        pagi += 10
    display_fight(patk, pdef, pagi, fatk)
    inpt = input(prompt)
    while (inpt != "a" and inpt != "p"):
        if (inpt == "s" and (job == "barbarian" or job == "thief")):
            break
        if (inpt == "h"):
            fight_info = "Choose an action:\na  : attack \np  : parry ("+str(pagi)+"% chance to take no damage, but if you fail, your attack is canceled)\nra : reroll attack (doesn't end your turn)\nrd : reroll defense (doesn't end your turn)\nrp : reroll parry (doesn't end your turn)\npot: heal 50% of your max life a with potion (doesn't end your turn)"
            if (job == "wizard"):
                fight_info += "\ns  : Wizard Special : reroll your ennemie's attack"
            elif (job == "barbarian"):
                fight_info += "\ns  : Barbarian Special : do 200% damage but your are tired for the next turn"
            elif (job == "thief"):
                fight_info += "\ns  : Thief Special : do 25% damage and steal gold"
        elif (inpt == "pot"):
            if (potion):
                player['hp'] = player['hp'] + round(player['hp_max'] / 2, 0)
                if (player['hp'] > player['hp_max']):
                    player['hp'] = player['hp_max']
                potion = 0
                fight_info += "\nDrinking your potion gave you back 50% of your max hp."
            else:
                fight_info += "\nYou do not have a potion to drink."
        elif ((inpt == "ra" or inpt == "rd" or inpt == "rp" or (inpt == "s" and job == "wizard")) and player["reroll"] <= 0):
            fight_info = "/!\ You can't reroll anymore this turn."
        elif (inpt == "ra"):
            patk = randint(0, player['atk'])
            player["reroll"] -= 1
            fight_info = "Your attack has been rerolled."
        elif (inpt == "rd"):
            pdef = randint(0, player['def'])
            player["reroll"] -= 1
            fight_info = "Your defense has been rerolled."
        elif (inpt == "rp"):
            pagi = randint(0, 70)
            if (job == "swordsman"):
                pagi += 10
            player["reroll"] -= 1
            fight_info = "Your parrying has been rereolled."
        elif (inpt == "s" and job == "wizard"):
            fatk = randint(round(foe['atk'] * 0.2, 0), foe['atk'])
            player["reroll"] -= 1
            fight_info = "Your ennemie's attack has been rerolled."
        else :
            print("\n /!\Invalid command")
        display_fight(patk, pdef, pagi, fatk)
        inpt = input(prompt)
    dmg = fatk - pdef
    if dmg < 0 :
        dmg = 0
    if (inpt == "a"):
        player["hp"] -= dmg
        foe["hp"] -= patk
        fight_info = "Your opponent take "+str(patk)+" damage!\nYou take "+str(dmg)+" damage!"
    elif (inpt == "p"):
        p = randint(0, 100)
        if p <= pagi:
            fight_info += "Your parry is successfull!\nYour opponent take "+str(patk)+" damage!"
            foe["hp"] -= patk
        else:
            fight_info += "Your parry failed!\nYou take "+str(dmg)+" damage!"
            player["hp"] -= dmg
    elif (inpt == "s" and job == "barbarian"):
        player["hp"] -= dmg
        patk = round(patk * 2, 0)
        foe["hp"] -= patk
        stun = 1
        fight_info = "Your opponent take "+str(patk)+" damage!\nYou take "+str(dmg)+" damage!"
    elif (inpt == "s" and job == "thief"):
        bounty = randint(round(w_lvl * 0.3, 0), round(w_lvl * 0.5, 0))
        gold += bounty
        patk = round(patk/4, 0)
        player["hp"] -= dmg
        foe["hp"] -= patk
        fight_info = "You stole "+str(bounty)+" gold!\nYour opponent take "+str(patk)+" damage!\nYou take "+str(dmg)+" damage!"

def fight():
    global stun
    global foe
    global gold
    global fight_info
    fight_info = ""
    foe['hp_max'] = randint(round(foes['hp_max'] * 0.8, 0), round(foes['hp_max'] * 1.2, 0))
    foe['hp'] = foe['hp_max']
    foe['atk'] = randint(round(foes['atk'] * 0.8, 0), round(foes['atk'] * 1.2, 0))
    stun = 0
    while (player['hp'] > 0 and foe['hp'] > 0):
        turn()
        clear_screen()
    if (player['hp'] <= 0):
        print(fight_info+"\n\nYou loose!\n\n "+name+" the "+job+" died in zone "+str(zone)+"\n\nRIP")
        sys.exit()
    else:
        bounty = randint(round(w_lvl * 0.6, 0), round(w_lvl * 1.4, 0))
        print(fight_info+"\n\nCreature defeated!\n You gain "+str(bounty)+" gold")
        gold += bounty

def main_loop():
    global nb_quest
    clear_screen()
    print ("Welcome "+name+" the "+job+"!\nYou are about to go on an epic adventure.\nYour first quest is about to begin.\n\nYou reached zone 1\n\n")
    while (42):
        nb_quest += 1
        clear_screen()
        print("\n2 fights left to complete this quest.\n\nProceed.\n")
        input(prompt)
        fight()
        print("\n\n1 fight left to complete this quest.\n\nProceed.\n")
        input(prompt)
        fight()
        print("\n\nQuest completed.\n You reached a shop.\n\nProceed.\n")
        input(prompt)
        shop()

def choose_job():
    return input('\n\nChoose your class by typing one of the following:\n\n"thief" \n(can perform a light attack that steals gold)\n\n"wizard"\n(can reroll his ennemie\'s attack)\n\n"barbarian"\n(can perform an attack that deals double damage but skip his next turn)\n\n"swordsman"\n(has +10% chance to perform a parry).\n\n'+prompt)

def display_shop(i1,i2,i3):
    clear_screen()
    if potion:
        pstr = "(You already have a potion)"
    else:
        pstr = "(You have no potion yet)"
    print("Zone "+str(zone)+"                        gold : "+str(gold)+"\n\nSHOP\nStuff Price : "+str(w_lvl)+"                 Potion Price : "+str(w_lvl * 2)+" "+pstr+"\n\nStuff to sell : ")
    print_wep("1 : ", i1)
    print_wep("2 : ", i2)
    print_wep("3 : ", i3)
    print("\n\n Your stuff : ")
    print_wep("", stuff['weapon'])
    print_wep("", stuff['armor'])
    print_wep("", stuff['shield'])
    print_wep("", stuff['ring'])
    print("\n\nYour stats : ")
    display_stat()
    print("\nChoose an action : \n1,2,3: buy stuff\npot  : buy a potion\ngo   : do another quest in this zone\nnext : move to the next zone")

def update_player(stuff, modif):
    player['hp_max'] += stuff['hp_max'] * modif
    player['def'] += stuff['def'] * modif
    player['atk'] += stuff['atk'] * modif
    player['reroll_max'] += stuff['reroll'] * modif

def shop():
    global potion
    global gold
    global w_lvl
    global zone
    i = [0,0,0]
    i[0] = create_stuff(stuff_types[randint(0,3)])
    i[1] = create_stuff(stuff_types[randint(0,3)])
    i[2] = create_stuff(stuff_types[randint(0,3)])
    while (42):
        player['hp'] = player['hp_max']
        display_shop(i[0],i[1],i[2])
        inpt = input(prompt)
        if (inpt == "pot" and potion == 0 and gold >= w_lvl * 2):
            potion = 1
            gold -= w_lvl * 2
        elif (inpt == "go"):
            break
        elif (inpt == "next"):
            zone += 1
            foes['hp'] = foes['hp'] * 2
            foes['hp_max'] = foes['hp_max'] * 2
            foes['atk'] = foes['atk'] * 2
            w_lvl *= 2
            clear_screen()
            print("You reached zone "+str(zone)+"\n\n")
            input(prompt)
            break
        elif (inpt == "1" or inpt == "2" or inpt == "3") and gold >= w_lvl:
            gold -= w_lvl
            wid = int(inpt) - 1
            update_player(stuff[i[wid]['type']], -1)
            update_player(i[wid], 1)
            stuff[i[wid]['type']] = i[wid]
            i[wid] = create_stuff(stuff_types[randint(0,3)])

stuff = {'weapon' : create_stuff('weapon'), 'armor' : create_stuff('armor'), 'shield' : create_stuff('shield'), 'ring' : create_stuff('ring')}
w_lvl = 25

clear_screen()
name = input('\nWhat is your name ?\n\n'+prompt)

clear_screen()
job = choose_job()
while (job != "thief" and job != "wizard" and job != "barbarian" and job != "swordsman" and job != "aze"):
    clear_screen()
    job = choose_job()
if (job == "swordsman"):
    max_parry += 10

main_loop()
# 0 help
# 1 atk
# 2 counter
# 3 rrl atk
# 4 rrl def
# 5 rrl pry
# 6 pot
# 7 sp (steal or confuse or hugeblow)
