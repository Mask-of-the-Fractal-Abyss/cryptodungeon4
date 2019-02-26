from tools import *


# Player searches for desired code
def search(codeToSearch):
    if player.room is None:
        if codeToSearch in codeClass.codes:
            room = searchRoomsByCode(codeToSearch)
            middle = int(room.size / 2)
            room.contents[middle][middle] = player
            player.coords = [middle, middle]
            player.room = room
            room.printRoom()
    else:
        print("You must leave your current room to search.")


# Moves the player in their room
def move(direction):
    if player.room is not None:
        if direction in "nesw":
            player.move(direction)
            player.room.printRoom()
        else:
            print("That's not a direction.  Try: N, S, E, W...\n")
    else:
        print("You must be in a room to move...\n")


# Player attacks in their room
def attack(direction):
    if player.room is not None:
        if player.weapon is not None:
            if direction in "nesw":
                player.attack(direction, True)
            else:
                print("That's not a direction.  Try: N, S, E, W")
        else:
            print("You must have a weapon to attack")
    else:
        print("You must be in a room to move")
