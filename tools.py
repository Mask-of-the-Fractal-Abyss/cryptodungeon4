import random

letters = "abcdefghijklmnopqrstuvwxyz"


# Generates a random code of length codeClass.codeLen
def genCode():
    code = ""
    for _ in range(codeClass.codeLen):
        code += random.choice(letters)
    return code


# Ensures the code has not already been created.
def genUniqueCode():
    code = genCode()
    while code in codeClass.codes:
        code = genCode()
    return code


# Find a monster type from monsterClass.monsterTypes, through the String name of the type
def searchMonsterTypesByName(name):
    for monsterType in monsterClass.monsterTypes:
        if monsterType.name == name:
            return monsterType
    return None


# Generate a random, vaguely-pronounceable word.
def generateRandomName(length=3):
    vowels = "aeiou"
    name = ""
    for _ in range(random.randint(1, length)):
        name += random.choice(letters)
        name += random.choice(vowels)
    if bool(random.randint(0, 1)):
        name += random.choice(letters)
    if len(name) == 2 and bool(random.randint(0, 10)):
        name += random.choice(letters)
    return name


# Generates random unicode symbol to use as display symbol in the room.
def unicodeChar():
    exoticChars = 800

    # Banlist blocks stupid unicode chars (like spaces and inconsistent length ones, etc.)
    banList = ["\n", " ", "\t", "\r"]
    for i in range(len(banList)):
        banList[i] = ord(banList[i])
    banList += [4, 21, 127, 128, 149, 17, 26, 2, 144]

    randomChar = random.randint(0, exoticChars)
    while randomChar in banList or chr(randomChar).isspace():
        randomChar = random.randint(0, exoticChars)
    return chr(randomChar).ljust(len(roomClass.emptyChar))


def searchRoomsByCode(code):
    for room in roomClass.rooms:
        if room.code.code == code:
            return room
    return None


def createPlayer():
    validName = False
    playerName = None
    while not validName:
        playerName = input("Enter your name")
        if len(playerName) < 1:
            print("Whoops, that's not a real name! :/")
        else:
            validName = True
    assert playerName is not None, "Oops, something went wrong :/"
    return playerClass(playerName)


# Class representing a unique String used to identify each room
class codeClass:
    codes = []
    codeLen = 3

    def __init__(self):
        self.code = genUniqueCode()
        codeClass.codes.append(self.code)


# Class which holds monsters and other objects, which the player can move around in
class roomClass:
    minRoomSize = 3
    maxRoomSize = 20
    rooms = []
    spaceChar = " "
    emptyChar = " "

    def __init__(self):
        self.size = random.randint(roomClass.minRoomSize, roomClass.maxRoomSize)
        while self.size % 2 != 1:
            self.size = random.randint(roomClass.minRoomSize, roomClass.maxRoomSize)
        self.contents = [[] for _ in range(self.size)]
        self.code = codeClass()
        self.populateRoom()
        self.playerHere = []
        roomClass.rooms.append(self)

    def printRoom(self):
        print("\n ".ljust(
            int(len(self.contents)) * int(
                len(roomClass.spaceChar) / 2)) + self.code.code.upper())  # Centering room code
        for x in self.contents:
            row = ""
            for y in x:
                if y is not None:
                    row += y.symbol + roomClass.spaceChar
                else:
                    row += roomClass.emptyChar + roomClass.spaceChar
            print(row.ljust(len(self.contents * len(roomClass.spaceChar))))

    def populateRoom(self):
        for x in self.contents:
            for y in range(self.size):
                if not bool(random.randint(0, 5)):
                    x.append(monsterClass(self))
                else:
                    x.append(None)


# Monsters which can inhabit rooms and attack players, etc.
class monsterClass:
    healthMin = 1
    healthMax = 10
    rarityMax = 5
    monsterTypes = []  # Stores types of monsters previously generated
    monsterVariety = 5

    def __init__(self, room, name=None):
        self.room = room
        if name is None:
            if not bool(random.randint(0, monsterClass.monsterVariety)) or len(monsterClass.monsterTypes) == 0:  # Generate a new monster type
                self.name = generateRandomName()
                self.rarity = random.randint(0, monsterClass.rarityMax)
                self.health = random.randint(monsterClass.healthMin, monsterClass.healthMax + self.rarity)
                self.symbol = unicodeChar()
                self.contents = [itemClass() for _ in range(random.randint(0, self.rarity))]

                monsterClass.monsterTypes.append(self)  # Add the new monster type to the list of all monster types
            else:
                monsterType = random.choice(monsterClass.monsterTypes)  # Copy a random monster type
                self.copyAttributes(monsterType)
        else:
            monsterType = searchMonsterTypesByName(name)  # Create a specific monster type is name is specified
            self.copyAttributes(monsterType)

    # Method to abstract the creation of monsters
    def copyAttributes(self, monsterType):
        self.name = monsterType.name
        self.health = monsterType.health
        self.symbol = monsterType.symbol
        self.rarity = monsterType.rarity
        self.contents = []
        if len(monsterType.contents) > 0:  # Makes it so some of the new monster's items are the same as the "parent" monster
            halfLength = int(len(monsterType.contents) / 2)
            self.contents = monsterType.contents[:halfLength] + [itemClass for _ in range(random.randint(0, halfLength))]


# Class for player, stores health, items, etc.
class playerClass:
    def __init__(self, name):
        self.name = name
        self.symbol = name[0].upper()
        self.health = 10
        self.room = None
        self.coords = []
        self.speed = 1
        self.contents = []
        self.weapon = weaponClass()

    # Low abstraction method to move player in their room
    def move(self, direction):
        y = self.coords[0]
        x = self.coords[1]
        speed = self.speed
        roomContents = self.room.contents

        # DirectionalKey abstracts movement and attack methods, containing the change in coordinates and edge detection
        directionalKey = {"n": [-speed, 0, y > speed - 1],
                          "e": [0, speed, x < len(roomContents) - speed],
                          "s": [speed, 0, y < len(roomContents) - speed],
                          "w": [0, -speed, x > speed - 1]}
        targetSquare = directionalKey[direction]
        if targetSquare[2]:
            target = roomContents[y + targetSquare[0]][x + targetSquare[1]]
            if target is None:
                roomContents[y + targetSquare[0]][x + targetSquare[1]] = self
                roomContents[y][x] = None
                self.coords[0] += targetSquare[0]
                self.coords[1] += targetSquare[1]

    # Method for attacking monster in room
    def attack(self, direction, showRoom=False):
        y = self.coords[0]
        x = self.coords[1]
        weapon = self.weapon
        weaponRange = weapon.range
        roomContents = self.room.contents

        # DirectionalKey abstracts movement and attack methods, containing the change in coordinates and edge detection
        directionalKey = {"n": [-weaponRange, 0, y > weaponRange - 1],
                          "e": [0, weaponRange, x < len(roomContents) - weaponRange],
                          "s": [weaponRange, 0, y < len(roomContents) - weaponRange],
                          "w": [0, -weaponRange, x > weaponRange - 1]}
        targetSquare = directionalKey[direction]
        if weapon.range > 0 and targetSquare[2]:
            target = roomContents[y + targetSquare[0]][x + targetSquare[1]]
            if target is not None:
                target.health -= weapon.damage
                if target.health < 1:
                    roomContents[y + targetSquare[0]][x + targetSquare[1]] = None
        else:
            weaponRange = 1
            directionalKey = {"n": [-weaponRange, 0],
                              "e": [0, weaponRange],
                              "s": [weaponRange, 0],
                              "w": [0, -weaponRange]}
            targetSquare = directionalKey[direction]
            target = roomContents[y + targetSquare[0]][x + targetSquare[1]]
            if target is not None:
                target.health -= weapon.damage
                self.health -= target.health
                roomContents[y][x] = None
                roomContents[y + targetSquare[0]][x + targetSquare[1]] = self
                self.coords = [y + targetSquare[0], x + targetSquare[1]]
        if showRoom and roomContents[y + targetSquare[0]][x + targetSquare[1]] is not None:
            player.room.printRoom()
            print(f"HEALTH: {player.health}")
            print(f"{target.name.capitalize()}: {target.health}")

    # Checks if player is in an edge space of their room
    @property
    def onEdge(self):
        if self.coords[0] == self.room.size - 1 or self.coords[1] == self.room.size - 1 or self.coords[0] == 0 or self.coords[1] == 0:
            return True
        return False

    def leave(self):
        self.room = None
        self.health -= 1
        self.coords = []
        print("Successfully left the room")

    def checkStats(self):
        weapon = self.weapon
        print(f"""
HEALTH      : {self.health}
SPEED       : {self.speed}
WEAPON      : {weapon.name.capitalize()}
 - ATTACK   : {weapon.damage}
 - RANGE    : {weapon.range}
""")


# Items which can be picked up and used by the player
class itemClass:
    def __init__(self, power=None):
        if power is None:
            power = random.randint(2, 10)
        self.name = generateRandomName(int(power / 3) + 2)
        self.symbol = unicodeChar()


# Predetermined weapons
class weaponClass:
    def __init__(self):
        self.name = generateRandomName()
        self.range = random.randint(0, 3)
        self.damage = random.randint(0, 3)
        self.symbol = unicodeChar()


player = createPlayer()  # Includes free code
