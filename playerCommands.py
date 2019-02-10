from tools import *


# Player searches for desired code
def search(codeToSearch):
    if codeToSearch in codeClass.codes:
        room = searchRoomsByCode(codeToSearch)
        room.contents[0][0] = player
        player.coords = [0, 0]
        player.room = room
        room.printRoom()


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
        if player.getWeapon() is not None:
            if direction in "nesw":
                player.attack(direction, True)
            else:
                print("That's not a direction.  Try: N, S, E, W")
        else:
            print("You must have a weapon to attack")
    else:
        print("You must be in a room to move")
