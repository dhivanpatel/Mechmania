# keep these three import statements
import game_API
import fileinput
import json
from datetime import datetime

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]
stanceindex = random.randint(0, 2)
oldushealth = 100
oldmonhealth = 4
newushealth = 0
newmonhealth = 0

def shiftLosing():
    global stanceindex
    result = 0
    if(stanceindex == 0):
        result = 2
    else:
        result = stanceindex - 1
    return result
        
def shiftNotLosing():
    global stanceindex
    result = 0
    if(stanceindex == 2):
        result = 0
    else:
        result = stanceindex + 1
    return result
        
def monster_damage():#return true if not expected damage and false if expected
    global oldmonhealth
    global newmonhealth
    global stanceindex
    tempmon = game.get_monster(me.location)
    newmonhealth = 0
    result = True
    if  game.has_monster(me.location) and (not tempmon.dead):
        newmonhealth = tempmon.health
        if(tempmon.stance == me.stance and oldmonhealth-1 == newmonhealth):
            result = False
        if(stances[shiftLosing()] == tempmon.stance):
            amount = oldmonhealth - newmonhealth
            if(stanceindex == 0 and amount == me.rock):
                result= False
            elif(stanceindex == 1 and amount == me.paper):
                result= False
            elif(stanceindex == 2 and amount == me.scissors):
                result= False
                
    oldmonhealth = newmonhealth
    return result
        
def check_opseen():
    global oldushealth
    global newushealth    
    tempmon = game.get_monster(me.location)
    newushealth = me.health
    x = 0
    exdamus = 0
    if  game.has_monster(me.location) and (not tempmon.dead):
        exdamus = tempmon.attack
    if((oldushealth - exdamus) != newushealth):
        if(oldushealth-exdamus-1 == newushealth):
            x = 1
        else:
            x = 2
    
    
    
    oldushealth = newushealth
    return x
#returns 0 if damage goes as expected, 1 if it is losing or tie case, and integer value greater than 1 if it is losing case
        
def get_winning_stance():
    global stanceindex
    if(check_opseen()!=0):
        if(check_opseen() == 1):
            stanceindex = shiftNotLosing()
        else:
            stanceindex = shiftLosing()
                       
    elif(monster_damage()):
        stanceindex-=1
        stanceindex+=1
    
    elif(game.has_monster(me.location)):
        stance = game.get_monster(me.location).stance
        if stance == "Rock":
            stanceindex = 1
        elif stance == "Paper":
            stanceindex = 2
        elif stance == "Scissors":
            stanceindex = 0
    return stances[stanceindex]

# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game

    me = game.get_self()

    if me.location == me.destination: # check if we have moved this turn
        # get all living monsters closest to me
        monster_tom_move_to = game.get_monster(0)
        count = 0
        if me.location == game.get_monster(me.location) and game.get_monster(me.location).dead == False:
            monster_tom_move_to = game.get_monster(me.location)
        else:
            if me.location == 0 and game.get_monster(1).dead == False:
                monster_tom_move_to = game.get_monster(1)
            elif me.location == 0 and game.get_monster(1).dead == True and game.get_monster(10).dead == False:
                monster_tom_move_to = game.get_monster(10)
            elif game.get_monster(0).dead == False:
                monster_tom_move_to = game.get_monster(0)
            elif me.location == 1 and game.get_monster(3).dead == False:
                monster_tom_move_to = game.get_monster(3)
            elif me.location == 3:
                monster_tom_move_to = game.get_monster(1)
            elif me.location == 10 and game.get_monster(16).dead == False:
                monster_tom_move_to = game.get_monster(16)
            elif me.location == 16:
                monster_tom_move_to = game.get_monster(10)

        # get the set of shortest paths to that monster
        paths = game.shortest_paths(me.location, monster_tom_move_to.location)
        destination_node = paths[random.randint(0, len(paths) - 1)][0]
    else:
        destination_node = me.destination

    chosen_stance = get_winning_stance()
#    if game.has_monster(me.location):
        # if there's a monster at my location, choose the stance that damages that monster
#        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
#    else:
        # otherwise, pick a random stance
#        chosen_stance = stances[random.randint(0, 2)]

    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)
