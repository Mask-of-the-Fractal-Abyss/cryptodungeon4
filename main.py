from playerCommands import *

codeClass.codeLen = 2  # Setting the length of the codes to 3
assert codeClass.codeLen > 1, "Yikes! Codes must be longer than 1 character!"
roomFindChance = 50 / 100
roomClass.spaceChar = "  "  # The char between spaces in a room when it's printed
roomClass.emptyChar = "-"  # The char in an empty room space
roomClass.maxRoomSize = 10  # Minsize is 3
monsterClass.monsterVariety = 1000  # Inverse relationship with the chance to create a new monster type

# Creates a number of rooms proportional to the code length and designated chance to find rooms.
numberOfRooms = int(roomFindChance * 26 ** codeClass.codeLen)
for _ in range(numberOfRooms):
    roomClass()

print(f"Here is your free code, use it wisely...\n{random.choice(roomClass.rooms).code.code}")

while player.health > 0:
    action = input("Search for code?").lower()
    if len(action) == codeClass.codeLen and " " not in action:
        search(action)  # Searches for desired code
    elif len(action) == 3:
        if action[0] == "m":
            move(action[2])  # Moves player in their room
        elif action[0] == "a":
            attack(action[2])  # Player attacks in their room
    elif action == "l":
        if player.onEdge:
            player.leave()
        else:
            print("You must be on the edge of the room to leave.")
    elif action == "stats":
        player.checkStats()

