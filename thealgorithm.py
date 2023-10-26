import random
import time


bold = "\033[1m"
red = "\033[91m"
end = "\033[0m"
cyan = "\033[96m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
purple = "\033[95m"
italics = "\x1B[3m "
underline = "\033[4m"


#Given a list of elements
#Will announce and remove 1 element from that list
#Returns the new list with that element removed
def remove_random(players):
    temprand = random.randrange(0,len(players))
    print(f"WE ARE REMOVING 2 PLAYERS FROM THE GAME :)")
    print(f"THAT PLAYER IS...")
    print(f"{players[temprand]}")
    players.pop(temprand)
    temprand = random.randrange(0,len(players))
    print(f"and {players[temp2]}")
    players.pop(temprand)
    return players


def algorithm(players, history, week_num):
    
    reset = False
    temp_players = [] + players
    fail_count = 0
    history[week_num] = {}
    for x in temp_players:
        history[week_num][x] = "empty"
    while len(temp_players) > 0:            
        if reset:
            fail_count += 1
            print(f"The code has failed {fail_count} times")
            temp_players = [] + players
            for x in temp_players:
                history[week_num][x] = "empty"
            reset = False
            if fail_count >= 100000:
                print("The code has failed 100000 times. There seems to be no possible combination for these players without a repeat")
                break
        player1 = temp_players[random.randrange(0,len(temp_players))]
        player2 = temp_players[random.randrange(0,len(temp_players))]
        while player2 == player1:
            player2 = temp_players[random.randrange(0,len(temp_players))]
        for x in history:
            if history[x][player1] == player2:
                reset = True
        history[week_num][player1] = player2
        history[week_num][player2] = player1
        temp_players.remove(player1)
        temp_players.remove(player2)
    return history, week_num

def announce_algorithm(history, week_num):
    print(f"{yellow}ITS TIME TO ANNOUNCE PARTNERS FOR WEEK {bold}{week_num}{end}")
    time.sleep(timer)
    this_week = history[week_num]
    already_said = []
    for x in this_week:
        if not x in already_said:
            print(f"{underline}{purple}{x}{end} {italics}will be partners with...{end}")
            time.sleep(timer)
            print(f"{red}{this_week[x]}{end}!!!")
            time.sleep(timer)
            already_said = already_said + [this_week[x]]
    return history
         




history = {}
week_num = 1
players = ['JMilk','Larry','Alv','Gible','Kaz','Mee6','Carl','Dyno']
timer = 2


for i in range(7):
    history = announce_algorithm(*algorithm(players, history, week_num))
    week_num += 1





