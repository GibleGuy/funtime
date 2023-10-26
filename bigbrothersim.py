import random
import time

timerson = True
#########################
########################
# HI VIEWERS
# IF YOU WANT THIS TO GO REALLY FAST
# CHANGE TIMERSON TO FALSE
##########################

# timerson = False

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

if timerson:
    timer = 2
    shorttimer = 1
else:
    timer = 0
    shorttimer = 0
juror_count = 7

# Given the competitions that are still eligible to compete and the status
# It will remove the outgoing HOH (if there is one) from competing
# and run the HOH comp and return the status, updated to only have the hoh
def hoh_comp(status):
    print(f"{green}-------{bold}WEEK {status['WEEKNUM']}{end}{green}--------")
    print(f"{blue}---------------------")
    print(f"---{bold}HOH COMPETITION{end}{blue}---")
    print(f"---------------------{end}")
    time.sleep(timer)
    print(f"It is time for our next {yellow}Head of Household{end} competition!")
    time.sleep(timer)

    competing = []
    if len(status["comps_left"]) == 0:
        status["comps_left"] = [] + status["comp_types"]
    comppick = status["comps_left"][random.randrange(0, len(status["comps_left"]))]
    status["comps_left"].remove(comppick)
    for x in status["PLAYERS"]:
        competing = competing + [x]
    if len(competing) == 3:
        print(f"Welcome to the {bold}FINAL{end} {yellow}Head of Household!{end}")
        time.sleep(timer)
        print("Since only 3 players remain, all of you are eligible to compete")
        time.sleep(timer)
    elif not status["HOH"] == "empty":
        print(
            f"As {yellow}outgoing HOH{end}, {blue}{status['HOH']}{end} is {red}not eligible to compete.{end}"
        )
        time.sleep(timer)
        competing.remove(status["HOH"])
    print(f"This weeks {yellow}HOH{end} is a battle of {purple}{comppick}{end}")
    time.sleep(timer)
    print("Let's begin!")
    time.sleep(timer)
    print()
    winner = announce_winner(result(competing, comppick))
    print()
    time.sleep(timer)
    print(
        f"Congratulations {yellow}{winner}{end}, you are the new {yellow}Head of Household!{end}"
    )
    status["HOH"] = winner
    return status


# Given the competitions left to be played so far and the status of the week
# Will return the status after calculating who the POV winner is
def veto_comp(status):
    print(f"{blue}---------------------")
    print(f"---{bold}POV COMPETITION{end}{blue}---")
    print(f"---------------------{end}")
    time.sleep(timer)
    competing = []
    print(f"It is time for the {yellow}Power of Veto{end} competition!")
    time.sleep(timer)
    competing = [status["HOH"], status["NOM1"], status["NOM2"], status["POVPLAYER1"]]
    if not status["POVPLAYER2"] == "empty":
        competing = competing + [status["POVPLAYER2"]]
        if not status["POVPLAYER3"] == "empty":
            competing = competing + [status["POVPLAYER3"]]
    if len(status["comps_left"]) == 0:
        status["comps_left"] = status["comps_left"] + status["comp_types"]
    comppick = status["comps_left"][random.randrange(0, len(status["comps_left"]))]
    status["comps_left"].remove(comppick)
    print(
        f"This weeks {yellow}POV{end} is a battle of {purple}{comppick}{end} strength!"
    )
    time.sleep(timer)
    print("Let's begin!")
    time.sleep(timer)
    print()
    winner = announce_winner(result(competing, comppick))
    status["POV"] = winner
    time.sleep(timer)
    print(
        f"Congratulations {yellow}{winner}{end}, you have won the {yellow}Golden Power of Veto{end}!"
    )
    time.sleep(timer)
    print()
    return status


# Given the placements of a competition, it will announce what placements everyone got and return the winner
def announce_winner(placements):
    currentplace = len(placements)
    shuffleme = []
    while currentplace > 0:
        placementannounce = placement_logic(currentplace)
        if currentplace == 3:
            shuffleme = shuffleme + placements
            random.shuffle(shuffleme)
            random.shuffle(shuffleme)
            random.shuffle(shuffleme)
            print(
                f"The top 3 players are {purple}{shuffleme[0]}{end}, {purple}{shuffleme[1]}{end}, and {purple}{shuffleme[2]}{end}"
            )
            time.sleep(timer)
        print(f"In {placementannounce} place")
        time.sleep(shorttimer)
        print("...")
        time.sleep(shorttimer)
        print(f"{underline}{placements[-1]}{end}")
        time.sleep(shorttimer)
        print()
        winner = placements[-1]
        placements.pop(-1)
        currentplace -= 1
    return winner


# Given a number (representing a placement)
# it will return that number with it's proper form of placement announcing
def placement_logic(placement):
    if placement == 0:
        ans = f"{placement}th"
    elif placement == 1:
        ans = f"{placement}st"
    elif placement == 2:
        ans = f"{placement}nd"
    elif placement == 3:
        ans = f"{placement}rd"
    elif placement > 3:
        ans = f"{placement}th"
    ans = f"{bold}{ans}{end}"
    return ans


# Given the players competing and competition type
# The function will determine who is the strongest in that type of comp
# Also, adds a random number 1-10 to your comp strength because it's more fun that way.
# if there's a tie the winner will be randomized between the strongest players
# Returns a list of placements from first to last
def result(competing, comptype, placements=[]):
    if not competing:
        return placements
    tielist = []
    topplayer = "empty"
    temp_rand = 0
    high_rand = 0
    for x in competing:
        temp_rand = random.randrange(0, 10)
        if (
            topplayer == "empty"
            or status["PLAYERS"][x]["compability"][comptype] + temp_rand
            > status["PLAYERS"][topplayer]["compability"][comptype] + high_rand
        ):
            topplayer = x
            tielist = []
            high_rand = temp_rand
        elif (
            status["PLAYERS"][x]["compability"][comptype] + temp_rand
            == status["PLAYERS"][topplayer]["compability"][comptype] + high_rand
        ):
            tielist = tielist + [topplayer] + [x]
    if tielist:
        topplayer = random.choice(tielist)
    placements = placements + [topplayer]
    competing.remove(topplayer)
    return result(competing, comptype, placements=placements)


# Given who the HOH is in status
# Will return the two houseguests that the HOH likes the least
def nominations(status, nominees=[]):
    lowest = "empty"
    tielist = []
    relatelist = status["PLAYERS"][status["HOH"]]["relations"]
    if len(nominees) == 2:
        status["NOM1"] = nominees[0]
        status["NOM2"] = nominees[1]
        return status
    for x in relatelist:
        if not x in nominees:
            if lowest == "empty" or relatelist[lowest] > relatelist[x]:
                lowest = x
                tielist = []
            elif relatelist[lowest] == relatelist[x]:
                tielist = tielist + [x]
                if not lowest in tielist:
                    tielist = tielist + [lowest]
    if tielist:
        lowest = random.choice(tielist)
    tempnoms = nominees + [lowest]
    return nominations(status, nominees=tempnoms)


# Given the HOH for the week
# Will print out the nomination ceremony for the week
def nomination_ceremony(status):
    status = nominations(status)
    print(f"{green}-------------------------")
    print(f"---{bold}NOMINATION CEREMONY{end}{green}---")
    print(f"-------------------------{end}")
    print()
    time.sleep(timer)
    print(
        f"{italics}{yellow}{status['HOH']}{end} {italics}walks into the kitchen, and stands infront of a table of the houseguests{end}"
    )
    time.sleep(timer)
    print(f"It is time for the {red}Nomination Ceremony{end}")
    time.sleep(timer)
    print(
        f"as {yellow}Head of Household{end} ({bold}{status['HOH']}{end}), it is my responsibility to nominate 2 houseguests for eviction"
    )
    time.sleep(timer)
    print("I will turn 2 keys, and their names will appear in the textbox")
    time.sleep(timer)
    print()
    print(f"{italics}My first nominee is...{end}")
    time.sleep(timer)
    print(f"{italics}...{end}")
    time.sleep(timer)
    print(f'{red}{status["NOM1"]}{end}')
    time.sleep(timer)
    print()
    print(f"{italics}My second nominee is...{end}")
    time.sleep(timer)
    print(f"{italics}...{end}")
    time.sleep(timer)
    print(f"{red}{status['NOM2']}{end}")
    time.sleep(timer)
    print()
    print(
        f"I have nominated you, {red}{status['NOM1']}{end} and you, {red}{status['NOM2']}{end}"
    )
    time.sleep(timer)
    print(
        "At this moment in time, you two are the houseguests I have the least connection with"
    )
    time.sleep(timer)
    print()
    print(f"{italics}This {red}Nomination Ceremony{end} is ajourned.{end}")
    print()
    time.sleep(timer)
    return status


# Given the status including the current POV holder, nominees, and HOH
# If a nominee is the POV holder, they will always use it on themselves
# If the HOH wins POV, they will always discard it
# If another person wins POV, they will see who they are closest too between HOH and the two noms
# If it is the HOH, then they discard it
# If it is a nominee, and they have a friendship score of greater than 5, they will use it on them
# Returns the updated status with an updated usage stat.
def veto_decision(status):
    pov_holder, HOH, nom1, nom2 = (
        status["POV"],
        status["HOH"],
        status["NOM1"],
        status["NOM2"],
    )
    if pov_holder == nom1 or pov_holder == nom2:
        status["USAGE"] = pov_holder
        return status
    if len(status["PLAYERS"]) == 4:
        status["USAGE"] = "discard"
        return status
    if not HOH == pov_holder:
        temp1 = comparison(pov_holder, HOH, nom1, "PLAYERS")
        temp2 = comparison(pov_holder, nom1, nom2, "PLAYERS")
        highest = comparison(pov_holder, temp1, temp2, "PLAYERS")
        if status["PLAYERS"][pov_holder]["relations"][highest] > 30:
            if not highest == HOH:
                status["USAGE"] = highest
                return status
    status["USAGE"] = "discard"
    return status


# Given the HOH, Veto & Noms this week
# Will return the renomination out of the players who are eligible
def renomination(status):
    safe_list = list(set([status["POV"], status["NOM1"], status["NOM2"]]))
    tielist = []
    lowest = "empty"
    relatelist = status["PLAYERS"][status["HOH"]]["relations"]
    for x in relatelist:
        if not x in safe_list:
            if lowest == "empty" or relatelist[lowest] > relatelist[x]:
                lowest = x
                tielist = []
            elif relatelist[lowest] == relatelist[x]:
                tielist = tielist + [x]
                if not lowest in tielist:
                    tielist = tielist + [lowest]
    if tielist:
        lowest = random.choice(tielist)
    status["RENOM"] = lowest
    return status


# Announces the power of veto ceremony
def veto_ceremony(status):
    print(f"{green}------------------------")
    print(f"------{bold}POV CEREMONY{end}{green}------")
    print(f"------------------------{end}")
    time.sleep(timer)
    print()
    print(
        f"{italics}{status['POV']} walks to the front of the living room, where {red}{status['NOM1']}{end} &{italics}{red}{status['NOM2']}{end} {italics}sit in the nomination chairs.{end}"
    )
    time.sleep(timer)
    print(f"It is time for the {yellow}Power of Veto Ceremony{end}!")
    time.sleep(timer)
    print()
    print(
        f"The {yellow}Head of Household, {status['HOH']}{end}, has nominated {red}{status['NOM1']}{end} & {red}{status['NOM2']}{end}"
    )
    time.sleep(timer)
    print(
        f"However, as the winner of the POV competition, I, {yellow}{status['POV']}{end}, have the power to remove one of the nominees"
    )
    time.sleep(timer)
    print(f"I have decided...")
    time.sleep(timer)
    print("...")
    status = veto_decision(status)
    if not status["USAGE"] == "discard":
        print(f"To use the {yellow}Power of Veto{end} on...")
        time.sleep(timer)
        print("...")
        time.sleep(timer)
        if status["POV"] == status["NOM1"] or status["POV"] == status["NOM2"]:
            print(f"{yellow}Myself.{end}")
        print(f"{yellow}{status['USAGE']}{end}")
        time.sleep(timer)
        print(
            f"Meaning that {yellow}{status['HOH']}{end} you must now name a {red}replacement nominee{end}"
        )
        time.sleep(timer)
        print()
        print(
            f"{italics}{yellow}{status['HOH']}{end} {italics}walks to the front of the room...{end}"
        )
        time.sleep(timer)
        print("I really didn't want to do this")
        time.sleep(timer)
        print(f"but my {red}replacement nominee{end} is...")
        time.sleep(timer)
        print("...")
        status = renomination(status)
        print(f"{red}{status['RENOM']}{end}")
        time.sleep(timer)
        if status["NOM1"] == status["USAGE"]:
            status["NOM1"] = status["RENOM"]
        elif status["NOM2"] == status["USAGE"]:
            status["NOM2"] = status["RENOM"]
        else:
            # this has never before been printed
            print("THE CODE IS FUCKED THE CODE IS FUCKED")
        print(
            f"Meaning that the {red}final nominees{end} for the week are {red}{status['NOM1']}{end} and {red}{status['NOM2']}{end}"
        )
        time.sleep(timer)
    else:
        print(f"{red}Not{end} to use the {yellow}Power of Veto.{end}")
        time.sleep(timer)
        print("I Really don't want to mess up anything this week")
        time.sleep(timer)
    print("Good luck to both of you, fight the good fight")
    time.sleep(timer)
    print(f"{italics}This {yellow}Power of Veto{end} ceremony, is ajourned.{end}")
    time.sleep(timer)
    print()
    return status


# Given the status of the house
# It creates a list of players minus the nominees & HOH
# Randomly draws from a bag with those names and a chip for houseguest choice
# and returns the chips that were chosen from the bag
def eligible_pick(status):
    list_players = []
    list_picks = []
    for x in status["PLAYERS"]:
        list_players = list_players + [x]
    list_players.remove(status["HOH"])
    list_players.remove(status["NOM1"])
    list_players.remove(status["NOM2"])
    list_all_eligible = list_players
    if len(list_players) <= 3:
        return list_all_eligible, list_players, list_picks
    list_players = list_players + ["HGC"]
    for i in range(3):
        randompick = random.randrange(0, len(list_players))
        list_picks += [list_players[randompick]]
        list_players.remove(list_players[randompick])
    return list_all_eligible, list_players, list_picks


# Given the player who chose houseguest choice and the players who are eligible to be picked
# Will announce and return the eligible player that the chooser has the best relationship with in the house
def houseguest_choice(person, listplayers):
    highest = "empty"
    relatelist = status["PLAYERS"][person]["relations"]
    tielist = []
    for x in listplayers:
        if not x == person:
            if highest == "empty" or relatelist[x] > relatelist[highest]:
                highest = x
                tielist = []
            elif relatelist[x] == relatelist[highest]:
                tielist = tielist + [x]
                if not highest in tielist:
                    tielist = tielist + [highest]
        if tielist:
            highest = random.choice(tielist)
    print(f"{bold}{person}{end} has picked {purple}Houseguest's Choice!{end}")
    time.sleep(timer)
    print(f"They choose...")
    time.sleep(timer)
    print(f"{purple}{highest}{end}!")
    time.sleep(timer)
    return highest


# Given who is picking, what chip they picked, and what players haven't been picked
# Will announce who they pick, and run the logic if they got houseguest choice.
def pick_me(who, pick, listplayers):
    print(f"{bold}{who}{end} picks...")
    time.sleep(timer)
    print("...")
    time.sleep(timer)
    if pick == "HGC":
        pick = houseguest_choice(who, listplayers)
    else:
        print(f"{purple}{pick}{end}!")
    time.sleep(timer)
    print()
    return pick


# Given who the HOH & Nominees are
# Will pick and announce the other players in POV for the week
# returning an updated status
def veto_pick(status):
    list_all_eligible, list_players, list_picks = eligible_pick(status)
    print(f"{cyan}------------------------")
    print(f"---{bold}VETO PICK CEREMONY{end}{cyan}---")
    print(f"------------------------{end}")
    print()
    time.sleep(timer)
    if len(list_all_eligible) <= 3:
        print(
            f"Since only {len(list_all_eligible) + 3} players remain, everyone will compete in the {yellow}Power of Veto{end}!"
        )
        time.sleep(timer)
        print()
        status["POVPLAYER1"] = list_all_eligible[0]
        if len(list_all_eligible) > 1:
            status["POVPLAYER2"] = list_all_eligible[1]
            if len(list_all_eligible) > 2:
                status["POVPLAYER3"] = list_all_eligible[2]
    else:
        print(
            f"{italics}{yellow}{status['HOH']}{end} {italics}stands at the front of the living room, infront of all the houseguests{end}"
        )
        time.sleep(timer)
        print(f"It is time for the {cyan}Veto Picking{end} ceremony!")
        time.sleep(timer)
        print(
            f"Only 6 players will compete in the {yellow}Power of Veto{end} ceremony."
        )
        time.sleep(timer)
        print(
            f"The {yellow}Head of Household{end}, {red}two nominees{end}, and 3 players chosen by {underline}random draw.{end}"
        )
        time.sleep(timer)
        print(f"As {yellow}HOH{end}, {bold}{status['HOH']}{end} will pick first.")
        time.sleep(timer)
        status["POVPLAYER1"] = pick_me(status["HOH"], list_picks[0], list_players)
        status["POVPLAYER2"] = pick_me(status["NOM1"], list_picks[1], list_players)
        status["POVPLAYER3"] = pick_me(status["NOM2"], list_picks[2], list_players)
    return status


# given a player and two choices of other players
# will return the choice that they like more in that relationship
def comparison(player, one, two, group):
    guyone = status[group][player]["relations"][one]
    guytwo = status[group][player]["relations"][two]
    if guyone > guytwo:
        return one
    elif guytwo > guyone:
        return two
    else:
        return random.choice([one, two])


# Given a player and two choices of other players
# Will return the player they like less
def reverse_comparison(player, one, two):
    guyone = status["PLAYERS"][player]["relations"][one]
    guytwo = status["PLAYERS"][player]["relations"][two]
    if guyone > guytwo:
        return two
    elif guytwo > guyone:
        return one
    else:
        return random.choice([one, two])


# Announces the votes at the end of the week
# If theres only 3 players, then it'll let the HOH vote
def vote_announce(status):

    print(f"{blue}-----------------------")
    print(f"---{bold}EVICTION CEREMONY{end}{blue}---")
    print(f"-----------------------{end}")
    print()
    time.sleep(timer)
    print(f"{underline}It is time to vote!{end}")
    time.sleep(timer)
    if len(status["PLAYERS"]) == 3:
        print(
            f"Since this is the FINAL {yellow}Head of Household{end}, only {status['HOH']} will vote"
        )
        time.sleep(timer)
        print(
            f"{bold}{yellow}{status['HOH']}{end} must vote for either {red}{status['NOM1']}{end} or {red}{status['NOM2']}{end} to be evicted"
        )
        time.sleep(timer)
        print(
            f"The player they don't choose will be the one sitting next to them in the final 2 chairs."
        )
        time.sleep(timer)
        print("Let's begin.")
    elif len(status["PLAYERS"]) == 4:
        print(f"Since this is the final 4, there will only be one vote this week!")
        time.sleep(timer)

        for x in status["PLAYERS"]:
            if not (x == status["HOH"] or x == status["NOM1"] or x == status["NOM2"]):
                voter = x
                status["VOTER"] = voter
        print(
            f"{purple}{bold}{voter}{end}, since you are neither {red}nominated{end} nor {yellow}HOH{end}, you will cast the only vote."
        )
        time.sleep(timer)
        print(
            f"Please stand at the head of the room, and cast your vote to {red}evict{end}!"
        )
        time.sleep(timer)

    else:
        tiecheck = (len(status["PLAYERS"]) - 3) % 2
        if tiecheck == 0:
            print(
                f"As Head of Household, {yellow}{status['HOH']}{end} will only vote in the case of a tie."
            )
            time.sleep(timer)
        else:
            print(
                f"As Head of Household, {yellow}{status['HOH']}{end} you are not allowed to vote."
            )
            time.sleep(timer)
        print(
            f"The nominees, {red}{status['NOM1']}{end} & {red}{status['NOM2']}{end} will not vote either."
        )
        time.sleep(timer)
        print(
            f"One by one the houseguests will go into the diary room and cast their vote to {red}evict{end}."
        )
        time.sleep(timer)
        print("Let's begin.")
    time.sleep(timer)
    print()


def vote_time(status):
    hoh, nom1, nom2, voter = (
        status["HOH"],
        status["NOM1"],
        status["NOM2"],
        status["VOTER"],
    )
    vote_announce(status)
    votes = {nom1: 0, nom2: 0}
    for x in status["PLAYERS"]:
        if not (
            x == status["NOM1"]
            or x == status["NOM2"]
            or x == status["HOH"]
            or len(status["PLAYERS"]) <= 4
        ):
            vote = reverse_comparison(x, nom1, nom2)
            votes[vote] += 1
            print(f"{purple}{x}{end} has voted for {red}{vote}{end}")
            time.sleep(timer)
            print("-------------------")
            time.sleep(timer)
    if len(status["PLAYERS"]) == 3:
        print(
            f"{yellow}{italics}{status['HOH']}{end} {italics}walks to the front of the room{end}"
        )
        time.sleep(timer)
        print(
            f"As the final head of household, it is my decision on who I bring to finale night"
        )
        time.sleep(timer)
        print(f"I am a loyal player, I will be taking the player I like more.")
        time.sleep(timer)
        status["EVICTED"] = reverse_comparison(hoh, nom1, nom2)
        print(f"for that reason I must vote to {red}evict...{end}")
        time.sleep(timer)
        print("...")
        time.sleep(timer)
        print(f"{red}{bold}{status['EVICTED']}{end}")
        print()
        time.sleep(timer)
    elif len(status["PLAYERS"]) == 4:
        print(
            f"{purple}{status['VOTER']}{end} {italics}walks to the front of the room{end}"
        )
        status["EVICTED"] = reverse_comparison(status["VOTER"], nom1, nom2)
        time.sleep(timer)
        print(
            "I need to carve my path to the end of the game, so I have to do what's best for me"
        )
        time.sleep(timer)
        print(f"For this reason, I vote to {red}evict{end}...")
        time.sleep(timer)
        print("...")
        time.sleep(timer)
        print(f"{red}{status['EVICTED']}{end}")
        time.sleep(timer)
    else:
        print(
            f"By a vote of {red}{bold}{votes[nom1]}{end} to {red}{bold}{votes[nom2]}{end}"
        )
        time.sleep(timer)
        if votes[nom1] > votes[nom2]:
            status["EVICTED"] = nom1
        elif votes[nom2] > votes[nom1]:
            status["EVICTED"] = nom2
        else:
            status["EVICTED"] = reverse_comparison(hoh, nom1, nom2)
            print(f"{bold}We have a tie!{end}")
            time.sleep(timer)
            print(f"{yellow}{hoh}{end} has voted for...")
            time.sleep(timer)
            print("...")
            time.sleep(timer)
            print(f"{red}{bold}{status['EVICTED']}{end}")
            time.sleep(timer)
    print(
        f"{italics}{red}{status['EVICTED']} you have been evicted from the {underline}Big Python{end} {red}{italics}house.{end}"
    )
    time.sleep(timer)
    status = end_week(status)
    return status


def game_logic(status):
    while len(status["PLAYERS"]) > 2:
        if len(status["PLAYERS"]) >= 3:
            status = hoh_comp(status)
            status = nomination_ceremony(status)
            if len(status["PLAYERS"]) >= 4:
                status = veto_pick(status)
                status = veto_comp(status)
                status = veto_ceremony(status)
            status = vote_time(status)
    finale_night(status)
    print("WE FINISHED THE GAME")
    return status


def end_week(status):
    if len(status["PLAYERS"]) <= juror_count + 2:
        status["JURY"][status["EVICTED"]] = status["PLAYERS"][status["EVICTED"]]
    elif len(status["PLAYERS"]) >= juror_count + 2:
        status["PREJURY"][status["EVICTED"]] = status["PLAYERS"][status["EVICTED"]]

    del status["PLAYERS"][status["EVICTED"]]
    for x in status["PLAYERS"]:
        del status["PLAYERS"][x]["relations"][status["EVICTED"]]
    status["POVPLAYER1"] = "empty"
    status["POVPLAYER2"] = "empty"
    status["POVPLAYER3"] = "empty"
    status["WEEKNUM"] += 1
    return status


def finale_night(status):
    print(f"{yellow}------------------")
    print(f"---{bold}FINALE NIGHT{end}{yellow}---")
    print(f"------------------{end}")
    finalists = []
    for x in status["PLAYERS"]:
        finalists += [x]
    print(f"{bold}WELCOME TO FINALE NIGHT EVERYONE!{end}")
    print(
        f"{purple}{finalists[0]}{end}, {purple}{finalists[1]}{end}, you have made it as far as you can in this game"
    )
    print(f"We would do {purple}jury{end} questions, but who has time for that?")
    print(f"LETS VOTE FOR THE {yellow}WINNER{end} BABY")
    votecount = {finalists[0]: 0, finalists[1]: 0}
    jover = False
    for i in status["JURY"]:
        vote = comparison(i, finalists[0], finalists[1], "JURY")
        votecount[vote] += 1
        if not jover:
            print(f"{purple}{i}{end} has voted for...")
            print("...")
            if votecount[vote] == 4:
                print(f"{yellow}{italics}{bold}THE WINNER OF BIG PYTHON...{end}")
                print(f"{yellow}{bold}{vote}!!!!{end}")
                status["WINNER"] = vote
                jover = True
            elif not jover:
                print(f"{yellow}{bold}{vote}{end}!")
                print(
                    f"That's {bold}{votecount[finalists[0]]}{end} votes {purple}{finalists[0]}{end}, {bold}{votecount[finalists[1]]}{end} votes {purple}{finalists[1]}{end}."
                )
    print()
    print(
        f"The final vote count was {bold}{votecount[finalists[0]]}{end} votes {purple}{finalists[0]}{end}, {bold}{votecount[finalists[1]]}{end} votes {purple}{finalists[1]}{end}."
    )


def reset_status(status):
    status["comps_left"] = [] + comp_types
    status["comp_types"] = [] + comp_types
    status["PLAYERS"] = temp_players
    status["WEEKNUM"] = 1
    status["JURY"] = {}
    status["PREJURY"] = {}


# players = {"Matty":{'relations':{}, 'compability':{}},
#            "Owen":{'relations':{}, 'compability':{}},
#            "Trent":{'relations':{}, 'compability':{}},
#            "Caine":{'relations':{}, 'compability':{}},
#            "Preston":{'relations':{}, 'compability':{}},
#            "TJ":{'relations':{}, 'compability':{}},
#            "Yvonne":{'relations':{}, 'compability':{}},
#            "Zay":{'relations':{}, 'compability':{}},
#            "Luz":{'relations':{}, 'compability':{}},
#            "Hope":{'relations':{}, 'compability':{}},
#            "Blaze":{'relations':{}, 'compability':{}},
#            "Moxie":{'relations':{}, 'compability':{}}}
comp_types = [
    "Physical",
    "Mental",
    "Endurance",
    "Memory",
    "Special",
    "Silly",
    "Luck",
    "Embarrassing",
    "Spelling",
    "Social",
    "Clutch",
]

playernames = [
    "Angela",
    "DJ",
    "Jason",
    "Carmen",
    "Greg",
    "Kevin",
    "Will",
    "Andy",
    "Hannah",
    "Cole",
    "Reuben",
    "Hillary Clinton",
    "JPZ",
    "Kamila",
    "Misa",
    "Nicole",
    "Anuva",
    "Trevor",
    "Anuva",
    "Alex",
    "Diaz",
    "Nate",
    "Ashley",
]

temp_players = {}
for x in playernames:
    temp_players[x] = {"relations": {}, "compability": {}}
    for y in playernames:
        if not x == y:
            temp_players[x]["relations"][y] = random.randrange(1, 50)
    for y in comp_types:
        temp_players[x]["compability"][y] = random.randrange(1, 50)

status = {
    "PLAYERS": {
        "Matty": {
            "relations": {
                "Owen": 3,
                "Trent": 9,
                "Caine": 8,
                "Preston": 6,
                "TJ": 6,
                "Yvonne": 10,
                "Zay": 10,
                "Luz": 6,
                "Hope": 1,
                "Blaze": 7,
                "Moxie": 8,
            },
            "compability": {
                "Physical": 3,
                "Mental": 8,
                "Endurance": 7,
                "Memory": 3,
                "Special": 2,
                "Silly": 4,
                "Luck": 3,
                "Embarrassing": 4,
                "Spelling": 9,
                "Social": 9,
                "Clutch": 6,
            },
        },
        "Owen": {
            "relations": {
                "Matty": 5,
                "Trent": 7,
                "Caine": 10,
                "Preston": 2,
                "TJ": 2,
                "Yvonne": 6,
                "Zay": 2,
                "Luz": 1,
                "Hope": 7,
                "Blaze": 9,
                "Moxie": 7,
            },
            "compability": {
                "Physical": 7,
                "Mental": 4,
                "Endurance": 9,
                "Memory": 5,
                "Special": 1,
                "Silly": 8,
                "Luck": 4,
                "Embarrassing": 3,
                "Spelling": 4,
                "Social": 6,
                "Clutch": 6,
            },
        },
        "Trent": {
            "relations": {
                "Matty": 10,
                "Owen": 3,
                "Caine": 1,
                "Preston": 9,
                "TJ": 9,
                "Yvonne": 5,
                "Zay": 1,
                "Luz": 5,
                "Hope": 6,
                "Blaze": 2,
                "Moxie": 1,
            },
            "compability": {
                "Physical": 9,
                "Mental": 5,
                "Endurance": 10,
                "Memory": 7,
                "Special": 2,
                "Silly": 5,
                "Luck": 10,
                "Embarrassing": 4,
                "Spelling": 6,
                "Social": 7,
                "Clutch": 6,
            },
        },
        "Caine": {
            "relations": {
                "Matty": 6,
                "Owen": 7,
                "Trent": 6,
                "Preston": 1,
                "TJ": 2,
                "Yvonne": 7,
                "Zay": 1,
                "Luz": 8,
                "Hope": 9,
                "Blaze": 7,
                "Moxie": 3,
            },
            "compability": {
                "Physical": 5,
                "Mental": 4,
                "Endurance": 4,
                "Memory": 6,
                "Special": 7,
                "Silly": 1,
                "Luck": 9,
                "Embarrassing": 1,
                "Spelling": 3,
                "Social": 1,
                "Clutch": 7,
            },
        },
        "Preston": {
            "relations": {
                "Matty": 4,
                "Owen": 6,
                "Trent": 1,
                "Caine": 9,
                "TJ": 1,
                "Yvonne": 7,
                "Zay": 5,
                "Luz": 6,
                "Hope": 9,
                "Blaze": 10,
                "Moxie": 6,
            },
            "compability": {
                "Physical": 4,
                "Mental": 8,
                "Endurance": 7,
                "Memory": 1,
                "Special": 6,
                "Silly": 6,
                "Luck": 6,
                "Embarrassing": 1,
                "Spelling": 9,
                "Social": 4,
                "Clutch": 2,
            },
        },
        "TJ": {
            "relations": {
                "Matty": 4,
                "Owen": 5,
                "Trent": 7,
                "Caine": 3,
                "Preston": 3,
                "Yvonne": 10,
                "Zay": 9,
                "Luz": 5,
                "Hope": 6,
                "Blaze": 8,
                "Moxie": 4,
            },
            "compability": {
                "Physical": 8,
                "Mental": 10,
                "Endurance": 1,
                "Memory": 5,
                "Special": 9,
                "Silly": 4,
                "Luck": 7,
                "Embarrassing": 5,
                "Spelling": 8,
                "Social": 1,
                "Clutch": 8,
            },
        },
        "Yvonne": {
            "relations": {
                "Matty": 7,
                "Owen": 3,
                "Trent": 10,
                "Caine": 6,
                "Preston": 7,
                "TJ": 8,
                "Zay": 6,
                "Luz": 1,
                "Hope": 4,
                "Blaze": 4,
                "Moxie": 4,
            },
            "compability": {
                "Physical": 4,
                "Mental": 7,
                "Endurance": 9,
                "Memory": 6,
                "Special": 10,
                "Silly": 3,
                "Luck": 2,
                "Embarrassing": 4,
                "Spelling": 3,
                "Social": 2,
                "Clutch": 1,
            },
        },
        "Zay": {
            "relations": {
                "Matty": 1,
                "Owen": 7,
                "Trent": 5,
                "Caine": 7,
                "Preston": 6,
                "TJ": 1,
                "Yvonne": 10,
                "Luz": 8,
                "Hope": 10,
                "Blaze": 6,
                "Moxie": 1,
            },
            "compability": {
                "Physical": 4,
                "Mental": 2,
                "Endurance": 1,
                "Memory": 8,
                "Special": 4,
                "Silly": 4,
                "Luck": 5,
                "Embarrassing": 7,
                "Spelling": 5,
                "Social": 7,
                "Clutch": 8,
            },
        },
        "Luz": {
            "relations": {
                "Matty": 7,
                "Owen": 5,
                "Trent": 8,
                "Caine": 6,
                "Preston": 1,
                "TJ": 3,
                "Yvonne": 8,
                "Zay": 4,
                "Hope": 3,
                "Blaze": 4,
                "Moxie": 7,
            },
            "compability": {
                "Physical": 9,
                "Mental": 10,
                "Endurance": 7,
                "Memory": 3,
                "Special": 7,
                "Silly": 6,
                "Luck": 7,
                "Embarrassing": 9,
                "Spelling": 1,
                "Social": 8,
                "Clutch": 6,
            },
        },
        "Hope": {
            "relations": {
                "Matty": 8,
                "Owen": 7,
                "Trent": 1,
                "Caine": 9,
                "Preston": 6,
                "TJ": 8,
                "Yvonne": 5,
                "Zay": 9,
                "Luz": 3,
                "Blaze": 6,
                "Moxie": 5,
            },
            "compability": {
                "Physical": 9,
                "Mental": 3,
                "Endurance": 2,
                "Memory": 1,
                "Special": 10,
                "Silly": 3,
                "Luck": 10,
                "Embarrassing": 8,
                "Spelling": 7,
                "Social": 1,
                "Clutch": 9,
            },
        },
        "Blaze": {
            "relations": {
                "Matty": 2,
                "Owen": 7,
                "Trent": 5,
                "Caine": 2,
                "Preston": 7,
                "TJ": 7,
                "Yvonne": 10,
                "Zay": 3,
                "Luz": 9,
                "Hope": 10,
                "Moxie": 6,
            },
            "compability": {
                "Physical": 9,
                "Mental": 7,
                "Endurance": 7,
                "Memory": 10,
                "Special": 9,
                "Silly": 3,
                "Luck": 4,
                "Embarrassing": 3,
                "Spelling": 2,
                "Social": 7,
                "Clutch": 9,
            },
        },
        "Moxie": {
            "relations": {
                "Matty": 3,
                "Owen": 2,
                "Trent": 6,
                "Caine": 7,
                "Preston": 3,
                "TJ": 5,
                "Yvonne": 1,
                "Zay": 7,
                "Luz": 3,
                "Hope": 6,
                "Blaze": 3,
            },
            "compability": {
                "Physical": 3,
                "Mental": 3,
                "Endurance": 2,
                "Memory": 2,
                "Special": 3,
                "Silly": 3,
                "Luck": 2,
                "Embarrassing": 6,
                "Spelling": 6,
                "Social": 8,
                "Clutch": 3,
            },
        },
    },
    "JURY": {},
    "PREJURY": {},
    "HOH": "empty",
    "NOM1": "empty",
    "NOM2": "empty",
    "POV": "empty",
    "POVPLAYER1": "empty",
    "POVPLAYER2": "empty",
    "POVPLAYER3": "empty",
    "USAGE": "empty",
    "RENOM": "empty",
    "EVICTED": "empty",
    "WEEKNUM": 1,
    "VOTER": "empty",
    "WINNER": "empty",
    "comps_left": [
        "Physical",
        "Mental",
        "Endurance",
        "Memory",
        "Special",
        "Silly",
        "Luck",
        "Embarrassing",
        "Spelling",
        "Social",
        "Clutch",
    ],
    "comp_types": [
        "Physical",
        "Mental",
        "Endurance",
        "Memory",
        "Special",
        "Silly",
        "Luck",
        "Embarrassing",
        "Spelling",
        "Social",
        "Clutch",
    ],
}
winlist = {}


# for i in range(100):
#     temp_players = {}
#     for x in playernames:
#         temp_players[x] = {"relations": {}, "compability": {}}
#         for y in playernames:
#             if not x == y:
#                 temp_players[x]["relations"][y] = random.randrange(1, 50)
#         for y in comp_types:
#             temp_players[x]["compability"][y] = random.randrange(1, 50)
#     reset_status(status)
#     temp = game_logic(status)
#     if temp["WINNER"] in winlist:
#         winlist[temp["WINNER"]] = winlist[temp["WINNER"]] + 1
#     else:
#         winlist[temp["WINNER"]] = 1
# print(winlist)

reset_status(status)
game_logic(status)
# status = {'HOH':"empty", "NOM1":"empty", "NOM2":'empty', "POV":"empty", "POVPLAYER1":"empty", "POVPLAYER2":"empty", "POVPLAYER3":"empty"}


# list_of_players = []
# for x in status["PLAYERS"]:
#     list_of_players = list_of_players + [x]
