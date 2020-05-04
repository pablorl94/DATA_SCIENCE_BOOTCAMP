"""
     --  MONTY HALL'S PROBLEM  --

A small app to simulate Monty Hall's Problem.

Imagine you are in a contest. There are three doors in front of you, one of
them hides a lot of money. The others hide a goat and a sheep. You have to 
choose carefully to select the correct one.

After your election, the presenter open a door with an animal. In that moment,
he gives you the opportunity to change your door with the one which is still
closed. What will you do? Will you retain your door or maybe change it?

Monty Hall's Problem is a good exercise to check why probabistic is as
important when analyzing situations where common sense may not be right.
"""

from random import shuffle
from time import sleep

def print_header():
    """Print application's header."""
    print("""

 __       __                        __                      __    __            __  __ 
/  \     /  |                      /  |                    /  |  /  |          /  |/  |
$$  \   /$$ |  ______   _______   _$$ |_    __    __       $$ |  $$ |  ______  $$ |$$ |
$$$  \ /$$$ | /      \ /       \ / $$   |  /  |  /  |      $$ |__$$ | /      \ $$ |$$ |
$$$$  /$$$$ |/$$$$$$  |$$$$$$$  |$$$$$$/   $$ |  $$ |      $$    $$ | $$$$$$  |$$ |$$ |
$$ $$ $$/$$ |$$ |  $$ |$$ |  $$ |  $$ | __ $$ |  $$ |      $$$$$$$$ | /    $$ |$$ |$$ |
$$ |$$$/ $$ |$$ \__$$ |$$ |  $$ |  $$ |/  |$$ \__$$ |      $$ |  $$ |/$$$$$$$ |$$ |$$ |
$$ | $/  $$ |$$    $$/ $$ |  $$ |  $$  $$/ $$    $$ |      $$ |  $$ |$$    $$ |$$ |$$ |
$$/      $$/  $$$$$$/  $$/   $$/    $$$$/   $$$$$$$ |      $$/   $$/  $$$$$$$/ $$/ $$/ 
                                           /  \__$$ |                                  
                                           $$    $$/                                   
                                            $$$$$$/                                    

    """)

def initialize_draw():
    """Distribute randomly the awards behind the doors."""
    print("The draw has been done so it's time to start the game. Will you find the money?", end="\n\n")
    sleep(3)
    awards = ["MONEY", "GOAT", "SHEEP"]
    shuffle(awards)
    return {1: awards[0], 2:awards[1], 3: awards[2]}

def select_door():
    """Ask the contestant to choose a door."""
    while True:
        election = input(">> Choose the number of the door you want to keep (1, 2 or 3): ")
        print()
        sleep(1)
        if election not in ["1", "2", "3"]:
            print("Remember, only numbers 1, 2 and 3 are available. Please, try again.", end="\n\n")
            sleep(2)
        else:
            print(f"You have selected the door number {election}.", end="\n\n")
            sleep(2)
            return int(election)

def drop_door(player_door, doors):
    """Drop one of the remaining doors that have an animal."""
    empty_door = [i for i in doors if (i != player_door) and (doors[i] != "MONEY")][0]
    print(f"We're going to open a door. Let's see for example door number {empty_door}...", end="\n\n")
    sleep(2)
    print("...", end="\n\n")
    sleep(2)
    print(f"The door number {empty_door} is not empty... We've find a {doors[empty_door].lower()}!", end="\n\n")
    sleep(2)
    return empty_door

def change_door(player_door, empty_door, doors):
    """Ask the contestant to change his door."""
    last_door = [i for i in doors if (i != player_door) and (i != empty_door)][0]
    print(f"So you have the door {player_door} selected but the door {last_door} is still here.", end="\n\n")
    sleep(1)
    while True:
        election = input(">> Do you want to change them? Select YES/NO: ")
        print()
        sleep(1)
        if election.upper() not in ["Y", "YES", "N", "NO"]:
            print("Remember, only YES/Y and NO/N. Please, try again.", end="\n\n")
        else:
            if election.upper() in ["Y", "YES"]:
                print("You have selected to change your door.", end="\n\n")
                sleep(2)
                final_door = last_door
            else:
                print("You have selected not to change your door.", end="\n\n")
                sleep(2)
                final_door = player_door
            
            print(f"So finally you have selected the door number {final_door}.", end="\n\n")
            sleep(2)
            return final_door

def end_contest(final_door, doors):
    """Check the result of the contest."""
    print("Let's see what's behind your door...", end="\n\n")
    sleep(2)
    print("...", end="\n\n")
    sleep(2)
    print("<The presenter opened the door.>", end="\n\n")
    sleep(2)
    if doors[final_door] == "MONEY":
        print("<Something is shining behind your door. The money is there!!!>", end="\n\n")
        sleep(2)
        print("Congratulations! You've won the game :)", end="\n\n")
    else:
        print(f"<A stinky {doors[final_door].lower()} appeared behind the door.>", end="\n\n")
        sleep(2)
        print("Oh, Im sorry. You've lost :(", end="\n\n")

def main():
    """The main function to run the application."""
    print_header()
    doors = initialize_draw()
    player_door = select_door()
    empty_door = drop_door(player_door, doors)
    final_door = change_door(player_door, empty_door, doors)
    end_contest(final_door, doors)

if __name__ == "__main__":
    main()